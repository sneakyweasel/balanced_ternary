# Juggler no-progress path structure

Status: **NO_PROGRESS_STRUCTURE_GREEN**

Standalone application phase. Not a Research Engine experiment and
not a termination theorem. Phase A is already `minimal_avoids_progress`.
A hypothetical minimal non-1 orbit avoids every `ReachesOne` state,
not only `[1, n)`.

## Branch budget

```text
Mathematical target     Necessary C on a long NO_CERTIFICATE prefix
Novelty hypothesis      Collapse-without-capture is ReachesOne or descent
Falsifier               Large even collapse to m>1 with no certificate
Existing machinery      minimal_avoids_progress, ReachesOne closure
Maximum Phase-0 scope   Census plus cheap ReachesOne wrappers
```

## Metadata

- basin: `[1]`
- cheap ReachesOne: `[1, 2, 4, 6, 8]`
- engine control layer modified: `False`
- classification: **NO_PROGRESS_STRUCTURE_GREEN**
- sorry-free: `True`

orbit avoids every ReachesOne state; even prefixes at n>=2 are descent; landing at 2,4,6,8 is ReachesOne-implied even when the image is at least n (OOE at 5 lands at 6); no defect reset.

## Annotated prefixes

- n=`3` word=`OOOEE` first_progress=`DESCENT` image=`2` path=`[3, 5, 11, 36, 6, 2]`
- n=`7` word=`OE` first_progress=`DESCENT` image=`4` path=`[7, 18, 4]`
- n=`13` word=`OE` first_progress=`DESCENT` image=`6` path=`[13, 46, 6]`
- n=`41` word=`OE` first_progress=`DESCENT` image=`16` path=`[41, 262, 16]`

## Collapse-without-capture

- even starts whose first step is already progress: `40/40`
- descent collapses: `78`
- reaches-one collapses: `2`
- extra-constraint (NO_CERTIFICATE image, cheap ReachesOne): `2`
- uncertified y>=n: `23`
- large collapse with delayed short-suffix progress: `1` (observation; not a refutation of ReachesOne-avoidance)

- minimized extra constraint: n=`3` word=`OOOE` `36 --E^1--> 6` kind=`NO_CERTIFICATE`
- minimized uncertified y>=n: n=`9` word=`OOE` `140 --E^1--> 11` kind=`NO_CERTIFICATE`
- largest-ratio uncertified y>=n: n=`37` word=`OOOOEOOOEE` `24906114455136 --E^2--> 2233` kind=`NO_CERTIFICATE`

## Defect reset

- orbits with a positive deficit: `75`
- resets to 0 after a first positive defect: `0`

No persistent-defect object is introduced. Existing strict
power-bound continuation already forbids a return to equality.

## Lean

- `two_reachesOne`: `True`
- `four_reachesOne`: `True`
- `six_reachesOne`: `True`
- `eight_reachesOne`: `True`
- `image_two_reachesOne`: `True`
- `image_four_reachesOne`: `True`
- `image_six_reachesOne`: `True`
- `image_eight_reachesOne`: `True`
- `reachesOne_of_image`: `True`
- `minimal_avoids_reachesOne_image`: `True`
- `even_word_descent`: `True`
- `minimal_odd_start`: `True`
- `minimal_avoids_progress`: `True`
- `reachesOne_of_iterate`: `True`
- `even_word_contracts`: `True`
- `floorPower_two`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- no `no_progress_prefix` type: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`

## Decision

**NO_PROGRESS_STRUCTURE_GREEN**

orbit avoids every ReachesOne state; even prefixes at n>=2 are descent; landing at 2,4,6,8 is ReachesOne-implied even when the image is at least n (OOE at 5 lands at 6); no defect reset.

This is not a halt result.

