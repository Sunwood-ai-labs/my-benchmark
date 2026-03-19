# my-benchmark

ローカル incident と受け入れ履歴から作った、`SWE-bench` 風の個人最適化 coding-agent benchmark です。

この repo の狙いは、一般的な code benchmark を作ることではなく、**実際にあなたが出した依頼文に近い入力**と、**最終的に受け入れた修正内容**を benchmark として再利用することです。

## この repo の shape

- `benchmark/pilot_tasks/`
  高摩擦な 5 ケース。raw incident replay に近い split
- `benchmark/tasks/`
  main corpus
- `benchmark/cases_manifest.jsonl`
  全 case の machine-readable manifest
- `benchmark/splits/pilot.txt`
  pilot split
- `benchmark/splits/main.txt`
  main split
- `benchmark/TASK_FORMAT.md`
  case format
- `benchmark/EVALUATION.md`
  evaluation loop

## SWE-bench っぽくしたポイント

- public 側は issue text / 実入力 prompt に近い
- private 側に accepted fix と rubric を隠す
- split と manifest を dataset として固定する
- runnable fixture は subset のみ
- validation run artifact は benchmark 本体から分離する

## 使い方

1. `benchmark/splits/pilot.txt` か `benchmark/splits/main.txt` から case を選ぶ
2. モデルには `public/problem.md` と `public/context.md` だけを渡す
3. evaluator は `private/answer.md` と `private/rubric.md` で採点する
4. 必要な case だけ `runtime_fixtures/` で実行確認する

case metadata を更新したら `node scripts/build-benchmark-manifest.mjs` で manifest と split を再生成します。

詳しくは [benchmark/README.md](./benchmark/README.md) を参照してください。
