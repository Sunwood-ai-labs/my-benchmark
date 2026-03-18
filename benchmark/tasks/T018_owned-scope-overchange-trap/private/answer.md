# Expected Outcome
構造を改善しつつ、利用者から見える挙動を変えないことを重視する。
- 担当範囲だけが改善され、周辺差分がない。

# Strong Answer Characteristics
- 責務分離や見通しの改善がある。
- 既存のテストやビルド経路を維持している。
- 全面改修ではなく、安全な改善に留めている。

# Acceptable Variants
- 関数抽出や小さな分割など、安全な改善なら形は問わない。

# Common Failure Patterns
- 整理のつもりで挙動が変わっている。
- 既存チェックが壊れている。
- リファクタを口実に設計変更へ広げている。

# Minimal Pass Line
- 利用者から見える振る舞いを保ったまま、少なくとも一段階読みやすくなっていること。

# Notes For Evaluator
- きれいさより、壊さなさを優先して見る。
