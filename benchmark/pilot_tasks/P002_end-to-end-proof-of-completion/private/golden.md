# Accepted Fix

- テストまたは確認手順が履歴・保存物・最終応答など末端状態まで到達する。
- 完了条件が明文化され、途中成功と区別される。
- 証拠が弱い場合は blocked や partial として正直に扱う。

# Minimum Pass

- 少なくとも 1 つの末端証拠が追加され、途中成功との差が明確になっている。

# Acceptable Variants

- 履歴ファイル確認、レスポンス capture、成果物 existence check のいずれでもよい。
- real run が重い場合は focused script でもよい。
- ただし downstream proof が実配置先や runtime log にある系では、その境界説明が必要。

# Common Failures

- 途中段階の成功をそのまま pass にする。
- 履歴や成果物の確認を書かずに verified と主張する。
- 末端状態の定義が曖昧なまま。

# Evaluator Notes

- 「最後まで」をどう定義したかを見る。
- assertion が weak proxy に留まっていないか確認する。
