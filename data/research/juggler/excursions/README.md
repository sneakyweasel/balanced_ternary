# Juggler first-return-below excursions

Phase-0 structure census of first returns strictly below the starting
value. SQLite `search.sqlite` is the row source of truth and is
gitignored. `summaries/` and `analysis/` hold the classification. A
search-horizon miss is not a bound L and not a termination theorem.

```text
README.md
search_config.json
manifest.json
search.sqlite          # gitignored
ranges/                # gitignored spill
summaries/
analysis/
```

## Commands

From the repository root:

```text
python -m research.juggler_sequence.excursions init
python -m research.juggler_sequence.excursions run
python -m research.juggler_sequence.excursions resume
python -m research.juggler_sequence.excursions status
python -m research.juggler_sequence.excursions summarize
```

`--data-dir` overrides this directory. `--n-end` bounds a smoke run.

The Research Engine control layer is not used. ResidualStep is not
extended.
