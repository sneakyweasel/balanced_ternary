# Juggler Heisenberg cut (the vertical is Riemann-integrable; no fourth layer at regularity)

Status: **PROMOTE** (the fourth ergodic layer, at observable
regularity, is exactly cut-charging of \(\{m^{3/2}\}\), and the cut
is not charged; characteristic-factor self-similarity stays
external)

Successor of [juggler_bracket_nil_lift](juggler_bracket_nil_lift.md)
and the leftover classification
[juggler_horizontal_weyl](juggler_horizontal_weyl.md), taking up
the regularity half of the recorded best next question: does the
Hardy-field bracket calculus absorb the Heisenberg vertical
\(\tfrac32 m^{3/4}\lfloor m^{3/2}\rfloor\bmod 1\) as a
Riemann-integrable nil-observable, or does the discontinuous fiber
add a fourth ergodic layer? Answer at the regularity level: **no
fourth layer.** The ambient fact is classical; the
project-specific reduction is that the only regularity obstruction
is cut-charging of \(\{m^{3/2}\}\). Not an equidistribution
theorem, not a characteristic-factor argument, not a Paper B edit.

## Problem

Whether the vertical Mal'cev coordinate of the nil-lift orbit is a
Riemann-integrable observable along that orbit, or whether the
floor discontinuity produces a new wall.

## Exact statement

**Lemma (EXACT — HUMAN PROOF,
`J-heisenberg-vertical-riemann`).** Let
\(X=H_3(\mathbb R)/H_3(\mathbb Z)\) with Mal'cev fundamental domain
\([0,1)^3\). The \(z\)-coordinate \(\chi:X\to\mathbb T\) is bounded
and discontinuous only on the faces, a Haar-null set, hence
Riemann integrable on \(X\). The identity of
`J-tower-heisenberg-coordinate` says
\[
n\mapsto\bigl\{\tfrac32 m^{3/4}\lfloor m^{3/2}\rfloor\bigr\}
=\chi\bigl(g(n)\Gamma\bigr),
\]
\(g(n)=\exp(A\,e_{12}+B\,e_{23})\), \(A=\tfrac32 m^{3/4}\),
\(B=m^{3/2}\), \(m=\lfloor n^{3/2}\rfloor\). The same continuous
sandwich already used for the hug observable (Paper A, Prop 5.5)
therefore yields: Haar equidistribution of \(g(n)\Gamma\) implies
equidistribution of the vertical, provided the orbit does not
charge the face \(\{y=0\}\). That face is \(\{B\}\in\mathbb Z\),
i.e. \(\{m^{3/2}\}=0\).

**Consequence.** At observable regularity the fourth ergodic layer
is exactly *cut-charging of \(\{m^{3/2}\}\)*. It is not a new
structural obstruction and it is not characteristic-factor
self-similarity (that recorded falsifier remains external).

**Exact hits.** If \(m=k^2\) then \(B=k^3\in\mathbb Z\), so the
orbit lands on the face. These landings are a thin set (order
\(P^{1/4}\) in a dyadic window of odd starts) and do not charge
Haar. They are not an atom.

## Current literature

Project relationship: **extended** (names the regularity
obstruction for this orbit; the ambient RI fact is KNOWN).

- Bergelson–Leibman: generalized polynomials are Riemann-integrable
  nil-observables; equidistribution of the orbit passes to them
  when the discontinuity set is not charged.
- Paper A Prop 5.5 already invokes the \(C^0\to\) RI extension for
  the hug function (monotone, one wrap jump).
- Frantzikinakis 2009: integer-part removal for Hardy entries in
  the *orbit position*, not a license to ignore a charged cut.
- The algebraic lift (`J-tower-heisenberg-coordinate`) identified
  the vertical; it did not discuss the face.

## Branch budget

- **Target:** is the vertical RI along the floor-Hardy orbit, or
  does the cut add a fourth layer?
- **Novelty hypothesis:** the cut is Haar-null; if \(\{m^{3/2}\}\)
  does not concentrate at \(0\), there is no regularity wall.
- **Falsifier:** (a) atom / heavy tail of \(\{m^{3/2}\}\) at \(0\);
  (b) vertical law on the cut differs from the bulk; (c) the claim
  is already KNOWN packaging of the nil-lift → CLOSE.
- **Existing machinery:** nil-lift identity, `bracket_nil_lift`
  scaled roots, Paper A Prop 5.5 sandwich.
- **Maximum Phase-0 scope:** the implication; cut-mass and
  cut-conditioned vertical censuses; records. No equidistribution
  proof, no Lean, no Paper B, no characteristic-factor work.
- **Promotion criterion:** the implication is exact and the cut
  is not charged — the fourth layer does not appear at
  regularity.
- **Stop criterion:** (a) or (b) fires, or (c) is all the
  branch produced.

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Two-sided cut mass
  \(\#\{\mathrm{dist}(\{B\},\mathbb Z)<\varepsilon\}/(2\varepsilon N)\).
  Uniform predicts \(1\). **COMPUTATIONALLY VERIFIED.**
- Exact zeros of \(\{B\}\) \(\Leftrightarrow\) \(m\) a square.
  **EXACT** (and **COMPUTATIONALLY VERIFIED**: 4 hits on
  \(5\cdot10^5\) odd starts, order \(P^{1/4}\)).
- TV distance of the 16-bin vertical law on
  \(\{\mathrm{dist}<0.02\}\) vs the complement.
  **COMPUTATIONALLY VERIFIED.**

## Experiments

- Probe: `research.juggler_sequence.heisenberg_cut`
- Artifact: `data/research/juggler/heisenberg_cut/summary.json`
- Tests: `tests/research/juggler_sequence/test_heisenberg_cut.py`

Science window: dyadic \((10^6,2\cdot10^6]\), \(5\cdot10^5\) odd
starts. Tests use a \(4\cdot10^4\) window plus synthetic atom /
independence checks.

## Conjectures

None new. `juggler_tower_rate_free_equidistribution` is unchanged:
rate-free equidistribution of the floor-Hardy nil-orbit still
suffices. The vertical is now a legitimate RI observable of that
orbit, not a second species.

## Counterexamples

None. No atom (cut-mass ratios \(1.081\) down to \(1.005\) along
the \(\varepsilon\)-ladder, all inside the Poisson cap). Vertical
TV on the cut \(0.012\) vs allowance \(0.084\); abelian control
\(0.008\). Four exact square landings, not an atom.

## Formalization

None. The implication is the standard RI sandwich plus the
already-recorded lift identity. Lean-ifying Haar-null faces is
machinery gravity.

## Results

Classification **HEISENBERG_CUT_GREEN**.

- **Implication (EXACT — HUMAN PROOF):** Haar equidistribution of
  \(g(n)\Gamma\) passes to the vertical iff \(\{m^{3/2}\}\) does
  not charge \(0\). That is the whole regularity content of the
  fourth layer.
- **No charge (COMPUTATIONALLY VERIFIED, finite window):** cut
  mass tracks \(2\varepsilon\); the fiber law does not jump;
  exact hits are the square-\(m\) law.
- **Not claimed:** equidistribution of the orbit;
  characteristic-factor regularity; a theorem that
  \(\{m^{3/2}\}\) is equidistributed for all \(N\).

## Open questions

- The remaining open of the rate-free route is still
  equidistribution of the floor-Hardy orbit. The
  \(\{v^{9/4}\}\) identification without \(\theta\)-unwind is
  answered by
  [juggler_v94_rate_free.md](juggler_v94_rate_free.md): **CLOSE**
  (published Hardy-nil doors miss; qualitative van der Corput
  is integer dilation of \(\{v^{5/4}\}\)). External composition
  lemma; not a laboratory method.
- Characteristic-factor self-similarity of floor-removal remains
  the named route-falsifier and is also external.

## Decision

**PROMOTE.** The recorded question is answered at the level it
could be answered in Phase 0: the discontinuous fiber does not
add a fourth layer at observable regularity. The ambient RI fact
is KNOWN; the project-specific reduction (fourth layer = cut-charge
of \(\{m^{3/2}\}\), and the cut is not charged on the window) is
the surviving statement. Best next question: does a rate-free
argument identify the floor-Hardy orbit — in particular
\(\{v^{9/4}\}\) without unwinding through \(\theta\) — or is that
still the unbuilt Hardy-field door? (The same question the
horizontal-species pass named; not opened here.)

## Publication assessment

Status: `STRUCTURAL`. A short exact implication plus a census.
Belongs next to the nil-lift identity in a problem note; not a
paper claim.
