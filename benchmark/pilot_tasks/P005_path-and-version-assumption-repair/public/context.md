# 関連ファイルと前提
- ローカルに path / version truth source がある。
- truth source は install dir、runtime log、config/path 実装、version metadata などを含みうる。
- validation 用 script や check は有用だが、それ自体は path/version の truth source の代替ではない。

# 最小仕様
- 前提確認が実装前に行われる。
- 古い target を前提にしない。
- install dir、runtime log、version metadata のどれを根拠にしたかが分かる。

# fixture について
- fixture は install dir 相当の設定、version file、runtime log excerpt の組でよい。

# 評価上の注意
- よくあるデフォルトパスを言い当てるゲームではない。
- exact patch version と version family のどちらで書くかは、ローカル証拠と整合していればよい。
