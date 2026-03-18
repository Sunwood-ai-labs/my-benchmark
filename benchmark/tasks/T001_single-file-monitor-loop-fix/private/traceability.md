# Why This Case Exists
owned file を明示した修正依頼と、monitor loop 系の小さい不具合修正が履歴に存在した。

# Source Pattern Summary
スコープ管理と bugfix convergence を同時に測る小粒ケースとして採用した。

# Evidence Used
- one-file ownership のある subtask。
- 監視や deferred state を扱う修正痕跡。

# Evidence Tags
- E01: Codex rollout corpus

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
