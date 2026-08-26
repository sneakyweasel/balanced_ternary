# Juggler odd-to-odd first-even residual

Status: **FIRST_EVEN_RESIDUAL_CLASSIFIED**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. An even residual `z` of an odd
start `n` is below `n^2`, in the return cell, or an overshoot.
A `MinimalNonTerm` start cannot close on the first `O^a E`.

## Branch budget

```text
Mathematical target     classify the first even residual of an odd-to-odd start
Novelty hypothesis      CE first O^a E is a cycle candidate or overshoot
Falsifier               below-n^2 on a CE, or first O^a E Descent on a CE
Existing machinery      even barrier, square-cell inverse, FiniteProgress, oddEvenBlock
Maximum Phase-0 scope   trichotomy; CE dichotomy; FiniteProgress if z<n^2; census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **FIRST_EVEN_RESIDUAL_CLASSIFIED**
- secondary: `['ODD_ODD_COUNTEREXAMPLE_CLASS']`
- sorry-free: `True`

first even residual is below n^2, return-to-n, or overshoot; a MinimalNonTerm start cannot Descent or Capture on the first O^a E; the window is all overshoot.

## Residual census

- odd-odd starts: `18`
- below n^2: `0`
- return cell: `0`
- overshoot: `18`
- post-even kinds: `{'CAPTURE': 5, 'STAY': 5, 'DESCENT': 8}`
- stay after maximal even run: `5`

## Stay-after-even samples

- n=`9` a=`2` z=`140` e=`11` b=`1` y=`11`
- n=`37` a=`4` z=`86818724` e=`9317` b=`1` y=`9317`
- n=`49` a=`2` z=`6352` e=`79` b=`1` y=`79`
- n=`69` a=`2` z=`13716` e=`117` b=`1` y=`117`
- n=`77` a=`3` z=`2322378` e=`1523` b=`1` y=`1523`

## Calibration

- n=`3` a=`3` z=`36` cell=`overshoot` e=`6` b=`3` y=`1` kind=`CAPTURE`
- n=`5` a=`2` z=`36` cell=`overshoot` e=`6` b=`3` y=`1` kind=`CAPTURE`
- n=`9` a=`2` z=`140` cell=`overshoot` e=`11` b=`1` y=`11` kind=`STAY`
- n=`13` bucket=`OE_PROGRESS`
- n=`25` a=`3` z=`52214` cell=`overshoot` e=`228` b=`2` y=`15` kind=`DESCENT`
- n=`37` a=`4` z=`86818724` cell=`overshoot` e=`9317` b=`1` y=`9317` kind=`STAY`
- n=`69` a=`2` z=`13716` cell=`overshoot` e=`117` b=`1` y=`117` kind=`STAY`
- n=`77` a=`3` z=`2322378` cell=`overshoot` e=`1523` b=`1` y=`1523` kind=`STAY`

## Lean

- `image_oddEvenBlock`: `True`
- `first_even_return`: `True`
- `even_floorPower_lt_iff`: `True`
- `even_floorPower_eq_iff`: `True`
- `even_floorPower_gt_iff`: `True`
- `even_ne_odd_square`: `True`
- `odd_even_residual_trichotomy`: `True`
- `odd_even_residual_image`: `True`
- `first_even_descent_iff`: `True`
- `finiteProgress_of_first_even_below`: `True`
- `minimal_even_residual_gt_sq`: `True`
- `minimal_nonterm_not_first_even_descent`: `True`
- `minimal_nonterm_not_first_even_capture`: `True`
- `first_even_return_cycle`: `True`
- `minimal_first_even_dichotomy`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- FloorPower not rewritten: `True`
- Progress spine unchanged: `True`
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
- first_even_descends: `False`
- cycle_impossible: `False`
- overshoot_is_progress: `False`

## Decision

**FIRST_EVEN_RESIDUAL_CLASSIFIED**

first even residual is below n^2, return-to-n, or overshoot; a MinimalNonTerm start cannot Descent or Capture on the first O^a E; the window is all overshoot.

This is not a halt result. Overshoot is not FiniteProgress.
Return-to-n is a cycle candidate, not a cycle-impossibility theorem.

