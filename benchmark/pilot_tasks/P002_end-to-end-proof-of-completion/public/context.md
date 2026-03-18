# 関連ファイルと前提
- 履歴 JSONL、保存ファイル、最終応答ログ、終了マーカーなど、末端状態を示すローカル証拠が少なくとも 1 つある。
- 既存 test 名、debug script、run wrapper のどれかは存在する。
- incident の前提は「local run は最後に何かが残るはずなのに、今の check は途中で止まっている」である。
- 末端証拠は history だけでなく、deployment dir、runtime log、version gate の通過でもよい。

# 最小仕様
- first response や send 完了だけでは pass にしない。
- 履歴や成果物の有無が assertion または確認手順に入る。
- checked / blocked / substitute evidence を言い分ける。

# fixture について
- fixture は request log、history 保存先、final artifact 置き場の組を持つ最小構成でよい。
- wrapper timeout や partial success が起こりうる前提でもよい。
- task によっては runtime log や実配置先が completion proof の一部になる。

# 評価上の注意
- これは generic な e2e 強化ではなく、「最後まで行ったと言うための条件」を incident から再定義する問題である。
- 末端証拠がないのに verified と書くのは hard fail。
