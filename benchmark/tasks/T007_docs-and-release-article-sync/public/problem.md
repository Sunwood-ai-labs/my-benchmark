# Goal
ローカル差分に基づいて release note や関連記事を正しく揃える。

# Background
release article、changelog、README のどれかが、実際の変更内容とずれている。

# Input Context
- git diff の文脈と docs surface が与えられる。

# User Prompt
ローカル差分だけを根拠に、release-facing な文書を修正してください。根拠のない盛りは避けてください。

# Constraints
- web 調査を使わないこと。
- ローカル差分と成果物にアンカーすること。

# Deliverables
- 修正文書。
- 根拠メモ。
