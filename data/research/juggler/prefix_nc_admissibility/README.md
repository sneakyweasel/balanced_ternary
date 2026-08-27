# Prefix-NC arithmetic admissibility

Backward floor-cell pullback of mixed prefix-noncontracting Juggler
words. JSON under `summaries/`, `analysis/`, and `words/` is the
source of truth.

An empty fiber over a bounded image interval is not a proof that
the word is unrealizable. A realized word of length 10 is not an
infinite family. This is not a termination theorem.

The Research Engine control layer is not used. `ResidualStep` is
not extended.

## Layout

```text
README.md
config.json
manifest.json
words/
summaries/
analysis/
```

## Commands

From the repository root:

```text
python -m research.juggler_sequence.prefix_nc_admissibility init
python -m research.juggler_sequence.prefix_nc_admissibility run
python -m research.juggler_sequence.prefix_nc_admissibility resume
python -m research.juggler_sequence.prefix_nc_admissibility status
python -m research.juggler_sequence.prefix_nc_admissibility summarize
```

`--data-dir` overrides this directory.
