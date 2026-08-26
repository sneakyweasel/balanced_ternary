# Juggler residual-chain certificate propagation

Status: **RESIDUAL_CHAIN_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. A residual step is one realized
`O^a E^b` excursion. ReachesOne, Capture, and ReturnBelow
propagate backward. Residual Descent need not.

## Branch budget

```text
Mathematical target     which residual certificates propagate, and which leftover is recursive
Novelty hypothesis      Descent at y with image ≥ n is not progress at n; persistent odd-odd is a subclass
Falsifier               FiniteProgress(y) ⇒ FiniteProgress(n); or every stay residual is odd-odd
Existing machinery      reachesOne_of_image, capture_of_suffix, ReturnBelow, oddEvenBlock
Maximum Phase-0 scope   ResidualStep; compose/non-compose; PersistentOddResidual; hard-chain census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **RESIDUAL_CHAIN_GREEN**
- secondary: `[]`
- sorry-free: `True`

residual steps compose ReachesOne, Capture, and ReturnBelow; Descent at y with image ≥ n is not Descent at n; persistent odd-odd leftovers [37, 69]; automatic FiniteProgress stay [9, 49, 77].

## First residual census

- odd-odd starts: `18`
- first residual kinds: `{'CAPTURE': 5, 'RETURN_BELOW': 8, 'CYCLE': 0, 'STAY_AUTO_FP': 3, 'PERSISTENT_ODD_ODD': 2, 'STAY_EVEN': 0, 'NO_EVEN': 0}`
- propagating (Capture or ReturnBelow): `13`
- stay with automatic FiniteProgress: `[9, 49, 77]`
- persistent odd-odd: `[37, 69]`

## Hard residual chains

### n = 9

- x=`9` O^2E^1 z=`140` y=`11` bucket=`OE_PROGRESS` vs_n=`STAY` kind=`STAY_AUTO_FP` persistent=`False`
- x=`11` O^1E^3 z=`36` y=`1` bucket=`ONE` vs_n=`CAPTURE` kind=`CAPTURE` persistent=`False`

### n = 37

- x=`37` O^4E^1 z=`86818724` y=`9317` bucket=`ODD_ODD` vs_n=`STAY` kind=`PERSISTENT_ODD_ODD` persistent=`True`
- x=`9317` O^3E^2 z=`24906114455136` y=`2233` bucket=`ODD_ODD` vs_n=`STAY` kind=`PERSISTENT_ODD_ODD` persistent=`False`
- x=`2233` O^2E^5 z=`34276462` y=`1` bucket=`ONE` vs_n=`CAPTURE` kind=`CAPTURE` persistent=`False`

### n = 49

- x=`49` O^2E^1 z=`6352` y=`79` bucket=`OE_PROGRESS` vs_n=`STAY` kind=`STAY_AUTO_FP` persistent=`False`
- x=`79` O^1E^2 z=`702` y=`5` bucket=`ODD_ODD` vs_n=`DESCENT` kind=`RETURN_BELOW` persistent=`False`

### n = 69

- x=`69` O^2E^1 z=`13716` y=`117` bucket=`ODD_ODD` vs_n=`STAY` kind=`PERSISTENT_ODD_ODD` persistent=`True`
- x=`117` O^2E^3 z=`44992` y=`3` bucket=`ODD_ODD` vs_n=`DESCENT` kind=`RETURN_BELOW` persistent=`False`

### n = 77

- x=`77` O^3E^1 z=`2322378` y=`1523` bucket=`OE_PROGRESS` vs_n=`STAY` kind=`STAY_AUTO_FP` persistent=`False`
- x=`1523` O^1E^1 z=`59436` y=`243` bucket=`ODD_ODD` vs_n=`STAY` kind=`PERSISTENT_ODD_ODD` persistent=`False`
- x=`243` O^2E^2 z=`233046` y=`21` bucket=`OE_PROGRESS` vs_n=`DESCENT` kind=`RETURN_BELOW` persistent=`False`

## Lean

- `ResidualStep`: `True`
- `PersistentOddResidual`: `True`
- `residualStep_word`: `True`
- `reachesOne_of_residualStep`: `True`
- `finiteProgress_of_residual_capture`: `True`
- `finiteProgress_of_residual_returnBelow`: `True`
- `residual_descent_not_below`: `True`
- `persistent_odd_odd`: `True`
- `persistent_residual_preserves_frontier`: `True`
- `minimal_residual_scale`: `True`
- `ResidualChain`: `True`
- `reachesOne_of_residualChain`: `True`
- `finiteProgress_of_residualChain_returnBelow`: `True`
- `finiteProgress_of_residualChain_capture`: `True`
- certificate unchanged: `True`
- ReturnBelow distinct: `True`
- `PowerHeight` absent: `True`
- FloorPower not rewritten: `True`
- Progress unchanged: `True`
- MinimalNonTerm unchanged: `True`
- no FiniteProgress propagation theorem: `True`
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
- finite_progress_propagates: `False`
- residual_descent_is_progress: `False`
- uniform_residual_horizon: `False`
- overshoot_is_progress: `False`

## Decision

**RESIDUAL_CHAIN_GREEN**

residual steps compose ReachesOne, Capture, and ReturnBelow; Descent at y with image ≥ n is not Descent at n; persistent odd-odd leftovers [37, 69]; automatic FiniteProgress stay [9, 49, 77].

This is not a halt result. FiniteProgress at a residual is not
FiniteProgress at the start. There is no uniform residual horizon.

