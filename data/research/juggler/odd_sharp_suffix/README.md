# Odd fourth-power successor search

Persistent exact search for

```text
T(n) = a^4
```

with `n` odd and non-square. The integer form is

```text
a^8 <= n^3 < (a^4 + 1)^2
```

This dataset is evidence, not a theorem. An empty range means the range
was searched and no odd non-square witness was found. It does not prove
that no such `n` exists.

The Research Engine control layer is not used.

## Layout

```text
README.md
search_config.json
manifest.json
search.sqlite          # gitignored; source of truth
ranges/                # optional spill; gitignored
hits/                  # one JSON file per interval cube
summaries/
analysis/
```

## Commands

From the repository root:

```text
python tools/odd_fourth_power_search.py benchmark --a-end 10000
python tools/odd_fourth_power_search.py init --a-end 1000000 --chunk-size 100000
python tools/odd_fourth_power_search.py run --workers 16
python tools/odd_fourth_power_search.py resume --workers 16
python tools/odd_fourth_power_search.py status
python tools/odd_fourth_power_search.py summarize
```

`--data-dir` overrides this directory.

## Resume

Work is disjoint chunks `[a0, a1)`. Statuses:

```text
PENDING
RUNNING
COMPLETE
FAILED
INVALIDATED
```

A `COMPLETE` chunk is never recomputed because another chunk failed.
`resume` returns stale `RUNNING` chunks to `PENDING`. If the algorithm
or arithmetic method changes, unfinished chunks are `INVALIDATED`.

## Arithmetic

Default method is Python arbitrary-precision integers and binary-search
cube roots (`python-int`). Optional `gmpy2.iroot` is recorded as
`gmpy2-iroot`. Those methods must not be mixed on one `search_id`.

No floating-point roots are used.

## Classifications

```text
INTERVAL_EMPTY
EVEN_CUBE
ODD_SQUARE
ODD_NON_SQUARE
```

`ODD_NON_SQUARE` is a counterexample to the current computational
conjecture and is written immediately under `hits/`.

## Completed range

`1 <= a < 10^8`, algorithm `odd-fourth-v1-cbrt`, arithmetic
`python-int`. See `manifest.json` and `summaries/`. Outcome:
`ODD_FOURTH_POWER_NO_WITNESS` and
`ODD_FOURTH_POWER_STRUCTURE_DISCOVERED`. Nearest-cube and even-`m`
notes live in `analysis/`. This is not a theorem. Do not rerun the
`10^8` search to refresh those notes.
