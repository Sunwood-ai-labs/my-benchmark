# Goal
詳細ログとユーザー通知を適切な面に分け、同一イベントの二重送出も防ぐ。

# Background
見にくいログがユーザー面に流れ、進捗が必要な場所では不足している。

# Input Context
- 既存 formatter と sender が近接している。
- ユーザー通知面は短文前提。

# User Prompt
ユーザー向け通知と CLI 診断の責務を整理して、不要なノイズと二重出力を解消してください。

# Constraints
- 全体アーキテクチャを作り直さない。

# Deliverables
- 局所修正
- 差の分かる確認結果
