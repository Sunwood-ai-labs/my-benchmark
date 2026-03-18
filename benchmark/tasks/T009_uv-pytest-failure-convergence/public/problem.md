# Goal
uv 管理の Python repo で、狭い pytest failure を素早く収束させる。

# Background
小さな recent change により test が壊れたが、依存更新や全面整理をする必要はない。

# Input Context
- 失敗 test と周辺 source path がある。

# User Prompt
repo 標準の uv 経路で test を再現し、原因を絞って最小差分で直してください。

# Constraints
- pytest は uv 経由で走らせること。
- requirements の広い整理をしないこと。

# Deliverables
- test を直す変更。
- passing check。
