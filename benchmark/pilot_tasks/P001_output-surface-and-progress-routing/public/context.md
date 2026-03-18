# 関連ファイルと前提
- repo には event emitter、terminal logger、chat relay formatter のいずれかがある。
- incident の前提は「長時間ジョブを CLI で監視しつつ、ユーザー向けチャットにも進捗を送る」構成である。
- verbose debug 自体は必要だが、出す面が違う。
- raw debug artifact や HTML dump を別出力として残せる場合がある。

# 最小仕様
- terminal には phase 進捗と原因調査に必要な詳細が残る。
- チャットには人間が読める短報だけが残る。
- 同じ event を二重送信したり、両面とも無言にしたりしない。

# fixture について
- fixture は `phase-start`, `retry`, `api-debug`, `final-summary` のようなイベント列を持つ最小 bot / automation でよい。
- chat relay は実サービス接続なしで再現してよいが、ユーザー面と terminal 面は分けて観測できる必要がある。
- failure signature が「応答本文ではなく UI chrome / debug dump が見えてしまう」系でもよい。

# 評価上の注意
- generic な UX 改善ではなく、incident の「どの面に何を出すべきだったか」を戻す問題である。
- チャット側から debug を消しても、CLI 側で進捗が追えないなら高得点にしない。
