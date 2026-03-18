# Fixtures

この case は実ファイルの生コピーではなく、最小再現用 fixture を想定します。

- 想定 fixture: local test と sandbox chat channel 相当の確認経路を分けて持つ最小 integration harness
- 匿名化方針: 固有 repo 名、アカウント名、会話原文、token 類は含めない。
- 再現の最小条件: local pass path、sandbox chat channel か recorded relay、必須外部設定不足時の blocked reporting format
