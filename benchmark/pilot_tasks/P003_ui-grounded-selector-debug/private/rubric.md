# Scoring Dimensions
- UI 実観測の質
- 原因線への一致
- 回帰回避
- 差分の局所性

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- grounding_before_change

# Automatic Checks
- layout 系ファイルに不要な大改変がない
- selector smoke が通る
- popup / state drift に触れた観測証拠がある場合は、それを説明に反映している

# Hard Fail Conditions
- 実観測なしでセレクタを推測変更するだけ
- 無関係なレイアウト変更を大量に入れる

# Partial Credit Rules
- 原因推定は当たっていても実観測証拠がなければ 3 点止まり。
