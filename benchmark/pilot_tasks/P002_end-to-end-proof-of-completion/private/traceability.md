# Why This Case Exists
途中まで通ったテストを「完了」と扱う失敗が、実務上もっとも信頼を落とすパターンの一つだったため。

# Source Pattern Summary
- 履歴が取れているか怪しいという明示的不満。
- request 送信や応答検出だけでは完了と認めないという不満。
- 末端状態まで確認せず verified と言うことへの強い反発。

# Evidence Used
- F02: incomplete verification cluster
- Claude history verification complaints
- local incident seed: 「最後まで行っているか」「履歴や保存物が残っているか」の要求

# Prompt Frame
- 元の要求は generic な test 強化ではなく、「最後まで行っているかを証明してほしい」「何をもって完了なのか明示してほしい」という completion definition の再要求だった。
- そのため problem では success criteria の見直しと completion evidence の明示を中心にした。

# Environment Frame
- ローカル run の末尾に履歴ファイル、保存済み成果物、最終応答ログなどが残る系の agent / harness を想定している。
- 既存 check は send / response start など途中イベントで pass していた。

# Abstractions Applied
- 具体的な履歴ファイル名やツール名は一般化した。
- 末端状態は history, final response, saved artifact の複数形で許容するよう抽象化した。

# Leakage Check
- 会話内容や生成物本文の生引用はしていない。
- channel 名や workspace 固有名は除去した。
