# Agent Interaction Analysis

Generated at: 2026-03-19T16:33:16.725790+09:00

## Scope

- Workspace: `D:\Prj\my-bench`
- Sources inspected: local `C:\Users\Aslan\.claude`, local `C:\Users\Aslan\.codex`, and snapshot roots found under `D:\Prj\my-bench\data`
- Primary interaction dataset: Claude project transcripts plus Codex session transcripts
- Auxiliary prompt-only dataset: Claude `history.jsonl` only when no project transcripts were present for that root

## Dataset Overview

- Total normalized messages: **64,497**
- Full interaction messages: **64,497**
- Prompt-only fallback messages: **0**
- User messages: **6,135**
- Assistant messages: **58,362**
- Tool invocations captured: **62,180**
- Distinct sessions / threads: **1,167**

### Source Inventory

| agent_family   | origin                               | root_path                                           |   project_jsonl_count |   subagent_jsonl_count |   team_config_count |   task_json_count |   todo_json_count | history_exists   | fallback_history_used   |   session_jsonl_count | session_index_exists   | state_db_exists   |
|:---------------|:-------------------------------------|:----------------------------------------------------|----------------------:|-----------------------:|--------------------:|------------------:|------------------:|:-----------------|:------------------------|----------------------:|:-----------------------|:------------------|
| claude         | local_home                           | C:\Users\Aslan\.claude                              |                    85 |                    209 |                   2 |                 0 |                 0 | True             | False                   |                       |                        |                   |
| claude         | data_snapshot:kali-aslan-20260319    | D:\Prj\my-bench\data\kali-aslan-20260319\.claude    |                     7 |                    244 |                   2 |                10 |               366 | True             | False                   |                       |                        |                   |
| claude         | data_snapshot:prox-200-maki-20260319 | D:\Prj\my-bench\data\prox-200-maki-20260319\.claude |                   423 |                    601 |                  34 |                79 |               455 | True             | False                   |                       |                        |                   |
| codex          | local_home                           | C:\Users\Aslan\.codex                               |                       |                        |                     |                   |                   |                  |                         |                   799 | True                   | True              |

### Message Volume by Agent Family / Origin

| agent_family   | origin                               | role      |   messages |
|:---------------|:-------------------------------------|:----------|-----------:|
| claude         | data_snapshot:prox-200-maki-20260319 | assistant |      32810 |
| codex          | local_home                           | assistant |      17096 |
| claude         | local_home                           | assistant |       6979 |
| claude         | data_snapshot:prox-200-maki-20260319 | user      |       3140 |
| codex          | local_home                           | user      |       2464 |
| claude         | data_snapshot:kali-aslan-20260319    | assistant |       1477 |
| claude         | local_home                           | user      |        486 |
| claude         | data_snapshot:kali-aslan-20260319    | user      |         45 |

## User Communication Patterns

### Top Projects / Working Directories

| agent_family   | origin                               | project_or_title               |   user_messages |   avg_chars |
|:---------------|:-------------------------------------|:-------------------------------|----------------:|------------:|
| codex          | local_home                           | onizuka-game-agi-co            |             517 |       285.4 |
| claude         | data_snapshot:prox-200-maki-20260319 | cbot                           |             327 |       697.1 |
| claude         | data_snapshot:prox-200-maki-20260319 | mao-army-dashboard             |             314 |      1016.4 |
| codex          | local_home                           | harina-v3                      |             299 |       150.8 |
| codex          | local_home                           | video-background-remover       |             287 |       130.3 |
| claude         | data_snapshot:prox-200-maki-20260319 | sat-cafe                       |             274 |       504.6 |
| claude         | data_snapshot:prox-200-maki-20260319 | cc-Agent-teams-sandbox         |             257 |       723.5 |
| claude         | data_snapshot:prox-200-maki-20260319 | Cinderella                     |             251 |      4012.5 |
| claude         | data_snapshot:prox-200-maki-20260319 | nannj                          |             209 |       652.4 |
| claude         | local_home                           | desktop-pet-mitarashi          |             150 |      1632.6 |
| codex          | local_home                           | MysticLibrary                  |             136 |       689.2 |
| claude         | data_snapshot:prox-200-maki-20260319 | last-train                     |             120 |       543   |
| codex          | local_home                           | my-bench                       |             117 |       626   |
| claude         | data_snapshot:prox-200-maki-20260319 | claude-glm-actions-lab-sandbox |             106 |       619.5 |
| claude         | data_snapshot:prox-200-maki-20260319 | ai-agent-desktop-ubuntu        |              94 |       942.1 |

### Active Hours (JST)

|   hour_jst |   user_messages |   share_pct |
|-----------:|----------------:|------------:|
|          0 |             389 |         6.3 |
|          1 |             460 |         7.5 |
|          2 |             416 |         6.8 |
|          3 |             289 |         4.7 |
|          4 |             196 |         3.2 |
|          5 |             117 |         1.9 |
|          6 |              60 |         1   |
|          7 |             105 |         1.7 |
|          8 |              67 |         1.1 |
|          9 |              88 |         1.4 |
|         10 |              75 |         1.2 |
|         11 |              40 |         0.7 |
|         12 |              55 |         0.9 |
|         13 |             109 |         1.8 |
|         14 |             243 |         4   |
|         15 |             158 |         2.6 |
|         16 |             251 |         4.1 |
|         17 |              96 |         1.6 |
|         18 |             108 |         1.8 |
|         19 |             321 |         5.2 |
|         20 |             278 |         4.5 |
|         21 |             573 |         9.3 |
|         22 |             687 |        11.2 |
|         23 |             954 |        15.6 |

### Language Mix

| language   |   user_messages |   share_pct |
|:-----------|----------------:|------------:|
| mixed      |            3721 |        60.7 |
| ja         |            1236 |        20.1 |
| en         |            1174 |        19.1 |
| other      |               4 |         0.1 |

### Frequent User Terms

| term     |   count |
|:---------|--------:|
| ai       |    3021 |
| 作成       |    2664 |
| remotion |    1840 |
| issue    |    1815 |
| claude   |    1708 |
| run      |    1473 |
| ファイル     |    1461 |
| only     |    1455 |
| ui       |    1446 |
| code     |    1417 |
| do       |    1402 |
| use      |    1390 |
| 完了       |    1369 |
| size     |    1340 |
| lines    |    1336 |
| pr       |    1281 |
| files    |    1271 |
| of       |    1269 |
| codex    |    1265 |
| are      |    1250 |
| test     |    1241 |
| チーム      |    1240 |
| if       |    1216 |
| コミット     |    1191 |
| ux       |    1186 |
| discord  |    1186 |
| タスク      |    1180 |
| qa       |    1147 |
| by       |    1107 |
| github   |    1095 |

## Topic / Genre Analysis

### Top User Request Categories

| category                 |   user_messages |   avg_chars |   share_pct |
|:-------------------------|----------------:|------------:|------------:|
| other                    |            2503 |       146.9 |        40.8 |
| implementation           |            1140 |      3012.2 |        18.6 |
| automation_orchestration |             788 |       940   |        12.8 |
| design_ui                |             406 |      1725.5 |         6.6 |
| review_qa                |             384 |       588.6 |         6.3 |
| analysis_research        |             321 |       899.8 |         5.2 |
| debug_fix                |             226 |       737.1 |         3.7 |
| docs_writing             |             204 |       304   |         3.3 |
| setup_config             |             138 |       633.5 |         2.2 |
| data_ml                  |              25 |      2481   |         0.4 |

### Session Size Snapshot

| agent_family   | origin                               | session_id                           | first_timestamp                  | last_timestamp                   |   total_messages |   user_messages |   assistant_messages |   avg_chars | project_name             | thread_title                        |   duration_minutes |
|:---------------|:-------------------------------------|:-------------------------------------|:---------------------------------|:---------------------------------|-----------------:|----------------:|---------------------:|------------:|:-------------------------|:------------------------------------|-------------------:|
| claude         | data_snapshot:prox-200-maki-20260319 | 8d30d253-924d-416f-89b7-f23ff458993a | 2026-02-23 04:38:26.274000+09:00 | 2026-02-23 15:37:29.862000+09:00 |             1522 |              32 |                 1490 |        87.8 | MysticLibrary            | nan                                 |              659.1 |
| claude         | local_home                           | 3baabcb3-8def-44ff-9084-3f2c823f4c0f | 2026-03-19 01:39:43.020000+09:00 | 2026-03-19 03:39:08.953000+09:00 |             1205 |              80 |                 1125 |       109.7 | workspace                | nan                                 |              119.4 |
| claude         | data_snapshot:kali-aslan-20260319    | 18c7fa20-5ac3-4a88-9f59-d0e9ecb05acd | 2026-02-27 02:39:28.704000+09:00 | 2026-02-27 18:56:46.140000+09:00 |             1195 |              20 |                 1175 |        42.8 | Spresense_demo           | nan                                 |              977.3 |
| claude         | data_snapshot:prox-200-maki-20260319 | 6ebe63a5-0906-4b7f-af99-15292426276d | 2026-02-11 00:37:32.713000+09:00 | 2026-02-11 02:39:48.230000+09:00 |             1000 |              24 |                  976 |        63.6 | clawra                   | nan                                 |              122.3 |
| claude         | local_home                           | a8f6caef-97c9-4df8-8325-296e882d658b | 2026-03-13 00:25:32.355000+09:00 | 2026-03-13 03:57:45.976000+09:00 |              928 |              34 |                  894 |       205.4 | video-background-remover | nan                                 |              212.2 |
| claude         | data_snapshot:prox-200-maki-20260319 | ef564f0d-1fb2-40cf-8250-d1380b072585 | 2026-02-03 21:40:52.140000+09:00 | 2026-02-04 02:41:07.354000+09:00 |              873 |              47 |                  826 |       109   | cbot                     | nan                                 |              300.3 |
| claude         | local_home                           | ea7b400b-2818-41e4-bd6e-072a0179735c | 2026-03-13 22:08:26.257000+09:00 | 2026-03-14 01:03:01.013000+09:00 |              643 |              44 |                  599 |        46.7 | desktop-pet-mitarashi    | nan                                 |              174.6 |
| claude         | local_home                           | c43031ff-afb9-4db4-8474-3ba4e6f9738b | 2026-03-13 18:58:39.540000+09:00 | 2026-03-13 19:53:34.881000+09:00 |              584 |              27 |                  557 |       274.3 | desktop-pet-mitarashi    | nan                                 |               54.9 |
| claude         | data_snapshot:prox-200-maki-20260319 | 2dc3bcbc-0125-481c-a561-91ae5ed60fd1 | 2026-02-06 20:51:17.959000+09:00 | 2026-02-06 22:37:26.950000+09:00 |              553 |              39 |                  514 |       172.8 | cc-Agent-teams-sandbox   | nan                                 |              106.1 |
| claude         | local_home                           | cbdb7b25-cdad-4d03-88bc-606820e4356c | 2026-03-19 02:37:04.580000+09:00 | 2026-03-19 03:38:55.172000+09:00 |              537 |              31 |                  506 |       161   | MysticLibrary            | nan                                 |               61.8 |
| codex          | local_home                           | 019cec48-2f9e-7d83-936a-b4776d83c4ce | 2026-03-14 21:21:02.642000+09:00 | 2026-03-16 02:06:32.844000+09:00 |              487 |              56 |                  431 |       151.8 | video-background-remover | 追加 Web/GIF 出力タブと設定                  |             1725.5 |
| codex          | local_home                           | 019cf4e1-7ad6-74f1-8ed7-165b417ae104 | 2026-03-16 13:24:02.165000+09:00 | 2026-03-18 23:08:22.986000+09:00 |              479 |              48 |                  431 |       148   | harina-v3                | 再トライと移動止め確認」} ??? need remove quote |             3464.3 |
| claude         | data_snapshot:prox-200-maki-20260319 | 29720b53-e46c-4fc1-a391-320c6edeec5e | 2026-01-29 12:28:28.770000+09:00 | 2026-01-29 20:31:19.848000+09:00 |              475 |              24 |                  451 |       241.8 | Cinderella               | nan                                 |              482.9 |
| claude         | data_snapshot:prox-200-maki-20260319 | 43cc4e75-baf8-4302-bd15-4452ca3c9401 | 2026-02-08 02:16:17.422000+09:00 | 2026-02-08 03:04:08.767000+09:00 |              456 |               3 |                  453 |        52.4 | sample07                 | nan                                 |               47.9 |
| claude         | data_snapshot:prox-200-maki-20260319 | 1b066dd3-1eb5-46f0-8687-635bf2319563 | 2026-02-12 21:44:31.886000+09:00 | 2026-02-12 23:03:29.030000+09:00 |              417 |              22 |                  395 |        64.8 | MysticLibrary            | nan                                 |               79   |

## Agent / Tool Interaction

### Most Used Tools

| agent_family   | tool_name     |   invocations |
|:---------------|:--------------|--------------:|
| codex          | shell_command |         34806 |
| claude         | Bash          |          7227 |
| codex          | apply_patch   |          4018 |
| claude         | Read          |          3216 |
| claude         | Edit          |          1819 |
| codex          | js_repl       |          1721 |
| claude         | SendMessage   |          1691 |
| claude         | Write         |          1372 |
| claude         | TaskUpdate    |           781 |
| claude         | Glob          |           616 |
| codex          | update_plan   |           521 |
| codex          | spawn_agent   |           427 |
| claude         | TeamDelete    |           360 |
| claude         | TaskCreate    |           348 |
| codex          | view_image    |           318 |
| claude         | TaskList      |           301 |
| codex          | close_agent   |           301 |
| claude         | Task          |           295 |
| codex          | wait          |           292 |
| codex          | wait_agent    |           274 |

## Notes And Caveats

- Claude `history.jsonl` is treated as prompt-only fallback because it can overlap with richer `projects/**/*.jsonl` transcripts.
- Codex message extraction intentionally ignores developer/system scaffolding and `reasoning` items, focusing on user-visible user/assistant messages plus tool calls.
- Imported snapshot roots may overlap with local roots; normalization deduplicates at the message key level where stable identifiers exist.
