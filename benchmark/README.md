# Benchmark

このディレクトリは、ローカル incident を元にした personal SWE-bench-style benchmark です。

## Core Idea

この benchmark で主に見たいのは、モデルが何を考えたかではなく、最後に何を生成したかです。

- model-facing input: `public/prompt.txt`, `public/env.md`
- evaluator-facing truth: `private/golden.md`, `private/eval.yaml`
- primary judged object: 生成物、最終返答、検証ログ、surface に出た実際の出力
- secondary judged object: diff や touched-file scope。これは overchange と safety の確認用です

要するに、diff は補助情報であって主役ではありません。あなたが普段そうしているように、この benchmark でも基本は生成物ベースで採点します。

## Artifact-First Rule

- meaningful な生成物がない task は、原則として高得点になりません
- task に対して意味のある生成物が出ていないのに blocked でもない場合、その case はデフォルトで `3 / 10` を上限にします
- blocked が許容される case でも、boundary note や verification note などの operator-facing artifact は必要です

## Dataset Surface

- [cases_manifest.jsonl](./cases_manifest.jsonl)
  model-facing stripped manifest
- [private_cases_manifest.jsonl](./private_cases_manifest.jsonl)
  evaluator-facing internal manifest
- [public_dataset/README.md](./public_dataset/README.md)
  model-facing bundle の説明
- [splits/pilot.txt](./splits/pilot.txt)
  pilot split
- [splits/main.txt](./splits/main.txt)
  main split
- [TASK_FORMAT.md](./TASK_FORMAT.md)
  case format
- [EVALUATION.md](./EVALUATION.md)
  evaluation loop

manifest、public bundle、split は `node ../scripts/build-benchmark-manifest.mjs` で再生成できます。

## Repository Layout

- `pilot_tasks/`
  pilot case packs
- `tasks/`
  main corpus
- `research/`
  design memo と調査結果
- `reports/`
  run ごとの summary、task report、score artifact
- `runtime_fixtures/`
  runnable subset 用 baseline
- `validation_runs/`
  local execution artifact

## What Is SWE-bench-Like

- public side は issue-like prompt と minimal env だけ
- private side は accepted fix と hidden rubric
- split と manifest を dataset surface として固定
- runnable fixture は subset のみ

## What Is Intentionally Different

- 公開 OSS issue ではなく、ローカル incident を抽象化した case を使う
- hidden tests だけでなく、acceptance alignment と human rubric を使う
- transcript や secret を public に出さない
- diff-first ではなく artifact-first で採点する

## Quickstart

1. [splits/pilot.txt](./splits/pilot.txt) か [splits/main.txt](./splits/main.txt) から case を選ぶ
2. モデルには `public_dataset/` 側の stripped manifest と各 case の `public/` だけを渡す
3. evaluator は `private/golden.md` と `private/eval.yaml` を使う
4. 全体スコアは [rubric.yaml](./rubric.yaml) を使う
5. runnable case だけ `runtime_fixtures/` と `../scripts/new-validation-run.ps1` を使う

## Packaging Rule

- model-facing bundle は `public_dataset/` のみ
- `private_cases_manifest.jsonl`、`private/`、`shared/`、`research/` は evaluator / curator 用
- root の `benchmark/` 全体をそのままモデルに見せない

## Research And Rationale

- [reference_benchmark_alignment.md](./research/reference_benchmark_alignment.md)
- [personal_benchmark_spec.md](./research/personal_benchmark_spec.md)
- [frustration_signals.md](./research/frustration_signals.md)
- [casepack_validation.md](./research/casepack_validation.md)

legacy mirror として `problem.md`, `context.md`, `answer.md`, `rubric.md` も残していますが、canonical surface は `prompt.txt`, `env.md`, `golden.md`, `eval.yaml` です。
