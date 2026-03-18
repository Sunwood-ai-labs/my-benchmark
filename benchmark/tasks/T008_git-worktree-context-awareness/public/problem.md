# Goal
main clone ではない作業場所でも、安全な root と branch を素早く把握する。

# Background
利用者は worktree か detached 文脈におり、雑に git を打つと対象を取り違えやすい。

# Input Context
- path のヒントと branch / worktree metadata がある。

# User Prompt
現在の repo 文脈を説明し、安全な working root と次の確認コマンドを提案してください。まだ編集はしないでください。

# Constraints
- 破壊的 git 操作はしないこと。

# Deliverables
- orientation メモ。
- 安全な次の一手。
