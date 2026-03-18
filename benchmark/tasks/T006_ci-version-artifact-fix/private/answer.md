# Expected Outcome
コードではなく実行経路や設定の問題を見極め、既存ツールチェーンで復旧できるかを見る。
- mismatch の原因が塞がれ、次回以降もズレにくくなる。

# Strong Answer Characteristics
- 正しい実行経路や設定ファイルを特定している。
- repo が採用しているツールを素直に使っている。
- 再発防止に必要な最小限の補強ができている。

# Acceptable Variants
- 設定修正、起動経路修正、workflow 修正のいずれでも、原因に合っていれば可。

# Common Failure Patterns
- 間違ったランタイムやパッケージマネージャを使う。
- 本質原因に触れず、その場しのぎで通す。
- 再現性のない直し方をする。

# Minimal Pass Line
- 壊れていた実行経路が復旧し、repo 標準の方法で確認できること。

# Notes For Evaluator
- 依存関係の大掃除で押し切っていないかを確認する。
