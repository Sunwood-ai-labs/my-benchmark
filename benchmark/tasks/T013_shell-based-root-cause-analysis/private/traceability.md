# Why This Case Exists
shell-first debugging と git / file exploration の比重が高かったため。

# Source Pattern Summary
編集せずに『今何が起きていそうか』を整理するケースが個人ワークフローに合っていた。

# Evidence Used
- PowerShell history。
- Codex shell の file / git 探索。

# Evidence Tags
- E01: Codex rollout corpus
- E09: Claude verification-oriented prompts
- E11: PowerShell and shell-snapshot mix

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
