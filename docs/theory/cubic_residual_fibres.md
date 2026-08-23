# Fibres of the cubic Newton image map

Master record for Milestone 20. The section operator remains a
**(3)-section / Cartier-style reparameterization**. This document
classifies the fibres of

\[
F_k(m,p)=\Phi_k(f_{m,p})
\]

and the resulting exact statements about \(M_k(x^3)\). It does **not**
give a closed cardinality formula for \(M_k(x^3)\).

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_residual_image.md](cubic_residual_image.md),
[cubic_deepest_layer.md](cubic_deepest_layer.md),
[cubic_intermediate_layer.md](cubic_intermediate_layer.md),
[cubic_deficit_two.md](cubic_deficit_two.md),
[cubic_n1_valuation.md](cubic_n1_valuation.md).

---

## 1. The equivalence

Parameters are pairs \((m,p)\) with \(0\le m<k\) and
\(p\in P_m\), where

\[
P_m
=
\bigl\{p\in\mathbb Z:|p|\le(3^m-1)/2\bigr\}.
\]

This is exactly the set of packed length-\(m\) prefixes, and
\(|P_m|=3^m\). **EXACT — HUMAN PROOF.**

\[
(m,p)\sim_k(n,q)
\iff
F_k(m,p)=F_k(n,q).
\]

Then \(M_k(x^3)=|(m,p)/{\sim_k}|\). **EXACT — HUMAN PROOF**
(Milestone 19).

---

## 2. Same-depth criterion

Fix \(m=n\). Then \(N_3\) agrees automatically. The remaining
conditions are

\[
\begin{aligned}
(N_2)&\qquad
3^{k-m-1}\mid(p-q)
&&\text{if }k>m+1,
\text{ else automatic},\\
(N_1)&\qquad
3^{k-1}\mid(p-q)(p+q+3^m),\\
(N_0)&\qquad
3^k\mid D^m(p^3)-D^m(q^3).
\end{aligned}
\]

**EXACT — LEAN VERIFIED** for \(N_2\) and the \(N_1\) factorization
(`sameDepth_n2`, `sameDepth_n2_succ`, `n1Resid_diff`).
**EXACT — HUMAN PROOF** that the three together are necessary and
sufficient (they are \(\Phi_k\) of a cubic).
**COMPUTATIONALLY VERIFIED** against \(F_k\) through \(k=6\).

### \(N_2\) does not imply \(N_1\)

**REFUTED.** Example: \(k=2\), \(m=1\), \(p=0\), \(q=1\). \(N_2\) is
automatic and \(N_1\) fails.

When \(k>m+1\) and \(p\neq -q\), \(N_2\) gives
\(v_3(p-q)\ge k-m-1\), while \(N_1\) needs
\(v_3(p-q)+v_3(p+q+3^m)\ge k-1\). This forces
\(v_3(p+q+3^m)\ge m\), hence \(p=-q\) because \(|p+q|<3^m\).
So for non-sign pairs, \(N_2\) is strictly weaker than \(N_1\).
**EXACT — HUMAN PROOF.**

### \(N_2+N_1\) do not imply \(N_0\)

**REFUTED.** Example: \(k=3\), \(m=2\), \(p=\pm 4\). The odd pair
satisfies \(N_2\) and \(N_1\), but \(D^2(\pm 64)\) do not agree
modulo \(27\).

---

## 3. Shallow separation and \(C_{k,m}\)

If \(2m+1\le k\), then \(N_2\) already forces \(p=q\) on \(P_m\).

**EXACT — LEAN VERIFIED** (`sameDepth_n2_injective`).

Therefore

\[
C_{k,m}=3^m
\qquad\text{whenever }2m+1\le k.
\]

**EXACT — HUMAN PROOF** (injectivity + \(|P_m|=3^m\)).

If \(2m+1>k\), \(C_{k,m}\) may still equal \(3^m\) (the extra \(N_1\)
and \(N_0\) conditions can kill every candidate pair). Examples:
\(C_{6,3}=27\), \(C_{7,4}=81\). There is no claim that the first
deep layer is always compressed.

No closed formula for general \(C_{k,m}\) is obtained.

---

## 4. Cross-depth criterion

\(N_3(m)=2\cdot 3^{2m+1}\). For \(m\le n\),

\[
3^k\mid(N_3(m)-N_3(n))
\iff
k\le 2m+1
\text{ or }m=n.
\]

**EXACT — LEAN VERIFIED** (`n3_dvd_iff`, `n3_dvd_of_deep`).

Hence distinct depths can collide only when both satisfy
\(2m+1\ge k\), i.e. \(m,n\ge\lceil(k-1)/2\rceil\).

After \(N_3\) vanishes, \(N_2\) becomes

\[
3^{m+1}(p+3^m)\equiv 3^{n+1}(q+3^n)\pmod{3^k},
\]

which is automatic if both sides have valuation at least \(k\). Then
\(N_1\) and \(N_0\) decide the pair, exactly as in the same-depth
deep regime.

The zero residuals \(p=q=0\) agree across depths as soon as
\(N_1(m,0)=3^{2m}\) also vanishes, i.e. \(m\ge\lceil k/2\rceil\).
**EXACT — HUMAN PROOF.**

Those depths form a single Newton class (the **zero spine**), which
absorbs the deepest \(0\)-fibre described below.

---

## 5. Role of the four coordinates

| Coordinate | Same depth | Cross depth |
|------------|------------|-------------|
| \(N_3\) | automatic | depth gate: both \(2m+1\ge k\) |
| \(N_2\) | \(3^{k-m-1}\mid(p-q)\) | valuation of \(p+3^m\) |
| \(N_1\) | extra unless \(p=-q\) | matches \(3p^2\) when leading terms vanish |
| \(N_0\) | independent; not implied | \(D^m(p^3)\) vs \(D^n(q^3)\) |

No coordinate is redundant in general. **EXACT — HUMAN PROOF.**

---

## 6. Sign-pair fibres

For \(p\neq 0\),

\[
F_k(m,p)=F_k(m,-p)
\iff
3^{\max(k-m-1,0)}\mid p
\text{ and }
3^k\mid D^m(p^3).
\]

The first clause is exactly \(N_2\), and for the odd pair it is
equivalent to \(N_1\).

**EXACT — LEAN VERIFIED** (`sameDepth_n2_sign`, `sameDepth_n1_sign`,
`sign_n2_of_n1`, `sign_n0`, `iterDZ_neg`).

If \(|p^3|<3^m\), then \(D^m(p^3)=0\) and the second clause is free.
In that case \(\tau(p,-p)=m+2+v_3(p)\), so the pair collides for
every horizon \(m<k\le m+1+v_3(p)\). **EXACT — HUMAN PROOF.**

Sign pairs do **not** exhaust the fibres. **REFUTED** as a complete
classification (zero clusters, high-valuation cosets, and
cross-depth extensions).

---

## 7. High-valuation clusters

At the deepest layer \(m=k-1\), the fibre of \(0\) is

\[
\bigl\{q\in P_{k-1}:3^{\lceil(2k-1)/3\rceil}\mid q\bigr\}.
\]

Its size is \(3^{k-1-\lceil(2k-1)/3\rceil}\).

**EXACT — HUMAN PROOF** from \(N_1\equiv 3q^2\) and
\(N_0=q^3/3^{k-1}\) on this layer; **COMPUTATIONALLY VERIFIED**
through \(k=12\).

Other deep fibres are cosets of the same shape: sign pairs around
\(\pm 3^a\), triples \(a+3^t P_1\), and occasional pairs such as
\(3^6\pm 3^2\) at \(k=8\). They are solutions of the fibre
congruences, not a separate mechanism.

**CONJECTURE:** every same-depth fibre is a finite union of
cosets \(\alpha+3^r P_t\). Not claimed as a theorem.

---

## 8. Per-depth counts and intersections

**COMPUTATIONALLY VERIFIED:**

| \(k\) | \(C_{k,0},\ldots,C_{k,k-1}\) | \(\sum C\) | \(M_k\) |
|------:|------------------------------|----------:|--------:|
| 2 | 1, 2 | 3 | 3 |
| 3 | 1, 3, 8 | 12 | 12 |
| 4 | 1, 3, 9, 24 | 37 | 36 |
| 5 | 1, 3, 9, 27, 76 | 116 | 115 |
| 6 | 1, 3, 9, 27, 80, 232 | 352 | 349 |
| 7 | 1, 3, 9, 27, 81, 240, 716 | 1077 | 1074 |
| 8 | 1, 3, 9, 27, 81, 243, 721, 2153 | 3238 | 3231 |
| 9 | 1, 3, 9, 27, 81, 243, 727, 2178, 6521 | 9790 | 9780 |
| 10 | 1, 3, 9, 27, 81, 243, 729, 2180, 6537, 19597 | 29407 | 29394 |
| 11 | 1, 3, 9, 27, 81, 243, 729, 2185, 6554, 19652, 58939 | 88423 | 88399 |
| 12 | 1, 3, 9, 27, 81, 243, 729, 2187, 6555, 19661, 58977, 176908 | 265381 | 265352 |

Cross-depth overcount is \(\sum C-M_k\). For \(k\ge 4\) it is exactly
the zero-spine multiplicity plus the surviving sign spines (and, at
\(k=8\), two prefix-extension pairs \(\pm 117\sim\pm 1089\)).

\[
M_k
=
\sum_{m<k}C_{k,m}
-
\sum_{\text{classes}}(d_c-1),
\]

where \(d_c\) is the number of depths meeting a class. **EXACT —
HUMAN PROOF.**

---

## 9. Exact \(M_k(x^3)\)

No closed form. **REFUTED:** \(M_{k+1}=3M_k+1\).

The exact description remains

\[
M_k(x^3)=|\operatorname{Im} F_k|=|(m,p)/{\sim_k}|
\]

with \(\sim_k\) given by the criteria above.

---

## 10. Bounds

Shallow lower bound (Milestone 19), now with a Lean \(N_2\)
injection:

\[
M_k(x^3)\ge\frac{3^{r+1}-1}{2},
\qquad
r=\bigl\lfloor(k-2)/2\bigr\rfloor.
\]

Zero-spine upper correction: for \(k\ge 2\),

\[
M_k
\le
\sum_{m<k}C_{k,m}
-
\max\bigl(\lfloor k/2\rfloor-1,0\bigr),
\]

and \(C_{k,m}=3^m\) on \(2m+1\le k\). **EXACT — HUMAN PROOF.**

The compression \(R_k-M_k\) is **not** claimed to be asymptotically
negligible.

---

## 11. Fibre lifting

Raising the horizon from \(k\) to \(k+1\) refines \(\Phi_k\). A class
splits iff some pair inside it has \(\tau=k+1\). The new depth
\(m=k\) contributes \(C_{k+1,k}\) classes, and the zero spine grows
by one layer when \(k\) is even.

This is a structural lifting law, not a closed recurrence for
\(M_k\). **EXACT — HUMAN PROOF** as a description;
**CONJECTURE** that no linear recurrence of small order exists.

**COMPUTATIONALLY VERIFIED** split counts of existing classes
(\(m<k\)) when the horizon rises from \(k\) to \(k+1\):

| \(k\) | \(M_k\) | stay | split |
|------:|--------:|-----:|------:|
| 4 | 36 | 32 | 4 |
| 5 | 115 | 112 | 3 |
| 6 | 349 | 341 | 8 |
| 7 | 1074 | 1067 | 7 |
| 8 | 3231 | 3207 | 24 |
| 9 | 9780 | 9761 | 19 |
| 10 | 29394 | 29342 | 52 |

The new depth \(m=k\) is not included in those split counts. No
closed splitting law is claimed.

---

## 12. Lean inventory

File: `formal/BTCalculus/CubicFibres.lean`. No `sorry`, `admit`, or
`axiom`.

| Theorem | Content |
|---------|---------|
| `sameDepth_n2`, `sameDepth_n2_succ` | \(N_2\) criterion |
| `sameDepth_n2_injective` | shallow prefixes are \(N_2\)-separated |
| `n1Resid_diff` | \(N_1\) factorization |
| `n3_dvd_iff`, `n3_dvd_of_deep` | cross-depth \(N_3\) gate |
| `sameDepth_n2_sign`, `sameDepth_n1_sign`, `sign_n2_of_n1` | sign-pair \(N_2\leftrightarrow N_1\) |
| `iterDZ_neg`, `sign_n0` | sign-pair \(N_0\) |

A closed formula for \(M_k(x^3)\) is **not** formalized.

---

## 13. CLI

```text
btprime calculus cubic-fibres --k <k>
btprime calculus cubic-fibre <m> <p> --k <k>
```

---

## 14. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The fibre
geometry of a residual prefix tree under \(\Phi_k\) is
project-specific.

---

## 15. What this milestone does not claim

- Arithmetic image computed through \(k=12\) (domain \(R_{12}=265720\)).
  No automata minimizer was used for \(k\ge 6\).
- No closed form for \(M_k(x^3)\) or \(C_{k,m}\) in the deep regime.
- No linear recurrence.
- No claim that every fibre is a sign pair.
- No claim that fibre sizes are powers of \(3\) (the \(0\)-fibre is;
  mixed cosets need not be).
- No work on \(x^4\), primes, Collatz, or normalization.

---

## 16. Strongest next question

Closed by Milestone 21. See [cubic_deepest_layer.md](cubic_deepest_layer.md).
The remaining obstruction to a single-term \(C_{k,k-1}\) is the
family of intermediate surpluses \(S_{k,s}\).

Do not start that work automatically.
