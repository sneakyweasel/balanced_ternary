# Juggler k=5 post-L OOE escape

Status: **K5_POST_L_OOE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The first square-cell failure
of M(OOE)^k, with M = L+OOE = OOEOOOEOOEEOOE. Not Z5, not a
length-11 assembler, and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     k=5 replacement corridor / parity
Novelty hypothesis      cube cell; even resets to n^{3/2}
Existing machinery      M(OOE)^k square max 4; 501 max k=2
Maximum Phase-0 scope   W_5 gaps; even reset; odd n^4; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **K5_POST_L_OOE_GREEN**
- sorry-free: `True`
- gaps: `{'w5_len': 29, 'w5_odds': 19, 'w5_num': 1162261467, 'w5_den': 536870912, 'w5_square': False, 'w5_cube': True, 'w5_fourth': True, 'w5_even_drops': False, 'w5_even_three_halves': True, 'w5_even_square': True, 'w5_odd_cube': False, 'w5_odd_fourth': True, 'w5_oe_square': True, 'k4_square': True, 'k5_square': False, 'k4_below_two': True, 'k5_above_two': True, 'ratio_nine_eighths': True, 'even_cannot_start_l': True, 'k4_under': 5077565, 'k5_over': 88519643}`
- W_5 hits in window: `0`

W_5 loses the square cell and occupies the cube corridor x_5 < n^{3^{19}/2^{29}} < n^3. The k=5/k=4 ratio is 9/8. Even x_5 resets below n^{3/2} and cannot start L; it is not FiniteProgress. Odd x_5 has next-O image below n^4. 501 never reaches k=5.

## Attack 1 — cube replacement of the square cell

`OOEOOOEOOEEOOEOOEOOEOOEOOEOOE` has length 29 and 19 odds,
so `x_5^{536870912} <= n^{1162261467}`. The square cell fails
(`1073741824 < 1162261467`). The cube cell holds
(`1162261467 < 1610612736`), hence `x_5 < n^3`. The exact
ceiling is `3^{19}/2^{29}`. The lower bound `x_5 >= n^2` is
not forced.

## Attack 2 — 9/8 leak, not a new scale regime

`M(OOE)^4` still has ceiling below 2 (`3^{17} < 2^{27}`).
`W_5` is the first ceiling above 2 (`3^{19} > 2^{30}`).
The exponent ratios differ by exactly `9/8`. Slack is
`5077565` under the square threshold at `k=4` and
`88519643` over it at `k=5`. First integer threshold is
`n^3`, not `n^4`.

## Attack 3 — even reset, odd fourth

Even `x_5` is not FiniteProgress (`1162261467 > 1073741824`)
but returns below `n^{3/2}` (same comparison as the cube
cell) and cannot start `L`. Odd `x_5` has next-`O` image
below `n^4` (`3486784401 < 4294967296`) and may exceed
`n^3`. 501 never follows `W_5` (max `k=2`, landing `12707`
starts `OE`).

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
- k5_contradiction: `False`
- x5_ge_n2_forced: `False`
- even_new_hierarchy: `False`
- even_drops: `False`
- generic_three_halves_only: `False`
- recurrent_l_episode: `False`

## Decision

**K5_POST_L_OOE_GREEN**

W_5 loses the square cell and occupies the cube corridor x_5 < n^{3^{19}/2^{29}} < n^3. The k=5/k=4 ratio is 9/8. Even x_5 resets below n^{3/2} and cannot start L; it is not FiniteProgress. Odd x_5 has next-O image below n^4. 501 never reaches k=5.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

