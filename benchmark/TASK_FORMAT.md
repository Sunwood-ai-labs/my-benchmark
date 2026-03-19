# Task Format

この repository では、各 task は `SWE-bench` 風の case pack として持つ。

## 基本形

各 case directory は次を持つ。

- `public/prompt.txt`
  モデルに渡す canonical prompt 本文。
- `public/problem.md`
  `prompt.txt` の markdown mirror。
- `public/env.md`
  モデルに渡す canonical environment 情報。
- `public/context.md`
  `env.md` の markdown mirror。
- `shared/meta.yaml`
  機械可読メタデータ。
- `private/golden.md`
  evaluator 向けの canonical accepted fix。
- `private/answer.md`
  `golden.md` の詳細版。
- `private/eval.yaml`
  evaluator 向けの canonical machine-readable rubric。
- `private/rubric.md`
  `eval.yaml` の詳細版。
- `private/traceability.md`
  ローカル incident との対応関係。

model-facing bundle では `public/prompt.txt` と `public/env.md` だけを配る。mirror、`shared/`、`private/` は evaluator / curator 用である。

## 何を public に置くか

`public/` は issue text に近い面であり、次だけを置く。

- 実際の依頼文に近い prompt
- 最低限の環境情報
- 問題を解くのに必要な観測可能証拠の種類

`public/` に置かないもの:

- evaluator 向けの採点観点
- hidden answer に相当するヒント
- verifier 向けの細かい採点条件

## 何を private に置くか

`private/` は hidden evaluator 面であり、次を置く。

- accepted fix の特徴
- hard fail 条件
- overchange / false done / verification gap の扱い
- traceability と leakage guardrail
- required evidence
- auto-check contract
- 1-5 score anchor

## SWE-bench との対応

- `public/prompt.txt` = issue text に相当
- `public/env.md` = repo state / minimal context
- `private/golden.md` = gold patch の説明版
- `private/eval.yaml` = hidden tests + human rubric のハイブリッド
- `runtime_fixtures/` = runnable subset 用の optional environment

## `private/eval.yaml` の最小 contract

少なくとも次を持つ。

- `required_evidence`
  採点時に必ず見る artifact
- `automatic_checks`
  自動評価の要点
- `auto_check_contract`
  check ごとの target / pass_when / fail_when
- `hard_fail_conditions`
  即失格条件
- `score_anchors`
  1-5 の anchor
- `partial_credit_rules`
  満点未満の扱い

## 追加の機械可読面

- `benchmark/cases_manifest.jsonl`
  model-facing stripped manifest
- `benchmark/private_cases_manifest.jsonl`
  evaluator-facing internal manifest
- `benchmark/public_dataset/`
  model-facing public-only bundle
- `benchmark/splits/pilot.txt`
  pilot split
- `benchmark/splits/main.txt`
  main split
