# Odd-odd residual admissibility

Phase-0 ResidualStep traces on `HARD_PROBES = (9, 37, 49, 69, 77)`
and every odd-odd start `2 <= n <= 80`. JSON under `summaries/` and
`analysis/` is the source of truth.

This dataset is evidence, not a bound `L` and not a termination
theorem. Depth `2` is the search-horizon maximum in this window.

The Research Engine control layer is not used.

## Layout

```text
README.md
search_config.json
manifest.json
summaries/
analysis/
```

## Commands

From the repository root:

```text
python -m research.juggler_sequence.odd_odd_residuals init
python -m research.juggler_sequence.odd_odd_residuals run
python -m research.juggler_sequence.odd_odd_residuals resume
python -m research.juggler_sequence.odd_odd_residuals status
python -m research.juggler_sequence.odd_odd_residuals summarize
```

`--data-dir` overrides this directory.

## Resume

`resume` recomputes only if `manifest.json` is missing or
`completed` is false. The window is small enough that a full run
is cheap.
