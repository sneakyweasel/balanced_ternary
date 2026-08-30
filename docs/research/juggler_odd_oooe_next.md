# Juggler next O after an odd OOOE landing

Status: **ODD_OOOE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The forced next O after an odd
OOEOOOE landing in [n, n^2). Not Z5, not a length-11 assembler,
and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     next O after odd OOEOOOE landing
Novelty hypothesis      q in [n^2, n^3); even q shrinks
Existing machinery      OOEOOOE envelope; cube lemma;
                        243 < 256
Maximum Phase-0 scope   inherited envelope; Case split;
                        no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ODD_OOOE_GREEN**
- sorry-free: `True`
- 729 < 768: `True`
- OOEOOOEOEE contracts: `True`
- gaps: `{'OOEOOOE': True, 'OOEOOOEO': False, 'OOEOOOEOE': True, 'OOEOOOEOO': False, 'OOEOOOEOOE': False, 'OOEOOOEOEE': True, 'q_lt_n3': True, 'ooeoooeeoe_contracts': True, 'next_o_refines_square': False}`
- first events: `{'even_odd_O': 2, 'odd_OOE': 2, 'even_even_drop': 1}`
- q / r fail: `0` / `0`

after an odd OOEOOOE landing, q lies in [n^2, n^3); even q returns to [n, n^{3/2}); odd q starts a second OO above n^2. OOEOOOEO is the first lost square-cell word.

## Attack 1 — inherited envelope

`OOEOOOE` gives `w^{128} <= n^{243}` and `w < n^2` (`256 > 243`).
The next-O square refinement `3*243 < 4*128` fails (`729 > 512`).
`OOEOOOEO` is the first lost square-cell word (`512 < 729`).
Raising one more odd step still gives `q^{256} <= n^{729} < n^{768}`,
so `q < n^3`. The cube lemma at `n+1` gives `q >= n^2`.

## Attack 2 — three-way split

If `q` is even, the OE landing `r` lies in `[n, n^{3/2})`.
Even `r` drops (`OOEOOOEOEE` contracts: `729 < 1024`).
Odd `r` forces another `O` from a strictly smaller upper bound.
If `q` is odd, a second `OO` starts from `[n^2, n^3)`.

## Attack 3 — 483 versus 491

Both have `w/n^2 ~ 0.533`. The split is the parity of `q`,
not the cell position. The corridor does not always shrink.

## Window samples

- n=`319` branch=`even_q` first=`even_even_drop` q<n3=`True`
- n=`483` branch=`even_q` first=`even_odd_O` q<n3=`True`
- n=`491` branch=`odd_q` first=`odd_OOE` q<n3=`True`
- n=`497` branch=`even_q` first=`even_odd_O` q<n3=`True`
- n=`501` branch=`odd_q` first=`odd_OOE` q<n3=`True`

## Named witnesses

- n=`319` branch=`even_q` first=`even_even_drop`
- n=`483` branch=`even_q` first=`even_odd_O`
- n=`491` branch=`odd_q` first=`odd_OOE`
- n=`501` branch=`odd_q` first=`odd_OOE`
- n=`1181` branch=`odd_q` first=`odd_OOO`

## Lean

- `CycleMin`: `True`
- `power_bound_word`: `True`
- `power_bound_contracts`: `True`
- `ooo_residual_ge_cube`: `True`
- `no_cycleMin_ooeoooe`: `True`
- `floorPower_oooee_five_step_lt`: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- cycles_impossible: `False`
- length_eleven_census: `False`
- z5_cells: `False`
- four_even_assembler: `False`
- even_q_always_drops: `False`
- corridor_always_shrinks: `False`

## Decision

**ODD_OOOE_GREEN**

after an odd OOEOOOE landing, q lies in [n^2, n^3); even q returns to [n, n^{3/2}); odd q starts a second OO above n^2. OOEOOOEO is the first lost square-cell word.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

