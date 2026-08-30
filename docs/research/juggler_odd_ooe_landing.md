# Juggler odd landing after OOEOOE

Status: **ODD_OOE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The forced next O after an odd
OOEOOE landing in [n, n^2). Not Z5, not a length-11 assembler,
and not a terminal-cluster reopen.

## Branch budget

```text
Mathematical target     CycleMin(n, OOEOOE O v) =>
                        FiniteProgress or another OO
Novelty hypothesis      the next O is a controlled dichotomy
Existing machinery      OOEOOE square cell; power_bound_word;
                        cycleMin_not_end_odd
Maximum Phase-0 scope   next-O envelope; Case A/B events;
                        no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ODD_OOE_GREEN**
- sorry-free: `True`
- 243 < 256: `True`
- gaps: `{'OOEOOE': True, 'OOEOOEO': True, 'OOEOOEOE': True, 'OOEOOEOOE': True, 'OOEOOEOO': False}`
- Case A / B: `4` / `4`
- A drop / survive: `4` / `0`
- z >= n^2 / cube fail: `0` / `0`
- second OOE below n^2: `3` / `3`
- OOO / escape n^2: `1` / `1`
- first events: `{'even_drop': 4, 'second_ooe': 3, 'ooo_b9': 1}`

after an odd OOEOOE landing, x^3 < n^4 so z < n^2; even z drops on the next E; odd z starts another OO. A later OOO run can escape n^2, so the ceiling is not eternal.

## Attack 1 — next-O envelope

`power_bound_word` on `OOEOOE` is `x^{64} <= n^{81}`. Then
`x^{192} <= n^{243}`. For `n >= 2`, `n^{243} < n^{256}`, so
`x^3 < n^4`. The next odd image `z = floor(x^{3/2})` satisfies
`z^2 <= x^3 < n^4`, hence `z < n^2`. The word `OOEOOEO` has
the same square-cell gap (`256 > 243`).

## Attack 2 — Case A / Case B

If `z` is even, the next letter is `E` and `T(z) <= n-1`.
If `z` is odd, the next letter is `O`, so another `OO` has
started. Empty continuation after the forced `O` is forbidden
by `cycleMin_not_end_odd`.

## Attack 3 — the ceiling is not eternal

A second completed `OOE` stays below `n^2` (`1024 > 729`).
A later long odd run can escape `n^2`. That is a residual,
not the dichotomy.

## Window samples

- n=`89` x=`291` z=`4964` case=`A` first=`even_drop`
- n=`111` x=`385` z=`7554` case=`A` first=`even_drop`
- n=`349` x=`1651` z=`67084` case=`A` first=`even_drop`
- n=`365` x=`1749` z=`73145` case=`B` first=`second_ooe`
- n=`429` x=`2145` z=`99343` case=`B` first=`second_ooe`
- n=`565` x=`3039` z=`167531` case=`B` first=`ooo_b9`
- n=`637` x=`3537` z=`210354` case=`A` first=`even_drop`
- n=`763` x=`4447` z=`296551` case=`B` first=`second_ooe`

## Named witnesses

- n=`89` x=`291` z=`4964` case=`A` first=`even_drop`
- n=`111` x=`385` z=`7554` case=`A` first=`even_drop`
- n=`365` x=`1749` z=`73145` case=`B` first=`second_ooe`
- n=`565` x=`3039` z=`167531` case=`B` first=`ooo_b9`

## Lean

- `CycleMin`: `True`
- `cycleMin_ge_twelve`: `True`
- `cycleMin_not_end_odd`: `True`
- `power_bound_word`: `True`
- `no_cycleMin_ooeooe`: `True`
- `oo_suffix_threshold`: `True`

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

**ODD_OOE_GREEN**

after an odd OOEOOE landing, x^3 < n^4 so z < n^2; even z drops on the next E; odd z starts another OO. A later OOO run can escape n^2, so the ceiling is not eternal.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler. Terminal clusters stay frozen.

