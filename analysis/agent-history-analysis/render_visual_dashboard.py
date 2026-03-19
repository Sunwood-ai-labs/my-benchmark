from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.text import Text


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
CHARTS = OUTPUTS / "charts"
LAYOUT_CHECKS = OUTPUTS / "layout_checks"


@dataclass
class TextBox:
    chart_name: str
    axes_label: str
    kind: str
    text: str
    bbox: tuple[float, float, float, float]


def load_data() -> dict[str, pd.DataFrame | dict]:
    return {
        "summary": json.loads((OUTPUTS / "analysis_summary.json").read_text(encoding="utf-8")),
        "messages": pd.read_csv(OUTPUTS / "messages_normalized.csv.gz", low_memory=False),
        "users": pd.read_csv(OUTPUTS / "user_messages.csv.gz", low_memory=False),
        "categories": pd.read_csv(OUTPUTS / "top_categories.csv"),
        "projects": pd.read_csv(OUTPUTS / "top_projects.csv"),
        "tools": pd.read_csv(OUTPUTS / "top_tools.csv"),
        "inventory": pd.read_csv(OUTPUTS / "source_inventory.csv"),
        "token_by_source": pd.read_csv(OUTPUTS / "token_usage_by_source.csv"),
        "token_sessions": pd.read_csv(OUTPUTS / "token_usage_by_session.csv", low_memory=False),
        "top_token_sessions": pd.read_csv(OUTPUTS / "top_token_sessions.csv", low_memory=False),
    }


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "#F7F1E5",
            "axes.facecolor": "#FFF9EF",
            "axes.edgecolor": "#D9C7A6",
            "axes.labelcolor": "#2E2A26",
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "axes.titlecolor": "#2E2A26",
            "xtick.color": "#4B4338",
            "ytick.color": "#4B4338",
            "grid.color": "#D8CBB5",
            "font.size": 10,
        }
    )


def shorten_origin(agent_family: str, origin: str) -> str:
    if agent_family == "codex" and origin == "local_home":
        return "Codex local"
    if agent_family == "claude" and origin == "local_home":
        return "Claude local"
    if "prox-200-maki" in origin:
        return "Claude snap prox"
    if "kali-aslan" in origin:
        return "Claude snap kali"
    return origin.replace("data_snapshot:", "snapshot:")


def add_card(ax: plt.Axes, title: str, value: str, subtitle: str, accent: str) -> None:
    ax.set_facecolor(accent)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0.06, 0.76, title, fontsize=11, fontweight="bold", color="#FFF9EF", transform=ax.transAxes)
    ax.text(0.06, 0.40, value, fontsize=24, fontweight="bold", color="#FFFFFF", transform=ax.transAxes)
    ax.text(0.06, 0.12, subtitle, fontsize=9, color="#F6E9D0", transform=ax.transAxes)


def trim_label(value: str, width: int = 24) -> str:
    text = str(value)
    if len(text) <= width:
        return text
    return textwrap.shorten(text, width=width, placeholder="...")


def format_compact_number(value: int | float) -> str:
    number = float(value)
    suffixes = [(1_000_000_000, "B"), (1_000_000, "M"), (1_000, "K")]
    for threshold, suffix in suffixes:
        if abs(number) >= threshold:
            compact = number / threshold
            return f"{compact:.1f}".rstrip("0").rstrip(".") + suffix
    return f"{int(number):,}"


def bbox_area(bbox: tuple[float, float, float, float]) -> float:
    return max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])


def bbox_overlap_metrics(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> tuple[float, float, float]:
    x0 = max(a[0], b[0])
    y0 = max(a[1], b[1])
    x1 = min(a[2], b[2])
    y1 = min(a[3], b[3])
    overlap_width = max(0.0, x1 - x0)
    overlap_height = max(0.0, y1 - y0)
    return overlap_width, overlap_height, overlap_width * overlap_height


def artist_bbox_tuple(artist: Text, renderer, padding: float = 2.0) -> tuple[float, float, float, float]:
    bbox = artist.get_window_extent(renderer)
    return (bbox.x0 - padding, bbox.y0 - padding, bbox.x1 + padding, bbox.y1 + padding)


def is_visible_text(artist: Text) -> bool:
    if not artist.get_visible():
        return False
    if artist.get_alpha() == 0:
        return False
    content = artist.get_text()
    return bool(content and content.strip())


def collect_text_boxes(fig: plt.Figure, chart_name: str) -> tuple[list[TextBox], dict[str, tuple[float, float, float, float]]]:
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes: list[TextBox] = []
    axes_boxes: dict[str, tuple[float, float, float, float]] = {}

    for idx, ax in enumerate(fig.axes):
        title = ax.get_title() or f"axes_{idx}"
        axes_label = f"{idx}:{title}"
        ax_bbox = ax.get_window_extent(renderer)
        axes_boxes[axes_label] = (ax_bbox.x0, ax_bbox.y0, ax_bbox.x1, ax_bbox.y1)

        text_artists: list[tuple[str, Text]] = [
            ("title", ax.title),
            ("x_label", ax.xaxis.label),
            ("y_label", ax.yaxis.label),
            ("x_offset", ax.xaxis.get_offset_text()),
            ("y_offset", ax.yaxis.get_offset_text()),
        ]
        text_artists.extend(("x_tick", tick) for tick in ax.get_xticklabels())
        text_artists.extend(("y_tick", tick) for tick in ax.get_yticklabels())
        text_artists.extend(("annotation", text) for text in ax.texts)

        legend = ax.get_legend()
        if legend:
            text_artists.extend(("legend", text) for text in legend.get_texts())
            text_artists.append(("legend_title", legend.get_title()))
        text_artists.extend(("descendant_text", text) for text in ax.findobj(match=lambda artist: isinstance(artist, Text)))

        seen_ids: set[int] = set()

        for kind, artist in text_artists:
            if id(artist) in seen_ids:
                continue
            seen_ids.add(id(artist))
            if not is_visible_text(artist):
                continue
            content = artist.get_text()
            boxes.append(
                TextBox(
                    chart_name=chart_name,
                    axes_label=axes_label,
                    kind=kind,
                    text=content.strip(),
                    bbox=artist_bbox_tuple(artist, renderer),
                )
            )

    for idx, text in enumerate(fig.texts):
        if not is_visible_text(text):
            continue
        boxes.append(
            TextBox(
                chart_name=chart_name,
                axes_label=f"figure_text_{idx}",
                kind="figure_text",
                text=text.get_text().strip(),
                bbox=artist_bbox_tuple(text, renderer),
            )
        )

    return boxes, axes_boxes


def write_layout_report(fig: plt.Figure, chart_name: str) -> list[dict[str, object]]:
    LAYOUT_CHECKS.mkdir(parents=True, exist_ok=True)
    boxes, axes_boxes = collect_text_boxes(fig, chart_name)
    findings: list[dict[str, object]] = []

    for box in boxes:
        for axes_label, axes_bbox in axes_boxes.items():
            if axes_label == box.axes_label:
                continue
            overlap_width, overlap_height, overlap_area = bbox_overlap_metrics(box.bbox, axes_bbox)
            overlap_ratio = overlap_area / max(bbox_area(box.bbox), 1.0)
            if overlap_area < 24 or overlap_ratio < 0.10 or overlap_width < 3 or overlap_height < 3:
                continue
            findings.append(
                {
                    "chart": chart_name,
                    "type": "text_overlaps_other_axes",
                    "source_axes": box.axes_label,
                    "target_axes": axes_label,
                    "kind": box.kind,
                    "text": box.text,
                    "overlap_area": round(overlap_area, 1),
                    "overlap_ratio": round(overlap_ratio, 3),
                }
            )

    for idx, first in enumerate(boxes):
        for second in boxes[idx + 1 :]:
            if first.axes_label == second.axes_label:
                continue
            overlap_width, overlap_height, overlap_area = bbox_overlap_metrics(first.bbox, second.bbox)
            overlap_ratio = overlap_area / max(min(bbox_area(first.bbox), bbox_area(second.bbox)), 1.0)
            if overlap_area < 90 or overlap_ratio < 0.20 or overlap_width < 3 or overlap_height < 3:
                continue
            findings.append(
                {
                    "chart": chart_name,
                    "type": "text_overlaps_text",
                    "source_axes": first.axes_label,
                    "target_axes": second.axes_label,
                    "kind": f"{first.kind}/{second.kind}",
                    "text": f"{trim_label(first.text, 28)} <> {trim_label(second.text, 28)}",
                    "overlap_area": round(overlap_area, 1),
                    "overlap_ratio": round(overlap_ratio, 3),
                }
            )

    report_path = LAYOUT_CHECKS / f"{chart_name}_layout_report.json"
    report_path.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")

    if findings:
        lines = [f"# Layout Report: {chart_name}", "", f"- Findings: {len(findings)}", ""]
        for item in findings[:20]:
            lines.append(
                f"- `{item['type']}` {item['source_axes']} -> {item['target_axes']} | {item['kind']} | {item['text']} | overlap={item['overlap_area']} | ratio={item['overlap_ratio']}"
            )
    else:
        lines = [f"# Layout Report: {chart_name}", "", "- Findings: 0", "", "- No static text overlap candidates detected."]
    (LAYOUT_CHECKS / f"{chart_name}_layout_report.md").write_text("\n".join(lines), encoding="utf-8")
    return findings


def render_dashboard(data: dict[str, pd.DataFrame | dict]) -> int:
    summary = data["summary"]
    messages = data["messages"]
    users = data["users"]
    categories = data["categories"]
    projects = data["projects"]
    tools = data["tools"]

    CHARTS.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(19, 13))
    gs = GridSpec(14, 12, figure=fig)
    fig.suptitle("Agent Interaction Analysis Dashboard", fontsize=22, fontweight="bold", color="#2E2A26")
    fig.subplots_adjust(left=0.06, right=0.985, top=0.93, bottom=0.05, wspace=0.82, hspace=1.22)

    cards = [
        ("Messages", format_compact_number(summary["message_count"]), "Normalized transcript rows", "#7C5C3B"),
        ("User Prompts", format_compact_number(summary["user_message_count"]), "Human-authored requests", "#A25D3D"),
        ("Sessions", format_compact_number(summary["session_count"]), "Distinct session / thread ids", "#336B6B"),
        ("Tool Calls", format_compact_number(summary["tool_invocation_count"]), "Captured assistant tool invocations", "#495C83"),
    ]

    card_axes = [
        fig.add_subplot(gs[0:2, 0:3]),
        fig.add_subplot(gs[0:2, 3:6]),
        fig.add_subplot(gs[0:2, 6:9]),
        fig.add_subplot(gs[0:2, 9:12]),
    ]
    for ax, (title, value, subtitle, color) in zip(card_axes, cards, strict=True):
        add_card(ax, title, value, subtitle, color)

    hourly = users.groupby("hour_jst").size().reindex(range(24), fill_value=0).reset_index(name="user_messages")
    ax_hourly = fig.add_subplot(gs[2:6, 0:8])
    ax_hourly.fill_between(hourly["hour_jst"], hourly["user_messages"], color="#E4B363", alpha=0.45)
    ax_hourly.plot(hourly["hour_jst"], hourly["user_messages"], color="#9C5E2F", linewidth=2.5)
    peak_row = hourly.loc[hourly["user_messages"].idxmax()]
    ax_hourly.scatter([peak_row["hour_jst"]], [peak_row["user_messages"]], color="#7C2D12", s=70, zorder=3)
    ax_hourly.annotate(
        f"Peak {int(peak_row['hour_jst'])}:00\n{int(peak_row['user_messages'])} msgs",
        (peak_row["hour_jst"], peak_row["user_messages"]),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "fc": "#FFF4DE", "ec": "#D9B679"},
    )
    ax_hourly.set_title("User Activity by Hour (JST)")
    ax_hourly.set_xlabel("Hour")
    ax_hourly.set_ylabel("User messages")
    ax_hourly.set_xticks(range(0, 24, 2))
    ax_hourly.grid(axis="y", linestyle=":")

    ax_lang = fig.add_subplot(gs[2:6, 8:12])
    lang = users.groupby("language").size().sort_values(ascending=True)
    lang_df = lang.reset_index(name="user_messages")
    lang_df["share_pct"] = (lang_df["user_messages"] / max(lang_df["user_messages"].sum(), 1) * 100).round(1)
    lang_colors = ["#B8A99A", "#7FB069", "#C06C54", "#4F6D7A"]
    ax_lang.barh(lang_df["language"], lang_df["share_pct"], color=lang_colors[: len(lang_df)])
    ax_lang.set_title("Language Mix")
    ax_lang.grid(axis="x", linestyle=":")
    for idx, row in lang_df.iterrows():
        ax_lang.text(row["share_pct"] + 0.6, idx, f"{row['share_pct']:.1f}%", va="center", fontsize=9)

    ax_categories = fig.add_subplot(gs[6:10, 0:3])
    categories_plot = categories.head(7).iloc[::-1]
    bar_colors = ["#CBB89D" if cat == "other" else "#5C7AEA" for cat in categories_plot["category"]]
    ax_categories.barh(categories_plot["category"], categories_plot["share_pct"], color=bar_colors)
    ax_categories.set_title("Top User Request Categories")
    ax_categories.grid(axis="x", linestyle=":")
    for idx, value in enumerate(categories_plot["share_pct"]):
        ax_categories.text(value + 0.35, idx, f"{value:.1f}%", va="center", fontsize=9, color="#2E2A26")

    ax_projects = fig.add_subplot(gs[6:10, 4:8])
    projects_plot = projects.head(8).iloc[::-1].copy()
    projects_plot["label"] = projects_plot["project_or_title"].map(lambda value: trim_label(value, width=20))
    project_colors = projects_plot["agent_family"].map({"codex": "#4F6D7A", "claude": "#C06C54"}).fillna("#8E8E8E")
    ax_projects.barh(projects_plot["label"], projects_plot["user_messages"], color=project_colors)
    ax_projects.set_title("Projects With The Most User Prompts")
    ax_projects.tick_params(axis="y", labelsize=9, pad=2)
    ax_projects.grid(axis="x", linestyle=":")

    ax_source = fig.add_subplot(gs[6:10, 9:12])
    source_mix = (
        messages.groupby(["agent_family", "origin", "role"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    source_mix["label"] = source_mix.apply(
        lambda row: shorten_origin(row["agent_family"], row["origin"]),
        axis=1,
    )
    source_mix["label"] = source_mix["label"].map(lambda value: trim_label(value, width=16))
    source_mix["total_messages"] = source_mix.get("assistant", 0) + source_mix.get("user", 0)
    source_mix = source_mix.sort_values("total_messages", ascending=False)
    source_mix = source_mix.head(4)
    ax_source.barh(source_mix["label"], source_mix.get("assistant", 0), color="#8D99AE", label="assistant")
    ax_source.barh(
        source_mix["label"],
        source_mix.get("user", 0),
        color="#D17A5C",
        label="user",
    )
    ax_source.set_title("Message Volume by Source")
    ax_source.tick_params(axis="y", labelsize=9, pad=2)
    ax_source.legend(frameon=False, loc="upper left")
    ax_source.grid(axis="x", linestyle=":")

    ax_tools = fig.add_subplot(gs[10:14, 0:6])
    tools_plot = tools.head(8).iloc[::-1].copy()
    tools_plot["label"] = tools_plot["tool_name"].map(lambda value: trim_label(value, width=22))
    tool_colors = tools_plot["agent_family"].map({"codex": "#495C83", "claude": "#A25D3D"}).fillna("#8E8E8E")
    ax_tools.barh(tools_plot["label"], tools_plot["invocations"], color=tool_colors)
    ax_tools.set_title("Most Used Tools")
    ax_tools.grid(axis="x", linestyle=":")

    ax_notes = fig.add_subplot(gs[10:14, 6:12])
    ax_notes.set_xticks([])
    ax_notes.set_yticks([])
    for spine in ax_notes.spines.values():
        spine.set_visible(False)
    ax_notes.set_facecolor("#F1E3C6")
    notes = (
        "Read as exploratory analysis.\n"
        f"- Mixed-language prompts dominate at {lang_df.iloc[-1]['share_pct']:.1f}%.\n"
        f"- Peak hour is {int(peak_row['hour_jst']):02d}:00 JST with {int(peak_row['user_messages'])} prompts.\n"
        f"- Strongest labeled genre is {categories.iloc[1]['category']} ({categories.iloc[1]['share_pct']:.1f}%) after `other`.\n"
        "- Claude snapshot coverage is much richer in prox than kali.\n"
        "- Token usage is charted separately to avoid label crowding."
    )
    ax_notes.text(0.04, 0.88, "Interpretation Notes", fontsize=14, fontweight="bold", color="#4B382A", transform=ax_notes.transAxes)
    ax_notes.text(0.04, 0.72, notes, fontsize=11, color="#4B382A", transform=ax_notes.transAxes, va="top")

    findings = write_layout_report(fig, "dashboard_overview")
    dashboard_path = CHARTS / "dashboard_overview.png"
    fig.savefig(dashboard_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return len(findings)


def render_token_dashboard(data: dict[str, pd.DataFrame | dict]) -> int:
    summary = data["summary"]
    token_by_source = data["token_by_source"].copy()
    top_token_sessions = data["top_token_sessions"].copy()

    token_by_source["label"] = token_by_source.apply(
        lambda row: shorten_origin(row["agent_family"], row["origin"]),
        axis=1,
    )
    token_by_source = token_by_source.sort_values("total_tokens", ascending=False)
    top_token_sessions["label"] = top_token_sessions["project_or_title"].map(lambda value: trim_label(value, width=32))
    top_token_sessions = top_token_sessions.head(8).iloc[::-1]

    fig = plt.figure(figsize=(18, 11))
    gs = GridSpec(10, 12, figure=fig)
    fig.suptitle("Token Usage Dashboard", fontsize=22, fontweight="bold", color="#2E2A26")
    fig.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.07, wspace=0.80, hspace=1.18)

    cards = [
        ("Tracked Tokens", format_compact_number(summary.get("total_tracked_tokens", 0)), "Sessions with token data", "#6C4A4A"),
        ("Token Sessions", format_compact_number(summary.get("token_session_count", 0)), "Claude + Codex sessions", "#2F5D62"),
        (
            "Top Token Source",
            trim_label(token_by_source.iloc[0]["label"], 18),
            f"{format_compact_number(int(token_by_source.iloc[0]['total_tokens']))} total tokens",
            "#7A5C61",
        ),
    ]
    axes = [
        fig.add_subplot(gs[0:2, 0:4]),
        fig.add_subplot(gs[0:2, 4:8]),
        fig.add_subplot(gs[0:2, 8:12]),
    ]
    for ax, (title, value, subtitle, color) in zip(axes, cards, strict=True):
        add_card(ax, title, value, subtitle, color)

    ax_source = fig.add_subplot(gs[2:6, 0:5])
    source_plot = token_by_source.head(6).iloc[::-1].copy()
    source_plot["label"] = source_plot["label"].map(lambda value: trim_label(value, width=16))
    colors = source_plot["agent_family"].map({"codex": "#4F6D7A", "claude": "#C06C54"}).fillna("#8E8E8E")
    ax_source.barh(source_plot["label"], source_plot["total_tokens"] / 1_000_000, color=colors)
    ax_source.set_title("Total Tokens by Source")
    ax_source.tick_params(axis="y", labelsize=9, pad=2)
    ax_source.grid(axis="x", linestyle=":")
    for idx, value in enumerate(source_plot["total_tokens"] / 1_000_000):
        ax_source.text(value + 0.05, idx, f"{value:.1f}M", va="center", fontsize=9)

    ax_avg = fig.add_subplot(gs[2:6, 7:12])
    avg_plot = token_by_source.head(6).iloc[::-1].copy()
    avg_plot["label"] = avg_plot["label"].map(lambda value: trim_label(value, width=16))
    ax_avg.barh(avg_plot["label"], avg_plot["avg_tokens_per_session"] / 1000, color="#7C90A0")
    ax_avg.set_title("Average Tokens per Session")
    ax_avg.tick_params(axis="y", labelsize=9, pad=2)
    ax_avg.grid(axis="x", linestyle=":")
    for idx, value in enumerate(avg_plot["avg_tokens_per_session"] / 1000):
        ax_avg.text(value + 0.2, idx, f"{value:.1f}k", va="center", fontsize=9)

    ax_top = fig.add_subplot(gs[6:10, 0:7])
    top_colors = top_token_sessions["agent_family"].map({"codex": "#4F6D7A", "claude": "#C06C54"}).fillna("#8E8E8E")
    ax_top.barh(top_token_sessions["label"], top_token_sessions["total_tokens"] / 1_000_000, color=top_colors)
    ax_top.set_title("Most Token-Heavy Sessions")
    ax_top.tick_params(axis="y", labelsize=9, pad=2)
    ax_top.grid(axis="x", linestyle=":")

    ax_mix = fig.add_subplot(gs[6:10, 8:12])
    mix = (
        token_by_source.groupby("agent_family")[["input_tokens", "cached_input_tokens", "output_tokens"]]
        .sum()
        .reset_index()
    )
    mix = mix[mix["agent_family"].isin(["claude", "codex"])].copy()
    if not mix.empty:
        x = range(len(mix))
        width = 0.22
        ax_mix.bar([pos - width for pos in x], mix["input_tokens"] / 1_000_000, width=width, color="#5C7AEA", label="input")
        ax_mix.bar(x, mix["cached_input_tokens"] / 1_000_000, width=width, color="#9BC1BC", label="cached input")
        ax_mix.bar([pos + width for pos in x], mix["output_tokens"] / 1_000_000, width=width, color="#E07A5F", label="output")
        ax_mix.set_xticks(list(x))
        ax_mix.set_xticklabels([agent.title() for agent in mix["agent_family"]])
        ax_mix.set_title("Token Composition by Family")
        ax_mix.legend(frameon=False, loc="upper right")
        ax_mix.grid(axis="y", linestyle=":")

    findings = write_layout_report(fig, "token_usage_dashboard")
    fig.savefig(CHARTS / "token_usage_dashboard.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return len(findings)


def render_source_artifacts(data: dict[str, pd.DataFrame | dict]) -> int:
    inventory = data["inventory"].fillna(0)
    claude_inventory = inventory[inventory["agent_family"] == "claude"].copy()
    if claude_inventory.empty:
        return

    metric_columns = [
        "project_jsonl_count",
        "subagent_jsonl_count",
        "team_config_count",
        "task_json_count",
        "todo_json_count",
    ]
    labels = [trim_label(origin.replace("data_snapshot:", "snapshot:"), width=26) for origin in claude_inventory["origin"]]
    x = range(len(labels))
    width = 0.16
    colors = ["#B56576", "#6D597A", "#355070", "#43AA8B", "#F4A261"]

    fig, ax = plt.subplots(figsize=(14, 6))
    for idx, (column, color) in enumerate(zip(metric_columns, colors, strict=True)):
        positions = [pos + (idx - 2) * width for pos in x]
        ax.bar(positions, claude_inventory[column], width=width, label=column.replace("_count", ""), color=color)

    ax.set_title("Claude Source Artifacts by Root")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("File count")
    ax.legend(frameon=False, ncol=3, loc="upper left")
    ax.grid(axis="y", linestyle=":")
    fig.tight_layout()
    findings = write_layout_report(fig, "source_artifacts")
    fig.savefig(CHARTS / "source_artifacts.png", dpi=180)
    plt.close(fig)
    return len(findings)


def write_visual_summary(data: dict[str, pd.DataFrame | dict], layout_counts: dict[str, int]) -> None:
    summary = data["summary"]
    text = f"""# Visual Summary

- Messages: {summary['message_count']:,}
- User prompts: {summary['user_message_count']:,}
- Sessions: {summary['session_count']:,}
- Tool calls: {summary['tool_invocation_count']:,}

Charts:
- `outputs/charts/dashboard_overview.png`
- `outputs/charts/token_usage_dashboard.png`
- `outputs/charts/source_artifacts.png`
- existing detail charts remain in `outputs/charts/`

Layout checks:
- `dashboard_overview`: {layout_counts.get('dashboard_overview', 0)} findings
- `token_usage_dashboard`: {layout_counts.get('token_usage_dashboard', 0)} findings
- `source_artifacts`: {layout_counts.get('source_artifacts', 0)} findings
- reports live in `outputs/layout_checks/`
"""
    (OUTPUTS / "visual_summary.md").write_text(text, encoding="utf-8")


def main() -> None:
    setup_style()
    data = load_data()
    layout_counts = {
        "dashboard_overview": render_dashboard(data),
        "token_usage_dashboard": render_token_dashboard(data),
        "source_artifacts": render_source_artifacts(data),
    }
    (LAYOUT_CHECKS / "layout_summary.json").write_text(
        json.dumps(layout_counts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_visual_summary(data, layout_counts)
    print(f"Rendered dashboard assets in {CHARTS}")


if __name__ == "__main__":
    main()
