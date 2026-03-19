# Accepted Fix

- 誤った前提が UI 実観測で特定され、セレクタまたは探索ロジックだけが局所的に直る。
- 無関係なレイアウト変更が入らない。
- 少なくとも 1 つの smoke か focused check がある。

# Minimum Pass

- UI 実観測に触れた上で局所修正し、回帰を避けている。

# Acceptable Variants

- selector の優先順変更、探索範囲修正、fallback 条件修正のどれでもよい。

# Common Failures

- レイアウトや CSS を勝手にいじる。
- 実観測なしの推測でセレクタを増やし続ける。
- 症状は消えても別の UI が壊れる。
- 初回状態だけ見て、再実行時の popup や pane state 差を無視する。

# Evaluator Notes

- 実観測の有無を厳しく見る。
- layout tinkering で逃げていないか確認する。
