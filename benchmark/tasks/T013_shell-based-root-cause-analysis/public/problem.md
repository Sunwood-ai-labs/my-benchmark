# Goal
短い shell log と repo 状態から有力な原因を絞り、次アクションを出す。

# Background
利用者は『壊れた』と言うが、最も信用できる証拠は短いコマンド履歴と repo 現在地だけである。

# Input Context
- shell excerpt、repo snapshot、必要なら failing command が与えられる。

# User Prompt
ローカル証拠だけを使ってもっとも有力な原因を説明し、観測事実と仮説を分けたうえで次の一手を提案してください。

# Constraints
- 存在しないログを想像で補わないこと。
- 不確実な点は仮説として明記すること。

# Deliverables
- 診断メモ。
- 次の確認手順。
