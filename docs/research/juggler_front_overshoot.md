# Juggler front overshoot versus short-cluster undershoot

Status: **FRONT_OVERSHOOT_PARK**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. First-even overshoot plus a later
`OO` against a bunched-short last cluster; not Z5, not a
length-11 assembler, and not a leftover-suffix retest.

## Branch budget

```text
Mathematical target     Can one internal OO after first-even
                        overshoot raise the state above every
                        cell from which a bunched-short tail
                        can still undershoot on a CycleMin?
Novelty hypothesis      first-even overshoot + later OO
                        permanently raises the return floor
Existing machinery      first-even overshoot; second-OO
                        transport; seven short last clusters
Maximum Phase-0 scope   front-to-back geometry; exact-return
                        cells; Case A/B words; no Lean
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **FRONT_OVERSHOOT_PARK**
- sorry-free: `True`
- weak floor compatible with all seven tails: `True`
- Case A OO events (n<201, a0<=7): `11`
- Case A vs EE: `{'above': 1, 'below': 10}`
- Case A vs EEE: `{'below': 11}`
- Case A never inside EE: `True`
- Case A never inside EEE: `True`
- Case A raise-above EEE uniform: `False`
- weak floor always below EE: `False`
- EEE scan OO events (n<501, a0<=8): `31`
- EEE scan vs EEE: `{'below': 27, 'above': 4}`
- EEE never inside: `True`
- Case A e=4 follows / stay / cycles / interval: `8` / `1` / `0` / `1`
- Case B e=5 follows / stay / cycles / interval: `4` / `0` / `0` / `0`
- diagnostic leaks: `4` later-OO `3` inside-tail `1` cycles `0`
- shared leak geometry: `False`
- parked suffix witnesses below n^2: `True`

the prefix-independent OO transport floor (n+2)^2 sits below every short-tail exact-return cell, so the same front lower bound is compatible with all seven families; T_OO(first-even y) is never inside the EEE cell in the scan (below for small a0, above for large) and no exact Case A/B return appears, but three interval leaks with later OO do not share a cell depth and the raise-above invariant is false.

## Attack 1 — first internal OO

The strongest prefix-independent lower bound after the first
internal `OO` is the existing transport `(y+1)^2` with `y>n`,
hence at least `(n+2)^2`. That sits below every exact-return
cell of remaining `E O^b E O^c E`.

Case A `T_OO` versus `[n^4,(n+1)^4)`: `{'above': 1, 'below': 10}`.
Case A `T_OO` versus `[n^8,(n+1)^8)`: `{'below': 11}`.
Weak floor versus EE: `{'above': 1, 'below': 10}`.

## Attack 2 — terminal cells

Remaining outer scales (real-power, not a preimage table):

- remaining `0,0`: `n^8/1`
- remaining `1,0`: `n^16/3`
- remaining `2,0`: `n^32/9`
- remaining `3,0`: `n^64/27`
- remaining `0,1`: `n^16/3`
- remaining `1,1`: `n^32/9`
- remaining `2,1`: `n^64/27`

No Case A start in the scan maps remaining `E+tail` exactly to `n`.
Exact remaining hits: `0`.

## Attack 3 — cell depth

`r(x,n) = max{r : x >= (n+r)^2}`, or `-1` if `x < n^2`.
Parked suffix witnesses all enter below `n^2`. Later-OO leaks
do not share a post-`OO` depth.

- witness start depths: `{'-1': 18}`
- leak post-OO depths: `{'29166': 1, '7782': 1, '86346': 1}`

## Attack 5 — Case A / B / C

Case A is the earliest internal `OO`. Case B words in the
e=5 window give `0` cycles and `0` interval hits.

## Attack 6 — diagnostic witnesses

The 18 parked suffix returns all start below the CycleMin
square. They are not CycleMin fronts. The four interval leaks
from the predecessor census, rescored here:

- n=`37` word=`OOOOEOOOEEOOEE` img=`76` y0=`9317` case=`A` depth_w=`29166` interval=`True`
- n=`103` word=`OOOOEOEOOOEE` img=`1674` y0=`124381` case=`inside_tail` depth_w=`19789` interval=`True`
- n=`113` word=`OOOEOOOOOEEE` img=`1942` y0=`2913` case=`A` depth_w=`7782` interval=`True`
- n=`205` word=`OOOOEOEOOEOOEE` img=`598` y0=`710537` case=`B` depth_w=`86346` interval=`True`

## Lean

- `CycleMin`: `True`
- `cycleMin_ge_twelve`: `True`
- `cycleMin_first_even_overshoots`: `True`
- `cycleMin_transport_second_oo`: `True`
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

**FRONT_OVERSHOOT_PARK**

the prefix-independent OO transport floor (n+2)^2 sits below every short-tail exact-return cell, so the same front lower bound is compatible with all seven families; T_OO(first-even y) is never inside the EEE cell in the scan (below for small a0, above for large) and no exact Case A/B return appears, but three interval leaks with later OO do not share a cell depth and the raise-above invariant is false.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler.

