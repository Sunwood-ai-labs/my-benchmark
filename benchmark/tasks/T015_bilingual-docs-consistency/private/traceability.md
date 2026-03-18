# Why This Case Exists
paired docs を持つ repo が複数あり、片側 drift が起きやすかったため。

# Source Pattern Summary
public docs の保守では、実装変更よりこのズレの方が頻出する場面があった。

# Evidence Used
- README / README.ja の併存。
- docs-oriented commit。

# Evidence Tags
- E03: Codex docs and diagram checks
- E12: Git-backed release and article repos
- E13: Bilingual docs repo family

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
