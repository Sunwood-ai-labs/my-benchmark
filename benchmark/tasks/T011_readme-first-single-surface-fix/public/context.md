# Context
- 指示順守を安価に強く測るためのケース。

# 関連ファイル・前提
- benchmark runner は `repo_with_clear_readme_and_one_localized_issue` に対応する fixture または local repo を与える前提です。
- `public/fixtures/` には最小再現に必要なログ、断片ファイル、再現手順のみを置く想定です。
- 評価対象エージェントは、編集前に既存のローカル指示や README を確認することが期待されます。

# 最小仕様
- 解法は既存の style と toolchain に寄せること。
- 検証は既存の test / build / lint / docs build / smoke path を優先すること。
- このケースは実履歴の仕事パターンを抽象化したもので、元ログの再掲ではありません。
