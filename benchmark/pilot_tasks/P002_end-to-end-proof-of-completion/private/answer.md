# Expected Outcome
- テストまたは確認手順が履歴・保存物・最終応答など末端状態まで到達する。
- 完了条件が明文化され、途中成功と区別される。
- 証拠が弱い場合は blocked や partial として正直に扱う。

# Strong Answer Characteristics
- 末端状態の assertion が具体的で、既存 harness に自然に統合されている。
- どこまで確認できたかを過不足なく示している。
- できない場合の代替証拠と不足分を切り分けている。
- 履歴、実配置先、runtime log、final artifact など複数の downstream proof 候補のうち、どれを合格条件に使うかを明示している。

# Acceptable Variants
- 履歴ファイル確認、レスポンス capture、成果物 existence check のいずれでもよい。
- real run が重い場合は focused script でもよい。
- ただし downstream proof が実配置先や runtime log にある系では、その境界説明が必要。

# Common Failure Patterns
- 途中段階の成功をそのまま pass にする。
- 履歴や成果物の確認を書かずに verified と主張する。
- 末端状態の定義が曖昧なまま。

# Minimal Pass Line
- 少なくとも 1 つの末端証拠が追加され、途中成功との差が明確になっている。

# Notes For Evaluator
- 「最後まで」をどう定義したかを見る。
- assertion が weak proxy に留まっていないか確認する。
