# Juggler nil-horizontal Weyl (Lemma G path: the horizontal half is not a theorem)

Status: **CLOSE** (independent confirmation of a classification already
in the ledger; the claim "existing depth-2 machinery already proves
the horizontal half" is `J-horizontal-theorem-r-shortcut`, REFUTED)

Successor of [juggler_bracket_nil_lift](juggler_bracket_nil_lift.md).
Runs the same question as
[juggler_horizontal_weyl](juggler_horizontal_weyl.md) by a different
expansion (Lemma G keep-\(m\), then substitute
\(m=n^{3/2}-\theta\)). Not a K3 bound, not a Paper B edit, not a
second leftover lemma.

## Problem

Whether the fixed-harmonic Weyl sums of the nil-lift horizontal
triple already sit on named Paper B bounds, or whether
\(n\)-linearization of some axis re-enters the amplitude-product
class that GG/BB block.

## Exact statement

**Lemma G substitution (EXACT — HUMAN PROOF; coefficients only).**
Nil-lift \(v=\lfloor n^{3/2}\rfloor\) is Paper B's \(m\). After
substituting \(m=n^{3/2}-\theta\) into Lemma G
(`J-second-order-linearization`):

\[
\begin{aligned}
m^{3/4}
&= n^{9/8}-\tfrac34 n^{-3/8}\,\theta+\text{decaying},\\
m^{9/4}
&= n^{27/8}-\tfrac94 n^{15/8}\,\theta+\tfrac{45}{32}n^{3/8}\theta^2+R_4.
\end{aligned}
\]

The smooth-model coefficients sum to \(1\)
(\(\tfrac5{32}-\tfrac9{16}+\tfrac{45}{32}=1\) and
\(\tfrac5{32}+\tfrac{15}{16}-\tfrac3{32}=1\)). Integer harmonics
kill integer parts: \(e(k_2 v^{3/2})=e(k_2\{m^{3/2}\})\).

**Axis catalog (already recorded).** The resulting species table is
`J-horizontal-axis-species`; the optimistic Theorem-R shortcut is
`J-horizontal-theorem-r-shortcut` (REFUTED). This branch does not
re-prove those rows. It confirms, by the keep-\(m\) route:

| Axis | After Lemma G / integer harmonics | Class |
|------|-----------------------------------|-------|
| \((\pm1,0,0)\) | decaying \(\theta\)-error; classical Weyl of \(n^{9/8}\) | cheap |
| \((0,\pm1,0)\) | \(e(k_2\{m^{3/2}\})\); Theorem R at \(\alpha=0\) not citable | Theorem C substrate |
| \((0,0,\pm1)\) | first-layer \(W\)-family at \(\alpha=15/8\in(9/8,9/4)\) | GG on \(n\)-reduction |

Drift of the \(9/4\) leftover: \(C(n)=\tfrac94 n^{15/8}\),
\(C(n+2)-C(n)\sim\tfrac{135}{16}n^{7/8}\), so the window with
drift \(\le 1\) has length \(\tfrac{32}{135}n^{-7/8}<1\) for every
odd \(n\ge 3\). BB does not fire (\(\alpha<9/4\), first layer).
`J-nested-floor-without-W-family` forbids absorbing the defect into
\(e(n^{27/8})\). Mixed harmonics inherit the leftover whenever
\(k_3\neq 0\).

## Current literature

Project relationship: **reproduced** (Lemma G path of
`J-horizontal-axis-species` / `J-horizontal-leftover-exponents`).

- Lemma G (`J-second-order-linearization`): keep-\(m\) identities.
- Sibling [juggler_horizontal_weyl](juggler_horizontal_weyl.md):
  Lagrange unwind, first-difference GG check, leftover exponents.
- Theorem R (`J-kernel-cancellation`): second-layer kernel at
  \(\alpha=9/8\), not \(\alpha=0\) and not \(e(m^{9/4})\).
- `J-w-family-below-nine-eighths` (CONJECTURE): no citation below
  \(9/8\).
- Proposition GG: \(A'\gg 1\) kills character windows.

## Branch budget

- **Target:** for each fixed \(k\in\mathbb Z^3\setminus\{0\}\), is
  \(S_k\) a named Paper B bound, or does \(n\)-linearization
  re-enter the amplitude-product class?
- **Novelty hypothesis:** the \(9/4\) axis is a first-layer
  \(W\)-family at \(15/8\) with GG-type drift; "already a theorem"
  is false.
- **Falsifier:** (a) all three axes reduce to named power-saving
  rows; (b) the \(9/4\) defect is \(o(1)\); (c) the leftover is
  second-layer or \(\alpha\ge 9/4\).
- **Existing machinery:** Lemma G, Theorem R, GG,
  `J-nested-floor-without-W-family`, the sibling leftover rows,
  nil-lift scaled roots.
- **Maximum Phase-0 scope:** coefficient identities; integer-
  harmonic check; scaled-integer defect witnesses; exponent/drift
  arithmetic. No new van der Corput proof, no Lean, no Paper B
  edit, no second leftover lemma.
- **Promotion criterion:** a new exact obstruction not already
  named.
- **Stop criterion:** the catalog matches named sibling rows →
  CLOSE.

## Balanced-ternary formulation

None required; the objects live on \(\mathbb T\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Lemma G coefficient sums after \(m=n^{3/2}-\theta\) —
  **EXACT — HUMAN PROOF** (rational identities).
- Integer-harmonic cancellation \(e(k_2 v^{3/2})=e(k_2\{v^{3/2}\})\)
  — **EXACT.** **COMPUTATIONALLY VERIFIED** on \(251\) odd starts.
- Defect ratios
  \((n^{27/8}-m^{9/4})/\bigl(\tfrac94 n^{15/8}\theta\bigr)\) and
  \((n^{9/8}-m^{3/4})/\bigl(\tfrac34 n^{-3/8}\theta\bigr)\) —
  **COMPUTATIONALLY VERIFIED** (min/max \(0.982\)–\(1.000\) and
  \(1.000\)–\(1.004\) on \(241\) used samples; \(9/4\) absolute
  defect from \(8\) to \(1.6\cdot 10^{17}\), not a remainder;
  \(3/4\) absolute defect \(<1\)).
- Drift prefactors \(\tfrac{135}{16}\) (per odd step) and
  \(\tfrac{32}{135}\) (window) — **EXACT.**

## Experiments

- Probe: `research.juggler_sequence.nil_horizontal_weyl`
- Artifact: `data/research/juggler/nil_horizontal_weyl/summary.json`
- Tests: `tests/research/juggler_sequence/test_nil_horizontal_weyl.py`

Science sample: odd \(n\in\{5,7,\ldots,499\}\) plus
\(10^6+1,10^7+1,10^9+1\) (\(241\) used after \(\theta\)-cutoff);
Lemma G reused via `second_order_scan`. Tests use a shorter
sample. No Weyl census — the nil-lift already has one.

## Conjectures

No new conjecture. The active record
`juggler_tower_rate_free_equidistribution` is unchanged in status.
The rated shortcut is already `J-horizontal-theorem-r-shortcut`
(REFUTED). Conjectures V/HH stay PARKED.

## Counterexamples

None for the identities. Falsifier (b) did not fire: the \(9/4\)
defect is not \(o(1)\). Falsifier (a) did not fire: the \(9/4\)
axis has no named power-saving bound. Falsifier (c) did not fire:
the leftover is first-layer at \(15/8<9/4\).

## Formalization

None. The coefficient identities are four rational sums; Lean
ahead of an equidistribution theorem that would consume them is
machinery gravity. The sibling rows are likewise unformalized.

## Results

Classification **NIL_HORIZONTAL_WEYL_SPLIT**.

- **Coefficients (EXACT):** Lemma G substitution recovers the
  same leading leftovers as the sibling Lagrange unwind
  (\(-\tfrac34 n^{-3/8}\theta\), \(-\tfrac94 n^{15/8}\theta\)).
- **Witnesses (COMPUTATIONALLY VERIFIED):** \(9/4\) defect ratio
  \(0.982\)–\(1.000\), not a remainder; \(3/4\) defect decays.
- **Catalog:** matches `J-horizontal-axis-species`. Theorem R
  does not prove the triple. GG re-enters every \(n\)-reduction
  of the abelian axis. No new ledger row.

## Open questions

None from this branch. The sibling's remaining question — a
rate-free identification of \(\{v^{9/4}\}\) that does not unwind
through \(\theta\) — is not opened here.

## Decision

**CLOSE.** The question is already answered:
`J-horizontal-theorem-r-shortcut` (REFUTED) and
`J-horizontal-axis-species`. This Phase-0 independently confirms
the same split by the Lemma G keep-\(m\) route and records that
the \(9/4\) defect is not a remainder. Every statement that
survives is `KNOWN` or `REPARAMETERIZATION` of those rows. Do not
add a fourth leftover lemma. Do not prove the first-layer
\(15/8\) estimate here. The Heisenberg identity and the rate-free
conjecture are untouched.

Best next question: none from this branch. The sibling's recorded
question (rate-free identification of \(\{v^{9/4}\}\) without
\(n\)-unwinding) is not opened.

## Publication assessment

Status: `ARCHIVED`. An independent confirmation, not a new
theorem and not a paper claim.
