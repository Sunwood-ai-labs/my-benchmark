# Why This Case Exists
途中まで通ったテストを「完了」と扱う失敗が、実務上もっとも信頼を落とすパターンの一つだったため。

# Source Pattern Summary
- 履歴が取れているか怪しいという明示的不満。
- Discord への実テスト未実施への強い不満。

# Evidence Used
- F02: incomplete verification cluster
- Claude history verification complaints

# Abstractions Applied
- 具体的な履歴名やツール名は一般化した。
- 末端状態の種類を複数許容できる形に抽象化した。

# Leakage Check
- 会話内容や生成物本文の生引用はしていない。
- channel 名や workspace 固有名は除去した。
