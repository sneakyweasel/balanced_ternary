# Juggler word atlas

Persistent exact census of finite Juggler `O/E` words. This dataset is
evidence under a search bound, not a theorem.

A missing word is `NOT_FOUND_WITHIN_BOUND`. That is not global
non-realizability. `PE_CERTIFIED` rows use the repository
`PersistentExpandingResidual` predicate on the host. The GPU does not
classify PE in Milestone 1.

The Research Engine control layer is not used. The closed word-language
branch (`JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`) is not reopened.

## Layout

```text
README.md
word_atlas.sqlite              # gitignored; metadata + registry
experiments/<experiment_id>/
  manifest.json
  observations/word_length=k/census.parquet
  census.tsv                   # optional native dump
```

## Commands

From the repository root:

```text
juggler-atlas build --k-max 12 --n-max 1000000
juggler-atlas validate
juggler-atlas factors --language REALIZABLE --r 4
juggler-atlas continuations --language REALIZABLE
juggler-atlas benchmark --k-max 8 --n-max 10000
```

`--data-dir` overrides this directory.

## Resume

Never overwrite an experiment. A new run creates a new
`experiment_id`. Interrupted runs are discarded; rerun `build`.

## Claim language

Use `COMPUTATIONALLY OBSERVED` and `NOT OBSERVED WITHIN SEARCH BOUND`.
Never write “forbidden”.
