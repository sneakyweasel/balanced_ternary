# Juggler finite-dynamics paper synthesis

Author: Philippe Cochin. Date: 28 August 2026.
Status: **PAPER_CANDIDATE**. The publication draft is dated 28 August 2026
and is not submitted. After the paper audit it is a standalone math note
(envelope, defect, short certificates, ambient discrepancy), not a
repository tour.

This branch opens no new attack and makes no claim that every positive
integer reaches \(1\).

## Problem

Can the accumulated exact and computational Juggler results be stated as one
coherent, externally reviewable finite-dynamics paper with a precise
pointwise-progress boundary?

## Exact statement

The paper-level target is not universal termination. It is the qualified
math note:

> Realized finite words obey an exact power envelope; even and odd-to-even
> starts have uniform short descent certificates; the complementary
> odd-to-odd class has density \(1/4\). That density is not Terras's
> theorem and not a density of arrival at \(1\).

Every substantive claim must be linked to one of:

- an exact Lean theorem;
- an exact human proof;
- a bounded computation with manifest and tests;
- a computational observation;
- a reproducible refutation.

## Current literature

- Pickover, *Computers and the Imagination*,
  `pickover-1991-computers-imagination` — historical source. **KNOWN**.
- OEIS A007320, `oeis-A007320` — computational sequence record and statement
  of the open totality question. **KNOWN**.
- Kuipers--Niederreiter, *Uniform Distribution of Sequences*,
  `kuipers-niederreiter-1974-uniform-distribution` — classical discrepancy
  tools. **KNOWN**.
- Prasad--Prasad 2025, `prasad-prasad-2025-juggler-like` — probabilistic and
  large-deviation context for juggler-like models. **KNOWN**; not a theorem on
  the exact floor-power map.

Project relationship: **extended and synthesized**. The paper combines a new
formal/computational apparatus and its exact finite results with explicitly
classical analytic tools. A full prior-art review remains an external-review
gate; no priority claim is made for the Juggler map, exponent heuristics, or
standard discrepancy inequalities.

## Branch budget

```text
Mathematical target     Produce one defensible theorem-and-certificate account
                        of finite Juggler structure and the remaining
                        pointwise gap.
Novelty hypothesis      The integrated Lean semantics, exact finite structure,
                        reproducible Word Atlas, and systematic tested-family
                        eliminations form a publishable research artifact.
Falsifier               A central statement lacks a proof/certificate, a
                        bounded absence is promoted to impossibility, or the
                        synthesis has no distinction from existing literature.
Existing machinery      formal/Problems/Juggler; atlas; Juggler dossiers and
                        research records; theorem ledger; refuted registry.
Maximum Phase-0 scope   Markdown paper, reviewer packet, formalization map,
                        branch ledger, literature records, and verification.
                        No new theorem attack, experiment, or Lean development.
Promotion criterion     Every paper claim is evidence-labelled, reproducible,
                        correctly quantified, and externally reviewable.
Stop criterion          Unsupported claims are removed or downgraded; missing
                        mathematics becomes the stated gap rather than a new
                        branch.
```

## Balanced-ternary formulation

None required. Juggler is an application on ordinary positive integers. The
paper does not use balanced ternary as a claimed solution mechanism.

## Why BT may be relevant

Only as laboratory context. The problem-specific mathematics remains under
`research.juggler_sequence` and `formal/Problems/Juggler`; no Juggler code is
added to `bt.*`.

## Candidate operations / invariants

- finite itinerary semantics and word images —
  **EXACT — LEAN VERIFIED**;
- finite-word power envelope and exponent-gap contraction —
  **EXACT — LEAN VERIFIED**;
- exact global defect —
  **EXACT — LEAN VERIFIED**;
- fixed-word monotonicity —
  **EXACT — LEAN VERIFIED**;
- even/odd inverse-cell asymmetry —
  **EXACT — LEAN VERIFIED**;
- cycle exponent, extrema, order, and cell constraints —
  **EXACT — LEAN VERIFIED**;
- Word Atlas scientific census —
  **COMPUTATIONALLY VERIFIED** within its configured bounds;
- \(|S_O(N)|\ll N^{5/6}\) on ambient odd inputs —
  **EXACT — HUMAN PROOF** using classical tools;
- automatic discrepancy transfer to Juggler-generated sets —
  **REFUTED** in the tested form;
- universal termination, irreducibility, or no-compression theorem —
  not claimed.

## Experiments

No new experiment. The synthesis cites existing artifacts:

- `data/research/juggler/word_atlas/`;
- `data/research/juggler/parity_discrepancy_next/`;
- `data/research/juggler/parity_transfer/`;
- `data/research/juggler/probabilistic/`;
- the records linked from
  [the branch ledger](../juggler_branch_ledger.md).

Reproducibility commands are in the
[paper](../theory/juggler_finite_dynamics_note.md) and
[reviewer packet](../theory/juggler_finite_dynamics_reviewer_packet.md).

## Conjectures

None opened. Universal convergence remains the historical Juggler conjecture,
not a new project conjecture.

## Counterexamples

The synthesis includes, among others:

- \(365\xrightarrow{OOE}763\xrightarrow{OOE}1749\), Lean-certified, against
  forced contraction after one persistent expanding block;
- two `OOE` cylinders with opposite next parity, Lean-certified, against the
  tested cylinder quotient;
- a monochromatic odd-input sign run of length \(52\) on
  \([952525,952627]\), exact computation, against a translation-uniform
  short-interval discrepancy law;
- finite separators for the residual and future quotients listed in their
  dossiers.

These refute the named candidate laws, not termination.

## Formalization

No Lean source is added by this synthesis. The formal map is
[juggler_finite_dynamics_formalization.md](../theory/juggler_finite_dynamics_formalization.md).
The paper-central theorem metadata is recorded in
`docs/theory/theorem_ledger.json` and the generated ledger. No `sorry` or
`admit`.

## Results

The publication stack consists of:

- [publication draft](../theory/juggler_finite_dynamics_note.md);
- [reviewer packet](../theory/juggler_finite_dynamics_reviewer_packet.md);
- [formalization map](../theory/juggler_finite_dynamics_formalization.md);
- [curated branch ledger](../juggler_branch_ledger.md).

The note makes the short-certificate boundary explicit: a uniform one- or
two-step argument covers a set of density \(3/4\). That is not a density
of all descent certificates and not a \(\operatorname{ReachesOne}\)
density. The Terras analogue — almost-all descent on odd-to-odd starts —
remains open.

## Open questions

Do almost all odd-to-odd starts have a finite descent certificate?

## Decision

**PROMOTE** the integrated document stack as a paper candidate. The individual
Atlas, discrepancy, probabilistic, and closed-compression branches keep their
original decisions. Promotion applies to the synthesis: its contribution is
the formal/computational map and exact evidence boundary, not a termination
claim.

Best next question: do almost all odd-to-odd starts have a finite descent
certificate?

## Publication assessment

Status: `PAPER_CANDIDATE`.

The candidate is a standalone math note: envelope, defect, short
certificates, and an ambient discrepancy corollary. External mathematical
review is the next gate. The Atlas and closed-compression diaries stay
in the laboratory record.
