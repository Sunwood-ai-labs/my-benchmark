# Benchmark Case Candidates

以下は、改訂後に優先度を上げた frustration-driven case 候補です。
既存の baseline case は main corpus に残しつつ、まずこの 10 ケースから運用開始することを推奨します。

| case_id | タイトル | タスク種別 | 測る能力 | benchmark に入れる理由 | 元ネタの履歴パターン | 期待アウトカム | fail condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P001 | 出力面と進捗ルーティング修正 | 最小差分バグ修正 | instruction_following, bugfix_convergence | どこに何を出すかを外すと不満が強い | F01 | chat は短い進捗、CLI は詳細診断になる | raw debug が chat に残る |
| P002 | 完了証拠の末端確認 | 検証強化 | test_retention, instruction_following | 途中成功の完了扱いを防ぐ | F02 | 履歴や成果物まで確認する | 末端証拠なしで verified と言う |
| P003 | UI 実観測ベースのセレクタ修正 | UI 調査バグ修正 | bugfix_convergence, ambiguity_handling | UI を見ずに推測修正すると壊す | F03 | DOM / UI 実観測に基づく局所修正 | layout を勝手に触る |
| P004 | 実チャネル検証必須ケース | 実運用面検証 | instruction_following, test_retention | 単体 pass と実面確認の差が大きい | F02 | real surface か blocked を正直に示す | 未確認なのに実面確認済みと主張 |
| P005 | パスとバージョン前提の修正 | 環境・前提修正 | repo_understanding_speed, instruction_following | path/version を外すと全体がずれる | F04 | truth source に基づき前提を正す | 未確認の path/version を断定 |
| T021 | CLI とチャットのログ面分離 | 最小差分バグ修正 | instruction_following, overchange_penalty | F01 を narrower に測る | F01 | ノイズが減り責務が分かれる | 重要進捗まで消す |
| T022 | UI ノイズを除いた応答抽出 | 最小差分バグ修正 | bugfix_convergence, test_retention | 件数少でも severity 高 | F05 | 本文中心の clean extraction | UI chrome が主体で残る |
| T023 | 応答後履歴の証拠確認 | 検証強化 | test_retention, bugfix_convergence | send success だけで終えない | F02 | history update まで確認する | history 未確認で完了主張 |
| T024 | DOM 実観測での新規チャット回帰修正 | UI 調査バグ修正 | bugfix_convergence, test_retention | new chat 系の高摩擦回帰を測る | F03 | 実観測で selector を戻す | 推測だけで fallback を増やす |
| T025 | 現行版互換性の確認修正 | 環境・前提修正 | instruction_following, repo_understanding_speed | 最新版前提の確認を測る | F04 | 現行版ベースで説明または修正する | 古い target のまま説明 |

## baseline corpus について
既存 T001-T020 は以下の役割で残している。
- 広い language/toolchain coverage を保つ。
- frustration-driven case で見えない一般的な refactor / docs / CI / orientation 能力を補完する。
- pilot で落ちた failure の原因が局所なのか基礎能力なのかを見分ける。
