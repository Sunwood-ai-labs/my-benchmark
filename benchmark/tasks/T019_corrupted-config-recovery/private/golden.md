# Accepted Fix

中断済みや壊れた途中状態をいったん観察してから、安全に再開できるかを見る。
- 盲目的な全戻しではなく、妥当な baseline で valid state に戻る。

# Minimum Pass

- 何を残し、何をやり直すかが説明でき、最終状態が整っていること。

# Acceptable Variants

- cleanup 先行でも、観察に基づくなら可。

# Common Failures

- 状態確認なしで最初からやり直す。
- 既にある成果を壊す。
- 中途半端な副作用を残したまま終わる。

# Evaluator Notes

- 雑なリトライではなく、状態差分を見ているかを確認する。
