# Why This Case Exists
Claude backup / corrupted artifact は復旧ケースの直接的な根拠だった。

# Source Pattern Summary
安全性と復旧力を同時に見られる重要ケースとして採用した。

# Evidence Used
- backup / corrupted artifact family。

# Evidence Tags
- E06: Abort and timeout recovery signals
- E10: Claude backup and corrupted config artifacts

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
