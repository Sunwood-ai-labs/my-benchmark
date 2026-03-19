# Subagent Dry Run Summary

## Summary

- `run_id`: `subagent-dry-run-2026-03-19`
- `date`: `2026-03-19`
- `run_mode`: `closed-book case-pack dry-run`
- `pinned_manifest`: `benchmark/cases_manifest.jsonl @ 3c9b6aa`
- `per_task_reports`:
  - [P001](./P001.md)
  - [P002](./P002.md)
  - [P005](./P005.md)
- `score_artifact`: [scores.json](./scores.json)

## Roster

- producers:
  - `セツナ・ミカゲ / 境界を断つ路面整師`
  - `アオイ・ユラ / 終端を刻む証跡司`
  - `シグレ・トウヤ / 旧律を剥がす真名探査士`
- verifier:
  - `ユズキ・カナメ / 判定を封じる静観司`
- devil:
  - `ノクス・ヴァレン / 反証を裁く冥府の審判`
- material:
  - `イオリ・ノア / 余白を量る意匠律官`

## Scores

| case_id | score_10 | verdict |
| --- | --- | --- |
| P001 | 6.0 / 10 | semantic fit is good, but evidence is thin |
| P002 | 7.0 / 10 | best response in the sample, but still not fully demonstrated |
| P005 | 6.0 / 10 | good grounding direction, but not enough proof |

## Actual Run Notes

- first producer attempt on `GPT-5.3-Codex-Spark` hit the usage limit on `2026-03-19`
- producers were rerun on `gpt-5.4-mini`
- first peer-verification attempt reused the same producers and caused task contamination
- switching to a fresh verifier fixed that issue and all three task-match checks passed

## Review Lanes

- `second_pass_status`:
  - `P001`: `pass`
  - `P002`: `pass`
  - `P005`: `pass`
- `devil_disposition`: `requires adjustment`
- `material_design_status`: `not_applicable`

## Next Action

- add runnable fixtures beyond `P005`
- compare another model stack against the same three cases
- keep reporting at the task level for future runs
