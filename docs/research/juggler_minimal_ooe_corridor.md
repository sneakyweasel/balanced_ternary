# Juggler minimal first-OO corridor OOEOOE

Status: **MINIMAL_OOE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The weakest a0=2 first-OO
prefix OOEOOE; the suffix after that prefix is not classified
beyond its first letter. Not Z5, not a length-11 assembler,
and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     CycleMin(n, OOEOOE v) =>
                        FiniteProgress or existing obstruction
Novelty hypothesis      two minimal OOE blocks from the
                        CycleMin minimum create a new constraint
Existing machinery      power_bound_word; no_cycleMin_ooeooe;
                        R(2)=0; first-even overshoot
Maximum Phase-0 scope   OOEOOE scale chain; square cell;
                        even/odd landing; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **MINIMAL_OOE_GREEN**
- sorry-free: `True`
- square-cell gap (OOE)^k: `{'1': True, '2': True, '3': True, '4': True, '5': True, '6': False}`
- square-cell gap OOE O^b E: `{'2': True, '3': True, '4': False, '5': False}`
- C expands / contracts / +1: `254` / `0` / `1`
- OOEOOE follows / x6 < n^2: `12` / `12`
- even land / even drop / odd land: `4` / `4` / `8`
- d2>d1 / reset / generic tight: `12` / `0` / `0`
- stay / hit n: `0` / `0`

T_OOEOOE(n) < n^2 so an even landing is FiniteProgress; a CycleMin prefix therefore continues with O. Odd landings exist, so OOEOOE v does not always drop.

## Attack 1 — square-cell ceiling

`power_bound_word` on `OOEOOE` is `x6^{64} <= n^{81}`.
`n^2 <= x6` would give `n^{128} <= n^{81}`, impossible for
`n >= 2`. The same comparison forbids the square cell for
`b=3` (`256 > 243`) and not for `b >= 4`.

## Attack 2 — even landing is FiniteProgress

If `x6` is even then the next letter is `E` and
`T(x6) <= n-1`. Empty `v` is already `no_cycleMin_ooeooe`.
A CycleMin prefix `OOEOOE v` therefore has `v` starting with `O`.

## Attack 3 — amplification is not the theorem

In the window every second increment exceeds the first, and
no second block resets the first surplus. The *provable* floor
is still the generic `x6 >= x3+1`. Odd landings show that the
prefix need not drop.

## Window samples

- n=`69` x3=`117` x6=`212` d1=`48` d2=`95` even=`True` steps=`1`
- n=`89` x3=`155` x6=`291` d1=`66` d2=`136` even=`False` steps=`2`
- n=`109` x3=`195` x6=`376` d1=`86` d2=`181` even=`True` steps=`1`
- n=`111` x3=`199` x6=`385` d1=`88` d2=`186` even=`False` steps=`2`
- n=`349` x3=`725` x6=`1651` d1=`376` d2=`926` even=`False` steps=`2`
- n=`365` x3=`763` x6=`1749` d1=`398` d2=`986` even=`False` steps=`9`
- n=`429` x3=`915` x6=`2145` d1=`486` d2=`1230` even=`False` steps=`6`
- n=`431` x3=`919` x6=`2156` d1=`488` d2=`1237` even=`True` steps=`1`

## Named witnesses

- n=`69` x3=`117` x6=`212` even=`True` next=`14`
- n=`89` x3=`155` x6=`291` even=`False` next=`None`

## Lean

- `CycleMin`: `True`
- `cycleMin_ge_twelve`: `True`
- `cycleMin_first_even_overshoots`: `True`
- `cycleMin_transport_second_oo`: `True`
- `cycleMin_transport_second_oo_ge`: `True`
- `power_bound_word`: `True`
- `oo_suffix_threshold`: `True`
- `no_cycleMin_ooeooe`: `True`
- `no_cycleMin_prefix_ooe_oe`: `True`
- `isolated_oe_r_max_two`: `True`

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

**MINIMAL_OOE_GREEN**

T_OOEOOE(n) < n^2 so an even landing is FiniteProgress; a CycleMin prefix therefore continues with O. Odd landings exist, so OOEOOE v does not always drop.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

