# Accepted Fix

- チャットに流れるメッセージが短い進捗中心になり、CLI でだけ詳細診断を追える。
- どのイベントをどの出力面に送るかの基準がコード上で明確になる。
- 既存の主処理フローは壊さない。

# Minimum Pass

- チャットのノイズが大幅に減り、CLI には進捗か詳細診断のいずれかが残っている。
- 変更が局所で、検証経路が示されている。

# Acceptable Variants

- イベント種別で分ける実装でも、formatter を分ける実装でもよい。
- テスト追加または focused smoke のどちらでも可。

# Common Failures

- チャットから必要情報まで消してしまう。
- CLI 側の可観測性も一緒に落とす。
- 出力面の責務を説明できていない。
- debug dump の混入や chrome ノイズを、surface routing ではなく message 内容の全面書き換えで誤魔化す。

# Evaluator Notes

- 人間が追いたい進捗がどちらの面に残ったかを見る。
- debug を隠しただけの変更は高得点にしない。
