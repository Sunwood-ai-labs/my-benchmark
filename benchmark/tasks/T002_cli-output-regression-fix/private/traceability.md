# Why This Case Exists
出力崩れやログ表示の違和感を指摘する流れがローカル履歴にあった。

# Source Pattern Summary
terminal-facing bugfix は小さいが、説明責任と再現確認が必要なので benchmark 向きだった。

# Evidence Used
- PowerShell-heavy workflow。
- 出力崩れを気にする bug report。

# Evidence Tags
- E01: Codex rollout corpus
- E11: PowerShell and shell-snapshot mix

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
