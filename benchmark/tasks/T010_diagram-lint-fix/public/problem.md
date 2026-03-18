# Goal
diagram asset の overlap / overflow 系 lint を局所修正で通す。

# Background
図表 asset が border、label、text overflow などの check で落ちている。

# Input Context
- diagram file と lint script または lint 出力がある。

# User Prompt
図そのものか lint support のどちらが原因かを見極め、最小の修正で check を通してください。

# Constraints
- 図全体を描き直さないこと。

# Deliverables
- 局所修正。
- lint 再実行結果。
