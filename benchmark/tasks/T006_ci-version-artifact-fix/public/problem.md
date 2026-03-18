# Goal
workflow は動くのに version や artifact がずれている状態を直す。

# Background
build か release pipeline は一応成功するが、公開される版数や成果物名がローカル truth と合っていない。

# Input Context
- workflow file、version metadata、見えている mismatch 症状がある。

# User Prompt
version の source of truth をたどり、最小の workflow または metadata 修正でズレを止めてください。

# Constraints
- release pipeline 全体の再設計に広げないこと。

# Deliverables
- 修正。
- 再発防止を含む説明。
