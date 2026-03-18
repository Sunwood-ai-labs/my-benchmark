# my-benchmark

ローカル履歴から設計した、個人最適化型の coding agent benchmark です。
メインの成果物は [benchmark/README.md](./benchmark/README.md) 以下にあります。

## このリポジトリにあるもの
- `benchmark/`: benchmark 本体。research、pilot tasks、main tasks、rubric を含みます。
- `benchmark/research/`: 設計根拠、失敗モード、評価指標、traceability の整理。
- `benchmark/pilot_tasks/`: 高摩擦パターンを先に見る 5 ケース。
- `benchmark/tasks/`: 本番用 25 ケース。

## 使い方
1. [benchmark/pilot_task_index.md](./benchmark/pilot_task_index.md) から pilot 5 件を回します。
2. 受け入れ条件を外しやすい failure pattern を把握します。
3. 問題なければ [benchmark/task_index.md](./benchmark/task_index.md) から main corpus を回します。
4. 採点は `public/` をモデルに渡し、`private/` と [benchmark/rubric.yaml](./benchmark/rubric.yaml) を evaluator が使います。

## この benchmark が重視するもの
- 最小差分 bugfix と過剰変更の抑制
- 指示遵守と repo 理解速度
- 検証の誠実さと false done の回避
- UI / 実物への grounding
- path / version 前提の勝手な固定を避けること

## 公開版の注意
- local transcript は raw で転載せず、抽象化した evidence と task へ変換しています。
- source path は公開版向けに匿名化しています。
- `public/` と `private/` を分けているため、そのまま評価運用に使えます。
