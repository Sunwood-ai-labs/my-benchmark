# Fixtures

この case は実ファイルの生コピーではなく、最小再現用 fixture を想定します。

- 想定 fixture: request 送信、history 保存、final artifact 生成の境界が分かる e2e harness
- 匿名化方針: 固有 repo 名、アカウント名、会話原文、token 類は含めない。
- 再現の最小条件: send / first-response で通ってしまう既存 check、history か artifact を確認できる保存先、focused end-state assertion
