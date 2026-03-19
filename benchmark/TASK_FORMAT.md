# Task Format

この repository の case pack は、SWE-bench 風の split を取りつつ、artifact-first に寄せた format です。

## Canonical Structure

各 case directory は次を持ちます。

- `public/prompt.txt`
  model-facing の canonical prompt
- `public/problem.md`
  `prompt.txt` の markdown mirror
- `public/env.md`
  model-facing の minimal environment description
- `public/context.md`
  `env.md` の markdown mirror
- `shared/meta.yaml`
  machine-readable metadata
- `private/golden.md`
  canonical accepted fix の要点
- `private/answer.md`
  `golden.md` の説明版
- `private/eval.yaml`
  canonical machine-readable rubric
- `private/rubric.md`
  `eval.yaml` の説明版
- `private/traceability.md`
  local incident との traceability

model-facing bundle は `public/prompt.txt` と `public/env.md` だけです。

## Public Side

`public/` は issue-like surface です。ここに置くのは次だけです。

- 実際の依頼に近い prompt
- 最小限の環境情報
- 実行可能なら最低限の前提

`public/` に置かないもの:

- hidden answer
- evaluator の採点観点
- 過度なヒント

## Private Side

`private/` は hidden evaluator surface です。ここに置くのは次です。

- accepted fix の要点
- hard fail 条件
- overchange / false done / verification gap の基準
- traceability と leakage guardrail
- required evidence
- auto-check contract
- score anchor

## Artifact-First Contract

この benchmark では、主に次を採点します。

- 生成されたファイル
- surface に現れた実際の出力
- 最終返答
- 実行ログや verification artifact

diff や touched-file scope は次の確認用です。

- overchange していないか
- scope を外していないか
- safety を壊していないか

つまり、primary judged object は patch ではなく generated artifact です。

## No-Artifact Rule

- meaningful な生成物がない case は、原則として高得点にしません
- blocked が許容される case でも、boundary note や verification note のような operator-facing artifact は必要です
- meaningful な生成物がなく、blocked でもない場合は `3 / 10` cap を標準にします

## `private/eval.yaml` Contract

`private/eval.yaml` では主に次を定義します。

- `required_evidence`
  評価時に確認したい artifact
- `artifact_first_policy`
  何を primary artifact として見るか、no-artifact cap をどう掛けるか
- `automatic_checks`
  自動評価観点
- `auto_check_contract`
  各 check の target / pass_when / fail_when
- `hard_fail_conditions`
  即失格条件
- `partial_credit_rules`
  部分点と cap
- `score_anchors`
  true 0-10 anchor

## Relation To SWE-bench

- `public/prompt.txt` = issue text に近い prompt
- `public/env.md` = repo state / minimal context
- `private/golden.md` = accepted fix summary
- `private/eval.yaml` = hidden tests + human rubric の hybrid
- `runtime_fixtures/` = runnable subset 用 optional environment

## Dataset Surface

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
