# Juggler second OO from the cube corridor

Status: **SECOND_OO_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The second OO after an odd
cube-corridor q from OOEOOOE. Not Z5, not a length-11
assembler, and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     second OO from odd q in [n^2, n^3)
Novelty hypothesis      inherited 729/256 beats generic 3/2
Existing machinery      odd OOEOOOE cube corridor;
                        729 < 768
Maximum Phase-0 scope   raise 729/256 through OO;
                        parity split; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **SECOND_OO_GREEN**
- sorry-free: `True`
- 2187 < 2560 and 6561 < 7168: `True`
- inherited u / v sharper: `True` / `True`
- gaps: `{'OOEOOOEOO': False, 'OOEOOOEOOE': False, 'OOEOOOEOOEE': True, 'u_lt_n5': True, 'u_lt_n4': False, 'u_sharper': True, 'v_lt_n7': True, 'v_lt_n6': False, 'v_sharper': True, 's_lt_n2': False, 't_lt_n': False, 'ooeoooeeooee_contracts': False}`
- first events: `{'even_odd_OOO': 1, 'even_even_c1': 1}`
- graph edges: `{'odd_u_odd_OOO': 3, 'even_odd_OOO': 1, 'even_even_c1': 1, 'odd_u_odd_OOE': 1}`
- C_1 return: `True`
- u / v / s fail: `0` / `0` / `0`

odd q from OOEOOOE carries q^{256} <= n^{729} into the next OO: n^3 <= T(q) < n^{2187/512}; even T(q) lands in [n^{3/2}, n^{2187/1024}); odd T(q) continues with T^2(q)^{1024} <= n^{6561}. Sharper than generic 3/2. The scale graph returns to C_1 (501).

## Attack 1 — inherited envelopes

`q^{256} <= n^{729}` and `u^2 <= q^3` give `u^{512} <= n^{2187}`.
So `n^3 <= u < n^{2187/512}` (`2187 < 2560`, `2187 > 2048`).
This is sharper than the generic `u < n^{9/2}` (`2187 < 2304`).
If `u` is odd, `v^{1024} <= n^{6561}`, so
`n^{9/2} <= v < n^{6561/1024}` (`6561 < 7168`, `6561 > 6144`,
and `6561 < 6912` beats generic `n^{27/4}`).

## Attack 2 — parity after the first image

Even `u` lands at `s` with `n^{3/2} <= s < n^{2187/1024}`.
`s < n^2` is not forced (`2187 > 2048`). The word
`OOEOOOEOOEE` does not contract versus `n` (`2187 > 2048`).
Odd `u` continues the second `OO` into the `6561/1024` band.

## Attack 3 — scale graph

Observed inherited odd-`q` types: `C_1 --O--> C_2 --O--> C_4`,
then even `u` to `C_2` or odd `u` to `C_6`. The even-even
landing of `501` returns to `C_1` (`763`). The scale graph
is not acyclic.

## Window samples

- n=`491` branch=`even_u` first=`even_odd_OOO` u-band=`4`
- n=`501` branch=`even_u` first=`even_even_c1` u-band=`4`

## Named witnesses

- n=`491` branch=`even_u` first=`even_odd_OOO`
- n=`501` branch=`even_u` first=`even_even_c1`
- n=`1181` branch=`odd_u` first=`odd_OOO`

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
- second_oo_in_c2_c3: `False`
- scale_automaton_acyclic: `False`
- even_u_always_drops: `False`
- defect_chain_constrained: `False`

## Decision

**SECOND_OO_GREEN**

odd q from OOEOOOE carries q^{256} <= n^{729} into the next OO: n^3 <= T(q) < n^{2187/512}; even T(q) lands in [n^{3/2}, n^{2187/1024}); odd T(q) continues with T^2(q)^{1024} <= n^{6561}. Sharper than generic 3/2. The scale graph returns to C_1 (501).

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

