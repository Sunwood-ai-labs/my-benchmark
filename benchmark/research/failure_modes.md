# Failure Modes

ローカル履歴で実際に強い不満につながった failure pattern を優先して整理した一覧です。

| failure mode | 何が起きたか | どう検出したか | benchmark への反映 |
| --- | --- | --- | --- |
| 出力面の取り違え | CLI に出すべき詳細ログをチャット面に流し、逆に必要な進捗が見えない。 | logging complaint cluster、surface mismatch evidence | P001, T021 |
| 途中成功の完了扱い | send success や smoke pass をもって、履歴や成果物未確認のまま完了宣言する。 | verification complaint cluster、history doubt | P002, P004, T023 |
| UI 実観測なしの推測修正 | DOM / screenshot / diagnostic を見ずに selector や layout を触る。 | layout complaint cluster、selector regression turns | P003, T024 |
| 実チャネル未確認 | 単体 test は通るが、本当に必要な利用面の確認をしていない。 | mandatory integration complaint | P004 |
| path / version 前提ミス | 実 path や現行 version を確認しないまま古い前提で進める。 | path/version complaint cluster | P005, T025 |
| 応答抽出ノイズ | 本文ではなく model list や mode list など UI chrome を拾う。 | extraction noise complaint | T022 |
| overchange | 局所修正で済むのに広範囲変更が混ざる。 | diff scope と unrelated file touch | 既存 main corpus + revised pilot 全般 |
| blocked 状態の曖昧化 | 確認できないのに verified と言う、または blocked をぼかす。 | final explanation と local check の不一致 | P004, rubric overlay |

## 観測上の重み付け
- F01 から F04 は再現頻度と不満強度の両方が高い。
- F05 は件数は少ないが、1 回踏むと成果物価値を大きく損なう高 severity パターン。
- したがって pilot は頻度よりも severity を優先して構成した。
