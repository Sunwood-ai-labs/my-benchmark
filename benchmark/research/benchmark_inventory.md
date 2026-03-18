# Benchmark Inventory

## 高摩擦パターン優先メモ
2026-03-19 改訂では、一般的な仕事パターンの頻度だけでなく、ユーザー不満が強く出たパターンを優先度高で扱うようにした。
とくに F01-F05 は「一度踏むと benchmark の価値が大きく落ちる」ため、pilot と追加 main case の中心に据えた。
また、この版から acceptance_alignment を明示的な macro-axis として扱う。
以下は、ローカル履歴から見えた仕事パターンを benchmark 向けに整理した一覧です。

| 観測パターン | 頻度 | 重要度 | 代表シグナル | 証拠ソース |
| --- | --- | --- | --- | --- |
| shell-first の repo scouting | 高 | 高 | Get-Content / git / Get-ChildItem / rg が支配的 | Codex sessions, PowerShell history |
| JS・Python・docs 混在保守 | 高 | 高 | package.json、pyproject、docs、release 面が同居 | selected git repos, Claude buckets |
| desktop packaging と runtime 修正 | 中 | 高 | packaged-path bug、build script、release prep | selected git repos, Codex cwd |
| uv 前提の Python 修復 | 中 | 高 | uv と uv-run-pytest が多い | Codex shell, Python repos |
| docs build・diagram validation | 中 | 高 | docs:build、vitepress、diagram check が反復 | Codex shell, selected git repos |
| release 文書と記事の同期 | 中 | 中 | release prep と docs surface が連動 | selected git repos |
| subagent orchestration | 中 | 高 | spawn_agent、subagent log、team policy | Codex, Claude, CLAUDE.md |
| 中断後の recovery | 中 | 高 | aborted turn、timeout、backup/corrupted artifact | Codex, Claude backups |
| owned scope での協調編集 | 中 | 高 | one-file / one-module boundary が出る | session patterns |
| Windows + bash / WSL path handling | 中 | 中 | PowerShell 主体だが shell snapshot もある | PS history, shell snapshots |
| paired docs 保守 | 中 | 中 | README と README.ja の併走 | selected git repos |
| 調査・説明タスク | 中 | 中 | 原因説明、次アクション整理、fact/hypothesis 分離 | prompt patterns |
| hardware / toolchain 支援 | 低〜中 | 中 | board 検出や example driven support がある | selected git repos, evidence map |

## 補足
- Codex 側の上位 cwd は、desktop app、Discord bot、game/agent、video utility、docs tooling といった複数 repo family に分散していた。
- Claude 側の上位 bucket は、desktop app 系と orchestrator / tooling 系が中心だった。
- grounding に使った git repo は 9 件で、desktop app、video utility、orchestrator、docs tooling、diagram tooling、game/agent、hardware support などを含む。
- PowerShell 上位 command: cd=1438, git=316, ssh=248, npm=108, python=107, uv=104, node=100, gh=49。
- task の実運用では index 順固定ではなく、stage 内シャッフルを推奨する。
