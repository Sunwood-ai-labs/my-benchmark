# Benchmark Sources Manifest

benchmark 生成時に実際に探索したローカル証拠源の一覧です。
Codex の transcript 件数は再帰カウントで、2026-03-18T22:30:29+09:00 時点の spot-check を反映しています。
transcript 系ソースは大量引用せず、構造要約のみを使う前提です。

| Path | 種別 | データ種別 | 期間 | 件数 | 取り扱い注意 | 信頼度 | 設計価値 | secret risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `%USERPROFILE%\\.codex\\session_index.jsonl` | Codex | session index | 2026-03-06 から 2026-03-18 | 538 行 | thread 名は話題を含みうるため、構造要約に留める。 | 高 | active session 全体像の把握に有効。 | 中 |
| `%USERPROFILE%\\.codex\\sessions` | Codex | rollout transcript | 2026-02-20 to 2026-03-18 | 389 | raw transcript は高リスク。大量引用しない。 | 高 | command、cwd、model、recovery signal の一次根拠。 | 高 |
| `%USERPROFILE%\\.codex\\archived_sessions` | Codex | archived transcript | 2026-03-07 から 2026-03-17 | 182 | 旧ログでも transcript である点は同じ。 | 中 | 経時的パターンと回復シグナルを補う。 | 高 |
| `%USERPROFILE%\\.codex\\config.toml` | Codex | tool config | 2026-03-17 | 1 file | 値の引用は避け、key だけ見る。 | 中 | default model と feature flag の確認に有効。 | 中 |
| `%USERPROFILE%\\.codex\\automations` | Codex | automation definition | 2026-03-07 から 2026-03-17 | 6 | prompt 要約は可だが id や中身の出しすぎに注意。 | 中 | automation 系 case の根拠。 | 中 |
| `%USERPROFILE%\\.codex\\worktrees` | Codex | repo-adjacent snapshot | 2026-03-13 から 2026-03-17 | 2970 | 一次真実ではなく周辺証拠として扱う。 | 中 | worktree 利用と repo 集中リスクの把握に有効。 | 中 |
| `%USERPROFILE%\\.claude\\history.jsonl` | Claude | top-level prompt history | 2026-02-22 から 2026-03-13 | 233 行 | 短い prompt でも案件意図を含みうるため要約のみ。 | 中 | 依頼の型と検証志向の把握に有効。 | 高 |
| `%USERPROFILE%\\.claude\\projects` | Claude | project session log | 2026-02-22 to 2026-03-14 | 500 | 高密度ログなので構造要約に限定する。 | 高 | Claude 側の cwd、branch、tool、subagent 運用の一次根拠。 | 高 |
| `%USERPROFILE%\\.claude\\projects\\**\\subagents\\agent-*.jsonl` | Claude | subagent log | 2026-03-05 から 2026-03-14 | 205 | role-rich だが transcript 性が高い。 | 高 | multi-agent workflow の強い根拠。 | 高 |
| `%USERPROFILE%\\.claude\\file-history` | Claude | edited file snapshot | 2026-03-05 から 2026-03-14 | 188 | file 名の追跡力は弱い。 | 中 | docs / code / asset の編集面を補足。 | 中 |
| `%USERPROFILE%\\.claude\\shell-snapshots` | Claude | shell context snapshot | 2026-01-08 から 2026-03-14 | 47 | 環境証拠としてのみ扱う。 | 低 | Windows + bash 混在ケースの補助。 | 中 |
| `%USERPROFILE%\\.claude\\CLAUDE.md` | Claude | workflow policy | 2026-03-14 | 1 file | 方針として要約し、原文 doctrine を貼らない。 | 中 | team-style / devil review の運用証拠。 | 低 |
| `%USERPROFILE%\\.claude\\backups` | Claude | backup / corrupted artifact | 2026-03-10 から 2026-03-14 | 10 | 実値を出さない。 | 中 | config recovery case の強い根拠。 | 高 |
| `%APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt` | Shell | PowerShell history | 2026-03-18 更新 | 5252 行 | timestamp がなく、paste 断片も混ざる。 | 中 | command family の頻度と toolchain mix の把握に有効。 | 中 |
| selected local git repos | Git | branch / status / commit / manifest | current local state | 9 | read-only で確認し、auth / remote config は見ない。 | 高 | repo family を grounded にするための補助証拠。 | 低 |
