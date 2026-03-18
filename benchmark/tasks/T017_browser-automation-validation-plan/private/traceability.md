# Why This Case Exists
ブラウザや Playwright で『本当に見たのか』を問う圧がローカル履歴にあったため。

# Source Pattern Summary
UI タスクでは、実装と同じくらい検証設計が差になると考えた。

# Evidence Used
- browser validation を求める prompt。
- browser-automation skill の存在。

# Evidence Tags
- E09: Claude verification-oriented prompts
- E16: UI and browser-validation prompts

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
