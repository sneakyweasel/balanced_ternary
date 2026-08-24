# Ostrowski R1 baseline freeze

Infrastructure snapshot before extracting `research_engine`.
Mathematical decision is unchanged: `PARK |L_0|`.
No theorem-ledger rows were added or retagged.

```text
git_sha: 0952da60e47286fd468336b541af57c0a509d77e
git_branch: cursor/word-wn-nk3-fragment-080b
git_status: clean
python: 3.13.9
pytest: 9.0.2
lean: 4.19.0 (commit 6caaee842e94)
date: 2026-08-24
```

## Ledger

```text
theorem_ledger.json_sha256: 7643b707d85cd877b9bea77de25221b595d7f692c9d5f9c31b4ca1e667bf3191
theorem_ledger.json_bytes: 84071
ledger_rows: 193
ostrowski_rows: 21
ostrowski_exact_lean_verified: 17
ostrowski_refuted: 4
render_theorem_ledger_check: pass
```

Ostrowski IDs:

```text
OST-np-kernel-unreach
OST-np-energy-step
OST-np-energy-telescope
OST-np-energy-ext-interval
OST-np-energy-homogeneous
OST-np-adjoint-window-det
OST-np-origin-particular
OST-np-impulse-place
OST-np-recurrence-word-zero
OST-np-particular-s3
OST-np-consumed-sum-append
OST-np-val-concat-energy
OST-np-complete-zero-monoid
OST-np-fold-s3
OST-np-unnormalized-mode-bound
OST-np-reset-pow-then-hub
OST-np-long-words-infinite-L0
OST-np-unique-predecessor
OST-np-extra-terminal-congruence
OST-np-reset-prefix
OST-np-same-energy-same-OnF
```

## Gates before extraction

```text
pytest tests/research/ostrowski: 137 passed, 1 skipped
pytest (fast): pass
pytest --runslow: 1293 passed
lake build: pass
lake build Problems.Ostrowski.NP: pass
python modules in src/research/ostrowski: 30
pytest modules in tests/research/ostrowski: 16
```

`pytest --runslow` is recorded in the R2 decision entry after the
extraction gates.

This freeze does not change any Ostrowski mathematical claim.
