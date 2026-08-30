# Juggler isolated-odd prefixes versus the exact short-tail fibre

Status: **ISO_FIBRE_PARK**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Isolated-odd CycleMin prefixes
into the exact (eps, eta) fibre; not Z5, not a length-11
assembler, and not a four-even leftover cell.

## Branch budget

```text
Mathematical target     Can an isolated-odd CycleMin prefix
                        land in the exact short-tail fibre?
Novelty hypothesis      isolated-odd transport cannot hit
                        the fibre while staying >= n
Existing machinery      EE identity; first-even overshoot;
                        oe_block_contracts
Maximum Phase-0 scope   e=5,6 isolated-odd words; exact
                        tail return; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ISO_FIBRE_PARK**
- sorry-free: `True`
- four-even excluded: `True`
- words: `588` by evens `{'5': 196, '6': 392}`
- follows: `34`
- stay >= n: `0`
- fibre hits: `0`
- CycleMin exact: `0`
- fibre with dip below n: `0`
- pairs: `{}`
- follows by a0: `{'2': 21, '3': 10, '5': 3}`

no isolated-odd e=5,6 prefix landed in the exact short-tail fibre on 13 <= n < 151; the 34 follows all drop below n (a0 in {2,3,5}) by isolated OE/EE contraction, so they are not CycleMin; that is a finite empty window, not a transport theorem, and e=4 stays the parked four-even cell.

## Follows that are not CycleMin

- n=`25` word=`OOOEEOEOEE` a0=`3` y0=`228` y=`7` min=`2` stay=`False`
- n=`25` word=`OOOEEOEOEEE` a0=`3` y0=`228` y=`4` min=`1` stay=`False`
- n=`33` word=`OOEEOEEE` a0=`2` y0=`50` y=`4` min=`1` stay=`False`
- n=`35` word=`OOEEOEEE` a0=`2` y0=`54` y=`4` min=`1` stay=`False`
- n=`39` word=`OOOEEOEOOEOE` a0=`3` y0=`482` y=`9` min=`6` stay=`False`
- n=`49` word=`OOEOEEOOEE` a0=`2` y0=`79` y=`5` min=`2` stay=`False`
- n=`59` word=`OOOEEOEOEE` a0=`3` y0=`972` y=`13` min=`2` stay=`False`
- n=`59` word=`OOOEEOEOEEE` a0=`3` y0=`972` y=`6` min=`1` stay=`False`
- n=`73` word=`OOEEOEEE` a0=`2` y0=`124` y=`6` min=`1` stay=`False`
- n=`75` word=`OOOEEEEE` a0=`3` y0=`1458` y=`6` min=`1` stay=`False`
- n=`81` word=`OOOEOEEEE` a0=`3` y0=`1661` y=`16` min=`2` stay=`False`
- n=`81` word=`OOOEOEEEEE` a0=`3` y0=`1661` y=`4` min=`1` stay=`False`

## Fibre hits

None in the window.

## Lean

- `CycleMin`: `True`
- `cycleMin_ge_twelve`: `True`
- `cycleMin_first_even_overshoots`: `True`
- `oe_block_contracts`: `True`

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

**ISO_FIBRE_PARK**

no isolated-odd e=5,6 prefix landed in the exact short-tail fibre on 13 <= n < 151; the 34 follows all drop below n (a0 in {2,3,5}) by isolated OE/EE contraction, so they are not CycleMin; that is a finite empty window, not a transport theorem, and e=4 stays the parked four-even cell.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler.

