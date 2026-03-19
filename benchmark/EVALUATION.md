# Evaluation

この benchmark は `public` と `private` を分けて運用する。

## 基本ループ

1. case を選ぶ
2. モデルには `public_dataset/` 側の stripped manifest と各 case の `public/` だけを渡す
3. repo / fixture の初期状態で解かせる
4. evaluator は `private/golden.md` と `private/eval.yaml` で採点する
5. 必要なら auto-check / runnable fixture を併用する

repo root ごと benchmark を渡さない。`private/`、`shared/`、`research/`、internal manifest は evaluator 面である。

## スコアの考え方

トップレベルは [rubric.yaml](./rubric.yaml) を使う。

- `capability_score`
  問題を解けたか
- `acceptance_alignment_score`
  あなたの受け入れ条件を外していないか
- `delivery_reliability_score`
  wrapper / orchestrator 経由で clean に運用できたか

現在の benchmark は true `0-10` を canonical score として扱う。5 段階を単純に 2 倍表示する運用はやめる。

## SWE-bench っぽい運用方針

- public prompt は薄くする
- private evaluator 面を厚くする
- hidden answer を public に漏らさない
- split は dataset として固定する
- runnable 環境は subset だけに付ける

## Case 評価の順番

1. `required_evidence` が揃っているかを見る
2. `auto_check_contract` の pass/fail を埋める
3. `hard_fail_conditions` を確認する
4. `score_anchors` に沿って 1-5 を付ける
5. case weight と split に従って dataset 集計する

## どこまで runnable にするか

全 case を runnable にする必要はない。

- benchmark 本体: case pack
- optional runtime: `runtime_fixtures/`
- local run artifacts: `validation_runs/`

この分離で、benchmark 自体と execution harness を混ぜない。

## Dataset 集計

- case comparison は pinned な manifest / split version ごとに行う
- dataset score は selected split の active case だけを `benchmark_weight` で重み付けして集計する
- case に applicable な acceptance signal がない場合、その case の `overall_score` は `capability_score` のみで計算する
- `delivery_reliability_score` は wrapper / orchestrator を固定した run 群にだけ重ねる

## Run Report Requirements

比較や再採点に使う run report には、最低でも次を書く。

- task ごとの report
- task ごとの score
- 機械可読な score artifact
- case ごとの score
- score を付けた理由
- 使った evidence
- 実際の agent / subagent の挙動
- second-pass / devil audit / material review の結果
- run mode の制約

report の雛形は [RUN_REPORT_TEMPLATE.md](./RUN_REPORT_TEMPLATE.md) を使う。
task ごとの report 雛形は [TASK_REPORT_TEMPLATE.md](./TASK_REPORT_TEMPLATE.md) を使う。
