# Task Format

この repository では、各 task は `SWE-bench` 風の case pack として持つ。

## 基本形

各 case directory は次を持つ。

- `public/problem.md`
  モデルに渡す prompt 本文。できるだけ実際の依頼文に寄せる。
- `public/context.md`
  最低限の repo / environment / evidence 情報。
- `shared/meta.yaml`
  機械可読メタデータ。
- `private/answer.md`
  evaluator 向けの accepted fix / expected outcome。
- `private/rubric.md`
  evaluator 向け rubric。
- `private/traceability.md`
  ローカル incident との対応関係。

## 何を public に置くか

`public/` は issue text に近い面であり、次だけを置く。

- 実際の依頼文に近い prompt
- 最低限の環境情報
- 問題を解くのに必要な観測可能証拠の種類

`public/` に置かないもの:

- evaluator 向けの採点観点
- hidden answer に相当するヒント
- verifier 向けの細かい採点条件

## 何を private に置くか

`private/` は hidden evaluator 面であり、次を置く。

- accepted fix の特徴
- hard fail 条件
- overchange / false done / verification gap の扱い
- traceability と leakage guardrail

## SWE-bench との対応

- `public/problem.md` = issue text に相当
- `public/context.md` = repo state / minimal context
- `private/answer.md` = gold patch の説明版
- `private/rubric.md` = hidden tests + human rubric のハイブリッド
- `runtime_fixtures/` = runnable subset 用の optional environment

## 追加の機械可読面

- `benchmark/cases_manifest.jsonl`
  全 case の dataset manifest
- `benchmark/splits/pilot.txt`
  pilot split
- `benchmark/splits/main.txt`
  main split
