# First intermediate cubic layer (\(m=k-2\))

Master record for Milestone 22. One unresolved ternary digit remains
below the deepest residual depth. This document records the exact
Newton simplification at depth deficit \(r=1\), the fibre criterion
for \(F_k(k-2,p)\), the Newton hierarchy, the horizon-lift surplus
\(\Delta_k\), and the comparison with the deepest layer. It does
**not** give a single-term closed formula for \(C_{k,k-2}\) or for
\(M_k(x^3)\).

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_deepest_layer.md](cubic_deepest_layer.md),
[cubic_residual_fibres.md](cubic_residual_fibres.md),
[cubic_deficit_two.md](cubic_deficit_two.md).

---

## 1. Exact \(m=k-2\) Newton formulas

The general cubic residual Newton coordinates are

\[
\begin{aligned}
N_0&=D^m(p^3),\\
N_1&=3^{2m}+3^{m+1}p+3p^2,\\
N_2&=2\cdot 3^{m+1}(p+3^m),\\
N_3&=2\cdot 3^{2m+1}.
\end{aligned}
\]

Set \(m=k-2\). Then

\[
\begin{aligned}
N_3&=2\cdot 3^{2k-3},\\
N_2&=2\cdot 3^{k-1}(p+3^{k-2}),\\
N_1&=3^{2k-4}+3^{k-1}p+3p^2,\\
N_0&=D^{k-2}(p^3).
\end{aligned}
\]

Side-by-side with the deepest layer:

```text
depth m=k-1
    N3 ≡ 0
    N2 ≡ 0
    N1 ≡ 3 p^2
    N0  = D^{k-1}(p^3)

depth m=k-2
    N3 ≡ 0                 (k ≥ 3)
    N2 ≡ 2 · 3^{k-1} p     (k ≥ 3)
    N1 ≡ 3 p^2 + 3^{k-1} p (k ≥ 4)
    N0  = D^{k-2}(p^3)
```

The terms that vanish at \(m=k-1\) and survive at \(m=k-2\) are
exactly \(2\cdot 3^{2k-3}\) in \(N_2\) (killed for \(k\ge 3\), but
the leftover factor \(2\cdot 3^{k-1}p\) is **not** killed) and
\(3^{2k-4}\) in \(N_1\) (killed for \(k\ge 4\)), leaving the extra
linear term \(3^{k-1}p\).

**EXACT — LEAN VERIFIED** (`inter_n3_zero`, `inter_n2_mod`,
`inter_n1_mod`).

Consequence: \(N_2\) sees only \(p\bmod 3\). It is **not** enough
to recover \(p\) up to sign. \(N_1\) is the first genuine
correction. \(N_0\) remains independent.

---

## 2. Same-depth fibre criterion

\[
F_k(k-2,p)=F_k(k-2,q)
\iff
\mathcal A_k(p,q),
\]

where

\[
\mathcal A_k(p,q)
:\Longleftrightarrow
p\equiv q\pmod{3}
\;\land\;
3^{k-1}\mid(p-q)(p+q+3^{k-2})
\;\land\;
3^k\mid D^{k-2}(p^3)-D^{k-2}(q^3).
\]

**EXACT — LEAN VERIFIED** (`inter_equiv_iff`, via `inter_n2_iff`
and `inter_n1_iff`). This is the Milestone 20 same-depth criterion
specialized to \(m=k-2\).

On \(P_{k-2}\), \(3^{k-2}\mid(p-q)\) still forces \(p=q\), but the
\(N_2\) condition is only modulus \(3\). Candidate fibres are
therefore residue classes modulo \(3\), not singletons or mere
sign pairs.

---

## 3. Role of \(N_2\), \(N_1\), \(N_0\)

### \(N_2\)

\[
N_2(p)\equiv N_2(q)\pmod{3^k}
\iff
3\mid(p-q).
\]

**EXACT — LEAN VERIFIED** (`inter_n2_iff`). For \(k\ge 3\) this
produces exactly three classes. **COMPUTATIONALLY VERIFIED**
through \(k=13\).

The ambiguity inside \(P_{k-2}\) is a full residue class modulo
\(3\), of size \(3^{k-3}\). It is **not** only sign.

### \(N_1\)

\[
N_1(p)-N_1(q)=(p-q)\bigl(3^{m+1}+3(p+q)\bigr),
\]

hence at \(m=k-2\)

\[
N_1(p)\equiv N_1(q)\pmod{3^k}
\iff
3^{k-1}\mid(p-q)(p+q+3^{k-2}).
\]

**EXACT — LEAN VERIFIED** (`inter_n1_iff`).

For sign pairs \(q=-p\), both \(N_2\) and \(N_1\) reduce to
\(3\mid p\). **EXACT — LEAN VERIFIED** (`inter_sign_n2_iff`,
`inter_sign_n1_iff`). Unit sign pairs \(\{\pm 1\}\) therefore
**cannot** collide at this layer: \(N_2\) already splits them.
**EXACT — LEAN VERIFIED** (`unit_sign_n2_splits`).

### \(N_0\)

The reconstruction identity of Milestone 21 gives

\[
p^3=\operatorname{bal}_{k-2}(p^3)+3^{k-2}D^{k-2}(p^3),
\]

so

\[
D^{k-2}(p^3)-D^{k-2}(q^3)
=
\frac{p^3-q^3-(\operatorname{bal}_{k-2}(p^3)-\operatorname{bal}_{k-2}(q^3))}{3^{k-2}}.
\]

\(N_0\) is **not** redundant once \(N_2\) and \(N_1\) agree.
The hierarchy through \(k=11\):

| \(k\) | \(N_2\) | \(N_2{+}N_1\) | full |
|------:|--------:|--------------:|-----:|
| 3 | 3 | 3 | 3 |
| 4 | 3 | 8 | 9 |
| 5 | 3 | 22 | 27 |
| 6 | 3 | 65 | 80 |
| 7 | 3 | 193 | 240 |
| 8 | 3 | 578 | 721 |
| 9 | 3 | 1732 | 2178 |
| 10 | 3 | 5195 | 6537 |
| 11 | 3 | 15583 | 19652 |

**REFUTED:** \(N_2{+}N_1\Rightarrow N_0\). \(N_0\) breaks remaining
sign pairs (those with \(3\mid p\) but \(3^k\nmid D^{k-2}(p^3)\))
and creates valuation conditions. It introduces no fibre type
beyond the five families already seen at the deepest layer,
except that twins are delayed (first at \(k=12\)).

---

## 4. Fibre types

Classified with the Milestone 21 labels, on \(P_{k-2}\):

| type | deepest \(m=k-1\) | intermediate \(m=k-2\) |
|------|-------------------|------------------------|
| singleton | majority | majority; all of \(P_{k-2}\) for \(k\le 5\) |
| sign pair | all units \(\pm u\) | only \(3\mid p\); units never pair |
| zero / valuation ball | \(3^{\lceil(2k-1)/3\rceil}\mid p\) | \(3^{\lceil(2k-2)/3\rceil}\mid p\) |
| translated high-val coset | present | present, typically refined |
| exceptional twin | \(\{720,738\}\) at \(k=8\) | first at \(k=12\): \(\pm\{19656,19710\}=3^9\pm 3^3\) |

**EXACT — HUMAN PROOF** (zero exponent: \(N_0\) of \(0\) forces
\(3^{2k-2}\mid p^3\), hence \(3^{\lceil(2k-2)/3\rceil}\mid p\);
sufficiency as in the deepest-layer cube argument with one fewer
digit). **COMPUTATIONALLY VERIFIED** for \(k\le 9\).

No new named type appears through \(k=12\). The deepest-layer
list is **not** assumed exhaustive; it simply remains adequate.

---

## 5. Counts \(C_{k,k-2}\)

Direct hashing of \(F_k(k-2,p)\), not automata minimization.

| \(k\) | raw \(3^{k-2}\) | \(C_{k,k-2}\) | \(C_{k-1,k-2}\) | \(\Delta_k\) |
|------:|----------------:|--------------:|----------------:|-------------:|
| 3 | 3 | 3 | 2 | 1 |
| 4 | 9 | 9 | 8 | 1 |
| 5 | 27 | 27 | 24 | 3 |
| 6 | 81 | 80 | 76 | 4 |
| 7 | 243 | 240 | 232 | 8 |
| 8 | 729 | 721 | 716 | 5 |
| 9 | 2187 | 2178 | 2153 | 25 |
| 10 | 6561 | 6537 | 6521 | 16 |
| 11 | 19683 | 19652 | 19597 | 55 |
| 12 | 59049 | 58977 | 58939 | 38 |
| 13 | 177147 | 177057 | 176908 | 149 |
| 14 | 531441 | 531230 | 531141 | 89 |

**COMPUTATIONALLY VERIFIED.** There is no single-term arithmetic
function \(F_2(k)\) with \(C_{k,k-2}=F_2(k)\). The exact
structural description is the fibre criterion of §2 together with
the horizon identity

\[
C_{k,k-2}=C_{k-1,k-2}+\Delta_k,
\]

where \(\Delta_k\) counts the extra Newton classes created by the
one-digit horizon lift (see §7). That is **not** a closed formula
for \(\Delta_k\).

**REFUTED:** \(C_{k,k-2}=C_{k-1,k-2}\).
**REFUTED:** \(C_{k,k-2}=3\,C_{k-1,k-3}\) (e.g. \(721\neq 3\cdot 240\)).

---

## 6. Difference from the deepest-layer mechanism

At \(m=k-1\), both leftover powers of \(3\) in \(N_2\) and the
linear term in \(N_1\) are multiples of \(3^k\). Fibres collapse
to

\[
p^2\equiv q^2\pmod{3^{k-1}}
\quad\text{and}\quad
D^{k-1}(p^3)\equiv D^{k-1}(q^3)\pmod{3^k}.
\]

At \(m=k-2\), one extra unresolved digit keeps

- \(N_2\equiv 2\cdot 3^{k-1}p\) alive, forcing \(p\equiv q\pmod{3}\);
- the linear term \(3^{k-1}p\) alive in \(N_1\), so the second
  factor is \(p+q+3^{k-2}\) rather than \(p+q\).

That is why the deepest-layer formula does not carry over
unchanged. Sign pairs of units, legal at \(m=k-1\), are illegal
here.

---

## 7. One-layer surplus and horizon lifting

Two liftings must be kept separate.

### A. Horizon lifting (\(k\to k+1\), depth \(m\) fixed)

On depth \(m=k-2\), the map \(\Phi_{k-1}\to\Phi_k\) **refines**
the previous deepest layer: Newton agreement modulo \(3^k\)
implies agreement modulo \(3^{k-1}\).

**EXACT — LEAN VERIFIED** (`inter_horizon_refines`).

The surplus

\[
\Delta_k=C_{k,k-2}-C_{k-1,k-2}
\]

is exactly the number of extra classes created by this
refinement. What splits:

- **Unit sign pairs always split** (\(N_2\): \(p\equiv -p\pmod{3}\)
  needs \(3\mid p\)). This is the primary source.
- Some twins split (e.g. \(\{720,738\}\) at the lift into \(k=9\)).
- Some high-valuation cosets refine into singletons or smaller
  cosets.
- The zero fibre may refine (size \(9\) at deepest \(k=8\) becomes
  three size-\(3\) classes at horizon \(k=9\), depth \(6\)).

**COMPUTATIONALLY VERIFIED** for \(k\le 9\) by explicit
`horizon_splits`. \(\Delta_k\) is **not** fitted.

**REFUTED:** \(N_2\) alone explains the surplus. \(N_2\) has only
three classes at every \(k\ge 3\); the surplus is created by
\(N_1\) and \(N_0\) acting on the previous deepest fibres after
\(N_2\) has already split the unit signs.

### B. Depth lifting (\(m\to m+1\), horizon \(k\) fixed)

This is a different operation. It is **not** the same as viewing
the previous deepest layer at a new horizon. In particular

\[
C_{k,k-2}\neq C_{k-1,k-2}
\]

already shows that “the \(m=k-2\) layer is the previous deepest
layer” is false.

A naive depth recurrence \(C_{k,m}=3\,C_{k-1,m-1}\) plus
corrections is **REFUTED** in the form
\(C_{k,k-2}=3\,C_{k-1,k-3}\).

---

## 8. Renormalization

The hoped-for scaling

\[
F_k(k-2,p)\;\longleftrightarrow\;F_{k'}(k'-1,u),
\qquad p=3^s u,
\]

does **not** hold as maps, even after adjusting \(k'\). The
obstruction is the surviving linear term \(3^{k-1}p\) in \(N_1\)
together with the nonzero \(N_2\). Those terms are identically
zero at the deepest layer and cannot be scaled away while
remaining inside a deepest-layer problem.

**REFUTED** as a literal identification of Newton images.
The weaker counting relation \(C_{k,k-2}=C_{k-1,k-2}\) is also
**REFUTED**.

What remains usable is the **depth-deficit** bookkeeping
\(r=k-1-m\):

- \(r=0\): \(N_2\) sees nothing;
- \(r=1\): \(N_2\) sees \(p\bmod 3\);
- \(r=2\): \(N_2\) would see \(p\bmod 9\) (not solved here).

This is a notation and a Newton-visibility pattern, not a
general solver.

---

## 9. Computational range

Direct \(F_k\) hashing, no automata minimizer.

- Fibre criterion vs \(F_k\): \(k\le 7\).
- Newton hierarchy \(N_2\) / \(N_2{+}N_1\) / full: \(k\le 11\).
- Exact \(C_{k,k-2}\) and \(\Delta_k\): \(k\le 14\).
- Horizon-split accounting: \(k\le 9\).
- Zero-fibre members: \(k\le 9\).
- Twins: first seen at \(k=12\).

CLI:

```text
btprime calculus cubic-layer --k <k> --depth-deficit 1
btprime calculus cubic-layer-fibre <p> --k <k> --depth-deficit 1
```

Only deficit \(1\) is implemented.

---

## 10. Lean inventory

File: `formal/BTCalculus/CubicIntermediateLayer.lean`. No `sorry`,
`admit`, or `axiom`.

| theorem | content |
|---------|---------|
| `inter_n3_zero` | \(N_3\equiv 0\) for \(k\ge 3\) |
| `inter_n2_mod` | \(N_2\equiv 2\cdot 3^{k-1}p\) |
| `inter_n2_iff` | \(N_2\) iff \(3\mid(p-q)\) |
| `inter_n1_mod` | \(N_1\equiv 3p^2+3^{k-1}p\) for \(k\ge 4\) |
| `inter_n1_iff` | \(N_1\) iff \(3^{k-1}\mid(p-q)(p+q+3^{k-2})\) |
| `inter_sign_n2_iff`, `inter_sign_n1_iff` | sign pairs: \(N_2\Leftrightarrow N_1\Leftrightarrow 3\mid p\) |
| `inter_equiv_iff` | complete fibre criterion |
| `inter_horizon_refines` | horizon \(k\) refines horizon \(k-1\) |
| `unit_sign_n2_splits` | \(\{\pm 1\}\) split |

No exact closed \(C_{k,k-2}\) is formalized.

---

## 11. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The
deficit-\(r\) Newton visibility, the horizon-lift surplus, and
the delayed twins are project-specific.

---

## 12. What this milestone does not claim

- No single-term closed \(C_{k,k-2}\) or \(M_k(x^3)\).
- No general depth-recursive formula
  \(C_{k,m}=3\,C_{k-1,m-1}+\text{corrections}\).
- No renormalization onto a deepest-layer problem.
- No work on \(x^4\), primes, Collatz, or a generic layer engine.

---

## 13. Strongest next question

Closed by Milestone 23. See [cubic_deficit_two.md](cubic_deficit_two.md).
The \(N_2\) visibility law is general; \(N_1\) is not the next trit.
