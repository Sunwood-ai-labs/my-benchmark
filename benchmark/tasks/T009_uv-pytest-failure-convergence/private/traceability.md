# Why This Case Exists
uv-run-pytest が現実に多く、Python compatibility fix も継続的にあった。

# Source Pattern Summary
この環境にとって pytest 修復は汎用ではなく、かなり日常的なパターンだった。

# Evidence Used
- uv-run-pytest / pytest の頻度。
- Python compatibility 系の recent commit。

# Evidence Tags
- E04: Codex uv and pytest usage

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
