# Juggler bracket nil-lift (the tower phase is a Heisenberg coordinate)

Status: **PROMOTE** (exact identity recorded; the rate-free tower
conjecture gains a precise nil-orbit formulation; the remaining open
step is a single ergodic transfer along a floor-Hardy orbit)

Successor of [juggler_k3_rate_free](juggler_k3_rate_free.md), taking
up its best next question: can the nil-lift that absorbs polynomial
brackets absorb \(v^{3/4}\{v^{3/2}\}\), or does floor-removal
self-similarity add a fourth, ergodic layer to the wall? Answer at
the algebraic level: **the lift applies verbatim** — the polynomial
hypothesis in Bergelson–Leibman is consumed only by the
equidistribution theorem applied *after* the lift, never by the lift
itself. Not an equidistribution theorem, not a K3 bound, not a
Paper B edit.

## Problem

Whether the depth-3 tower phase \(\{z^{3/2}\}\) — the K3 kernel's
argument — is a coordinate of an explicit nilmanifold orbit, so that
the rate-free target's species (ergodic, bracket-Hardy) becomes a
concrete orbit statement instead of an analogy.

## Exact statement

**Identity (EXACT — HUMAN PROOF,
`J-tower-heisenberg-coordinate`).** Let \(v=\lfloor n^{3/2}\rfloor\),
\(B=v^{3/2}\), \(z=\lfloor B\rfloor\), \(\theta=\{B\}\), and
\(A=\tfrac32 v^{3/4}\). Then

\[
z^{3/2}=v^{9/4}-A\theta+r,\qquad
0\le r=\tfrac38\,\theta^2\,\xi^{-1/2}\le\tfrac38\,\theta^2 z^{-1/2},
\quad\xi\in(z,B),
\]

by the exact Lagrange form of the second-order Taylor expansion of
\(x\mapsto x^{3/2}\) at \(B\) (the mechanism of Paper B's Lemma 7.2).
Since \(A\theta=AB-A\lfloor B\rfloor\) and \(AB=\tfrac32 v^{9/4}\)
stays inside the Hardy monomial family,

\[
\{z^{3/2}\}=\Bigl\{-\tfrac12 v^{9/4}
+\tfrac32 v^{3/4}\lfloor v^{3/2}\rfloor+r\Bigr\},
\]

and \(\tfrac32 v^{3/4}\lfloor v^{3/2}\rfloor \bmod 1\) is exactly the
vertical Mal'cev coordinate of the Heisenberg orbit
\(g(n)\Gamma\) with
\(g(n)=\begin{pmatrix}1&A(n)&0\\0&1&B(n)\\0&0&1\end{pmatrix}\):
right-multiplying by \(\gamma\in\Gamma\) with the integer entry
\(-\lfloor B\rfloor\) reduces the \(y\)-coordinate to \(\{B\}\) and
deposits \(-A\lfloor B\rfloor\) in the \(z\)-entry; reducing \(x\)
and \(z\) completes the Mal'cev normal form. The lift is pure group
algebra, valid for arbitrary real \(A,B\).

**Consequence.** Up to the explicit \(O(n^{-9/8})\) error \(r\), the
depth-3 tower phase is a coordinate of an orbit on
\(\mathbb T\times H_3(\mathbb R)/H_3(\mathbb Z)\) whose horizontal
torus is \(\bigl(\tfrac32 v^{3/4},\,v^{3/2},\,\tfrac12
v^{9/4}\bigr)\bmod 1\). The amplitude-product class dissolves: no
amplitude ever multiplies a harmonic in the horizontal data (the
harmonics are fixed integers), so Proposition GG's amplitude-drift
mechanism does not apply to the base by construction. What remains
open is the ergodic transfer: equidistribution of this specific
floor-Hardy orbit, with the bracket coordinate's discontinuity
handled as in Bergelson–Leibman (Riemann-integrable observables).

## Current literature

Project relationship: **extended** (gives the lab's rate-free target
its exact nil-orbit formulation; the polynomial-entry counterpart is
KNOWN).

- Bergelson–Leibman: bounded generalized polynomials are exactly the
  piecewise-polynomial coordinates of polynomial nil-orbits; the
  Heisenberg representation of \(A\lfloor B\rfloor\bmod 1\) is the
  depth-1 case. Their equidistribution theorem needs polynomial
  entries — that, and only that, is what the tower lacks.
- Leibman 2005 (polynomial orbits equidistribute in nilmanifolds,
  horizontal criterion); Green–Tao 2012 (quantitative version).
- Frantzikinakis 2009; Richter 2022; Tsinas 2023: Hardy-field
  sequences in nilmanifolds, with an integer-part removal step —
  covers Hardy entries *in the orbit position* but not the nested
  floor-power tower.
- The lab's Theorem R (`J-kernel-cancellation`): the depth-2 kernel
  with power savings — evidence that fixed-harmonic Hardy pair
  statements at these exponents are within reach of the classical
  toolkit.

## Branch budget

- **Target:** is \(\{z^{3/2}\}\) an explicit nilmanifold-orbit
  coordinate — does the Heisenberg lift survive Hardy entries?
- **Novelty hypothesis:** the lift is algebra, not equidistribution;
  \(AB=\tfrac32 v^{9/4}\) stays in the monomial family, so the
  bracket dissolves into fixed-harmonic data plus one open transfer.
- **Falsifier:** (a) the two-term expansion fails its exact error
  bound; (b) the horizontal triple resonates (non-uniform); (c) the
  Heisenberg vertical correlates with the abelian coordinate.
- **Existing machinery:** Lemma 7.2-style linearization, the
  k3_rate_free census tooling, exact scaled-integer roots, Theorem R.
- **Maximum Phase-0 scope:** exact expansion witnesses; horizontal
  triple census; fixed-harmonic Weyl grid; vertical/abelian pair
  census; records. No equidistribution proof attempt, no Lean, no
  Paper B edit.
- **Promotion criterion:** the identity is exact and the censuses
  clean — the active conjecture gains a nil-orbit formulation.
- **Stop criterion:** any falsifier fires → the route is refuted and
  the wall gains its fourth (ergodic) layer.

## Balanced-ternary formulation

None required; the objects live on \(\mathbb T\) and the Heisenberg
nilmanifold.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Exact scaled-integer roots
  (\(\lfloor\sqrt m\cdot 10^d\rfloor\), \(\lfloor m^{1/4}\cdot
  10^d\rfloor\) via nested `isqrt`) — every fractional part exact to
  \(10^{-d}\) before any float. **EXACT.**
- Taylor witness ratio \(r\sqrt z/\theta^2\) — sharp at \(3/8\).
  **COMPUTATIONALLY VERIFIED** (worst observed exactly \(0.375\);
  a 22-digit first pass showed apparent violations up to \(274\) —
  both were precision artifacts: big-int float subtraction, then
  \(\theta\)-truncation amplified by \(A\approx 1.8\cdot 10^7\);
  30 digits and single-integer combination fix both, and mpmath
  ground truth confirms \(0.37499\ldots\) at every flagged \(n\)).
- Fixed-harmonic Weyl sums over the horizontal triple — max
  \(|S_k|/\sqrt N=2.11\) over all \(124\) harmonics \(|k|\le 2\),
  square-root scale. **COMPUTATIONALLY VERIFIED.**
- Vertical/abelian joint census — uniform (max deviation \(0.080\)
  vs allowance \(0.109\) on \(16^2\) cells). **COMPUTATIONALLY
  VERIFIED.**

## Experiments

- Probe: `research.juggler_sequence.bracket_nil_lift`
- Artifact: `data/research/juggler/bracket_nil_lift/summary.json`
- Tests: `tests/research/juggler_sequence/test_bracket_nil_lift.py`

Science window: dyadic \((10^6,2\cdot 10^6]\), \(5\cdot 10^5\) odd
starts; expansion witnesses at 30 scaled digits; censuses and Weyl
grid at 22. Tests use a \(4\cdot 10^4\) window.

## Conjectures

The active record `juggler_tower_rate_free_equidistribution` now
carries the nil-orbit formulation: rate-free equidistribution of the
orbit \(\bigl(\tfrac32 v^{3/4},v^{3/2},0\bigr)\) on the Heisenberg
nilmanifold jointly with \(\tfrac12 v^{9/4}\) on \(\mathbb T\)
implies the depth-4 parity split, hence (with the analogous lifts at
higher depth) the rate-free reduction's hypothesis. No new
conjecture record: this is the same target, sharpened.

## Counterexamples

None. All three falsifiers passed on the science window.

## Formalization

None, deliberately. The identity is three lines of calculus plus the
Heisenberg group law; Lean-ifying Mal'cev coordinates for one
identity is machinery gravity ahead of the ergodic theorem that
would consume it.

## Results

Classification **BRACKET_NIL_LIFT_GREEN**.

- **Identity (EXACT — HUMAN PROOF):**
  \(\{z^{3/2}\}=\{-\tfrac12 v^{9/4}+\tfrac32 v^{3/4}\lfloor
  v^{3/2}\rfloor+r\}\) with \(0\le r\le\tfrac38\theta^2 z^{-1/2}\);
  the middle term is a Heisenberg vertical Mal'cev coordinate. The
  Taylor constant is attained: worst witness exactly \(0.375\).
- **Species conversion:** amplitude-product \(\to\) fixed-harmonic
  pair + nil-transfer. GG's drift mechanism cannot see the
  horizontal base; BB's differencing and JJ's de-randomization are
  not invoked anywhere.
- **Empirical face:** horizontal triple uniform
  (\(512/512\) cells, max deviation \(0.103\) vs \(0.161\)); all
  \(124\) fixed harmonics at square-root scale (max \(2.11\sqrt N\),
  worst harmonic \((0,-1,0)\)); vertical/abelian pair uniform.

## Open questions

- The single remaining open step of the rate-free route:
  equidistribution of the floor-Hardy orbit
  \(n\mapsto\bigl(\tfrac32 v^{3/4},v^{3/2},0\bigr)\Gamma\times
  \tfrac12 v^{9/4}\) — a concrete instance of the (unbuilt)
  Hardy-field bracket theory. Exportable as stated.
- Whether the horizontal triple's fixed-harmonic Weyl sums fall to
  the lab's existing van der Corput / Theorem-R machinery (the
  entries are Hardy monomials of \(v=\lfloor n^{3/2}\rfloor\) at
  exponents \(3/4,3/2,9/4\); harmonics fixed, no drift). If so, the
  horizontal half of the nil-route is a theorem and only the
  transfer step remains.
- The same lift iterates: depth-\(k\) tower phases are coordinates
  of orbits on products of \(\mathbb T\) and Heisenberg factors
  (each floor removal spends one two-term Taylor and one vertical
  coordinate). Not pursued: depth 3 is the K3 frontier.

## Decision

**PROMOTE.** The identity is exact, the falsifiers all passed, and
the active tower conjecture now has a nil-orbit formulation instead
of a species analogy: the wall's fourth layer did **not**
materialize at the algebraic level — floor-removal self-similarity
is absorbed by the group structure exactly as in the polynomial
case, and only the ergodic transfer along this specific floor-Hardy
orbit remains open. Best next question: do the fixed-harmonic Weyl
sums of the horizontal triple \(\bigl(\tfrac32
v^{3/4},v^{3/2},\tfrac12 v^{9/4}\bigr)\bmod 1\) admit power savings
by the existing depth-2 machinery (Theorem R's van der Corput chain
on Hardy monomials of \(v\)) — i.e. is the horizontal half of the
nil-route already a theorem?

## Publication assessment

Status: `STRUCTURAL`. The identity is elementary but the reduction
it effects (amplitude-product \(\to\) nil-orbit) is the right
exportable formulation of the K3 frontier; it belongs in any future
problem note alongside Conjecture HH.
