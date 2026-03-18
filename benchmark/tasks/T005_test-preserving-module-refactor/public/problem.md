# Goal
混み合った module を、挙動を変えずに少し整理する。

# Background
hotspot file が読みにくくなっているが、外から見える挙動は変えてはいけない。

# Input Context
- 抽出や整理の seam が1つはある。
- 挙動維持を確かめる check が存在する。

# User Prompt
最小限の構造改善を行い、既存の振る舞いを保ったまま検証してください。

# Constraints
- UI や public contract の設計変更をしないこと。
- 既存 test を不用意に消さないこと。

# Deliverables
- 構造改善。
- 挙動維持の検証。
