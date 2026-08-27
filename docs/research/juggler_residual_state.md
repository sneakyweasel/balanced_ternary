# Juggler residual-state sufficiency

Status: **RESIDUAL_STATE_NEEDS_X**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. ResidualStep stays the successor.
The question is which coordinates of
`(y, parity, A, G, ρ, cell)` determine the next constraint class.

## Branch budget

```text
Mathematical target     which coordinates predict the next residual constraint
Novelty hypothesis      a proper quotient, not x and not history, determines V
Falsifier               every proper quotient splits, or every coord is a function of (n, x)
Existing machinery      residual_excursion, residual_cell, residual_class, remainder, driftG
Maximum Phase-0 scope   HARD_PROBES + odd-odd n<=80; ablation; no Lean state
```

## Metadata

- algorithm: `residual-state-v1`
- engine control layer modified: `False`
- classification: **RESIDUAL_STATE_NEEDS_X**
- secondary: `['ESCAPE_STATE_REPLAY', 'VN_NEEDS_N']`
- sorry-free: `True`
- ResidualState.lean absent: `True`

no proper quotient of (parity, A, G, ρ, cell) predicts V: every fiber-bearing subset splits, and V is a function of y; [['G', 'rho'], ['parity', 'G', 'rho'], ['A', 'G', 'rho'], ['G', 'rho', 'cell'], ['parity', 'A', 'G', 'rho'], ['parity', 'G', 'rho', 'cell'], ['A', 'G', 'rho', 'cell'], ['parity', 'A', 'G', 'rho', 'cell']] predict V on non-start landings only because each class has a single y (window-injective rewriting, not a nonempty fiber); incoming history varies at some y and does not change V; V_n is not a function of y.

## Functions census

- landings: `43`
- start landings: `18`
- distinct y: `30`
- distinct (n, y): `43`
- V determined by y: `True`
- V_n determined by y: `False`
- history varies at y: `6`
- history changes V: `False`
- A varies at a fixed y: `5`
- cell varies at a fixed y: `2`
- A varies at a fixed (n, y): `0`

## Ablation (intrinsic V, non-start landings)

- subsets tested: `31`
- sufficient: `8`
- proper quotients: `0`
- sufficient coordinate lists: `[['G', 'rho'], ['parity', 'G', 'rho'], ['A', 'G', 'rho'], ['G', 'rho', 'cell'], ['parity', 'A', 'G', 'rho'], ['parity', 'G', 'rho', 'cell'], ['A', 'G', 'rho', 'cell'], ['parity', 'A', 'G', 'rho', 'cell']]`

## Ablation (intrinsic V, all landings)

- proper quotients: `0`
- sufficient coordinate lists: `[]`

## Ablation (relative V_n)

- drop n, proper quotients: `0`
- drop n, sufficient: `[['y', 'A'], ['y', 'G'], ['y', 'parity', 'A'], ['y', 'parity', 'G'], ['y', 'A', 'G'], ['y', 'A', 'rho'], ['y', 'A', 'cell'], ['y', 'G', 'rho'], ['y', 'G', 'cell'], ['y', 'parity', 'A', 'G'], ['y', 'parity', 'A', 'rho'], ['y', 'parity', 'A', 'cell'], ['y', 'parity', 'G', 'rho'], ['y', 'parity', 'G', 'cell'], ['y', 'A', 'G', 'rho'], ['y', 'A', 'G', 'cell'], ['y', 'A', 'rho', 'cell'], ['y', 'G', 'rho', 'cell'], ['y', 'parity', 'A', 'G', 'rho'], ['y', 'parity', 'A', 'G', 'cell'], ['y', 'parity', 'A', 'rho', 'cell'], ['y', 'parity', 'G', 'rho', 'cell'], ['y', 'A', 'G', 'rho', 'cell'], ['y', 'parity', 'A', 'G', 'rho', 'cell']]`
- drop y, proper quotients: `0`
- drop y, sufficient: `[['n', 'G'], ['n', 'parity', 'G'], ['n', 'A', 'G'], ['n', 'A', 'rho'], ['n', 'G', 'rho'], ['n', 'G', 'cell'], ['n', 'rho', 'cell'], ['n', 'parity', 'A', 'G'], ['n', 'parity', 'A', 'rho'], ['n', 'parity', 'G', 'rho'], ['n', 'parity', 'G', 'cell'], ['n', 'parity', 'rho', 'cell'], ['n', 'A', 'G', 'rho'], ['n', 'A', 'G', 'cell'], ['n', 'A', 'rho', 'cell'], ['n', 'G', 'rho', 'cell'], ['n', 'parity', 'A', 'G', 'rho'], ['n', 'parity', 'A', 'G', 'cell'], ['n', 'parity', 'A', 'rho', 'cell'], ['n', 'parity', 'G', 'rho', 'cell'], ['n', 'A', 'G', 'rho', 'cell'], ['n', 'parity', 'A', 'G', 'rho', 'cell']]`

## History collisions at a fixed y

- y=`3` histories=`[[0, 0, 'overshoot'], [2, 23, 'overshoot']]` ns=`[3, 69]` V_unique=`True`
- y=`1` histories=`[[1, 13, 'below'], [2, 23, 'overshoot'], [2, 55, 'overshoot'], [2, 119, 'overshoot'], [3, 37, 'overshoot'], [3, 229, 'overshoot']]` ns=`[3, 5, 9, 37, 43, 45, 75]` V_unique=`True`
- y=`5` histories=`[[0, 0, 'overshoot'], [1, 5, 'below']]` ns=`[5, 49]` V_unique=`True`
- y=`9` histories=`[[0, 0, 'overshoot'], [2, 7, 'overshoot']]` ns=`[9, 53, 55]` V_unique=`True`
- y=`11` histories=`[[2, -1, 'overshoot'], [2, 7, 'overshoot']]` ns=`[9, 73]` V_unique=`True`
- y=`21` histories=`[[2, 7, 'overshoot'], [3, 5, 'overshoot']]` ns=`[39, 77]` V_unique=`True`

## V_n splits at a fixed y

- y=`9` ns=`[9, 53, 55]` n_values=`2`

## Hard traces

### n = 9

- i=`0` y=`9` A=`0` G=`0` rho=`0` cell=`overshoot` V.class=`STAY_AUTO_FP` Vn.kind=`STAY`
- i=`1` y=`11` A=`2` G=`-1` rho=`35` cell=`overshoot` V.class=`CAPTURE` Vn.kind=`CAPTURE`
- i=`2` y=`1` A=`1` G=`13` rho=`0` cell=`below` V.class=`None` Vn.kind=`None`

### n = 37

- i=`0` y=`37` A=`0` G=`0` rho=`28` cell=`overshoot` V.class=`PERSISTENT_ODD_ODD` Vn.kind=`STAY`
- i=`1` y=`9317` A=`4` G=`-49` rho=`1394252` cell=`overshoot` V.class=`RETURN_BELOW` Vn.kind=`STAY`
- i=`2` y=`2233` A=`3` G=`5` rho=`123976` cell=`overshoot` V.class=`CAPTURE` Vn.kind=`CAPTURE`
- i=`3` y=`1` A=`2` G=`119` rho=`0` cell=`overshoot` V.class=`None` Vn.kind=`None`

### n = 49

- i=`0` y=`49` A=`0` G=`0` rho=`0` cell=`overshoot` V.class=`STAY_AUTO_FP` Vn.kind=`STAY`
- i=`1` y=`79` A=`2` G=`-1` rho=`235` cell=`overshoot` V.class=`RETURN_BELOW` Vn.kind=`DESCENT`
- i=`2` y=`5` A=`1` G=`5` rho=`4` cell=`below` V.class=`CAPTURE` Vn.kind=`CAPTURE`

### n = 69

- i=`0` y=`69` A=`0` G=`0` rho=`180` cell=`overshoot` V.class=`PERSISTENT_ODD_ODD` Vn.kind=`STAY`
- i=`1` y=`117` A=`2` G=`-1` rho=`1388` cell=`overshoot` V.class=`RETURN_BELOW` Vn.kind=`DESCENT`
- i=`2` y=`3` A=`2` G=`23` rho=`2` cell=`overshoot` V.class=`CAPTURE` Vn.kind=`CAPTURE`

### n = 77

- i=`0` y=`77` A=`0` G=`0` rho=`908` cell=`overshoot` V.class=`STAY_AUTO_FP` Vn.kind=`STAY`
- i=`1` y=`1523` A=`3` G=`-11` rho=`4571` cell=`overshoot` V.class=`RETURN_BELOW` Vn.kind=`STAY`
- i=`2` y=`243` A=`1` G=`1` rho=`7538` cell=`below` V.class=`RETURN_BELOW` Vn.kind=`DESCENT`
- i=`3` y=`21` A=`2` G=`7` rho=`45` cell=`overshoot` V.class=`RETURN_BELOW` Vn.kind=`DESCENT`

## Lean

- `ResidualStep`: `True`
- `PersistentOddResidual`: `True`
- `ResidualChain`: `True`
- ResidualStep unchanged: `True`
- ResidualState.lean absent: `True`
- no ResidualState def: `True`
- no forbidden engines: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- residual_state_object: `False`
- residual_step_extended: `False`
- history_is_new_state: `False`
- defect_financing_opened: `False`
- global_defect_growth_opened: `False`

## Decision

**RESIDUAL_STATE_NEEDS_X**

no proper quotient of (parity, A, G, ρ, cell) predicts V: every fiber-bearing subset splits, and V is a function of y; [['G', 'rho'], ['parity', 'G', 'rho'], ['A', 'G', 'rho'], ['G', 'rho', 'cell'], ['parity', 'A', 'G', 'rho'], ['parity', 'G', 'rho', 'cell'], ['A', 'G', 'rho', 'cell'], ['parity', 'A', 'G', 'rho', 'cell']] predict V on non-start landings only because each class has a single y (window-injective rewriting, not a nonempty fiber); incoming history varies at some y and does not change V; V_n is not a function of y.

This is not a halt result. ResidualStep is not a state object.
Objects B and C were not opened.

