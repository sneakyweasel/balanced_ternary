# Juggler reviewer bundle (two manuscripts)

Author: Philippe Cochin. Date: 30 August 2026.
Status: Paper A is a submission candidate; Paper B is a working draft.

This folder is a snapshot of the files to send for external review. It
is not the laboratory. No termination theorem is claimed.

## Read this first

1. [juggler_finite_dynamics_note.pdf](juggler_finite_dynamics_note.pdf)
   — **Paper A**: *Small cycles of the Juggler map*. Envelope, exact
   defect, inverse cells, the length-\(\le 7\) census, and leftover
   families (Theorems 3.12--3.20). Lean-backed throughout; no
   density claims; no length-8 or length-9 census.
2. [juggler_parity_discrepancy_note.pdf](juggler_parity_discrepancy_note.pdf)
   — **Paper B**: parity equidistribution of nested floor powers, the
   kernel theorem, depth-4 completeness over odd starts, and the
   certified-descent density \(13/16\). Human proofs. (The former
   length-5/7/8 splits and deeper densities were withdrawn after
   referee review and are not claimed.)
3. [juggler_finite_dynamics_reviewer_packet.md](juggler_finite_dynamics_reviewer_packet.md)
   — claim map and falsifiers for both papers. Optional for the proofs.

Markdown sources:
[juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md) and
[juggler_parity_discrepancy_note.md](juggler_parity_discrepancy_note.md).
Paper B's Section 7 figure is
[figures/juggler_frontier.png](figures/juggler_frontier.png).

## Optional Lean map

- [juggler_finite_dynamics_formalization.md](juggler_finite_dynamics_formalization.md)
  — theorem names. The Lean import graph is
  [figures/juggler_lean_layers.png](figures/juggler_lean_layers.png).

The paper barrel depends on the repository's full Lean source tree and is
therefore not duplicated in this snapshot. To check the Lean proofs, clone
the repository and from `formal/` run

```text
lake build Problems.JugglerPaper
```

Paper A Zenodo deposit kit (one PDF, paste-ready fields):
[zenodo_paper_a/](zenodo_paper_a/).

Repository: https://github.com/sneakyweasel/balanced_ternary/

Every theorem of Paper A is in Lean. Every analytic estimate of
Paper B (including the kernel theorem and the shift-average theorem)
is a human proof and is not in Lean; only the exact floor reductions
beneath them are (`GapCells.lean`, including the double-gap identity
`seq_floor_gap_second`).

## What is not here

The full `Problems.Juggler` laboratory stack, the Word Atlas, pytest
records, and internal dossiers. Those are not required to read either
paper.
