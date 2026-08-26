# Juggler repeated O^a E^b blocks

Status: **REPEATED_BLOCK_SCALE_GREEN**

Standalone application phase. Not a Research Engine experiment,
not a frequency theorem, and not a termination theorem. If a
minimal non-1 orbit realizes `(O^a E^b)^r` from a later state `x`,
then `n^{2^{r(a+b)}} ≤ x^{3^{a r}}`. Formally contracting blocks
cannot start at `n_*`. Repeated expansion can stay above the start.

## Branch budget

```text
Mathematical target     (O^a E^b)^r on MinimalNonTerm => n^{2^{r(a+b)}} <= x^{3^{a r}}
Novelty hypothesis      Contracting start is forbidden; expanding repetition may survive
Falsifier               Envelope fail, stay-ge-n scale fail, or start-contracting stay
Existing machinery      power_bound_word, power_bound_contracts, oddEvenBlock, MinimalNonTerm
Maximum Phase-0 scope   Repeated envelope+barrier; start contraction; expanding census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **REPEATED_BLOCK_SCALE_GREEN**
- secondary: `['REPEATED_CONTRACTION_FORBIDDEN', 'REPEATED_EXPANSION_SURVIVES']`
- sorry-free: `True`

(O^a E^b)^r on a minimal non-1 orbit requires n^{2^{r(a+b)}} <= x^{3^{a r}}; contracting blocks cannot start at n_*; expanding repetition can stay above the start.

## Repeated-block census

- realized runs: `247`
- stay >= n: `53`
- envelope failures: `0`
- scale failures on stay-ge-n: `0`
- expanding stay: `29`
- contracting stay: `24`
- expanding r>=2 stay: `2`
- start contracting stay: `0`
- max r: `2`
- max expanding stay r: `2`

- longest expanding stay: n=`37` x0=`225` O^3E^1 r=`2` xr=`4990602` kind=`EXPANDING`

## Closest expanding regimes

- O^2E^1: 3^2=`9` vs 2^3=`8`
- O^4E^2: 3^4=`81` vs 2^6=`64`
- O^3E^1: 3^3=`27` vs 2^4=`16`
- O^5E^2: 3^5=`243` vs 2^7=`128`
- O^4E^1: 3^4=`81` vs 2^5=`32`
- O^5E^1: 3^5=`243` vs 2^6=`64`

## Calibration

- n=`13` word=`OE` T=`6` kind=`DESCENT` stay=`False` expanded=`False`
- n=`69` word=`OOEOOE` T=`212` kind=`NO_CERTIFICATE` stay=`True` expanded=`True`
- n=`5` word=`OOE` T=`6` kind=`NO_CERTIFICATE` stay=`True` expanded=`True`
- n=`17537` word=`OEOE` T=`243` kind=`DESCENT` stay=`False` expanded=`False`
- n=`225` word=`OOOEOOOE` T=`4990602` kind=`NO_CERTIFICATE` stay=`True` expanded=`True`

## Lean

- `repeatedOddEven`: `True`
- `odd_even_exponents_ne`: `True`
- `contracting_gap_repeat`: `True`
- `repeated_block_power_bound`: `True`
- `repeated_odd_even_scale_barrier`: `True`
- `contracting_odd_even_block_contracts`: `True`
- `contracting_repeated_odd_even_contracts`: `True`
- `initial_contracting_block_forbidden`: `True`
- `initial_contracting_repeated_forbidden`: `True`
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
- repetition_global_obstruction: `False`
- contracting_later_forbidden: `False`

## Decision

**REPEATED_BLOCK_SCALE_GREEN**

(O^a E^b)^r on a minimal non-1 orbit requires n^{2^{r(a+b)}} <= x^{3^{a r}}; contracting blocks cannot start at n_*; expanding repetition can stay above the start.

Repetition alone is not a global obstruction. This is not a
halt result and not a block-frequency theorem.

