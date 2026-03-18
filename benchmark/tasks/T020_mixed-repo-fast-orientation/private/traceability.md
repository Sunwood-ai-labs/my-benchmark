# Why This Case Exists
mixed-language repo での scouting が shell-first workflow として繰り返し現れていたため。

# Source Pattern Summary
実装前の数分で勝負が決まるタイプの作業を benchmark に入れたかった。

# Evidence Used
- docs、Python、JS、packaging が共存する repo 群。
- file listing と targeted read が多いこと。

# Evidence Tags
- E01: Codex rollout corpus
- E07: Codex worktree concentration
- E11: PowerShell and shell-snapshot mix

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
