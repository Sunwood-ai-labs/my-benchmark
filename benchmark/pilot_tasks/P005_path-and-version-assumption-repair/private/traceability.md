# Why This Case Exists
前提を外したまま進めると、修正能力以前に「聞いていない」と受け取られるため。

# Source Pattern Summary
- install path に関する修正要求。
- 最新版互換性に関する確認要求。
- runtime log や配置先を truth source として見てほしいという要求。

# Evidence Used
- F04: path_version_assumption_error cluster
- Claude history path/version complaints
- local incident seed: install dir、runtime log、version gate を見てから前提を直す要求

# Prompt Frame
- 元の要求は generic な docs 修正ではなく、「配置先はそこではない」「最新版 build / current version でも通るのか確認してほしい」という前提修正だった。
- そのため problem では install dir、runtime log、version metadata を truth source 候補として明示した。

# Environment Frame
- install dir と runtime log が現実の挙動を示し、README や stale guide が古い path/version を持ちうる環境だった。
- 実装変更ではなく説明変更だけで解決する可能性もある。

# Abstractions Applied
- 具体的なゲーム名、保存先、バージョン番号は一般化した。
- exact build number や固有 repo 名は公開 benchmark では出していない。

# Leakage Check
- 個人環境の完全パスは一般化した。
