# Goal
小さな CLI 機能を追加し、README や guide を必要最小限同期する。

# Background
ノイズ削減や初回利用の改善につながる小さな option を増やしたいが、CLI 全体の再設計は不要。

# Input Context
- CLI entrypoint と docs が近くにある。
- 追加したい振る舞いは narrow である。

# User Prompt
既存 CLI の流れに沿って option を追加し、必要な docs だけ更新して、最短の確認コマンドを示してください。

# Constraints
- CLI 全体の設計変更に広げないこと。

# Deliverables
- 機能追加。
- docs 更新。
- 確認コマンド。
