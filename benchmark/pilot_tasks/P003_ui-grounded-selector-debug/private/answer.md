# Expected Outcome
- 誤った前提が UI 実観測で特定され、セレクタまたは探索ロジックだけが局所的に直る。
- 無関係なレイアウト変更が入らない。
- 少なくとも 1 つの smoke か focused check がある。

# Strong Answer Characteristics
- DOM / screenshot / diagnostic のどれを見たかが明確。
- 変更がセレクタ近傍に留まり、レイアウト破壊を避けている。
- 症状と原因のつながりが説明できている。

# Acceptable Variants
- selector の優先順変更、探索範囲修正、fallback 条件修正のどれでもよい。

# Common Failure Patterns
- レイアウトや CSS を勝手にいじる。
- 実観測なしの推測でセレクタを増やし続ける。
- 症状は消えても別の UI が壊れる。

# Minimal Pass Line
- UI 実観測に触れた上で局所修正し、回帰を避けている。

# Notes For Evaluator
- 実観測の有無を厳しく見る。
- layout tinkering で逃げていないか確認する。
