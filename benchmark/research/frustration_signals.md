# Frustration Signals

このメモは、ローカル履歴のうち「ユーザー不満が強く出た箇所」を benchmark 設計へ反映するための要約です。
raw transcript は貼らず、抽象化した failure pattern と source family だけを残しています。怒りの強さそのものではなく、そこから抽出した acceptance-alignment 信号を評価に使います。

## 抽出方針
- Codex local transcripts の user message 系イベントを走査。
- Claude history の display を補助的に使用。
- 「なんで」「ちゃんと」「壊れた」「検証した」「ここじゃないの」などの強い不満語を起点に cluster 化。
- 同一文の重複 line はそのまま件数に含むため、厳密な unique turn 数ではなく evidence volume として扱う。

## 高信頼の frustration pattern
| Tag | Pattern Label | Evidence Volume | Primary Complaint | benchmark への反映 |
| --- | --- | --- | --- | --- |
| F01 | Output Surface Mismatch | 58 hits | 詳細ログをユーザー面に流し、欲しい進捗が CLI に出ない。 | P001, T021 |
| F02 | Incomplete Verification | 13 hits | 途中成功を完了扱いし、履歴や実チャネル確認がない。 | P002, P004, T023 |
| F03 | UI Not Grounded | high volume | 実 UI を見ずにレイアウトや selector を推測変更する。 | P003, T024 |
| F04 | Path / Version Assumption Error | 14 hits | 実 path や現行 version を確認せずに進める。 | P005, T025 |
| F05 | Response Extraction Noise | low volume / high severity | 本文ではなく UI chrome を抽出してしまう。 | T022 |

## 設計上の含意
- あなた向け benchmark では「汎用的に賢いか」より「地雷を踏まないか」の方が重要。
- とくに hard fail 相当なのは、未確認なのに verified と言うこと、UI を見ずに推測修正すること、出力面を取り違えること。
- そのため pilot は frustration-driven に再構成し、一般的な難問よりも high-friction failure を先に測る構成にした。
