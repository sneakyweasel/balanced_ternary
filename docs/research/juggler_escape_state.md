# Juggler escape-state margin

Status: **ESCAPE_STATE_COMPLEX**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. An escape prefix is mixed,
prefix-NC, and non-contracting. The question is whether
`M = formal_gap − Δ` is a progress measure.

## Branch budget

```text
Mathematical target     Does M or a small tuple progress on escape prefixes?
Novelty hypothesis      escape now implies a strictly tighter escape later
Falsifier               M is T^{2^k}-n^{2^k}; sign is image>=n; M grows
Existing machinery      formal_gap, tiny_deficit, compensated contraction,
                        prefix_noncontracting, first defect
Maximum Phase-0 scope   identity; HARD_STARTS; n<=200 k<=8; no automaton
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **ESCAPE_STATE_COMPLEX**
- secondary: `['ESCAPE_COUNTEREXAMPLE']`
- sorry-free: `True`

on G<=0, M = T^{2^k}-n^{2^k} and M>=0 iff T>=n; that is actual non-contraction, not a new progress law; escape images move farther from the start on known expanders.

## Window

- prefixes: `1592`
- escape prefixes: `187`
- identity failures on G<=0: `0`
- sign failures: `0`
- M not decreasing: `0`
- first-defect budget not decreasing: `0`
- image not approaching n: `69`
- M=0 with n>=2: `[]`
- longest escape in window: `8` (horizon, not L)

## Hard starts

### n = 5

- k=`1` `O` image=`11` G=`-1` escape=`False` M=`96` W=`96`
- k=`2` `OO` image=`36` G=`-5` escape=`False` M=`1678991` W=`1952496`
- k=`3` `OOE` image=`6` G=`-1` escape=`True` M=`1288991` W=`1562496`

### n = 9

- k=`1` `O` image=`27` G=`-1` escape=`False` M=`648` W=`None`
- k=`2` `OO` image=`140` G=`-5` escape=`False` M=`384153439` W=`387413845`
- k=`3` `OOE` image=`11` G=`-1` escape=`True` M=`171312160` W=`344373685`
- k=`4` `OOEO` image=`36` G=`-11` escape=`True` M=`None` W=`None`

### n = 37

- k=`1` `O` image=`225` G=`-1` escape=`False` M=`49256` W=`49256`
- k=`2` `OO` image=`3375` G=`-5` escape=`False` M=`129746336016464` W=`129961737920888`
- k=`3` `OOO` image=`196069` G=`-19` escape=`False` M=`None` W=`None`
- k=`5` `OOOOE` image=`9317` G=`-49` escape=`True` M=`None` W=`None`
- k=`6` `OOOOEO` image=`899319` G=`-179` escape=`True` M=`None` W=`None`
- k=`7` `OOOOEOO` image=`852846071` G=`-601` escape=`True` M=`None` W=`None`
- k=`8` `OOOOEOOO` image=`24906114455136` G=`-1931` escape=`True` M=`None` W=`None`

### n = 69

- k=`1` `O` image=`573` G=`-1` escape=`False` M=`323568` W=`323568`
- k=`2` `OO` image=`13716` G=`-5` escape=`False` M=`35392391185699215` W=`35452087812908928`
- k=`3` `OOE` image=`117` G=`-1` escape=`True` M=`34600734383587200` W=`34938289461147408`
- k=`4` `OOEO` image=`1265` G=`-11` escape=`True` M=`None` W=`None`
- k=`5` `OOEOO` image=`44992` G=`-49` escape=`True` M=`None` W=`None`
- k=`6` `OOEOOE` image=`212` G=`-17` escape=`True` M=`None` W=`None`

### n = 173

- k=`1` `O` image=`2275` G=`-1` escape=`False` M=`5145696` W=`5145696`
- k=`2` `OO` image=`108510` G=`-5` escape=`False` M=`138636968690388264959` W=`138808137875468113680`
- k=`3` `OOE` image=`329` G=`-1` escape=`True` M=`136464969980530382880` W=`138005778697887767040`
- k=`4` `OOEO` image=`5967` G=`-11` escape=`True` M=`None` W=`None`
- k=`5` `OOEOO` image=`460929` G=`-49` escape=`True` M=`None` W=`None`
- k=`6` `OOEOOO` image=`312932773` G=`-179` escape=`True` M=`None` W=`None`
- k=`7` `OOEOOOO` image=`5535751327289` G=`-601` escape=`True` M=`None` W=`None`
- k=`8` `OOEOOOOO` image=`13024613938403266721` G=`-1931` escape=`True` M=`None` W=`None`

## Lean

- `power_bound_contracts`: `True`
- `power_bound_compensated_contracts`: `True`
- `power_bound_eq_iff_extremal`: `True`
- `powerDeficit`: `True`
- new EscapeState file absent: `True`
- ResidualStep not extended: `True`
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
- escape_margin_is_new_progress: `False`
- finite_progress_for_all: `False`

## Decision

**ESCAPE_STATE_COMPLEX**

on G<=0, M = T^{2^k}-n^{2^k} and M>=0 iff T>=n; that is actual non-contraction, not a new progress law; escape images move farther from the start on known expanders.

The future orbit is a function of the current integer.
Indefinite escape is non-termination, not a new local state.
A search-horizon escape prefix is not a bound L.

