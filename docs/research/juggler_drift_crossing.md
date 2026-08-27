# Juggler first positive-drift crossing and endpoint arithmetic

Status: **DRIFT_ENDPOINT_COMPLEX**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Walks actual orbits until the
first G_k = 2^k - 3^{o_k} > 0. Does not claim tau_+ < infinity.
Does not reopen prefix-NC word admissibility, the corridor,
escape-state margins, ResidualStep, or odd-fourth-power.

## Branch budget

```text
Mathematical target     If an actual orbit stays prefix-NC through k,
                        what new arithmetic is forced on x_k?
Novelty hypothesis      long NC survival forces an endpoint
                        filtration not implied by G or T>=n
Falsifier               every endpoint predicate is G-recurrence or T>=n
Existing machinery      power_bound_*, exponent_gap, first-defect,
                        square_depth, floor_power
Maximum Phase-0 scope   one probe; actual orbits until first G>0; no Lean
```

## Metadata

- search_id: `juggler-drift-crossing-phase0-n2-2000`
- algorithm_version: `drift-crossing-v1`
- window: `n=2..2000`
- horizon: `10000` (not L)
- bit_cap: `4096`
- crossing_policy: `stop at first G_k>0; absorb if T^k=1 still NC`
- engine control layer modified: `False`
- classification: **DRIFT_ENDPOINT_COMPLEX**
- secondary: `['DRIFT_FIRST_CROSSING_GREEN']`
- sorry-free: `True`

the only exact crossing law is the G-recurrence (first positive G is an even letter); mixed prefix-NC endpoints keep both parities, both gcd regimes, and both square statuses, so no new endpoint filtration survives.

## Census

- starts: `1999`
- crossed: `1999`
- absorbed at 1 still NC: `0`
- unfinished: `0`
- identity failures: `0`
- even tau_+ failures: `0`
- G = 0 hits: `0`
- NC prefixes: `4812`
- mixed NC prefixes: `2797`
- monochrome NC prefixes: `2015`
- max tau_+: `70`
- max NC k: `69`
- max peak bits: `900`
- mixed gcd > 1: `493`
- mixed gcd = 1: `2304`
- crossing predecessor square: `31`
- crossing predecessor not square: `1968`
- filtration shrink notes: `11`

## tau_+ histogram

- tau_+ = `1`: `1000`
- tau_+ = `2`: `494`
- tau_+ = `4`: `124`
- tau_+ = `5`: `126`
- tau_+ = `7`: `46`
- tau_+ = `8`: `54`
- tau_+ = `10`: `19`
- tau_+ = `12`: `18`
- tau_+ = `13`: `26`
- tau_+ = `15`: `11`
- tau_+ = `16`: `15`
- tau_+ = `18`: `11`
- tau_+ = `20`: `3`
- tau_+ = `21`: `7`
- tau_+ = `23`: `7`
- tau_+ = `24`: `11`
- tau_+ = `26`: `5`
- tau_+ = `27`: `6`
- tau_+ = `29`: `2`
- tau_+ = `31`: `1`
- tau_+ = `32`: `2`
- tau_+ = `35`: `2`
- tau_+ = `37`: `1`
- tau_+ = `40`: `1`
- tau_+ = `43`: `1`
- tau_+ = `46`: `1`
- tau_+ = `50`: `2`
- tau_+ = `51`: `1`
- tau_+ = `62`: `1`
- tau_+ = `70`: `1`

## Closest NC gaps (largest G <= 0)

- n=`3` k=`1` G=`-1` o=`1` word=`O` x_bits=`3` mixed=`False` gcd=`1`
- n=`5` k=`1` G=`-1` o=`1` word=`O` x_bits=`4` mixed=`False` gcd=`1`
- n=`7` k=`1` G=`-1` o=`1` word=`O` x_bits=`5` mixed=`False` gcd=`1`
- n=`9` k=`1` G=`-1` o=`1` word=`O` x_bits=`5` mixed=`False` gcd=`9`
- n=`11` k=`1` G=`-1` o=`1` word=`O` x_bits=`6` mixed=`False` gcd=`1`
- n=`13` k=`1` G=`-1` o=`1` word=`O` x_bits=`6` mixed=`False` gcd=`1`
- n=`15` k=`1` G=`-1` o=`1` word=`O` x_bits=`6` mixed=`False` gcd=`1`
- n=`17` k=`1` G=`-1` o=`1` word=`O` x_bits=`7` mixed=`False` gcd=`1`
- n=`19` k=`1` G=`-1` o=`1` word=`O` x_bits=`7` mixed=`False` gcd=`1`
- n=`21` k=`1` G=`-1` o=`1` word=`O` x_bits=`7` mixed=`False` gcd=`3`
- n=`23` k=`1` G=`-1` o=`1` word=`O` x_bits=`7` mixed=`False` gcd=`1`
- n=`25` k=`1` G=`-1` o=`1` word=`O` x_bits=`7` mixed=`False` gcd=`25`

## Longest crossings

- n=`193` tau_+=`70` word=`OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOOOEOOOOEEOOEOOEOEEOOEOOEEOEEEE` o=`44` G=`195820718533800070543` pred_bits=`13` letter=`E`
- n=`761` tau_+=`62` word=`OOOOOOOOOEEOEOEEOOEEOOOEOOOOEOOOEOEOOOEEOOOOEOOOOEEEOOOEEEEOEE` o=`39` G=`559130865408411637` pred_bits=`17` letter=`E`
- n=`1773` tau_+=`51` word=`OOOOOOOEOOOEOEEOOOOEEEOEOOEOOEOOOEOEEEOOEOOEOOOOEEE` o=`32` G=`398779624833407` pred_bits=`18` letter=`E`
- n=`1181` tau_+=`50` word=`OOEOOOEOOOOOEOEEOOEOOOEEOOOEOOOEEOEOOEOOOEOEOEOEEE` o=`31` G=`508226510558677` pred_bits=`12` letter=`E`
- n=`1721` tau_+=`50` word=`OOOOEOOOOOOEEOEOEOOOOOEOOEOOEEOOEOOOEEEEOOOOEOEEEE` o=`31` G=`508226510558677` pred_bits=`12` letter=`E`
- n=`425` tau_+=`46` word=`OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE` o=`29` G=`1738366812781` pred_bits=`18` letter=`E`
- n=`293` tau_+=`43` word=`OOOOOOOOEEEOOOOOEOEOOOOOEEEEOOEOOEOEOEOEOEE` o=`27` G=`1170495537221` pred_bits=`15` letter=`E`
- n=`807` tau_+=`40` word=`OOOEOOEOOOOOOOOOEOEEOEOEOEOOOEOOEOEOEEEE` o=`25` G=`252223018333` pred_bits=`15` letter=`E`
- n=`1123` tau_+=`37` word=`OOOEOOOEOOEOOOEEEOEOOOOOOEEOOOEEOOEEE` o=`23` G=`43295774645` pred_bits=`14` letter=`E`
- n=`805` tau_+=`35` word=`OOOEOOOOEOEOOOOOEOOEEOEEEOOOOOEEEOE` o=`22` G=`2978678759` pred_bits=`18` letter=`E`
- n=`899` tau_+=`35` word=`OOOOOEOEOOOEOOOEOOOEOOEOOEEOEOEEOEE` o=`22` G=`2978678759` pred_bits=`18` letter=`E`
- n=`1011` tau_+=`32` word=`OOOOEEOOEOOOOOOOEOOEEEOEOEOOEOEE` o=`20` G=`808182895` pred_bits=`17` letter=`E`

## Hard starts

- n=`9` status=`CROSSED` tau_+=`5` word=`OOEOE` peak_bits=`8` pred_even=`True`
- n=`37` status=`CROSSED` tau_+=`15` word=`OOOOEOOOEEOOEEE` peak_bits=`45` pred_even=`True`
- n=`49` status=`CROSSED` tau_+=`5` word=`OOEOE` peak_bits=`13` pred_even=`True`
- n=`69` status=`CROSSED` tau_+=`7` word=`OOEOOEE` peak_bits=`16` pred_even=`True`
- n=`77` status=`CROSSED` tau_+=`10` word=`OOOEOEOOEE` peak_bits=`22` pred_even=`True`
- n=`173` status=`CROSSED` tau_+=`26` word=`OOEOOOOOOOOEOOEOOEEOEEOEEE` peak_bits=`272` pred_even=`True`

## Tall starts

- n=`193` status=`CROSSED` tau_+=`70` word=`OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOOOEOOOOEEOOEOOEOEEOOEOOEEOEEEE` peak_bits=`900`
- n=`557` status=`CROSSED` tau_+=`27` word=`OOOOOEOOOOOOOOEOEOEEEOEEOEE` peak_bits=`888`
- n=`761` status=`CROSSED` tau_+=`62` word=`OOOOOOOOOEEOEOEEOOEEOOOEOOOOEOOOEOEOOOEEOOOOEOOOOEEEOOOEEEEOEE` peak_bits=`851`

## Mixed-NC invariant hits

- `x_even`: `1428` / `2797`
- `x_odd`: `1369` / `2797`
- `x_square`: `8` / `2797`
- `x_not_square`: `2789` / `2797`
- `v2_ge_1`: `1428` / `2797`
- `v3_ge_1`: `938` / `2797`
- `gcd_gt_1`: `493` / `2797`
- `gcd_eq_1`: `2304` / `2797`
- `square_depth_ge_1`: `8` / `2797`
- `mod8_0`: `363` / `2797`
- `mod8_1`: `317` / `2797`
- `mod8_4`: `371` / `2797`
- `mod9_0`: `344` / `2797`
- `image_ge_n`: `2797` / `2797`

## Lean

- `power_bound_word`: `True`
- `power_bound_contracts`: `True`
- `power_bound_eq_iff_extremal`: `True`
- `power_bound_compensated_contracts`: `True`
- new DriftCrossing file absent: `True`
- ResidualStep not extended: `True`
- CycleDiophantine not rewritten: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- search_horizon_is_L: `False`
- tau_plus_finite: `False`
- endpoint_invariant_is_T_ge_n: `False`
- new_parity_grammar: `False`

## Decision

**DRIFT_ENDPOINT_COMPLEX**

the only exact crossing law is the G-recurrence (first positive G is an even letter); mixed prefix-NC endpoints keep both parities, both gcd regimes, and both square statuses, so no new endpoint filtration survives.

A finite tau_+ on this window is not tau_+ < infinity.
A search-horizon miss is not a bound L. Do not claim termination.

