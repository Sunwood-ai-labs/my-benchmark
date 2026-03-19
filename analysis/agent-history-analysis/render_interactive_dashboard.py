from __future__ import annotations

import html
import json
import textwrap
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
HTML_PATH = OUTPUTS / "interactive_dashboard.html"
SUMMARY_PATH = OUTPUTS / "interactive_summary.md"
LAYOUT_CHECKS = OUTPUTS / "layout_checks"

PAGE_BG = "#f6efe3"
PANEL_BG = "#fffaf0"
INK = "#2f261d"
MUTED = "#6a5d50"
GRID = "#d8cbb5"
ACCENT = "#9c5e2f"
CLAUDE = "#c06c54"
CODEX = "#4f6d7a"
NEUTRAL = "#b8a99a"
SUCCESS = "#5b8a72"


def trim_label(value: str, width: int = 28) -> str:
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


def chart_layout(title: str, height: int = 360) -> dict:
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "paper_bgcolor": PANEL_BG,
        "plot_bgcolor": PANEL_BG,
        "font": {"family": "Aptos, 'Segoe UI', 'Yu Gothic UI', sans-serif", "color": INK, "size": 13},
        "margin": {"l": 64, "r": 28, "t": 56, "b": 48},
        "height": height,
        "hoverlabel": {"bgcolor": "#fff7ea", "font": {"color": INK}},
    }


def load_data() -> dict[str, pd.DataFrame | dict]:
    return {
        "summary": json.loads((OUTPUTS / "analysis_summary.json").read_text(encoding="utf-8")),
        "messages": pd.read_csv(OUTPUTS / "messages_normalized.csv.gz", low_memory=False),
        "users": pd.read_csv(OUTPUTS / "user_messages.csv.gz", low_memory=False),
        "categories": pd.read_csv(OUTPUTS / "top_categories.csv"),
        "projects": pd.read_csv(OUTPUTS / "top_projects.csv"),
        "tools": pd.read_csv(OUTPUTS / "top_tools.csv"),
        "inventory": pd.read_csv(OUTPUTS / "source_inventory.csv"),
        "sessions": pd.read_csv(OUTPUTS / "session_summary.csv", low_memory=False),
        "token_by_source": pd.read_csv(OUTPUTS / "token_usage_by_source.csv"),
        "top_token_sessions": pd.read_csv(OUTPUTS / "top_token_sessions.csv", low_memory=False),
        "layout_summary": json.loads((LAYOUT_CHECKS / "layout_summary.json").read_text(encoding="utf-8")),
    }


def fig_to_html(fig: go.Figure, include_plotlyjs: bool) -> str:
    return pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs="inline" if include_plotlyjs else False,
        config={
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
        },
    )


def build_hourly_chart(users: pd.DataFrame) -> go.Figure:
    hourly = users.groupby("hour_jst").size().reindex(range(24), fill_value=0).reset_index(name="user_messages")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=hourly["hour_jst"],
            y=hourly["user_messages"],
            mode="lines+markers",
            line={"color": ACCENT, "width": 3},
            fill="tozeroy",
            fillcolor="rgba(228,179,99,0.35)",
            marker={"size": 7, "color": "#7c2d12"},
            hovertemplate="Hour %{x}:00 JST<br>User prompts %{y}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("User Activity by Hour (JST)", height=360))
    fig.update_xaxes(title="Hour", tickmode="linear", dtick=2, gridcolor=GRID)
    fig.update_yaxes(title="User prompts", gridcolor=GRID)
    return fig


def build_daily_chart(users: pd.DataFrame) -> go.Figure:
    daily = users.groupby("date_jst").size().reset_index(name="user_messages")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["date_jst"],
            y=daily["user_messages"],
            mode="lines",
            line={"color": "#7c90a0", "width": 2.5},
            fill="tozeroy",
            fillcolor="rgba(124,144,160,0.22)",
            hovertemplate="%{x}<br>User prompts %{y}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Prompt Timeline by Day", height=320))
    fig.update_xaxes(title="Date (JST)", gridcolor=GRID)
    fig.update_yaxes(title="User prompts", gridcolor=GRID)
    return fig


def build_language_chart(users: pd.DataFrame) -> go.Figure:
    lang = users.groupby("language").size().sort_values(ascending=True).reset_index(name="user_messages")
    lang["share_pct"] = lang["user_messages"] / max(lang["user_messages"].sum(), 1) * 100
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=lang["share_pct"],
            y=lang["language"],
            orientation="h",
            marker={"color": [NEUTRAL, "#83b26b", CLAUDE, CODEX][: len(lang)]},
            customdata=lang["user_messages"],
            text=[f"{value:.1f}%" for value in lang["share_pct"]],
            textposition="outside",
            hovertemplate="%{y}<br>Share %{x:.1f}%<br>User prompts %{customdata}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Language Mix", height=320))
    fig.update_xaxes(title="Share of user prompts (%)", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_category_chart(categories: pd.DataFrame) -> go.Figure:
    plot = categories.head(8).iloc[::-1].copy()
    colors = [NEUTRAL if item == "other" else "#5c7aea" for item in plot["category"]]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot["share_pct"],
            y=plot["category"],
            orientation="h",
            marker={"color": colors},
            customdata=plot[["user_messages", "avg_chars"]],
            text=[f"{value:.1f}%" for value in plot["share_pct"]],
            textposition="outside",
            hovertemplate="%{y}<br>Share %{x:.1f}%<br>User prompts %{customdata[0]}<br>Avg chars %{customdata[1]:.1f}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Top User Request Categories", height=360))
    fig.update_xaxes(title="Share of prompts (%)", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_prompt_length_chart(users: pd.DataFrame) -> go.Figure:
    top_categories = users["category"].value_counts().head(6).index.tolist()
    plot = users[users["category"].isin(top_categories)].copy()
    plot["category"] = pd.Categorical(plot["category"], categories=top_categories, ordered=True)
    fig = go.Figure()
    for category in top_categories:
        subset = plot[plot["category"] == category]
        fig.add_trace(
            go.Box(
                y=subset["char_count"],
                name=category,
                boxpoints=False,
                marker_color="#7c90a0" if category == "other" else "#c06c54",
                hovertemplate=f"{category}<br>Chars %{{y}}<extra></extra>",
            )
        )
    fig.update_layout(**chart_layout("Prompt Length by Category", height=320))
    fig.update_yaxes(title="Characters per prompt", gridcolor=GRID)
    return fig


def build_projects_chart(projects: pd.DataFrame) -> go.Figure:
    plot = projects.head(10).iloc[::-1].copy()
    plot["label"] = plot["project_or_title"].map(lambda value: trim_label(value, 22))
    colors = plot["agent_family"].map({"codex": CODEX, "claude": CLAUDE}).fillna(NEUTRAL)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot["user_messages"],
            y=plot["label"],
            orientation="h",
            marker={"color": colors},
            customdata=plot[["project_or_title", "avg_chars", "origin"]],
            hovertemplate="%{customdata[0]}<br>User prompts %{x}<br>Avg chars %{customdata[1]:.1f}<br>%{customdata[2]}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Projects With The Most User Prompts", height=380))
    fig.update_xaxes(title="User prompts", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_session_scatter_chart(sessions: pd.DataFrame) -> go.Figure:
    plot = sessions.copy()
    plot["duration_minutes"] = plot["duration_minutes"].fillna(0.1).clip(lower=0.1)
    plot["total_messages"] = plot["total_messages"].fillna(1).clip(lower=1)
    plot["user_messages"] = plot["user_messages"].fillna(1).clip(lower=1, upper=60)
    plot["label"] = plot["project_name"].fillna(plot["thread_title"]).fillna("untitled").map(lambda value: trim_label(value, 28))
    colors = plot["agent_family"].map({"codex": CODEX, "claude": CLAUDE}).fillna(NEUTRAL)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=plot["duration_minutes"],
            y=plot["total_messages"],
            mode="markers",
            marker={
                "color": colors,
                "size": plot["user_messages"],
                "sizemode": "diameter",
                "line": {"width": 0.5, "color": "rgba(47,38,29,0.25)"},
                "opacity": 0.78,
            },
            customdata=plot[["label", "session_id", "origin", "user_messages", "assistant_messages"]],
            hovertemplate=(
                "%{customdata[0]}<br>"
                "Duration %{x:.1f} min<br>"
                "Messages %{y}<br>"
                "User %{customdata[3]} / Assistant %{customdata[4]}<br>"
                "%{customdata[2]}<br>"
                "%{customdata[1]}<extra></extra>"
            ),
        )
    )
    fig.update_layout(**chart_layout("Session Duration vs Message Volume", height=420))
    fig.update_xaxes(title="Duration (minutes, log scale)", type="log", gridcolor=GRID)
    fig.update_yaxes(title="Total messages (log scale)", type="log", gridcolor=GRID)
    return fig


def build_source_mix_chart(messages: pd.DataFrame) -> go.Figure:
    plot = (
        messages.groupby(["agent_family", "origin", "role"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    plot["label"] = plot.apply(lambda row: shorten_origin(row["agent_family"], row["origin"]), axis=1)
    plot["label"] = plot["label"].map(lambda value: trim_label(value, 18))
    plot["total_messages"] = plot.get("assistant", 0) + plot.get("user", 0)
    plot = plot.sort_values("total_messages", ascending=False).head(6).iloc[::-1]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot.get("assistant", 0),
            y=plot["label"],
            orientation="h",
            name="assistant",
            marker={"color": "#8d99ae"},
            hovertemplate="%{y}<br>Assistant messages %{x}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=plot.get("user", 0),
            y=plot["label"],
            orientation="h",
            name="user",
            marker={"color": "#d17a5c"},
            hovertemplate="%{y}<br>User messages %{x}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Message Volume by Source", height=380), barmode="stack")
    fig.update_xaxes(title="Messages", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_tools_chart(tools: pd.DataFrame) -> go.Figure:
    plot = tools.head(10).iloc[::-1].copy()
    plot["label"] = plot["tool_name"].map(lambda value: trim_label(value, 24))
    colors = plot["agent_family"].map({"codex": "#495c83", "claude": "#a25d3d"}).fillna(NEUTRAL)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot["invocations"],
            y=plot["label"],
            orientation="h",
            marker={"color": colors},
            customdata=plot["agent_family"],
            hovertemplate="%{y}<br>Invocations %{x}<br>Family %{customdata}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Most Used Tools", height=360))
    fig.update_xaxes(title="Invocations", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_token_source_chart(token_by_source: pd.DataFrame) -> go.Figure:
    plot = token_by_source.copy()
    plot["label"] = plot.apply(lambda row: shorten_origin(row["agent_family"], row["origin"]), axis=1)
    plot["label"] = plot["label"].map(lambda value: trim_label(value, 18))
    plot = plot.sort_values("total_tokens", ascending=False).head(6).iloc[::-1]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot["total_tokens"] / 1_000_000,
            y=plot["label"],
            orientation="h",
            name="Total tokens",
            marker={"color": CODEX},
            customdata=plot[["sessions", "avg_tokens_per_session"]],
            hovertemplate="%{y}<br>Total %{x:.1f}M tokens<br>Sessions %{customdata[0]}<br>Avg/session %{customdata[1]:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Total Tokens by Source", height=360))
    fig.update_xaxes(title="Million tokens", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_token_average_chart(token_by_source: pd.DataFrame) -> go.Figure:
    plot = token_by_source.copy()
    plot["label"] = plot.apply(lambda row: shorten_origin(row["agent_family"], row["origin"]), axis=1)
    plot["label"] = plot["label"].map(lambda value: trim_label(value, 18))
    plot = plot.sort_values("avg_tokens_per_session", ascending=False).head(6).iloc[::-1]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot["avg_tokens_per_session"] / 1000,
            y=plot["label"],
            orientation="h",
            marker={"color": "#7c90a0"},
            customdata=plot[["sessions", "total_tokens"]],
            hovertemplate="%{y}<br>Avg/session %{x:.1f}k tokens<br>Sessions %{customdata[0]}<br>Total %{customdata[1]:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Average Tokens per Session", height=360))
    fig.update_xaxes(title="Thousand tokens per session", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_token_sessions_chart(top_token_sessions: pd.DataFrame) -> go.Figure:
    plot = top_token_sessions.head(12).iloc[::-1].copy()
    plot["label"] = plot["project_or_title"].fillna(plot["thread_title"]).map(lambda value: trim_label(value, 28))
    colors = plot["agent_family"].map({"codex": CODEX, "claude": CLAUDE}).fillna(NEUTRAL)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot["total_tokens"] / 1_000_000,
            y=plot["label"],
            orientation="h",
            marker={"color": colors},
            customdata=plot[["token_source", "first_timestamp", "session_id"]],
            hovertemplate="%{y}<br>Total %{x:.1f}M tokens<br>Source %{customdata[0]}<br>Started %{customdata[1]}<br>%{customdata[2]}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Most Token-Heavy Sessions", height=420))
    fig.update_xaxes(title="Million tokens", gridcolor=GRID)
    fig.update_yaxes(title=None)
    return fig


def build_token_composition_chart(token_by_source: pd.DataFrame) -> go.Figure:
    plot = (
        token_by_source.groupby("agent_family")[["input_tokens", "cached_input_tokens", "output_tokens"]]
        .sum()
        .reset_index()
    )
    plot = plot[plot["agent_family"].isin(["claude", "codex"])].copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=plot["agent_family"], y=plot["input_tokens"] / 1_000_000, name="input", marker={"color": "#5c7aea"}))
    fig.add_trace(
        go.Bar(
            x=plot["agent_family"],
            y=plot["cached_input_tokens"] / 1_000_000,
            name="cached input",
            marker={"color": "#9bc1bc"},
        )
    )
    fig.add_trace(go.Bar(x=plot["agent_family"], y=plot["output_tokens"] / 1_000_000, name="output", marker={"color": "#e07a5f"}))
    fig.update_layout(**chart_layout("Token Composition by Family", height=420), barmode="group")
    fig.update_xaxes(title=None)
    fig.update_yaxes(title="Million tokens", gridcolor=GRID)
    return fig


def build_inventory_chart(inventory: pd.DataFrame) -> go.Figure:
    plot = inventory.copy().fillna(0)
    plot["label"] = plot.apply(lambda row: shorten_origin(row["agent_family"], row["origin"]), axis=1)
    plot["label"] = plot["label"].map(lambda value: trim_label(value, 20))
    plot["artifact_total"] = (
        plot["project_jsonl_count"]
        + plot["subagent_jsonl_count"]
        + plot["team_config_count"]
        + plot["task_json_count"]
        + plot["todo_json_count"]
        + plot["session_jsonl_count"]
    )
    plot = plot.sort_values("artifact_total", ascending=False).head(6)
    fig = go.Figure()
    metrics = [
        ("project_jsonl_count", "projects", "#b56576"),
        ("subagent_jsonl_count", "subagents", "#6d597a"),
        ("todo_json_count", "todo", "#43aa8b"),
        ("session_jsonl_count", "sessions", "#355070"),
    ]
    for column, label, color in metrics:
        fig.add_trace(
            go.Bar(
                x=plot["label"],
                y=plot[column],
                name=label,
                marker={"color": color},
            )
        )
    fig.update_layout(**chart_layout("Source Artifact Inventory", height=360), barmode="group")
    fig.update_xaxes(title=None)
    fig.update_yaxes(title="File count", gridcolor=GRID)
    return fig


def build_layout_chart(layout_summary: dict[str, int]) -> go.Figure:
    labels = list(layout_summary.keys())
    values = list(layout_summary.values())
    colors = [SUCCESS if value == 0 else CLAUDE for value in values]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            marker={"color": colors},
            text=[str(value) for value in values],
            textposition="outside",
            hovertemplate="%{x}<br>Static overlap findings %{y}<extra></extra>",
        )
    )
    fig.update_layout(**chart_layout("Static Layout Checks", height=320))
    fig.update_xaxes(title=None)
    fig.update_yaxes(title="Findings", gridcolor=GRID)
    return fig


def build_cards(summary: dict, token_by_source: pd.DataFrame) -> str:
    top_source = token_by_source.sort_values("total_tokens", ascending=False).iloc[0]
    cards = [
        ("Messages", format_compact_number(summary["message_count"]), "Normalized transcript rows", f"{summary['message_count']:,}"),
        ("User Prompts", format_compact_number(summary["user_message_count"]), "Human-authored requests", f"{summary['user_message_count']:,}"),
        ("Sessions", format_compact_number(summary["session_count"]), "Distinct session or thread ids", f"{summary['session_count']:,}"),
        ("Tracked Tokens", format_compact_number(summary.get("total_tracked_tokens", 0)), "Sessions with token usage", f"{summary.get('total_tracked_tokens', 0):,}"),
        ("Token Sessions", format_compact_number(summary.get("token_session_count", 0)), "Claude + Codex sessions", f"{summary.get('token_session_count', 0):,}"),
        (
            "Top Token Source",
            html.escape(shorten_origin(top_source["agent_family"], top_source["origin"])),
            f"{format_compact_number(int(top_source['total_tokens']))} total tokens",
            f"{int(top_source['total_tokens']):,} total tokens",
        ),
    ]
    chunks = []
    for title, value, subtitle, exact_value in cards:
        chunks.append(
            f"""
            <article class="stat-card">
              <p class="eyebrow">{title}</p>
              <h3 title="{html.escape(exact_value)}">{value}</h3>
              <p class="subtitle">{subtitle}</p>
            </article>
            """
        )
    return "\n".join(chunks)


def build_top_sessions_table(top_token_sessions: pd.DataFrame) -> str:
    rows = []
    for item in top_token_sessions.head(12).itertuples():
        rows.append(
            f"""
            <tr>
              <td>{html.escape(trim_label(getattr(item, 'project_or_title', '') or getattr(item, 'thread_title', ''), 42))}</td>
              <td>{html.escape(item.agent_family)}</td>
              <td>{html.escape(shorten_origin(item.agent_family, item.origin))}</td>
              <td>{item.total_tokens:,}</td>
              <td>{item.input_tokens:,}</td>
              <td>{item.output_tokens:,}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def write_summary(data: dict[str, pd.DataFrame | dict]) -> None:
    summary = data["summary"]
    lines = [
        "# Interactive Summary",
        "",
        f"- HTML: `outputs/interactive_dashboard.html`",
        f"- Messages: {summary['message_count']:,}",
        f"- User prompts: {summary['user_message_count']:,}",
        f"- Sessions: {summary['session_count']:,}",
        f"- Tracked tokens: {summary.get('total_tracked_tokens', 0):,}",
        f"- Layout checks: `outputs/layout_checks/layout_summary.json`",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_html(data: dict[str, pd.DataFrame | dict]) -> str:
    summary = data["summary"]
    messages = data["messages"]
    users = data["users"]
    categories = data["categories"]
    projects = data["projects"]
    tools = data["tools"]
    inventory = data["inventory"]
    sessions = data["sessions"]
    token_by_source = data["token_by_source"]
    top_token_sessions = data["top_token_sessions"]
    layout_summary = data["layout_summary"]

    charts = [
        build_hourly_chart(users),
        build_daily_chart(users),
        build_language_chart(users),
        build_category_chart(categories),
        build_prompt_length_chart(users),
        build_projects_chart(projects),
        build_session_scatter_chart(sessions),
        build_source_mix_chart(messages),
        build_tools_chart(tools),
        build_token_source_chart(token_by_source),
        build_token_average_chart(token_by_source),
        build_token_sessions_chart(top_token_sessions),
        build_token_composition_chart(token_by_source),
        build_inventory_chart(inventory),
        build_layout_chart(layout_summary),
    ]
    chart_html_parts: list[str] = []
    for idx, fig in enumerate(charts):
        chart_html_parts.append(fig_to_html(fig, include_plotlyjs=idx == 0))

    generated = summary.get("generated_at") or "analysis outputs"
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Agent Interaction Interactive Dashboard</title>
  <style>
    :root {{
      --bg: {PAGE_BG};
      --panel: {PANEL_BG};
      --ink: {INK};
      --muted: {MUTED};
      --line: #decdb3;
      --accent: {ACCENT};
      --accent-soft: rgba(156, 94, 47, 0.12);
      --shadow: 0 20px 40px rgba(62, 42, 26, 0.08);
      --radius: 22px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Aptos, "Segoe UI", "Yu Gothic UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(224, 199, 157, 0.42), transparent 30%),
        radial-gradient(circle at 85% 15%, rgba(79, 109, 122, 0.18), transparent 24%),
        linear-gradient(180deg, #f8f1e6 0%, #f3eadb 100%);
    }}
    a {{ color: var(--accent); }}
    .shell {{
      max-width: 1500px;
      margin: 0 auto;
      padding: 28px 24px 48px;
    }}
    .hero {{
      background: linear-gradient(135deg, rgba(255, 250, 240, 0.96), rgba(246, 232, 210, 0.92));
      border: 1px solid var(--line);
      border-radius: 28px;
      box-shadow: var(--shadow);
      padding: 28px;
      margin-bottom: 22px;
    }}
    .hero h1 {{
      margin: 0 0 8px;
      font-size: clamp(28px, 4vw, 42px);
      letter-spacing: -0.03em;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      max-width: 900px;
      line-height: 1.7;
    }}
    .nav {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      padding: 12px 0 18px;
      backdrop-filter: blur(8px);
    }}
    .nav a {{
      text-decoration: none;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255, 250, 240, 0.9);
      border: 1px solid var(--line);
      color: var(--ink);
      font-weight: 600;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .stat-card {{
      background: linear-gradient(160deg, #7c5c3b, #a5653b);
      color: #fffaf0;
      border-radius: var(--radius);
      padding: 20px 22px;
      box-shadow: var(--shadow);
    }}
    .stat-card:nth-child(2) {{ background: linear-gradient(160deg, #a25d3d, #c77952); }}
    .stat-card:nth-child(3) {{ background: linear-gradient(160deg, #336b6b, #478381); }}
    .stat-card:nth-child(4) {{ background: linear-gradient(160deg, #6c4a4a, #8b6262); }}
    .stat-card:nth-child(5) {{ background: linear-gradient(160deg, #2f5d62, #3f7980); }}
    .stat-card:nth-child(6) {{ background: linear-gradient(160deg, #7a5c61, #956e76); }}
    .eyebrow {{
      margin: 0 0 10px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      opacity: 0.85;
    }}
    .stat-card h3 {{
      margin: 0 0 8px;
      font-size: clamp(28px, 4vw, 48px);
      line-height: 1.05;
      letter-spacing: -0.03em;
    }}
    .subtitle {{
      margin: 0;
      color: rgba(255, 248, 236, 0.84);
    }}
    .section {{
      margin-top: 28px;
    }}
    .section-head {{
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: end;
      margin: 0 0 14px;
    }}
    .section-head h2 {{
      margin: 0;
      font-size: clamp(24px, 2vw, 32px);
      letter-spacing: -0.03em;
    }}
    .section-head p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      max-width: 720px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }}
    .panel {{
      background: rgba(255, 250, 240, 0.92);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 12px 12px 8px;
      overflow: hidden;
    }}
    .span-4 {{ grid-column: span 4; }}
    .span-5 {{ grid-column: span 5; }}
    .span-6 {{ grid-column: span 6; }}
    .span-7 {{ grid-column: span 7; }}
    .span-8 {{ grid-column: span 8; }}
    .span-12 {{ grid-column: span 12; }}
    .note-panel {{
      background: linear-gradient(160deg, rgba(255, 250, 240, 0.94), rgba(244, 229, 202, 0.96));
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 18px 20px;
      margin-top: 18px;
    }}
    .note-panel h3 {{
      margin: 0 0 10px;
      font-size: 18px;
    }}
    .note-panel ul {{
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      line-height: 1.7;
    }}
    .table-shell {{
      overflow: auto;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255, 250, 240, 0.92);
      box-shadow: var(--shadow);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 760px;
    }}
    th, td {{
      padding: 12px 14px;
      border-bottom: 1px solid rgba(222, 205, 179, 0.7);
      text-align: left;
    }}
    th {{
      background: rgba(156, 94, 47, 0.08);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    td {{
      color: var(--muted);
    }}
    footer {{
      margin-top: 28px;
      color: var(--muted);
      font-size: 13px;
    }}
    @media (max-width: 1100px) {{
      .span-4, .span-5, .span-6, .span-7, .span-8 {{ grid-column: span 12; }}
      .section-head {{ display: block; }}
      .section-head p {{ margin-top: 8px; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <h1>Agent Interaction Interactive Dashboard</h1>
      <p>
        Claude / Codex の履歴分析をローカル単体 HTML にまとめたダッシュボードです。
        ホバー、ズーム、系列の ON/OFF で掘り下げられます。生成元は `analysis_summary.json` と各種 CSV、
        レイアウト検査は `outputs/layout_checks/` の結果を反映しています。
      </p>
    </section>

    <nav class="nav">
      <a href="#usage">Usage</a>
      <a href="#behavior">Behavior</a>
      <a href="#tokens">Tokens</a>
      <a href="#artifacts">Artifacts</a>
      <a href="#sessions">Sessions</a>
    </nav>

    <section class="stats">
      {build_cards(summary, token_by_source)}
    </section>

    <section class="section" id="usage">
      <div class="section-head">
        <h2>Usage Rhythm</h2>
        <p>時間帯と日次推移から、いつ集中的にエージェントを使っているかを見られます。</p>
      </div>
      <div class="grid">
        <article class="panel span-8">{chart_html_parts[0]}</article>
        <article class="panel span-4">{chart_html_parts[2]}</article>
        <article class="panel span-12">{chart_html_parts[1]}</article>
      </div>
    </section>

    <section class="section" id="behavior">
      <div class="section-head">
        <h2>Prompt Behavior</h2>
        <p>どんなジャンルの依頼が多いか、どのプロジェクトが中心か、ツール利用がどこに偏っているかを多角的に追えます。</p>
      </div>
      <div class="grid">
        <article class="panel span-4">{chart_html_parts[3]}</article>
        <article class="panel span-4">{chart_html_parts[4]}</article>
        <article class="panel span-4">{chart_html_parts[7]}</article>
        <article class="panel span-7">{chart_html_parts[5]}</article>
        <article class="panel span-5">{chart_html_parts[8]}</article>
      </div>
    </section>

    <section class="section" id="tokens">
      <div class="section-head">
        <h2>Token Footprint</h2>
        <p>ソース別のトークン総量、1 セッション平均、重いセッション、入出力構成を並べて確認できます。</p>
      </div>
      <div class="grid">
        <article class="panel span-6">{chart_html_parts[9]}</article>
        <article class="panel span-6">{chart_html_parts[10]}</article>
        <article class="panel span-8">{chart_html_parts[11]}</article>
        <article class="panel span-4">{chart_html_parts[12]}</article>
      </div>
    </section>

    <section class="section" id="artifacts">
      <div class="section-head">
        <h2>Artifacts & Quality</h2>
        <p>履歴ソースの厚みと、静的レイアウト検査の健康状態をまとめています。</p>
      </div>
      <div class="grid">
        <article class="panel span-8">{chart_html_parts[13]}</article>
        <article class="panel span-4">{chart_html_parts[14]}</article>
      </div>
      <div class="note-panel">
        <h3>Interpretation Notes</h3>
        <ul>
          <li>Mixed-language prompts が最も多く、英日混在の作業スタイルが強く出ています。</li>
          <li>主要ジャンルでは `implementation` と `automation_orchestration` が目立ちます。</li>
          <li>トークン利用は `Codex local` が支配的ですが、Claude 側は snapshot の差分比較に向いています。</li>
          <li>静的レイアウト検査は現時点で 0 findings です。詳細は `outputs/layout_checks/` を参照できます。</li>
        </ul>
      </div>
    </section>

    <section class="section" id="sessions">
      <div class="section-head">
        <h2>Sessions Explorer</h2>
        <p>セッション時間と総メッセージ量の関係を見ながら、トークン消費が大きかったセッションを表で確認できます。</p>
      </div>
      <div class="grid">
        <article class="panel span-12">{chart_html_parts[6]}</article>
      </div>
      <div style="height: 16px;"></div>
      <div class="table-shell">
        <table>
          <thead>
            <tr>
              <th>Project or Title</th>
              <th>Family</th>
              <th>Origin</th>
              <th>Total Tokens</th>
              <th>Input</th>
              <th>Output</th>
            </tr>
          </thead>
          <tbody>
            {build_top_sessions_table(top_token_sessions)}
          </tbody>
        </table>
      </div>
    </section>

    <footer>
      Generated from local analysis outputs. Source summary timestamp: {html.escape(str(generated))}. Open locally at
      <code>{html.escape(str(HTML_PATH))}</code>.
    </footer>
  </main>
</body>
</html>
"""


def main() -> None:
    data = load_data()
    html_text = build_html(data)
    HTML_PATH.write_text(html_text, encoding="utf-8")
    write_summary(data)
    print(f"Rendered interactive dashboard at {HTML_PATH}")


if __name__ == "__main__":
    main()
