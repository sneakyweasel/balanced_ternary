# Juggler post-overshoot residual

Status: **PERSISTENT_OVERSHOOT_COUNTEREXAMPLE**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. After a first-even overshoot the
residual `y = T(z)` exceeds `n` and may be even or odd. Return
below the original start is a finite-prefix certificate, not a
proved law.

## Branch budget

```text
Mathematical target     classify post-overshoot y=T(z)>n and leftover certificates
Novelty hypothesis      even y on a CE forces n^4 ≤ z; two excursions need not return
Falsifier               even y on a CE with y < n^2; or a universal two-excursion return
Existing machinery      even_floorPower_gt_iff, even barrier, FiniteProgress, follows_append
Maximum Phase-0 scope   y>n; parity split; CE even-y scale; ReturnBelow; two-excursion census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **PERSISTENT_OVERSHOOT_COUNTEREXAMPLE**
- secondary: `[]`
- sorry-free: `True`

first post-overshoot state is classified even or odd; even y on a CE forces n^4 ≤ z; ReturnBelow is FiniteProgress when it fires; two excursions do not always return below n ([37, 77]).

## Post-overshoot census

- odd-odd overshoots: `18`
- first post-even parity: `{'even': 13, 'odd': 5}`
- first O^a E^b kinds: `{'CAPTURE': 5, 'STAY': 5, 'DESCENT': 8}`
- stay after first excursion: `[9, 37, 49, 69, 77]`
- second-excursion kinds from stay: `{'CAPTURE': 1, 'STAY': 2, 'DESCENT': 2}`
- two-excursion stay: `[37, 77]`

## Hard probes

- n=`9` z1=`140` y1=`11` parity=`odd` first=`STAY` second=`CAPTURE` z2=`36` y2=`1` below=`{'step': 5, 'value': 6}` one=`{'step': 7, 'value': 1}` min=`1` max=`140`
- n=`37` z1=`86818724` y1=`9317` parity=`odd` first=`STAY` second=`STAY` z2=`24906114455136` y2=`2233` below=`{'step': 15, 'value': 8}` one=`{'step': 17, 'value': 1}` min=`1` max=`24906114455136`
- n=`49` z1=`6352` y1=`79` parity=`odd` first=`STAY` second=`DESCENT` z2=`702` y2=`5` below=`{'step': 5, 'value': 26}` one=`{'step': 11, 'value': 1}` min=`1` max=`6352`
- n=`69` z1=`13716` y1=`117` parity=`odd` first=`STAY` second=`DESCENT` z2=`44992` y2=`3` below=`{'step': 7, 'value': 14}` one=`{'step': 14, 'value': 1}` min=`1` max=`44992`
- n=`77` z1=`2322378` y1=`1523` parity=`odd` first=`STAY` second=`STAY` z2=`59436` y2=`243` below=`{'step': 10, 'value': 21}` one=`{'step': 19, 'value': 1}` min=`1` max=`2322378`

## Lean

- `post_even_overshoot`: `True`
- `overshoot_residual_gt_start`: `True`
- `post_overshoot_parity`: `True`
- `ReturnBelow`: `True`
- `finiteProgress_of_returnBelow`: `True`
- `finiteProgress_of_oddEven_lt`: `True`
- `minimal_nonterm_no_returnBelow`: `True`
- `minimal_post_even_even_y_ge_sq`: `True`
- `minimal_post_even_even_overshoots`: `True`
- `minimal_post_even_even_z_ge_fourth`: `True`
- `minimal_first_even_dichotomy`: `True`
- `even_floorPower_gt_iff`: `True`
- certificate unchanged: `True`
- ReturnBelow distinct: `True`
- `PowerHeight` absent: `True`
- FloorPower not rewritten: `True`
- Progress spine unchanged: `True`
- no universal return-below: `True`
- no two-excursion progress theorem: `True`
- no cycle engine: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- all_odd_orbit: `False`
- finite_progress_for_all: `False`
- overshoot_is_progress: `False`
- return_below_universal: `False`
- two_excursion_always_returns: `False`
- cycle_impossible: `False`

## Decision

**PERSISTENT_OVERSHOOT_COUNTEREXAMPLE**

first post-overshoot state is classified even or odd; even y on a CE forces n^4 ≤ z; ReturnBelow is FiniteProgress when it fires; two excursions do not always return below n ([37, 77]).

This is not a halt result. Overshoot is not FiniteProgress.
Two excursions are not a general return-below theorem.

