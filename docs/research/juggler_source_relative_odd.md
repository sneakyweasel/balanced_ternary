# Juggler source-relative odd reset

Status: **SOURCE_RELATIVE_ODD_CLOSED**

Persistent-odd cube lifts do not postpone source-relative descent.
Not a halt theorem.

## Branch budget

```text
Mathematical target     first even after odd cube lift < x^2?
Novelty hypothesis      persistent odd postpones the same reset
Maximum Phase-0 scope   37 witness; leftover tau; no new Lean
```

## Metadata

- classification: **SOURCE_RELATIVE_ODD_CLOSED**
- falsifier A: `True`
- leftover first lifts tau=1: `True`

persistent-odd cube lift does not postpone the source-relative reset: two odds give e^4 <= x^9 (9>8), and 37 has first even 86818724 >= 3375^2 with T(e)=9317 >= 3375; episode sources 3375, 9317, 2233 oscillate.

## Lean

- `cube_lift_even_reset`: `True`
- `cube_lift_odd_continues`: `True`
- `floorPower_odd_even_two_step_lt`: `True`
- `EnvelopeState`: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- source_relative_odd_reset: `False`
- episode_source_descent: `False`
- power_census: `False`

## Decision

**SOURCE_RELATIVE_ODD_CLOSED**

persistent-odd cube lift does not postpone the source-relative reset: two odds give e^4 <= x^9 (9>8), and 37 has first even 86818724 >= 3375^2 with T(e)=9317 >= 3375; episode sources 3375, 9317, 2233 oscillate.

