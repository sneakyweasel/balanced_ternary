# Newton-class image of the cubic residual machine

Master record for Milestone 19. The section operator remains a
**(3)-section / Cartier-style reparameterization**. This document is
about the **image** of the residual tree of \(x^3\) inside
Newton-function space, not another kernel theorem.

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [polynomial_function_congruence.md](polynomial_function_congruence.md),
[quadratic_residual_complexity.md](quadratic_residual_complexity.md).

Do **not** read this as a formula for \(M_k(x^d)\) in general.

---

## 1. The counting problem

Milestone 18 identified residual classes with Newton residues

\[
\Phi_k(f)=\bigl(\Delta^j f(0)\bmod 3^k\bigr)_{j\ge 0}.
\]

For \(f(x)=x^3\) and residual word \(w\), write \(f_w=\mathfrak D_w f\)
and \(C_k(w)=\Phi_k(f_w)\). The exact count is

\[
\boxed{
M_k(x^3)
=
\bigl|\{\,C_k(w):|w|<k\,\}\bigr|.
}
\]

This is no longer a raw-polynomial count. Distinct prefixes still give
distinct ordinary polynomials, so \(R_k(x^3)\) is the size of the
domain, not of the image.

---

## 2. Closed form of cubic residuals

Write \(q(x)=Ax^3+Bx^2+Cx+D\). The section step is

\[
\mathfrak D_a q(x)
=
9A\,x^3
+(9Aa+3B)x^2
+(3Aa^2+2Ba+C)x
+\mathrm{DZ}(Aa^3+Ba^2+Ca+D).
\]

**EXACT — LEAN VERIFIED** (`sectionDeriv_cubic`).

Starting from \(x^3\) and an LSD-first trit word \(w\) with packed
prefix \(p(w)=\sum_i a_i 3^i\) and \(m=|w|\),

\[
\boxed{
f_w(x)
=
3^{2m}x^3
+
3^{m+1}p(w)\,x^2
+
3p(w)^2\,x
+
\mathrm{DZ}^m\bigl(p(w)^3\bigr).
}
\]

Equivalently,

\[
f_w(x)
=
\mathrm{DZ}^m\bigl((p(w)+3^m x)^3\bigr).
\]

**EXACT — LEAN VERIFIED** (`residualAlong_Xcube`, `eval_cubicResid_iter`).

The packed prefix alone determines the residual: no extra digit moment
is required. The leading coefficient recovers depth, and the quadratic
coefficient recovers \(p(w)\). Hence every prefix gives a distinct
polynomial:

\[
R_k(x^3)=\frac{3^k-1}{2}\qquad(k\ge 1).
\]

**EXACT — LEAN VERIFIED** (`residualAlong_Xcube_injective`).

---

## 3. Newton coordinates

For a general cubic \(Ax^3+Bx^2+Cx+D\),

\[
N_0=D,\qquad
N_1=A+B+C,\qquad
N_2=6A+2B,\qquad
N_3=6A.
\]

**EXACT — LEAN VERIFIED** as the vanishing data of
`vanishesMod_cubic_iff`; \(N_2=2(3A+B)\).

On the residual family this is

\[
\begin{aligned}
N_0&=\mathrm{DZ}^m(p^3),\\
N_1&=3^{2m}+3^{m+1}p+3p^2,\\
N_2&=2\cdot 3^{m+1}(p+3^m),\\
N_3&=2\cdot 3^{2m+1}.
\end{aligned}
\]

**EXACT — LEAN VERIFIED** (`newton_cubicResid`).

Depth forces \(N_3\). The prefix enters \(N_2\) only through a factor
\(3^{m+1}\), so modulo \(3^k\) one recovers at most
\(p\bmod 3^{k-m-1}\). That is the compression.

The independent residual data are \((m,p)\). After reduction modulo
\(3^k\), the independent Newton data are those four residues; \(N_3\)
is a depth indicator and \(N_2\) is a truncated prefix.

---

## 4. Newton-coordinate section transition

On an arbitrary cubic the monomial step of Section 2 induces

\[
N_3'=9N_3,
\qquad
N_2'=3N_2+3(a+2)N_3,
\]

with \(N_0'=\mathrm{DZ}(q(a))\) and \(N_1'=A'+B'+C'\).
(The naive formula \(N_2'=9N_2+3a N_3\) holds only when \(B=0\).)

**EXACT — LEAN VERIFIED** (`newton_section_N3`, `newton_section_N2`,
`sectionDeriv_cubic`).

On the residual family this is just the closed increment
\((m,p)\mapsto(m+1,p+3^ma)\).

**EXACT — LEAN VERIFIED** (`sectionDeriv_cubicResid`).

---

## 5. The arithmetic image map

Define

\[
F_k(m,p)
=
\Phi_k\bigl(f_{(m,p)}\bigr)
=
(N_0,N_1,N_2,N_3)\bmod 3^k
\]

on pairs with \(0\le m<k\) and \(p\) a balanced width-\(m\) integer.
Milestone 18 gives \(f\equiv_k g\iff\Phi_k(f)=\Phi_k(g)\), so

\[
\boxed{
M_k(x^3)
=
\bigl|\operatorname{Im} F_k\bigr|.
}
\]

**EXACT — HUMAN PROOF** from the closed form plus the Lean cubic
equivalence `equivK_cubic_newton`. This is the desired transition

\[
\text{residual automaton}
\to
\text{Newton invariant}
\to
\text{image of an explicit arithmetic map}.
\]

It is **not** a closed cardinality formula.

---

## 6. Collision-class characterization

Two prefixes collide at horizon \(k\) iff \(F_k(m,p)=F_k(n,q)\).

### Same depth

For \(|w|=|v|=m\) and \(p\neq q\):

1. \(3^{k-m-1}\mid(p-q)\) whenever \(k>m+1\) (from \(N_2\); automatic if
   \(k\le m+1\));
2. \(3^{k-1}\mid(p-q)(p+q+3^m)\) (from \(N_1\));
3. \(3^k\mid\mathrm{DZ}^m(p^3)-\mathrm{DZ}^m(q^3)\) (from \(N_0\)).

**EXACT — HUMAN PROOF.**

If \(2m+1<k\), condition 1 forces \(p=q\) because
\(|p-q|<3^m\le 3^{k-m-1}\). Distinct such depths have distinct exact
\(N_3=2\cdot 3^{2m+1}\). Therefore every residual with
\(2m+1<k\) is \(\equiv_k\)-separated from every other residual in the
universe.

**EXACT — HUMAN PROOF.** Lower bound:

\[
M_k(x^3)
\ge
\frac{3^{r+1}-1}{2},
\qquad
r=\bigl\lfloor(k-2)/2\bigr\rfloor
\quad(k\ge 2).
\]

### Cross depth

Different depths can collide only after both \(N_3\) residues vanish:
\(\min(m,n)\ge\lceil(k-1)/2\rceil\). The remaining conditions are the
same \(N_0,N_1,N_2\) congruences.

### Packed-prefix congruence is not enough

**REFUTED:** Newton classes of \(x^3\) are not the congruence classes
of \(p(w)\) modulo a power of \(3\). Same-depth collisions are mostly
sign pairs \(p\leftrightarrow -p\), together with high-valuation
clusters and a few cross-depth zero-ish branches. At \(k=6\) one also
sees triples of the form \(\varepsilon 3^s+3^{s+1}\delta\) with
\(\varepsilon=\pm 1\) and \(\delta\in\{-1,0,1\}\).

---

## 7. First merge

The depth-1 sign pair has Newton data

\[
N(-1)=(0,3,36,54),\qquad
N(+1)=(0,21,72,54).
\]

The differences are \((0,-18,-36,0)\), all of valuation at least \(2\).
Hence \(\Phi_2\) agrees and \(\Phi_3\) does not.

**EXACT — LEAN VERIFIED** (`x3_first_merge_via_newton`,
`x3_first_merge_newton_not_three`).

This is not a special case. It is the \(m=1\), \(p=\pm 1\) instance of
the same-depth criterion: \(N_3\) matches, and \(N_0,N_1,N_2\) agree
modulo \(9\).

---

## 8. Delayed distinctions

Milestone 18: \(\tau(f,g)=1+\min_j v_3(\Delta^j(f-g)(0))\).

For the odd pair \((m,p)\) versus \((m,-p)\) with \(p\neq 0\),
\(\Delta N_2\) and \(\Delta N_1\) both have valuation
\(m+1+v_3(p)\). If \(\mathrm{DZ}^m(p^3)=0\) (automatic when
\(|p^3|<3^m\)), then

\[
\tau(p,-p)=m+2+v_3(p).
\]

**EXACT — HUMAN PROOF** under the vanishing-constant hypothesis;
**COMPUTATIONALLY VERIFIED** for all computed sign pairs through
\(k=10\). In particular \(\pm 1\) at depth \(m\) collide only at
horizon \(k=m+1\).

Zero prefixes: \(f_{0^m}=3^{2m}x^3\), so
\(0^m\equiv_k 0^n\) iff \(k\le 2\min(m,n)\) and \(m,n<k\).

**EXACT — HUMAN PROOF.**

A closed form for \(\tau(w,v)\) on every collision pair, depending only
on \(v_3(p-q)\), is **not** claimed. Higher-order terms from \(N_0\)
appear as soon as \(\mathrm{DZ}^m(p^3)\) is nonzero.

---

## 9. Exact values of \(M_k(x^3)\)

No closed form or linear recurrence was obtained.

**REFUTED:** \(M_{k+1}=3M_k+1\). The raw count does satisfy
\(R_{k+1}=3R_k+1\). The Newton image does not, because raising the
horizon both adds the length-\(k\) layer and refines \(\Phi_k\) to
\(\Phi_{k+1}\).

**COMPUTATIONALLY VERIFIED** values of \(F_k\):

| \(k\) | \(R_k\) | \(M_k\) | \(R_k-M_k\) | \(M_k/R_k\) |
|------:|--------:|--------:|------------:|------------:|
| 1 | 1 | 1 | 0 | 1 |
| 2 | 4 | 3 | 1 | 0.75 |
| 3 | 13 | 12 | 1 | 0.923 |
| 4 | 40 | 36 | 4 | 0.90 |
| 5 | 121 | 115 | 6 | 0.950 |
| 6 | 364 | 349 | 15 | 0.959 |
| 7 | 1093 | 1074 | 19 | 0.983 |
| 8 | 3280 | 3231 | 49 | 0.985 |
| 9 | 9841 | 9780 | 61 | 0.994 |
| 10 | 29524 | 29394 | 130 | 0.996 |

For \(k\le 5\) these \(M_k\) agree with the automata Myhill–Nerode
count. For \(k\ge 6\) the table is the Newton image of \(F_k\), which
is the definition.

The table is **not** the main result. It is evidence that collisions
are sparse and concentrated on high-depth, high-valuation prefixes.

---

## 10. Bounds

Master equation, for any \(f\):

\[
\boxed{
M_k(f)
=
\bigl|\operatorname{Im}(\Phi_k\circ\mathrm{Residual}_f^{(<k)})\bigr|
\le
R_k(f).
}
\]

**EXACT — HUMAN PROOF.**

For \(x^3\),

\[
\frac{3^{r+1}-1}{2}
\le
M_k(x^3)
\le
\frac{3^k-1}{2},
\qquad
r=\bigl\lfloor(k-2)/2\bigr\rfloor.
\]

The upper bound is equality of raw residuals. The lower bound is the
shallow separated layer. Both are exact; neither is an asymptotic fit.
No tighter closed envelope is claimed.

---

## 11. Comparison with \(x^4\)

The same reconstruction applies:

\[
f_w(x)=\mathrm{DZ}^{|w|}\bigl((p(w)+3^{|w|}x)^4\bigr).
\]

The first \(x^4\) merge \(27x^4\equiv_3 729x^4\) is again
\(\Phi_3(-702x^4)=0\) with \(\Phi_4\neq 0\). The common structure is:

\[
(p+3^mx)^d
\;\xrightarrow{\;\mathrm{DZ}^m\;}\;
f_w
\;\xrightarrow{\;\Phi_k\;}\;
C_k(w).
\]

What is new at degree 4 is that even powers of \(p\) survive, so the
odd symmetry \(p\leftrightarrow -p\) is no longer the dominant
collision. This document does **not** compute \(M_k(x^4)\).

---

## 12. Lean inventory

File: `formal/BTCalculus/CubicResidual.lean`. No `sorry`, `admit`, or
`axiom`.

| Theorem | Content |
|---------|---------|
| `sectionDeriv_cubic` | cubic section recurrence |
| `sectionDeriv_cubicResid` | residual-family step |
| `residualAlong_Xcube` | closed form |
| `residualAlong_Xcube_injective` | \(R_k(x^3)=(3^k-1)/2\) |
| `eval_cubicResid_iter` | reconstruction \(\mathrm{DZ}^m((p+3^mx)^3)\) |
| `newton_cubicResid` | Newton coordinates of residuals |
| `newton_section_N3`, `newton_section_N2` | Newton transition |
| `equivK_cubic`, `equivK_cubic_newton` | \(\equiv_k\) iff \(\Phi_k\) |
| `x3_first_merge_via_newton` | first merge from Newton residues |

A cardinality theorem for \(M_k(x^3)\) is **not** formalized.

---

## 13. CLI

```text
btprime calculus newton-class <polynomial> --k <k>
btprime calculus class-collisions <polynomial> --k <k>
```

The first prints residual word, residual polynomial, Newton
coordinates, Newton residues modulo \(3^k\), and a class ID. The
second prints only colliding classes.

---

## 14. Literature

Integer-valued polynomials and the Mahler / Newton binomial basis
(Kempner 1921 and later) are the language of \(\Phi_k\). That is
**REPARAMETERIZATION**, already recorded in Milestone 18.

3-section / Cartier residual automata remain the ambient computational
language.

The project-specific layer is the image of the residual prefix tree of
\(x^3\) under \(\Phi_k\), the explicit map \(F_k\), and the
same-depth / sign-pair collision calculus. That image problem is not a
standard kernel or interpolation theorem.

---

## 15. What this milestone does not claim

- No closed form for \(M_k(x^3)\).
- No linear recurrence in \(k\).
- No formula for \(M_k(x^d)\) when \(d\neq 3\).
- No claim that collisions are congruence classes of \(p(w)\).
- No new kernel, Collatz, prime, or normalization result.

---

## 16. Strongest next question

The image is an explicit arithmetic map. The remaining count is:

> For each depth \(m<k\), how many balanced width-\(m\) prefixes share
> a common \(F_k\)-value, and how do those fibres lift from
> \(k\) to \(k+1\)?

A closed fibre description of \(F_k\) would give \(M_k(x^3)\) exactly.
Do not start that work automatically.
