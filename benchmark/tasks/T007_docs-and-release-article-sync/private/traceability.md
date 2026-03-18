# Why This Case Exists
release note と記事・README の整合調整が何度も必要になっていた。

# Source Pattern Summary
git-backed な docs 整備は、実装と別の能力差が出ると考えた。

# Evidence Used
- release prep と docs article の commit。
- release-facing docs surface の存在。

# Evidence Tags
- E03: Codex docs and diagram checks
- E12: Git-backed release and article repos

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
