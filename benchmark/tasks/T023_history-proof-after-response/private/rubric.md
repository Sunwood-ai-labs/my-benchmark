# Scoring Dimensions
- 末端 state 確認
- assertion の強さ

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- false_done_penalty
- verification_gap

# Automatic Checks
- history-related assertion 追加

# Hard Fail Conditions
- history 未確認で verified と断定

# Partial Credit Rules
- manual 手順のみなら 3 点止まり。
