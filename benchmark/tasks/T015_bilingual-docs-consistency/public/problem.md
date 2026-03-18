# Goal
片方だけ古くなった docs surface を必要最小限で同期する。

# Background
README と README.ja のような paired docs の片方が recent change に追随していない。

# Input Context
- canonical doc と stale 側の doc が与えられる。

# User Prompt
古くなった方だけを必要最小限で更新し、無関係な段落の全面書き換えは避けてください。

# Constraints
- 文体や構成を保つこと。
- 全文再翻訳にしないこと。

# Deliverables
- 局所的な docs 更新。
