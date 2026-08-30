# Juggler expanding-residual concatenation

Status: **EXPANDING_CONCAT_CE_CLOSE**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Expanding concatenations stay
expanding. A CE never realizes an exponent gap. The leftover
is MinimalNonTerm, not a stricter PE class.

## Branch budget

```text
Mathematical target     Is infinite PE concatenation without a
                        contracting word a stricter class than
                        MinimalNonTerm?
Novelty hypothesis      the leftover is the same CE branch
Existing machinery      exponentExpanding; power_bound_contracts;
                        residual_chain
Maximum Phase-0 scope   expanding_append; CE prefix-NC; chain scan
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **EXPANDING_CONCAT_CE_CLOSE**
- sorry-free: `True`
- PE blocks expanding: `87` / `87`
- contracting PE: `0`
- concat fail: `0`
- contracting above start (not PE): `83`
- 365 blocks: `[(2, 1), (2, 1), (2, 1)]`

expanding concatenations stay expanding; a CE never realizes an exponent gap; the leftover is MinimalNonTerm, not a stricter PE class.

## Attack 1 — concatenation closure

If `u` and `v` are expanding, then `u ++ v` is expanding:
`2^{|u|+|v|} = 2^{|u|} 2^{|v|} < 3^{o(u)} 3^{o(v)}`.
A PE concatenation is never an exponent-gap certificate.

## Attack 2 — CE prefix-NC

`power_bound_contracts` plus `minimal_nonterm_no_descent`
forbid every exponent-gap word on a CE. Every realized
prefix is prefix-noncontracting.

## Attack 3 — the leftover is not smaller

The prefix `[365, 763, 1749, 4447]` is three expanding `OOE`
blocks. Formal contraction does not kill it. Infinite PE
without a contracting word is the unbounded CE branch.

## Lean

- `exponentExpanding_append`: `True`
- `minimal_nonterm_not_exponentGap`: `True`
- `minimal_nonterm_prefix_noncontracting`: `True`
- `minimal_ooeooe_forces_oo`: `True`
- `exponentExpanding`: `True`
- `exponentGap`: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- no_escape: `False`
- cycles_impossible: `False`
- finite_pe_run_bound: `False`
- smaller_than_minimal_nonterm: `False`

## Decision

**EXPANDING_CONCAT_CE_CLOSE**

expanding concatenations stay expanding; a CE never realizes an exponent gap; the leftover is MinimalNonTerm, not a stricter PE class.

This is not a halt result and not a finite PE-run bound.

