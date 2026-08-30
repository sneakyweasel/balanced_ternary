# Juggler first-lift eighth cell

Status: **FIRST_LIFT_EIGHTH_REFUTED**

First leftover cube-odd even lifts are not forced into `x^3 < n^8`.
Not a halt theorem.

## Branch budget

```text
Mathematical target     leftover first cube-odd => x^3 < n^8?
Novelty hypothesis      inherited PE envelope ratio <= 8/3
Maximum Phase-0 scope   leftover first hits; OOEOOEOO census
```

## Metadata

- classification: **FIRST_LIFT_EIGHTH_REFUTED**
- Falsifier A: `True`
- leftovers enveloped: `True`
- unsafe word: `OOEOOEOO`

AboveAnchor first cube-odd even lift does not force x^3 < n^8: n=4309 follows OOEOOEOO; named leftovers sit below only because their first-lift words keep 3^{o+1} < 8*2^{|w|}.

## Lean

- `AboveAnchor`: `True`
- `odd_even_eighth_lt_sq`: `True`
- `finiteProgress_of_odd_even_eighth`: `True`
- `power_bound_word`: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- first_lift_always_eighth: `False`
- letter_chain: `False`
- q_return: `False`

## Decision

**FIRST_LIFT_EIGHTH_REFUTED**

AboveAnchor first cube-odd even lift does not force x^3 < n^8: n=4309 follows OOEOOEOO; named leftovers sit below only because their first-lift words keep 3^{o+1} < 8*2^{|w|}.

