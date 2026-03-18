# 関連ファイルと前提
- 完全な外部接続がなくても、少なくとも sandbox chat channel、staging bridge、recorded relay のいずれかの確認点がある。
- 外部設定や権限が揃わないと live 確認が blocked になる場合がある。
- incident の前提は「local pass と real-surface confirmation が別物」である。

# 最小仕様
- 実面確認の有無が明確。
- 必須外部設定の不足があれば明示される。
- 確認不能部分が曖昧にぼかされない。
- 既存 test の価値も否定せず整理する。

# fixture について
- fixture は sandbox channel、staging endpoint、recorded bridge のいずれかでよい。
- 実 payload に近い画像や message body を 1 つ持てるとよい。

# 評価上の注意
- verified と blocked の言い分けが評価の中心。
- real-surface equivalent を mock と取り違えないこと。
