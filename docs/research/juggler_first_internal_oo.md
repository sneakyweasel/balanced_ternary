# Juggler first internal OO after isolated OE transport

Status: **FIRST_OO_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. First internal `OO` after
first-even overshoot and isolated `OE` transport; the suffix
after that `OO` is not classified. Not Z5, not a length-11
assembler, and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     first-even overshoot + isolated OE
                        + first OO => FiniteProgress or
                        existing obstruction, or a bound on r
Novelty hypothesis      first OO creates an irreversible
                        return-cost surplus
Existing machinery      power_bound_word; repeated_oe_scale;
                        first-even overshoot; oe_block_contracts
Maximum Phase-0 scope   first-OO decomposition; r-bound;
                        forward geometry; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **FIRST_OO_GREEN**
- sorry-free: `True`
- R(a0): `{'2': 0, '3': 1, '4': 3, '5': 4, '6': 6, '7': 7, '8': 8, '9': 10, '10': 11, '11': 13, '12': 14}`
- isolated starts / first-OO events: `99` / `52`
- exceed R: `0`
- a0=2 events / nonzero r: `23` / `0`
- r counts: `{'0': 46, '1': 6}`
- drop below n / stay / hit n: `52` / `0` / `0`
- OOE landing >= n / < n: `26` / `0`
- T^2 > (xj+1)^2 / tight: `52` / `0`
- x1 even (outside corridor): `101`

B^r(x1) >= n after O^{a0}E forces 2^{2r+a0+1} <= 3^{a0+r}, so r <= R(a0) with R(2)=0; the first-OO dichotomy and the irreversible-surplus claim are not theorems.

## Attack 1 — isolated-OE r-bound

If `O^{a0}E` follows at `n` and `(OE)^r` follows at the
first-even landing `x1`, and `B^r(x1) >= n`, then
`2^{2r+a0+1} <= 3^{a0+r}`. In particular `R(2)=0`:
a CycleMin-shaped `a0=2` prefix cannot complete one `OE`
after the first even while staying `>= n`.

## Attack 2 — first-OO geometry

On odd `13 <= n < 801` the isolated corridor has
`52` first-OO events, all with `r <= R(a0)`,
all dropping below `n`, none returning to `n`.
Drop prefixes: `{'OOOE': 15, 'OOEE': 13, 'OOEO': 13, 'OOOO': 11}`.

## Attack 3 — surplus falsifiers

Immediate kill is false: `n=193` stays 66 steps after its
first `OO`. `OOE` itself lands `>= n` on every `b=2` event
in the window. Families with `r >= 2` exist and still obey
`r <= R(a0)`; `r -> infinity` with `xj >= n` is false.

## Window samples

- n=`37` a0=`4` r=`0` b=`3` steps=`10` drop=`OOOEEOOEEE`
- n=`69` a0=`2` r=`0` b=`2` steps=`4` drop=`OOEE`
- n=`77` a0=`3` r=`1` b=`2` steps=`4` drop=`OOEE`
- n=`89` a0=`2` r=`0` b=`2` steps=`5` drop=`OOEOE`
- n=`99` a0=`3` r=`0` b=`2` steps=`4` drop=`OOEE`
- n=`103` a0=`4` r=`1` b=`3` steps=`6` drop=`OOOEEE`
- n=`105` a0=`2` r=`0` b=`3` steps=`5` drop=`OOOEE`
- n=`109` a0=`2` r=`0` b=`2` steps=`4` drop=`OOEE`

## Named r>=2 witnesses

- n=`2155` a0=`5` r=`2` b=`2` xj/n=`6.11e+03` steps=`10` drop=`OOEOOOEEEE`
- n=`2503` a0=`4` r=`2` b=`2` xj/n=`27.6` steps=`4` drop=`OOEE`
- n=`2985` a0=`9` r=`2` b=`2` xj/n=`1.25e+34` steps=`13` drop=`OOEEOOOEEOEE`

## Lean

- `CycleMin`: `True`
- `cycleMin_ge_twelve`: `True`
- `cycleMin_first_even_overshoots`: `True`
- `cycleMin_transport_second_oo`: `True`
- `oe_block_contracts`: `True`
- `oe_block_scale`: `True`
- `repeated_oe_scale`: `True`
- `power_bound_word`: `True`

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

## Decision

**FIRST_OO_GREEN**

B^r(x1) >= n after O^{a0}E forces 2^{2r+a0+1} <= 3^{a0+r}, so r <= R(a0) with R(2)=0; the first-OO dichotomy and the irreversible-surplus claim are not theorems.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

