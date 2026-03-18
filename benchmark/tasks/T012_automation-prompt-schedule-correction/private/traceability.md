# Why This Case Exists
ローカルに automation 定義と run 履歴があり、状態付きメンテナンスのケースとして成立していた。

# Source Pattern Summary
コード修正ではなく運用定義の保守も、個人 benchmark に含める価値があると判断した。

# Evidence Used
- automation ファイル。
- run 履歴。

# Evidence Tags
- E18: Automation definitions and runs

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
