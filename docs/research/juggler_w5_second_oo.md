# Juggler W_5 second OO

Status: **W5_SECOND_OO_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The second OO after odd y on
the W_5 branch. Not Z5, not a length-11 assembler, and not a
terminal-cluster reopen.

## Branch budget

```text
Mathematical target     second-OO z/u corridor / first integer
Novelty hypothesis      n^5 for u; even z to C_2
Existing machinery      y < n^4; z fifth already named
Maximum Phase-0 scope   z/u gaps; even resets; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **W5_SECOND_OO_GREEN**
- sorry-free: `True`
- gaps: `{'w5oo_len': 31, 'w5oo_odds': 21, 'w5ooo_len': 32, 'w5ooo_odds': 22, 'z_num': 10460353203, 'z_den': 2147483648, 'u_num': 31381059609, 'u_den': 4294967296, 'z_first_integer': 5, 'u_first_integer': 8, 'z_fourth': False, 'z_fifth': True, 'z_below_generic_six': True, 'z_even_square': False, 'z_even_five_halves': True, 'z_even_cube': True, 'u_fourth': False, 'u_fifth': False, 'u_sixth': False, 'u_seventh': False, 'u_eighth': True, 'u_below_generic_nine': True, 'u_below_generic_from_z': True, 'u_even_cube': False, 'u_even_fourth': True, 'odd_u_tenth': False, 'odd_u_eleventh': True, 'rung_two_o_plus_one': False, 'even_cannot_start_l': True, 'recover_OE': False, 'recover_OOE': False, 'recover_OEE': False, 'recover_OOEE': False, 'z_fifth_under': 277065037, 'u_fifth_over': 9906223129, 'u_eighth_under': 2978678759}`
- W_5 hits in window: `0`

Odd y has next-O image z < n^{3^{21}/2^{31}} < n^5. If z is odd, u = T(z) satisfies u < n^{3^{22}/2^{32}} < n^8; the n^5 candidate fails. Even z resets below n^{5/2}; even u resets below n^4. The two-O plus-one-rung hypothesis fails. 501 never reaches W_5.

## Attack 1 — z is the first n^5 corridor

`W_5+OO` has length 31 and 21 odds, so
`z^{2147483648} <= n^{10460353203}`. The fourth-power cell
fails (`10460353203 > 8589934592`). The fifth-power cell
holds (`10460353203 < 10737418240`). Hence
`z < n^{3^{21}/2^{31}} < n^5`. Crossing `n^4` is possible,
not forced.

## Attack 2 — completed OO is not n^5

If `z` is odd, `W_5+OOO` has length 32 and 22 odds, so
`u^{4294967296} <= n^{31381059609}`. Then `n^5` fails
(`31381059609 > 21474836480`). The first surviving integer
is `n^8` (`31381059609 < 34359738368`). The ceiling still
beats generic `n^9` from `y < n^4`. Two further odds do not
raise the integer ceiling by exactly one.

## Attack 3 — even pullbacks

Even `z` returns below `n^{5/2}` (`10460353203 < 10737418240`)
and below `n^3`, not below `n^2`. Even `u` returns below `n^4`,
not below `n^3`. Neither even landing can start `L`. 501 never
follows `W_5`.

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
- generic_three_halves_only: `False`
- u_fifth_forced: `False`
- u_ge_n4_forced: `False`
- rung_two_o_plus_one: `False`
- even_new_hierarchy: `False`
- same_l_entrance: `False`
- recurrent_episode: `False`

## Decision

**W5_SECOND_OO_GREEN**

Odd y has next-O image z < n^{3^{21}/2^{31}} < n^5. If z is odd, u = T(z) satisfies u < n^{3^{22}/2^{32}} < n^8; the n^5 candidate fails. Even z resets below n^{5/2}; even u resets below n^4. The two-O plus-one-rung hypothesis fails. 501 never reaches W_5.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

