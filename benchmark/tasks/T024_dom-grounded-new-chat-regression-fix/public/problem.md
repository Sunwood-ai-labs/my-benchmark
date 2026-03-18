# Goal
新規チャット開始の回帰を、実際の DOM 状態を見て最小差分で戻す。

# Background
selector drift を抽象的に扱うと、回帰が長引きやすい。

# Input Context
- new chat trigger の候補 selector が複数ある。

# User Prompt
DOM または screenshot を確認して、new chat 回帰の原因 selector を特定し修正してください。

# Constraints
- layout/CSS を不用意に変更しない。

# Deliverables
- 局所修正
- smoke 結果
