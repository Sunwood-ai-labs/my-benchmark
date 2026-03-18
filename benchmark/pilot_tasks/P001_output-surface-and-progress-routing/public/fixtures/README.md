# Fixtures

この case は実ファイルの生コピーではなく、最小再現用 fixture を想定します。

- 想定 fixture: terminal logger と chat relay が同じ progress/debug event を共有する最小 bot / automation 構成
- 匿名化方針: 固有 repo 名、アカウント名、会話原文、token 類は含めない。
- 再現の最小条件: 長時間ジョブ相当の phase event、2 系統の formatter、CLI 出力と chat 出力を比較できる focused smoke
