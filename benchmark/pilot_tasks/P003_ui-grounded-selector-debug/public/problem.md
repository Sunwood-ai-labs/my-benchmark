# Goal
live UI の状態遷移を観測し、popup や surface drift を見落とさずに、無関係なレイアウトを壊さず selector / 探索ロジックを最小差分で直す。

# Background
実際の incident では、新しい操作フローを自動化する browser task が live UI の権限 popup や pane 状態遷移で詰まっていたのに、観測なしで selector をいじったため、症状の本体を外したまま別の UI を壊しやすかった。ユーザーが求めていたのは「今見えている UI を確認してから押せ」という対応だった。

# Input Context
- 既存の selector fallback や diagnostic script がある。
- screenshot、DOM dump、raw debug artifact、または live browser 観測のいずれかが利用できる。
- incident 当時の要求は、初回だけでなく再実行時の状態差や popup の有無も含めて UI を見て判断することだった。

# User Prompt
実際の UI 状態を確認し、どの surface で詰まっているかを先に特定してから、最小差分で selector または探索ロジックを直してください。permission popup や pane 状態の違いを見落とさず、レイアウト側には不要な変更を入れないでください。

# Constraints
- screenshot、DOM、raw debug artifact、live browser 観測のいずれも見ずに推測修正しないこと。
- 見た目のレイアウト調整で誤魔化さないこと。
- 無関係な CSS / UI 文言変更を混ぜないこと。

# Deliverables
- 実観測に基づく最小差分修正
- どの UI 状態差または popup が原因だったかの説明
- 初回と再実行で UI を壊していない確認
