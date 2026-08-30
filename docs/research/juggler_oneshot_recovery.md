# Juggler recovery after the one-shot OOEOOOEOOEE loop

Status: **ONESHOT_RECOVERY_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Post-L recovery on the inherited
even-even second-OO corridor. Not Z5, not a length-11
assembler, and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     post-L entrance exclusion / recovery
Novelty hypothesis      E or OE after L drops below n
Existing machinery      t^{2048} <= n^{2187}; 501 / 6187
Maximum Phase-0 scope   compose 2187/2048 through E, OE;
                        named OO residual; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ONESHOT_RECOVERY_GREEN**
- sorry-free: `True`
- gaps: `{'even_t_drops': True, 'oe_from_t_drops': True, 'ooe_from_t_drops': False, 'ooee_from_t_drops': True, 'ooeoe_from_t_drops': True, 'oooee_from_t_drops': True, 'L_composes_below_n': False, '501_recovery_composes': True}`

after L(n)=T_OOEOOOEOOEE(n), even t or OE forces FiniteProgress by 2187<4096 and 6561<8192. Those states are outside the OOE entrance. The OO residual 501 recovers by OOEOOEOOEOEE and does not re-enter L.

## Attack 1 — composed exponents

If `t^{2048} <= n^{2187}` and `t` follows `W`, then
`T_W(t) < n` whenever `2187 * 3^{#O(W)} < 2048 * 2^{|W|}`.
`E` gives `2187 < 4096`. `OE` gives `6561 < 8192`.
`OOE` fails. `OOEOOOEOOEE` itself fails, so a second `L`
is not an exponent drop.

## Attack 2 — three-way post-L split

Even `t` drops by `E` (`11233 -> 145`). Odd `t` following
`OE` drops (`6187 -> 1087`, `11853 -> 1831`). Those images
cannot start `OOE`, so they are outside the pre-L entrance.
The residual is odd `t` starting `OO` (`501 -> 763`).

## Attack 3 — the OO residual does not re-enter L

`763` still starts `OOE` but never pays a first `OOO`.
It recovers by `OOEOOEOOEOEE` (`2187 * 2187 < 2048 * 4096`)
to `34`. `L(763)` is undefined on the word; `second_oo(763)`
is missing.

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
- all_recoveries_oe: `False`
- remainder_lyapunov: `False`
- oo_residual_closed: `False`

## Decision

**ONESHOT_RECOVERY_GREEN**

after L(n)=T_OOEOOOEOOEE(n), even t or OE forces FiniteProgress by 2187<4096 and 6561<8192. Those states are outside the OOE entrance. The OO residual 501 recovers by OOEOOEOOEOEE and does not re-enter L.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

