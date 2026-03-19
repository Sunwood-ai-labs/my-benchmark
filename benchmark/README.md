# Benchmark

この directory は、ローカル履歴から起こした **personal SWE-bench-style benchmark** です。

## Core idea

この benchmark の本体は、説明の整った課題文ではなく、次の組です。

- 実際の依頼文に近い `public/prompt.txt`
- 最低限の `public/env.md`
- 受け入れ済みの正をまとめた `private/golden.md`
- hidden evaluator 面の `private/eval.yaml`

つまり、public は薄く、private は厳しく、runtime は任意です。

## Dataset surface

- [cases_manifest.jsonl](./cases_manifest.jsonl)
  全 case の manifest
- [splits/pilot.txt](./splits/pilot.txt)
  pilot split
- [splits/main.txt](./splits/main.txt)
  main split
- [TASK_FORMAT.md](./TASK_FORMAT.md)
  case format
- [EVALUATION.md](./EVALUATION.md)
  evaluation loop

manifest と split は `node ../scripts/build-benchmark-manifest.mjs` で再生成できます。

## Repository layout

- `pilot_tasks/`
  raw incident replay に近い高摩擦 split
- `tasks/`
  main corpus
- `research/`
  設計根拠と監査メモ
- `runtime_fixtures/`
  runnable subset 用 baseline
- `validation_runs/`
  local run artifact

## What is SWE-bench-like here

- public prompt は issue text / 実入力に近い
- evaluator 側は hidden answer と rubric を持つ
- split と manifest を dataset として固定する
- accepted fix を gold 側の基準にする

## What is intentionally different

- 問題は公開 OSS issue ではなく、ローカル incident を匿名化して作る
- tests-only ではなく、human rubric と acceptance rubric を併用する
- contamination を避けるため、生 transcript や secret は public に出さない

## Quickstart

1. [splits/pilot.txt](./splits/pilot.txt) か [splits/main.txt](./splits/main.txt) から case を選ぶ
2. モデルには `public/prompt.txt` と `public/env.md` だけを渡す
3. evaluator は `private/golden.md` と `private/eval.yaml` を使う
4. 全体スコアは [rubric.yaml](./rubric.yaml) を使う
5. runnable case だけ `runtime_fixtures/` と `../scripts/new-validation-run.ps1` を使う

## Research and rationale

- [reference_benchmark_alignment.md](./research/reference_benchmark_alignment.md)
- [personal_benchmark_spec.md](./research/personal_benchmark_spec.md)
- [frustration_signals.md](./research/frustration_signals.md)
- [casepack_validation.md](./research/casepack_validation.md)

legacy mirror として `problem.md`, `context.md`, `answer.md`, `rubric.md` も残すが、canonical surface は `prompt.txt`, `env.md`, `golden.md`, `eval.yaml` である。
