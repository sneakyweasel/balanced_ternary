# Cubic Newton stratum

Canonical record for the same-depth fibres of the Newton image \(F_k\) of
\(x^3\). Layer notes from Milestones 19–26 are corollaries. This page records the exact same-depth count \(C_{k,m}\) and `CLOSE`s the
dedicated \(x^3\) counting line (§8).

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

Python: `research.residuals.stratum`. Lean: `BTCalculus/NewtonStratum.lean`.
What is new versus classical integer-valued polynomials:
[residual_vs_classical.md](residual_vs_classical.md).

---

## 1. Setup

Packed prefixes \(P_m=\{p\in\mathbb Z:|p|\le(3^m-1)/2\}\) are the
length-\(m\) balanced-ternary words. **EXACT — HUMAN PROOF.**

Along a packed prefix \(p\) of length \(m\),

\[
f_{m,p}(x)=D^m((p+3^m x)^3)
=3^{2m}x^3+3^{m+1}p\,x^2+3p^2 x+D^m(p^3).
\]

**EXACT — LEAN VERIFIED** (`residualAlong_Xcube`). Then
\(F_k(m,p)=\Phi_k(f_{m,p})\) and \(M_k(x^3)=|\operatorname{Im} F_k|\).
**EXACT — HUMAN PROOF** as a definition of the image cardinality
(`BTA-x3-Fk`). Distinct words remain distinct as ordinary polynomials, so
\(R_k(x^3)=(3^k-1)/2\). **EXACT — LEAN VERIFIED.**

Write Newton coordinates \((N_0,N_1,N_2,N_3)\). Same-depth equivalence at
horizon \(k\) is agreement of these residues modulo \(3^k\).

---

## 2. Unified theorem

Fix a horizon \(k\) and a deficit \(r\) with \(r+1\le k\). Set
\(m=k-1-r\). For \(p,q\in P_m\):

1. **\(N_2\) visibility.** \(N_2(p)\equiv N_2(q)\pmod{3^k}\) if and only if
   \(p\equiv q\pmod{3^r}\).
   **EXACT — LEAN VERIFIED** (`newtonStratum_n2`,
   `depthDeficit_n2_visibility`).
2. **\(N_1\) after \(N_2\).** If \(p-q=3^r\delta\), then \(N_1\) agrees if
   and only if \(3^{k-1-r}\mid\delta(p+q+3^m)\). If also \(v_3(p)<r\), then
   \(p=q\). Every nontrivial \(N_2{+}N_1\) fibre lies in \(3^r\mathbb Z\).
   **EXACT — LEAN VERIFIED** (`newtonStratum_n1`, `newtonStratum_n1_val`,
   `newtonStratum_n21_fibre`).
3. **\(N_0\) on the surviving locus.** Write \(p=3^ru\). Then

   \[
   D^m((3^ru)^3)
   =
   \begin{cases}
   3^{3r-m}u^3,& m\le 3r,\\
   D^{m-3r}(u^3),& m\ge 3r.
   \end{cases}
   \]

   Equivalently \(k\le 4r+1\) versus \(k\ge 4r+1\). In the exhausted regime
   this is the mismatched quotient
   \(Q_{t,K,W}(u)=D^t(u^3)\bmod 3^K\) with
   \((t,K,W)=(k-1-4r,\,k,\,k-1-2r)\).
   **EXACT — LEAN VERIFIED** (`newtonStratum_n0_le`, `newtonStratum_n0_ge`,
   `newtonStratum_q`).

The remaining \(Q\)-fibres have no compact classifier (§6). Their
contribution to \(C_{k,m}\) is the image count in §7.

---

## 3. Corollaries (former layer notes)

| Deficit | Depth | Historical note |
|---------|-------|-----------------|
| \(r=0\) | \(m=k-1\) | [cubic_deepest_layer.md](cubic_deepest_layer.md) |
| \(r=1\) | \(m=k-2\) | [cubic_intermediate_layer.md](cubic_intermediate_layer.md) |
| \(r=2\) | \(m=k-3\) | [cubic_deficit_two.md](cubic_deficit_two.md) |
| general \(N_1\) | \(m=k-1-r\) | [cubic_n1_valuation.md](cubic_n1_valuation.md) |
| general \(N_0\) | two-regime | [cubic_n0_reduction.md](cubic_n0_reduction.md) |
| mismatched \(Q\) | \((t,K,W)\) | [mismatched_cubic_quotient.md](mismatched_cubic_quotient.md) |

Image and fibre dictionaries that do not depend on a single deficit:
[cubic_residual_image.md](cubic_residual_image.md),
[cubic_residual_fibres.md](cubic_residual_fibres.md).

Shallow residuals with \(2m+1<k\) remain \(\equiv_k\)-separated.
**EXACT — HUMAN PROOF.** \(C_{k,m}=3^m\) whenever \(2m+1\le k\).
**EXACT — HUMAN PROOF** (from \(N_2\) injectivity).

---

## 4. Refuted shortcuts

These remain on the ledger. They are not revived by the unified statement.

- Newton classes are congruence classes of \(p(w)\).
- \(M_{k+1}(x^3)=3M_k(x^3)+1\).
- Same-depth \(N_2\) implies \(N_1\); \(N_2{+}N_1\) implies \(N_0\).
- Every fibre is a sign pair or a full \(3\)-adic coset.
- Stripped \(N_0\) is a standard residual at horizon \(k-2r\).
- \(Q\)-equality is a single residue \(u\equiv v\pmod{3^s}\).
- A bounded residue / valuation / sign / \(B_t\) invariant classifies
  \(Q\)-fibres independently of the parameters.

---

## 5. Dedicated counting line

**CLOSE**d in §8. Do not open another numbered
\(x^3\) counting milestone. The \(Q\)-taxonomy is already closed in §6.

---

## 6. Invariant decision for \(Q\)

Write \(u=a+3^tb\) with \(a=\mathrm{bal}_t(u)\). The exact expansion
**EXACT — LEAN VERIFIED** (`q_split_high`, `q_one_shift`) is

\[
Q(u)\equiv D^t(a^3)+3a^2b+3^{t+1}ab^2+3^{2t}b^3\pmod{3^K}.
\]

The linear carry has valuation \(1\). Sufficient information exponents
are \(\alpha=t\) and \(\beta=K-1\) on units
**EXACT — HUMAN PROOF**. On the cubic domain \(W-t=2r<K-1\), that
means the whole high word \(b\).

The discarded digits \(B_t(u)=\mathrm{bal}_t(u^3)\) *are* compressible:
if \(s\ge 1\) and \(t\le s+1\), then \(u\equiv v\pmod{3^s}\) implies
\(B_t(u)=B_t(v)\). **EXACT — LEAN VERIFIED** (`balCubic_of_mod`).
So \(B_t\) is not an independent growing jet.

They are nevertheless not enough to classify \(Q\). For \(t\ge 1\),

\[
Q(1+3^tb)\equiv Q(1+3^tc)\pmod{3^K}
\iff
b\equiv c\pmod{3^{K-1}}.
\]

**EXACT — LEAN VERIFIED** (`q_one_family_dvd`,
`newtonStratum_q_one_family`). Every such prefix shares
\(v_3=0\), the residue \(1\bmod 3^t\), and the same \(B_t\). On
\(P_W\) one therefore obtains \(3^{W-t}\) distinct \(Q\)-classes
with identical \(\Psi_4=(v_3,u\bmod 3^t,B_t)\).
**COMPUTATIONALLY VERIFIED** at the exhausted samples
\((r,k)=(1,6),(1,7),(1,8)\). Any invariant constant on that family
must carry at least \(W-t\) extra trits. On cubic parameters this is
exactly the width excess \(2r\).

High valuation remains compact: if \(t\le 3s\) and \(K\le 3s-t\), then
\(Q(3^sw)=0\). **EXACT — LEAN VERIFIED** (`q_high_zero`).
Threshold \(3s=t\) reduces to a cube \(w^3\bmod 3^K\).

**REFUTED**: a bounded residue / valuation / sign / \(B_t\) invariant
classifies \(Q\)-fibres independently of \(t,K,W\).

**CLOSE**, with a partial high-valuation invariant. The
\(Q\)-classification line should not continue by inventing further
fibre types. Counting proceeds in §7 by image cardinality, not by a
new invariant. The counting line itself closes in §8.

---

## 7. Exact state complexity

Master identity **EXACT — HUMAN PROOF** (`BTA-x3-Fk`):

\[
M_k(x^3)
=
\Bigl\lvert
\bigcup_{m=0}^{k-1}
\operatorname{Im} F_k(m,\cdot)
\Bigr\rvert.
\]

Write \(r=k-1-m\) and \(W=k-1-2r\). The balanced interval satisfies
\(3^ru\in P_m\) if and only if \(u\in P_W\) when \(r\le m\), and forces
\(u=0\) when \(r>m\). **EXACT — LEAN VERIFIED**
(`balWidth_pow_iff`, `newtonStratum_core_width`).

On \(P_m\), the prefixes with \(v_3(p)<r\) are first-nonzero-digit
words of length \(m\). Their count is

\[
E_{k,r}
=
\begin{cases}
0,& r=0,\\
3^m-3^{m-r},& 1\le r\le m,\\
3^m,& r>m.
\end{cases}
\]

**EXACT — HUMAN PROOF.** After \(N_2\), each such prefix is a singleton
(`n1_val_lt_injective`). The complementary core is hashed as
\(\{(N_1,N_0)\}\) on \(P_W\) only. Therefore

\[
C_{k,k-1-r}
=
E_{k,r}
+
\bigl\lvert
\{F_k(k-1-r,\,3^ru):u\in P_W\}
\bigr\rvert
\]

when \(r\le m\), and \(C_{k,m}=3^m\) when \(r>m\).
**EXACT — HUMAN PROOF** (`BTA-x3-C-decomp`). On the core, once
\(k\ge 2r+2\),

\[
N_1\equiv 3^{2r+1}u^2\pmod{3^k}.
\]

**EXACT — LEAN VERIFIED** (`n1_on_core_mod`).

In the strict unexhausted regime \(k<4r+1\), \(N_1\) sees \(u^2\)
completely on \(P_W\), so collisions are only sign pairs, and a
surviving sign pair already forces the zero class. Hence

\[
C_{k,k-1-r}
=
3^{k-1-r}-Z_{k,r}+1,
\qquad
Z_{k,r}=3^{\max(W-s,0)},
\quad
s=\Bigl\lceil\frac{2k-4r-1}{3}\Bigr\rceil
\]

(with \(Z=1\) if \(s>W\)). **EXACT — HUMAN PROOF**, and
**COMPUTATIONALLY VERIFIED** through \(k=14\).

On units \(3\nmid a\) and \(t\ge 1\),

\[
G_a(b)\equiv G_a(c)\pmod{3^K}
\iff
b\equiv c\pmod{3^{K-1}}.
\]

**EXACT — LEAN VERIFIED** (`q_unit_family_dvd`). This is the unit
stratum image law: each fixed unit low part contributes
\(3^{\min(W-t,K-1)}\) distinct \(Q\)-values. Different \(a\) may still
overlap, and \(N_1\) is not a function of \(N_0\) on the exhausted
core, so the same-depth count uses the joint image
\(\lvert(N_1,N_0)\rvert\), not \(\lvert N_0\rvert\) alone.

Cross-depth collisions require \(k\le 2\min(m,n)+1\)
**EXACT — LEAN VERIFIED** (`n3_dvd_iff`). All shallow layers
\(2m+1<k\) are therefore disjoint from each other and from the deep
block, which gives the exact algorithm

\[
M_k
=
\frac{3^{\lfloor k/2\rfloor}-1}{2}
+
\Bigl\lvert
\bigcup_{m\ge\lfloor k/2\rfloor}
\operatorname{Im} F_k(m,\cdot)
\Bigr\rvert.
\]

The zero spine \(p=0\) at depths \(2m\ge k\) is a single Newton class
**EXACT — LEAN VERIFIED** (`zero_spine_n1`, `zero_spine_n2`,
`zero_spine_n0`, `zero_spine_n3`). It is **not** the only overlap:
already at \(k=6\) the sign pair \(\{\pm 3\}\) is shared by depths
\(4\) and \(5\). **COMPUTATIONALLY VERIFIED** through \(k=14\). The
nonzero families are small-prefix sign pairs with vanishing \(N_0\),
valuation translates, and high-valuation cube residues.

The counting method enumerates \(P_W\) for each deficit and the deep
layers for the union. The deepest layer still has width \(k-1\), so
the exact algorithm is exponential in \(k\), not polynomial.

Verification table. \(R_k=(3^k-1)/2\). Every \(C_{k,m}\) and \(M_k\)
is an exact arithmetic image count (unexhausted \(C\) by the formula
above; exhausted \(C\) and all \(M_k\) by hashing \(F_k\)). Through
\(k=9\), \(M_k\) also matches the full Myhill–Nerode image
`M_k_x3`. \(M_{12}=265352\) matches the Milestone 20 value.

| \(k\) | \(R_k\) | \(M_k\) | \(R_k-M_k\) | \(M_k/R_k\) | source |
|------:|--------:|--------:|------------:|------------:|:-------|
| 2 | 4 | 3 | 1 | 0.750 | MN + arithmetic |
| 3 | 13 | 12 | 1 | 0.923 | MN + arithmetic |
| 4 | 40 | 36 | 4 | 0.900 | MN + arithmetic |
| 5 | 121 | 115 | 6 | 0.950 | MN + arithmetic |
| 6 | 364 | 349 | 15 | 0.959 | MN + arithmetic |
| 7 | 1093 | 1074 | 19 | 0.983 | MN + arithmetic |
| 8 | 3280 | 3231 | 49 | 0.985 | MN + arithmetic |
| 9 | 9841 | 9780 | 61 | 0.994 | MN + arithmetic |
| 10 | 29524 | 29394 | 130 | 0.996 | arithmetic |
| 11 | 88573 | 88399 | 174 | 0.998 | arithmetic |
| 12 | 265720 | 265352 | 368 | 0.999 | arithmetic |
| 13 | 797161 | 796678 | 483 | 0.999 | arithmetic |
| 14 | 2391484 | 2390443 | 1041 | 0.999 | arithmetic |

Per-depth \(C_{k,m}\) for \(m=0,\ldots,k-1\):

| \(k\) | \(C_{k,m}\) |
|------:|:------------|
| 2 | 1, 2 |
| 3 | 1, 3, 8 |
| 4 | 1, 3, 9, 24 |
| 5 | 1, 3, 9, 27, 76 |
| 6 | 1, 3, 9, 27, 80, 232 |
| 7 | 1, 3, 9, 27, 81, 240, 716 |
| 8 | 1, 3, 9, 27, 81, 243, 721, 2153 |
| 9 | 1, 3, 9, 27, 81, 243, 727, 2178, 6521 |
| 10 | 1, 3, 9, 27, 81, 243, 729, 2180, 6537, 19597 |
| 11 | 1, 3, 9, 27, 81, 243, 729, 2185, 6554, 19652, 58939 |
| 12 | 1, 3, 9, 27, 81, 243, 729, 2187, 6559, 19661, 58977, 176908 |
| 13 | 1, 3, 9, 27, 81, 243, 729, 2187, 6559, 19677, 59022, 177057, 531141 |
| 14 | 1, 3, 9, 27, 81, 243, 729, 2187, 6561, 19681, 59028, 177083, 531230, 1593644 |

CLI: `btprime calculus x3-states --k <k>`,
`btprime calculus x3-layer-count --k <k> --deficit <r>`,
`btprime calculus x3-image-count --k <k> --deficit <r>`,
and `btprime calculus x3-overlaps --k <k>`.
The commands `newton-class`, `cubic-layer`, and `cubic-quotient` are
unchanged.

The dedicated counting line is **CLOSE**d in §8. There is
no single closed term \(M_k=F(k)\). The exact algorithm remains the
\(N_3\)-gated deep-image union.

---

## 8. CLOSE — counting obstruction

This is the last dedicated \(x^3\) counting record. Do not open another
numbered counting milestone.

### Reduced core

On the exhausted core \(p=3^ru\) with \(k\ge 2r+2\),

\[
N_1\equiv 3^{2r+1}u^2\pmod{3^k}
\qquad\Longleftrightarrow\qquad
A_{k,r}(u)=u^2\bmod 3^{k-2r-1}.
\]

**EXACT — LEAN VERIFIED** (`n1_on_core_mod`, `n1_core_square_iff`,
`newtonStratum_n1_square`). The observable square exponent equals the
core width: \(k-2r-1=W\). **EXACT — LEAN VERIFIED**
(`square_exp_eq_width`). The joint core map is therefore

\[
H_{k,r}(u)=\bigl(u^2\bmod 3^W,\; Q_{t,k,W}(u)\bigr),
\qquad
t=k-1-4r,
\]

and

\[
C_{k,k-1-r}=E_{k,r}+\lvert\operatorname{Im} H_{k,r}\rvert
\]

in the exhausted regime. **EXACT — HUMAN PROOF.** The \(Q\)-image,
the \(N_1\)-image, and the joint image are three different sets.
**COMPUTATIONALLY VERIFIED**: at \((k,r)=(6,1)\) one has
\(\lvert\operatorname{Im} H\rvert=26\), \(\lvert\operatorname{Im} Q\rvert=23\),
\(\lvert\operatorname{Im} A\rvert=11\).

### Unit contribution

If \(3\nmid u,v\) and \(u,v\in P_W\), then
\(u^2\equiv v^2\pmod{3^W}\) if and only if \(u=\pm v\).
**EXACT — LEAN VERIFIED** (`unit_square_pm`,
`newtonStratum_unit_square`). Next,
\(N_0(u)\equiv N_0(-u)\pmod{3^k}\) if and only if
\(N_0(u)\equiv 0\pmod{3^k}\). **EXACT — LEAN VERIFIED**
(`n0_eq_of_neg`, `newtonStratum_n0_neg`). Hence two units collide in
\(H\) if and only if they are a sign pair with vanishing \(Q\). For
\(W\ge 1\),

\[
U_{k,r}
=
2\cdot 3^{W-1}-S^\times_{k,r},
\]

where \(S^\times_{k,r}\) is the number of positive units
\(u\in P_W\) with \(Q(u)=0\). **EXACT — HUMAN PROOF.** The count
\(S^\times\) is the vanishing locus of \(Q\) on \(P_W^\times\). That
locus has no compact residue / valuation / \(B_t\) classifier
independent of the parameters (§6). **EXACT — HUMAN PROOF** as a
citation of the Milestone 27 CLOSE.

### Valuation strata

Write \(u=3^sw\) with \(3\nmid w\).

- Low \(3s<t\): \(Q\) is a genuine mismatched cubic. Units in this
  range contribute to \(U_{k,r}\).
- Threshold \(3s=t\): \(Q\) is a cube residue \(w^3\bmod 3^k\).
- High \(3s>t\): \(Q=0\). **EXACT — LEAN VERIFIED** (`q_high_zero`).

When \(2s\ge W\), the square coordinate collapses: \(A(u)=0\). Distinct
high-valuation prefixes may then share \(A=0\) with distinct or
identical \(Q\). These zero-\(A\) merges are an exact correction to
\(\lvert P_W\rvert\), not a new invariant. **COMPUTATIONALLY VERIFIED**
through \(k=12\).

Non-units can also share a nonzero square without being a sign pair
(twins). At the deepest layer \(k=8\) the pairs
\(\{720,738\}\) and \(\{-738,-720\}\) are distinct twin fibres
(\(A=81\), distinct \(Q\)). At \((k,r)=(12,1)\) the same pattern
reappears. **COMPUTATIONALLY VERIFIED.** No compact arithmetic law
enumerating all twins was found; they sit on the same vanishing /
near-square locus as the unit \(Q\)-zeros.

Therefore

\[
\lvert\operatorname{Im} H_{k,r}\rvert
=
3^W-S_{k,r}-\text{(zero-\(A\) merges)}-\text{(twin surplus)},
\]

where every correction term is a \(Q\)-vanishing or square-collision
count on \(P_W\). This is an exact bookkeeping identity, not a closed
formula. **EXACT — HUMAN PROOF.**

### Cross-depth families

Collisions across depths require \(m\in D_k=\{m:2m+1\ge k\}\).
**EXACT — LEAN VERIFIED** (`n3_dvd_iff`). The observed nonzero
families, after the zero spine, are:

| family | typical witness | status |
|--------|-----------------|--------|
| shared-sign | \(\{\pm 3\}\) at \(k=6\); \(\{\pm 9\},\{\pm 18\}\) at \(k=12\) | **COMPUTATIONALLY VERIFIED** |
| valuation translate | \(117\leftrightarrow 1089\) | **COMPUTATIONALLY VERIFIED** |
| one-to-coset | depth \(10\) vs \(11\) at \(k=10\) | **COMPUTATIONALLY VERIFIED** |
| high-valuation cubes | \(3\)-to-\(27\) fibres at \(k=12\), depths \(8,11\) | **COMPUTATIONALLY VERIFIED** |
| twin translates | \(\{\pm 19656,\pm 19710\}\) vs \(\{\pm 59022,\pm 59076\}\) at \(k=12\) | **COMPUTATIONALLY VERIFIED** |

**REFUTED**: every nonzero overlap is the zero spine or a shared sign
pair. **REFUTED** as a closed taxonomy: the heuristic buckets
`shared-sign` / `translate` / `one-to-coset` do not exhaust the
\(k=12\) sample (the remainder is high-valuation cubes and twin
translates). No theorem was obtained that every future overlap lies
in a finite list of closed arithmetic families independent of \(k\).

Triple (or longer) intersections occur. The zero spine is one such
class. Nonzero triples through \(k=12\) are shared-sign prefixes
\(\{\pm 9\}\) and \(\{\pm 18\}\). **COMPUTATIONALLY VERIFIED.**
Inclusion-exclusion over all deep layers is therefore unnecessary
once the spine is removed, but the remaining pairwise families still
have no closed count.

### Complexity

The exact algorithm hashes \(F_k(m,\cdot)\) on
\(m\ge\lfloor k/2\rfloor\). The deepest layer is \(P_{k-1}\), so the
cost is \(\Theta(3^{k-1})\) residual evaluations. Unexhausted same-depth
counts are closed form, and exhausted cores hash \(P_W\) rather than
\(P_m\), but the leading term remains the deepest layer. This is still
exponential in \(k\), of the same order as enumerating the residual
tree. It is not polynomial and not subexponential.
**EXACT — HUMAN PROOF.**

### Decision

**CLOSE.** After the exact Newton-hierarchy reductions, the
remaining objects are image cardinalities of cubic maps on balanced
intervals of width \(\Theta(k)\). Counting them is equivalent to
enumerating the vanishing locus of the mismatched quotient \(Q\) on
\(P_W\), together with a short list of classified but non-closed-form
cross-depth families. Milestone 27 proved that this locus has no
compact residue classifier. Therefore there is no substantially
simpler exact counting representation within the natural \(3\)-adic
arithmetic of \((N_1,Q)\) than hashing those domains.

The strongest exact theorem remains

\[
M_k(x^3)
=
\frac{3^{\lfloor k/2\rfloor}-1}{2}
+
\Bigl\lvert
\bigcup_{m\ge\lfloor k/2\rfloor}
\operatorname{Im} F_k(m,\cdot)
\Bigr\rvert.
\]

**EXACT — HUMAN PROOF**, with the union evaluated by hashing through
\(k=14\) (**COMPUTATIONALLY VERIFIED**; \(M_{14}=2390443\)).

The dedicated \(x^3\) counting line is closed. The Newton-stratum
structure (visibility, valuation injectivity, two-regime \(N_0\),
mismatched \(Q\), joint-image reduction) is the paper-worthy record.
The sequence \(M_k\) is a computational appendix, not a closed-form
theorem. Do not start another \(x^3\) counting milestone.
