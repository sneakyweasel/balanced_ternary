# General N1 refinement and the 3-adic valuation stratification

Master record for Milestone 24. Residual depth is written as the
depth deficit

\[
r=k-1-m.
\]

Milestone 23 proved the linear visibility law

\[
N_2(p)\equiv N_2(q)\pmod{3^k}
\iff
p\equiv q\pmod{3^r}
\]

in the valid range \(r+1\le k\). This document asks what \(N_1\) does
with those visible residue classes. It does **not** give a formula for
\(M_k(x^3)\), a general \(N_0\) theory, or a generic deficit solver.

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_deficit_two.md](cubic_deficit_two.md),
[cubic_intermediate_layer.md](cubic_intermediate_layer.md),
[cubic_deepest_layer.md](cubic_deepest_layer.md).

---

## 1. Exact \(N_1\) difference after the \(N_2\) filter

Write \(m=k-1-r\) and

\[
N_1(p)=3^{2m}+3^{m+1}p+3p^2,\qquad
N_2(p)=2\cdot 3^{m+1}(p+3^m).
\]

The identity

\[
N_1(p)-N_1(q)=3(p-q)(p+q+3^m)
\]

is already **EXACT — LEAN VERIFIED** (`n1Resid_diff`). Therefore

\[
N_1(p)\equiv N_1(q)\pmod{3^k}
\iff
3^{k-1}\mid(p-q)(p+q+3^m)
\]

whenever \(1\le k\). **EXACT — LEAN VERIFIED** (`deficit_n1_iff`).

After the \(N_2\) filter, \(p-q=3^r\delta\). Substituting gives the
exact post-filter law

\[
N_1(p)\equiv N_1(q)\pmod{3^k}
\iff
3^{k-1-r}\mid\delta(p+q+3^m).
\]

**EXACT — LEAN VERIFIED** (`n1_after_n2_iff`). No heuristic valuation
is used.

---

## 2. Valuation-stratified \(N_1\) theorem

Assume \(r\ge 1\), \(r+1\le k\), and \(p,q\in P_m\) with
\(m=k-1-r\). After \(N_2\) equality one has \(p\equiv q\pmod{3^r}\).

Write \(s=v_3(p)\) when \(p\neq 0\). Because a nonzero prefix in
\(P_m\) satisfies \(|p|<(3^m)\), one has \(s<m\). Combined with
\(p\equiv q\pmod{3^r}\), the same valuation is forced on \(q\)
whenever \(s<r\). Then

\[
p+q+3^m=3^s(u+v+3^{m-s}),\qquad 3\nmid(u+v+3^{m-s}),
\]

so the post-filter \(N_1\) condition upgrades \(3^r\mid(p-q)\) to
\(3^m\mid(p-q)\). Balanced width then forces \(p=q\).

**EXACT — LEAN VERIFIED** (`n1_low_val_injective`, `n1_val_lt_injective`):

\[
\begin{aligned}
&m=k-1-r,\quad
p\equiv q\pmod{3^r},\\
&v_3(p)<r,\quad
N_1(p)\equiv N_1(q)\pmod{3^k}
\end{aligned}
\Longrightarrow
p=q.
\]

The exact range is \(1\le r\) and \(r+1\le k\), on the balanced
prefix domain \(P_m\). The theorem is **not** claimed for \(r=0\):
there \(N_2\) is vacuous and unit sign pairs survive \(N_1\).

No counterexample was found for \(r=1,\ldots,5\) and
\(k\le r+7\) with \(m\le 8\). **COMPUTATIONALLY VERIFIED**. The
smallest-obstruction search is empty.

---

## 3. Unit injectivity

The case \(s=0\) is the unit theorem.

**EXACT — LEAN VERIFIED** (`n1_unit_injective`, specialised as
`n1_unit_r1`, `n1_unit_r2`):

\[
3\nmid p
\land
N_2(p)\equiv N_2(q)
\land
N_1(p)\equiv N_1(q)
\Longrightarrow
p=q
\]

on \(P_m\), for every \(r\ge 1\) with \(r+1\le k\). Equivalently,
\(N_2+N_1\) is injective on

\[
U_{k,r}=\{p\in P_m:3\nmid p\}.
\]

At \(r=0\) this is **REFUTED**: \(N_1(1)\equiv N_1(-1)\) at every
horizon (sign pairs of units).

---

## 4. Surviving locus \(3^r\mathbb Z\)

**EXACT — LEAN VERIFIED** (`n21_fibre_in_pow`):

\[
\text{every nontrivial }N_2+N_1\text{ fibre on }P_m
\text{ lies in }3^r\mathbb Z.
\]

This is the generalisation of the observed \(r=1\) locus \(3\mid p\)
and the \(r=2\) locus \(9\mid p\). Membership in \(3^r\mathbb Z\) is
**necessary** for a nontrivial merge after \(N_1\). It is **not**
sufficient.

On the remaining locus \(p=3^ru\), \(q=3^rv\) the post-filter
condition bifurcates.

| range | remaining \(N_1\) |
|---|---|
| \(k<2r+1\) | only \(p=0\) can be \(3^r\)-divisible in \(P_m\) |
| \(k=2r+1\) | \(N_1\) is automatic on that locus |
| \(k\ge 2r+2\) | \(N_1(3^ru)\equiv N_1(3^rv)\pmod{3^k}\) iff deepest-layer \(N_1\) agrees on \((u,v)\) at horizon \(k-2r\) |

**EXACT — LEAN VERIFIED** for the last row (`n1_high_val_scaled`):

\[
3^k\mid N_1(3^ru)-N_1(3^rv)
\iff
3^{k-2r}\mid N_1^{(k-2r-1)}(u)-N_1^{(k-2r-1)}(v).
\]

This is **partial recursion** (outcome B). Only the high-valuation
stratum, and only when \(k\ge 2r+2\), reduces to a deepest-layer
\(N_1\) problem. It is not a recursive solution of the full fibre
relation: \(N_0\) is still absent, and the reduction does not
reproduce the original deficit-\(r\) problem.

---

## 5. Sign-pair corollary

For \(q=-p\), both \(N_2\) and \(N_1\) collapse to the same
divisibility.

**EXACT — LEAN VERIFIED** (`n21_sign_n2_iff`, `n21_sign_n1_iff`,
`n21_sign_iff`): if \(1\le k\) and \(r+1\le k\), then

\[
p\sim -p\text{ after }N_2+N_1
\iff
3^r\mid p.
\]

This is a corollary of the valuation theorem plus the factor-of-two
lemma `three_pow_dvd_of_two_mul_pow`, not a separate empirical
pattern. It recovers:

- \(r=0\): units can survive;
- \(r=1\): sign pairs require \(3\mid p\);
- \(r=2\): sign pairs require \(9\mid p\).

---

## 6. What \(N_0\) still distinguishes

Restrict to a nontrivial \(N_2+N_1\) fibre inside \(3^r\mathbb Z\).
Then \(N_0=D^m(p^3)\) can still split:

- **sign pairs** \(p\sim -p\) with \(3^r\mid p\) and \(p\neq 0\);
- the **zero fibre** versus nearby multiples of \(3^r\);
- **translated cosets** of a high power of \(3\);
- occasional **exceptional twins** that share \(N_1\) but not \(N_0\).

No general \(N_0\) theorem is claimed. After the \(N_1\) filter,
\(N_0\) is the remaining cubic-quotient layer on the
\(3^r\)-divisible locus. Whether that layer itself rescales to a
deepest-layer \(N_0\) problem at horizon \(k-2r\) is **not**
proved here.

**COMPUTATIONALLY VERIFIED** examples:

- At \((r,k)=(2,9)\) the \(N_2+N_1\) fibre of \(0\) is the
  nine-point set \(\{-324,-243,\ldots,324\}\). \(N_0\) splits it
  down to the known full Newton fibre \(\{-243,0,243\}\) and
  isolates the other coset representatives. So \(N_0\) refines the
  surviving locus; it does not automatically produce singletons.
- At \((r,k)=(3,9)\) the four surviving \(N_2+N_1\) fibres are
  \(\{\pm 27\}\), \(\{\pm 54\}\), \(\{\pm 108\}\), and
  \(\{-81,0,81\}\). \(N_0\) separates every pair in that sample.
- At \((r,k)=(1,6)\) every unit is already a singleton and the
  eleven surviving merges lie in \(3\mathbb Z\).

---

## 7. Recovery of \(r=1\) and \(r=2\)

The general theorems specialise automatically.

### \(r=1\) (\(m=k-2\))

- \(N_2\) sees \(p\bmod 3\) (`depthDeficit_n2_visibility`);
- \(N_1\) kills every unit (`n1_unit_r1`);
- nontrivial \(N_2+N_1\) fibres lie in \(3\mathbb Z\).

### \(r=2\) (\(m=k-3\))

- \(N_2\) sees \(p\bmod 9\);
- \(N_1\) kills every \(v_3(p)<2\) class (`n1_unit_r2` plus
  `n1_low_val_injective`);
- nontrivial \(N_2+N_1\) fibres lie in \(9\mathbb Z\).

These are not separate ad hoc proofs.

---

## 8. Visibility / refinement table

Only proved rows are listed.

| deficit | \(N_2\) sees | \(N_1\) removes | remaining locus |
|---|---|---|---|
| \(0\) | nothing | quadratic / sign filtering; units can survive | all \(p\) |
| \(1\) | \(p\bmod 3\) | units (\(v_3(p)<1\)) | \(3\mid p\) |
| \(2\) | \(p\bmod 9\) | \(v_3(p)<2\) | \(9\mid p\) |
| general \(r\ge 1\) | \(p\bmod 3^r\) | \(v_3(p)<r\) | \(3^r\mid p\) |

The last row is **EXACT — LEAN VERIFIED** for the refinement
statement. The count of \(N_2\) classes is \(3^r\) once
\(m\ge r\) (i.e. \(k\ge 2r+1\)).

---

## 9. Computational validation

Direct arithmetic, no automata minimizer. For each pair below,
every nontrivial \(N_2+N_1\) fibre lies in \(3^r\mathbb Z\),
unit classes equal unit prefixes, and the low-valuation collision
search is empty.

| \(r\) | \(k\) | \(m\) | \(N_2\) | \(N_2+N_1\) | nontrivial fibres | note |
|---|---|---|---|---|---|---|
| \(1\) | \(6\) | \(4\) | \(3\) | \(65\) | \(11\) | recovers Milestone 22 |
| \(1\) | \(7\) | \(5\) | \(3\) | \(193\) | \(31\) | |
| \(2\) | \(7\) | \(4\) | \(9\) | \(76\) | \(4\) | recovers Milestone 23 |
| \(2\) | \(8\) | \(5\) | \(9\) | \(227\) | \(11\) | |
| \(3\) | \(8\) | \(4\) | \(27\) | \(80\) | \(1\) | first new deficit |
| \(3\) | \(9\) | \(5\) | \(27\) | \(238\) | \(4\) | |
| \(4\) | \(10\) | \(5\) | \(81\) | \(242\) | \(1\) | |
| \(5\) | \(11\) | \(5\) | \(243\) | \(243\) | \(0\) | only \(0\) is \(3^5\)-divisible |
| \(5\) | \(12\) | \(6\) | \(243\) | \(728\) | \(1\) | sign pair \(\{\pm 243\}\) |

**COMPUTATIONALLY VERIFIED**. Computation is not a substitute for
the Lean theorems above.

---

## 10. Counterexamples

None for the gold theorem on \(P_m\) in the stated range. The
only sharp negative is \(r=0\) unit injectivity, which is
excluded from the theorem.

---

## 11. CLI

```
btprime calculus n1-strata --k <k> --deficit <r>
btprime calculus n1-fibre <p> --k <k> --deficit <r>
```

The existing `cubic-layer` commands for deficits \(1\) and \(2\)
are unchanged. This is not a generic deficit engine: it reports
the \(N_2+N_1\) valuation stratification only.

---

## 12. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The
valuation-stratified refinement law is project-specific.

---

## 13. What this milestone does not claim

- No formula for \(M_k(x^3)\) or \(C_{k,m}\).
- No general \(N_0\) theorem.
- No claim that \(p=3^ru\) reduces the **full** fibre problem to
  a smaller copy of the same deficit-\(r\) problem.
- No \(x^4\), primes, Collatz, or hardware.
- No generic \((r)\)-solver.

---

## 14. Strongest next question

After \(N_2+N_1\) confine fibres to \(3^r\mathbb Z\), does
\(N_0=D^{k-1-r}(p^3)\) on \(p=3^ru\) reduce to a deepest-layer
cubic-quotient problem at horizon \(k-2r\), or is that the next
obstruction?

Do not start that work automatically.
