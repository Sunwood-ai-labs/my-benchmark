# Goal
応答送信後に履歴 store まで更新されたことを検証に含める。

# Background
途中成功だけでは、後段の履歴欠落を見逃しやすい。

# Input Context
- send success と history persistence が別段階にある。

# User Prompt
履歴 store まで含めた check を追加してください。

# Constraints
- history format 自体を大改造しない。

# Deliverables
- assertion 追加
- proof path 説明
