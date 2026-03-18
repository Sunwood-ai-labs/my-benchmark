# Why This Case Exists
複数 agent / ownership 前提の作業で、担当外に触れないことが強く求められていたため。

# Source Pattern Summary
壊さない協調作業能力を測るケースとして必要だった。

# Evidence Used
- ownership を明示する subagent prompt。

# Evidence Tags
- E02: Codex multi-agent usage
- E08: Claude sidechains and subagents

# Abstractions Applied
- 固有の repo 名、会話ログ、社内固有文脈は抽象化している。
- パターンだけを残し、個別案件の再利用にならないようにしている。

# Leakage Check
secret、token、auth、cache の具体値や原文ログは含めていない。
