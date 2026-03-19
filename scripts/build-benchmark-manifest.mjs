import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const benchmarkRoot = path.join(repoRoot, "benchmark");
const publicDatasetRoot = path.join(benchmarkRoot, "public_dataset");

const splits = [
  { split: "pilot", dir: "pilot_tasks" },
  { split: "main", dir: "tasks" }
];

function parseScalar(raw) {
  const value = raw.trim();

  if ((value.startsWith("\"") && value.endsWith("\"")) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }

  if (value === "true") return true;
  if (value === "false") return false;

  if (/^-?\d+(\.\d+)?$/.test(value)) {
    return Number(value);
  }

  return value;
}

function parseSimpleYaml(text) {
  const result = {};
  let currentListKey = null;

  for (const rawLine of text.split(/\r?\n/)) {
    if (!rawLine.trim() || rawLine.trimStart().startsWith("#")) {
      continue;
    }

    const listMatch = rawLine.match(/^\s*-\s+(.*)$/);
    if (listMatch && currentListKey) {
      result[currentListKey].push(parseScalar(listMatch[1]));
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
      result[key] = parseScalar(tail);
      currentListKey = null;
    }
  }

  return result;
}

function listCaseDirs(rootDir) {
  return fs
    .readdirSync(rootDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort((a, b) => a.localeCompare(b));
}

const manifestEntries = [];
const privateManifestEntries = [];

fs.rmSync(publicDatasetRoot, { recursive: true, force: true });
fs.mkdirSync(publicDatasetRoot, { recursive: true });

for (const { split, dir } of splits) {
  const splitRoot = path.join(benchmarkRoot, dir);
  const caseDirs = listCaseDirs(splitRoot);
  const splitFile = path.join(benchmarkRoot, "splits", `${split}.txt`);
  fs.mkdirSync(path.dirname(splitFile), { recursive: true });
  fs.writeFileSync(splitFile, `${caseDirs.join("\n")}\n`, "utf8");

  const publicSplitFile = path.join(publicDatasetRoot, "splits", `${split}.txt`);
  fs.mkdirSync(path.dirname(publicSplitFile), { recursive: true });
  fs.writeFileSync(publicSplitFile, `${caseDirs.join("\n")}\n`, "utf8");

  for (const caseDir of caseDirs) {
    const caseRoot = path.join(splitRoot, caseDir);
    const metaPath = path.join(caseRoot, "shared", "meta.yaml");
    const meta = parseSimpleYaml(fs.readFileSync(metaPath, "utf8"));
    const sourcePromptPath = path.join(caseRoot, "public", "prompt.txt");
    const sourceEnvPath = path.join(caseRoot, "public", "env.md");
    const publicCaseRoot = path.join(publicDatasetRoot, dir, caseDir);
    const publicCasePublicRoot = path.join(publicCaseRoot, "public");

    fs.mkdirSync(publicCasePublicRoot, { recursive: true });
    fs.copyFileSync(sourcePromptPath, path.join(publicCasePublicRoot, "prompt.txt"));
    fs.copyFileSync(sourceEnvPath, path.join(publicCasePublicRoot, "env.md"));

    manifestEntries.push({
      case_id: meta.case_id,
      split,
      directory: path.relative(repoRoot, publicCaseRoot).replaceAll("\\", "/"),
      title: meta.title,
      task_type: meta.task_type,
      difficulty: meta.difficulty,
      benchmark_weight: meta.benchmark_weight,
      status: meta.status,
      version: meta.version,
      public_prompt: path.relative(repoRoot, path.join(publicCasePublicRoot, "prompt.txt")).replaceAll("\\", "/"),
      public_env: path.relative(repoRoot, path.join(publicCasePublicRoot, "env.md")).replaceAll("\\", "/")
    });

    privateManifestEntries.push({
      case_id: meta.case_id,
      split,
      directory: path.relative(repoRoot, caseRoot).replaceAll("\\", "/"),
      title: meta.title,
      task_type: meta.task_type,
      difficulty: meta.difficulty,
      benchmark_weight: meta.benchmark_weight,
      status: meta.status,
      version: meta.version,
      public_prompt: path.relative(repoRoot, sourcePromptPath).replaceAll("\\", "/"),
      public_env: path.relative(repoRoot, sourceEnvPath).replaceAll("\\", "/"),
      private_golden: path.relative(repoRoot, path.join(caseRoot, "private", "golden.md")).replaceAll("\\", "/"),
      private_eval: path.relative(repoRoot, path.join(caseRoot, "private", "eval.yaml")).replaceAll("\\", "/"),
      legacy_problem: path.relative(repoRoot, path.join(caseRoot, "public", "problem.md")).replaceAll("\\", "/"),
      legacy_context: path.relative(repoRoot, path.join(caseRoot, "public", "context.md")).replaceAll("\\", "/"),
      legacy_answer: path.relative(repoRoot, path.join(caseRoot, "private", "answer.md")).replaceAll("\\", "/"),
      legacy_rubric: path.relative(repoRoot, path.join(caseRoot, "private", "rubric.md")).replaceAll("\\", "/"),
      private_traceability: path.relative(repoRoot, path.join(caseRoot, "private", "traceability.md")).replaceAll("\\", "/"),
      meta: path.relative(repoRoot, metaPath).replaceAll("\\", "/"),
      primary_metrics: meta.primary_metrics ?? [],
      secondary_metrics: meta.secondary_metrics ?? [],
      acceptance_alignment_signals: meta.acceptance_alignment_signals ?? []
    });
  }
}

const manifestPath = path.join(benchmarkRoot, "cases_manifest.jsonl");
fs.writeFileSync(
  manifestPath,
  `${manifestEntries.map((entry) => JSON.stringify(entry)).join("\n")}\n`,
  "utf8"
);

const publicDatasetManifestPath = path.join(publicDatasetRoot, "cases_manifest.jsonl");
fs.writeFileSync(
  publicDatasetManifestPath,
  `${manifestEntries.map((entry) => JSON.stringify(entry)).join("\n")}\n`,
  "utf8"
);

const privateManifestPath = path.join(benchmarkRoot, "private_cases_manifest.jsonl");
fs.writeFileSync(
  privateManifestPath,
  `${privateManifestEntries.map((entry) => JSON.stringify(entry)).join("\n")}\n`,
  "utf8"
);

const publicDatasetReadmePath = path.join(publicDatasetRoot, "README.md");
fs.writeFileSync(
  publicDatasetReadmePath,
  [
    "# Public Dataset Bundle",
    "",
    "この directory は model-facing bundle です。",
    "",
    "- モデルに渡すのはこの bundle の `cases_manifest.jsonl` と各 case の `public/` だけにする。",
    "- `private/`, `shared/`, research, traceability は含めない。",
    "- evaluator は元の `benchmark/` 側にある private artifact を使う。"
  ].join("\n"),
  "utf8"
);

const summaryPath = path.join(benchmarkRoot, "dataset_summary.md");
const pilotCount = manifestEntries.filter((entry) => entry.split === "pilot").length;
const mainCount = manifestEntries.filter((entry) => entry.split === "main").length;
fs.writeFileSync(
  summaryPath,
  [
    "# Dataset Summary",
    "",
    `- pilot cases: ${pilotCount}`,
    `- main cases: ${mainCount}`,
    `- total cases: ${manifestEntries.length}`,
    `- public manifest: \`benchmark/cases_manifest.jsonl\``,
    `- private manifest: \`benchmark/private_cases_manifest.jsonl\``,
    `- public bundle: \`benchmark/public_dataset/\``,
    `- splits: \`benchmark/splits/pilot.txt\`, \`benchmark/splits/main.txt\``
  ].join("\n"),
  "utf8"
);

console.log(`Wrote ${manifestEntries.length} cases to ${manifestPath}`);
