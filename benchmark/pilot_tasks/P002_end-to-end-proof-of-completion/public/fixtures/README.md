# Fixtures

この case は実ファイルの生コピーではなく、最小再現用 fixture を想定します。

- 想定 fixture: 途中成功と末端履歴確認の差が分かる e2e harness
- 匿名化方針: 固有 repo 名、アカウント名、会話原文、token 類は含めない。
- 再現の最小条件: send event、final artifact/history store、assertion point
