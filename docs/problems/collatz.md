# Collatz (accelerated odd-only map)

Status: **STRUCTURAL**

This module does **not** claim a proof or disproof of the Collatz conjecture.

## Exact statement

Study \(T(n)=(3n+1)/2^{v_2(3n+1)}\) on positive odd integers through
exponent codes, cylinders, lift digits, affine centers, and BT observables.

## Why balanced ternary is relevant

BT represents the canonical realizer \(R\) and supplies word maps such as
\(W\). \(\operatorname{BT}(R)\) is determined by \(R\); it is not an
independent solving coordinate.

## Existing record

See [collatz_mathematics.md](../collatz_mathematics.md),
[collatz_research_questions.md](../collatz_research_questions.md), and the
milestone documents indexed from [docs/README.md](../README.md).

## Lean

`formal/Problems/Collatz/` with compatibility re-exports in `formal/CollatzDual/`.

## Conjectures / refutations

Registry ids include `Nk_state_count`, `n_star_le_n`,
`BT_R_suffix_determines_next_valuation`, `W_commutes_T`.

## Branch budget

- **Target:** what exponent codes, cylinders, lift digits, and affine
  centers determine exactly about \(T\), and what they provably do not.
- **Novelty hypothesis:** balanced-ternary observables of the realizer
  \(R\) carry information the 2-adic exponent code does not.
- **Falsifier:** any BT observable shown to be a function of \(R\).
- **Existing machinery:** `research.collatz`, `bt.transducers`,
  `bt.automata`, the four-coordinate literature dictionary.
- **Maximum Phase-0 scope:** finite certificates and bounded censuses
  over stated ranges.
- **Promotion criterion:** an exact statement about \(T\) that is not a
  reparameterization of the exponent-code literature.
- **Stop criterion:** the observable is determined by \(R\), or the
  remaining work is range extension.

The novelty hypothesis was **REFUTED**: `H_BT` is not an independent
entropy and \(\operatorname{BT}(R)\) is determined by \(R\)
([balanced_ternary_vs_collatz_literature.md](../balanced_ternary_vs_collatz_literature.md)).

## Decision

`PARK`. The exact results — \(T^m\), unique realizers, cylinder density,
zero-lift equivalences, the \(G_m\) recurrence, cycle pruning — stand and
are Lean-backed in part, but the BT-independence hypothesis that would
have justified a dedicated push is refuted, and the open items
(`Nk_state_count`, low-\(K_m/m\) lifts, non-contraction compatibility)
are conjectures without a bounded falsification plan. Keep the module and
the registry; do not open a numbered Collatz milestone by default.

Best next question: is exceptional non-contracting itinerary
compatibility decidable on a stated finite family?

## Publication assessment

Status: `STRUCTURAL`. Not a `PAPER_CANDIDATE` as a Collatz contribution:
the exact theorems are a coordinate dictionary against the exponent-code
literature, and no claim about the conjecture itself is made.
