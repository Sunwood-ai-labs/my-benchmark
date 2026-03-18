# Scoring Dimensions
- grounding
- 回帰修正
- 局所性

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- grounding_before_change

# Automatic Checks
- new-chat smoke pass

# Hard Fail Conditions
- 実観測なしの推測修正

# Partial Credit Rules
- 症状は消えるが根拠薄なら 3 点。
