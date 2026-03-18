# Why This Case Exists
ユーザーの強い不満が「どこに何を出すべきか」を外した時に発生しており、汎用 bugfix よりも体験差が大きかったため。

# Source Pattern Summary
- ユーザー向け chat 面に低レベルログが流れて見にくいという不満。
- 長い処理中に CLI で進捗が追えないという不満。
- 同じ event stream を両面にそのまま流したことによる surface mismatch。

# Evidence Used
- F01: output surface mismatch cluster
- Codex local transcript family with repeated logging complaints
- local incident seed: long-running job 中の「進捗は CLI、短報はチャット」という要求

# Prompt Frame
- 元の要求は generic な logging 改善ではなく、「CLI を見れば進捗が分かり、チャットには短い進捗だけが欲しい」という surface-specific 指示だった。
- そのため problem では terminal と chat relay の役割差を明示し、短報と詳細診断を分ける incident として再構成した。

# Environment Frame
- 長時間ジョブを走らせる bot / automation で、terminal とユーザー向け chat の両方が開いていた。
- 同一イベント列が terminal logger と chat notifier の両方に流れる構造だった。

# Abstractions Applied
- 具体的な bot 名、チャンネル名、ログ本文、payload は一般化した。
- 固有サービス名は公開 benchmark では chat relay / user-facing channel に抽象化した。

# Leakage Check
- raw transcript の長文引用はしていない。
- 固有の channel ID、user ID、URL は含めていない。
