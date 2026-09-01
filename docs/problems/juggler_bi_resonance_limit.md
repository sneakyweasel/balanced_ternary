# Juggler BI resonance ceiling (the sub-density barrier is beyond the method's dream)

Status: **CLOSE** (the answer to the barrier phase's external question
is **NO**, with a published structural reason and a factor-two margin:
sub-density on \(T_j\) needs an exponent pair with \(p<2/27\) on the
BI line \(q=p+\tfrac12\), while the Bombieri–Iwaniec method's ceiling —
both spacing problems resolved perfectly — is the zeta-exponent floor
\(p=3/20\). The gap is exactly \(81/40=2.025\). The rate-free door
needs post-BI technology; its difficulty is now fully named.)

Successor of
[juggler_ps_inversion_barrier](juggler_ps_inversion_barrier.md)
(**CLOSE**), answering its single open question: can the
Bombieri–Iwaniec resonance method be run for
\(T_j=\sum_{m\le M}e(cm^{9/4}-jm^{2/3})\) to give any exponent pair
with \((5/4)p+q<2/3\)? Not a reopen of the PS inversion, the
composition door, BB/GG/JJ, or any Paper edit; not an attempt to run
the method natively (a method cannot beat its own ceiling).

## Problem

Whether the Bombieri–Iwaniec method — today's output, or its
structural limit under optimal resolution of both spacing problems —
can produce an exponent pair strong enough for the sub-density bound
\(T_j\ll M^{2/3}/\log^2M\) that the rate-free floor-Hardy axis
requires.

## Exact statement

**1. The criterion is one number (EXACT — HUMAN PROOF; elementary).**
BI-type pairs sit on the line \(q=p+\tfrac12\) (all four historical
outputs do: \((9/56)\), \((89/570)\), \((32/205,269/410)\),
\((13/84,55/84)\)). On that line the \(T_j\) functional is
\((5/4)p+q=(9/4)p+\tfrac12\), with equality against the density
exponent \(2/3\) at exactly \(p=2/27\approx 0.0741\). The
\(B\)-process fixes the line pointwise
(\(B(p,p+\tfrac12)=(p,p+\tfrac12)\)), and the \(A\)-process worsens
the functional precisely when \(9p^2+\tfrac92p-1<0\), i.e.
\(p<1/6\) (exact root) — every BI pair qualifies. So the
BI-reachable minimum of the functional is attained at the raw pair,
and the question is exactly: **can BI produce \(p<2/27\)?**

**2. The method ceiling says no (KNOWN).** In the zeta normalization,
a half-line pair gives \(\zeta(\tfrac12+it)\ll t^{\theta}\) with
\(\theta=(p+q)/2-\tfrac14=p\): the zeta exponent *is* \(p\). The
recorded structural limit of the Bombieri–Iwaniec method
(`huxley-1996-area-lattice-points`; Encyclopedia of Mathematics,
"Bombieri–Iwaniec method"; Huxley's survey *Integer points in plane
regions and exponential sums*): **even a complete resolution of both
the first and second spacing problems cannot get the zeta exponent
below \(3/20=0.15\)**. Hence no BI-producible pair has \(p<3/20\), and

\[
\frac{3/20}{2/27}=\frac{81}{40}=2.025:
\]

the dream version of the method misses the sub-density threshold by a
factor of two. The dream-ceiling functional is
\((9/4)\cdot\tfrac3{20}+\tfrac12=\tfrac{67}{80}=0.8375\), still far
above \(2/3\).

**3. The slack is already half spent (KNOWN).** Bourgain's
\(13/84\) (`bourgain-2017-exponent-pair`) resolves the **first**
spacing problem optimally by decoupling ("the only input of this
paper is to provide an optimal result for the first spacing
problem"). The entire remaining within-method slack is the second
spacing problem, and item 2 says zeroing it still cannot reach
\(2/27\). Achieved chain, all exact:

\[
\underbrace{2/27}_{\text{needed}}<\underbrace{3/20}_{\text{ceiling}}
<\underbrace{13/84}_{\text{Bourgain}}<\underbrace{32/205}_{\text{Huxley
2005}}<\underbrace{89/570}_{\text{Huxley 1993}}
<\underbrace{9/56}_{\text{BI 1986}}.
\]

**4. No regime loophole (KNOWN).** The method's working middle range
is \(\alpha=\log M/\log T\) near \(\tfrac12\), with Sargos's 1995
variant near \(\tfrac25\). Our sums have \(T\asymp M^{9/4}\), so
\(\alpha=4/9\in(2/5,1/2)\): squarely inside the middle range. The
secondary phase \(-jm^{2/3}\) is lower order in every derivative on
the relevant blocks (recorded in the barrier phase) and does not
change the resonance geometry. Running the method natively on
\((T,M)=(M^{9/4},M)\) is subject to the same ceiling; the comparison
is the complete answer.

**Conclusion.** The Bombieri–Iwaniec method — as achieved, and as
conjecturally perfected within its own framework — cannot reach the
sub-density barrier for \(T_j\). The rate-free floor-Hardy axis needs
post-BI technology: exponent-pair-conjecture-scale progress
(\(p\to 0\) on the half-line), not resonance refinements.

## Current literature

Project relationship: **known** (ceiling, pairs, regimes) /
**reproduced** (the functional arithmetic).

- `huxley-1996-area-lattice-points` — the monograph; the \(3/20\)
  ceiling under perfect spacing (new registry row).
- `huxley-2005-zeta-v` — the pair \((32/205,269/410)\); resonance
  curves axiomatized (new registry row).
- `bourgain-2017-exponent-pair` — \((13/84,55/84)\); first spacing
  problem resolved optimally by decoupling.
- The Iwaniec–Mozzochi lattice-point branch shows the same
  ceiling phenomenon (its literature records \(\theta=5/16\) as the
  unbeatable barrier of existing methods for the circle/divisor
  exponent) — corroborating that hard method floors are structural,
  not bookkeeping.
- [juggler_ps_inversion_barrier](juggler_ps_inversion_barrier.md) —
  the sub-density placement this record completes.

## Branch budget

```text
Mathematical target     can Bombieri–Iwaniec, run for T_j, produce a pair
                        with (5/4)p+q < 2/3 — equivalently p < 2/27 on the
                        BI line q = p + 1/2 — including under optimal
                        resolution of both spacing problems?
Novelty hypothesis      the regime T = M^{9/4} (just above the critical
                        T = M^2) might be BI-favorable, or the method's
                        conjectural limit might dip below p = 2/27
Falsifier               BI output depends only on (T, M) and the spacing
                        counts; its structural limit under perfect spacing
                        stays well above 2/27; nothing about the exponents
                        9/4, 2/3 changes the resonance geometry
Existing machinery      the sub-density placement, the Bourgain / Huxley
                        pairs, the hull functional
Maximum Phase-0 scope   desk arithmetic of the BI regime + literature
                        verification of the method-limit statement; exact
                        exponent arithmetic sealed in one fast test; no
                        census, no Lean, no paper edits
Promotion criterion     a pair with (5/4)p+q < 2/3 within BI reach, or a
                        published method limit below p = 2/27
Stop criterion          the method limit sits above 2/27 -> answer NO, CLOSE
```

## Balanced-ternary formulation

None required. The objects are exponent pairs and a published method
ceiling.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Half-line criterion \((9/4)p+\tfrac12<\tfrac23\iff p<2/27\) —
  **EXACT — HUMAN PROOF** (elementary; sealed by exact-fraction tests)
- \(B\) fixes the half-line; \(A\) worsens the functional iff
  \(p<1/6\) (exact root of \(9p^2+\tfrac92p-1\)) —
  **EXACT — HUMAN PROOF**
- Zeta-normalization identity \(\theta=p\) on the half-line —
  **KNOWN** (elementary)
- Method ceiling \(p\ge 3/20\) under perfect spacing — **KNOWN**
  (Huxley; Encyclopedia of Mathematics)
- Margin \(\tfrac{3/20}{2/27}=\tfrac{81}{40}\) — **EXACT — HUMAN
  PROOF** (arithmetic)
- Regime check \(\alpha=4/9\in(2/5,1/2)\) — **KNOWN**
- A native BI run beating the ceiling — not attempted; impossible by
  definition of the ceiling
- Any claim about the truth of the sub-density bound — not made (the
  empirics of the barrier phase already sit at square-root scale)

## Experiments

None as a research module. All arithmetic is exact and sealed in
`tests/research/juggler_sequence/test_bi_resonance_limit.py`
(fractions only: criterion, chain, margin, transforms, regime).

## Conjectures

None new. `juggler_tower_rate_free_equidistribution` stays **ACTIVE**;
its difficulty is now fully named: sub-density cancellation a factor
\(81/40\) beyond the BI dream ceiling.

## Counterexamples

None. The novelty hypothesis died by a published obstruction (the
\(3/20\) ceiling), not by a counterexample.

## Formalization

None. Lean-ifying exponent-pair bookkeeping ahead of the missing
theorem would be machinery gravity.

## Results

Classification **BI_CEILING_ABOVE_SUB_DENSITY**.

- The BI question is answered **NO**: needed \(p<2/27\); method
  ceiling \(3/20\) under perfect spacing; achieved \(13/84\) with the
  first spacing problem already optimal. Margins \(81/40=2.025\)
  (dream) and \(\tfrac{13/84}{2/27}=\tfrac{351}{168}\approx 2.089\)
  (today).
- The functional's BI-reachable minimum is at the raw half-line pair
  (\(B\) fixes, \(A\) worsens below \(p=1/6\)); no transform escapes.
- No regime loophole: \(\alpha=4/9\) is mid-range; the \(-jm^{2/3}\)
  perturbation is inert.
- The rate-free floor-Hardy axis therefore needs post-BI technology
  (EPC-scale progress \(p\to0\)); within current and
  conjecturally-perfected resonance analysis it is out of reach.
- Not claimed: that the sub-density bound is false (empirically the
  sums sit at square-root scale); no new exponent pair; no new ledger
  row.

## Open questions

None from this laboratory. The external problem is now stated with
its full price: prove \(T_j=\sum_{m\le M}e(cm^{9/4}-jm^{2/3})=
o(M^{2/3})\), which requires exponent-pair progress past the
Bombieri–Iwaniec ceiling — technology that does not exist today. The
only remaining laboratory move is exporting the problem note; that is
a writing task, not a Phase-0.

## Decision

**CLOSE.** The stop criterion fired with a published ceiling:
\(2/27<3/20\), so the answer to the barrier phase's question is NO
with a factor-two margin, and no within-method refinement (resonance
curves, spacing improvements, decoupling inputs) can change it. The
rate-free conjecture stays ACTIVE as external mathematics whose
difficulty is now completely named. Best next question: none from
this branch; the export note is the only remaining move and is not a
research phase.

## Publication assessment

Status: `ARCHIVED`. A placement record: one exact reduction
(\(p<2/27\)) matched against one published ceiling (\(3/20\)). Not a
paper claim; no Paper A or Paper B edit.
