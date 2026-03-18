# Scoring Dimensions
- 通知面の適合
- 差分の局所性

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- surface_fit

# Automatic Checks
- 二重出力検知が消える

# Hard Fail Conditions
- ユーザー面に raw debug が残る

# Partial Credit Rules
- 片面だけ改善は 3 点止まり。
