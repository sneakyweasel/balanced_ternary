# Experiments

Bounded computations write versioned records under `experiments/<problem>/`.
Generated JSONL, Parquet, CSV, and report artifacts are gitignored.
Normalization theory dumps belong under `experiments/normalization/`.

## Shared infrastructure

`research.experiments` holds the reusable I/O pieces:

- manifest / schema helpers
- JSONL writer
- optional Parquet writer (`pyarrow`, extra `experiments`)

Collatz runners stay as functions. The CLI registry
(`btlab experiments list|run|inspect`) wraps them; it does not rewrite
them.

## Contract

Each registered experiment should record:

- name and problem
- parameters
- code / schema version
- input range
- output schema
- reproducibility metadata

JSONL plus a manifest is the portable baseline. Parquet is optional.

## Existing runners

Collatz runners remain under `research.collatz.experiments`. Output
paths such as `experiments/collatz/raw/...` are unchanged.
