# Why This Case Exists
PowerShell と shell-snapshot が共存しており、path 問題は実務的な失敗モードだった。

# Source Pattern Summary
環境差によるバグは地味だが差が出るため、独立ケース化した。

# Evidence Used
- PowerShell history と shell snapshots。
- path 系の error cluster。

# Evidence Tags
- E11: PowerShell and shell-snapshot mix

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
