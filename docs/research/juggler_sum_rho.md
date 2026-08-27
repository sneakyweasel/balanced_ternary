# Juggler global sum-rho / word-statistics

Status: **RHO_COMPLEX**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Rho is the existing naive
`pathDefectSum`, not a new remainder and not weighted Delta.

## Branch budget

```text
Mathematical target     does pathDefectSum admit a non-circular word-statistics bound?
Novelty hypothesis      H1-H3, a new telescope, or a non-T<n H4
Falsifier               H1-H3 fail; only known path identity; H4 is T<n
Existing machinery      local_defect, pathDefectSum, globalDefect, powGap
Maximum Phase-0 scope   n<=4000, k<=20, bit cap; H1-H4; no GPU/Lean/induction
```

## Metadata

- algorithm: `sum-rho-v1`
- engine control layer modified: `False`
- classification: **RHO_COMPLEX**
- secondary: `['RHO_COUNTEREXAMPLE', 'RHO_REPACK']`
- rows: `79553`
- sorry-free: `True`
- pathDefectSum present: `True`

H1 and H3 fail: Rho varies at fixed (k,o) and at fixed run signature (first H1 {'k': 1, 'o': 0, 'n_values': 124, 'pair': [{'n': 4, 'word': 'E', 'rho_sum': 0}, {'n': 3968, 'word': 'E', 'rho_sum': 124}]}; first H3 {'k': 1, 'o': 0, 'runs': 1, 'max_O': 0, 'max_E': 1, 'n_values': 124, 'pair': [{'n': 4, 'word': 'E', 'rho_sum': 0}, {'n': 3968, 'word': 'E', 'rho_sum': 124}]}); H2 k*2n fails at {'n': 3, 'k': 3, 'word': 'OOO', 'rho_sum': 41, 'bound': 21}; H2 k*2n^3 fails at {'n': 25, 'k': 3, 'word': 'OOO', 'rho_sum': 97493, 'bound': 93753}; no new telescope (only pathPows = nextSquares + Rho); H4 is the circular rewrite Rho > surplus implies T<n only because Delta >= Rho and Delta > surplus iff T<n; it never fires on expanding rows; same-word OOE Rho varies ({'word': 'OOE', 'n_realizers': 106, 'min': {'n': 5, 'rho_sum': 39}, 'max': {'n': 775, 'rho_sum': 6023969}, 'varies': True}).

Closed branches were not reopened: residual future-quotient,
PE-factor grammar, R=Delta/S, scalar residual state.

## Recovered identities

- n=`9` `{'path_identity': True, 'compose_additive': True, 'delta_eq_slack': True, 'delta_ge_rho': True, 'one_step_eq': True}`
- n=`10` `{'path_identity': True, 'compose_additive': True, 'delta_eq_slack': True, 'delta_ge_rho': True, 'one_step_eq': True}`
- n=`13` `{'path_identity': True, 'compose_additive': True, 'delta_eq_slack': True, 'delta_ge_rho': True, 'one_step_eq': True}`
- n=`37` `{'path_identity': True, 'compose_additive': True, 'delta_eq_slack': True, 'delta_ge_rho': True, 'one_step_eq': True}`
- n=`365` `{'path_identity': True, 'compose_additive': True, 'delta_eq_slack': True, 'delta_ge_rho': True, 'one_step_eq': True}`

- telescope all-zero: `{'id': False, 'sq': False, 'cube': False, 'local_defect': False}`
- known path identity on the telescope probe: `True`

## H1 pure word bound

- holds: `False`
- groups: `142` splits: `123`
- first split: `{'k': 1, 'o': 0, 'n_values': 124, 'pair': [{'n': 4, 'word': 'E', 'rho_sum': 0}, {'n': 3968, 'word': 'E', 'rho_sum': 124}]}`

## H2 scale-aware bound

- `k_times_2n3` holds=`False` counterexample=`{'n': 25, 'k': 3, 'word': 'OOO', 'rho_sum': 97493, 'bound': 93753}` worst=`{'n': 3547, 'word': 'OOOEOOOEOOOOOO', 'ratio': 1.7180881280189654e+103, 'rho_sum': 21467774938663757729688406338589392906662976205686818682158585739140952822775240350190598911294724532344512259949066, 'bound': 1249515353058}`
- `k_times_2n` holds=`False` counterexample=`{'n': 3, 'k': 3, 'word': 'OOO', 'rho_sum': 41, 'bound': 21}` worst=`{'n': 3547, 'word': 'OOOEOOOEOOOOOO', 'ratio': 2.1612579219433966e+110, 'rho_sum': 21467774938663757729688406338589392906662976205686818682158585739140952822775240350190598911294724532344512259949066, 'bound': 99330}`

## H3 run-sensitive bound

- holds: `False`
- groups: `2573` splits: `1969`
- first split: `{'k': 1, 'o': 0, 'runs': 1, 'max_O': 0, 'max_E': 1, 'n_values': 124, 'pair': [{'n': 4, 'word': 'E', 'rho_sum': 0}, {'n': 3968, 'word': 'E', 'rho_sum': 124}]}`

## H4 defect-compensated

- Rho > Delta anywhere: `0`
- Rho > Delta on expanding: `0`
- Rho <= |gap| fails at: `{'n': 3, 'word': 'O', 'rho_sum': 2, 'gap': 1}`
- Rho >= |gap| fails at: `{'n': 1, 'word': 'O', 'rho_sum': 0, 'gap': 1}`
- circularity: Rho > surplus implies T<n only because Delta >= Rho and Delta > surplus iff T<n; it never fires on expanding rows

## Same-word variation

- OOE: `{'word': 'OOE', 'n_realizers': 106, 'min': {'n': 5, 'rho_sum': 39}, 'max': {'n': 775, 'rho_sum': 6023969}, 'varies': True}`
- EOO: `{'word': 'EOO', 'n_realizers': 43, 'min': {'n': 2, 'rho_sum': 1}, 'max': {'n': 674, 'rho_sum': 1565}, 'varies': True}`

## Hard traces

- n=`9` `{'word': 'OOEOEEEO', 'rho_sum': 140, 'delta': None, 'end': 1, 'overflow': False}`
- n=`37` `{'word': 'OOOOEOOO', 'rho_sum': 32064036900595, 'delta': None, 'end': 24906114455136, 'overflow': False}`
- n=`49` `{'word': 'OOEOEEOO', 'rho_sum': 6115, 'delta': None, 'end': 36, 'overflow': False}`
- n=`69` `{'word': 'OOEOOEEE', 'rho_sum': 10086, 'delta': None, 'end': 3, 'overflow': False}`
- n=`77` `{'word': 'OOOEOEOO', 'rho_sum': 1441315, 'delta': None, 'end': 233046, 'overflow': False}`

## Lean

- sorry_free: `True`
- pathDefectSum: `True`
- pathPows_eq_next_add_defects: `True`
- globalDefect: `True`
- no_new_rho: `True`
- no_ResidualState: `True`
- no_global_termination_theorem: `True`
- FloorPower_absent: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- new_rho: `False`
- residual_quotient_reopened: `False`
- pe_factor_reopened: `False`
- finite_residual_automaton: `False`
- new_scalar_energy: `False`
- first_return_induction: `False`

## Decision

**RHO_COMPLEX**

H1 and H3 fail: Rho varies at fixed (k,o) and at fixed run signature (first H1 {'k': 1, 'o': 0, 'n_values': 124, 'pair': [{'n': 4, 'word': 'E', 'rho_sum': 0}, {'n': 3968, 'word': 'E', 'rho_sum': 124}]}; first H3 {'k': 1, 'o': 0, 'runs': 1, 'max_O': 0, 'max_E': 1, 'n_values': 124, 'pair': [{'n': 4, 'word': 'E', 'rho_sum': 0}, {'n': 3968, 'word': 'E', 'rho_sum': 124}]}); H2 k*2n fails at {'n': 3, 'k': 3, 'word': 'OOO', 'rho_sum': 41, 'bound': 21}; H2 k*2n^3 fails at {'n': 25, 'k': 3, 'word': 'OOO', 'rho_sum': 97493, 'bound': 93753}; no new telescope (only pathPows = nextSquares + Rho); H4 is the circular rewrite Rho > surplus implies T<n only because Delta >= Rho and Delta > surplus iff T<n; it never fires on expanding rows; same-word OOE Rho varies ({'word': 'OOE', 'n_realizers': 106, 'min': {'n': 5, 'rho_sum': 39}, 'max': {'n': 775, 'rho_sum': 6023969}, 'varies': True}).

This is not a halt result. No new rho was defined.
The PE-factor and residual-quotient branches were not reopened.

