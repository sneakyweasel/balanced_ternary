# Newton-stratum fibre laws for residual cubes

**Status:** publication draft from existing theorems. Not a
`PAPER_CANDIDATE` elevation and not marked ready for external review.
The canonical laboratory record remains
[cubic_newton_stratum.md](cubic_newton_stratum.md). This page is the
short extract of that record.

## Abstract

The section residuals of \(x^3\) along balanced-ternary prefixes form a
Mealy machine whose finite-horizon states are Newton residue classes.
At horizon \(k\) and depth deficit \(r\), same-depth fibres are governed
by a three-step hierarchy. The quadratic Newton coordinate \(N_2\) sees
exactly the prefix modulo \(3^r\). After that filter, \(N_1\) injects
every prefix of valuation less than \(r\), and every nontrivial fibre
lies in \(3^r\mathbb Z\). On the surviving locus the constant term \(N_0\)
is either a scaled cube or the mismatched-width quotient
\(Q_{t,K,W}(u)=D^t(u^3)\bmod 3^K\). The family \(1+3^tb\) shows that
\(Q\) admits no compact residue, valuation, or discarded-digit
classifier independent of the width parameters.

These fibre laws are Lean-verified. They are not a closed formula for
the Myhill–Nerode count \(M_k(x^3)\), not a Collatz statement, and not
a template claimed for every degree. In degree at most 3, residue
visibility at deficit \(1\) is exactly the condition that the cubic
coefficient is a unit modulo \(3\).

## 1. Introduction

The \((3)\)-section of an integer polynomial is classical: it is a
Cartier / \(p\)-kernel operator, and the Newton (binomial) coordinates
of \(\operatorname{Int}(\mathbb Z)\) classify polynomial functions
modulo \(3^k\). The question here is narrower.

> Which Newton coordinates of the residual family of \(x^3\) are
> visible at a given depth deficit, and what exact obstruction remains
> after that hierarchy?

The answer has four parts.

1. Packed prefixes of length \(m\) label the residual polynomials of
   \(x^3\). Same-depth equivalence at horizon \(k\) is agreement of
   Newton residues modulo \(3^k\).
2. At deficit \(r\), \(N_2\) is equivalent to congruence of the prefix
   modulo \(3^r\).
3. After \(N_2\), \(N_1\) separates every prefix with \(v_3(p)<r\), and
   every remaining collision lives in \(3^r\mathbb Z\).
4. On that locus, \(N_0\) reduces to a two-regime identity whose
   exhausted case is the mismatched quotient \(Q\). The family
   \(1+3^tb\) forces \(W-t\) extra trits, so \(Q\) has no compact
   classifier.

The first item is a dictionary with the classical section calculus.
The next three are the project-specific stratum. The last is a
boundary, not a prompt to invent further fibre types.

No closed formula for \(M_k(x^3)\) is claimed. The image identity
\(M_k(x^3)=\lvert\bigcup_m\operatorname{Im} F_k(m,\cdot)\rvert\) and
the computational table through \(k=14\) stay in the laboratory
monograph.

## 2. Residual machine and Newton coordinates

Let \(\operatorname{lsd}(n)\in\{-1,0,+1\}\) be the balanced residue of
\(n\) modulo \(3\), and write
\[
D(n)=\frac{n-\operatorname{lsd}(n)}{3}.
\]
For \(f\in\mathbb Z[x]\) and a trit \(a\in\{-1,0,+1\}\), the section
\[
\mathfrak D_a f(x)=\frac{f(a+3x)-\rho_a(f)}{3},\qquad
\rho_a(f)=\operatorname{lsd}(f(a))
\]
is the Cartier / \(p\)-kernel operator on \(\mathbb Z[x]\). Iterating
along an LSD-first trit word \(w\) produces a residual polynomial
\(f_w\) and an output word of length \(\lvert w\rvert\). Two polynomials
are equivalent at horizon \(k\), written \(f\equiv_k g\), when every
word of length \(k\) yields the same output. This coincides with
function congruence modulo \(3^k\):
\[
f\equiv_k g
\iff
\forall n\in\mathbb Z,\quad
3^k\mid(f(n)-g(n)).
\]
The complete finite invariant is the Newton residue sequence
\[
\Phi_k(f)=\bigl(\Delta^j f(0)\bmod 3^k\bigr)_{j\ge 0}.
\]
These statements are classical once the residual machine is identified
with the section operator (registry ids
`cahen-chabert-1997-integer-valued-polynomials`,
`kempner-1921-polynomials-residue-systems`). Nonlinear polynomials have
infinitely many distinct sections
(`ahmed-savchuk-2020-polynomial-tree-endomorphisms`).

Packed prefixes
\[
P_m=\bigl\{p\in\mathbb Z:\lvert p\rvert\le(3^m-1)/2\bigr\}
\]
are the length-\(m\) balanced-ternary words. Along \(p\in P_m\),

\[
f_{m,p}(x)=D^m\bigl((p+3^m x)^3\bigr)
=3^{2m}x^3+3^{m+1}p\,x^2+3p^2 x+D^m(p^3).
\]

The Lean identity is `residualAlong_Xcube`. Distinct words remain
distinct as ordinary polynomials, so the raw residual count is
\(R_k(x^3)=(3^k-1)/2\). Write
\[
F_k(m,p)=\Phi_k(f_{m,p})
\]
and label the Newton coordinates of this image by
\((N_0,N_1,N_2,N_3)\). Same-depth equivalence at horizon \(k\) is
agreement of these residues modulo \(3^k\).

The Myhill–Nerode count is the image cardinality
\(M_k(x^3)=\lvert\operatorname{Im} F_k\rvert\). That definition is
used only as context. The theorem below classifies same-depth fibres,
not the size of the image.

## 3. Unified stratum theorem

Fix a horizon \(k\) and a deficit \(r\) with \(r+1\le k\). Set
\(m=k-1-r\). For \(p,q\in P_m\):

**Theorem (Newton stratum of \(x^3\)).**

1. **\(N_2\) visibility.**
   \(N_2(p)\equiv N_2(q)\pmod{3^k}\) if and only if
   \(p\equiv q\pmod{3^r}\).
2. **\(N_1\) after \(N_2\).** If \(p-q=3^r\delta\), then \(N_1\)
   agrees if and only if
   \(3^{k-1-r}\mid\delta(p+q+3^m)\). If also \(v_3(p)<r\), then
   \(p=q\). Every nontrivial \(N_2{+}N_1\) fibre lies in
   \(3^r\mathbb Z\).
3. **\(N_0\) on the surviving locus.** Write \(p=3^ru\). Then
   \[
   D^m\bigl((3^ru)^3\bigr)
   =
   \begin{cases}
   3^{3r-m}u^3,& m\le 3r,\\
   D^{m-3r}(u^3),& m\ge 3r.
   \end{cases}
   \]
   Equivalently \(k\le 4r+1\) versus \(k\ge 4r+1\). In the exhausted
   regime this is the mismatched quotient
   \(Q_{t,K,W}(u)=D^t(u^3)\bmod 3^K\) with
   \((t,K,W)=(k-1-4r,\,k,\,k-1-2r)\).

The Lean façade is `newtonStratum_n2`, `newtonStratum_n1`,
`newtonStratum_n1_val`, `newtonStratum_n21_fibre`,
`newtonStratum_n0_le`, `newtonStratum_n0_ge`, and
`newtonStratum_q`. Ledger row: `BTA-x3-stratum`.

Shallow residuals with \(2m+1<k\) remain \(\equiv_k\)-separated, so
the same-depth count is \(C_{k,m}=3^m\) whenever \(2m+1\le k\). That
count is a corollary of \(N_2\) injectivity, not a separate theory.

The hierarchy does **not** collapse further. Same-depth \(N_2\) does
not imply \(N_1\), and \(N_2{+}N_1\) does not imply \(N_0\). Newton
classes are not congruence classes of the packed prefix. Those
shortcuts are recorded as refutations on the laboratory ledger and
are not revived here.

## 4. The \(Q\) boundary

Write \(u=a+3^tb\) with \(a=\mathrm{bal}_t(u)\). The exact expansion
\[
Q(u)\equiv D^t(a^3)+3a^2b+3^{t+1}ab^2+3^{2t}b^3\pmod{3^K}
\]
has linear carry of valuation \(1\). The discarded digits
\(B_t(u)=\mathrm{bal}_t(u^3)\) are compressible: if \(s\ge 1\) and
\(t\le s+1\), then \(u\equiv v\pmod{3^s}\) implies \(B_t(u)=B_t(v)\).
So \(B_t\) is not an independent growing jet.

They are nevertheless not enough to classify \(Q\). For \(t\ge 1\),

\[
Q(1+3^tb)\equiv Q(1+3^tc)\pmod{3^K}
\iff
b\equiv c\pmod{3^{K-1}}.
\]

The Lean theorem is `newtonStratum_q_one_family`. Every such prefix
shares valuation \(0\), the residue \(1\bmod 3^t\), and the same
\(B_t\). On \(P_W\) one therefore obtains \(3^{W-t}\) distinct
\(Q\)-classes with identical
\(\Psi_4=(v_3,u\bmod 3^t,B_t)\). Any invariant constant on that
family must carry at least \(W-t\) extra trits. On the cubic
parameters this is exactly the width excess \(2r\).

High valuation remains compact: if \(t\le 3s\) and \(K\le 3s-t\), then
\(Q(3^sw)=0\). Threshold \(3s=t\) reduces to a cube residue.

Thus a bounded residue / valuation / sign / \(B_t\) invariant does
not classify \(Q\)-fibres independently of \(t,K,W\). This is the
exact boundary of the stratum. It is not a closed-form counting
theorem, and it is not an invitation to a further \(Q\)-taxonomy.

## 5. Novelty

| Claim | Novelty | Why |
|-------|---------|-----|
| \((3)\)-section / Cartier operator on \(\mathbb Z[x]\) | `KNOWN` / `REPARAMETERIZATION` | standard \(p\)-kernel |
| Newton / binomial coordinates of \(\operatorname{Int}(\mathbb Z)\) | `KNOWN` / `REPARAMETERIZATION` | `cahen-chabert-1997-integer-valued-polynomials`, `kempner-1921-polynomials-residue-systems` |
| Nonlinear polynomials have infinitely many sections | `KNOWN` | `ahmed-savchuk-2020-polynomial-tree-endomorphisms` |
| Residual Mealy machine on LSD-first trit words; \(M_k(f)\) | `PROJECT-SPECIFIC` measurement | dictionary plus prefix locality |
| \(N_2\) visibility, \(N_1\) valuation filter, two-regime \(N_0\) | `PROJECT-SPECIFIC` | not in Cahen–Chabert or Kempner |
| \(Q\) has no compact residue / valuation / \(B_t\) classifier | `PROJECT-SPECIFIC` obstruction | family \(1+3^tb\) |

The fibre laws are not a Collatz theorem. They are also not claimed
for a general degree. For \(\deg f\le 3\) at deficit \(r=1\), some
Newton coordinate sees \(p\bmod 3\) if and only if \(v_3(a_3)=0\).
That is a corollary of \(N_2\) scaling by the cubic coefficient
(**EXACT — HUMAN PROOF**; the coefficient box
\(\{-2,\ldots,2\}\) at \(k\in\{4,5\}\) is
**COMPUTATIONALLY VERIFIED**). Degree \(4\) and \(5\) break the same
line: \(x^3+x^4\) is a same-valuation \(p^2\) contamination, and
\(x^5\) sees residues via \(p^3\equiv p\pmod 3\).

## 6. What is not claimed

- A closed term or polynomial algorithm for \(M_k(x^3)\).
- That \(Q\)-equality is a single residue \(u\equiv v\pmod{3^s}\).
- That stripped \(N_0\) is a standard residual at horizon \(k-2r\).
- A Newton-stratum template for \(x^4\) or for an arbitrary family.
  Phase 0 on \(x^4\) is `CLOSE`d: the linear-in-\(p\) coordinate
  vanishes, and \(N_2\) is only a square filter.
  The degree-\(\le 3\) visibility class is the one-line corollary
  \(v_3(a_3)=0\), not a general-\(f\) classifier
  ([residuals.md](../problems/residuals.md)).
- A solution of the Collatz conjecture, or that balanced ternary is
  an independent solving coordinate for the accelerated map \(T\).

## Lean source map

All names live in `formal/BTCalculus/NewtonStratum.lean` unless noted.

| English | Lean |
|---------|------|
| residual of \(x^3\) along a packed prefix | `residualAlong_Xcube` |
| \(N_2\) visibility | `newtonStratum_n2` |
| \(N_1\) difference law after \(N_2\) | `newtonStratum_n1` |
| valuation injectivity | `newtonStratum_n1_val` |
| nontrivial fibres in \(3^r\mathbb Z\) | `newtonStratum_n21_fibre` |
| \(N_0\) unexhausted / exhausted | `newtonStratum_n0_le`, `newtonStratum_n0_ge` |
| exhausted \(N_0\) is \(Q\) | `newtonStratum_q` |
| family \(1+3^tb\) | `newtonStratum_q_one_family` |

Ledger row: `BTA-x3-stratum`
([theorem_ledger.md](theorem_ledger.md)).

## Appendix. Image identity

By definition,
\[
M_k(x^3)
=
\Bigl\lvert
\bigcup_{m=0}^{k-1}
\operatorname{Im} F_k(m,\cdot)
\Bigr\rvert.
\]
The laboratory monograph evaluates the union by hashing through
\(k=14\) (\(M_{14}=2390443\)) and records the obstruction that the
remaining arithmetic is the vanishing locus of \(Q\) on a balanced
interval of width \(\Theta(k)\). That table and those overlap
families are not part of the theorem package above.

## References and source map

- P.-J. Cahen and J.-L. Chabert, *Integer-Valued Polynomials* (1997),
  registry id `cahen-chabert-1997-integer-valued-polynomials`.
- A. J. Kempner, *Polynomials and their residue systems* (1921),
  registry id `kempner-1921-polynomials-residue-systems`.
- E. Ahmed and D. Savchuk, *Endomorphisms of regular rooted trees
  induced by the action of polynomials on the ring \(\mathbb Z_d\)*
  (2020), registry id
  `ahmed-savchuk-2020-polynomial-tree-endomorphisms`.

Canonical project records:

- [docs/theory/cubic_newton_stratum.md](cubic_newton_stratum.md)
  (laboratory monograph);
- [docs/theory/residual_vs_classical.md](residual_vs_classical.md);
- [docs/problems/residuals.md](../problems/residuals.md);
- `formal/BTCalculus/NewtonStratum.lean`;
- ledger row `BTA-x3-stratum`.
