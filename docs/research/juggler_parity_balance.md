# Juggler infinite AboveAnchor parity balance

Status: **PARITY_BALANCE_CLOSED**

Shared finite-prefix language of AboveAnchor words.
Not a halt theorem. Not a CycleMin census.

## Branch budget

```text
Mathematical target     opposite envelope 2^|w| > 3^oddCount(w)
Novelty hypothesis      shared exclusions cap odd density
Maximum Phase-0 scope   integer optimizer; no Lean; no automaton
```

## Metadata

- classification: **PARITY_BALANCE_CLOSED**
- rho_max = 1 (O*): `True`
- mixed max = N-1 (O^{N-1}E): `True`
- isolated = prefix envelope: `True`
- OOE 3^2 vs 2^3: `9` vs `8`
- leftover last-above survives: `True`

shared language is the prefix envelope 2^|w| <= 3^oddCount(w); rho_max = 1 via O* and (N-1)/N via O^{N-1}E; OOE has 9 > 8 so the cycle mean is positive.

## Maximizing families

- `O*`: length `18` odd `18` 2^N=`262144` 3^o=`387420489` ratio=`262144/387420489`
- `O^{N-1}E`: length `18` odd `17` 2^N=`262144` 3^o=`129140163` ratio=`262144/129140163`
- `(OOE)*` block: 2^3=`8` 3^2=`9` ratio=`8/9`

## Isolated prefix vs envelope

The isolated comparison `2^{a+2r+1} <= 3^{a+r}` is the same pair of
exponents as the shared prefix envelope on `O^a E (OE)^r`.
Checked `a,r <= 12`; mismatches `[]`.

## Leftovers

- `365`: word=`OOEOOEOOEOOEOEE` last_above k=`14` O=`9` 2^k=`16384` 3^O=`19683` drop_contracts=`True`
- `501`: word=`OOEOOOEOOEEOOEOOEOOEOEE` last_above k=`22` O=`14` 2^k=`4194304` 3^O=`4782969` drop_contracts=`True`
- `1517`: word=`OOEOOEOOEOEOOOEE` last_above k=`15` O=`10` 2^k=`32768` 3^O=`59049` drop_contracts=`True`
- `6187`: word=`OOEOOOEOOEEOE` last_above k=`12` O=`8` 2^k=`4096` 3^O=`6561` drop_contracts=`True`

## Existing Lean (unchanged)

- `aboveAnchor_not_envelope_drop`: `True`
- `aboveAnchor_not_odd_even`: `True`
- `isolatedOddSurvival_bound`: `True`
- `isolatedOESurvives`: `True`
- `power_bound_word`: `True`
- `AboveAnchor`: `True`
- new Lean file: `False`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- independent_odd_density_upper_bound: `False`
- universal_odd_density: `False`
- numerical_parity_contradiction: `False`
- cyclemin_in_language: `False`
- parity_balance_lean: `False`
- letter_chain: `False`

## Decision

**PARITY_BALANCE_CLOSED**

shared language is the prefix envelope 2^|w| <= 3^oddCount(w); rho_max = 1 via O* and (N-1)/N via O^{N-1}E; OOE has 9 > 8 so the cycle mean is positive.

