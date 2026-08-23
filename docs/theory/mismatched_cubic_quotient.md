# Mismatched-width cubic quotient

Master record for Milestone 26. After Milestone 25, the surviving
\(N_0\) term on \(p=3^ru\) is **not** a standard cubic residual.
This document studies the actual object

\[
Q_{t,K,W}(u)=D^t(u^3)\bmod 3^K,
\qquad u\in P_W.
\]

For the cubic residual problem in the exhausted regime,

\[
t=k-1-4r,\qquad K=k,\qquad W=k-1-2r=t+2r.
\]

The three parameters are not hidden. The point is specifically the
mismatch \(W>t\) and \(K>t+1\).

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_n0_reduction.md](cubic_n0_reduction.md),
[cubic_n1_valuation.md](cubic_n1_valuation.md).

---

## 1. Definition

**EXACT — LEAN VERIFIED** (`qCubic`, `qCubic_def`).

\[
Q_{t,K,W}(u)
=
D^t(u^3)\bmod 3^K,
\qquad
u\in P_W=\Bigl\{n\in\mathbb Z:\lvert n\rvert\le\tfrac{3^W-1}{2}\Bigr\}.
\]

The integer lift is \(qCubic(t,u)=D^t(u^3)\). The balanced low part is

\[
\operatorname{bal}_t(u^3)=\operatorname{packWord}(\operatorname{integerJet}_t(u^3)).
\]

This is not another residual machine: the legal prefix width is not
the \(D\)-depth, and the comparison modulus is not \(3^{t+1}\).

---

## 2. Two \(N_0\) regimes

Write \(m=k-1-r\) and \(p=3^ru\).

### Unexhausted

If \(m\le 3r\iff k\le 4r+1\), then
**EXACT — LEAN VERIFIED** (`q_from_unexhausted`):

\[
N_0=3^{4r-k+1}u^3.
\]

This is an ordinary scaled cubic congruence. The object \(Q\) is not
used.

### Exhausted

If \(m\ge 3r\iff k\ge 4r+1\), then
**EXACT — LEAN VERIFIED** (`q_from_exhausted`, `n0_scaled_exhausted`):

\[
N_0=D^{k-1-4r}(u^3)=Q_{t,k,W}(u).
\]

The boundary \(k=4r+1\) is included in both formulas and they agree:
\(t=0\) and \(N_0=u^3\). Concrete specializations
**EXACT — LEAN VERIFIED**:

| \(r\) | threshold | identity |
|---|---|---|
| \(1\) | \(k\ge 5\) | \(D^{k-2}(3u)=Q_{k-5,k,k-3}(u)\) (`q_of_deficit_one`) |
| \(2\) | \(k\ge 9\) | \(D^{k-3}(9u)=Q_{k-9,k,k-5}(u)\) (`q_of_deficit_two`) |
| \(3\) | \(k\ge 13\) | \(D^{k-4}(27u)=Q_{k-13,k,k-7}(u)\) (`q_of_deficit_three`) |

The width identity \(W=t+2r\) is **EXACT — LEAN VERIFIED**
(`cubic_q_width`).

---

## 3. Exact equality criterion

**EXACT — LEAN VERIFIED** (`q_recon`, `q_recon_diff`, `q_eq_iff`).

The reconstruction identity

\[
z=\operatorname{bal}_t(z)+3^t D^t(z)
\]

applied to \(z=u^3\) and \(z=v^3\) gives

\[
u^3-v^3-\bigl(\operatorname{bal}_t(u^3)-\operatorname{bal}_t(v^3)\bigr)
=
3^t\bigl(D^t(u^3)-D^t(v^3)\bigr).
\]

Therefore

\[
\boxed{
Q(u)=Q(v)
\iff
3^{t+K}\mid
\bigl(u^3-v^3-\Delta\mathrm{bal}_t(u,v)\bigr),
}
\]

where \(\Delta\mathrm{bal}_t(u,v)=\operatorname{bal}_t(u^3)-\operatorname{bal}_t(v^3)\).

Raw cube congruence \(u^3\equiv v^3\pmod{3^{t+K}}\) is **sufficient**
(`q_eq_of_cube_mod`) and **not necessary**.
**COMPUTATIONALLY VERIFIED**: already \((t,K)=(1,2)\) has pairs such as
\((-20,-13)\) with equal \(Q\) and unequal cubes modulo \(27\).

If the discarded digits agree, cube-mod becomes necessary as well.
**EXACT — LEAN VERIFIED** (`q_eq_iff_of_same_bal`):

\[
\operatorname{bal}_t(u^3)=\operatorname{bal}_t(v^3)
\Longrightarrow
\bigl(Q(u)=Q(v)\iff u^3\equiv v^3\pmod{3^{t+K}}\bigr).
\]

That is the exact interaction between the forgotten low \(t\) digits
and the quotient.

---

## 4. What \(D^t\) forgets

```text
u³
 │
 ├── low t balanced digits   bal_t(u³)
 │
 └── quotient                D^t(u³)  →  Q = that residue mod 3^K
```

The pair \((\operatorname{bal}_t(u^3),D^t(u^3))\) reconstructs \(u^3\)
exactly. \(Q\) keeps only the second coordinate modulo \(3^K\).
Equality of \(Q\) therefore permits a nonzero \(\Delta\mathrm{bal}\)
provided it is absorbed into \(u^3-v^3\) at precision \(t+K\).

This is the obstruction to a standard residual isomorphism: a matched
machine would compare \(D^t(u^3)\) modulo \(3^{t+1}\) on a domain of
width \(t\). Here the modulus is larger and the forgotten digits remain
arithmetically live.

---

## 5. Sharp input-precision bound

**EXACT — LEAN VERIFIED** (`q_visible_mod`, reused `n0_visible_mod`).

If \(s\ge 1\) and \(s\ge t+K-1\), then

\[
u\equiv v\pmod{3^s}
\Longrightarrow
Q(u)=Q(v).
\]

The bound \(s=\max(1,t+K-1)\) is sufficient for every \(u,v\in\mathbb Z\),
not only units. It is **not** a characterization:

- the converse fails as soon as discarded digits differ;
- on the cubic residual domain one has the exact identity
  \(t+K-1=2W\) (**EXACT — HUMAN PROOF**), so the sufficient congruence
  is stronger than \(u\equiv v\pmod{3^W}\), hence forces \(u=v\) on
  \(P_W\).

**REFUTED** as a global fibre law: \(Q(u)=Q(v)\) is not equivalent to
\(u\equiv v\pmod{3^s}\) for any fixed \(s\) independent of valuation.
Witnesses on \(P_W\) include the sign pair \(\{-1,1\}\) whenever
\(D^t(1)\equiv 0\pmod{3^K}\), and the unbalanced pairs
\((-13,-2)\) at \((t,K,W)=(1,6,3)\), \((-34,4)\) at \((2,7,4)\),
\((-89,71)\) at \((3,8,5)\).

Dependence on valuation is exact and different: see §7.

---

## 6. Unit stratum

Let \(3\nmid u\) and \(3\nmid v\). The only residues in
\((\mathbb Z/3\mathbb Z)^\times\) are \(\pm 1\), so either
\(u\equiv v\pmod 3\) or \(u\equiv -v\pmod 3\).

**EXACT — LEAN VERIFIED** (`cube_diff`, `three_dvd_sq_sum`,
`cube_val_succ`, `not_three_dvd_sq_sum_of_opp`).

\[
u^3-v^3=(u-v)(u^2+uv+v^2).
\]

- If \(u\equiv v\pmod 3\), then \(3\mid(u^2+uv+v^2)\), so
  \(v_3(u^3-v^3)\ge v_3(u-v)+1\).
- If \(u\equiv -v\pmod 3\) and \(3\nmid u\), then
  \(3\nmid(u^2+uv+v^2)\), so
  \(v_3(u^3-v^3)=v_3(u-v)\).

The usual LTE-style extra factor of \(3\) therefore holds on the
*same-residue* branch and **fails** on the opposite-residue branch.
That is why sign pairs and other opposite-residue pairs can collide
with much smaller \(u-v\).

Sign law, reused: \(Q(-u)=-Q(u)\), and
\(Q(u)=Q(-u)\) iff \(3^K\mid Q(u)\) (`q_neg`, `q_sign`).

**COMPUTATIONALLY VERIFIED** on every exhausted sample below: no two
distinct same-residue units share a \(Q\)-class. All observed unit
collisions mix the two residues \(\pm 1\). This is **not** promoted
to a theorem.

---

## 7. Valuation strata

Write \(u=3^sw\) with \(3\nmid w\).
**EXACT — LEAN VERIFIED** (`q_val_of_le`, `q_val_of_ge`):

\[
D^t(u^3)
=
\begin{cases}
3^{3s-t}w^3,& t\le 3s,\\
D^{t-3s}(w^3),& t\ge 3s.
\end{cases}
\]

The second threshold is \(3s=t\). Combined with the modulus:

- **unit stratum** \(s=0\): opposite-residue collisions as in §6;
- **low valuation** \(0<3s<t\): \(Q(u)=Q_{t-3s,K,W}(w)\), a
  shallower mismatched quotient of the unit \(w\);
- **threshold** \(3s=t\): \(Q(u)=w^3\bmod 3^K\);
- **high valuation** \(3s\ge t\): \(Q(u)=3^{3s-t}w^3\bmod 3^K\),
  and if \(K\le 3s-t\) then \(Q(u)=0\)
  (`q_zero_of_high`).

The zero class therefore collects every sufficiently divisible
prefix together with those units whose cube quotient vanishes
modulo \(3^K\). **COMPUTATIONALLY VERIFIED** at
\((t,K,W)=(2,7,4)\): one five-point class mixes valuations
\(\{0,3,\infty\}\).

Collision mechanisms differ by stratum. There is no single residue
modulus that describes all of them.

---

## 8. Width excess \(W-t=2r\)

The extra \(2r\) input trits are **not** invisible.

**EXACT — LEAN VERIFIED** (`cube_expand`, `q_shift`, `q_split_high`).
If \(t\le s+1\) and \(t\le 3s\),

\[
D^t\bigl((a+3^sx)^3\bigr)
=
D^t(a^3)+3^{s+1-t}a^2x+3^{2s+1-t}ax^2+3^{3s-t}x^3.
\]

At the high-trit split \(s=t\), \(u=a+3^tb\),

\[
D^t(u^3)=D^t(a^3)+3a^2b+3^{t+1}ab^2+3^{2t}b^3.
\]

For a unit \(a\) the leading carry is \(3a^2b\), valuation exactly
\(1\). On every exhausted cubic instance \(K=k\ge 4r+1\ge 5\), this
term survives modulo \(3^K\). **COMPUTATIONALLY VERIFIED**:
\(D^2((1+9b)^3)-D^2(1^3)\) equals \(-57,0,111\) for \(b=-1,0,1\).

So the extra width is encoded through cubic carry, not discarded.
That is also why \(N_1\) and \(N_0\) cannot share the reduced
horizon \(k-2r\): \(N_0\) keeps modulus \(3^k\) and continues to
read \(2r\) trits past its \(D\)-depth.

Effective input precision depends on valuation: high-valuation
inputs collapse as in §7; units feel the full carry.

---

## 9. Visibility law for \(Q\)

The \(N_2\) law was \(r\) unresolved \(\Rightarrow p\bmod 3^r\).
The strongest exact analogue for \(Q\) is **not** a residue
visibility theorem.

**EXACT — LEAN VERIFIED** invariant:

\[
Q(u)=Q(v)
\iff
3^{t+K}\mid\bigl(u^3-v^3-\Delta\mathrm{bal}_t(u,v)\bigr).
\]

**REFUTED**: no fixed residue modulus \(\Psi(u)=u\bmod 3^s\) classifies
the fibres, even after restricting to units. The discarded low-\(t\)
cubic digits interact essentially with the quotient.

**COMPUTATIONALLY VERIFIED** intermediate shape: on the scanned
exhausted samples, unit fibres are either singletons or mix the two
unit residues. Valuation strata have their own collapsing law into
the zero class.

This is a successful negative visibility theorem, in the sense of
Milestone 26: the obstruction is identified and exact.

---

## 10. Concrete cubic parameters

Only exhausted cases \(t\ge 0\). Direct enumeration on \(P_W\).

| \(r\) | \(k\) | \(t\) | \(K\) | \(W\) | \(\lvert P_W\rvert\) | \(\lvert\mathrm{im}\,Q\rvert\) | unit classes | max fibre | extras |
|---|---|---|---|---|---|---|---|---|---|
| \(1\) | \(5\) | \(0\) | \(5\) | \(2\) | \(9\) | \(9\) | \(6\) | \(1\) | \(0\) |
| \(1\) | \(6\) | \(1\) | \(6\) | \(3\) | \(27\) | \(23\) | \(15\) | \(3\) | \(3\) |
| \(1\) | \(7\) | \(2\) | \(7\) | \(4\) | \(81\) | \(75\) | \(51\) | \(5\) | \(3\) |
| \(1\) | \(8\) | \(3\) | \(8\) | \(5\) | \(243\) | \(229\) | \(157\) | \(7\) | \(8\) |
| \(2\) | \(9\) | \(0\) | \(9\) | \(4\) | \(81\) | \(79\) | \(54\) | \(3\) | \(0\) |
| \(2\) | \(10\) | \(1\) | \(10\) | \(5\) | \(243\) | \(231\) | \(159\) | \(5\) | \(3\) |
| \(3\) | \(13\) | \(0\) | \(13\) | \(6\) | \(729\) | \(723\) | \(486\) | \(3\) | \(0\) |

**COMPUTATIONALLY VERIFIED**.

Compare \((t,K,W)=(1,6,3)\) with \((1,10,5)\): same depth, different
modulus and width. Image sizes \(23\) versus \(231\). So \(r\) does
not act only through \(W-t=2r\); \(K-t=4r+1\) matters independently.

When \(t=0\), \(Q(u)=u^3\bmod 3^K\). Units are injective on these
samples; the only merges are high-valuation cube-zero classes.

---

## 11. Existing \(N_0\) examples in \(Q\)-language

### \((r,k)=(2,9)\)

Then \(t=0\), \(K=9\), \(W=4\), so \(Q(u)=u^3\bmod 3^9\) on \(P_4\).
**EXACT — HUMAN PROOF** plus **COMPUTATIONALLY VERIFIED**.

The nine-point \(N_2{+}N_1\) fibre of \(0\) is
\(\{-324,-243,\ldots,324\}=27\cdot P_4^{(9)}\) in the sense of
Milestone 24. After \(N_0\),

\[
\{u\in P_4:u^3\equiv 0\pmod{3^9}\}=\{-27,0,27\},
\]

because \(27^3=3^9\). Scaling back by \(3^r=9\) recovers the known
full Newton fibre \(\{-243,0,243\}\). The new language does not
change the example; it names the map that cut the fibre.

### \((r,k)=(3,9)\)

Here \(k=9<13=4r+1\), so the case is **unexhausted**:
\(N_0=3^{4}u^3=81u^3\), not a \(Q\)-instance.
The four surviving \(N_2{+}N_1\) fibres
\(\{\pm 27\}\), \(\{\pm 54\}\), \(\{\pm 108\}\), \(\{-81,0,81\}\)
are separated by this scaled cube, because the values
\(\pm 81,\pm 648,\pm 5184,\pm 2187,0\) are distinct modulo \(3^9\).
**COMPUTATIONALLY VERIFIED**. This confirms the regime split of §2
rather than the exhausted \(Q\)-calculus.

---

## 12. Internal recursion

**EXACT — LEAN VERIFIED** (`q_shift`). The identity of §8 is the
mismatched-width substitute for \(D(f(a+3x))\). It expands
\(D^t((a+3^sx)^3)\) into an explicit cubic polynomial in the high
digits plus the lower-depth value \(D^t(a^3)\). It is **not** a
standard residual section.

No further closed recursion is claimed.

---

## 13. Finite-state exploration

Not a theorem. LSD-first Myhill–Nerode class counts of
\(u\mapsto Q(u)\) on \(P_W\):

| \((t,K,W)\) | prefix-length counts | \(\lvert\mathrm{im}\,Q\rvert\) | naive \(3^j\) |
|---|---|---|---|
| \((0,5,2)\) | \(1,3,9\) | \(9\) | \(1,3,9\) |
| \((1,6,3)\) | \(1,3,9,24\) | \(23\) | \(1,3,9,27\) |
| \((2,7,4)\) | \(1,3,9,27,78\) | \(75\) | \(1,3,9,27,81\) |
| \((0,9,4)\) | \(1,3,9,27,80\) | \(79\) | \(1,3,9,27,81\) |
| \((1,3,4)\) | \(1,3,9,16,18\) | \(9\) | \(1,3,9,27,81\) |

When the visibility bound is smaller than the width, as in the last
row, the state count compresses after that bound. On actual cubic
parameters the bound is \(2W\), so the transducer tracks almost the
full prefix. No compact-FST claim is made.

---

## 14. CLI

```
btprime calculus cubic-quotient --t <t> --modulus <k> --width <W>
btprime calculus cubic-quotient-fibre <u> --t <t> --modulus <k> --width <W>
btprime calculus compare-cubic-quotient <u> <v> [<w> ...] --t <t> --modulus <k>
```

Existing `n0-reduction` / `n1-strata` / `cubic-layer` commands are
unchanged.

---

## 15. Lean inventory

`formal/BTCalculus/MismatchedCubicQuotient.lean`, no `sorry`.

| theorem | content |
|---|---|
| `qCubic`, `balCubic` | definition |
| `q_recon`, `q_recon_diff`, `q_eq_iff` | reconstruction criterion |
| `q_eq_of_cube_mod`, `q_eq_iff_of_same_bal` | cube-mod vs discarded digits |
| `q_visible_mod` | sufficient input precision |
| `q_val_of_le`, `q_val_of_ge`, `q_zero_of_high` | valuation strata |
| `q_from_exhausted`, `q_from_unexhausted` | two \(N_0\) regimes |
| `q_of_deficit_one`, `q_of_deficit_two`, `q_of_deficit_three` | \(r=1,2,3\) |
| `cube_diff`, `not_three_dvd_sq_sum_of_opp` | unit branches |
| `q_neg`, `q_sign` | sign |
| `cube_expand`, `q_shift`, `q_split_high` | mismatched recursion |
| `cubic_q_width` | \(W=t+2r\) |

---

## 16. Computational range

Direct arithmetic on every prefix of \(P_W\), no automata.

- Reconstruction iff-check for \(0\le t<4\), \(1\le K<5\),
  \(\lvert u\rvert,\lvert v\rvert\le 20\).
- Two-regime formula on \(\lvert u\rvert\le 30\), \(t<6\).
- High-trit expansion on \(\lvert a\rvert\le 6\), \(\lvert b\rvert\le 4\),
  \(t<4\).
- Exhausted image tables: \(r=1\) and \(k\le 8\); \(r=2\) and
  \(k\le 10\); \(r=3\) and \(k=13\).
- Reinterpretation of \((2,9)\) and \((3,9)\).

---

## 17. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The
mismatched-width quotient and the reconstruction criterion are
project-specific.

---

## 18. What this milestone does not claim

- \(Q\) is not a standard residual machine.
- No smaller-\(k\) isomorphism.
- No global converse \(Q(u)=Q(v)\Rightarrow u\equiv v\pmod{3^{t+K-1}}\).
- No closed \(M_k(x^3)\).
- No \(x^4\), no generic \(p\)-adic quotient library, no FST theorem.

---

## 19. Strongest project-specific theorem

The independent \(N_0\) core is the mismatched-width cubic quotient
\(Q_{t,K,W}\), with exact fibre relation

\[
Q(u)=Q(v)
\iff
3^{t+K}\mid\bigl(u^3-v^3-\Delta\mathrm{bal}_t(u,v)\bigr)
\]

and exact two-regime / valuation / high-trit calculus. On the cubic
domain the extra \(2r\) trits remain visible through the carry
\(3a^2b\). No residue/valuation invariant replaces the discarded
low-\(t\) cubic digits.

The cubic tower is now

\[
N_2=\text{visibility }p\bmod 3^r
\;\longrightarrow\;
N_1=\text{valuation filter }3^r\mid p
\;\longrightarrow\;
Q=\text{mismatched cubic quotient}.
\]

---

## 20. Strongest next question

After the exact reconstruction law, is there a small explicit
invariant \(\Psi_{t,K,W}\) (valuation, residue, sign, and a bounded
function of \(\operatorname{bal}_t(u^3)\)) that classifies
\(Q\)-fibres, or is the discarded low-\(t\) cubic jet an essential
obstruction to any residue-scale \(\Psi\)?

Do not start that work automatically.
