# Goal
既存の配置先や version family を思い込みで決めず、install dir / runtime log / version metadata の truth source を先に確認してから修正方針を決める。

# Background
実際の incident では、配置先と current version 前提が外れているまま話が進み、ユーザーは「ここじゃないの？」「最新版でも使えるようにした？」と差し戻した。問題は実装能力以前に、どの path と version が本物かを見ずに進めたことだった。

# Input Context
- README や setup guide に、古い path や stale version family が残っている可能性がある。
- repo か fixture には install dir、runtime log、config 実装、version metadata のいずれかがある。
- incident 当時の要求は、実配置先と現行 version 条件を先に確認し、その前提に合わせて変更か説明を行うことだった。

# User Prompt
実際の配置先と現行バージョン条件を先に確認し、その前提に合わせて修正か説明を行ってください。デフォルト値や古い例を鵜呑みにせず、どの truth source を根拠にしたかを示してください。

# Constraints
- ローカル証拠より一般論を優先しないこと。
- install dir、runtime log、version metadata のいずれも見ずに断定しないこと。
- validation script と truth source を混同しないこと。

# Deliverables
- 修正済みの前提整理
- path/version に合った変更または説明
- 確認に使った truth source
- 変更したファイル名、または変更不要と判断した理由
- 実行した確認手順
