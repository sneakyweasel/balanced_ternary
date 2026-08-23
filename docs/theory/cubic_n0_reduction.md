# N0 on the \(3^r\)-divisible locus

Master record for Milestone 25. After Milestone 24, every nontrivial
\(N_2{+}N_1\) fibre lies in \(3^r\mathbb Z\). Write \(p=3^ru\) and
\(m=k-1-r\). This document determines the exact value of

\[
N_0=D^m(p^3)=D^m(3^{3r}u^3)
\]

and whether that remaining problem is a smaller standard cubic residual.

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_n1_valuation.md](cubic_n1_valuation.md),
[cubic_deficit_two.md](cubic_deficit_two.md),
[cubic_deepest_layer.md](cubic_deepest_layer.md).

---

## 1. Exact scaling theorem

**EXACT — LEAN VERIFIED** (`DZ_mul_three`, `iterDZ_pow_mul`,
`iterDZ_pow_mul_ge`, `n0_scaled_of_le`, `n0_scaled_of_ge`).

The identity \(D(3n)=n\) iterates: for \(j\le e\),

\[
D^j(3^e n)=3^{e-j}n,
\]

and for \(e\le j\),

\[
D^j(3^e n)=D^{j-e}(n).
\]

With \(p^3=3^{3r}u^3\),

\[
D^m((3^ru)^3)
=
\begin{cases}
3^{3r-m}u^3,& m\le 3r,\\
D^{m-3r}(u^3),& m\ge 3r.
\end{cases}
\]

The two formulas agree on the boundary \(m=3r\). This is an equality
of integers, not merely a congruence modulo \(3^k\).

---

## 2. Regime \(m\le 3r\)

Equivalent to \(k\le 4r+1\) whenever \(r+1\le k\).
**EXACT — LEAN VERIFIED** (`deficit_unexhausted_iff`,
`n0_scaled_unexhausted`).

\[
N_0=3^{4r-k+1}u^3.
\]

No further \(D\) remains. Agreement of \(N_0\) is the cubic congruence

\[
u^3\equiv v^3\pmod{3^{2k-1-4r}}.
\]

---

## 3. Regime \(m\ge 3r\)

Equivalent to \(k\ge 4r+1\). **EXACT — LEAN VERIFIED**
(`n0_scaled_exhausted`).

\[
N_0=D^{k-1-4r}(u^3).
\]

---

## 4. Reduced depth

**EXACT — LEAN VERIFIED** (`n0_reduced_depth`).

\[
t=m-3r=k-1-4r.
\]

The domain of \(u\) is the balanced interval \(P_{m-r}=P_{k-1-2r}\):
if \(|3^ru|\le(3^m-1)/2\), then \(|u|\le(3^{m-r}-1)/2\).
**EXACT — HUMAN PROOF**.

The comparison modulus remains \(3^k\). Define

\[
Q_{r,k}(u)=D^t(u^3)\bmod 3^k
\qquad\text{on}\qquad u\in P_{k-1-2r},
\]

only when \(k\ge 4r+1\). This is the stripped \(N_0\) map. It is
**not** automatically a standard residual coordinate.

---

## 5. Sign pairs

**EXACT — LEAN VERIFIED** (`n0_sign_survives`, reused `sign_n0`,
`iterDZ_neg`).

\[
D^m((-p)^3)=-D^m(p^3),
\]

so

\[
N_0(p)\equiv N_0(-p)\pmod{3^k}
\iff
3^k\mid N_0(p).
\]

Combined with Milestone 24, a sign pair survives the full Newton
invariant if and only if \(3^r\mid p\) and \(D^m(p^3)\equiv 0\pmod{3^k}\).
In the unexhausted regime this is \(3^k\mid 3^{3r-m}u^3\).

---

## 6. Valuation stratification

Write \(p=3^sw\) with \(3\nmid w\). Milestone 24 already forces
\(s\ge r\) on every nontrivial \(N_2{+}N_1\) fibre.

**EXACT — LEAN VERIFIED** (`n0_val_stratum_le`, `n0_val_stratum_ge`):

\[
D^m(p^3)
=
\begin{cases}
3^{3s-m}w^3,& m\le 3s,\\
D^{m-3s}(w^3),& m\ge 3s.
\end{cases}
\]

The second threshold is real:

| layer | threshold |
|---|---|
| \(N_2{+}N_1\) | \(v_3(p)=r\) |
| \(N_0\) | \(3\,v_3(p)=m\) |

| \(r\) | \(s\) | \(m-3s\) | \(N_0\) regime |
|---|---|---|---|
| \(1\) | \(1\) | \(k-2-3\) | exhausted iff \(k\ge 6\) |
| \(2\) | \(2\) | \(k-3-6\) | exhausted iff \(k\ge 10\) |
| \(r\) | \(s\ge r\) | \(k-1-r-3s\) | exhausted iff \(k\ge 3s+r+1\) |

---

## 7. No standard smaller residual

**REFUTED** as an exact residual isomorphism (outcome C for a
standard instance; outcome B for the raw \(D\)-process).

A standard cubic residual \(N_0\) at parameters \((k',m')\) is
\(D^{m'}(x^3)\bmod 3^{k'}\) on the domain \(P_{m'}\).

The stripped map has

- domain \(P_{k-1-2r}\),
- depth \(t=k-1-4r\),
- modulus \(3^k\).

These match a standard instance if and only if \(m'=k-1-2r=t=k-1-4r\)
and \(k'=k\), hence \(r=0\).

**EXACT — LEAN VERIFIED** (`n0_width_ne_depth`): for \(r\ge 1\) and
\(k\ge 4r+1\),

\[
k-1-2r\neq k-1-4r.
\]

The prefix is \(2r\) trits wider than the remaining depth.

---

## 8. Exact obstruction

Three independent mismatches prevent a standard recursion.

1. **Width versus depth.** Domain width \(k-1-2r\), remaining depth
   \(k-1-4r\). The residual depth/horizon relation is not the
   original deficit \(r\); it would be deficit \(4r\) at horizon
   \(k\), but then the legal prefix width would be \(k-1-4r\).

2. **Modulus stays \(3^k\).** A reduced horizon \(k'<k\) would
   compare \(N_0\) modulo a strictly smaller power of \(3\).

3. **Mismatch with the Milestone 24 \(N_1\) reduction.** \(N_1\) on
   \(p=3^ru\) reduces to deepest-layer \(N_1\) at horizon \(k-2r\)
   when \(k\ge 2r+2\). That deepest \(N_0\) would be
   \(D^{k-2r-1}(u^3)\bmod 3^{k-2r}\). **EXACT — LEAN VERIFIED**
   (`n0_depth_eq_n1_deepest`): for \(k\ge 4r+1\),

   \[
   k-1-4r=k-2r-1\iff r=0.
   \]

   So \(N_1\) and \(N_0\) do **not** reduce to the same smaller
   object. **COMPUTATIONALLY VERIFIED**: at \((r,k)=(1,8)\),
   \(D^3(u^3)\bmod 3^8\) is not the deepest \(N_0\) at horizon \(6\).

The raw \(D\)-process on \(u^3\) **is** the same operator
(partial recursion of the iteration). The residual *machine*
(domain, depth, deficit, modulus) does not close.

Naive claims that were checked and **REFUTED**:

- \(N_0(3^ru)\) at \((k,m)\) equals deepest \(N_0(u)\) at horizon
  \(k-2r\);
- the stripped map is the standard residual \(N_0\) at
  \((k,t)\);
- \(N_1\) and \(N_0\) share one reduced cubic instance.

---

## 9. Precision of \(N_0\)

**EXACT — LEAN VERIFIED** (`n0_of_cube_mod`, `cube_val_succ`,
`n0_visible_mod`).

\(D^t(u^3)\bmod 3^k\) depends on \(u^3\bmod 3^{t+k}\). If
\(1\le s\) and \(t+k-1\le s\), then

\[
u\equiv v\pmod{3^s}
\Longrightarrow
D^t(u^3)\equiv D^t(v^3)\pmod{3^k}.
\]

The sufficient bound is \(s=\max(1,t+k-1)\). It is sharp for units:
already \((t,k)=(1,2)\) fails at \(s=t+k-2\).
**COMPUTATIONALLY VERIFIED**.

On the actual domain \(P_{k-1-2r}\) this bound is typically larger
than the width, so \(N_0\) can see the whole of \(u\). That is the
\(N_0\) analogue of visibility, and it is the opposite of the
\(N_2\) law: \(N_2\) exposes a short residue, \(N_0\) does not.

---

## 10. Zero fibre

**EXACT — LEAN VERIFIED** (`n0_scaled_zero`). For \(u=0\),
\(N_0=0\) in both regimes. The existing deepest-layer zero-fibre
theorem remains the special case \(r=0\). No new zero-ball formula
is claimed.

---

## 11. Computational validation

Direct arithmetic, no automata. The two-regime formula matches
iterated \(D\) for \(r=0,\ldots,4\) and \(k\le r+9\) on every legal
\(u\). Sign-pair survival matches \(3^k\mid N_0(p)\). The
\(N_1\)-horizon candidate is already distinct at \((1,8)\). At
\((r,k)=(2,9)\) the \(N_2{+}N_1\) fibre of \(0\) is nine points;
\(N_0\) cuts it to \(\{-243,0,243\}\).

---

## 12. CLI

```
btprime calculus n0-reduction --k <k> --deficit <r>
btprime calculus n0-fibre <p> --k <k> --deficit <r>
```

This is not a generic reducer. Existing `n1-strata` / `cubic-layer`
commands are unchanged.

---

## 13. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The
two-regime stripping law and the width/depth obstruction are
project-specific.

---

## 14. What this milestone does not claim

- No formula for \(M_k(x^3)\).
- No claim that the cubic fibre problem is recursively solved.
- No identification of \(Q_{r,k}\) with a deepest-layer instance.
- No \(x^4\), primes, Collatz, or hardware.

---

## 15. Strongest next question

The remaining same-depth problem on the locus is the pair
\((N_1^\mathrm{scaled},N_0^\mathrm{stripped})\) on \(u\in P_{k-1-2r}\).
Is there a useful calculus of that pair as a *cubic quotient of
mismatched width*, or must \(N_0\) be treated as an independent
\(D^t(u^3)\bmod 3^k\) constraint?

Do not start that work automatically.
