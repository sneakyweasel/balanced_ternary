# Juggler m-cycle finance

Status: **M_CYCLE_FINANCE_GREEN**

Simons-circuit log-unroll of CycleFinance at each local minimum.
Not a halt theorem. Not a no-cycle-of-any-length theorem.
No new Lean.

## Metadata

- classification: **M_CYCLE_FINANCE_GREEN**
- seeds: `[25, 37, 77, 365, 1999, 30817]`
- step cap: `400`
- usable circuit starts: `6`
- max raw full/minima: `11.964650691331236`
- max cycle-like full/minima: `1.2064364502258211`
- cycle-like Steiner holds: `True`
- L=19 m=1 killed: `True`
- L=30 all m killed: `True`
- Lean-surviving all-m kills ≤ 90: `[30, 41, 44, 52, 55, 60, 63, 66, 71, 74, 77, 82, 85, 88, 90]`

CycleMin joint-minima finance with climb/even error terms excludes leftover pairs that cycleMin_finance misses: L=19 is impossible as a 1-cycle, and L=30 is impossible for every m. Lean-surviving lengths ≤ 90 killed for all m: [30, 41, 44, 52, 55, 60, 63, 66, 71, 74, 77, 82, 85, 88, 90]. Adversarial circuit-partition remains a reparameterization of the global bound. Cycle-like transient ratio 1.21 ≤ 2.0.

## Transient circuits

- start=`25` m=`2` cycle-like m=`1` raw full/minima=`1.1839` cycle-like full/minima=`1.2064`
- start=`37` m=`2` cycle-like m=`2` raw full/minima=`1.1144` cycle-like full/minima=`1.1144`
- start=`77` m=`5` cycle-like m=`3` raw full/minima=`1.2223` cycle-like full/minima=`1.1575`
- start=`365` m=`5` cycle-like m=`4` raw full/minima=`11.9647` cycle-like full/minima=`1.0296`
- start=`1999` m=`7` cycle-like m=`6` raw full/minima=`11.6231` cycle-like full/minima=`1.0137`
- start=`30817` m=`17` cycle-like m=`17` raw full/minima=`1.0733` cycle-like full/minima=`1.0733`

## Leftover lengths

- L=`19` o=`12` even=`7` global n_max=`297` Lean survives=`True` kills m=1=`True` kills all m=`False` new m=`[1]`
- L=`30` o=`19` even=`11` global n_max=`102` Lean survives=`True` kills m=1=`True` kills all m=`True` new m=`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]`
- L=`84` o=`53` even=`31` global n_max=`5599` Lean survives=`True` kills m=1=`False` kills all m=`False` new m=`[]`

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
- steiner_form: `False`
- stronger_than_cycleMin_finance: `False`
- peak_finance_reopened: `False`
- extremal_composition_reopened: `False`

## Decision

**M_CYCLE_FINANCE_GREEN**

CycleMin joint-minima finance with climb/even error terms excludes leftover pairs that cycleMin_finance misses: L=19 is impossible as a 1-cycle, and L=30 is impossible for every m. Lean-surviving lengths ≤ 90 killed for all m: [30, 41, 44, 52, 55, 60, 63, 66, 71, 74, 77, 82, 85, 88, 90]. Adversarial circuit-partition remains a reparameterization of the global bound. Cycle-like transient ratio 1.21 ≤ 2.0.

