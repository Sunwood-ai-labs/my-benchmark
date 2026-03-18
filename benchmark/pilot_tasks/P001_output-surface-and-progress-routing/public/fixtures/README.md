# Fixtures

この case は実ファイルの生コピーではなく、最小再現用 fixture を想定します。

- 想定 fixture: CLI ログとチャット送信が同じイベントを共有する最小 bot 構成
- 匿名化方針: 固有 repo 名、アカウント名、会話原文、token 類は含めない。
- 再現の最小条件: イベントループ、2系統の formatter、focused smoke 用ログ期待値
