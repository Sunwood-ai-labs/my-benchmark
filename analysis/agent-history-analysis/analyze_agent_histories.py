from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import matplotlib
import pandas as pd
from janome.tokenizer import Tokenizer

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
DATA_ROOT = REPO_ROOT / "data"
OUTPUT_ROOT = ROOT / "outputs"
CHART_ROOT = OUTPUT_ROOT / "charts"

LOCAL_CLAUDE = Path(r"C:\Users\Aslan\.claude")
LOCAL_CODEX = Path(r"C:\Users\Aslan\.codex")

TOKENIZER = Tokenizer()

JA_STOPWORDS = {
    "こと",
    "これ",
    "それ",
    "ため",
    "よう",
    "もの",
    "感じ",
    "さん",
    "そこ",
    "ここ",
    "あと",
    "今日",
    "明日",
    "昨日",
    "お願い",
    "確認",
    "作業",
    "対応",
    "実装",
    "修正",
    "分析",
    "調査",
}

EN_STOPWORDS = {
    "to",
    "in",
    "is",
    "not",
    "or",
    "you",
    "available",
    "timestamp",
    "final",
    "file",
    "docs",
    "skill",
    "notification",
    "idle",
    "idle_notification",
    "idlereason",
    "shut",
    "down",
    "kb",
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "have",
    "your",
    "about",
    "please",
    "need",
    "make",
    "just",
    "like",
    "help",
    "want",
    "look",
    "also",
    "there",
    "been",
    "when",
    "where",
    "what",
    "which",
    "would",
    "should",
    "could",
    "using",
    "used",
}

ANALYSIS_NOISE_TOKENS = {
    "agent",
    "agents",
    "assistant",
    "user",
    "teammate",
    "teammates",
    "teammate-message",
    "message",
    "messages",
    "summary",
    "response",
    "responses",
    "thread",
    "threads",
    "session",
    "sessions",
    "status",
    "color",
    "type",
    "types",
    "tool",
    "tools",
    "call",
    "calls",
    "prompt",
    "prompts",
    "return",
    "print",
    "json",
    "api",
    "role",
    "roles",
    "team",
    "teams",
    "task",
    "tasks",
    "phase",
    "shell_command",
    "apply_patch",
    "js_repl",
    "update_plan",
    "wait_agent",
    "spawn_agent",
    "readme",
    "id",
    "ids",
    "md",
    "git",
}

CATEGORY_KEYWORDS = {
    "implementation": [
        "作って",
        "作成",
        "追加",
        "構築",
        "実装",
        "build",
        "implement",
        "scaffold",
        "feature",
        "repo",
        "project",
    ],
    "debug_fix": [
        "直して",
        "修正",
        "バグ",
        "エラー",
        "壊れ",
        "動か",
        "fix",
        "bug",
        "error",
        "failing",
        "exception",
    ],
    "analysis_research": [
        "分析",
        "調査",
        "比較",
        "見て",
        "調べ",
        "まとめ",
        "benchmark",
        "research",
        "report",
        "inspect",
        "look up",
    ],
    "automation_orchestration": [
        "automation",
        "workflow",
        "agent",
        "subagent",
        "codex",
        "claude",
        "orchestrator",
        "github actions",
        "自動",
        "エージェント",
        "並列",
    ],
    "docs_writing": [
        "readme",
        "docs",
        "documentation",
        "記事",
        "release notes",
        "ブログ",
        "説明",
        "書いて",
        "note.com",
    ],
    "setup_config": [
        "setup",
        "install",
        "config",
        "設定",
        "環境",
        "uv",
        "docker",
        "mcp",
        "認証",
        "credential",
    ],
    "review_qa": [
        "review",
        "test",
        "qa",
        "lint",
        "検証",
        "確認",
        "監査",
        "smoke",
        "rubric",
    ],
    "design_ui": [
        "ui",
        "ux",
        "css",
        "layout",
        "component",
        "frontend",
        "画面",
        "デザイン",
        "見た目",
    ],
    "data_ml": [
        "data",
        "dataset",
        "csv",
        "jsonl",
        "sqlite",
        "llm",
        "model",
        "embedding",
        "vector",
        "training",
        "推論",
        "学習",
    ],
}


@dataclass
class ClaudeRoot:
    root: Path
    origin_label: str


@dataclass
class CodexRoot:
    root: Path
    origin_label: str


def ensure_dirs() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    CHART_ROOT.mkdir(parents=True, exist_ok=True)


def discover_roots() -> tuple[list[ClaudeRoot], list[CodexRoot]]:
    claude_roots: list[ClaudeRoot] = []
    codex_roots: list[CodexRoot] = []
    if LOCAL_CLAUDE.exists():
        claude_roots.append(ClaudeRoot(root=LOCAL_CLAUDE, origin_label="local_home"))
    if LOCAL_CODEX.exists():
        codex_roots.append(CodexRoot(root=LOCAL_CODEX, origin_label="local_home"))

    if DATA_ROOT.exists():
        for path in sorted(DATA_ROOT.rglob(".claude")):
            claude_roots.append(ClaudeRoot(root=path, origin_label=f"data_snapshot:{path.parent.name}"))
        for path in sorted(DATA_ROOT.rglob(".codex")):
            codex_roots.append(CodexRoot(root=path, origin_label=f"data_snapshot:{path.parent.name}"))

    return claude_roots, codex_roots


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def text_hash(*parts: Any) -> str:
    joined = "\u241f".join("" if part is None else str(part) for part in parts)
    return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:16]


def flatten_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(part for part in (flatten_text(item) for item in value) if part)
    if isinstance(value, dict):
        kind = value.get("type")
        if kind in {"text", "input_text", "output_text"}:
            return str(value.get("text", ""))
        if kind == "tool_result":
            return flatten_text(value.get("content"))
        if "text" in value and isinstance(value.get("text"), str):
            return value["text"]
        return "\n".join(part for part in (flatten_text(item) for item in value.values()) if part)
    return str(value)


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def looks_like_tool_result(content: Any) -> bool:
    return isinstance(content, list) and bool(content) and all(
        isinstance(item, dict) and item.get("type") == "tool_result" for item in content
    )


def flatten_claude_message_blocks(content: Any) -> tuple[str, list[str]]:
    texts: list[str] = []
    tool_names: list[str] = []
    if isinstance(content, str):
        texts.append(content)
    elif isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                texts.append(flatten_text(block))
                continue
            block_type = block.get("type")
            if block_type == "text":
                text = block.get("text")
                if isinstance(text, str):
                    texts.append(text)
            elif block_type == "thinking":
                continue
            elif block_type == "tool_use":
                name = block.get("name")
                if isinstance(name, str):
                    tool_names.append(name)
            elif block_type == "tool_result":
                result_text = normalize_whitespace(flatten_text(block.get("content")))
                if result_text:
                    texts.append(result_text)
            else:
                generic_text = normalize_whitespace(flatten_text(block))
                if generic_text:
                    texts.append(generic_text)
    elif isinstance(content, dict):
        texts.append(flatten_text(content))
    return normalize_whitespace("\n".join(texts)), tool_names


def flatten_codex_content(content: Any) -> str:
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if not isinstance(item, dict):
                parts.append(str(item))
                continue
            item_type = item.get("type")
            if item_type in {"output_text", "input_text"}:
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
            elif item_type == "output_image":
                continue
            else:
                parts.append(flatten_text(item))
        return normalize_whitespace("\n".join(parts))
    return normalize_whitespace(flatten_text(content))


def load_codex_titles(codex_root: CodexRoot) -> dict[str, str]:
    titles: dict[str, str] = {}
    session_index = codex_root.root / "session_index.jsonl"
    if session_index.exists():
        for obj in iter_jsonl(session_index):
            thread_id = obj.get("id")
            title = obj.get("thread_name")
            if isinstance(thread_id, str) and isinstance(title, str) and title.strip():
                titles[thread_id] = title.strip()
    state_db = codex_root.root / "state_5.sqlite"
    if state_db.exists():
        try:
            with sqlite3.connect(state_db) as conn:
                for thread_id, title in conn.execute("select id, title from threads"):
                    if isinstance(thread_id, str) and isinstance(title, str) and title.strip():
                        titles.setdefault(thread_id, title.strip())
        except sqlite3.DatabaseError:
            pass
    return titles


def discover_claude_project_files(root: ClaudeRoot) -> list[Path]:
    projects_root = root.root / "projects"
    if not projects_root.exists():
        return []
    files = []
    for path in projects_root.rglob("*.jsonl"):
        if "subagents" in path.parts:
            continue
        files.append(path)
    return sorted(files)


def discover_codex_session_files(root: CodexRoot) -> list[Path]:
    files: list[Path] = []
    archived_dir = root.root / "archived_sessions"
    session_dir = root.root / "sessions"
    if archived_dir.exists():
        files.extend(sorted(archived_dir.glob("*.jsonl")))
    if session_dir.exists():
        files.extend(sorted(session_dir.rglob("*.jsonl")))
    return files


def classify_language(text: str) -> str:
    japanese_chars = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", text))
    english_chars = len(re.findall(r"[A-Za-z]", text))
    if japanese_chars and english_chars:
        return "mixed"
    if japanese_chars:
        return "ja"
    if english_chars:
        return "en"
    return "other"


def classify_category(text: str) -> str:
    lowered = clean_text_for_analysis(text).lower()
    scores = {
        category: sum(1 for keyword in keywords if keyword in lowered)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "other"
    return best_category


def parse_timestamp_value(value: Any) -> pd.Timestamp | pd.NaT:
    if value is None or value == "":
        return pd.NaT
    if isinstance(value, str) and value.isdigit():
        value = int(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        numeric = int(value)
        if numeric >= 10**12:
            return pd.to_datetime(numeric, unit="ms", utc=True, errors="coerce")
        if numeric >= 10**9:
            return pd.to_datetime(numeric, unit="s", utc=True, errors="coerce")
    return pd.to_datetime(value, utc=True, errors="coerce")


def clean_text_for_analysis(text: str) -> str:
    cleaned = normalize_whitespace(text)
    cleaned = re.sub(r"```[\s\S]*?```", " ", cleaned)
    cleaned = re.sub(r"`[^`]*`", " ", cleaned)
    cleaned = re.sub(r"<[^>\n]+>", " ", cleaned)
    cleaned = re.sub(r"https?://\S+", " ", cleaned)
    cleaned = re.sub(r"\b[A-Za-z]:\\[^\s]+", " ", cleaned)
    cleaned = cleaned.replace("**", " ").replace("##", " ")
    cleaned = re.sub(r"[=:]{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def extract_terms(text: str) -> list[str]:
    normalized = clean_text_for_analysis(text.lower())
    terms: list[str] = []

    for token in TOKENIZER.tokenize(normalized):
        surface = token.surface.strip()
        base = token.base_form if token.base_form != "*" else surface
        base_lower = base.lower()
        pos = token.part_of_speech.split(",")[0]
        if pos != "名詞":
            continue
        if len(base) <= 1 or base in JA_STOPWORDS:
            continue
        if base_lower in EN_STOPWORDS or base_lower in ANALYSIS_NOISE_TOKENS:
            continue
        if base in ANALYSIS_NOISE_TOKENS:
            continue
        if re.fullmatch(r"[0-9._/-]+", base):
            continue
        if not re.search(r"[A-Za-z0-9_\u3040-\u30ff\u3400-\u9fff]", base):
            continue
        terms.append(base)

    for token in re.findall(r"[A-Za-z][A-Za-z0-9_./+-]{1,}", normalized):
        if token in EN_STOPWORDS or token in ANALYSIS_NOISE_TOKENS:
            continue
        if token.startswith("agent-") or token.startswith("session-"):
            continue
        terms.append(token)

    return terms


def render_table(df: pd.DataFrame, index: bool = False) -> str:
    if df.empty:
        return "_No data_"
    return df.to_markdown(index=index)


def plot_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, output_name: str, rotate: int = 0) -> None:
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df[x_col].astype(str), df[y_col], color="#2E6F95")
    ax.set_title(title)
    ax.set_ylabel(y_col.replace("_", " ").title())
    ax.set_xlabel("")
    if rotate:
        plt.setp(ax.get_xticklabels(), rotation=rotate, ha="right")
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(CHART_ROOT / output_name, dpi=160)
    plt.close(fig)


def build_report(*args: Any, **kwargs: Any) -> str:
    messages_df: pd.DataFrame = kwargs["messages_df"]
    tools_df: pd.DataFrame = kwargs["tools_df"]
    inventory_df: pd.DataFrame = kwargs["inventory_df"]
    user_df: pd.DataFrame = kwargs["user_df"]
    session_summary: pd.DataFrame = kwargs["session_summary"]
    top_projects: pd.DataFrame = kwargs["top_projects"]
    top_categories: pd.DataFrame = kwargs["top_categories"]
    language_mix: pd.DataFrame = kwargs["language_mix"]
    top_terms: pd.DataFrame = kwargs["top_terms"]
    top_tools: pd.DataFrame = kwargs["top_tools"]
    hour_summary: pd.DataFrame = kwargs["hour_summary"]
    message_counts: pd.DataFrame = kwargs["message_counts"]

    prompt_only_count = int((messages_df["phase"] == "history_only").sum()) if "phase" in messages_df else 0
    full_interaction_count = len(messages_df) - prompt_only_count

    return f"""# Agent Interaction Analysis

Generated at: {pd.Timestamp.now(tz='Asia/Tokyo').isoformat()}

## Scope

- Workspace: `{REPO_ROOT}`
- Sources inspected: local `C:\\Users\\Aslan\\.claude`, local `C:\\Users\\Aslan\\.codex`, and snapshot roots found under `{DATA_ROOT}`
- Primary interaction dataset: Claude project transcripts plus Codex session transcripts
- Auxiliary prompt-only dataset: Claude `history.jsonl` only when no project transcripts were present for that root

## Dataset Overview

- Total normalized messages: **{len(messages_df):,}**
- Full interaction messages: **{full_interaction_count:,}**
- Prompt-only fallback messages: **{prompt_only_count:,}**
- User messages: **{len(user_df):,}**
- Assistant messages: **{len(messages_df[messages_df['role'] == 'assistant']):,}**
- Tool invocations captured: **{len(tools_df):,}**
- Distinct sessions / threads: **{messages_df['session_id'].nunique():,}**

### Source Inventory

{render_table(inventory_df.fillna(''))}

### Message Volume by Agent Family / Origin

{render_table(message_counts)}

## User Communication Patterns

### Top Projects / Working Directories

{render_table(top_projects)}

### Active Hours (JST)

{render_table(hour_summary)}

### Language Mix

{render_table(language_mix)}

### Frequent User Terms

{render_table(top_terms)}

## Topic / Genre Analysis

### Top User Request Categories

{render_table(top_categories)}

### Session Size Snapshot

{render_table(session_summary)}

## Agent / Tool Interaction

### Most Used Tools

{render_table(top_tools)}

## Notes And Caveats

- Claude `history.jsonl` is treated as prompt-only fallback because it can overlap with richer `projects/*.jsonl` transcripts.
- Codex message extraction intentionally ignores developer/system scaffolding and `reasoning` items, focusing on user-visible user/assistant messages plus tool calls.
- Imported snapshot roots may overlap with local roots; normalization deduplicates at the message key level where stable identifiers exist.
"""


def parse_claude(roots: list[ClaudeRoot]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    messages: list[dict[str, Any]] = []
    tools: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    seen_message_ids: set[str] = set()
    seen_tool_ids: set[str] = set()

    for claude_root in roots:
        project_files = discover_claude_project_files(claude_root)
        history_path = claude_root.root / "history.jsonl"
        subagent_files = sorted((claude_root.root / "projects").rglob("subagents/*.jsonl")) if (claude_root.root / "projects").exists() else []
        team_configs = sorted((claude_root.root / "teams").rglob("config.json")) if (claude_root.root / "teams").exists() else []
        task_files = sorted((claude_root.root / "tasks").rglob("*.json")) if (claude_root.root / "tasks").exists() else []
        todo_files = sorted((claude_root.root / "todos").glob("*.json")) if (claude_root.root / "todos").exists() else []
        inventory.append(
            {
                "agent_family": "claude",
                "origin": claude_root.origin_label,
                "root_path": str(claude_root.root),
                "project_jsonl_count": len(project_files),
                "subagent_jsonl_count": len(subagent_files),
                "team_config_count": len(team_configs),
                "task_json_count": len(task_files),
                "todo_json_count": len(todo_files),
                "history_exists": history_path.exists(),
                "fallback_history_used": len(project_files) == 0 and history_path.exists(),
            }
        )

        if project_files:
            for project_file in project_files:
                for obj in iter_jsonl(project_file):
                    record_type = obj.get("type")
                    if record_type == "file-history-snapshot":
                        continue

                    session_id = obj.get("sessionId") or project_file.stem
                    timestamp = obj.get("timestamp")
                    raw_uuid = obj.get("uuid") or obj.get("messageId") or text_hash(
                        project_file,
                        record_type,
                        timestamp,
                        obj.get("parentUuid"),
                    )
                    cwd = obj.get("cwd")
                    project_name = Path(cwd).name if isinstance(cwd, str) else None
                    message = obj.get("message", {})
                    role = None
                    content = None
                    tool_names: list[str] = []

                    if record_type == "user":
                        content = message.get("content")
                        role = "tool" if looks_like_tool_result(content) or obj.get("sourceToolAssistantUUID") else "user"
                    elif record_type == "assistant":
                        role = "assistant"
                        content = message.get("content")
                    else:
                        continue

                    text, tool_names = flatten_claude_message_blocks(content)
                    model = message.get("model") if isinstance(message, dict) else None
                    key = f"claude:{session_id}:{raw_uuid}"

                    if role in {"user", "assistant"} and key not in seen_message_ids:
                        seen_message_ids.add(key)
                        messages.append(
                            {
                                "agent_family": "claude",
                                "origin": claude_root.origin_label,
                                "root_path": str(claude_root.root),
                                "session_id": session_id,
                                "message_key": key,
                                "raw_id": raw_uuid,
                                "timestamp": timestamp,
                                "role": role,
                                "text": text,
                                "char_count": len(text),
                                "line_count": text.count("\n") + 1 if text else 0,
                                "cwd": cwd,
                                "project_name": project_name,
                                "thread_title": None,
                                "model": model,
                                "phase": None,
                                "event_type": record_type,
                            }
                        )

                    for tool_name in tool_names:
                        tool_key = f"claude:{session_id}:{raw_uuid}:{tool_name}"
                        if tool_key in seen_tool_ids:
                            continue
                        seen_tool_ids.add(tool_key)
                        tools.append(
                            {
                                "agent_family": "claude",
                                "origin": claude_root.origin_label,
                                "root_path": str(claude_root.root),
                                "session_id": session_id,
                                "timestamp": timestamp,
                                "role": "assistant",
                                "tool_name": tool_name,
                                "event_type": "tool_use",
                            }
                        )
        elif history_path.exists():
            for obj in iter_jsonl(history_path):
                text = normalize_whitespace(str(obj.get("display", "")))
                if not text:
                    continue
                session_id = obj.get("sessionId")
                timestamp = obj.get("timestamp")
                key = f"claude_history:{session_id}:{timestamp}:{text_hash(text)}"
                if key in seen_message_ids:
                    continue
                seen_message_ids.add(key)
                project_path = obj.get("project")
                project_name = Path(project_path).name if isinstance(project_path, str) else None
                messages.append(
                    {
                        "agent_family": "claude",
                        "origin": claude_root.origin_label,
                        "root_path": str(claude_root.root),
                        "session_id": session_id,
                        "message_key": key,
                        "raw_id": key,
                        "timestamp": timestamp,
                        "role": "user",
                        "text": text,
                        "char_count": len(text),
                        "line_count": text.count("\n") + 1 if text else 0,
                        "cwd": project_path,
                        "project_name": project_name,
                        "thread_title": None,
                        "model": None,
                        "phase": "history_only",
                        "event_type": "history_prompt",
                    }
                )

    return messages, tools, inventory


def parse_codex(roots: list[CodexRoot]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    messages: list[dict[str, Any]] = []
    tools: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    seen_message_ids: set[str] = set()
    seen_tool_ids: set[str] = set()

    for codex_root in roots:
        session_files = discover_codex_session_files(codex_root)
        titles = load_codex_titles(codex_root)
        inventory.append(
            {
                "agent_family": "codex",
                "origin": codex_root.origin_label,
                "root_path": str(codex_root.root),
                "session_jsonl_count": len(session_files),
                "session_index_exists": (codex_root.root / "session_index.jsonl").exists(),
                "state_db_exists": (codex_root.root / "state_5.sqlite").exists(),
            }
        )

        seen_threads_in_root: set[str] = set()
        for session_file in session_files:
            meta_thread_id = None
            session_meta: dict[str, Any] | None = None
            local_messages: list[dict[str, Any]] = []
            local_tools: list[dict[str, Any]] = []

            for obj in iter_jsonl(session_file):
                obj_type = obj.get("type")
                if obj_type == "session_meta":
                    payload = obj.get("payload", {})
                    meta_thread_id = payload.get("id") or meta_thread_id
                    session_meta = payload
                    continue

                thread_id = meta_thread_id or session_file.stem
                cwd = session_meta.get("cwd") if isinstance(session_meta, dict) else None
                project_name = Path(cwd).name if isinstance(cwd, str) else None

                if obj_type == "event_msg":
                    payload = obj.get("payload", {})
                    if payload.get("type") != "user_message":
                        continue
                    text = normalize_whitespace(payload.get("message", ""))
                    if not text:
                        continue
                    timestamp = obj.get("timestamp")
                    key = f"codex:{thread_id}:user:{timestamp}:{text_hash(text)}"
                    local_messages.append(
                        {
                            "agent_family": "codex",
                            "origin": codex_root.origin_label,
                            "root_path": str(codex_root.root),
                            "session_id": thread_id,
                            "message_key": key,
                            "raw_id": key,
                            "timestamp": timestamp,
                            "role": "user",
                            "text": text,
                            "char_count": len(text),
                            "line_count": text.count("\n") + 1 if text else 0,
                            "cwd": cwd,
                            "project_name": project_name,
                            "thread_title": titles.get(thread_id),
                            "model": None,
                            "phase": None,
                            "event_type": "user_message",
                        }
                    )
                    continue

                if obj_type != "response_item":
                    continue

                payload = obj.get("payload", {})
                payload_type = payload.get("type")
                if payload_type == "message" and payload.get("role") == "assistant":
                    text = flatten_codex_content(payload.get("content"))
                    if not text:
                        continue
                    timestamp = obj.get("timestamp")
                    key = f"codex:{thread_id}:assistant:{timestamp}:{text_hash(text)}"
                    local_messages.append(
                        {
                            "agent_family": "codex",
                            "origin": codex_root.origin_label,
                            "root_path": str(codex_root.root),
                            "session_id": thread_id,
                            "message_key": key,
                            "raw_id": key,
                            "timestamp": timestamp,
                            "role": "assistant",
                            "text": text,
                            "char_count": len(text),
                            "line_count": text.count("\n") + 1 if text else 0,
                            "cwd": cwd,
                            "project_name": project_name,
                            "thread_title": titles.get(thread_id),
                            "model": None,
                            "phase": obj.get("phase"),
                            "event_type": "assistant_message",
                        }
                    )
                elif payload_type in {"function_call", "custom_tool_call", "web_search_call"}:
                    tool_name = payload.get("name") or payload.get("tool_name") or payload.get("recipient_name")
                    if not tool_name:
                        continue
                    timestamp = obj.get("timestamp")
                    local_tools.append(
                        {
                            "agent_family": "codex",
                            "origin": codex_root.origin_label,
                            "root_path": str(codex_root.root),
                            "session_id": thread_id,
                            "timestamp": timestamp,
                            "role": "assistant",
                            "tool_name": tool_name,
                            "event_type": payload_type,
                        }
                    )

            thread_id = meta_thread_id or session_file.stem
            if thread_id in seen_threads_in_root:
                continue
            seen_threads_in_root.add(thread_id)

            for record in local_messages:
                if record["message_key"] in seen_message_ids:
                    continue
                seen_message_ids.add(record["message_key"])
                messages.append(record)
            for record in local_tools:
                tool_key = f"{record['session_id']}:{record['timestamp']}:{record['tool_name']}:{record['event_type']}"
                if tool_key in seen_tool_ids:
                    continue
                seen_tool_ids.add(tool_key)
                tools.append(record)

    return messages, tools, inventory


def main() -> None:
    ensure_dirs()

    claude_roots, codex_roots = discover_roots()
    claude_messages, claude_tools, claude_inventory = parse_claude(claude_roots)
    codex_messages, codex_tools, codex_inventory = parse_codex(codex_roots)

    messages_df = pd.DataFrame(claude_messages + codex_messages)
    tools_df = pd.DataFrame(claude_tools + codex_tools)
    inventory_df = pd.DataFrame(claude_inventory + codex_inventory)

    if messages_df.empty:
        raise SystemExit("No messages were discovered.")

    messages_df["timestamp"] = messages_df["timestamp"].map(parse_timestamp_value)
    messages_df["timestamp_jst"] = messages_df["timestamp"].dt.tz_convert("Asia/Tokyo")
    messages_df["date_jst"] = messages_df["timestamp_jst"].dt.date.astype("string")
    messages_df["hour_jst"] = messages_df["timestamp_jst"].dt.hour.fillna(-1).astype(int)
    messages_df["language"] = messages_df["text"].map(classify_language)
    messages_df["category"] = messages_df["text"].map(classify_category)
    messages_df["text_preview"] = messages_df["text"].str.replace("\n", " ", regex=False).str.slice(0, 120)

    user_df = messages_df[messages_df["role"] == "user"].copy()
    assistant_df = messages_df[messages_df["role"] == "assistant"].copy()

    session_summary = (
        messages_df.groupby(["agent_family", "origin", "session_id"], dropna=False)
        .agg(
            first_timestamp=("timestamp_jst", "min"),
            last_timestamp=("timestamp_jst", "max"),
            total_messages=("message_key", "count"),
            user_messages=("role", lambda values: int((pd.Series(values) == "user").sum())),
            assistant_messages=("role", lambda values: int((pd.Series(values) == "assistant").sum())),
            avg_chars=("char_count", "mean"),
            project_name=("project_name", "first"),
            thread_title=("thread_title", "first"),
        )
        .reset_index()
    )
    session_summary["duration_minutes"] = (
        (session_summary["last_timestamp"] - session_summary["first_timestamp"]).dt.total_seconds() / 60
    ).fillna(0)
    session_snapshot = session_summary.sort_values("total_messages", ascending=False).head(15).copy()
    session_snapshot["avg_chars"] = session_snapshot["avg_chars"].round(1)
    session_snapshot["duration_minutes"] = session_snapshot["duration_minutes"].round(1)

    top_projects = (
        user_df.assign(project_or_title=user_df["project_name"].fillna(user_df["thread_title"]).fillna("(unknown)"))
        .groupby(["agent_family", "origin", "project_or_title"], dropna=False)
        .agg(user_messages=("message_key", "count"), avg_chars=("char_count", "mean"))
        .reset_index()
        .sort_values("user_messages", ascending=False)
        .head(15)
    )
    top_projects["avg_chars"] = top_projects["avg_chars"].round(1)

    top_categories = (
        user_df.groupby("category", dropna=False)
        .agg(user_messages=("message_key", "count"), avg_chars=("char_count", "mean"))
        .reset_index()
        .sort_values("user_messages", ascending=False)
    )
    top_categories["share_pct"] = (top_categories["user_messages"] / max(len(user_df), 1) * 100).round(1)
    top_categories["avg_chars"] = top_categories["avg_chars"].round(1)

    language_mix = (
        user_df.groupby("language", dropna=False)
        .agg(user_messages=("message_key", "count"))
        .reset_index()
        .sort_values("user_messages", ascending=False)
    )
    language_mix["share_pct"] = (language_mix["user_messages"] / max(len(user_df), 1) * 100).round(1)

    top_tools = (
        tools_df.groupby(["agent_family", "tool_name"], dropna=False)
        .agg(invocations=("tool_name", "count"))
        .reset_index()
        .sort_values("invocations", ascending=False)
        .head(20)
        if not tools_df.empty
        else pd.DataFrame(columns=["agent_family", "tool_name", "invocations"])
    )

    hour_summary = (
        user_df[user_df["hour_jst"] >= 0]
        .groupby("hour_jst")
        .agg(user_messages=("message_key", "count"))
        .reset_index()
        .sort_values("hour_jst")
    )
    hour_summary["share_pct"] = (hour_summary["user_messages"] / max(len(user_df), 1) * 100).round(1)

    message_counts = (
        messages_df.groupby(["agent_family", "origin", "role"], dropna=False)
        .agg(messages=("message_key", "count"))
        .reset_index()
        .sort_values("messages", ascending=False)
    )

    term_counter: Counter[str] = Counter()
    for text in user_df["text"].tolist():
        term_counter.update(extract_terms(text))
    top_terms = pd.DataFrame(term_counter.most_common(30), columns=["term", "count"])

    messages_df.to_csv(OUTPUT_ROOT / "messages_normalized.csv.gz", index=False, compression="gzip")
    user_df.to_csv(OUTPUT_ROOT / "user_messages.csv.gz", index=False, compression="gzip")
    assistant_df.to_csv(OUTPUT_ROOT / "assistant_messages.csv.gz", index=False, compression="gzip")
    session_summary.to_csv(OUTPUT_ROOT / "session_summary.csv", index=False)
    top_projects.to_csv(OUTPUT_ROOT / "top_projects.csv", index=False)
    top_categories.to_csv(OUTPUT_ROOT / "top_categories.csv", index=False)
    top_tools.to_csv(OUTPUT_ROOT / "top_tools.csv", index=False)
    inventory_df.to_csv(OUTPUT_ROOT / "source_inventory.csv", index=False)

    summary_payload = {
        "message_count": int(len(messages_df)),
        "user_message_count": int(len(user_df)),
        "assistant_message_count": int(len(assistant_df)),
        "tool_invocation_count": int(len(tools_df)),
        "session_count": int(messages_df["session_id"].nunique()),
        "top_category": top_categories.iloc[0]["category"] if not top_categories.empty else None,
        "top_language": language_mix.iloc[0]["language"] if not language_mix.empty else None,
        "top_project": top_projects.iloc[0]["project_or_title"] if not top_projects.empty else None,
    }
    (OUTPUT_ROOT / "analysis_summary.json").write_text(
        json.dumps(summary_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    plot_bar(
        message_counts.assign(
            label=message_counts["agent_family"] + " / " + message_counts["origin"] + " / " + message_counts["role"]
        ),
        "label",
        "messages",
        "Message Volume by Source / Role",
        "message_volume_by_source.png",
        rotate=45,
    )
    plot_bar(
        top_categories.head(10),
        "category",
        "user_messages",
        "Top User Request Categories",
        "top_user_categories.png",
        rotate=30,
    )
    plot_bar(
        hour_summary,
        "hour_jst",
        "user_messages",
        "User Activity by Hour (JST)",
        "user_activity_by_hour.png",
    )
    plot_bar(
        top_projects.head(10),
        "project_or_title",
        "user_messages",
        "Top Projects / Threads by User Messages",
        "top_projects.png",
        rotate=45,
    )

    report = build_report(
        messages_df=messages_df,
        tools_df=tools_df,
        inventory_df=inventory_df,
        user_df=user_df,
        session_summary=session_snapshot,
        top_projects=top_projects,
        top_categories=top_categories,
        language_mix=language_mix,
        top_terms=top_terms,
        top_tools=top_tools,
        hour_summary=hour_summary,
        message_counts=message_counts,
    )
    (OUTPUT_ROOT / "report.md").write_text(report, encoding="utf-8")

    print(f"Messages: {len(messages_df):,}")
    print(f"User messages: {len(user_df):,}")
    print(f"Assistant messages: {len(assistant_df):,}")
    print(f"Sessions: {messages_df['session_id'].nunique():,}")
    print(f"Outputs: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
