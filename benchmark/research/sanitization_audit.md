# Sanitization Audit

生成後に行った leakage 低減チェックの記録です。

## scan ルール
- 生成済み benchmark ファイルから、`auth.json`、`cap_sid`、`.credentials.json`、`.sandbox-secrets`、`mcp-needs-auth-cache.json` などの secret-adjacent filename を確認した。
- 各 `traceability.md` が raw transcript や prompt text ではなく、abstract source family と evidence tag で書かれているか確認した。
- source manifest では、公開版に合わせてローカル absolute path を環境変数ベースの匿名表記へ置き換えた。

## 結果
- 生成された benchmark ファイル内に、auth / credential 内容の転載はない。
- case traceability は raw session id や prompt 原文ではなく evidence tag ベースにした。
- source manifest の path は `%USERPROFILE%` や `%APPDATA%` ベースの匿名表記へ差し替えた。

## 残留リスク
- transcript 系ソース自体は upstream input として高リスクのままなので、今後も summary-only で扱う必要がある。
- 外部公開時も、repo family 名や transcript 原文をこれ以上具体化しない運用を維持するべきである。
