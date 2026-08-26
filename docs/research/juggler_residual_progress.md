# Juggler residual progress

Status: **RESIDUAL_PROGRESS_GREEN**

Standalone application phase. Not a Research Engine experiment and
not a termination theorem. After an uncertified collapse `n→y`,
progress is measured from the residual `y` itself.

## Branch budget

```text
Mathematical target     Useful R with ProgressWithin; residuals from known collapses
Novelty hypothesis      All y<12 are ReachesOne; even y<144 follow
Falsifier               Some y<12 fails, or a calibration residual escapes
Existing machinery      ReachesOne closure, floorPower_pos, collapse census
Maximum Phase-0 scope   Census plus Lean interval <12 and even <144
```

## Metadata

- basin: `[1]`
- certified R: `y<12` and even `y<144`
- engine control layer modified: `False`
- classification: **RESIDUAL_PROGRESS_GREEN**
- sorry-free: `True`

R={1,...,11} is ReachesOne; even residuals below 144 are ReachesOne by one even step; known uncertified collapse residuals locally descend from y; 9→11 is now ReachesOne-implied.

## Calibration residuals

- y=`11` from n=`9` kind=`REACHES_ONE` horizon=`1` image=`36` renewal=`2`→`6`
- y=`9317` from n=`37` kind=`LOCAL_DESCENT` horizon=`5` image=`2233` renewal=`10`→`8`
- y=`2233` from n=`37` kind=`REACHES_ONE` horizon=`4` image=`76` renewal=`5`→`8`

## Small interval and even square

- all `1≤y<12` have ProgressWithin: `True` (max horizon `2`)
- all even `2≤y<144` have ProgressWithin in one step: `True`
- uncertified residuals outside R: `13`
- renewal counterexamples `T^r(y)<n`: `0`

## Uniform horizon

- y=`193` first progress=`REACHES_ONE` horizon=`70` image=`80` max bits=`900`
- No uniform `L` works for every positive integer. The useful `R` is the
  certified initial segment, not all of `ℕ`.

## Lean

- `three_reachesOne`: `True`
- `five_reachesOne`: `True`
- `seven_reachesOne`: `True`
- `nine_reachesOne`: `True`
- `ten_reachesOne`: `True`
- `eleven_reachesOne`: `True`
- `reachesOne_of_lt_twelve`: `True`
- `image_lt_twelve_reachesOne`: `True`
- `non_reachesOne_ge_twelve`: `True`
- `even_lt_sq_twelve_reachesOne`: `True`
- `image_pos`: `True`
- `reachesOne_of_image`: `True`
- `minimal_avoids_reachesOne_image`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- no residual-path datatype: `True`
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

**RESIDUAL_PROGRESS_GREEN**

R={1,...,11} is ReachesOne; even residuals below 144 are ReachesOne by one even step; known uncertified collapse residuals locally descend from y; 9→11 is now ReachesOne-implied.

This is not a halt result.

