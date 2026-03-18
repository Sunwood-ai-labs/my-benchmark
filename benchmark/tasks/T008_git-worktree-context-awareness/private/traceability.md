# Why This Case Exists
Codex worktree と git status first の流れが明確に観測されたため。

# Source Pattern Summary
編集力以前に、作業場所を正しく理解する力が個人環境で重要だった。

# Evidence Used
- 大量の git status。
- worktree 利用痕跡。

# Evidence Tags
- E01: Codex rollout corpus
- E07: Codex worktree concentration

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
