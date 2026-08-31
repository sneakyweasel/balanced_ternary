# Cycle finance inequality

Finance bound n ln n <= (6/5) L 3^o/(3^o - 2^L) on Juggler cycle
minima, exact gap table, descent-induction floor, orbit slack.
Not a halt theorem. The floor is COMPUTATIONALLY VERIFIED.

Regenerate with `python -m research.juggler_sequence.cycle_finance`.
Length-only parity table: `exceptions_parity.json`
(`write_parity_artifacts`; does not replace this crude table).
Prefix-weight leftover scan: `prefix_weights.json`
(`write_prefix_weight_artifacts`; does not replace either table).
Run-type leftover scan: `budget_opt.json`
(`write_budget_opt_artifacts`; does not replace the tables).
Cyclic run-extremum scan: `run_extremum.json`
(`write_run_extremum_artifacts`; does not replace the tables).
Prefix-feasibility scan: `prefix_feasibility.json`
(`write_prefix_feasibility_artifacts`; does not replace the tables).
Finance-conditioned closure scan: `conditioned_closure/summary.json`
(`write_conditioned_artifacts`; does not replace the tables).
Modular-closure scan: `mod_closure/summary.json`
(`write_mod_closure_artifacts`; does not replace the tables).
Ordered-excursion scan: `ordered_excursion/summary.json`
(`write_ordered_artifacts`; does not replace the tables).
Survivor lattice reading of the 99 lengths:
`docs/theory/juggler_run_survivor_lattice_note.md`.
