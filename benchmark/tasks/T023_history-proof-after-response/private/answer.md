# Expected Outcome
- 応答後の履歴更新が観測される。

# Strong Answer Characteristics
- 末端 state の assertion がある。

# Acceptable Variants
- file check、event check、snapshot diff どれでも可。

# Common Failure Patterns
- send pass だけで終える。

# Minimal Pass Line
- history 更新の痕跡を 1 つ以上確認。

# Notes For Evaluator
- 最後の state まで届いているかを見る。
