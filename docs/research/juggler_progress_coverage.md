# Juggler finite-progress coverage

Status: **ODD_ODD_FRONTIER_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Strong induction reduces
`ReachesOne` to `FiniteProgress`. Even states and odd-to-even
states are covered. The leftover automatic class is odd-to-odd.

## Branch budget

```text
Mathematical target     isolate the FiniteProgress coverage gap after even and OE
Novelty hypothesis      leftover class is odd-to-odd; first even residual stays >= n
Falsifier               even or OE without FiniteProgress, or a halt theorem
Existing machinery      even_word_contracts, floorPower_odd_even_two_step_lt, ReachesOne
Maximum Phase-0 scope   induction spine; even/OE coverage; odd-odd leftover census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ODD_ODD_FRONTIER_GREEN**
- secondary: `['INDUCTION_SPINE_GREEN', 'RESIDUAL_CLASS_IDENTIFIED']`
- sorry-free: `True`

even and OE states have FiniteProgress; the leftover class is odd-to-odd, and in the window the first even residual stays at or above the start.

## Coverage census

- even FiniteProgress: `40`
- OE FiniteProgress: `21`
- odd-odd leftover: `18`
- first-even stays above start: `18`
- first-even descent: `0`
- no even within horizon: `0`
- odd-run lengths a: `[2, 3, 4]`

## Stay-above samples

- n=`3` a=`3` xa=`36` y=`6`
- n=`5` a=`2` xa=`36` y=`6`
- n=`9` a=`2` xa=`140` y=`11`
- n=`25` a=`3` xa=`52214` y=`228`
- n=`33` a=`2` xa=`2598` y=`50`
- n=`35` a=`2` xa=`2978` y=`54`
- n=`37` a=`4` xa=`86818724` y=`9317`
- n=`39` a=`3` xa=`233046` y=`482`

## Calibration

- n=`2` T=`1` bucket=`EVEN_PROGRESS`
- n=`3` T=`5` bucket=`ODD_ODD` a=`3` y=`6` kind=`FIRST_EVEN_STAYS_ABOVE_START`
- n=`5` T=`11` bucket=`ODD_ODD` a=`2` y=`6` kind=`FIRST_EVEN_STAYS_ABOVE_START`
- n=`7` T=`18` bucket=`OE_PROGRESS` OE=`4` lt=`True`
- n=`13` T=`46` bucket=`OE_PROGRESS` OE=`6` lt=`True`
- n=`25` T=`125` bucket=`ODD_ODD` a=`3` y=`228` kind=`FIRST_EVEN_STAYS_ABOVE_START`
- n=`69` T=`573` bucket=`ODD_ODD` a=`2` y=`117` kind=`FIRST_EVEN_STAYS_ABOVE_START`
- n=`77` T=`675` bucket=`ODD_ODD` a=`3` y=`1523` kind=`FIRST_EVEN_STAYS_ABOVE_START`

## Lean

- `FiniteProgress`: `True`
- `finiteProgress_of_descent`: `True`
- `finiteProgress_of_capture`: `True`
- `reachesOne_of_finiteProgress`: `True`
- `reachesOne_of_all_finiteProgress`: `True`
- `even_finiteProgress`: `True`
- `odd_even_finiteProgress`: `True`
- `finiteProgress_of_not_odd_odd`: `True`
- `unresolved_is_odd_odd`: `True`
- `odd_odd_image_gt`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- FloorPower not rewritten: `True`
- no all-FiniteProgress theorem: `True`
- no progress tactic: `True`
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
- odd_odd_is_nonterminating: `False`
- cycle_obstruction: `False`

## Decision

**ODD_ODD_FRONTIER_GREEN**

even and OE states have FiniteProgress; the leftover class is odd-to-odd, and in the window the first even residual stays at or above the start.

This is not a halt result. FiniteProgress is not proved for
odd-to-odd states.

