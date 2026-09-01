# Juggler horizontal Weyl classification (the Theorem-R shortcut dies)

Status: **PROMOTE** (exact unwind identities, leftover lemma, and a
named GG/HH obstruction of the rated shortcut; the rate-free tower
conjecture stays ACTIVE)

Successor of [juggler_bracket_nil_lift](juggler_bracket_nil_lift.md),
taking up its best next question: do the fixed-harmonic Weyl sums of
the horizontal triple
\(\bigl(\tfrac32 v^{3/4},\,v^{3/2},\,\tfrac12 v^{9/4}\bigr)\)
admit power savings by Theorem R's van der Corput chain? A first
leftover-only pass (`J-horizontal-leftover-exponents`) showed BB
silent and PARKED the write-up. This pass adds the \(A'\) table and
the first-difference engine-line check: **no** — two axes reduce to
recorded or classical statements, but the abelian \(v^{9/4}\) axis
re-enters GG/HH. Not a K3 bound, not an equidistribution theorem,
not a Paper B edit.

## Problem

Whether the horizontal half of the nil-orbit formulation of
`juggler_tower_rate_free_equidistribution` is already a theorem via
existing depth-2 machinery, or whether the only available treatments
of the three monomials re-enter the amplitude-product class.

## Exact statement

**Identities (EXACT — HUMAN PROOF, `J-horizontal-axis-species`).**
Let \(X=n^{3/2}\), \(v=\lfloor X\rfloor\), \(\theta=\{X\}\) (nil-lift
\(v\) is Paper B's \(m\)). Lagrange Taylor of \(x\mapsto x^\alpha\)
at \(X\) with remainder \(\tfrac12 f''(\xi)\theta^2\),
\(\xi\in(v,X)\), gives

\[
\begin{aligned}
v^{3/4}
&= n^{9/8}-\tfrac34 n^{-3/8}\,\theta+R_{3/4},
&&-\tfrac{3}{32}v^{-5/4}\theta^2\le R_{3/4}\le 0,\\
v^{3/2}
&= n^{9/4}-\tfrac32 n^{3/4}\,\theta+R_{3/2},
&&0\le R_{3/2}\le\tfrac38 v^{-1/2}\theta^2,\\
v^{9/4}
&= n^{27/8}-\tfrac94 n^{15/8}\,\theta+R_{9/4},
&&\tfrac{45}{32}v^{1/4}\theta^2\le R_{9/4}\le\tfrac{45}{32}X^{1/4}\theta^2.
\end{aligned}
\]

The keep-\(m\) forms of the first and third are Lemma G
(`J-second-order-linearization`); they are reused, not re-proved.

**First-difference of the abelian axis.** For odd \(n\), step \(2\),

\[
v(n+2)-v(n)=\lfloor\Delta X\rfloor+\kappa,\qquad\kappa\in\{0,1\},
\]

and by the mean-value theorem
\(v(n+2)^{9/4}-v(n)^{9/4}=\tfrac94\xi^{5/4}\bigl(v(n+2)-v(n)\bigr)\).
The carry term has amplitude \(C=\tfrac94\xi^{5/4}\asymp n^{15/8}\)
(below Theorem R's engine line \(9/4\)) and derivative
\(C'\asymp n^{7/8}\gg 1\) (GG species: no drift-1 window).

**Species table.**

| Axis | \(A\) | \(A'\) | Species | Ledger match |
|------|-------|--------|---------|--------------|
| \(v^{3/4}\) | \(n^{-3/8}\) decaying | \(n^{-11/8}\) | decaying | classical van der Corput on \(e(kn^{9/8})\) |
| \(v^{3/2}\) | \(n^{3/4}\) | \(n^{-1/4}\ll 1\) | tame | Theorem C substrate; Theorem R at \(\alpha=0\) not citable (`J-w-family-below-nine-eighths` is CONJECTURE) |
| \(v^{9/4}\) unwind | \(n^{15/8}\) | \(n^{7/8}\gg 1\) | HH | forbidden by `J-nested-floor-without-W-family` |
| \(v^{9/4}\) one Weyl step | \(n^{15/8}<n^{9/4}\) | \(n^{7/8}\gg 1\) | GG | BB does not fire; GG does |

Mixed harmonics with \(k_3\neq 0\) are dominated by the \(9/4\) axis.

**Refutation (`J-horizontal-theorem-r-shortcut`).** The hypothesis
that the horizontal Weyl sums admit power savings by Theorem R's
chain is **REFUTED**. The rate-free conjecture is unharmed: it never
needed a rate.

## Current literature

Project relationship: **extended** (classifies the horizontal
coordinates of the recorded nil-orbit; the polynomial-entry
counterpart remains KNOWN; the rated shortcut is new negative
knowledge).

- `J-horizontal-leftover-exponents`: first-level leftover
  \(\alpha\in\{-3/8,3/4,15/8\}\), all below \(9/4\) (BB silent).
  Survives; this pass adds the \(A'\) / first-difference landing.
- Lemma G (`J-second-order-linearization`): keep-\(m\) identities
  for \(m^{3/4}\) and \(m^{9/4}\).
- Theorem C (`J-nested-parity-discrepancy`): the \(v^{3/2}\) axis
  is its substrate.
- Theorem R (`J-kernel-cancellation`): \(e(c\{m^{3/2}\})\) at
  \(\alpha=9/8\), not \(e(m^{9/4})\) and not \(\alpha=0\).
- `J-nested-floor-without-W-family` (REFUTED): do not replace
  nested floors by smooth powers.
- `J-w-family-below-nine-eighths` (CONJECTURE, Corollary R'
  withdrawn): Theorem R is not citable below \(\alpha=9/8\).
- Proposition GG (`J-intra-block-harmonic-obstruction`): \(A'\gg 1\)
  kills character windows. The \(v^{9/4}\) Weyl step lands here.
- Bergelson–Leibman / Frantzikinakis / Richter / Tsinas: the
  rate-free ergodic door is still unbuilt, and is not opened here.

## Branch budget

- **Target:** for each fixed harmonic of the horizontal triple, is
  the Weyl sum a recorded theorem / classical van der Corput, or
  does the only available treatment re-enter \(A'\gg 1\) (HH/GG)?
- **Novelty hypothesis:** axes \(3/4\) and \(3/2\) are cheap; the
  abelian \(9/4\) axis is the obstruction — either a PS-monomial /
  Lemma-G reduction, or a named kill of the Theorem-R shortcut.
- **Falsifier:** (a) an unwind / Lemma-G identity fails its
  remainder; (b) the \(9/4\) leftover is actually tame
  (\(A'\ll 1\)); (c) one Weyl step on \(v^{9/4}\) produces a
  \(W\)-family past \(9/4\) or \(C'\gg 1\).
- **Existing machinery:** Lemma G, Theorems C/R, the nested-floor
  REFUTED row, HH/GG, nil-lift scaled roots.
- **Maximum Phase-0 scope:** exact Taylor/Lemma-G unwinds; \(A/A'\)
  table; one first-difference engine-line check; records. No K3
  bound, no Paper B, no Lean, no new Weyl engine, no large census.
- **Promotion criterion:** a reduction lemma (some axes are
  theorems) or a named obstruction that closes the shortcut.
- **Stop criterion:** all three are KNOWN reparameterizations, or
  the classification is already in the ledger.

## Balanced-ternary formulation

None required; the objects live on \(\mathbb T\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Lagrange unwind of \(v^\alpha\) through \(\theta=\{n^{3/2}\}\)
  with explicit remainder — **EXACT — HUMAN PROOF.** Taylor
  constants attained on the sample: \(3/32\), \(3/8\), \(45/32\).
  **COMPUTATIONALLY VERIFIED.**
- Lemma G keep-\(m\) oracle (`second_order_scan`) — **EXACT —
  HUMAN PROOF**, reused.
- First-difference carry identity
  \(\Delta v=\lfloor\Delta X\rfloor+\kappa\), \(\kappa\in\{0,1\}\),
  and the mean-value enclosure of \(\Delta(v^{9/4})\) —
  **EXACT — HUMAN PROOF.** Leading ratios \(C/n^{15/8}\to 9/4\)
  and \(C'/n^{7/8}\to 135/32\). **COMPUTATIONALLY VERIFIED.**
- Engine line \(9/4\) versus spawned amplitude \(15/8\) (BB does
  not fire) and \(C'\asymp n^{7/8}\gg 1\) (GG does). **EXACT.**

## Experiments

- Probe: `research.juggler_sequence.horizontal_weyl`
- Artifact: `data/research/juggler/horizontal_weyl/summary.json`
- Tests: `tests/research/juggler_sequence/test_horizontal_weyl.py`

Science sample: odd \(n\) in \(\{5,7,\ldots,499\}\) plus
\(10^{4}+1,10^{5}+1,10^{6}+1,10^{8}+1,10^{10}+1,10^{12}+1\)
(244 used after \(\theta\)-cutoff \(10^{-8}\)); Lemma G on \(250\)
points; first-difference on \(240\) consecutive odd pairs near
\(10^{6}\) and \(10^{8}\). Tests use a shorter sample. No new Weyl
census — the nil-lift already has \(124\) harmonics at square-root
scale.

## Conjectures

The active record `juggler_tower_rate_free_equidistribution` is
unchanged in status. The rated shortcut
("horizontal half is already Theorem R") is recorded as the
REFUTED ledger row `J-horizontal-theorem-r-shortcut`, not as a
new conjecture file. Conjectures V/HH stay PARKED.

## Counterexamples

None for the identities. Falsifier (b) did not fire: the \(9/4\)
leftover is not tame (\(C'\ge 7.5\cdot 10^{5}\) on the sample).
Falsifier (c) fired in the expected direction: one Weyl step
produces \(C'\gg 1\), which *closes the shortcut* rather than
killing the identities.

## Formalization

None, deliberately. The identities are Lagrange Taylor plus the
standard floor-gap carry; Lean-ifying them ahead of an ergodic
theorem that would consume them is machinery gravity.

## Results

Classification **HORIZONTAL_WEYL_GREEN**.

- **Identities (EXACT — HUMAN PROOF):** the three unwinds with
  the recorded remainders. Worst witness ratios attain the
  constants: \(0.09375=3/32\), \(0.375=3/8\),
  \(1.40625=45/32\). Lemma G reused and green.
- **Reduction lemmas:** \(v^{3/4}\) is classical van der Corput
  on \(e(kn^{9/8})\) after a decaying error; \(v^{3/2}\) is the
  tame Theorem C substrate (\(A'\ll 1\)). Neither may cite
  Theorem R at \(\alpha=0\).
- **Named obstruction:** one Weyl step on \(v^{9/4}\) has
  spawned amplitude \(15/8<9/4\) (BB silent) and
  \(C'\asymp n^{7/8}\gg 1\) (GG). Unwinding \(v^{9/4}\) is HH
  and is forbidden by `J-nested-floor-without-W-family`.
  Measured leading ratios: \(C/n^{15/8}=2.25000\),
  \(C'/n^{7/8}=4.21875=135/32\).
- **Refutation:** `J-horizontal-theorem-r-shortcut`. The
  rate-free target is unharmed.

## Open questions

- The remaining open step of the rate-free route is unchanged in
  species: ergodic identification of the floor-Hardy nil-orbit.
  Any *rated* proof that unwinds or Weyl-differences the abelian
  coordinate re-enters GG/HH. The rate-free identification of
  \(\{v^{9/4}\}\) without \(n\)-unwinding is answered by
  [juggler_v94_rate_free.md](juggler_v94_rate_free.md): **CLOSE**
  (published doors miss; qualitative van der Corput is the same
  composition).
- Mixed harmonics with \(k_3=0\) reduce to the two cheap axes;
  they do not move density one.

## Decision

**PROMOTE.** Two axes are exact reduction lemmas and the abelian
axis supplies a named obstruction: the optimistic "horizontal half
is already Theorem R" is false, recorded as
`J-horizontal-theorem-r-shortcut`. The wall does not gain a fourth
algebraic layer on the Heisenberg lift — only the *rated shortcut*
dies. The rate-free conjecture stays ACTIVE (ergodic, no rate
needed). Best next question: does a rate-free (not power-saving)
argument identify \(\{v^{9/4}\}\) without unwinding through
\(\theta\) — unique ergodicity of the Hardy monomial of the
Piatetski–Shapiro sequence \(\lfloor n^{3/2}\rfloor\) — or is that
still the unbuilt Hardy-field door?

## Publication assessment

Status: `STRUCTURAL`. The identities are elementary Taylor; the
contribution is the species table that permanently closes a
recorded shortcut without reopening K3/HH. Not a paper claim.
