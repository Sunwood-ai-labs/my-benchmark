# ローカル履歴ベース benchmark

この benchmark は、ローカルの Codex / Claude / git / shell / docs / test 運用から逆算して作った、あなた専用の coding agent 評価パックです。
2026-03-19 の改訂では、一般論寄りの task 群だけでなく、「実際にあなたが強く不満を示した failure pattern」を pilot spine に据え、acceptance_alignment を明示的な評価軸として追加しました。

## 目的
- 最小差分 bugfix、uv 前提の Python 修復、docs build 修正、release 文書同期、multi-agent 設計、中断後 recovery といったローカル実務を測る。
- raw transcript や secret を出さずに、観測されたパターンへトレース可能な benchmark を作る。
- とくに frustration-driven pilot で、地雷を踏まない能力を先に測る。

## benchmark の二層構造
- `pilot_tasks/`: 高摩擦 failure を先に見る 5 ケース。ここは「あなたが怒りやすい失敗」を強く測る。
- `tasks/`: 幅広い実務パターンを測る main corpus。既存 20 ケースに加え、frustration-driven 追加ケースを増やした。

## benchmark 本体と optional 実行層
- benchmark 本体は `public/problem.md`, `public/context.md`, `shared/meta.yaml`, `private/answer.md`, `private/rubric.md`, `private/traceability.md` の case pack である。
- つまり基本形は「Q / A / rubric を履歴から作った評価セット」であり、これだけで採点運用できる。
- `runtime_fixtures/` は benchmark の補助層で、実行型 agent に対して local workspace 付きで試験したいケースだけに付ける。
- したがって全 case に runnable fixture が必要なわけではない。fixture がない case も benchmark として成立する。

## 監査性
- `research/benchmark_sources_manifest.md` で探索した source family を追える。
- `research/frustration_signals.md` で怒りシグナル由来の設計根拠を確認できる。
- `research/evidence_trace_map.md` と `research/sanitization_audit.md` で traceability と leakage 低減方針を確認できる。

## ディレクトリ構成
- `research/`: source manifest、inventory、taxonomy、failure mode、metric、spec、frustration signal など。
- `pilot_tasks/`: calibration 用の 5 ケース。
- `tasks/`: 本番用 case。
- `task_index.md`: 全ケース一覧。
- `pilot_task_index.md`: pilot の選定理由つき一覧。
- `rubric.yaml`: 全体スコア、submetric、frustration overlay。
- `design_notes.md`: 強く測れる能力と今後の拡張方針。

## なぜ public / private / shared を分けるか
- `public/` は評価対象 agent に渡す問題面で、答えの核心を漏らさない。
- `private/` は evaluator 用で、期待解・rubric・traceability を持つ。
- `shared/` は機械処理しやすい metadata を置く。

## 使い方
1. まず `pilot_task_index.md` を見て P001-P005 を回す。
2. gate に引っかかった failure pattern を見て、モデルの弱点を把握する。
3. 問題なければ `task_index.md` から main corpus を回す。
4. 採点は `shared/meta.yaml`、`private/rubric.md`、`rubric.yaml` を合わせて行う。

## 実行ノイズを避ける運用
- 同じ workspace を別モデルで使い回すと、前の差分や生成物が次の run に混ざる。
- runnable なケースは optional に `runtime_fixtures/` に baseline を置き、各評価 run では fresh copy を `validation_runs/` に作って使う。
- `validation_runs/` は local artifact 用で git ignore 済みなので、比較時の repo 差分ノイズを増やさない。

## pilot から本番へ拡張する方法
- pilot で落ちた failure pattern に対応する main case を追加で回す。
- 新しい怒りシグナルが履歴で見えたら `research/frustration_signals.md` に tag を足し、その tag に対応する case を増やす。
- 1 回限りの特殊事例ではなく、再発パターンとして抽象化できたときだけ case 化する。

## 何が測れて何が測れないか
- 強く測れる: scope control、検証の誠実さ、UI 実観測、path/version 前提確認、出力面の適合、recovery。
- 弱くしか測れない: cloud 前提運用、長期 greenfield 企画、対人調整、外部サービスの最新事情依存タスク。
