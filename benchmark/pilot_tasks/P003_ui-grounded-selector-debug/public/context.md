# 関連ファイルと前提
- DOM dump、screenshot、raw debug artifact、または live browser 観測のいずれかが取得できる。
- selector 候補が複数存在し、pane 状態や popup の有無で正解が変わる可能性がある。
- incident の前提は「live UI を見れば分かる状態差を、推測で飛ばしてしまった」である。

# 最小仕様
- UI 実観測を根拠として使う。
- permission popup や state drift の有無を確認する。
- レイアウトは不必要に変えない。
- セレクタ修正後の smoke がある。

# fixture について
- fixture は DOM snapshot と failing selector だけでもよいが、可能なら popup あり / なしの状態差も持つ。

# 評価上の注意
- 「見た目を直す」タスクではなく「観測して原因線を直す」タスク。
- UI 実観測の証拠なしは大きく減点。
