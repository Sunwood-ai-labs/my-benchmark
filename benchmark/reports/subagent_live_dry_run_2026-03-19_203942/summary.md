# Subagent Live Dry Run Summary

## Summary

- `run_id`: `subagent-live-dry-run-2026-03-19_203942`
- `date`: `2026-03-19`
- `run_mode`: `closed-book case-pack dry-run with live subagents`
- `pinned_manifest`: `benchmark/cases_manifest.jsonl @ 2e7bf03`
- `per_task_reports`:
  - [P001](./P001.md)
  - [P002](./P002.md)
  - [P005](./P005.md)
- `score_artifact`: [scores.json](./scores.json)

## Roster

- producers:
  - `セツナ・ミカゲ / 境界を断つ路面整師` for `P001`
  - `アオイ・ユラ / 終端を刻む証跡司` for `P002`
  - `シグレ・トウヤ / 旧律を剥がす真名探査士` for `P005`
- qa verifier:
  - `ユズキ・カナメ / 判定を封じる静観司`
- devil:
  - `ノクス・ヴァレン / 反証を裁く冥府の審判`
- material:
  - `イオリ・ノア / 余白を量る意匠律官`

## Scores

| case_id | score_10 | verdict |
| --- | --- | --- |
| P001 | 6 / 10 | strong task fit, but evidence-light |
| P002 | 6 / 10 | strongest completion logic, but still unproven |
| P005 | 5 / 10 | good grounding direction, but source proof is still thin |

## Actual Run Notes

- producers were run as live subagents in this thread
- `GPT-5.3-Codex-Spark` had already hit usage limits earlier on `2026-03-19`, so producer lanes ran on `gpt-5.4-mini`
- all three candidate answers were confirmed as task-match `pass` by the qa verifier
- Devil audit pushed the final scores downward on `P002` and `P005`

## Review Lanes

- `second_pass_status`:
  - `P001`: `pass`
  - `P002`: `pass`
  - `P005`: `pass`
- `devil_disposition`: `requires adjustment`
- `material_design_status`: `not_applicable`

## Next Action

- add runnable fixtures beyond `P005`
- compare a second model stack against the same three cases
- keep recording task-level behavior and score rationale for every run
