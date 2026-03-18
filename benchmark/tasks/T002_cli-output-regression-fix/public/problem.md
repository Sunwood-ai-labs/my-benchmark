# Goal
文字化けや整形崩れを含む CLI 出力の退行を直す。

# Background
terminal 向けツールの出力が recent change 以降、読みにくいか構造的に壊れている。

# Input Context
- 失敗した出力例と関連コマンドがある。
- 回収すべき問題は局所的である。

# User Prompt
CLI 出力を最小差分で正常化し、コマンドライン上で before/after を確認してください。

# Constraints
- 元のコマンド経路をできるだけ維持すること。

# Deliverables
- 局所修正。
- 出力確認メモ。
