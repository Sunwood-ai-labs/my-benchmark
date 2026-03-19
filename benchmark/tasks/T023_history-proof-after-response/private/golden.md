# Accepted Fix

- 応答後の履歴更新が観測される。

# Minimum Pass

- history 更新の痕跡を 1 つ以上確認。

# Acceptable Variants

- file check、event check、snapshot diff どれでも可。

# Common Failures

- send pass だけで終える。

# Evaluator Notes

- 最後の state まで届いているかを見る。
