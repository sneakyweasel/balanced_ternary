# Deepest-layer fibres of \(x^3\)

Master record for Milestone 21. The residual of \(x^3\) at depth
\(m=k-1\) is controlled by two Newton coordinates. This document
records their exact simplification, the fibre criterion, the zero
fibre, the unit/sign analysis, and the stratified count of
\(C_{k,k-1}\). It does **not** give a single-term closed formula for
\(C_{k,k-1}\) or for \(M_k(x^3)\).

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_residual_fibres.md](cubic_residual_fibres.md).

---

## 1. Deepest-layer Newton formulas

Set \(m=k-1\). Then

\[
\begin{aligned}
N_3&=2\cdot 3^{2k-1},\\
N_2&=2\cdot 3^k(p+3^{k-1}),\\
N_1&=3^{2k-2}+3^k p+3p^2,\\
N_0&=D^{k-1}(p^3).
\end{aligned}
\]

For \(k\ge 1\), \(N_3\equiv N_2\equiv 0\pmod{3^k}\).
For \(k\ge 2\),

\[
N_1\equiv 3p^2\pmod{3^k}.
\]

**EXACT — LEAN VERIFIED** (`deepest_n3_zero`, `deepest_n2_zero`,
`deepest_n1_mod`).

The reconstruction identity gives

\[
p^3=\operatorname{bal}_{k-1}(p^3)+3^{k-1}D^{k-1}(p^3),
\]

with \(\operatorname{bal}_{k-1}(z)\in P_{k-1}\). Equivalently

\[
N_0=\frac{p^3-\operatorname{bal}_{k-1}(p^3)}{3^{k-1}}.
\]

If \(3^{k-1}\mid p^3\), then the balanced residue is \(0\) and
\(N_0=p^3/3^{k-1}\). **EXACT — LEAN VERIFIED** (`iterDZ_of_dvd`,
`n0Resid_of_dvd`). The residue is **not** always zero: it vanishes
precisely when \(3^{k-1}\mid p^3\).

---

## 2. Square congruence

On \(P_{k-1}\),

\[
N_1(p)\equiv N_1(q)\pmod{3^k}
\iff
p^2\equiv q^2\pmod{3^{k-1}}
\iff
3^{k-1}\mid(p-q)(p+q).
\]

**EXACT — LEAN VERIFIED** (`deepest_n1_iff`, `deepest_sq_of_n1`).

Because \(P_{k-1}\) is the interval of width \(3^{k-1}-1\),

\[
3^{k-1}\mid(p-q)\implies p=q,
\qquad
3^{k-1}\mid(p+q)\implies p=-q.
\]

**EXACT — LEAN VERIFIED** (`balWidth_dvd_sub`, `balWidth_dvd_add`).

Therefore a nontrivial valuation split
\(v_3(p-q)+v_3(p+q)\ge k-1\) with both factors positive forces
\(3\mid p\) and \(3\mid q\). **EXACT — HUMAN PROOF.**
Units collide under the square condition only as \(\{p,-p\}\).

---

## 3. Cubic quotient

\[
N_0(p)\equiv N_0(q)\pmod{3^k}
\iff
p^3-q^3\equiv
\operatorname{bal}_{k-1}(p^3)-\operatorname{bal}_{k-1}(q^3)
\pmod{3^{2k-1}}.
\]

**EXACT — LEAN VERIFIED** as the reconstruction identity
(`n0_congr_decomp`). This is **not** equivalent to
\(p^3\equiv q^3\pmod{3^{2k-1}}\) unless the balanced residues agree.
**EXACT — HUMAN PROOF.**

---

## 4. Combined fibre criterion

For \(p,q\in P_{k-1}\) and \(k\ge 1\),

\[
F_k(k-1,p)=F_k(k-1,q)
\iff
p^2\equiv q^2\pmod{3^{k-1}}
\;\land\;
D^{k-1}(p^3)\equiv D^{k-1}(q^3)\pmod{3^k}.
\]

**EXACT — LEAN VERIFIED** (`deepest_equiv_iff`).
**COMPUTATIONALLY VERIFIED** against \(F_k\) through \(k=6\).

For units this collapses to the sign-pair law

\[
F_k(k-1,p)=F_k(k-1,-p)
\iff
3^k\mid D^{k-1}(p^3).
\]

**EXACT — LEAN VERIFIED** (`sign_deepest`).

---

## 5. Zero fibre

Let \(r(k)=\lceil(2k-1)/3\rceil=(2k+1)//3\). For \(k\ge 2\),

\[
F_k(k-1,p)=F_k(k-1,0)
\iff
3^{r(k)}\mid p.
\]

The fibre is the ball \(3^{r(k)}P_{k-1-r(k)}\) and has size

\[
Z_k=3^{k-1-r(k)}.
\]

**EXACT — LEAN VERIFIED** (`zero_fibre_of`, `zero_fibre_imp`).
**COMPUTATIONALLY VERIFIED** through \(k=12\).

---

## 6. Coset conjecture

Milestone 20 conjectured that every same-depth fibre is a finite
union of full residue classes \(\alpha+3^r P_t\).

At \(k=8\) the pairs \(\{720,738\}\) and \(\{-738,-720\}\) are
twins \(3^6\pm 3^2\), not a full class modulo any \(3^r\) with
\(r\ge 1\). **REFUTED** as a complete classification by nontrivial
full cosets. They remain highly structured (\(3\)-adic twins).

High-valuation fibres **are** often full cosets: the zero fibre, and
the size-\(3\) classes \(3^4(u+3^2 P_1)\) at \(k=8\).
**COMPUTATIONALLY VERIFIED.**

---

## 7. Fibre normal form

Every deepest fibre observed through \(k=14\) is one of:

1. a singleton;
2. a sign pair \(\{p,-p\}\);
3. the zero ball \(3^{r(k)}P_{k-1-r(k)}\);
4. a translated high-valuation coset \(\alpha+3^\mu P_t\);
5. a twin \(\varepsilon 3^a\pm 3^b\).

**COMPUTATIONALLY VERIFIED** through \(k=8\) with explicit labels;
types \(1\)–\(3\) are theorems. Type \(5\) first appears at \(k=8\).
No claim that this list is exhaustive for all \(k\).

---

## 8. Exact \(C_{k,k-1}\)

Write \(p=3^s u\) with \(3\nmid u\). The pair \((N_1,N_0)\) records
the valuation \(s\) whenever \(2s+1<k\). Let

\[
s_0(k)=\lceil(k-1)/2\rceil=k//2,
\qquad
r(k)=\lceil(2k-1)/3\rceil.
\]

Then

\[
C_{k,k-1}
=
1+\sum_{s=0}^{r(k)-1} I_{k,s},
\]

where \(I_{k,s}\) is the number of distinct invariants among exact
valuation \(s\), and the \(+1\) is the zero class (all \(s\ge r(k)\)).

**EXACT — HUMAN PROOF** (disjointness of \(v_3(N_1)\) plus the zero
class). **COMPUTATIONALLY VERIFIED** through \(k=12\).

### High strata (\(s_0\le s<r\))

Here \(N_1\equiv 0\) and \(N_0=3^{3s-k+1}u^3\), so \(I_{k,s}\) is
the number of unit cubes of \(P_{k-1-s}\) modulo \(3^{2k-1-3s}\).

\[
J(k,s)=
\begin{cases}
2\cdot 3^{k-s-2} & \text{if }2s=k-1,\\
2 & \text{if }2s\ge k\text{ and }\nu=1,\\
2\cdot 3^{\nu-2} & \text{if }2s\ge k\text{ and }\nu\ge 2,
\end{cases}
\]

with \(\nu=2k-1-3s\). The odd-horizon case \(2s=k-1\) is injective
because nontrivial cube roots of unity modulo \(3^{\mu+1}\) lie
outside \(P_\mu\). **EXACT — HUMAN PROOF.**
**COMPUTATIONALLY VERIFIED** on \(k\le 12\).

### Unit stratum (\(s=0\))

\[
I_{k,0}=2\cdot 3^{k-2}-S_{k,0},
\qquad
S_{k,0}=T_k-\lfloor T_k/3\rfloor+L(k),
\]

where \(T_k=\lfloor((3^{k-1}-1)/2)^{1/3}\rfloor\) counts small units
with \(D^{k-1}(p^3)=0\), and \(L(k)\) is the number of large units
satisfying \(|p^3-t\,3^{2k-1}|\le(3^{k-1}-1)/2\).

**EXACT — HUMAN PROOF** for the split into small/large.
**COMPUTATIONALLY VERIFIED:** \(L(k)=0\) for odd \(k\le 17\);
the endpoint \(B_{k-1}=(3^{k-1}-1)/2\) is always a large solution
for even \(k\in\{4,\ldots,16\}\); extras exist at \(k=8\) (\(907\))
and \(k=16\) (\(2198089\)).

**CONJECTURE:** \(L(k)=0\) for every odd \(k\); the endpoint works
for every even \(k\ge 4\); extras are sporadic.

### Intermediate strata (\(1\le s<s_0\))

Same shape \(I_{k,s}=2\cdot 3^{k-2-s}-S_{k,s}\) with a smaller
surplus. No closed formula for every \(S_{k,s}\) is claimed.

There is therefore **no single-term closed \(F(k)\)** for
\(C_{k,k-1}\). The count is exact as the stratified sum above.

---

## 9. Computational range

\(C_{k,k-1}\) by hashing \((N_1,N_0)\), not the automaton:

| \(k\) | \(3^{k-1}\) | \(C_{k,k-1}\) |
|------:|------------:|--------------:|
| 2 | 3 | 2 |
| 3 | 9 | 8 |
| 4 | 27 | 24 |
| 5 | 81 | 76 |
| 6 | 243 | 232 |
| 7 | 729 | 716 |
| 8 | 2187 | 2153 |
| 9 | 6561 | 6521 |
| 10 | 19683 | 19597 |
| 11 | 59049 | 58939 |
| 12 | 177147 | 176908 |
| 13 | 531441 | 531141 |
| 14 | 1594323 | 1593644 |

Matches the Milestone 20 deepest column for \(k\le 12\).

---

## 10. Other deep layers

| \(k\) | \(C_{k,k-3}\) | \(C_{k,k-2}\) | \(C_{k,k-1}\) |
|------:|--------------:|--------------:|--------------:|
| 6 | 27 | 80 | 232 |
| 7 | 81 | 240 | 716 |
| 8 | 243 | 721 | 2153 |
| 13 | 59022 | 177057 | 531141 |

\(C_{k,k-2}\) is close to, but strictly larger than, \(C_{k-1,k-2}\)
(the previous deepest layer): \(721>716\), \(177057>176908\).
\(N_2\) begins to separate states one layer above the deepest.
The same \(3\)-adic mechanism governs deep layers only after the
surviving coordinates are rewritten at that depth.
**CONJECTURE** for general \(m\), not proved here.

---

## 11. Consequences for \(M_k(x^3)\)

Milestone 20 still applies:

\[
M_k=\sum_{m<k}C_{k,m}-\text{cross-depth overcount}.
\]

The deepest term is now an exact stratified count, not a hash table.
The remaining obstruction to a closed \(M_k\) is the family
\(C_{k,m}\) for \(\lceil(k-1)/2\rceil\le m<k-1\) together with the
zero-spine overcount. Do not treat \(C_{k,k-1}\) as a global formula
for \(M_k\).

---

## 12. Lean inventory

File: `formal/BTCalculus/CubicDeepestLayer.lean`. No `sorry`,
`admit`, or `axiom`.

| Theorem | Content |
|---------|---------|
| `deepest_n1_mod`, `deepest_n2_zero`, `deepest_n3_zero` | Newton simplification |
| `deepest_n1_iff`, `deepest_equiv_iff` | fibre criterion |
| `sq_factor`, `deepest_sq_of_n1`, `balWidth_dvd_sub/add` | square analysis |
| `n0_congr_decomp`, `iterDZ_of_dvd` | cubic quotient |
| `zero_fibre_of`, `zero_fibre_imp` | zero fibre |
| `sign_deepest` | unit sign pairs |
| `three_pow_dvd_sq`, `three_pow_dvd_cube` | valuation lemmas |

A single-term formula for \(C_{k,k-1}\) is **not** formalized.

---

## 13. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The
deepest-layer fibre geometry (unit signs, cube-count high strata,
sporadic twins) is project-specific.

---

## 14. What this milestone does not claim

- No single-term closed \(C_{k,k-1}\) or \(M_k(x^3)\).
- No claim that every fibre is a full \(3\)-adic coset.
- No claim that every collision is a sign pair.
- No work on \(x^4\), primes, Collatz, or normalization.

---

## 15. Strongest next question

Derive a closed formula for the intermediate surpluses \(S_{k,s}\)
(\(1\le s<s_0(k)\)), or prove that they are given by the small-unit
count of a scaled horizon. That would turn the stratified sum into
an explicit arithmetic formula for \(C_{k,k-1}\).

Do not start that work automatically.
