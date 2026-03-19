# Evaluation

この benchmark は `public` と `private` を分けて運用する。

## 基本ループ

1. case を選ぶ
2. モデルには `public/problem.md` と `public/context.md` だけを渡す
3. repo / fixture の初期状態で解かせる
4. evaluator は `private/answer.md` と `private/rubric.md` で採点する
5. 必要なら auto-check / runnable fixture を併用する

## スコアの考え方

トップレベルは [rubric.yaml](./rubric.yaml) を使う。

- `capability_score`
  問題を解けたか
- `acceptance_alignment_score`
  あなたの受け入れ条件を外していないか
- `delivery_reliability_score`
  wrapper / orchestrator 経由で clean に運用できたか

通常の比較では `0-10` 表示を使う。

## SWE-bench っぽい運用方針

- public prompt は薄くする
- private evaluator 面を厚くする
- hidden answer を public に漏らさない
- split は dataset として固定する
- runnable 環境は subset だけに付ける

## どこまで runnable にするか

全 case を runnable にする必要はない。

- benchmark 本体: case pack
- optional runtime: `runtime_fixtures/`
- local run artifacts: `validation_runs/`

この分離で、benchmark 自体と execution harness を混ぜない。
