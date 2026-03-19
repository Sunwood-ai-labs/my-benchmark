# Public Dataset Bundle

この directory は model-facing bundle です。

- モデルに渡すのはこの bundle の `cases_manifest.jsonl` と各 case の `public/` だけにする。
- `private/`, `shared/`, research, traceability は含めない。
- evaluator は元の `benchmark/` 側にある private artifact を使う。