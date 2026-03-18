# Scoring Dimensions
- 前提確認の正確さ
- truth source の扱い
- 変更の必要十分性

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- assumption_refresh

# Automatic Checks
- path/version truth source が参照されている
- 誤前提のままの記述が残っていない

# Hard Fail Conditions
- 未確認の path/version を断定する

# Partial Credit Rules
- 前提は正したが変更や説明が雑な場合は 3 点止まり。
