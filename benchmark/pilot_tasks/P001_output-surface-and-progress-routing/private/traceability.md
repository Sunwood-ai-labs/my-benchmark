# Why This Case Exists
ユーザーの強い不満が「どこに何を出すべきか」を外した時に発生しており、汎用 bugfix よりも体験差が大きかったため。

# Source Pattern Summary
- Discord 側に低レベルログが流れて見にくいという不満。
- CLI に必要な進捗が見えないという不満。
- チャット自動化 repo での観測面分離失敗。

# Evidence Used
- F01: output surface mismatch cluster
- Codex local transcript family with repeated logging complaints

# Abstractions Applied
- 具体的な bot 名、ログ本文、チャンネル名は一般化した。
- 実際の送信文は要約化し、要件だけ残した。

# Leakage Check
- raw transcript の長文引用はしていない。
- 固有の channel ID、user ID、URL は含めていない。
