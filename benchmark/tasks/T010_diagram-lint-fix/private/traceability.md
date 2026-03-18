# Why This Case Exists
diagram lint は local docs tooling の中で比較的独立した recurring pattern だった。

# Source Pattern Summary
図表系の修正は、単なる docs 修正とは別の skill 差が出ると判断した。

# Evidence Used
- diagram check script。
- label / border / overflow を直す commit。

# Evidence Tags
- E03: Codex docs and diagram checks
- E14: Diagram lint repo family

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
