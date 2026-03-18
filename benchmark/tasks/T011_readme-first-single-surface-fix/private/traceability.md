# Why This Case Exists
workspace と repo の両方で README を最初に読むよう強い指示が存在したため。

# Source Pattern Summary
『まず README』が個人ルールとして重要なので、専用ケースを作った。

# Evidence Used
- README first 指示。

# Evidence Tags
- E17: README-first local rules

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
