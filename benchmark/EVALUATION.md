# Evaluation

この benchmark は `public` と `private` を分けて運用します。

## Evaluation Loop

1. case を選ぶ
2. モデルには `public_dataset/` 側の manifest と対象 case の `public/` だけを渡す
3. まず generated artifacts を回収する
4. その後に evaluator が `private/golden.md` と `private/eval.yaml` で採点する
5. runnable case なら auto-check を回す

ここでいう generated artifacts には次が含まれます。

- 生成されたファイル
- surface に出た実際の出力
- final response
- executed check log
- verification note
- blocked note

## Artifact-First Scoring

- primary judged object: generated artifacts と final surfaced output
- secondary judged object: diff / touched-file scope
- diff は overchange と safety の判定に使う。主スコアの中心にはしない

## No-Artifact Cap

- meaningful な生成物がない
- blocked でもない
- final response だけで終わっている

この条件なら、その case はデフォルトで `3 / 10` cap にします。

## Score View

トップレベル定義は [rubric.yaml](./rubric.yaml) を使います。

- `overall_score`
  case pack 自体の canonical score
- `delivery_reliability_score`
  wrapper / orchestrator / automation harness 越しで clean に終わったか
- `stack_score`
  上の 2 つを合わせた run-layer score

この benchmark は true `0-10` を canonical score として使います。

## Automatic And Manual Evaluation

自動評価では主に次を見ます。

- task-specific test または focused smoke
- build / docs validation
- generated artifact presence
- fixture-specific state check
- acceptance signal condition check
- touched-file scope check

人手評価では主に次を見ます。

- generated artifact の受け入れ可能性
- instruction following
- assumption quality
- explanation usefulness
- recovery judgment
- acceptance alignment

## Run Report Requirements

各 run report には最低限次を入れます。

- task ごとの report
- task ごとの score
- machine-readable な score artifact
- score reason
- generated outputs
- 使った evidence
- 足りなかった evidence
- 実際の agent / subagent の挙動
- second-pass / devil audit / material review の結果
- run mode と制約

run 全体の雛形は [RUN_REPORT_TEMPLATE.md](./RUN_REPORT_TEMPLATE.md) を使い、task ごとの雛形は [TASK_REPORT_TEMPLATE.md](./TASK_REPORT_TEMPLATE.md) を使います。

## Runnable Subset

全 case を runnable にする必要はありません。

- benchmark 本体は case pack
- optional runtime は `runtime_fixtures/`
- local execution artifact は `validation_runs/`

この benchmark では、benchmark 本体と execution harness を分けて扱います。
