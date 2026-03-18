# Goal
応答抽出結果から model list や mode list などの UI chrome を除き、本当に欲しい本文だけを返す。

# Background
抽出ロジックが UI 上の周辺要素まで拾い、本来の assistant 本文が埋もれている。

# Input Context
- 抽出対象は複数カードや pane を持つ UI である。
- 本文と chrome が近接している。

# User Prompt
実際の UI 構造を見て、本文抽出の境界を見直してください。本文以外の chrome を拾わないことを focused に確認してください。

# Constraints
- 全文 parser を全面 rewrite しない。

# Deliverables
- 抽出ロジック修正
- focused fixture または golden check
