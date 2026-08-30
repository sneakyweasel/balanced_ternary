# Juggler second post-L OOE residual

Status: **SECOND_POST_L_OOE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The second OOE after M=L+OOE.
Not Z5, not a length-11 assembler, and not a terminal-cluster
reopen.

## Branch budget

```text
Mathematical target     second post-L OOE square cell / k-max
Novelty hypothesis      M+OOE still < n^2; k<=4; even r drops
Existing machinery      M square cell; 501 -> 1749
Maximum Phase-0 scope   M+(OOE)^k gaps; 501 r=4447; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **SECOND_POST_L_OOE_GREEN**
- sorry-free: `True`
- gaps: `{'M2_square': True, 'M2_contracts': False, 'M2_even_drops': True, 'M2_oe_contracts': False, 'M2_oe_square': True, 'M2_oee_contracts': True, 'k0_square': True, 'k4_square': True, 'k5_square': False, 'k_max': 4}`

M+(OOE)^k stays below n^2 for k<=4 and loses the square cell at k=5. The second OOE has r < n^2; even r drops; OE after it does not contract. 501 lands at 4447 and starts another OO.

## Attack 1 — M+OOE square cell

`OOEOOOEOOEEOOEOOE` has length 17 and 11 odds, so
`r^{131072} <= n^{177147}` and `262144 > 177147` gives
`r < n^2`. Contraction versus `n` fails (`177147 > 131072`).
Even `r` drops (`177147 < 262144`).

## Attack 2 — finite k-budget

`M+(OOE)^k` has the square gap `2^{15+3k} > 3^{9+2k}`
exactly for `k <= 4`. The cell is lost at `k=5`
(`1073741824 < 1162261467`). This is a corridor budget,
not a halt bound.

## Attack 3 — OE is no longer FiniteProgress

`M+OOEOE` still has a square cell (`531441 < 1048576`)
but does not contract (`531441 > 524288`). If that
landing is even, `M+OOEOEE` contracts. 501 lands at
`4447` and starts `OO`, so the residual continues.

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
- k_unbounded: `False`
- second_oe_drops: `False`
- generic_ooe_only: `False`
- anchor_induction: `False`

## Decision

**SECOND_POST_L_OOE_GREEN**

M+(OOE)^k stays below n^2 for k<=4 and loses the square cell at k=5. The second OOE has r < n^2; even r drops; OE after it does not contract. 501 lands at 4447 and starts another OO.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

