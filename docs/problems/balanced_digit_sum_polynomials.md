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
  \(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\).
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
  **PROVED** (König recurrences plus exhaustive check; OEIS A065363).
- Terminal correction — **PROVED** from prefix locality.
- Joint state \((\mathrm{residual},S_k)\) — Phase-0 object;
  cardinality \(3^k\) through \(k=10\) on every listed \(P\).
- Remaining-horizon accept signatures of \(x^2\) at horizon \(2\) —
  **COMPUTATIONALLY VERIFIED** at even depths \(\le 8\).
- Cylinder refinement counts — **COMPUTATIONALLY VERIFIED**
  through \(k\le 10\).

## Experiments

`research.balanced_digit_sum_polynomials.triage` with the five
polynomials and exact depths \(k\le 10\). Runtime of the Phase-0
import was \(38.5\,\mathrm{s}\) on the laboratory machine; that
figure is not a mathematical claim. Tests live in
`tests/research/balanced_digit_sum_polynomials/test_triage.py`.
No experiment runner is registered.

## Conjectures

None registered.

## Counterexamples

1. **Prefix zero is not exact integer zero.** For \(P=x^2\) there
   are length-\(3\) words with \(S_3=0\) and
   \(s_{\mathrm{bal}}(n_w^2)\ne 0\).
2. **Ordinary \(s_3(P(n))=0\) is not the balanced zero set.** On the
   nonnegative slice of \(P_6\) (\(|P_6\cap\mathbb Z_{\ge 0}|=365\)),
   \(x^2\) has \(55\) balanced zeros and \(1\) ordinary zero.
3. **Candidate A (finite-state recognizer).** Raw joint states of
   \(x^2\) are the full prefix tree \(3^k\) through \(k=10\);
   partial sums take \(2k-1\) values. No bounded predictive state
   independent of horizon was obtained.
4. **Nested cylinders.** Every listed \(P\) has large
   `leave_zero` and `enter_zero` at every depth \(k\ge 2\).
   \(E^{(k)}_{P,0}\) is not an inverse limit of a single 3-adic set.

## Formalization

None. No `sorry`. Lean is not opened on this gate.

## Results

### What was learned

1. The integer predicate is exactly the ordinary correlation
   \(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\).
2. The terminal-correction identity holds for every tested word and
   is the residual form of prefix locality, not a new invariant.
3. \(S_k=0\) and \(s_{\mathrm{bal}}(P(n_w))=0\) are different
   predicates; cylinders are not nested.
4. Joint residual/sum states equal \(3^k\) through \(k=10\) for all
   five polynomials. Partial-sum alphabets grow linearly in \(k\).
5. Signed zeros are abundant relative to ordinary
   \(s_3(P(n))=0\), but that gap is a property of \(s_{\mathrm{bal}}\)
   itself, not of nonlinearity.
6. Prefixes \(10^m\) of \(x^2\) are pairwise distinguished by short
   continuations through \(m\le 3\). That is a finite table, not an
   infinite Myhill–Nerode proof.
7. Horizon-\(2\) predictive types of \(x^2\) were
   \(1,8,27,42,47\) at even depths \(0..8\). Horizon-dependent
   growth is not a depth-independent automaton.

### Known baseline

Balanced digit sums, their generating function, the
\(s_3(2n)-s_3(n)\) translation, Gelfond-type distribution of
\(s_q(P(n))\) in residue classes, and non-automaticity of exact zeros
of unbounded \(q\)-additive functions.

### Balanced-specific phenomenon

Cancellation makes \(E^{\mathbb Z}_{P,0}\) much larger than
\(\{n:s_3(P(n))=0\}\). After the translation this is the ordinary
statement that \(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\)
is weaker than \(s_3(P(n))=0\).

### Strongest candidate theorem

For every integer \(m\),
\(s_{\mathrm{bal}}(m)=s_3(2\lvert m\rvert)-s_3(\lvert m\rvert)\)
with the sign of \(m\). Consequently
\(n\in E^{\mathbb Z}_{P,0}\) if and only if
\(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\).
**EXACT — HUMAN PROOF** as the OEIS / recurrence identity; tagged
`REPARAMETERIZATION`.

### Strongest refutation

A finite-state LSD-first recognizer of
\(\{n:s_{\mathrm{bal}}(n^2)=0\}\) with a depth-independent state
bound. Raw joint states are \(3^k\); the sum coordinate is
unbounded; prefix-zero cylinders do not stabilize.

### State complexity

For each listed \(P\) and \(k\le 10\),
\(\lvert\{\text{residual polynomials at depth }k\}\rvert=3^k\)
and the joint \((\mathrm{residual},S_k)\) count is the same.
Distinct partial sums: \(1,2,3,5,7,\ldots,19\) (linear). Predictive
signatures of \(x^2\) at remaining horizon \(2\) grew through depth
\(8\) and were not shown unbounded independently of the horizon.

### 3-adic geometry

Exact integer zeros of \(x^2\) on \(P_k\):
\(1,1,3,5,15,35,109,279,781,2251,6495\).
Prefix zeros at \(k=10\): \(9495\), with
`leave_zero` \(=6368\) and `enter_zero` \(=6068\).
No closed refinement recursion.

### Monna geometry

Not opened.

### Literature verdict

`KNOWN` / `REPARAMETERIZATION`. The census is
`PROJECT-SPECIFIC` measurement and is not promoted.

### Census table for \(x^2\)

| \(k\) | joint | \(S_k\) values | prefix \(0\) | exact \(0\) | stay | leave | enter |
|------:|------:|---------------:|-------------:|------------:|-----:|------:|------:|
| 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 9 | 3 | 5 | 3 | 3 | 0 | 2 |
| 4 | 81 | 7 | 27 | 15 | 13 | 8 | 14 |
| 6 | 729 | 11 | 171 | 109 | 71 | 88 | 100 |
| 8 | 6561 | 15 | 1227 | 781 | 465 | 768 | 762 |
| 10 | 59049 | 19 | 9495 | 6495 | 3427 | 6368 | 6068 |

Controls at \(k=10\): exact zeros \(x^3=6093\), \(x^3-x=11807\),
\(x^4=4883\), \(x^2+x=14351\). Ordinary comparison on the
nonnegative slice of \(P_6\): balanced zeros \(55,66,115,34,113\)
versus ordinary zeros \(1,1,2,1,1\).

## Open questions

None retained. In particular, digital-root depth, jump-depth
spectra, and Monna plots are not opened.

## Decision

`CLOSE`. The integer target is the ordinary digit-sum correlation
\(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\). After that
translation, the residual/sum census is a finite-horizon table:
joint states fill the prefix tree, prefix-zero cylinders do not
nest, and no exact refinement or depth-independent finite-state
law appears. Signed cancellation is real and is already the
definition of \(s_{\mathrm{bal}}\). A branch whose exact statements
are `KNOWN` or `REPARAMETERIZATION` is a close.

Best next question: none on this branch; the gate is closed.

## Publication assessment

Status: `EXPLORATORY`.

Not a `PAPER_CANDIDATE`. The translation is classical; the census
is a computational appendix without a surviving nonlinear theorem.
