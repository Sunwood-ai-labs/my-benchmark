# P005 Runtime Fixture

この fixture は `P005_path-and-version-assumption-repair` を実行可能な最小 workspace に具体化したものです。

## 目的
- path/version の truth source を local file から確認できること
- stale な README を修正すると focused check が通ること
- 2 回目以降の評価でも、毎回同じ初期状態から始められること

## 運用ルール
- このディレクトリは tracked な baseline です。
- 実行時はここを直接編集せず、`scripts/new-validation-run.ps1` で `benchmark/validation_runs/` 配下へコピーして使ってください。
- `benchmark/validation_runs/` は ignore 済みなので、モデル別 run artifact が repo の差分ノイズになりません。
