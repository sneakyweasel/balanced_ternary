# Juggler repeated OE scale budget

Status: **REPEATED_OE_SCALE_GREEN**

Standalone application phase. Not a Research Engine experiment,
not a frequency theorem, and not a termination theorem. If a
minimal non-1 orbit contains `r` consecutive `OE` blocks from `x`,
then `n^{4^r} ≤ x^{3^r}`.

## Branch budget

```text
Mathematical target     r consecutive OE blocks require n^{4^r} <= x^{3^r}
Novelty hypothesis      Repeated OE is a finite scale budget
Falsifier               Envelope fail, or stay-ge-n run with x^{3^r} < n^{4^r}
Existing machinery      power_bound_word, MinimalNonTerm, even_run_scale_barrier
Maximum Phase-0 scope   OE/(OE)^r envelope; barrier; start-forbidden (OE)^r
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **REPEATED_OE_SCALE_GREEN**
- sorry-free: `True`

r consecutive OE blocks on a minimal non-1 orbit require n^{4^r} <= x^{3^r}; (OE)^r cannot start at n_* itself.

## Consecutive OE census

- realized OE runs: `79`
- runs with exit >= n: `20`
- envelope failures: `0`
- scale failures on stay-ge-n: `0`
- max consecutive r: `2`
- max r with exit >= n: `2`

- longest stay-ge-n: n=`77` x=`17537` r=`2` image=`243`

## Calibration

- n=`13` word=`OE` T=`6` kind=`DESCENT`
- n=`27` word=`OE` T=`11` kind=`DESCENT`
- n=`25` word=`OOOE` T=`228` kind=`NO_CERTIFICATE`

## Lean

- `wordOE`: `True`
- `repeatedOE`: `True`
- `oe_block_scale`: `True`
- `oe_block_contracts`: `True`
- `repeated_oe_scale`: `True`
- `repeated_oe_scale_barrier`: `True`
- `oe_requires_scale`: `True`
- `minimal_nonterm_not_repeated_oe`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
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

## Decision

**REPEATED_OE_SCALE_GREEN**

r consecutive OE blocks on a minimal non-1 orbit require n^{4^r} <= x^{3^r}; (OE)^r cannot start at n_* itself.

This is not a halt result and not an OE-frequency theorem.

