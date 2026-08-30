# Juggler post-L OOE residual

Status: **POST_L_OOE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The first OOE after L on the
inherited even-even corridor. Not Z5, not a length-11
assembler, and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     post-L OOE: new L-entrance or not
Novelty hypothesis      M+E / M+OE drop; M has a square cell
Existing machinery      2187/2048; 501 OO residual
Maximum Phase-0 scope   M envelope; E/OE after one OOE;
                        501 / 17245; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **POST_L_OOE_GREEN**
- sorry-free: `True`
- gaps: `{'M_square': True, 'M_contracts': False, 'ME_contracts': True, 'MOE_contracts': True, 'M_envelope': True, 'ooe_from_t_drops': False, 'ooeoe_from_t_drops': True, 'two_ooe_oe_contracts': False}`

L+OOE gives T_M(n)^{16384} <= n^{19683} and T_M < n^2. If the landing is even or follows OE, M+E / M+OE contract versus n. 17245 is the OE drop. 501 continues OO and does not re-enter L.

## Attack 1 — the word M = L+OOE

`OOEOOOEOOEEOOE` has length 14 and 9 odds, so
`T_M(n)^{16384} <= n^{19683}`. The square-cell gap
`32768 > 19683` gives `T_M(n) < n^2`. Contraction versus
`n` fails (`19683 > 16384`).

## Attack 2 — E or OE after the first post-L OOE

`M+E` contracts (`19683 < 32768`). `M+OE` contracts
(`59049 < 65536`). So a post-L OOE landing that does not
start `OO` is FiniteProgress. `OOE` from `t` alone does
not drop. A second `OOE` then `OE` does not contract
versus `n` (`3^{12} > 2^{19}`).

## Attack 3 — 501 versus 17245

`17245` lands at `122949` and follows `OE` to `6565`.
`501` lands at `1749`, starts `OO`, and never pays a
first `OOO` or a second `L`. The residual is a second
post-L `OOE`, not an L-entrance.

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
- reenters_L: `False`
- post_l_ooe_always_drops: `False`
- anchor_induction: `False`
- generic_ooe_only: `False`

## Decision

**POST_L_OOE_GREEN**

L+OOE gives T_M(n)^{16384} <= n^{19683} and T_M < n^2. If the landing is even or follows OE, M+E / M+OE contract versus n. 17245 is the OE drop. 501 continues OO and does not re-enter L.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

