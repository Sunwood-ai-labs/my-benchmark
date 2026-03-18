# Why This Case Exists
デモや簡易 UI を『もう少し意図のある見た目に』という依頼が複数あった。

# Source Pattern Summary
曖昧だが実装が期待される依頼は、個人ワークフロー上かなり重要だった。

# Evidence Used
- UI 強化系 prompt。
- 既存 UI と repo fit の両立を求める傾向。

# Evidence Tags
- E16: UI and browser-validation prompts

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
