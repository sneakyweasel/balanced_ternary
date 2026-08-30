# Juggler minimum-relative consolidation

Status: **MINIMUM_RELATIVE_GREEN**

Shared `AboveAnchor` layer. CycleMin and MinimalNonTerm are
consumers. Not a halt theorem and not a no-cycle theorem.

## Branch budget

```text
Mathematical target     share minimum-relative geometry
                        between CycleMin and MinimalNonTerm
Novelty hypothesis      Type B lemmas do not use closure
Maximum Phase-0 scope   AboveAnchor; isolated survival;
                        square trap; FiniteProgress bridge
```

## Metadata

- classification: **MINIMUM_RELATIVE_GREEN**
- leftover coincide: `False`
- leftover: odd-landing corridors that stay AboveAnchor on every finite prefix, never land even below n^2, may sit in a cube cell (image < n^3) without a square cell, never realize a scale-gap isolated prefix, and do not eventually cycle

AboveAnchor serves CycleMin and MinimalNonTerm; isolated survival and the OOEOOE even-trap produce FiniteProgress; no-cycle implies no bounded nonterm; odd-landing escape corridors remain.

## Lean

- `AboveAnchor`: `True`
- `aboveAnchor_of_cycleMin`: `True`
- `aboveAnchor_of_minimalNonTerm`: `True`
- `aboveAnchor_not_lt`: `True`
- `finiteProgress_of_prefix_drop`: `True`
- `even_below_square_drop`: `True`
- `even_below_anchor_pow`: `True`
- `even_below_fourth`: `True`
- `even_below_cube`: `True`
- `finiteProgress_of_even_below_square`: `True`
- `finiteProgress_of_power_bound_lt_pow`: `True`
- `finiteProgress_of_even_power_bound_square`: `True`
- `EnvelopeState`: `True`
- `envelope_lt_pow`: `True`
- `power_bound_lt_pow`: `True`
- `PowerCorridor`: `True`
- `power_corridor_contradiction`: `True`
- `envelope_corridor_contradiction`: `True`
- `two_even_below_fourth`: `True`
- `aboveAnchor_even_run_ge_pow`: `True`
- `aboveAnchor_not_envelope_drop`: `True`
- `isolatedOddSurvival_bound`: `True`
- `aboveAnchor_isolated_two`: `True`
- `finiteProgress_of_ooe_oe`: `True`
- `finiteProgress_of_ooeooe_even_landing`: `True`
- `finiteProgress_of_aboveAnchor_returnBelow`: `True`
- `no_nontrivial_cycle_no_bounded_nonterm`: `True`
- `minimal_nonterm_not_finiteProgress`: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- cycles_impossible: `False`
- no_escape: `False`
- above_anchor_is_closure: `False`

## Decision

**MINIMUM_RELATIVE_GREEN**

AboveAnchor serves CycleMin and MinimalNonTerm; isolated survival and the OOEOOE even-trap produce FiniteProgress; no-cycle implies no bounded nonterm; odd-landing escape corridors remain.

