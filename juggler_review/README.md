# Juggler finite-dynamics reviewer bundle

Author: Philippe Cochin. Date: 29 August 2026.
Status: publication draft, not submitted.

This folder is a snapshot of the files to send for external review. It
is not the laboratory. No termination theorem is claimed.

## Read this first

1. [juggler_finite_dynamics_note.pdf](juggler_finite_dynamics_note.pdf)
   — the math note (the review object).
2. [juggler_finite_dynamics_reviewer_packet.md](juggler_finite_dynamics_reviewer_packet.md)
   — claim map and falsifiers. Optional for the proofs.

The Markdown source of the note is
[juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md).
The Section 6 figure is [figures/juggler_frontier.png](figures/juggler_frontier.png).

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

Repository: https://github.com/sneakyweasel/balanced_ternary/

The analytic estimates of Sections 5 and 6 (including the kernel
theorem and the shift-average theorem) and Proposition 6.1 are human
proofs and are not in Lean; only their exact floor reductions are
(`GapCells.lean`, including the double-gap identity
`seq_floor_gap_second`).

## What is not here

The full `Problems.Juggler` laboratory stack, the Word Atlas, pytest
records, and internal dossiers. Those are not required to read the note.
