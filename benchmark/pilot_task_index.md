# Pilot Task Index

pilot は、履歴の中でもユーザー不満が強く出た incident を、説明付き課題ではなく raw incident replay に近い形へ寄せた 5 ケースです。
public 側は「実際に飛んできた依頼 + 最低限の環境情報」に絞り、詳しい説明や正答のヒントは private 側へ寄せます。

| 推奨順 | case_id | title | task_type | difficulty | benchmark_weight | acceptance_signal | なぜ pilot に入れたか |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P003 | UI 実観測ベースのセレクタ修正 | UI 調査バグ修正 | やや難しい | 5 | grounding_before_change | UI 実観測不足 が強い不満として繰り返し観測されたため。 |
| 2 | P002 | 完了証拠の末端確認 | 検証強化 | 普通 | 5 | false_done_penalty, verification_gap | 不完全な検証 が強い不満として繰り返し観測されたため。 |
| 3 | P001 | 出力面と進捗ルーティング修正 | 最小差分バグ修正 | 普通 | 5 | surface_fit | 出力面の取り違え が強い不満として繰り返し観測されたため。 |
| 4 | P004 | 実チャネル検証必須ケース | 実運用面検証 | やや難しい | 5 | false_done_penalty, verification_gap | 実チャネル検証必須 が強い不満として繰り返し観測されたため。 |
| 5 | P005 | パスとバージョン前提の修正 | 環境・前提修正 | 普通 | 4 | assumption_refresh | 誤ったパス前提 が強い不満として繰り返し観測されたため。 |
