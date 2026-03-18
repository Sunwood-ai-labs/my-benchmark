# Scoring Dimensions
- 本文抽出の精度
- ノイズ除去
- 回帰防止

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- surface_fit

# Automatic Checks
- golden fixture が期待本文を含み、chrome 語を含まない

# Hard Fail Conditions
- 本文より UI chrome を多く返す

# Partial Credit Rules
- 一部ノイズが残るが本文取得はできるなら 3 点。
