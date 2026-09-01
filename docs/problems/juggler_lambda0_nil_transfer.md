# Juggler \(\lambda=0\) nil-transfer (the Heisenberg lift does not derandomize)

Status: **CLOSE** (the outside-toolkit reopen of quantitative
\(K_3\) / HH is closed; Conjectures V / HH stay PARKED; one
obstruction row records that the lift is a dictionary, not a
transfer)

Successor of [juggler_bracket_nil_lift](juggler_bracket_nil_lift.md)
on the **rated** side only. Attack 3 from the termination map:
does today's Heisenberg identity transfer Proposition 7.4
(`J-shift-average-square-root`) from almost every shift to the
identity section \(\lambda=0\)? Answer: **no** — \(\lambda=0\) is a
free center fiber, and JJ (i)–(iii) survive verbatim in Heisenberg
language. Not a \(K_3\) bound, not a proof of HH, not a Paper B
edit, and not a reopen of differencing or character windows.

## Problem

Whether the Heisenberg lift of the depth-3 tower phase supplies a
method outside BB/GG/JJ that pins the deterministic amplitude-product
sum at \(\lambda=0\).

## Exact statement

**Identity (EXACT — HUMAN PROOF).** For arbitrary reals
\(A,B,\lambda\),

\[
A\{B+\lambda\}=AB+A\lambda-A\lfloor B+\lambda\rfloor.
\]

The last term, reduced mod \(1\), is the vertical Mal'cev coordinate
of \(g_\lambda=\bigl(\begin{smallmatrix}1&A&0\\0&1&B+\lambda\\0&0&1\end{smallmatrix}\bigr)\):
right-multiply by \(\gamma\in\Gamma\) with \(y\)-entry
\(-\lfloor B+\lambda\rfloor\) to obtain
\(\bigl(A,\{B+\lambda\},-A\lfloor B+\lambda\rfloor\bigr)\), then
reduce \(x\) and \(z\). This is the \(\lambda\)-family of
`J-tower-heisenberg-coordinate` (replace \(B\) by \(B+\lambda\)).

**Identity-section classification (EXACT — HUMAN PROOF).** The
instance's special arithmetic is the real parabola
\(A^2=\tfrac94 B\) (tower pair \(A=\tfrac32 v^{3/4}\),
\(B=v^{3/2}\)) or \(A^2=\tfrac{9k^2}{16}B\) (pure-model pair
\(A=\tfrac{3k}{4}\mu^{9/8}\), \(B=\mu^{9/4}\)). A parabola is not a
Leibman horizontal character \(k_1 A+k_2 B\in\mathbb Z\), so it
does not close the horizontal torus and does not pin
\(\lambda=0\) as a closed, rational, or resonant fiber. The
identity section is one fiber of a free center circle. The parabola
is consumed by making \(AB\) a Hardy monomial — the reason the
unshifted lift stays in the coordinate ring — and does not
distinguish the section.

**Obstruction (`J-nil-lift-does-not-derandomize`, EXACT — HUMAN
PROOF).** The Heisenberg identification of the Proposition 7.4
shift does not transfer the almost-every-shift \(L^2\) bound to
\(\lambda=0\). JJ (i)–(iii) survive:

- (i) Integration over \(\lambda\) is Haar measure on the center
  (the \(y\)-circle before reduction). Pinning the identity
  section is the same specific-point problem. No new second
  averaging variable appears; the named family averages stay
  forbidden and were not retested.
- (ii) A Fourier mode \(j\) of the vertical coordinate is the
  same orbit at amplitude \(jA\). Inverse self-similarity
  survives on the nilmanifold.
- (iii) \(y\)-translation deposits \(-A\lambda\) in the center;
  the translation speed is \(A\), so \(S_\lambda\) decorrelates
  at scale \(1/A_{\max}\asymp P^{-27/16}\) — the same scale, not
  a new one.

Consequence: the lift is a dictionary for the shift, not a method
outside the toolkit. Conjectures V / HH remain PARKED.

## Current literature

Project relationship: **extended** (tests the one new candidate
method since the Phase-21 parking of HH; the polynomial-entry
counterpart of the unshifted lift is KNOWN).

- Bergelson–Leibman: the Heisenberg representation of
  \(A\lfloor B\rfloor\bmod 1\) is the depth-1 case; their
  equidistribution theorem needs polynomial entries and does not
  address a specific-point transfer of an \(L^2\) shift average.
- Leibman 2005: horizontal criterion for polynomial nil-orbits —
  linear characters, not real parabolas.
- Proposition 7.4 / Lemma II (`J-shift-average-square-root`) and
  Proposition JJ (`J-derandomization-obstruction`): the recorded
  a.e. bound and the three-clause obstruction this branch
  rephrases, not retests.
- `J-tower-heisenberg-coordinate`: the unshifted lift; this
  branch is the \(\lambda\)-family and the rated question.

## Branch budget

- **Target:** after the Heisenberg lift, is the Proposition 7.4
  shift a center/\(y\)-translation whose identity section
  \(\lambda=0\) can be transferred, or does JJ survive unchanged?
- **Novelty hypothesis:** the group law makes \(\lambda\)-shift a
  nil-orbit translation; the monomial relation \(A^2=\tfrac94 B\)
  might distinguish the identity section, or might only rephrase JJ.
- **Falsifier:** (a) the shifted Mal'cev identity fails; (b)
  \(\lambda=0\) is a closed/rational/resonant fiber; (c) a
  genuinely new average appears that is not a BB/GG/JJ-named family.
- **Existing machinery:** `J-tower-heisenberg-coordinate`,
  Proposition 7.4, JJ, `pure_model_census`, `shift_average_probe`,
  scaled roots from `bracket_nil_lift`.
- **Maximum Phase-0 scope:** exact shifted identity + JJ-clause
  dictionary + one cheap typicality check of \(S_0\) on the
  existing \(\lambda\)-grid. No \(K_3\) bound, no Paper B, no Lean,
  no new large census, no differencing / character / family-average
  retest.
- **Promotion criterion:** a new exact dictionary lemma, or a
  named obstruction that the lift does not derandomize, or a
  genuine new average.
- **Stop criterion:** the lift is a REPARAMETERIZATION of JJ, or
  any falsifier fires as a toolkit re-entry.

## Balanced-ternary formulation

None required; the objects live on \(\mathbb T\) and the Heisenberg
nilmanifold.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Shifted Mal'cev identity
  \(A\{B+\lambda\}=AB+A\lambda-A\lfloor B+\lambda\rfloor\) —
  definition of \(\{\,\}\) plus the Heisenberg group law.
  **EXACT.**
- Real parabola \(A^2=\tfrac94 B\) (tower) /
  \(A^2=\tfrac{9k^2}{16}B\) (pure model) — monomial algebra, not
  a Leibman character. **EXACT.**
- Horizontal-character sample on 24 forms \(k_1 A+k_2 B\),
  \(|k_i|\le 2\): min torus distance \(0.0023\), max spread
  \(0.46\). **COMPUTATIONALLY VERIFIED** (witness that the
  algebraic non-character statement is not secretly a constant
  form on the sampled starts).
- \(\lvert S_0\rvert/\sqrt L\) rank on the existing
  `shift_average_probe` grid — typicality witness, not a
  transfer. **OBSERVATION.**

## Experiments

- Probe: `research.juggler_sequence.lambda0_nil_transfer`
- Artifact: `data/research/juggler/lambda0_nil_transfer/summary.json`
- Tests: `tests/research/juggler_sequence/test_lambda0_nil_transfer.py`

Cheap typicality window: \(P=10^6\), \(8\) blocks of length \(31\),
\(32\) shifts; `shift_average_probe` oracle at the same \(P\).
Tests use \(P=10^4\).

## Conjectures

None new. Conjecture HH (`J-pure-model-amplitude-product`) and
Conjecture V stay PARKED. The active rate-free record
`juggler_tower_rate_free_equidistribution` is untouched except a
one-line cross-reference: the lift does not reopen the rated line.

## Counterexamples

None. Falsifier (a) did not fire (exact identity, scaled gap
\(0\)). Falsifier (b) did not fire (free center fiber). Falsifier
(c) did not fire (no new average).

## Formalization

None, deliberately. The identity is the definition of the
fractional part plus the Heisenberg group law already recorded;
Lean-ifying a dictionary that does not transfer the bound is
machinery gravity.

## Results

Classification **LAMBDA0_NIL_TRANSFER_CLOSED**.

- **Shifted identity (EXACT — HUMAN PROOF):**
  \(A\{B+\lambda\}=AB+A\lambda-A\lfloor B+\lambda\rfloor\), the
  last term the vertical Mal'cev coordinate of \(g_\lambda\).
  Scaled-integer witness exact (gap \(0\)).
- **Free fiber (EXACT — HUMAN PROOF):** \(A^2=\tfrac94 B\) is a
  real parabola, not a horizontal character; \(\lambda=0\) is one
  fiber of a free center circle. Character sample: \(24\) forms,
  min distance \(0.0023\), max spread \(0.46\).
- **JJ dictionary:** all three clauses survive; no new average,
  no new scale. Oracle stability increments
  \(0.077 / 0.736 / 1.472\) at \(\delta=m/(2\pi A)\) for
  \(m=0.1,1,10\) reproduce JJ (iii).
- **Typicality (OBSERVATION, not a transfer):**
  \(\lvert S_0\rvert/\sqrt L\) has mean \(0.946\) vs grid mean
  \(0.888\), median rank \(17/32\), max \(2.10\). \(S_0\) is
  typical of the a.e. bound; typicality does not pin it.

## Open questions

- HH at \(\lambda=0\) remains a specific-point-in-metric-theory
  problem, the same species as the normality of \(\sqrt 2\). No
  laboratory method is recorded. External metric theory is not
  opened here.
- The rate-free tower target
  (`juggler_tower_rate_free_equidistribution`) is a different
  species (qualitative, no rate) and is not this branch.

## Decision

**CLOSE.** The Heisenberg lift is a dictionary for the
Proposition 7.4 shift, not a method outside BB/GG/JJ:
\(\lambda=0\) is a free center fiber, and every JJ clause
survives in this language. The outside-toolkit reopen of
quantitative \(K_3\) is closed; Conjectures V / HH stay PARKED
exactly as Phase 21 left them. The obstruction is recorded as
`J-nil-lift-does-not-derandomize`. Best next question: none on
the rated line — the live termination attack remains the
rate-free tower target, which this branch does not touch.

## Publication assessment

Status: `ARCHIVED`. Negative knowledge: the one new candidate
since the parking of HH does not transfer \(\lambda=0\). The
dictionary belongs next to Proposition JJ if a revision of
Paper B is ever requested; Paper B stays frozen.
