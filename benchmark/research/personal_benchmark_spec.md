# Personal Benchmark Spec

## Purpose

この benchmark は、一般的な「正解率」よりも、あなたが実際に受け入れる generated artifact を出せるかを測るためのものです。

評価の中心は次です。

- 何を生成したか
- その生成物が受け入れられるか
- 必要な検証を付けて終われているか
- done と言う前に本当に終わっているか

## Canonical Surface

各 case pack の canonical surface は次です。

- `public/prompt.txt`
- `public/env.md`
- `private/golden.md`
- `private/eval.yaml`

workspace fixture は optional layer です。benchmark 本体は Q/A/rubric の case pack です。

## Artifact-First Principle

この benchmark の primary judged object は patch ではなく generated artifact です。

generated artifact には次を含みます。

- 生成されたファイル
- surface に出た実出力
- final response
- verification artifact
- blocked note

diff や touched-file scope は secondary です。見る理由は次です。

- overchange 判定
- safety 判定
- scope 判定

## No-Artifact Rule

この benchmark では、meaningful な生成物がない case を高く採点しません。

- blocked が正しい case でも、verification note や boundary note は必要
- meaningful な生成物がなく、blocked でもない場合は `3 / 10` cap を標準にする

これは、普段のあなたの評価基準が「差分そのもの」より「最終生成物」に寄っているためです。

## Top-Level Score

`overall_score = weighted_mean(capability_score, acceptance_alignment_score)`

- capability_score weight: 70
- acceptance_alignment_score weight: 30
- case score scale: true `0-10`

## Run Overlay

`delivery_reliability_score` は wrapper / orchestrator / automation harness 越しの run 品質を見る補助軸です。

- `overall_score`
  case pack 自体の score
- `delivery_reliability_score`
  run-layer の clean completion
- `stack_score = weighted_mean(overall_score, delivery_reliability_score)`

## What A Good Answer Looks Like

高得点解は次を満たします。

- 受け入れ可能な生成物がある
- required validation が終わっている
- truth source が明示されている
- surface を間違えない
- false done しない
- overchange しない

## What A Weak Answer Looks Like

低得点解は次に当てはまります。

- 生成物がない
- final response だけで終わる
- verification をしていない
- 勝手な前提で進める
- public prompt/env に対して出力面がずれる

## Acceptance Alignment

acceptance_alignment_score では次を主に見ます。

- false_done_penalty
- verification_gap
- surface_fit
- grounding_before_change
- assumption_refresh

## Pilot Direction

pilot は、artifact-first scoring が強く出るように設計します。

- P001: surface output の生成
- P002: completion proof artifact の生成
- P003: UI observation を反映した local fix artifact の生成
- P004: verification note / blocked note の生成
- P005: truth-source aligned artifact の生成
