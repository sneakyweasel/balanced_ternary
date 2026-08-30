# Juggler cube-odd return

Status: **CUBE_ODD_RETURN_GREEN**

Even reset after an odd cube lift returns below the source.
Not a halt theorem.

## Branch budget

```text
Mathematical target     odd-cube-lift return geometry
Novelty hypothesis      even y => T^2 < x < n^3
Maximum Phase-0 scope   Lean even-reset; 501 square refute
```

## Metadata

- classification: **CUBE_ODD_RETURN_GREEN**
- even reset: `True`
- 501 later square-return false: `True`

odd cube lift splits: even y returns below the source (hence below n^3); odd y continues above x and at least n^4; even return below n^2 is false (501 later landing).

## Lean

- `CubeOddLanding`: `True`
- `odd_lt_cube_floor_sq_lt_nine`: `True`
- `odd_lt_cube_floor_lt_five`: `True`
- `cube_odd_lift`: `True`
- `cube_lift_even_reset`: `True`
- `cube_lift_even_reset_lt_cube`: `True`
- `cube_lift_even_reset_fourth`: `True`
- `cube_lift_odd_continues`: `True`
- `cube_lift_odd_ge_fourth`: `True`
- `finiteProgress_of_cube_odd_even_below_square`: `True`
- `minimal_cube_odd_even_not_even_below_square`: `True`
- `odd_ge_sq_floor_ge_cube`: `True`
- `even_below_anchor_pow`: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- even_return_below_square: `False`
- power_census: `False`

## Decision

**CUBE_ODD_RETURN_GREEN**

odd cube lift splits: even y returns below the source (hence below n^3); odd y continues above x and at least n^4; even return below n^2 is false (501 later landing).

