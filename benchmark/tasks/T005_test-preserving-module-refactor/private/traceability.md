# Why This Case Exists
cleanup 依頼は多いが、同時に『壊さないで』という圧も強かったため。

# Source Pattern Summary
apply_patch 中心の小さな構造改善と validation の組み合わせが頻出した。

# Evidence Used
- 反復する apply_patch。
- cleanup と compatibility fix が並ぶ commit 群。

# Evidence Tags
- E01: Codex rollout corpus

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
