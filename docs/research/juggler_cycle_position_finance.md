# Juggler position-dependent cycle finance

Status: **POSITION_FINANCE_GREEN**

Odd-run height refinement of joint-minima m-finance.
Not a new paper. Not a halt theorem.
No new Lean.

## Metadata

- classification: **POSITION_FINANCE_GREEN**
- floor: `257`
- T(n): `4120` even=`True`
- tau_1: `4121`
- tau_2: `264547`
- L=38 all m by joint-minima: `True`
- L=84 m=1 by height law: `True`
- new pairs at 257: `[{'L': 84, 'm': [1, 2]}, {'L': 103, 'm': [17]}, {'L': 168, 'm': [1, 2, 3, 4]}, {'L': 187, 'm': [17, 18, 19]}]`
- joint all-m kills among finance-survivors ≤ 200: `[19, 38, 57, 76, 95, 114, 133, 152, 160, 171, 179, 190, 198]`

Odd-run height law is strictly stronger than charging every climb at T(n). Joint-minima at floor 257 already excludes every length-38 cycle (any m); global finance does not (n_max=299). Position-dependent packing newly excludes leftover pairs [{'L': 84, 'm': [1, 2]}, {'L': 103, 'm': [17]}, {'L': 168, 'm': [1, 2, 3, 4]}, {'L': 187, 'm': [17, 18, 19]}], in particular L=84 at m=1 and m=2. Circuit-partition without a height law remains a reparameterization of cycleMin_finance.

## Focus leftovers at floor 257

- L=`19` o=`12` even=`7` global n_max=`297` joint all m=`True` position all m=`True` new m=`[]`
- L=`38` o=`24` even=`14` global n_max=`299` joint all m=`True` position all m=`True` new m=`[]`
- L=`84` o=`53` even=`31` global n_max=`5599` joint all m=`False` position all m=`False` new m=`[1, 2]`
- L=`168` o=`106` even=`62` global n_max=`5604` joint all m=`False` position all m=`False` new m=`[1, 2, 3, 4]`

## Focus leftovers at floor 53

- L=`19` joint all m=`False` position all m=`False` new m=`[2]`
- L=`38` joint all m=`False` position all m=`False` new m=`[3, 4]`
- L=`84` joint all m=`False` position all m=`False` new m=`[]`
- L=`168` joint all m=`False` position all m=`False` new m=`[]`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- halt_theorem: `False`
- no_cycle_all_lengths: `False`
- floor_raise: `False`
- new_lean: `False`
- new_paper: `False`
- partition_stronger_than_cycleMin_finance: `False`
- peak_finance_reopened: `False`

## Decision

**POSITION_FINANCE_GREEN**

Odd-run height law is strictly stronger than charging every climb at T(n). Joint-minima at floor 257 already excludes every length-38 cycle (any m); global finance does not (n_max=299). Position-dependent packing newly excludes leftover pairs [{'L': 84, 'm': [1, 2]}, {'L': 103, 'm': [17]}, {'L': 168, 'm': [1, 2, 3, 4]}, {'L': 187, 'm': [17, 18, 19]}], in particular L=84 at m=1 and m=2. Circuit-partition without a height law remains a reparameterization of cycleMin_finance.

