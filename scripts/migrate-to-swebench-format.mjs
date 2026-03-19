import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const benchmarkRoot = path.join(repoRoot, "benchmark");

const splitDirs = [
  path.join(benchmarkRoot, "pilot_tasks"),
  path.join(benchmarkRoot, "tasks")
];

function cleanBlock(text) {
  return text
    .replace(/\r\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function parseMarkdownSections(text) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const sections = [];
  let currentTitle = null;
  let currentLines = [];
  let preambleLines = [];

  function flushSection() {
    if (currentTitle !== null) {
      sections.push({ title: currentTitle, body: cleanBlock(currentLines.join("\n")) });
    }
    currentTitle = null;
    currentLines = [];
  }

  for (const line of lines) {
    const headingMatch = line.match(/^#{1,6}\s+(.*)$/);
    if (headingMatch) {
      flushSection();
      currentTitle = headingMatch[1].trim();
      continue;
    }

    if (currentTitle === null) {
      preambleLines.push(line);
    } else {
      currentLines.push(line);
    }
  }

  flushSection();

  return {
    preamble: cleanBlock(preambleLines.join("\n")),
    sections
  };
}

function findSection(parsed, names) {
  const wanted = names.map((name) => name.toLowerCase());
  return parsed.sections.find((section) => wanted.includes(section.title.toLowerCase()))?.body ?? "";
}

function bodyToList(text) {
  if (!text) return [];
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.replace(/^[-*]\s+/, ""))
    .filter(Boolean);
}

function normalizePrompt(problemText) {
  const parsed = parseMarkdownSections(problemText);
  const prompt =
    findSection(parsed, ["User Prompt", "Prompt"]) ||
    (parsed.sections.length === 1 ? parsed.sections[0].body : "") ||
    parsed.preamble ||
    cleanBlock(problemText);

  return `${cleanBlock(prompt)}\n`;
}

function normalizeEnvironment(contextText) {
  const transformedText = contextText
    .replace(/\r\n/g, "\n")
    .replace(/^(?:#\s+Environment\s*\n\s*)+/i, "")
    .replace(/^(?:(?:##\s+(?:Environment|Context)\s*)\n\s*)+/i, "");

  if (/^#\s+Environment/i.test(contextText.trim())) {
    return `# Environment\n\n${cleanBlock(transformedText)}\n`;
  }

  const parsed = parseMarkdownSections(contextText);

  if (parsed.sections.length === 0) {
    return `# Environment\n\n${cleanBlock(contextText)}\n`;
  }

  const dropMatchers = [/^最小仕様$/i, /^評価/i, /^notes?$/i];
  const keepMatchers = [/context/i, /environment/i, /関連ファイル/i, /前提/i, /fixture/i, /evidence/i];

  const kept = parsed.sections.filter((section) => {
    if (dropMatchers.some((matcher) => matcher.test(section.title))) {
      return false;
    }
    if (keepMatchers.some((matcher) => matcher.test(section.title))) {
      return true;
    }
    return parsed.sections.length === 1;
  });

  const selected = kept.length > 0 ? kept : parsed.sections.slice(0, 1);
  if (
    selected.length === 1 &&
    /^(context|environment)$/i.test(selected[0].title)
  ) {
    const body = selected[0].body
      .replace(/^(?:(?:##\s+(?:Environment|Context)\s*)\n\s*)+/i, "");
    return `# Environment\n\n${cleanBlock(body)}\n`;
  }

  const blocks = selected.map((section) => {
    const title = section.title.toLowerCase() === "context" ? "Context" : section.title;
    return `## ${title}\n${section.body}`;
  });

  return `# Environment\n\n${cleanBlock(blocks.join("\n\n"))}\n`;
}

function normalizeGolden(answerText) {
  const parsed = parseMarkdownSections(answerText);
  const expected = findSection(parsed, ["Expected Outcome"]) || parsed.preamble;
  const minPass = findSection(parsed, ["Minimal Pass Line"]);
  const variants = findSection(parsed, ["Acceptable Variants"]);
  const failures = findSection(parsed, ["Common Failure Patterns"]);
  const notes = findSection(parsed, ["Notes For Evaluator"]);

  const parts = [];
  if (expected) parts.push(`# Accepted Fix\n\n${expected}`);
  if (minPass) parts.push(`# Minimum Pass\n\n${minPass}`);
  if (variants) parts.push(`# Acceptable Variants\n\n${variants}`);
  if (failures) parts.push(`# Common Failures\n\n${failures}`);
  if (notes) parts.push(`# Evaluator Notes\n\n${notes}`);

  return `${cleanBlock(parts.join("\n\n"))}\n`;
}

function parseSimpleYaml(text) {
  const result = {};
  let currentListKey = null;

  for (const rawLine of text.replace(/\r\n/g, "\n").split("\n")) {
    if (!rawLine.trim() || rawLine.trimStart().startsWith("#")) continue;

    const listMatch = rawLine.match(/^\s*-\s+(.*)$/);
    if (listMatch && currentListKey) {
      result[currentListKey].push(listMatch[1].trim().replace(/^"|"$/g, ""));
      continue;
    }

    const keyMatch = rawLine.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (!keyMatch) {
      currentListKey = null;
      continue;
    }

    const [, key, tail] = keyMatch;
    if (tail === "") {
      result[key] = [];
      currentListKey = key;
    } else {
      result[key] = tail.trim().replace(/^"|"$/g, "");
      currentListKey = null;
    }
  }

  return result;
}

function yamlList(lines, key, values) {
  lines.push(`${key}:`);
  for (const value of values) {
    lines.push(`  - "${String(value).replaceAll('"', '\\"')}"`);
  }
}

function buildEvalYaml(caseId, metaText, rubricText) {
  const meta = parseSimpleYaml(metaText);
  const rubric = parseMarkdownSections(rubricText);

  const scoringDimensions = bodyToList(findSection(rubric, ["Scoring Dimensions"]));
  const automaticChecks = bodyToList(findSection(rubric, ["Automatic Checks"])).map((line) =>
    line
      .replace(/`problem\.md`/g, "`prompt.txt`")
      .replace(/problem\.md/gi, "prompt.txt")
      .replace(/prompt\.txt に書かれた deliverable が揃っているか確認する。/g, "public prompt に対する提出物が揃っているか確認する。")
      .replace(/`prompt\.txt` に書かれた deliverable が揃っているか確認する。/g, "public prompt に対する提出物が揃っているか確認する。")
  );
  const hardFails = bodyToList(findSection(rubric, ["Hard Fail Conditions"]));
  const partialCredit = bodyToList(findSection(rubric, ["Partial Credit Rules"]));
  const acceptanceSignals = Array.isArray(meta.acceptance_alignment_signals) ? meta.acceptance_alignment_signals : [];
  const primaryMetrics = Array.isArray(meta.primary_metrics) ? meta.primary_metrics : [];
  const secondaryMetrics = Array.isArray(meta.secondary_metrics) ? meta.secondary_metrics : [];

  const lines = [
    `case_id: "${caseId}"`,
    `score_scale: "1-5"`,
    `benchmark_weight: ${meta.benchmark_weight ?? 1}`,
    `task_type: "${meta.task_type ?? ""}"`,
    `difficulty: "${meta.difficulty ?? ""}"`,
    `status: "${meta.status ?? ""}"`,
    `version: "${meta.version ?? ""}"`
  ];

  yamlList(lines, "scoring_dimensions", scoringDimensions);
  yamlList(lines, "automatic_checks", automaticChecks);
  yamlList(lines, "hard_fail_conditions", hardFails);
  yamlList(lines, "partial_credit_rules", partialCredit);
  yamlList(lines, "primary_metrics", primaryMetrics);
  yamlList(lines, "secondary_metrics", secondaryMetrics);
  yamlList(lines, "acceptance_alignment_signals", acceptanceSignals);

  return `${lines.join("\n")}\n`;
}

function listCaseRoots(rootDir) {
  return fs
    .readdirSync(rootDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(rootDir, entry.name))
    .sort((a, b) => a.localeCompare(b));
}

let rewrittenCases = 0;

for (const splitDir of splitDirs) {
  for (const caseRoot of listCaseRoots(splitDir)) {
    const publicDir = path.join(caseRoot, "public");
    const privateDir = path.join(caseRoot, "private");
    const sharedDir = path.join(caseRoot, "shared");

    const problemPath = path.join(publicDir, "problem.md");
    const contextPath = path.join(publicDir, "context.md");
    const promptPath = path.join(publicDir, "prompt.txt");
    const envPath = path.join(publicDir, "env.md");
    const answerPath = path.join(privateDir, "answer.md");
    const rubricPath = path.join(privateDir, "rubric.md");
    const goldenPath = path.join(privateDir, "golden.md");
    const evalPath = path.join(privateDir, "eval.yaml");
    const metaPath = path.join(sharedDir, "meta.yaml");

    const problemText = fs.readFileSync(problemPath, "utf8");
    const contextText = fs.readFileSync(contextPath, "utf8");
    const answerText = fs.readFileSync(answerPath, "utf8");
    const rubricText = fs.readFileSync(rubricPath, "utf8");
    const metaText = fs.readFileSync(metaPath, "utf8");
    const meta = parseSimpleYaml(metaText);

    const normalizedPrompt = normalizePrompt(problemText);
    const normalizedEnv = normalizeEnvironment(contextText);
    const normalizedGolden = normalizeGolden(answerText);
    const evalYaml = buildEvalYaml(meta.case_id ?? path.basename(caseRoot), metaText, rubricText);

    fs.writeFileSync(problemPath, normalizedPrompt, "utf8");
    fs.writeFileSync(promptPath, normalizedPrompt, "utf8");
    fs.writeFileSync(contextPath, normalizedEnv, "utf8");
    fs.writeFileSync(envPath, normalizedEnv, "utf8");
    fs.writeFileSync(goldenPath, normalizedGolden, "utf8");
    fs.writeFileSync(evalPath, evalYaml, "utf8");

    rewrittenCases += 1;
  }
}

console.log(`Refreshed ${rewrittenCases} cases into SWE-bench-style prompt/env/golden/eval surfaces.`);
