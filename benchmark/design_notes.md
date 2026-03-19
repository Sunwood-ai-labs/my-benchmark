# Design Notes

## この benchmark が強く測れる能力
- acceptance_alignment: あなたの受け入れ条件を外さないこと。
- 最小差分での修正収束。
- 「確認したか」「見たか」「本当にその面で出すべきか」を外さないこと。
- 出力面の責務分離、UI 実観測、末端証拠確認、path/version 前提確認。
- blocked を誠実に扱うこと。

## benchmark の基本形
- 基本形は execution harness ではなく case pack である。
- つまり「実入力に近い public prompt + 最低限の environment + accepted fix + rubric」を履歴から作ったこと自体が benchmark の中心成果である。
- runnable fixture は強化要素であり、全ケース必須ではない。
- public 面は `SWE-bench` 的に薄く、private 面は `IFEval` 的に verifiable な rubric を持つのが望ましい。

## 弱くしか測れない能力
- cloud 前提の運用オペレーション。
- 長期の zero-to-one 企画。
- 人間同士の調整や政治性。
- 最新の外部 SaaS 事情への適応。
- wrapper / harness 起因の運用 friction は、task score だけだと過小評価しやすい。そのため実運用では delivery_reliability_score を併記するのが望ましい。

## Codex と Claude Code で差が出そうな観点
- Codex は shell-first orientation と局所修正で有利になりやすい。
- Claude Code は long-context の言語整理や multi-turn 説明で有利な場合がある。
- ただしこの benchmark では、説明のうまさよりも「怒られる failure を避ける」ことを強く見るため、未確認の断定や UI 未観測推測には厳しい。

## 今後増やすべきケース
- 文字化け・encoding 異常を含む観測系 case。
- 実チャネル確認が blocked のときの代替証拠設計 case。
- 反復作業の中で progress message が stale になる automation case。
- 1 つの UI から複数 pane を抽出する content-focus case の派生。
