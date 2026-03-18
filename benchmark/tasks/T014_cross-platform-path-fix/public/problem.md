# Goal
Windows と bash / WSL のどちらかでだけ壊れる path / quoting 問題を直す。

# Background
ある shell では動くのに、別の shell 文脈では quoting や separator の違いで失敗する。

# Input Context
- 最低2種類の shell 文脈か、差分が分かる log がある。

# User Prompt
絶対パスの埋め込みに逃げず、cross-shell で成立する path handling に直してください。

# Constraints
- ローカルの絶対 user path を埋め込まないこと。

# Deliverables
- path-safe 修正。
- 確認手順。
