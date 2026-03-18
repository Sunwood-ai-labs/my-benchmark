# Why This Case Exists
「単体で通った」だけでは信頼されず、実利用面に触れるかどうかで評価が大きく変わるため。

# Source Pattern Summary
- Discord へのテストは必須という明示要求。
- ローカル成功と実面確認の区別不足。

# Evidence Used
- F02: incomplete verification cluster

# Abstractions Applied
- 実チャネル名や外部面は一般化した。

# Leakage Check
- チャンネル名や credential は含めていない。
