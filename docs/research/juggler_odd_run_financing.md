# Juggler odd-run financing

Status: **ODD_RUN_FINANCING_GREEN**

Standalone application phase. Not a Research Engine experiment,
not a frequency theorem, and not a termination theorem. If a
minimal non-1 orbit realizes `O^a E^b` from a later state `x`,
then `n^{2^{a+b}} ≤ x^{3^a}`. At the start itself the first even
residual cannot occur before `OOE`.

## Branch budget

```text
Mathematical target     MinimalNonTerm n and O^a E from x => n^{2^{a+1}} <= x^{3^a}
Novelty hypothesis      Odd growth finances the first legal even residual
Falsifier               Envelope fail, or xa>=n^2 with n^{2^{a+1}} > x^{3^a}
Existing machinery      power_bound_word, even_run_scale_barrier, follows
Maximum Phase-0 scope   Financing inequality; O^a E^b; start a>=2; later a=1 census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ODD_RUN_FINANCING_GREEN**
- secondary: `['ODD_RUN_MINIMUM_GREEN', 'BLOCK_FINANCING_GREEN', 'SCALE_FINANCING_COUNTEREXAMPLE']`
- sorry-free: `True`

O^a E^b on a minimal non-1 orbit requires n^{2^{a+b}} <= x^{3^a}; at the start the first even residual cannot occur before OOE (smallest a=2); later a=1 occurs (34 times), so an absolute later odd-run lower bound of 2 is false.

## Odd-run census

- realized O^a E^b blocks: `99`
- later (not at start) blocks: `60`
- later a=1 blocks: `34`
- start a=1 blocks: `21`
- odd starts whose first even has a>=2: `18`
- envelope failures: `0`
- financing failures on xa>=n^2: `0`
- block-financing failures: `0`
- blocks with xa>=n^2: `23`
- max a / max b: `4` / `5`
- smallest a with 2^{a+1}<=3^a: `2`

- closest legal even residual: n=`5` x0=`5` a=`2` xa=`36` n^2=`25` margin_bits=`3`
- closest legal even residual with n>=12: n=`33` x0=`33` a=`2` xa=`2598` n^2=`1089` margin_bits=`6`
- later a=1 sample: n=`77` x0=`1523` xa=`59436` xab=`243`

## Calibration

- n=`13` word=`OE` xa=`46` T=`6` kind=`DESCENT` xa>=n^2=`False` exponent_ok=`False`
- n=`27` word=`OE` xa=`140` T=`11` kind=`DESCENT` xa>=n^2=`False` exponent_ok=`False`
- n=`25` word=`OOOE` xa=`52214` T=`228` kind=`NO_CERTIFICATE` xa>=n^2=`True` exponent_ok=`True`
- n=`5` word=`OOE` xa=`36` T=`6` kind=`NO_CERTIFICATE` xa>=n^2=`True` exponent_ok=`True`
- n=`33` word=`OOE` xa=`2598` T=`50` kind=`NO_CERTIFICATE` xa>=n^2=`True` exponent_ok=`True`

## Lean

- `oddEvenBlock`: `True`
- `follows_of_append_right`: `True`
- `odd_run_even_residual`: `True`
- `two_pow_succ_le_three_pow_iff`: `True`
- `odd_run_power_bound`: `True`
- `odd_even_block_scale_barrier`: `True`
- `odd_run_financing_scale_barrier`: `True`
- `initial_even_not_before_ooe`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- FloorPower not rewritten: `True`
- no infinite-path type: `True`
- no frequency theorem: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- all_odd_orbit: `False`
- oe_frequency_theorem: `False`
- absolute_later_odd_run_length: `False`
- repeated_block_obstruction: `False`

## Decision

**ODD_RUN_FINANCING_GREEN**

O^a E^b on a minimal non-1 orbit requires n^{2^{a+b}} <= x^{3^a}; at the start the first even residual cannot occur before OOE (smallest a=2); later a=1 occurs (34 times), so an absolute later odd-run lower bound of 2 is false.

This is not a halt result, not an odd-run frequency theorem,
and not an absolute lower bound on later odd runs.

