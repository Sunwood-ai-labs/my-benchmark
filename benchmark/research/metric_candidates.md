# Metric Candidates

この版では「キレた回数」をそのまま点数化するのではなく、そこから抽出した acceptance-alignment 信号を正式候補として扱う。

## 採用した macro axis
| 指標名 | 何を測るか | なぜ重要か | 計測方法 | 自動 / 手動 | スコア範囲 | 重み | 重みの根拠 | 歪み / 弱点 | 使う証拠 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| acceptance_alignment_score | ユーザー受け入れ条件とのズレをどれだけ避けられるか | あなたの不満は objective pass では拾えないズレを示すため | 5 つの acceptance signal の applicable 平均 | automatic plus manual | 0-5 | 30 | 強い frustration signal が局所的でなく再発しているため | task 設計が悪いと signal が発火しにくい | F01-F05 |
| delivery_reliability_score | 実行 runner を通したとき clean に完了し、最終応答が素直に届くか | 実務では「正しい修正をした」だけでなく「ちゃんと終わる」ことも重要なため | timeout、manual recovery、stuck shutdown、最終応答到達可否を run log から採点 | automatic plus manual | 0-5 | reporting-only | artifact score が高くても運用体験が悪いケースを分離するため | runner 固有の問題を多少含む | run logs, wrapper logs, session logs |

## 採用した acceptance signal
| 指標名 | family | 定義 | 計測方法 | 採用理由 | 不採用理由 / 弱点 |
| --- | --- | --- | --- | --- | --- |
| false_done_penalty | reliability_safety | 終わっていないのに done / verified と言う失敗を強く罰する | 末端証拠と完了主張の整合を確認 | キレの強さと trust break が最も一致した | real-world blocked case と区別が必要 |
| verification_gap | outcome_quality | 必要な検証と実施した検証の差 | required verification と executed check を比較 | 「検証した？」の再発が多い | fixture 設計が弱いと測りにくい |
| surface_fit | interaction_cost | 正しい情報を正しい面に出せたか | CLI / chat / report の surface 別に確認 | あなたの不満が表示面ミスに集中した | output 面が単一の case では N/A |
| grounding_before_change | reliability_safety | UI / log / runtime truth を見てから変えたか | DOM, screenshot, log, runtime 証拠の有無を確認 | 推測修正への不満が強い | read-only 調査 task では過剰になりうる |
| assumption_refresh | reliability_safety | path / version / env の truth source を先に確認したか | config, README, metadata, local log を確認 | 誤前提のまま進める失敗を直接測れる | truth source が薄い case では N/A |

## 明示的に不採用にしたもの
| 指標名 | 不採用理由 |
| --- | --- |
| raw_anger_count | ユーザーの表現強度に依存しすぎてノイズが大きい。 |
| all_caps_or_exclamation_score | 文章癖に引っ張られ、失敗の本質を測れない。 |
| single_turn_user_sentiment | タスクの重要度と感情が混ざるため再現性が弱い。 |
