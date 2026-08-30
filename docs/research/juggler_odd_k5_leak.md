# Juggler odd k=5 leak

Status: **ODD_K5_LEAK_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The odd residual after W_5.
Not Z5, not a length-11 assembler, and not a terminal-cluster
reopen.

## Branch budget

```text
Mathematical target     odd x_5 next-O corridor / parity
Novelty hypothesis      y < n^{3^{20}/2^{30}} < n^4; even y to C_1
Existing machinery      W_5 cube cell; power_bound_word
Maximum Phase-0 scope   y gaps; OEE recovery; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ODD_K5_LEAK_GREEN**
- sorry-free: `True`
- gaps: `{'w5o_len': 30, 'w5o_odds': 20, 'y_num': 3486784401, 'y_den': 1073741824, 'y_cube': False, 'y_fourth': True, 'y_below_nine_halves': True, 'y_even_drops': False, 'y_even_three_halves': False, 'y_even_square': True, 'y_oe_square': True, 'y_oo_fourth': False, 'y_oo_fifth': True, 'y_oo_even_cube': True, 'even_y_cannot_start_l': True, 'recover_E': False, 'recover_OE': False, 'recover_OOE': False, 'recover_OOOE': False, 'recover_OEE': True, 'recover_OOEE': False, 'y_cube_over': 265558929, 'y_fourth_under': 808182895}`
- W_5 hits in window: `0`

Odd x_5 has next-O image y < n^{3^{20}/2^{30}} < n^4; the cube cell fails, so y may cross n^3. Even y resets below n^2 and cannot start L; OEE contracts. E/OE/OOE/OOOE do not. The leftover is odd y (second OO below n^5).

## Attack 1 — inherited next-O envelope

`W_5+O` has length 30 and 20 odds, so
`y^{1073741824} <= n^{3486784401}`. The cube cell fails
(`3486784401 > 3221225472`). The fourth-power cell holds
(`3486784401 < 4294967296`), and the ceiling is below the
generic `9/2` (`3486784401 < 4831838208`). Hence
`y < n^{3^{20}/2^{30}} < n^4`. Crossing `n^3` is possible,
not forced.

## Attack 2 — even y resets to C_1

Even `y` is not FiniteProgress (`3486784401 > 2147483648`)
and does not return below `n^{3/2}`. It does return below
`n^2` (`3486784401 < 4294967296`) and cannot start `L`.
`W_5+OEE` contracts (`3486784401 < 4294967296`). `E`, `OE`,
`OOE`, and `OOOE` do not.

## Attack 3 — odd y is the leftover

A second `O` stays below `n^5` and may exceed `n^4`. An even
landing after that second `O` returns below `n^3`. 501 never
follows `W_5`.

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
- generic_nine_halves_only: `False`
- y_stays_in_c3: `False`
- y_ge_n3_forced: `False`
- even_y_new_hierarchy: `False`
- even_y_drops: `False`
- short_ooe_recovers: `False`
- recurrent_k5_episode: `False`

## Decision

**ODD_K5_LEAK_GREEN**

Odd x_5 has next-O image y < n^{3^{20}/2^{30}} < n^4; the cube cell fails, so y may cross n^3. Even y resets below n^2 and cannot start L; OEE contracts. E/OE/OOE/OOOE do not. The leftover is odd y (second OO below n^5).

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

