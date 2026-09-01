# Juggler three-term lift of \(\{v^{9/4}\}\) (Lemma G in Heisenberg language)

Status: **CLOSE** (the three-term identity is Lemma G; the linear
leftover's Heisenberg packaging does not cite Richter; the door is
still the unbuilt composition the sibling named)

Follow-up of [juggler_v94_rate_free](juggler_v94_rate_free.md)
(**CLOSE**): that placement record showed published Hardy-nil
theorems miss \(\{v^{9/4}\}\) and the two-term leftover
\(\tfrac94 n^{15/8}\theta\) is not \(o(1)\). This pass asked whether
one more Taylor term plus a Hardy-entry Heisenberg lift changes
that. Answer: the remainder becomes \(o(1)\), and the identity is
`J-second-order-linearization` (Lemma G) for \(m^{9/4}\). Not a
new theorem, not a K3 bound, not a Paper B edit, and not a
citation of Richter.

## Problem

Whether a rate-free identification of \(\{v^{9/4}\}\) exists that
does not treat the linear leftover as an amplitude-product, or
whether continuing Taylor still lands on the unbuilt Hardy-of-floor
composition.

## Exact statement

**Identity (REPARAMETERIZATION of `J-second-order-linearization`).**
Let \(X=n^{3/2}\), \(v=\lfloor X\rfloor\), \(\theta=\{X\}\). Taylor
of \(x\mapsto x^{9/4}\) at \(X\) through the quadratic term gives

\[
v^{9/4}
= n^{27/8}-\tfrac94 n^{15/8}\,\theta
+\tfrac{45}{32}n^{3/8}\,\theta^2+R_3,
\qquad
\lvert R_3\rvert\le\tfrac{15}{128}\,v^{-3/4}\theta^3=O(n^{-9/8}).
\]

Packaging the linear leftover as \(A\theta=AB-A\lfloor B\rfloor\)
with Hardy entries \(A=\tfrac94 n^{15/8}\), \(B=n^{3/2}\), then
substituting \(\theta=X-v\) throughout, recovers Lemma G:

\[
v^{9/4}
=\tfrac{5}{32}n^{27/8}-\tfrac{9}{16}n^{15/8}\,v
+\tfrac{45}{32}n^{3/8}\,v^2+R_4,
\]

with the recorded cubic remainder (Lemma G bounds
\(\lvert R_4\rvert\le\tfrac{15}{128}(X-1)^{-3/4}\); the
\(\theta^3\) form above is the same Lagrange term before
\(\theta\le 1\)).

The two-term leftover of `J-horizontal-axis-species` is not
\(o(1)\) — that is the sibling's point, and it stands. Continuing
Taylor makes the *remainder* \(o(1)\) and lands on a quadratic
polynomial in \(\lfloor n^{3/2}\rfloor\) with Hardy coefficients.
That is exactly the missing composition
\(a^{f(\lfloor h(n)\rfloor)}\) named in
[juggler_v94_rate_free](juggler_v94_rate_free.md). The Heisenberg
language for the linear term does not move the instance into
Richter 2023 (Hardy times) or Frantzikinakis 2009 (floor in the
time slot of a fixed nilrotation).

## Current literature

Project relationship: **reproduced** (Lemma G) / **known** (the
sibling's mismatch table).

- `J-second-order-linearization` (Lemma G): the \(m^{9/4}\)
  identity above, already in the ledger.
- [juggler_v94_rate_free](juggler_v94_rate_free.md): Richter /
  Frantzikinakis / Boshernitzan miss \(\{v^{9/4}\}\); qualitative
  van der Corput is integer dilation of \(\{v^{5/4}\}\).
- `J-horizontal-axis-species`: two-term leftover is HH; one Weyl
  step is GG. Not re-tested.
- `J-nested-floor-without-W-family` (REFUTED): the identity does
  not replace \(\{v^{9/4}\}\) by \(\{n^{27/8}\}\).

## Branch budget

- **Target:** can \(\{v^{9/4}\}\) be written as a nil-orbit with
  Hardy (floor-free) entries plus \(o(1)\), so published Hardy-nil
  theorems apply?
- **Novelty hypothesis:** 3-term Taylor plus the Heisenberg lift of
  \((n^{15/8},n^{3/2})\) dissolves the linear leftover; the
  \(\theta^2\) term is tame.
- **Falsifier:** the identity is Lemma G; or the remainder is not
  \(o(1)\); or the lift recreates \(A'\gg 1\) as the *whole*
  leftover.
- **Existing machinery:** Lemma G, `J-horizontal-axis-species`,
  the sibling placement record, scaled roots.
- **Maximum Phase-0 scope:** exact 3-term remainder; match against
  Lemma G; passenger \(A'\); Hardy-pair occupancy. No K3, no
  Paper B, no Lean, no equidistribution claim.
- **Promotion criterion:** exact reduction to a published Hardy-nil
  orbit that the sibling missed.
- **Stop criterion:** KNOWN reparameterization of Lemma G, or the
  remainder cannot be \(o(1)\).

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Three-term Lagrange remainder
  \(\lvert R_3\rvert\le\tfrac{15}{128}v^{-3/4}\theta^3\).
  **EXACT — HUMAN PROOF** (Lemma G). Bound attained
  (\(15/128\)). **COMPUTATIONALLY VERIFIED.**
- Heisenberg packaging of the linear leftover. **REPARAMETERIZATION**
  of the substitution \(\theta=X-v\) already in Lemma G.
- Passenger \(A_2\sim n^{3/8}\), \(A_2'\sim n^{-5/8}\ll 1\).
  **EXACT** (exponents of the Lemma G quadratic term).
- Joint occupancy of \(\bigl(\{n^{15/8}\},\{n^{3/2}\}\bigr)\).
  **OBSERVATION** (finite window; not used as a theorem).

## Experiments

- Probe: `research.juggler_sequence.v94_hardy_lift`
- Artifact: `data/research/juggler/v94_hardy_lift/summary.json`
- Tests: `tests/research/juggler_sequence/test_v94_hardy_lift.py`

Science sample: odd \(n\) in \(\{5,7,\ldots,499\}\) plus
\(10^{4}+1,10^{6}+1\) (remainder ratio attains \(15/128\);
\(\lvert R_3\rvert\le 1.1\cdot10^{-18}\) at \(n\ge10^{6}\));
\(A_2'\) leading \(0.530\) vs \(135/256\); Hardy pair occupies
\(64/64\) cells on \(20\,000\) odd starts in
\((4\cdot10^{4},8\cdot10^{4}]\). Tests use a shorter sample.

## Conjectures

None new. `juggler_tower_rate_free_equidistribution` stays ACTIVE.
The sibling's composition gap is unchanged. Conjectures V/HH stay
PARKED.

## Counterexamples

None. The remainder *is* \(o(1)\) after three terms — that does
not open a published door. The novelty hypothesis died by
reparameterization (Lemma G), not by a failed bound.

## Formalization

None. Lemma G is already recorded; Lean-ifying a packaging is
machinery gravity.

## Results

Classification **V94_HARDY_LIFT_GREEN** (computational witnesses
only).

- The cubic remainder bound holds and is attained. At
  \(n\ge10^{6}\), \(\lvert R_3\rvert\le 1.1\cdot10^{-18}\).
- After substituting \(\theta=X-v\), the identity is Lemma G for
  \(m^{9/4}\). No new ledger row.
- The passenger / quadratic term is tame (\(A'\to 0\)). That is
  the exponent of Lemma G's \(m^2 n^{3/8}\) coefficient, not a
  new species.
- Published Hardy-nil theorems still miss \(\{v^{9/4}\}\) (sibling
  table). Richter is not cited.
- Not claimed: equidistribution; density-one; a K3 bound.

## Open questions

None from this door. The live target remains the rate-free
conjecture as the external composition
\(a^{f(\lfloor h(n)\rfloor)}\). Characteristic factors are not
opened.

## Decision

**CLOSE.** A rate-free argument does **not** identify
\(\{v^{9/4}\}\) without unwinding through \(\theta\), and the
unbuilt Hardy-field door is still the door. Continuing Taylor
makes the remainder \(o(1)\) and recovers Lemma G — a polynomial
in \(\lfloor n^{3/2}\rfloor\) with Hardy coefficients — which is
the missing composition the sibling already named. The two-term
HH leftover not being \(o(1)\) stands; it is not an invitation to
cite Richter on the smooth model. Best next question: none from
this door; the rate-free conjecture stays ACTIVE as an external
composition problem.

## Publication assessment

Status: `ARCHIVED`. Confirmation that the three-term reading is
Lemma G. Not a paper claim.
