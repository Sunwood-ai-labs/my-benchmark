# Reference Benchmark Alignment

この benchmark をどの既存 benchmark に寄せるべきかを、公式ソースベースで整理したメモ。

## 結論
- もっとも近い土台は `SWE-bench`。
- runnable case の運用は `Terminal-Bench` を参考にする。
- UI / real-surface 系の一部 case だけ `OSWorld` 的な初期状態と完了条件の考え方を借りる。
- `Constraints` や `Output` のような verifier 向け条件は `IFEval` 的な private rubric に閉じ込める。

## 1. SWE-bench がいちばん近い

近い理由:
- モデルには public な問題文だけを渡す。
- evaluator 側は hidden tests や gold patch を持つ。
- repo の初期状態が評価の中心にある。

公式ソース:
- OpenAI は SWE-bench について「モデルは original issue text と修正前 repo 状態だけを見て、tests は見ない」と説明している。
- OpenAI は同時に、task statement と tests のずれや contamination を問題として挙げている。

設計に取り込む点:
- `public/problem.md` は issue text / 実入力 prompt に近づける。
- evaluator 向けの期待条件は `private/` に寄せる。
- 正解は「accepted fix」寄りに持つ。

設計に取り込まない点:
- 公開 OSS issue をそのまま benchmark 問題にするやり方。
- open benchmark として広く流通させることで contamination しやすくなる形。

この benchmark への意味:
- あなた向け benchmark は「説明の整った課題文」より、「実際に飛んできた prompt + 修正前状態 + private evaluator 面」に寄せるのが正しい。

Sources:
- https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- https://github.com/SWE-bench/SWE-bench

## 2. IFEval は public prompt ではなく private rubric に近い

近い理由:
- instruction following を verifiable instruction で測る。
- 自動チェックしやすい形式条件を evaluator 側に持てる。

設計に取り込む点:
- `false_done_penalty`
- `verification_gap`
- `surface_fit`
- `scope_control`
- `grounding_before_change`

設計に取り込まない点:
- public prompt に verifier 向け制約を全部書き込むこと。

この benchmark への意味:
- `Constraints` や `Output` を public 問題面に置きすぎると、instruction benchmark になってしまう。
- それらは private rubric / auto-check へ送るのがよい。

Sources:
- https://arxiv.org/abs/2311.07911
- https://github.com/google-research/google-research/tree/master/instruction_following_eval

## 3. Terminal-Bench は runnable subset の参考になる

近い理由:
- realistic task を実行環境ごと評価する。
- task quality と verification quality を重視している。

設計に取り込む点:
- runnable case は少数精鋭にする。
- fixture は fresh initial state から毎回切る。
- task pack と execution harness を分ける。

設計に取り込まない点:
- 全 case を runnable にする前提。
- benchmark 本体を harness 中心にしてしまうこと。

この benchmark への意味:
- `runtime_fixtures/` は benchmark 本体ではなく optional subset でよい。
- `validation_runs/` は local artifact として分離し、採点本体と混ぜない。

Sources:
- https://www.tbench.ai/news/announcement-2-0
- https://www.tbench.ai/

## 4. OSWorld は UI / real-surface 系だけに使える

近い理由:
- 現実に近い computer-use task を初期状態から評価する。
- 表面的な回答ではなく、状態変化と task completion を見る。

設計に取り込む点:
- UI 系 case は初期状態、観測可能証拠、完了条件を明確にする。
- 「見たかどうか」を採点軸に入れる。

設計に取り込まない点:
- benchmark 全体を desktop automation benchmark に寄せること。

この benchmark への意味:
- P003 や P004 など一部の pilot にだけ、この発想を使う。

Sources:
- https://os-world.github.io/
- https://github.com/xlang-ai/OSWorld

## 採用する設計原則

今後の benchmark は、基本的に次の shape に寄せる。

### Public
- `problem.md`: 実際の依頼文に近い prompt 本文だけ
- `context.md`: 最低限の repo / environment / available evidence

### Private
- `answer.md`: accepted fix と evaluator メモ
- `rubric.md`: acceptance / overchange / verification / scope / grounding
- `traceability.md`: incident 由来の説明

### Optional runtime
- `runtime_fixtures/`: runnable な少数ケースだけ
- `validation_runs/`: local-only artifact

## 今回の明確な方針

- `public/problem.md` に evaluator 向け `Constraints` や `Output` を書かない。
- それらは `private/rubric.md` と auto-check に寄せる。
- benchmark 本体は `SWE-bench` 寄り、acceptance rubric は `IFEval` 的に検証可能、runnable subset は `Terminal-Bench` 的に扱う。
