# Juggler bunched-short predecessor cells

Status: **BUNCHED_SHORT_FRONT_PARK**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Predecessor cells at `y = T_u(n)`
for bunched-short last clusters; not Z5, not a length-11
assembler, and not a four-even leftover cell.

## Branch budget

```text
Mathematical target     Does every CycleMin short tail force
                        a predecessor cell disjoint from the
                        backward-feasible cell of that tail?
Novelty hypothesis      one two-cluster / cell-intersection
                        obstruction, not seven terminal maps
Falsifier               a CycleMin front whose short tail
                        stays in [n, y]; or no finite geometry
Existing machinery      CycleMin overshoot and transport;
                        trailing-even cells; 18-return family
Maximum Phase-0 scope   re-root lemma; S_{b,c} cells; censuses
                        A/B; no Lean, no Z5, no length-11
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **BUNCHED_SHORT_FRONT_PARK**
- sorry-free: `True`
- reroot forbidden suffixes: `0`
- window reroot forbidden: `0`
- short-tail interval hits below 256: `197`
- short-tail overshoots: `0`
- (3,1) unique expanding in rectangle: `True`
- n>=12 returns: `18`
- even-n returns: `11`
- CycleMin-feasible known returns: `0`
- census-B follows: `24`
- census-B survivors: `4`
- census-B cycles: `0`
- census-B clusters: `4`
- shared predecessor/cell geometry: `False`
- all leaks S>n: `True`
- all leaks c=0: `True`

the 18 leftover-suffix returns are predecessor-infeasible and no CycleMin word u ++ O^b E O^c E appears below 256, but four interval leaks with S > n scatter across predecessor types and ranks; trailing-even overflow is equivalent to S >= n+1, not a new cell; no single empty cell-intersection kills the class.

## Attack 1 — re-root

Every even-landing suffix of a bunched-short word keeps the same last cluster (b,c) and the same last three-even gap a < a_min, or is shorter than three evens. None is an excluded leftover.

Short-spec forbidden suffixes: `0`. Expanding-window forbidden suffixes: `0`.

## Attack 5 — missing (3,1)

`(3,1)` is `O^3 EOE`, already `no_cycleMin_prefix_two_even_eoe`. It is the unique pair in `{0,1,2,3} x {0,1}` with `3^{b+c} > 2^{b+c+2}`. The seven survivors are exactly the contracting pairs. `Q` increases toward the leftover threshold and therefore does not obstruct the short tails.

## Census A — known n>=12 returns

- pred types: `{'a_ge2': 15, 'a1': 3}`
- enter ranks: `{'0': 13, '19': 1, '25': 1, '28': 1, '10057': 1, '25226': 1}`

- `OOOOOEEE` y3=`129` n=`100` enter=`103162534` pred=`a_ge2` odd=`False` feasible=`False`
- `OOOOOEEE` y3=`209` n=`159` enter=`644363658` pred=`a_ge2` odd=`True` feasible=`False`
- `OOOEOEE` y3=`81` n=`16` enter=`1661` pred=`a_ge2` odd=`False` feasible=`False`
- `OOOEOEE` y3=`87` n=`16` enter=`1873` pred=`a_ge2` odd=`False` feasible=`False`
- `OOEOOEE` y3=`69` n=`14` enter=`117` pred=`a_ge2` odd=`False` feasible=`False`
- `OOEOOEE` y3=`109` n=`19` enter=`195` pred=`a_ge2` odd=`True` feasible=`False`
- `OOOEOOEE` y3=`99` n=`78` enter=`2331` pred=`a_ge2` odd=`False` feasible=`False`
- `OOOEOOEE` y3=`247` n=`186` enter=`10903` pred=`a_ge2` odd=`False` feasible=`False`
- `OEOOOEE` y3=`135` n=`21` enter=`39` pred=`a1` odd=`True` feasible=`False`
- `OEOOOEE` y3=`231` n=`31` enter=`59` pred=`a1` odd=`True` feasible=`False`
- `OEOOOEE` y3=`233` n=`31` enter=`59` pred=`a1` odd=`True` feasible=`False`
- `OOEOOOEE` y3=`105` n=`82` enter=`187` pred=`a_ge2` odd=`False` feasible=`False`
- `OOOEEOE` y3=`59` n=`13` enter=`972` pred=`a_ge2` odd=`True` feasible=`False`
- `OOEOEOE` y3=`97` n=`17` enter=`171` pred=`a_ge2` odd=`True` feasible=`False`
- `OOEOEOE` y3=`137` n=`22` enter=`253` pred=`a_ge2` odd=`False` feasible=`False`
- `OOEOEOE` y3=`157` n=`24` enter=`295` pred=`a_ge2` odd=`False` feasible=`False`
- `OOEOOEOE` y3=`89` n=`70` enter=`155` pred=`a_ge2` odd=`False` feasible=`False`
- `OOEOOEOE` y3=`111` n=`86` enter=`199` pred=`a_ge2` odd=`False` feasible=`False`

## Census B — CycleMin-shaped fronts

- pred types: `{'a0': 1, 'a1': 1, 'a_ge2': 2}`
- ranks: `{'0': 1, '11': 1, '90': 1, '3774164': 1}`
- pairs: `{'0,0': 1, '2,0': 2, '3,0': 1}`

- pred=`a0` (b,c)=`(2,0)` rank=`11` count=`1`
- pred=`a1` (b,c)=`(3,0)` rank=`0` count=`1`
- pred=`a_ge2` (b,c)=`(0,0)` rank=`3774164` count=`1`
- pred=`a_ge2` (b,c)=`(2,0)` rank=`90` count=`1`

### Survivor samples

- n=`37` y=`2233` s=`76` u=`OOOOEOOOEE` tail=`O^2EO^0E` rank=`11`
- n=`103` y=`6623` s=`1674` u=`OOOOEOE` tail=`O^3EO^0E` rank=`0`
- n=`113` y=`14245160192996` s=`1942` u=`OOOEOOOOOE` tail=`O^0EO^0E` rank=`3774164`
- n=`205` y=`86551` s=`598` u=`OOOOEOEOOE` tail=`O^2EO^0E` rank=`90`

### Leak geometry

Trailing-even overflow `z >= (n+1)^4` holds on every `c=0` leak and is equivalent to `S >= n+1`. It is not a new cell.

- n=`37` s=`76` z=`34276462` overflow=`True` eq_S=`True`
- n=`103` s=`1674` z=`7871516405498` overflow=`True` eq_S=`True`
- n=`113` s=`1942` z=`14245160192996` overflow=`True` eq_S=`True`
- n=`205` s=`598` z=`128487885014` overflow=`True` eq_S=`True`

## Lean

- `CycleMin`: `True`
- `cycleMin_ge`: `True`
- `cycleMin_ge_twelve`: `True`
- `cycleMin_first_even_overshoots`: `True`
- `cycleMin_transport_second_oo`: `True`
- `cycle_trailing_evens_lt`: `True`
- `cycle_last_odd_interval`: `True`
- `oe_block_contracts`: `True`
- `no_cycleMin_prefix_two_even_eoe`: `True`
- `no_cycleMin_prefix_eee`: `True`

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

**BUNCHED_SHORT_FRONT_PARK**

the 18 leftover-suffix returns are predecessor-infeasible and no CycleMin word u ++ O^b E O^c E appears below 256, but four interval leaks with S > n scatter across predecessor types and ranks; trailing-even overflow is equivalent to S >= n+1, not a new cell; no single empty cell-intersection kills the class.

This is not a halt result, not a Z5 exclusion, and not a
length-11 assembler.

