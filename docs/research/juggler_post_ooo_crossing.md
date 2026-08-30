# Juggler post-OOO square-ceiling crossing

Status: **POST_OOO_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The completed OOOE landing after
a first OOO from C_3(n). Not Z5, not a length-11 assembler,
and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     post-OOO OOOE corridor from C_3(n)
Novelty hypothesis      even OOOE drops; odd OOOE stays in C_3
Existing machinery      second-odd escape; OOEOOOE gap;
                        ooo_residual_ge_cube; OOOEE contracts
Maximum Phase-0 scope   k=1 OOOE envelope; Case A/B/C;
                        no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **POST_OOO_GREEN**
- sorry-free: `True`
- 243 < 256: `True`
- OOEOOOEE contracts: `True`
- gaps: `{'OOOE': True, 'OOOEE': True, 'OOOEO': False, 'OOOEOE': True, 'OOEOOOE': True, 'OOEOOOEE': True, 'k1_u_lt_n4': True, 'ooeoooe_contracts': True}`
- cases A/B/C: `{'C': 5, 'B': 5, 'A': 2}`
- k=1 OOOE in C_3: `7` / `7`
- first events: `{'drop': 6, 'next_OOO': 4, 'even_drop': 2}`
- second OOO in/out of n^2: `3` / `1`
- falsifier B: `0`

after first OOO following one OOE, T^3(x) < n^4 so a completed OOOE landing lies in [n, n^2); even w drops; odd w stays in C_3(n). A longer odd run is a residual.

## Attack 1 — k=1 third-odd envelope

`power_bound_word` on `OOE` is `x^8 <= n^9`. On `OOO` it is
`u^8 <= x^{27}`. Then `u^{64} <= n^{243} < n^{256} = (n^4)^{64}`,
so `T^3(x) < n^4`. Completed `OOOE` has `w = isqrt(u) < n^2`.
The cube lemma gives `u >= (x+1)^3`, hence `w >= n`. The word
`OOEOOOE` has the same square-cell gap (`256 > 243`).

## Attack 2 — even / odd landing

If `w` is even, `OOEOOOEE` contracts versus `n` (`243 < 256`),
and the even-below-`n^2` trap also drops. If `w` is odd, the
next letter is `O` from a state still in `[n, n^2)`.

## Attack 3 — OOO is not fatal

A longer odd run can leave the OOOE corridor. A second OOO
may start inside or outside `n^2`. No monotone strengthening.

## Window samples

- n=`105` case=`A` kind=`OOOE` first=`even_drop` w<n2=`True`
- n=`173` case=`C` kind=`O^8E` first=`drop` w<n2=`False`
- n=`229` case=`C` kind=`O^9E` first=`drop` w<n2=`False`
- n=`269` case=`A` kind=`OOOE` first=`even_drop` w<n2=`True`
- n=`319` case=`B` kind=`OOOE` first=`drop` w<n2=`True`
- n=`483` case=`B` kind=`OOOE` first=`next_OOO` w<n2=`True`
- n=`491` case=`B` kind=`OOOE` first=`next_OOO` w<n2=`True`
- n=`497` case=`B` kind=`OOOE` first=`next_OOO` w<n2=`True`

## Named witnesses

- n=`105` case=`A` kind=`OOOE` first=`even_drop`
- n=`483` case=`B` kind=`OOOE` first=`next_OOO`
- n=`491` case=`B` kind=`OOOE` first=`next_OOO`
- n=`565` case=`C` kind=`O^9E` first=`drop`
- n=`173` case=`C` kind=`O^8E` first=`drop`

## Lean

- `CycleMin`: `True`
- `power_bound_word`: `True`
- `power_bound_contracts`: `True`
- `floorPower_oooee_five_step_lt`: `True`
- `oo_suffix_threshold`: `True`
- `ooo_residual_ge_cube`: `True`
- `odd_ge_succ_sq_floorPower_ge_cube`: `True`
- `no_cycleMin_ooeoooe`: `True`
- `ooo_suffix_threshold`: `True`

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
- ooo_fatal: `False`
- second_ooo_stronger: `False`

## Decision

**POST_OOO_GREEN**

after first OOO following one OOE, T^3(x) < n^4 so a completed OOOE landing lies in [n, n^2); even w drops; odd w stays in C_3(n). A longer odd run is a residual.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

