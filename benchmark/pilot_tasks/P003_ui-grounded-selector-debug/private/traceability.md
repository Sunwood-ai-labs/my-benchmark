# Why This Case Exists
UI を実際に見ずに抽象推論で進めると、ユーザーがもっとも強く苛立つパターンが繰り返し出ていたため。

# Source Pattern Summary
- live UI のレイアウトや popup を認識できていないという強い不満。
- 壊れたのに別方向を触る失敗。
- 初回と再実行で状態が変わる flow を見ずに selector だけいじる失敗。

# Evidence Used
- F03: ui_not_grounded cluster
- local incident seed: new action flow の live UI state、permission popup、debug DOM artifact を見て判断すべきだったケース

# Prompt Frame
- 元の要求は「ちゃんとレイアウトを認識しろ」「今見えている UI を確認して押せ」に近く、generic な selector 修正ではなかった。
- そのため problem では popup と pane state を含む UI 状態差を観測対象として明示した。

# Environment Frame
- browser / Electron 風の UI automation で、live browser、DOM dump、screenshot、raw debug artifact のいずれかが取れる前提だった。
- 自動化対象の flow は初回と再実行で見える UI が少し変わりうる。

# Abstractions Applied
- 固有 UI 名称、selector 文字列、service 名は一般化した。
- 外部面は browser task / live UI / popup という class レベルの名詞に留めた。

# Leakage Check
- スクリーンショットや DOM の raw 断片は埋め込んでいない。
