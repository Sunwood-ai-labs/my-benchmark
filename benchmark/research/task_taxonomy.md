# Task Taxonomy

generic な benchmark bucket ではなく、ローカル履歴から見えた仕事の型で taxonomy を切っています。

| Task Type | 定義 | 判断基準 | 代表傾向 |
| --- | --- | --- | --- |
| targeted_bugfix | 明確な不具合を最小差分で直すタスク。 | 症状がはっきりしており、主な fault line が狭い。 | monitor loop、path fix、CLI regression など。 |
| ambiguous_feature | 曖昧な依頼から useful な機能を新規実装するタスク。 | 仕様が足りないが、実装して着地することが求められる。 | UI 改善、小さな option 追加など。 |
| refactor_preserve_behavior | 外から見える挙動を保ったまま構造改善するタスク。 | repo は既に動いており、壊さないことが最優先。 | cleanup、責務分離、小さな整理。 |
| env_or_ci_repair | 実行経路、設定、workflow、metadata の破損を直すタスク。 | コードそのものより run path が壊れている。 | uv、docs build、packaging、workflow mismatch。 |
| investigation_and_design | ローカル証拠から説明や次アクションを作るタスク。 | 編集なしでも成立するが、具体性が必要。 | shell triage、repo orientation、device diagnosis。 |
| recovery_and_retry | 途中状態を観察してから安全に再開するタスク。 | partial state の把握が必須。 | 中断後の再開、壊れた config の回復。 |
| docs_release_polish | docs や release-facing surface を local truth に合わせるタスク。 | 差分根拠と cross-surface consistency が重要。 | release note、README sync、diagram docs。 |
| orchestration_plan | 作業分担と検証責任を設計するタスク。 | 実装より execution plan が成果物。 | subagent 役割分担、verification lane 設計。 |
