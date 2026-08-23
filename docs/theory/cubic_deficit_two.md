# Depth-deficit 2 and the first visibility theorem

Master record for Milestone 23. Residual depth is written as a
**depth deficit**

\[
r=k-1-m.
\]

This document treats \(r=2\) (\(m=k-3\)) and proves that the
\(N_2\) visibility pattern

\[
r=0:\text{ nothing},\qquad
r=1:p\bmod 3,\qquad
r=2:p\bmod 9
\]

is a theorem, in fact the \(r=2\) case of a general law. It does
**not** give a single-term formula for \(C_{k,k-3}\) or \(M_k(x^3)\).

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Related: [cubic_intermediate_layer.md](cubic_intermediate_layer.md),
[cubic_deepest_layer.md](cubic_deepest_layer.md),
[cubic_residual_fibres.md](cubic_residual_fibres.md).

---

## 1. Exact \(r=2\) Newton formulas

Set \(m=k-3\). Then

\[
\begin{aligned}
N_3&=2\cdot 3^{2k-5},\\
N_2&=2\cdot 3^{k-2}p+2\cdot 3^{2k-5},\\
N_1&=3^{2k-6}+3^{k-2}p+3p^2,\\
N_0&=D^{k-3}(p^3).
\end{aligned}
\]

| coordinate | surviving form | range | information |
|---|---|---|---|
| \(N_3\) | \(0\) | \(k\ge 5\) | depth only |
| \(N_2\) | \(2\cdot 3^{k-2}p\) | \(k\ge 5\) | \(p\bmod 9\) |
| \(N_1\) | \(3p^2+3^{k-2}p\) | \(k\ge 6\) | quadratic refinement |
| \(N_0\) | \(D^{k-3}(p^3)\) | all \(k\ge 3\) | cubic quotient |

For \(k=3,4\) the extra powers \(3^{2k-5}\) do **not** vanish;
the difference \(N_2(p)-N_2(q)\) is still exact.

**EXACT — LEAN VERIFIED** (`deficitTwo_n3_zero`, `deficitTwo_n2_mod`,
`deficitTwo_n1_mod`).

---

## 2. \(N_2\) visibility theorem

**EXACT — LEAN VERIFIED** (`depthDeficit_two_N2_visibility`).
For \(k\ge 3\),

\[
N_2(p)\equiv N_2(q)\pmod{3^k}
\iff
p\equiv q\pmod{9}.
\]

This is the first named theorem of the milestone. The valid range
is exactly \(k\ge 3\) (so that \(m=k-3\ge 0\)). The simplified
representative \(N_2\equiv 2\cdot 3^{k-2}p\) needs \(k\ge 5\).

On \(P_{k-3}\) the number of \(N_2\) classes is
\(\min(9,3^{k-3})\): \(1,3,9,9,\ldots\). Exactly **9** classes
for every \(k\ge 5\). **COMPUTATIONALLY VERIFIED** through
\(k=14\).

---

## 3. \(N_1\) refinement

\[
N_1(p)-N_1(q)=3(p-q)(p+q+3^{k-3}),
\]

so

\[
N_1(p)\equiv N_1(q)\pmod{3^k}
\iff
3^{k-1}\mid(p-q)(p+q+3^{k-3}).
\]

**EXACT — LEAN VERIFIED** (`deficitTwo_n1_iff`).

After \(N_2\), write \(p-q=9\delta\). Then \(N_1\) becomes

\[
3^{k-3}\mid\delta\bigl(p+q+3^{k-3}\bigr).
\]

**EXACT — LEAN VERIFIED** (`deficitTwo_n1_after_n2`).

This is **not** “the next trit of \(p\)”.

- If \(3\nmid p\) (unit residue mod \(9\)), then
  \(3\nmid(p+q+3^{k-3})\) for \(k\ge 4\), so \(3^{k-3}\mid\delta\),
  hence \(3^{k-1}\mid(p-q)\). On \(P_{k-3}\) this forces \(p=q\).
  **EXACT — HUMAN PROOF**; **COMPUTATIONALLY VERIFIED** for
  \(6\le k\le 9\).
- If \(3\mid p\), the second factor may carry valuation and \(N_1\)
  is a quadratic / sign condition on the remaining residue.

**REFUTED:** after \(N_2\) has shown two trits, \(N_1\) reveals
exactly the next trit.

Sign pairs: \(N_2(p)\equiv N_2(-p)\) iff \(9\mid p\).
**EXACT — LEAN VERIFIED** (`deficitTwo_sign_n2_iff`).
At \(r=1\) the same test was only \(3\mid p\).

---

## 4. \(N_0\) refinement

\[
3^k\mid D^{k-3}(p^3)-D^{k-3}(q^3).
\]

The reconstruction identity still writes this as a cubic quotient
modulo balanced residues of width \(k-3\). After \(N_2\) and \(N_1\)
agree, \(N_0\) remains independent:

**REFUTED:** \(N_2{+}N_1\Rightarrow N_0\) (\(\Delta^{(0)}_k>0\) for
all \(k\ge 6\)).

It behaves like a lower-precision cubic quotient on the
high-valuation classes that \(N_1\) did not already kill. It is
**not** a deepest-layer problem at a smaller horizon: the leftover
linear \(N_1\) term and the mod-\(9\) filter have no deepest-layer
analogue.

Zero fibre: \(3^{\lceil(2k-3)/3\rceil}\mid p\).
**EXACT — HUMAN PROOF** (same cube-divisibility as Milestone 21
with two fewer digits). Matches \(\{-243,0,243\}\) at \(k=9\),
and the size-\(9\) ball at \(k=12\).

---

## 5. Complete same-depth fibre criterion

**EXACT — LEAN VERIFIED** (`deficitTwo_equiv_iff`).

\[
F_k(k-3,p)=F_k(k-3,q)
\iff
\mathcal C_{k,2}(p,q),
\]

where

\[
\begin{aligned}
\mathcal C_{k,2}(p,q)
:\Longleftrightarrow
&\ p\equiv q\pmod{9}\\
&\land\ 3^{k-1}\mid(p-q)(p+q+3^{k-3})\\
&\land\ 3^k\mid D^{k-3}(p^3)-D^{k-3}(q^3).
\end{aligned}
\]

Hierarchy: residue modulo \(9\), then quadratic refinement, then
cubic quotient. Exact as a residue-prefix normal form.

---

## 6. Class counts

Direct \(F_k\) hashing, no automata.

| \(k\) | raw | \(N_2\) | \(N_2{+}N_1\) | full \(C_{k,k-3}\) | \(\Delta^{(1)}\) | \(\Delta^{(0)}\) | \(\Delta_k^{(r=2)}\) |
|------:|----:|--------:|--------------:|-------------------:|-----------------:|-----------------:|---------------------:|
| 5 | 9 | 9 | 9 | 9 | 0 | 0 | 0 |
| 6 | 27 | 9 | 26 | 27 | 17 | 1 | 0 |
| 7 | 81 | 9 | 76 | 81 | 67 | 5 | 1 |
| 8 | 243 | 9 | 227 | 243 | 218 | 16 | 3 |
| 9 | 729 | 9 | 679 | 727 | 670 | 48 | 6 |
| 10 | 2187 | 9 | 2036 | 2180 | 2027 | 144 | 2 |
| 11 | 6561 | 9 | 6106 | 6554 | 6097 | 448 | 17 |
| 12 | 19683 | 9 | 18317 | 19661 | 18308 | 1344 | 9 |
| 13 | 59049 | 9 | 54949 | 59022 | 54940 | 4073 | 45 |
| 14 | 177147 | 9 | 164846 | 177083 | 164837 | 12237 | 26 |

**COMPUTATIONALLY VERIFIED.** \(N_1\) consistently dominates the
post-\(N_2\) refinement. \(N_0\) still adds a growing correction.
No formulas are fitted.

The layer is uncompressed for \(k\le 8\), even though the shallow
\(N_2\)-injection theorem only covers \(k\le 5\). First collisions
at \(k=9\).

No single-term \(C_{k,k-3}\). Structural identity:

\[
C_{k,k-3}=C_{k-1,k-3}+\Delta_k^{(r=2)},
\]

and \(C_{k-1,k-3}=C_{k-1,(k-1)-2}\) is the previous \(r=1\) count
at the same depth.

---

## 7. Fibre types

Through \(k=12\), the Milestone 21/22 labels remain adequate. No
new named type.

| \(k\) | non-singletons |
|------:|---|
| \(\le 8\) | none |
| 9 | zero-coset \(\{-243,0,243\}\) |
| 10–11 | \(\{\pm 9\}\) sign; zero-coset; two translated cosets |
| 12 | signs \(\{\pm 9\},\{\pm 18\}\); six translated cosets; 9-element zero ball |

Twins, present at \(r=1\) from \(k=12\), do **not** appear at
\(r=2\) through \(k=12\).

---

## 8. Horizon lifting

Fixed depth \(m=k-3\): horizon \(k-1\) has deficit \(r=1\), horizon
\(k\) has deficit \(r=2\). So

\[
\Phi_{k-1}\to\Phi_k
\]

is the lift \(r=1\to r=2\) at that depth. It refines.
**EXACT — LEAN VERIFIED** (`deficitTwo_horizon_refines`).

Splits are **not** explained by \(N_2\) alone, but the primary
visible splits are sign pairs that satisfied \(3\mid p\) and fail
\(9\mid p\) (e.g. \(\{\pm 3\}\) at \(k=7,8,9,10\); \(\{\pm 6\}\) at
\(k=9,10\)). High-valuation cosets also refine.

\(\Delta_k^{(r=2)}\) is that surplus. Do not fit it.

---

## 9. Comparison \(r=0,1,2\)

| quantity | \(r=0\) | \(r=1\) | \(r=2\) |
|---|---:|---:|---:|
| depth | \(k-1\) | \(k-2\) | \(k-3\) |
| \(N_2\) precision | none | mod \(3\) | mod \(9\) |
| \(N_2\) classes | 1 | 3 | 9 (\(k\ge 5\)) |
| unit sign pairs | possible | forbidden | forbidden |
| sign pairs allowed | any unit | \(3\mid p\) | \(9\mid p\) |
| main \(N_1\) role | \(p^2\) congruence | first correction after mod \(3\) | singletons on unit residues; quadratic on \(3\mid p\) |
| \(N_0\) role | independent | independent | independent |
| first collision | \(k=2\) | \(k=6\) | \(k=9\) |
| new fibre type | twins at \(k=8\) | twins at \(k=12\) | none through \(k=12\) |

**EXACT — LEAN VERIFIED** for the three \(N_2\) rows
(`depthDeficit_zero_N2`, `depthDeficit_one_N2`,
`depthDeficit_two_N2_visibility`). Remaining rows
**COMPUTATIONALLY VERIFIED** / **EXACT — HUMAN PROOF**.

Increasing \(r\) does **not** merely reveal another digit of the
whole Newton tower. \(N_2\) is digit-revealing; \(N_1\) and \(N_0\)
change role with \(r\).

---

## 10. The general depth-deficit law

The same derivation as \(r=2\) is `sameDepth_n2_succ` at
\(m=k-1-r\). For \(r+1\le k\),

\[
N_2(p)\equiv N_2(q)\pmod{3^k}
\iff
p\equiv q\pmod{3^r}.
\]

**EXACT — LEAN VERIFIED** (`depthDeficit_n2_visibility`).

This is the first real **depth-deficit visibility law**. It is
only a law for \(N_2\). The extra term \(2\cdot 3^{2k-1-2r}\) in
\(N_2\) vanishes for \(k\ge 2r+1\), which recovers the simplified
representatives used at \(r=0,1,2\).

A general fibre criterion, a general \(C_{k,k-1-r}\), and a
generic deficit solver are **not** claimed.

---

## 11. Lean inventory

File: `formal/BTCalculus/CubicDeficitTwo.lean`. No `sorry`,
`admit`, or `axiom`.

| theorem | content |
|---------|---------|
| `depthDeficit_n2_visibility` | general \(N_2\) law at deficit \(r\) |
| `depthDeficit_zero_N2` / `one_N2` / `two_N2_visibility` | \(r=0,1,2\) |
| `deficitTwo_n3_zero`, `n2_mod`, `n1_mod` | Newton simplification |
| `deficitTwo_n1_iff`, `n1_after_n2` | \(N_1\) refinement |
| `deficitTwo_equiv_iff` | complete fibre criterion |
| `deficitTwo_sign_n2_iff` | signs iff \(9\mid p\) |
| `deficitTwo_horizon_refines` | horizon lift refines |

---

## 12. Computational range

Direct hashing through \(k=14\). Fibre criterion vs \(F_k\) through
\(k=8\). Horizon splits through \(k=10\). Fibre types through
\(k=12\). General visibility checked for \(r\le 3\) on small
horizons.

CLI:

```text
btprime calculus cubic-layer --k <k> --depth-deficit 2
btprime calculus cubic-layer-fibre <p> --k <k> --depth-deficit 2
```

Only deficits \(1\) and \(2\) are implemented.

---

## 13. Literature

Still **REPARAMETERIZATION** of the Mahler / Newton basis. The
visibility law and the \(N_1\) obstruction (not the next trit)
are project-specific.

---

## 14. What this milestone does not claim

- No single-term \(C_{k,k-3}\) or \(M_k(x^3)\).
- No generic deficit engine.
- No claim that \(N_1\) or \(N_0\) expose \(p\bmod 3^{r+1}\).
- No work on \(x^4\), primes, or Collatz.

---

## 15. Strongest next question

Does \(N_1\) after a general \(N_2\) filter \(p\equiv q\pmod{3^r}\)
always force singletons on residues coprime to \(3\), with all
surviving fibres confined to \(3\mid p\)? If yes, the residual
geometry of \(x^3\) would split into a visibility law plus a
uniform unit-killing lemma, and only the \(3\)-divisible locus
would need a recursive theory.

Do not start that work automatically.
