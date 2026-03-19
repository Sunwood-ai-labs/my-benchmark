# Accepted Fix

- path/version の前提が実証され、その前提に沿って変更または説明が行われる。

# Minimum Pass

- ローカル証拠に基づいて path/version の誤前提を正している。
- 期待された validation が通る、または通らない理由が benchmark の制約と整合して説明されている。

# Acceptable Variants

- コード変更なしで前提修正だけでも、要求に合えば可。
- version 表記は current patch version でも current minor family でも、ローカル証拠と整合していれば可。

# Common Failures

- 一般的なデフォルトパスを前提に進める。
- 古い version 向けのまま説明する。
- validation script の期待値だけを見て、実際の truth source を確認しない。
- install dir や runtime log があるのに README の古い説明だけを信じる。
- required check を実行しない、または fail のまま完了扱いにする。

# Evaluator Notes

- 実装量より前提の正しさを重く見る。
- harmless な wording 正規化や同一ファイル内の小さな整形は、過剰変更として扱わない。
