# Cubic Newton stratum

Canonical record for the same-depth fibres of the Newton image \(F_k\) of
\(x^3\). Layer notes from Milestones 19–26 are corollaries. This page does
**not** give a closed formula for \(M_k(x^3)\).

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

There is no closed cardinality for the remaining \(Q\)-fibres.
The invariant decision is recorded in §6.

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

## 5. What remains open

A closed formula for \(M_k(x^3)\). The \(Q\)-invariant question is
closed in §6: no compact residue/valuation/\(B_t\) classifier exists,
and the obstruction is the high-trit carry. Do not open a numbered
milestone for a further \(Q\)-taxonomy.

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

**Outcome C**, with a partial high-valuation invariant. Counting
\(\lvert\mathrm{im}\,Q\rvert\) is not reduced to an elementary formula
for \(M_k(x^3)\). The \(Q\)-classification line should not continue by
inventing further fibre types. The remaining complexity is the cubic
carry on the extra \(2r\) trits.
