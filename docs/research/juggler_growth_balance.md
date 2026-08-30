# Juggler prefix growth / retention balance

Status: **GROWTH_BALANCE_CLOSED**

Prefix-level growth and floor-retention on AboveAnchor orbits.
Not a halt theorem. Not a new cell.

## Branch budget

```text
Mathematical target     independent prefix growth/retention law
Novelty hypothesis      F_k >= n^{2^k-3^{O_k}} is a new budget
Maximum Phase-0 scope   leftovers; odd n<201; no Lean
```

## Metadata

- classification: **GROWTH_BALANCE_CLOSED**
- leftover identity fail: `False`
- leftover gamma fail: `False`
- leftover formal drop: `True`
- window identity ok: `True`

F_k >= n^{2^k-3^{O_k}} is x_k >= n; 3^{O_k} >= 2^k is the word envelope plus AboveAnchor.

## Leftovers

- `365`: word=`OOEOOEOOEOOEOEE` runs=`[2, 2, 2, 2, 1]` last_above k=`14` x=`1196` 3^O=`19683` 2^k=`16384`; drop k=`15` x=`34` 3^O=`19683` 2^k=`32768` formal=`True`
- `501`: word=`OOEOOOEOOEEOOEOOEOOEOEE` runs=`[2, 3, 2, 2, 2, 2, 1]` last_above k=`22` x=`1196` 3^O=`4782969` 2^k=`4194304`; drop k=`23` x=`34` 3^O=`4782969` 2^k=`8388608` formal=`True`
- `1517`: word=`OOEOOEOOEOEOOOEE` runs=`[2, 2, 2, 1, 3]` last_above k=`15` x=`539470` 3^O=`59049` 2^k=`32768`; drop k=`16` x=`734` 3^O=`59049` 2^k=`65536` formal=`True`
- `6187`: word=`OOEOOOEOOEEOE` runs=`[2, 3, 2, 1]` last_above k=`12` x=`1183550` 3^O=`6561` 2^k=`4096`; drop k=`13` x=`1087` 3^O=`6561` 2^k=`8192` formal=`True`

## Existing Lean (unchanged)

- `power_bound_word`: `True`
- `aboveAnchor_not_envelope_drop`: `True`
- `global_defect_identity`: `True`
- `power_bound_compensated_contracts`: `True`
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
- independent_retention_budget: `False`
- q_descriptor_reopen: `False`
- amplify_reopen: `False`
- growth_balance_lean: `False`
- letter_chain: `False`

## Decision

**GROWTH_BALANCE_CLOSED**

F_k >= n^{2^k-3^{O_k}} is x_k >= n; 3^{O_k} >= 2^k is the word envelope plus AboveAnchor.

