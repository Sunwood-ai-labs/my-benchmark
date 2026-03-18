# Expected Outcome
- 抽出結果が本文中心になり、UI ノイズが消える。

# Strong Answer Characteristics
- 境界条件が明確で regression check がある。

# Acceptable Variants
- selector 修正、tree filter、post-filter のいずれでも可。

# Common Failure Patterns
- ノイズだけでなく本文まで落とす。

# Minimal Pass Line
- 主要本文が取得でき、chrome ノイズが大きく減る。

# Notes For Evaluator
- 本文 relevance を人手でも確認する。
