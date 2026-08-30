# Juggler odd-u next O

Status: **ODD_U_NEXT_O_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The next O after odd u on the
W_5 branch. Not Z5, not a length-11 assembler, and not a
terminal-cluster reopen.

## Branch budget

```text
Mathematical target     odd-u next-O corridor / first integer
Novelty hypothesis      n^{11}; even reset to C_1-C_4
Existing machinery      u < n^8; power_bound_word
Maximum Phase-0 scope   v gaps; even n^6; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ODD_U_NEXT_O_GREEN**
- sorry-free: `True`
- gaps: `{'w5oooo_len': 33, 'w5oooo_odds': 23, 'v_num': 94143178827, 'v_den': 8589934592, 'v_first_integer': 11, 'v_tenth': False, 'v_eleventh': True, 'v_below_generic_twelve': True, 'v_even_square': False, 'v_even_cube': False, 'v_even_fourth': False, 'v_even_fifth': False, 'v_even_sixth': True, 'odd_v_sixteenth': False, 'odd_v_seventeenth': True, 'extra_k0': 3, 'extra_k1': 4, 'extra_k2': 5, 'extra_k3': 8, 'extra_k4': 11, 'even_cannot_start_l': True, 'recover_OE': False, 'recover_OOE': False, 'recover_OEE': False, 'v_tenth_over': 8243832907, 'v_eleventh_under': 346101685, 'v_twelve_under': 8936036277}`
- W_5 hits in window: `0`

Odd u has next-O image v < n^{3^{23}/2^{33}} < n^{11}; n^{10} fails. Inherited beats generic n^{12}. Even v resets below n^6, not to C_1-C_4. Integer cells 3,4,5,8,11 are crossings of (3/2)^k * 3^{19}/2^{29}. 501 never reaches W_5.

## Attack 1 — inherited eleventh-power cell

`W_5+OOOO` has length 33 and 23 odds, so
`v^{8589934592} <= n^{94143178827}`. The tenth-power cell
fails (`94143178827 > 85899345920`). The eleventh holds
(`94143178827 < 94489280512`). Hence
`v < n^{3^{23}/2^{33}} < n^{11}`. This beats generic
`v < n^{12}` from `u < n^8`. Crossing `n^8` is possible,
not forced.

## Attack 2 — even v is not C_1-C_4

Even `v` does not return below `n^2`, `n^3`, `n^4`, or `n^5`.
It does return below `n^6` (`94143178827 < 103079215104`).
That is a new even-reset band, still finite, not a C_1-C_4
replay. Even `v` cannot start `L`. `OE`/`OOE`/`OEE` from `u`
do not contract.

## Attack 3 — integer rungs are crossings

After `W_5` plus `k` extra odds the first integers are
`3,4,5,8,11` for `k=0..4`. These are the crossings of
`(3/2)^k * 3^{19}/2^{29}`, not a new structural rung at
`n^{11}`. Repeated `O` multiplies the rational ceiling by
`3/2`, so the odd residual is not a finite exponent-state
set. 501 never follows `W_5`.

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
- generic_twelve_only: `False`
- v_ge_n8_forced: `False`
- even_resets_to_c4: `False`
- finite_exponent_states: `False`
- n11_new_structural_rung: `False`
- recurrent_episode: `False`

## Decision

**ODD_U_NEXT_O_GREEN**

Odd u has next-O image v < n^{3^{23}/2^{33}} < n^{11}; n^{10} fails. Inherited beats generic n^{12}. Even v resets below n^6, not to C_1-C_4. Integer cells 3,4,5,8,11 are crossings of (3/2)^k * 3^{19}/2^{29}. 501 never reaches W_5.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

