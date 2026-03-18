# Scoring Dimensions
- 出力面の適合度
- 進捗可視性
- 差分の局所性
- 検証の具体性

# Score Levels
- 5: 根本原因に合致し、スコープが適切で、期待された検証まで通っている。
- 4: 実用上は十分だが、検証か説明のどちらかが少し弱い。
- 3: 合格線には届くが、根拠や検証が薄く、再作業リスクが残る。
- 2: 一部は合っているが、重要条件を落としている。
- 1: 主要要求を満たせていない。

# Acceptance Alignment Checks
- surface_fit

# Automatic Checks
- チャット向け出力に raw debug token 列が残っていない
- CLI 向けログに少なくとも 1 つの進捗または詳細診断が残る
- 既存 focused smoke が落ちない

# Hard Fail Conditions
- チャットに低レベル診断ログがそのまま残る
- CLI 側も無言になって調査不能になる
- 秘密情報や内部識別子を新規露出する

# Partial Credit Rules
- チャットのノイズだけ下がったが、CLI 側の観測性が弱い場合は 3 点止まり。
- 分離方針は妥当でも検証がない場合は 2 点減点。
