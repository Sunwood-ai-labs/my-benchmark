# Why This Case Exists
「単体で通った」だけでは信頼されず、実利用面に触れるかどうかで評価が大きく変わるため。

# Source Pattern Summary
- test channel への live 確認は必須という明示要求。
- ローカル成功と実面確認の区別不足。
- 外部設定不足なら blocked を切るべきなのに、その境界が曖昧だった。

# Evidence Used
- F02: incomplete verification cluster
- local incident seed: 実画像や実 payload shape を sandbox chat channel へ送り、reply まで見ろという要求

# Prompt Frame
- 元の要求は generic な integration test ではなく、「用意した test channel に実際に送って reply まで確認してほしい」という real-surface specific なものだった。
- そのため problem では sandbox chat channel と同等の real-surface equivalent を明示した。

# Environment Frame
- chat bot / integration repo で、local test はあるが real-surface equivalent の確認経路が別にある。
- live 確認には外部設定や権限が必要で、不足時は blocked がありうる。

# Abstractions Applied
- 実チャネル名、サービス名、資格情報名は一般化した。
- 公開 benchmark では sandbox chat channel / staging bridge / recorded relay という class レベルに留めた。

# Leakage Check
- チャンネル名や credential は含めていない。
