# Goal
長時間ジョブ中の CLI とチャット relay の役割を分け直し、CLI には進捗と診断、チャットには短い進捗だけが出る状態に最小差分で戻す。

# Background
実際に観測された incident では、1 つのイベント列から terminal logger と chat notifier を組み立てていたため、ユーザー向けチャットに低レベル payload が流れ、逆に CLI では進捗が追いにくくなっていた。ユーザーが求めていたのは「CLI を見れば進捗が追え、チャットには短報だけが来る」状態である。

# Input Context
- terminal 側と chat relay 側が同じ progress event と debug event を共有している。
- 既存の check は送信の有無や件数は見るが、どの面に何が出るかまでは保証していない。
- incident 当時の要求は、長い処理中に CLI を監視しつつ、チャットには人間向けの短報だけを流すことだった。

# User Prompt
既存の出力経路を読み、CLI とチャット relay の役割を分け直してください。CLI には進捗と詳細診断を残し、チャットには 1 から 2 行の短い進捗だけを出してください。どのイベントをどちらに残したか分かる確認も付けてください。

# Constraints
- bot / automation の主処理フローや message schema を全面的に設計し直さないこと。
- symptom 隠しのために単純にログを消すだけで終わらないこと。
- token、内部識別子、raw payload をチャット向け出力へ混ぜないこと。

# Deliverables
- terminal logger と chat relay の責務を分けた最小差分修正
- CLI とチャットの出力差が分かる focused check または snapshot
- incident の何がズレていたかの短い説明
