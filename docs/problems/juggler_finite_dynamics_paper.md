# Juggler finite-dynamics paper synthesis

Author: Philippe Cochin. Date: 31 August 2026.
Status: **PAPER_CANDIDATE**. The publication draft is dated 31 August 2026
and is not submitted. It is a cycle-length note titled
*Lower bounds for nontrivial cycles of the Juggler map*:
finance plus the verified descent floor \(10^6\) give \(L\ge 1054\)
(Theorem A) and an admissible set of \(397\) lengths through
\(10^5\) (Theorem B). The even-count assembly is Theorem C
(period at least eleven). Section 4 is the financing inequality.
The envelope is the tool; the defect is motivation, not the
input to finance.

This branch opens no new attack and makes no claim that every positive
integer reaches \(1\).

## Problem

Can the accumulated exact and computational Juggler results be stated as one
coherent, externally reviewable finite-dynamics paper with a precise
pointwise-progress boundary?

## Exact statement

The paper-level target is not universal termination. It is the qualified
math note:

> Realized finite words obey a power envelope. Inverse cells and a
> classification of even-count \(\le 3\) exclude every such cycle
> word (Theorem C: period at least eleven). A financing inequality
> at a cycle minimum, plus the verified descent floor \(10^6\),
> excludes every period at most \(1053\) (Theorem A) and leaves
> only an explicit admissible set of \(397\) lengths through
> \(10^5\) (Theorem B). Membership in that set is not evidence
> for a cycle. The paper does not prove termination.

Every substantive claim must be linked to one of:

- an exact Lean theorem;
- an exact human proof;
- a bounded computation with manifest and tests;
- a computational observation;
- a reproducible refutation.

## Current literature

- Pickover, *Computers and the Imagination*,
  `pickover-1991-computers-imagination` — historical source. **KNOWN**.
- OEIS A094683, `oeis-A094683` — one-step Juggler map. **KNOWN**.
- OEIS A007320, `oeis-A007320` — stopping-time table and the open totality
  question. **KNOWN**; not the paper citation.
- Kuipers--Niederreiter, *Uniform Distribution of Sequences*,
  `kuipers-niederreiter-1974-uniform-distribution` — classical discrepancy
  tools. **KNOWN**.
- Iwaniec--Kowalski, *Analytic Number Theory* — van der Corput's derivative
  estimate. **KNOWN**.
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
                        global-defect calculus, and certified cycle
                        consequences form a publishable research artifact.
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
- exact global defect, vanishing, and two-term composition —
  **EXACT — LEAN VERIFIED**;
- fixed-word monotonicity —
  **EXACT — LEAN VERIFIED**;
- even/odd inverse-cell asymmetry —
  **EXACT — LEAN VERIFIED**;
- cycle exponent, extrema, order, and cell constraints —
  **EXACT — LEAN VERIFIED**;
- leftover length-six orientations \(OOOEOE\) and \(OOOOEE\) —
  **EXACT — LEAN VERIFIED** (recorded in the leftover-cycles branch);
- leftover length-seven orientations \(OOOOEOE\) and \(OOOOOEE\) —
  **EXACT — LEAN VERIFIED** (ledger `J-leftover-length-seven-orientations`);
- small-cycle census: no cycle word of length at most seven —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_length_le_six`,
  `no_cycle_word_length_le_seven`, ledgers `J-small-cycle-census` and
  `J-small-cycle-census-seven`; strengthened by Theorem 3.22);
- even-count assembly: no cycle word with fewer than four evens,
  so the period is at least eleven —
  **EXACT — LEAN VERIFIED** (Paper A Theorem 3.22 / Corollary 3.23;
  `no_cycle_word_even_count_le_three`,
  `cycle_word_length_ge_eleven`; ledger `J-even-count-le-three`);
- two-even leftover families \(O^{k-2}EE\) and \(O^{k-3}EOE\) —
  **EXACT — LEAN VERIFIED** (Paper A Theorem 3.12; ledgers
  `J-two-even-leftover-ee`, `J-two-even-leftover-eoe`);
- first-even transport of gapped three-even leftovers on a cycle
  minimum —
  **EXACT — LEAN VERIFIED** (Paper A Theorem 3.13; CycleMin only);
- bunched families \(O^aEEE\), \(O^aEOEE\), \(O^aEOOEE\),
  \(O^aEOOOEE\), \(O^aEEOE\), \(O^aEOEOE\), and \(O^aEOOEOE\) —
  **EXACT — LEAN VERIFIED** (Paper A Theorems 3.14--3.20);
- gapped leftovers as cycle words —
  **EXACT — LEAN VERIFIED** (Paper A Theorem 3.21);
- finance inequality at a cycle minimum —
  **EXACT — LEAN VERIFIED** (Paper A Theorem 4.4; `cycleMin_finance`);
- per-length exclusion given a floor —
  **EXACT — HUMAN PROOF** (Paper A Corollary 4.5);
- verified computation at floor \(10^6\) —
  **COMPUTATIONALLY VERIFIED** (Paper A Theorem 4.6; no period
  \(\le 1053\); \(397\) exceptions through \(10^5\));
- cycle surplus \(\Delta_w(n)=n^{3^{\#O(w)}}-n^{2^{|w|}}\) and the
  per-step slack-scale bound \(x^e<(J(x)+1)^2\) —
  **EXACT — LEAN VERIFIED** (`image_eq_start_defectRatio`,
  `one_plus_eta_lt_succ_sq`);
- certified four-block expanding chain
  \(1999\to5169\to50093\to193753\to887471\) —
  **EXACT — LEAN VERIFIED** (`four_block_pe_1999`);
- horizon-\(20\) first-return census through \(N=10^6\) —
  **COMPUTATIONALLY VERIFIED** with exact Python integers and zero unresolved
  cases;
- \(|S_O(N)|\ll N^{5/6}\) on ambient odd inputs —
  **EXACT — HUMAN PROOF** using classical tools;
- automatic discrepancy transfer to Juggler-generated sets —
  **REFUTED** in the tested form;
- universal termination, irreducibility, or no-compression theorem —
  not claimed.

## Experiments

The publication audit reran the horizon-\(20\) census without a bit-size
cutoff. The horizon-\(40\) probe remains capped and outside the paper.
Laboratory context remains in:

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

The census consolidation added
`formal/Problems/Juggler/SmallCycleCensus.lean`
(`no_cycle_word_length_le_six`, later `no_cycle_word_length_le_seven`).
The length-seven leftovers reuse `LeftoverEval.lean` / `LeftoverCycles.lean`
with a `Fin 14` table; the census assembly itself adds no
`native_decide` table. The discrepancy consolidation added
`formal/Problems/Juggler/GapCells.lean`
(`floor_add_eq_add_carry`, `floor_gap_eq_carry`, `seq_floor_gap`,
`seq_floor_gap_second`, `floor_odd_iff_half_le_fract_half`): the exact
floor reductions under Paper B, over the reals, including the
double-gap identity used by the kernel theorem; the analytic estimates
themselves are human proofs and stay outside Lean. The Paper A review
object is `formal/Problems/JugglerPaper.lean` and does not import
`GapCells` or `CycleHeightFinance`. It imports `CycleFinance` for
Theorem 4.4, the leftover-family modules
`LeftoverTwoEven`, `FirstETransport`, `BunchedEEE`, `BunchedEOEE`,
and `BunchedEOOEE`, and `EvenCountThree` for Theorem 3.22. The formal map is
[juggler_finite_dynamics_formalization.md](../theory/juggler_finite_dynamics_formalization.md).
The paper-central theorem metadata is recorded in
`docs/theory/theorem_ledger.json` and the generated ledger. No `sorry` or
`admit`.

## Results

The publication stack was split into two manuscripts on external
review (August 2026): the single note tried to be both a Lean-backed
finite-dynamics note and an analytic discrepancy paper, and the
review's verdict was to ship the former and rewrite the latter to
standalone checkability. The stack now consists of:

- [Paper A](../theory/juggler_finite_dynamics_note.md) — power
  envelopes, exact defects, cycle restrictions, the small-cycle
  census (Theorems 3.6 and 3.8), leftover families
  (Theorems 3.12--3.21), even-count assembly (Theorem 3.22:
  period at least eleven), finance (Theorems 4.4--4.6), short
  certificates as a remark. The complement of those
  certificates is the odd-to-odd class. Lean is an independent
  check except Theorem 4.6; no density claims; leftover
  \(84\) is Appendix A companion; submission candidate;
- [Paper B](../theory/juggler_parity_discrepancy_note.md) — parity
  equidistribution of nested floor powers: exact linearization,
  the kernel theorem (Theorem 5.3, \(\delta=1/96\), at
  Graham–Kolesnik length with the level-2 wave Lemma 5.2 as a
  standalone statement and Step 5b repaired by global sublevel
  splitting), depth-4 completeness over odd starts (Theorem 6.1,
  full passenger inventory), densities \(3/4\) and \(13/16\) as
  corollaries (4.2, 4.9), the Terras-style reduction
  (Proposition 7.1), and the level-3 frontier (Conjectures 7.3/7.5,
  Proposition 7.4). The former length-5/7/8 splits and densities
  \(7/8\), \(57/64\), \(29/32\) were withdrawn in the Phase-26
  referee response (ledger `CONJECTURE` rows with recorded holes).
  Includes a proved branch-consistency lemma (3.6) and a genuine
  related-work section; no laboratory narration or machine gates
  inside proofs. Working draft;
- [reviewer packet](../theory/juggler_finite_dynamics_reviewer_packet.md)
  (two-paper claim map);
- [formalization map](../theory/juggler_finite_dynamics_formalization.md);
- [curated branch ledger](../juggler_branch_ledger.md).

None of the densities is a density of all descent certificates nor a
\(\operatorname{ReachesOne}\) density.

## Open questions

Do almost all odd-to-odd starts have a finite descent certificate?
Equivalently, by Paper B's Proposition 7.1, does parity
equidistribution hold at all depths — beginning with the level-3
kernel bound (Conjecture 7.3), whose distilled deterministic form is
the pure amplitude-product model (Conjecture 7.5)?

## Decision

**PROMOTE** Paper A as the submission candidate. Paper B stays a
**working draft with a frozen claim set**. A later write-up closed
the publication-readiness gaps that did not change the theorems:
Step 5b now names the interpolant
\(\Phi=a\nu^{5/4}+b\nu^{11/8}+w\nu^{3/2}\) and expands the
\(J_F\) replacement in the second derivative, not in the phase;
Theorem 6.1 Step E estimates the decorated composites at
\(\lambda_a'\) and \(\lambda_0'\); Corollary 4.9 is restricted to
\(E\), \(OE\), \(OOEE\); Proposition 7.1 is \(O\)-rooted;
Proposition 3.1 is written out; Vaaler, Weyl, and
\(T\ge8(1+|B|)\) are aligned. The claim set is unchanged.

Best next question: one independent human check of Paper B's
Section 5 by someone who did not write it.

## Publication assessment

Status: Paper A `PAPER_CANDIDATE`; Paper B `WORKING_DRAFT`
(post-Phase-26; claim set frozen at depth 4 + kernel + conditional
implication, \(\delta=1/96\); pending one independent check of
Section 5).

Paper A is a cycle-length note titled *Lower bounds for
nontrivial cycles of the Juggler map*: finance plus the published
floor \(10^6\) give Theorems A and B (\(L\ge 1054\); \(397\)
admissible lengths through \(10^5\)); the even-count assembly is
Theorem C. Section 4 is the financing inequality. The envelope
is the tool. Short certificates are a remark in Section 5.
Leftover \(84\) is a laboratory companion, not a paper theorem.
Related work now includes Pickover 2002, Weisstein, and OEIS
A094716. The Smith letter and the 2026 webpage record through
\(7\,110\,200\) were dropped from the note. Python listings were
removed from the body.

Paper B carries the analytic novelty (exact linearization of nested
floor powers; the level-2 kernel theorem) and the risk: external
review judged the previous six-step kernel sketch "a plan, not a
proof". The split version isolates the level-2 wave bound as
Lemma 5.2 with the explicit third differencing, balance, and
dominance checks, adds the branch-consistency identity as a proved
lemma, adds a real related-work section (Piatetski–Shapiro, Leitmann,
Rivat–Sargos, Rivat–Wu, Mauduit–Rivat, Morgenbesser,
Müllner–Spiegelhofer, Bergelson–Leibman, Baker et al., Beatty),
moves every density after the theorems, and confines numerics to a
software note. The Phase-25 expansion corrected the mixed-piece
model and the kernel exponent (\(\delta=1/72\to1/96\)); the Phase-26
referee response repaired Step 5b (global sublevel splitting with a
trivial transition bound), added the parity-reindexing lemma,
rewrote Theorems 4.4 and 6.1 as full proofs, withdrew the
length-5/7/8 harvest, corrected Proposition 7.4's quantification,
and stripped every machine gate and Lean identifier from the
analytic text (the validators `master_identity_check` and
`kernel_margin_scan` remain repository checks). Remaining gate
before candidate status: one independent human check of Section 5.
