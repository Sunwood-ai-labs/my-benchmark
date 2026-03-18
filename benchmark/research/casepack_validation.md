# Casepack Validation

benchmark の `Q / A / rubric` 自体が機能するかを、実モデルで解かせて確認した記録です。
ここで見るのは runtime harness の派手さではなく、case pack が妥当な評価単位として成立しているかどうかです。

## V001: P005 single-run validation
- target case: `P005_path-and-version-assumption-repair`
- execution style: single-run with the public case pack embedded verbatim into the prompt
- model used: `qwen3.5-plus`
- local fixture: tracked `runtime_fixtures/P005_path-and-version-assumption-repair` baseline から fresh copy

## 観察結果
- public `problem.md` と `context.md` だけでも、モデルは path/version 前提修正タスクを自然に解けた。
- 出力は `README.md` のみを修正し、`npm run check:docs` を通した。
- final answer では `package.json`, `src/config-path.mjs`, `logs/startup.log` を truth source として引用した。
- 一方で validation script `scripts/check-docs.mjs` も evidence として挙げており、truth source と validation source の区別は rubric でより明確にすべきと分かった。

## benchmark pack 側の改善点
- `public/problem.md` に、変更したファイルまたは変更不要理由、実行した確認手順も deliverable として明記した。
- `public/context.md` に、truth source と validation script の役割差を追記した。
- `private/answer.md` に、exact patch version と version family の両許容条件を明記した。
- `private/rubric.md` に、truth source と validation source の区別を採点観点として追加した。

## benchmark-wide に分かったこと
- case pack 自体は benchmark 本体として機能する。
- ただし run 経由評価では task artifact score が甘くなりうるため、`delivery_reliability_score` のような run-layer 指標を別に持つのが妥当である。
- runnable fixture は benchmark 本体の必須条件ではないが、pilot の一部を smoke validation しておく価値は高い。

## 次の推奨
- P001-P005 のうち、性質が異なる 2 〜 3 ケースを追加で real-run validation する。
- 特に `surface_fit` 系と `verification_gap` 系は P005 と違う失敗の出方をするため、別検証が必要。
