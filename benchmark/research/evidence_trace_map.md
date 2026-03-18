# Evidence Trace Map

匿名化した evidence family と benchmark case の対応表です。
raw transcript や private repo 名を露出せずに、ケースの根拠を追跡できるようにしています。

| Evidence ID | 抽象化した証拠 family | 要約 | 強さ | 対応ケース |
| --- | --- | --- | --- | --- |
| E01 | Codex rollout corpus | Shell-first repo scouting and targeted patching dominate local Codex traces. | 高 | P001, P003, P005, T001, T002, T005, T008, T013, T020 |
| E02 | Codex multi-agent 運用 | spawn_agent, wait_agent, and related patterns show real orchestration workflows. | 高 | P004, T018 |
| E03 | Codex docs / diagram check 群 | docs:build, vitepress, and diagram validation recur across active repos. | 高 | P003, T007, T010, T015 |
| E04 | Codex uv / pytest 利用 | uv, uv-run-python, and uv-run-pytest are common in local Python work. | 高 | P002, T004, T009 |
| E05 | desktop packaging / build 系 repo | Desktop packaging, startup, and release preparation are repeated local themes. | 高 | P001, T006 |
| E06 | abort / timeout recovery signal | Aborted turns, timeout markers, and partial-state recovery are visible in local logs. | 高 | P005, T019 |
| E07 | Codex worktree 集中 | Worktree-heavy activity reveals branch and root-context risks and overfitting risk. | 中 | T008, T020 |
| E08 | Claude sidechain / subagent 運用 | Claude project logs show sidechain-heavy, team-style execution. | 高 | P004, T018 |
| E09 | Claude の検証志向 prompt | Top-level Claude history emphasizes validation, placement, and compatibility checks. | 中 | T013, T017 |
| E10 | Claude backup / corrupted config artifact | Backup and corrupted files indicate real config recovery scenarios. | 高 | P005, T019 |
| E11 | PowerShell と shell-snapshot の混在 | Windows-first command history plus shell snapshots support cross-shell path and recovery cases. | 中 | T002, T013, T014, T020 |
| E12 | git 根拠の release / article repo | Selected repos show release prep, public docs, and article synchronization work. | 中 | T006, T007, T015 |
| E13 | 二言語 docs 系 repo | Multiple repos maintain parallel README surfaces that drift after changes. | 中 | T015 |
| E14 | diagram lint 系 repo | Diagram overlap, label, and text-overflow checks are active local work patterns. | 高 | P003, T010 |
| E15 | hardware / toolchain support 系 repo | Local hardware-support work broadens the benchmark beyond web and docs repos. | 中 | T016 |
| E16 | UI / browser validation prompt 群 | Local prompts include richer UI asks and explicit pressure to verify browser behavior. | 中 | T003, T017 |
| E17 | README-first ローカルルール | Workspace and repo instructions repeatedly emphasize reading README before acting. | 高 | P001, T011 |
| E18 | automation 定義と run 履歴 | Local automation files and runs justify stateful automation-maintenance cases. | 中 | T012 |

## 使い方
- ある case が単発の思いつきではなく、繰り返し観測されたパターンに基づくかを監査するときに使う。
- repo 名や transcript 原文は intentionally 抽象化している。
- case を更新したら、この表と各 `traceability.md` を同時に更新する。
