# Task Index

この index は human-readable 一覧です。dataset としての正は [cases_manifest.jsonl](./cases_manifest.jsonl) と [splits](./splits) にあります。
pilot 5 件は high-friction split、main corpus 25 件は broader coding-work split です。
各 case は `public` と `private` を分けた SWE-bench-style case pack として扱います。

## Pilot
| case_id | title | difficulty | benchmark_weight | primary_metrics | acceptance_signals | 一言説明 |
| --- | --- | --- | --- | --- | --- | --- |
| P001 | 出力面と進捗ルーティング修正 | 普通 | 5 | instruction_following, bugfix_convergence | surface_fit | 詳細デバッグは CLI に残しつつ、ユーザー向けチャンネルには短い進捗だけを出すように最小差分で直す。 |
| P002 | 完了証拠の末端確認 | 普通 | 5 | test_retention, instruction_following | false_done_penalty, verification_gap | 成功判定を「送れた」段階で止めず、履歴や成果物まで確認してから完了扱いにする。 |
| P003 | UI 実観測ベースのセレクタ修正 | やや難しい | 5 | bugfix_convergence, ambiguity_handling | grounding_before_change | 実際の DOM / UI 状態を観測して、無関係なレイアウトを壊さずにセレクタまわりの不具合を直す。 |
| P004 | 実チャネル検証必須ケース | やや難しい | 5 | instruction_following, test_retention | false_done_penalty, verification_gap | 単体やローカル smoke だけで済ませず、実チャネルに相当する面で確認するか、できないなら blocked を明確にする。 |
| P005 | パスとバージョン前提の修正 | 普通 | 4 | repo_understanding_speed, instruction_following | assumption_refresh | デフォルト前提で進めず、実際のパスと現行バージョンを確認してから修正方針を決める。 |

## Main
| case_id | title | task_type | difficulty | benchmark_weight | primary_metrics | acceptance_signals | 一言説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | 所有ファイル限定の監視ループ修正 | 最小差分バグ修正 | 普通 | 1.2 | instruction_following, overchange_penalty, bugfix_convergence |  | 1ファイル ownership を守りながら監視ループの退行を直す。 |
| T002 | CLI 出力崩れ修正 | 最小差分バグ修正 | 普通 | 1 | bugfix_convergence, overchange_penalty, tool_use_efficiency |  | 文字化けや整形崩れを含む CLI 出力の退行を直す。 |
| T003 | 曖昧要求の UI 強化 | 曖昧要求からの新規実装 | 普通 | 1.1 | ambiguity_handling, first_pass_acceptance, instruction_following |  | 仕様が足りない状態で、まとまりのある UI 改善を実装する。 |
| T004 | CLI オプション追加と docs 同期 | 曖昧要求からの新規実装 | 普通 | 1 | ambiguity_handling, test_retention, instruction_following |  | 小さな CLI 機能を追加し、README や guide を必要最小限同期する。 |
| T005 | テスト維持リファクタ | 既存挙動維持リファクタ | 難しい | 1.1 | test_retention, overchange_penalty, first_pass_acceptance |  | 混み合った module を、挙動を変えずに少し整理する。 |
| T006 | CI 版数・成果物不整合修正 | 環境・CI修復 | 難しい | 1.1 | bugfix_convergence, instruction_following, test_retention |  | workflow は動くのに version や artifact がずれている状態を直す。 |
| T007 | リリース文書同期 | ドキュメント・リリース整備 | 普通 | 0.9 | first_pass_acceptance, explanation_usefulness, instruction_following |  | ローカル差分に基づいて release note や関連記事を正しく揃える。 |
| T008 | worktree・branch 文脈理解 | 調査・設計相談 | 普通 | 0.8 | repo_understanding_speed, instruction_following, explanation_usefulness |  | main clone ではない作業場所でも、安全な root と branch を素早く把握する。 |
| T009 | uv・pytest 失敗収束 | 環境・CI修復 | 難しい | 1 | test_retention, bugfix_convergence, instruction_following |  | uv 管理の Python repo で、狭い pytest failure を素早く収束させる。 |
| T010 | 図表 lint 修正 | ドキュメント・リリース整備 | 普通 | 0.9 | test_retention, overchange_penalty, bugfix_convergence |  | diagram asset の overlap / overflow 系 lint を局所修正で通す。 |
| T011 | README 先読みの局所修正 | 最小差分バグ修正 | 易しい | 0.8 | instruction_following, overchange_penalty, repo_understanding_speed |  | README に書いてある前提を読めばすぐ直せる小さな不具合を直す。 |
| T012 | automation 定義更新 | 調査・設計相談 | 普通 | 0.8 | recovery_quality, instruction_following, explanation_usefulness |  | 既存 automation を読み、重複作成せずに prompt や schedule を直す。 |
| T013 | shell 証拠ベース原因調査 | 調査・設計相談 | 普通 | 0.9 | explanation_usefulness, repo_understanding_speed, ambiguity_handling |  | 短い shell log と repo 状態から有力な原因を絞り、次アクションを出す。 |
| T014 | cross-shell path 修正 | 最小差分バグ修正 | 普通 | 0.9 | bugfix_convergence, instruction_following, test_retention |  | Windows と bash / WSL のどちらかでだけ壊れる path / quoting 問題を直す。 |
| T015 | 二言語 docs 整合 | ドキュメント・リリース整備 | 普通 | 0.8 | first_pass_acceptance, overchange_penalty, explanation_usefulness |  | 片方だけ古くなった docs surface を必要最小限で同期する。 |
| T016 | hardware setup 調査 | 調査・設計相談 | 難しい | 0.7 | ambiguity_handling, explanation_usefulness, instruction_following |  | device や board のセットアップ詰まりを、ローカル証拠だけで切り分ける。 |
| T017 | browser 検証計画 | 調査・設計相談 | 普通 | 0.7 | explanation_usefulness, instruction_following, tool_use_efficiency |  | UI 変更を本当に動かしたかを確認するための短いブラウザ検証計画を立てる。 |
| T018 | owned scope の overchange 罠 | 既存挙動維持リファクタ | 普通 | 0.9 | overchange_penalty, instruction_following, first_pass_acceptance |  | 担当範囲だけ改善し、ついで修正の誘惑に負けないかを見る。 |
| T019 | 壊れた設定の復旧 | 失敗後の復旧・再実行 | 難しい | 0.9 | recovery_quality, instruction_following, overchange_penalty |  | current config と backup を見比べ、secret を漏らさずに正しい状態へ戻す。 |
| T020 | mixed repo の高速オリエンテーション | 調査・設計相談 | 易しい | 0.8 | repo_understanding_speed, tool_use_efficiency, explanation_usefulness |  | docs、script、app code が混在する repo で、最初に当たるべき場所を素早く見抜く。 |
| T021 | CLI とチャットのログ面分離 | 最小差分バグ修正 | 普通 | 4 | instruction_following, overchange_penalty | surface_fit | 詳細ログとユーザー通知を適切な面に分け、同一イベントの二重送出も防ぐ。 |
| T022 | UI ノイズを除いた応答抽出 | 最小差分バグ修正 | やや難しい | 4 | bugfix_convergence, test_retention | surface_fit | 応答抽出結果から model list や mode list などの UI chrome を除き、本当に欲しい本文だけを返す。 |
| T023 | 応答後履歴の証拠確認 | 検証強化 | 普通 | 4 | test_retention, bugfix_convergence | false_done_penalty, verification_gap | 応答送信後に履歴 store まで更新されたことを検証に含める。 |
| T024 | DOM 実観測での新規チャット回帰修正 | UI 調査バグ修正 | やや難しい | 4 | bugfix_convergence, test_retention | grounding_before_change | 新規チャット開始の回帰を、実際の DOM 状態を見て最小差分で戻す。 |
| T025 | 現行版互換性の確認修正 | 環境・前提修正 | 普通 | 4 | instruction_following, repo_understanding_speed | assumption_refresh, verification_gap | 現行版で使えるかをローカル証拠で確認し、古い target のまま説明しない。 |
