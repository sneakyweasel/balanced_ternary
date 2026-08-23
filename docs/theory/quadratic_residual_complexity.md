# Quadratic residual complexity of \(x^2\)

Master record for Milestone 17. The section operator remains a
**(3)-section / Cartier-style reparameterization**. This document is
about **polynomial residual automata** of \(x^2\), not a new
differential calculus.

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [residual_state_complexity.md](residual_state_complexity.md),
[jet_transducers.md](jet_transducers.md).

---

## 1. Closed form of quadratic residuals

Write \(q(x)=Ax^2+Bx+C\). The section step is

\[
\mathfrak D_a q(x)
=
3A\,x^2+(B+2Aa)x+\mathrm{DZ}(Aa^2+Ba+C).
\]

**EXACT — LEAN VERIFIED** (`sectionDeriv_quad`, `eval_sectionDeriv_quad`).

Starting from \(x^2\) and an LSD-first trit word \(w\) with packed
prefix \(p(w)=\sum_i a_i 3^i\) and \(m=|w|\),

\[
\boxed{
f_w(x)
=
3^m x^2
+
2p(w)\,x
+
\mathrm{DZ}^m\bigl(p(w)^2\bigr).
}
\]

**EXACT — LEAN VERIFIED** (`residualAlong_Xsq`).

The leading coefficient depends only on depth. The linear coefficient
is twice the packed prefix. The constant term is the balanced quotient
of the square of that prefix.

## 2. Residual count

The map \(w\mapsto f_w\) is injective on trit words: length is recovered
from \(A=3^m\), and the prefix from \(B=2p(w)\) together with uniqueness
of fixed-width balanced ternary.

Therefore every prefix of length \(<k\) (including the empty word)
produces a distinct residual polynomial, and

\[
R_k(x^2)=\frac{3^k-1}{2}
\qquad(k\ge 1),\qquad R_0=1.
\]

**EXACT — LEAN VERIFIED** for injectivity (`residualAlong_Xsq_injective`).
**EXACT — HUMAN PROOF** for the geometric count of trit words of length
\(<k\).

## 3. Finite-horizon Myhill–Nerode

As in Milestone 16: \(f\equiv_k g\) iff every trit word of length \(k\)
produces the same output word.

For degree \(\le 2\), this is coefficient congruence:

\[
Ax^2+Bx+C
\equiv_k
A'x^2+B'x+C'
\iff
3^k\mid(A-A'),\;
3^k\mid(B-B'),\;
3^k\mid(C-C').
\]

**EXACT — LEAN VERIFIED** (`equivK_quad`).

Reason: prefix locality says \(f\equiv_k g\) iff \(3^k\) divides
\((f-g)(n)\) for every packed prefix \(n\) of length \(k\). The three
probe words \(0^k\), \(10^{k-1}\), \((-1)0^{k-1}\) evaluate the
difference at \(0,1,-1\). Since \(2\) is a unit modulo \(3^k\), those
three values recover the three coefficient differences.

The same probes are a **canonical distinguishing continuation**.

**EXACT — LEAN VERIFIED** (the converse direction of `equivK_quad`
constructs them). **COMPUTATIONALLY VERIFIED** in
`canonical_distinguishing_word`.

## 4. Exact state count

On residuals of \(x^2\) in \(U_k=\{f_w:|w|<k\}\):

- if \(m\neq n\) then \(v_3(3^m-3^n)=\min(m,n)<k\), so \(3^k\nmid\Delta A\);
- if \(m=n\) then \(3^k\mid 2(p-q)\) forces \(p=q\), because
  \(|p-q|<3^k\) and \(2\) is coprime to \(3^k\).

Hence distinct residuals are \(\equiv_k\)-separated:

\[
w\neq v,\quad |w|<k,\ |v|<k
\Longrightarrow
f_w\not\equiv_k f_v.
\]

**EXACT — LEAN VERIFIED** (`xsq_equivK_iff_eq`).

Combined with the existing upper bound \(M_k\le R_k\le(3^k-1)/2\),

\[
\boxed{
M_k(x^2)=R_k(x^2)=\frac{3^k-1}{2}
\qquad(k\ge 1).
}
\]

**EXACT — HUMAN PROOF** (cardinality of the prefix tree plus the Lean
separation theorem). Lean does not currently count the finite set of
trit words; it proves that MN classes inject into that set and that
distinct prefixes remain distinct.

The zero branch \(0^m\) isolates only the chain of leading coefficients
\(3^m\). Nonzero prefixes supply the remaining exponentially many
classes. Last-layer \(\rho\)-triples are **not** unique (`k=7`: 729
polynomials, 9 triples), so one-step output vectors cannot prove the
count. The proof uses the full coefficient invariant modulo \(3^k\).

**COMPUTATIONALLY VERIFIED** through `k=7` (and the Python exact
minimizer agrees for all tested `k≤6` in unit tests).

## 5. Why \(x^2\) does not compress

The residual machine of \(x^2\) preserves the entire balanced-ternary
prefix tree at every finite horizon. Prefix locality therefore does
**not** imply state compression.

This is **not** a claim that the infinite-horizon transducer of \(x^2\)
is minimal among all (possibly non-polynomial) realizations, and it is
**not** a claim about Collatz or any number-theoretic decision problem.

## 6. Higher degree: finite-horizon merges

Do **not** conclude \(M_k(x^d)=R_k(x^d)\) for \(d\ge 3\).

A nonzero polynomial difference can vanish as a function on
\(\mathbb Z/3^k\mathbb Z\) when every coefficient has \(3\)-adic
valuation at least \(k\). Distinct polynomials then satisfy
\(f\equiv_k g\) without being equal.

These merges are **delayed distinctions**, not infinite equivalence.
Distinct elements of \(\mathbb Z[x]\) that agree on all of \(\mathbb Z\)
are equal as polynomials, so \(f\equiv_k g\) for every \(k\) implies
\(f=g\).

### First merge of \(x^3\)

**COMPUTATIONALLY VERIFIED.** First merge at horizon \(k=2\)
(\(M_2=3<R_2=4\)):

| | |
|--|--|
| words | \(w=(-1)\) vs \(w=(1)\) |
| residuals | \(9x^3-9x^2+3x\) vs \(9x^3+9x^2+3x\) |
| difference | \(-18x^2\), \(v_3(18)=2\) |
| behaviour | \(\equiv_k\) for \(k\le 2\), split at \(k=3\) |

Odd/even symmetry of \(x^3\) makes the linear jet at depth \(2\)
blind to the sign of a length-\(1\) prefix.

### First merge of \(x^4\)

**COMPUTATIONALLY VERIFIED.** First merge at horizon \(k=3\)
(\(M_3=11<R_3=13\)):

| | |
|--|--|
| words | \(w=(0)\) vs \(w=(0,0)\) |
| residuals | \(27x^4\) vs \(729x^4\) |
| difference | \(-702x^4\), \(702=2\cdot 3^3\cdot 13\), \(v_3=3\) |
| behaviour | \(\equiv_k\) for \(k\le 3\), split at \(k=4\) |

Leading-coefficient differences with large \(v_3\) vanish on
\(\mathbb Z/3^k\mathbb Z\) until the horizon exceeds that valuation.
Odd/even pairs such as \((0,-1)\) vs \((0,1)\) also merge at the same
depth. At horizon \(k=4\), some distinct residuals of \(x^4\) remain
equivalent at \(k=5\) as well: delayed distinction can last more than
one extra step. That is still not infinite equivalence.

Do **not** fit an asymptotic law for \(M_k(x^3)\) or \(M_k(x^4)\) from
\(k\le 6\).

## 7. Lower-bound template

If a family of residual states carries an invariant \(I(f)\) that a
finite continuation can expose, then \(M_k\ge |I|\).

For degree \(\le 2\), \(I(f)=(A,B,C)\bmod 3^k\), exposed by
\(\{0^k,10^{k-1},(-1)0^{k-1}\}\). On residuals of \(x^2\) in \(U_k\)
this invariant is injective, giving the matching lower bound.

For \(x^3\) and \(x^4\) the same coefficient triple is **not** a
complete invariant of \(\equiv_k\): polynomials that differ by a
multiple of \(3^k\) in every coefficient (or by a polynomial that
vanishes on \(\mathbb Z/3^k\mathbb Z\)) merge.

## 8. Composition

Milestone 16 already has

\[
\operatorname{outputAlong}(w,f\circ g)
=
\operatorname{outputAlong}(\operatorname{outputAlong}(w,g),f)
\]

and \(M_k(f\circ g)\le M_k(f)M_k(g)\).

**COMPUTATIONALLY VERIFIED:** \(M_5(x^4)=110<121=M_5(x^2)\), and
strictly below the product bound \(121\cdot 121\). Squaring composed
with itself therefore **collapses** relative to the cascade of two
quadratic machines. The quadratic theorem explains the factors, not
the inequality: \(x^4\) is a degree-\(4\) map, so the higher-degree
merge mechanism of §6 applies.

## 9. Normalization

Unchanged from Milestone 16. For \(\deg d\ge 2\),

\[
\operatorname{LC}(\mathfrak D_w f)=3^{|w|(d-1)}\operatorname{LC}(f),
\]

so any fixed coefficient bound \(B\) eventually fails. Semantic
residual state is not a bounded coefficient word. The `[2]` regression
is independent of the quadratic count.

## 10. Lean inventory

| theorem | content |
|---------|---------|
| `sectionDeriv_quad` | coefficient recurrence of \(\mathfrak D_a\) |
| `residualAlong_Xsq` | closed form of residuals of \(x^2\) |
| `residualAlong_Xsq_injective` | syntactic injectivity \(w\mapsto f_w\) |
| `equivK_quad` | \(f\equiv_k g\) iff coefficients agree mod \(3^k\) (deg \(\le 2\)) |
| `xsq_equivK_iff_eq` | distinct prefixes of length \(<k\) are \(\equiv_k\)-separated |

No `sorry`. No `admit`. The equality \(M_k=(3^k-1)/2\) as a cardinal
identity is the human combination of `xsq_equivK_iff_eq` with the
prefix-tree count and the existing upper bound.

## 11. CLI (discovery, not theorem labels)

```text
btprime calculus distinguish-pair <f> <g> --depth <k>
btprime calculus residual-formula <polynomial> --depth <k>
btprime calculus witness <polynomial> --depth <k>
btprime calculus merge-examples <polynomial> --depth <k>
```

## 12. Literature

3-section / Cartier / \(p\)-kernel residual automata are standard.
What is project-specific is the exact finite-horizon MN count of
\(x^2\) over balanced ternary, the coefficient-mod-\(3^k\) criterion
for quadratics, and the first explicit delayed-distinction pairs for
\(x^3\) and \(x^4\).

Do **not** claim that this complexity says anything about an open
number-theory problem.

## 13. What remains

- Cardinality of trit words of length \(<k\) in Lean (would upgrade
  \(M_k=(3^k-1)/2\) from human combination to a single Lean theorem).
- A general degree-\(d\) distinguishability criterion — treated in
  [polynomial_function_congruence.md](polynomial_function_congruence.md).
- Which cascade pairs of \(x^2\circ x^2\) collapse at a given horizon.

Do not start a further milestone automatically.
