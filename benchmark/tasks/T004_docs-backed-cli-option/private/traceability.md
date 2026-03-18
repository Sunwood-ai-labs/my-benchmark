# Why This Case Exists
CLI 機能追加と README 同期が local tool repo で繰り返されていた。

# Source Pattern Summary
機能実装だけでなく docs の追従まで要求される作業が多かった。

# Evidence Used
- lite mode や docs repositioning 系の commit。
- README / guide の継続更新。

# Evidence Tags
- E04: Codex uv and pytest usage

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
