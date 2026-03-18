# Why This Case Exists
release 前後で version 表示や artifact の整合が話題になることがあった。

# Source Pattern Summary
コード・docs・workflow の三者整合を取る作業が個人ベンチに向いていた。

# Evidence Used
- release prep 系 repo。
- build / release tooling の利用履歴。

# Evidence Tags
- E05: Desktop packaging and build repos
- E12: Git-backed release and article repos

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
