# Juggler survivor-fan growth from the log-3 measure

Status: **ACTIVE** (Phase 0 decided)

Attack C of the post-fan-minimum Diophantine programme
([juggler_cycle_walk_fan_minimum.md](juggler_cycle_walk_fan_minimum.md)).
Wu–Wang’s linear-independence measure for \(1,\log 2,\log 3\) is
imported as a **growth law** for survivor-fan width, not as a
leftover killer. Not a halt theorem, not a floor raise, not a
Paper A edit, and not a reopen of the REFUTED Baker/Rhin transfer
([juggler_cycle_gap_baker.md](juggler_cycle_gap_baker.md)).

## Problem

The fan-minimum law says \(R_{\min}\approx e^{4/(a+2)}\) for the
dangerous fan closed by partial quotient \(a\) of
\(\log 2/\log 3\). Boundedness of those quotients is a classical
OPEN problem, so the laboratory cannot prove \(R_{\min}\) stays
away from \(1\). Does the strongest published measure for
\(\log 3\) still give a rigorous polynomial cap on how wide a
survivor fan can become, and is the computational continuation
of the laboratory CF consistent with that cap?

## Exact statement

Write \(\alpha=\log 2/\log 3\) and \(\Lambda=q\log 3-p\log 2\), so

\[
\Bigl\lvert\alpha-\frac{p}{q}\Bigr\rvert
=\frac{\lvert\Lambda\rvert}{q\log 3}.
\]

Wu–Wang (2014) give, for every \(\varepsilon>0\) and all
sufficiently large \(H=\max(\lvert b\rvert,\lvert c\rvert)\),

\[
\lvert a+b\log 2+c\log 3\rvert
\ge H^{-4.1163051-\varepsilon},
\]

hence \(\mu(\log 3)\le 5.1163051\). Specialising to
\(\Lambda\) with \(H=q\) (since \(\alpha<1\)) yields

\[
\Bigl\lvert\alpha-\frac{p}{q}\Bigr\rvert
\ge\frac{q^{-5.1163051-\varepsilon}}{\log 3}.
\]

A convergent satisfies
\(\lvert\alpha-p_j/q_j\rvert<1/(a_{j+1}q_j^2)\), so

\[
\boxed{
a_{j+1}\le C_\varepsilon\,q_j^{3.1163051+\varepsilon}
}
\]

for an implied \(C_\varepsilon\) and all large \(j\). Bondareva–
Luchin–Salikhov (2018) sharpen the exponent only to \(3.116201\);
the shape is unchanged. Rhin/SdW Lemma 12 is fully effective but
weaker: \(a_{j+1}\lesssim q_j^{12.3}\).

**Fan-width transfer (EXACT — HUMAN PROOF, citing Wu–Wang).**
A survivor fan \(L_k=q+kQ\) is the semiconvergent family of the
closing quotient \(a_{j+1}\). Its width is that quotient, hence

\[
\text{fan width}=O_\varepsilon\bigl(q^{3.1163051+\varepsilon}\bigr).
\]

The next dangerous seed satisfies
\(q_{j+1}\le C_\varepsilon q_j^{4.1163051+\varepsilon}\).

**What the bound does not give.** It does **not** give
\(a_{j+1}=O(1)\). Combined with the fan-minimum law
\(e^{4/(a+2)}\le R_{\min}\lesssim e^{4/a}\), the most
pathological Wu–Wang-allowed fan still has

\[
R_{\min}\ge\exp\bigl(4/(C_\varepsilon q^{3.1163051+\varepsilon}+2)\bigr)
\to 1
\qquad(q\to\infty).
\]

The fan obstruction discovered by the competition programme
survives.

**Consistency (COMPUTATIONALLY VERIFIED).** On the deep
sandwich \(171928773/272500658<\alpha<53715833/85137581\) the
interval CF of \(\alpha\) is
\([0;1,1,1,2,2,3,1,5,2,23,2,2,1,1,55,1,4]\), matching the
certified \(\theta_{\mathrm{rot}}\) tail. Every certified
quotient with \(q\ge 19\) sits below the \(\varepsilon=0\)
diagnostic envelope \(a<(\log 3)\,q^{3.1163051}\):

- laboratory-max ratio \(a/\mathrm{cap}=2.827\cdot 10^{-4}\) at
  \(q=19\), \(a=3\);
- \(a=23\) at \(q=1054\): ratio \(7.958\cdot 10^{-9}\);
- \(a=55\) at \(q=301994\) (the \(55\)-fan): ratio
  \(4.190\cdot 10^{-16}\), \(R_{\min}(55)=1.0727\).

The same diagnostic already allows \(R_{\min}\le 1.07\) at
\(q\gtrsim 3.55\) and \(R_{\min}\le 1.001\) at \(q\gtrsim 13.9\).
At the first leftover \(q=19\) the Wu–Wang-allowed floor is
\(R_{\min}\ge 1.00038\). An 80-digit observed continuation
(prefix matches the sandwich; terminal quotient dropped)
through \(q\approx 3.26\cdot 10^{20}\) has max \(a=37\) and max
ratio \(5.17\cdot 10^{-27}\). The computational continuation is
consistent, with enormous margin.

No cycle of any length — not claimed. No new period bound.

## Current literature

- Wu–Wang linear-independence measure for \(1,\log 2,\log 3\) —
  **KNOWN** (`wu-wang-2014-irrationality-measure-log3`)
- Bondareva–Luchin–Salikhov sharpening \(\mu(\log 3)\le 5.116201\) —
  **KNOWN** (`bondareva-luchin-salikhov-2018-log3-irrationality`);
  the exponent drop is \(10^{-4}\) and is not used as a new
  attack
- Rhin effective two-logarithm measure / SdW Lemma 12 —
  **KNOWN** (`rhin-1987-pade-irrationality`); leftover-killer
  transfer **REFUTED**
  (`juggler_baker_kills_near_convergents`)
- Archimedean / p-adic coupling (literature attack B) —
  **CLOSE**
  ([juggler_cycle_padic_coupling.md](juggler_cycle_padic_coupling.md))
- Fan-minimum law \(R_{\min}\approx e^{4/(a+2)}\) —
  **COMPUTATIONALLY VERIFIED** instances, **CONJECTURE**
  asymptotic form
  ([juggler_cycle_walk_fan_minimum.md](juggler_cycle_walk_fan_minimum.md))
- Boundedness of the CF quotients of \(\log 2/\log 3\) — **OPEN**
- Every start reaches 1 — not claimed

Project relationship: **extended** (a quantitative growth law
for the survivor lattice; not a Baker revival).

## Branch budget

```text
Mathematical target     Does Wu–Wang’s measure give a rigorous
                        polynomial cap on survivor-fan width, and
                        is the laboratory CF consistent with it?
Novelty hypothesis      Fan width ~ a_{j+1} ≲ q_j^{3.116+ε} is a
                        genuine growth theorem for the lattice;
                        it does not claim a = O(1) or R_min ↛ 1
Falsifier               A certified q≥19 quotient above the
                        diagnostic envelope, or a claim that the
                        bound kills leftovers / bounds a
Existing machinery      Deep x-sandwich and interval CF
                        (competition); fan-minimum law; Rhin/SdW
                        already REFUTED as a leftover killer
Maximum Phase-0 scope   One arithmetic probe: transfer + certified
                        CF census + WW-allowed R_min scales. No
                        Lean, no floor raise, no Baker solver, no
                        Paper A edit
Promotion criterion     Clean transferred width theorem plus a
                        consistency census; explicit that R_min
                        can still → 1
Stop criterion          Characterization recorded. Do not import
                        a sharper Baker constant
```

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Wu–Wang \(\lvert a+b\log 2+c\log 3\rvert\ge H^{-4.1163051-\varepsilon}\) —
  **KNOWN**
- CF transfer \(a_{j+1}=O_\varepsilon(q_j^{3.1163051+\varepsilon})\) —
  **EXACT — HUMAN PROOF** (standard continued-fraction algebra
  on the published measure)
- Fan-width corollary
  \(\#\{L_k=q+kQ\}=O_\varepsilon(q^{3.1163051+\varepsilon})\) —
  **EXACT — HUMAN PROOF**
- Diagnostic \(\varepsilon=0\) envelope vs certified/observed CF —
  **COMPUTATIONALLY VERIFIED** (consistency only; not a finite-\(q\)
  theorem)
- “The bound kills leftovers / forces \(a=O(1)\)” — **REFUTED**
  as a reading of Wu–Wang; the leftover-killer slogan stays
  **REFUTED**
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_walk_fan_growth`
- Artifacts: `data/research/juggler/cycle_walk_fan_growth/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_walk_fan_growth.py`

No CLI, no Lean, no new big-int sandwich, no floor work.

## Conjectures

`juggler_walk_fan_growth_measure` — **EXACT — HUMAN PROOF**
(proved record): Wu–Wang implies a polynomial cap on every
partial quotient of \(\log 2/\log 3\), hence on every survivor-fan
width. The computational census is consistency, not a conjecture.

## Counterexamples

None against the transfer. The \(\varepsilon=0\) diagnostic is
violated by the tiny-\(q\) \(\theta_{\mathrm{rot}}\) quotient
\(a_1=2\) at \(q=1\) (ratio \(1.82\)); that is expected and is
not a laboratory leftover. The bound is an asymptotic statement
for large \(H\).

## Formalization

None. No new Lean, no `sorry`, no Rhin/Wu–Wang import. Paper A
is unchanged. Not a halt theorem.

## Results

Classification **WALK_FAN_GROWTH_GREEN**.

- Transfer: fan width
  \(O_\varepsilon(q^{3.1163051+\varepsilon})\); next seed
  \(O_\varepsilon(q^{4.1163051+\varepsilon})\)
- Certified \(\alpha=[0;1,1,1,2,2,3,1,5,2,23,2,2,1,1,55,1,4]\)
  on the stored deep sandwich (powers not recomputed)
- Laboratory max \(a/\mathrm{cap}=2.827\cdot 10^{-4}\) at
  \(q=19\); the \(55\)-fan sits at \(4.190\cdot 10^{-16}\)
- Observed continuation through \(q\sim 3\cdot 10^{20}\)
  (max \(a=37\)) stays below \(5.17\cdot 10^{-27}\)
- Wu–Wang already allows \(R_{\min}\le 1.001\) at \(q\gtrsim 14\),
  so the bound is vacuous as a uniform gap on every leftover the
  laboratory prices
- Rhin’s effective companion is worse (\(q^{12.3}\)) and is not
  reopened as a killer

## Open questions

None on this attack. Sharper published exponents (BLS
\(3.116201\), or any future improvement of the same polynomial
shape) do not change the conclusion; do not import them as a
new branch. The fan obstruction remains. Attack A is CLOSE
([juggler_cycle_fan_multipoint.md](juggler_cycle_fan_multipoint.md)).
The inhomogeneous reading of Wu–Wang (nonzero integer \(p\))
is CLOSE
([juggler_cycle_inhomogeneous_log.md](juggler_cycle_inhomogeneous_log.md)).

## Decision

**PROMOTE.** The Phase-0 target is answered: Wu–Wang supplies a
genuine polynomial growth theorem for survivor-fan width, the
certified and observed CFs are consistent with huge margin, and
the same theorem is explicitly too coarse to prevent
\(R_{\min}\to 1\) or to kill a leftover. That is the
characterization Attack C promised. It is not a Baker revival
and it does not reopen finance.

Best next question: none from this width theorem. The
literature programme is complete: A CLOSE, B CLOSE,
inhomogeneous CLOSE, C a width bound only.

## Publication assessment

Status: `THEOREM`.

A one-page transfer of a published linear-independence measure
onto the laboratory survivor lattice, with a finite consistency
census. Useful as a quantitative bound on how pathological the
families can become; useless as a leftover killer. Not a paper
candidate on its own and not a halt theorem.
