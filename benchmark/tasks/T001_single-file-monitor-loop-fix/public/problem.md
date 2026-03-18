# Goal
1ファイル ownership を守りながら監視ループの退行を直す。

# Background
JS の監視ループが状態遷移を取りこぼすか、deferred 状態を長く保持しすぎる。

# Input Context
- 担当ファイルは1つだけで、周辺には test または log がある。
- 不具合は narrow で before/after がはっきりしている。

# User Prompt
担当ファイルの中だけで監視ループを修正し、挙動確認を行ってください。隣接 module には触れないでください。

# Constraints
- 担当外ファイルを編集しないこと。
- 見た目の整理や style cleanup を混ぜないこと。

# Deliverables
- 1ファイル修正。
- 短い挙動確認メモ。
