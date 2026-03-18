# Fixtures

この case は実ファイルの生コピーではなく、最小再現用 fixture を想定します。

- 想定 fixture: send step と history update step が分かれた workflow
- 匿名化方針: 固有 repo 名、アカウント名、会話原文、token 類は含めない。
- 再現の最小条件: history store、send log、assertion hook
