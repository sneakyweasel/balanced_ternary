# Balanced digit sums of nonlinear polynomial values

Status: **EXPLORATORY**

Exact integer level sets of the balanced digit sum of nonlinear
polynomial values, with finite-prefix zero sets kept separate.

## Problem

Determine whether
\(E^{\mathbb Z}_{P,0}=\{n\in\mathbb Z:s_{\mathrm{bal}}(P(n))=0\}\)
has a structural law, for nonlinear \(P\in\mathbb Z[x]\), that is not
already present in ordinary \(q\)-additive digit-sum theory.

## Exact statement

Write \(s_{\mathrm{bal}}(n)=\sum_i a_i\) for the canonical balanced
expansion \(n=\sum_i a_i 3^i\), \(a_i\in\{-1,0,+1\}\). The exact
target is the integer level set \(E^{\mathbb Z}_{P,0}\). The
finite-prefix family
\[
E^{(k)}_{P,0}=\{n\bmod 3^k:S_k(P;n)=0\},\qquad
S_k=\sum_{i<k}\operatorname{lsd}(D^i P(n))
\]
is a different object: the sets need not be nested. Cylinder
refinement is recorded by `stay_zero`, `leave_zero`, and
`enter_zero`.

The Phase-0 theorem-selection polynomial is \(P(x)=x^2\). Controls:
\(x^3\), \(x^3-x\), \(x^4\), \(x^2+x\).

## Current literature

- `oeis-A065363`, `ruskey-sawada-2009-digital-sum-gf`: the sequence
  \(s_{\mathrm{bal}}\) itself, its recurrences, and its generating
  function. `KNOWN`.
- Xie / OEIS A065363: \(s_{\mathrm{bal}}(m)=s_3(2m)-s_3(m)\) for
  \(m\ge 0\), and \(s_{\mathrm{bal}}(-m)=-s_{\mathrm{bal}}(m)\).
  `KNOWN` / `REPARAMETERIZATION` of the integer function
  \(s_{\mathrm{bal}}\). This is the translation falsifier. It recasts
  \(s_{\mathrm{bal}}(P(n))=0\) as the ordinary correlation
  \(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\). It does **not**
  classify the LSD-first language, the residual/sum state, or the
  cylinder refinement of \(E^{(k)}_{P,0}\).
- `peter-2002-summatory-digits-polynomials`,
  `drmota-mauduit-rivat-2011-sum-of-digits-polynomials`,
  `stoll-2012-digits-polynomial-ap`: ordinary \(s_q(P(n))\)
  summatory laws and residue-class distribution (Gelfond line).
  `KNOWN`. Modular constraints with \((m,q-1)=1\), not the exact
  zero \(s_{\mathrm{bal}}(P(n))=0\).
- `allouche-shallit-2003-automatic-sequences`: exact level sets of
  an unbounded \(q\)-additive function are the typical non-automatic
  example; \(s(n)\bmod m\) can be automatic. `KNOWN`.
- `ahmed-savchuk-2020-polynomial-tree-endomorphisms`: unrestricted
  residual closures are finite-state iff \(P\) is linear. `KNOWN`.
- `anashin-2012-automata-finiteness`: van der Put finite-Mealy
  criterion. `KNOWN`.
- `avizienis-1961-signed-digit`, `knuth-taocp-vol2`,
  `hayes-2001-third-base`: signed-digit arithmetic and unique
  balanced expansion. `KNOWN`.
- `monna-1952-digit-reversal`: digit-reversal map. `KNOWN`. Not
  opened in Phase 0.

The translation gate stays **open**: existing theory settles
\(s_{\mathrm{bal}}\) as a function of ordinary \(s_3\), not the
polynomial preimage language or the finite-prefix cylinders.

## Branch budget

```text
Mathematical target     For P=x², decide whether the exact zero digit-sum
                        language or finite-prefix zero sets have a structural
                        law not inherited from ordinary ternary digit sums.
Novelty hypothesis      Signed cancellation yields either an exact refinement
                        recursion or a provably unbounded predictive-state law.
Falsifier               s_bal(P(n)) reduces completely to known ordinary
                        digit-sum correlations, or the census yields only
                        horizon-dependent tables with no exact invariant.
Existing machinery      bt.metrics/sequences, polynomial sections and
                        output_along/residual_along, Myhill–Nerode signatures.
Maximum Phase-0 scope   Literature gate; P∈{x²,x³,x³−x,x⁴,x²+x}; exact
                        exhaustive census through k=10; one candidate theorem
                        or one obstruction. No CLI, UI, Lean, or generic package.
Promotion criterion     One exact nonlinear theorem: finite-state recognition,
                        non-regularity/unbounded state, or an exact cylinder
                        refinement law not already covered by ordinary theory.
Stop criterion          All surviving claims are KNOWN/REPARAMETERIZATION, or
                        only numerical growth remains after the bounded census.
```

## Balanced-ternary formulation

Packed prefixes \(n_w=\mathrm{pack}(w)\) are the balanced words of
length \(k\). Residual outputs of \(P\) along \(w\) are the first
\(k\) balanced digits of \(P(n_w)\). The terminal-correction identity
\[
s_{\mathrm{bal}}(P(n_w))
=
\sum\operatorname{outputAlong}(w,P)
+s_{\mathrm{bal}}(P_w(0))
\]
separates the finite-prefix sum \(S_k\) from the exact integer sum.

## Why BT may be relevant

Signed digits make \(\{n:s_{\mathrm{bal}}(n)=0\}\) infinite by
cancellation, whereas ordinary \(\{n:s_3(n)=0\}=\{0\}\). The residual
machine supplies the output path of \(P(n_w)\). Relevance is not a
novelty claim.

## Candidate operations / invariants

- Translation \(s_{\mathrm{bal}}(m)=s_3(2m)-s_3(m)\) —
  **PROVED** (recurrences; exhaustive on the Phase-0 window).
- Terminal correction — **PROVED** from prefix locality.
- Joint state \((\text{residual},S_k)\) — Phase-0 object.
- Remaining-horizon accept signatures
  \(\mathrm{accept}(g,s)\iff s+s_{\mathrm{bal}}(g(0))=0\).
- Cylinder refinement counts — **COMPUTATIONALLY VERIFIED**
  through \(k\le 10\).

## Experiments

`research.balanced_digit_sum_polynomials.triage` with the five
polynomials and exact depths \(k\le 10\). Tests live in
`tests/research/balanced_digit_sum_polynomials/test_triage.py`.
No experiment runner is registered.

## Conjectures

None registered.

## Counterexamples

Recorded after the census in **Results**.

## Formalization

None. No `sorry`. Lean is not opened on this gate.

## Results

See the census tables and the distilled statement in **Decision**.
Filled after the Phase-0 run.

## Open questions

Filled after the Phase-0 run.

## Decision

`PARK` pending the Phase-0 census recorded in this same dossier.
The literature gate does not by itself force `CLOSE`: the ordinary
translation recasts the integer predicate and does not classify the
language or the cylinders.

Best next question: after the census, does \(x^2\) have one exact
law not inherited from \(s_3(2n^2)=s_3(n^2)\)?

## Publication assessment

Status: `EXPLORATORY`.
