# Unrestricted residual complexity \(C_F(m,r)\)

## Problem

Exact two-parameter census of unrestricted residual right-language types
after input depth \(m\) and remaining horizon \(r\).

## Exact statement

Let \(F\in\mathbb Z[x]\). Write \(C_F(m,r)\) for the number of distinct
remaining-horizon-\(r\) right-language types among **unrestricted**
residuals of \(F\) after input depth \(m\) (all \(3^m\) prefixes; no
safety or live filter). Equivalently: types of the residual Mealy
machine of \(F\) at depth \(m\), distinguished by exact finite-horizon
equivalence \(\equiv_r\).

Question: is there an exact two-parameter law for \(C_F(m,r)\) (start
with \(F(x)=x\) and \(F(x)=x^2\)), or a proved obstruction that this is
not a remaining-horizon clock and not a closed low-degree formula?

This is **not** the live safety census of
[regular_output_preimages.md](regular_output_preimages.md). That
module's `census_count` counts live types for \(Y=\{0,+\}^\omega\).
\(C_F\) is unconstrained. Horizon-7 live counts
\(1,3,7,16,33,66,131,260\) are not \(C_F\).

## Current literature

- `ahmed-savchuk-2020-polynomial-tree-endomorphisms`: an integer
  polynomial induces a finite-state rooted-tree endomorphism if and
  only if it is linear. Unrestricted \(x^2\) is infinite-state.
  `KNOWN`. Infinite-state is the raw residual tree, not the two-parameter
  slice \(C_F(m,r)\).
- `anashin-2012-automata-finiteness`,
  `grigorchuk-savchuk-2023-solenoidal-maps`: finite-Mealy criteria for
  1-Lipschitz maps. `KNOWN`.
- Ledger `BTA-x2-mn` / [quadratic_residual_complexity.md](../theory/quadratic_residual_complexity.md):
  \(M_k(x^2)=R_k(x^2)=(3^k-1)/2\) counts \(\equiv_k\)-classes among
  residuals of length \(<k\). That is the triangle \(m<k\), summed.
  `KNOWN`. It does not name \(C_F(m,r)\) for \(m>r\).
- Ledger `BTA-x3-M-obstruct`: cubic \(M_k(x^3)\) counting is `CLOSE`.
  This gate does not reopen it, does not add fibre types, and does not
  open \(x^4\)/\(x^5\) counting.
- Ledger `BTR-x2-safety-nonsific`: safety preimage of \(\{0,+\}^\omega\)
  is not regular. A different pair (constrained \(L\)). Not this census.

## Branch budget

```text
Mathematical target     Is there an exact two-parameter law for unrestricted C_F(m,r), starting with F(x)=x and F(x)=x², or a proved obstruction that the census is not a remaining-horizon clock and not a closed low-degree formula?
Novelty hypothesis      For low-degree F, C_F(m,r) may have a closed two-parameter expression (or a short recurrence) that is not the safety table, not M_k(x²) restated on the triangle m<r, and not Ahmed–Savchuk infinite-state.
Falsifier               Growth that still needs width-Θ enumeration; a table with no law inside Phase-0 range; reduction to the closed M_k(x³) line; restatement of Ahmed–Savchuk unrestricted infinite-state; accidentally recomputing the safety census.
Existing machinery      bt.calculus residual rho/delta/residual_along/output_along; IntPoly; Φ_r / degree-≤2 coeff mod 3^r; reachable layers; levelled_mealy_count as the clock contrast; safety census only as a contrast table.
Maximum Phase-0 scope   F ∈ {x, x²}, exact m,r ≤ 7, exact finite-horizon types, no manufactured countdown states, no cubic fibres, no CLI.
Promotion criterion     A proved closed law, or a proved obstruction that this census cannot have a simple two-parameter closed form in the intended class.
Stop criterion          Bounded tables only; safety-census reparameterization; Ahmed–Savchuk restatement; cubic-stratum reopen.
```

## Balanced-ternary formulation

The residual machine is the existing Mealy law

\[
F \xrightarrow{a/\rho_a(F)} \mathfrak D_a F, \qquad a\in\{-1,0,+1\}.
\]

A type at horizon \(r\) is an \(\equiv_r\)-class: equal output words on
every input of length \(r\). For degree \(\le 2\) this is the coefficient
triple modulo \(3^r\). Depth-\(m\) residuals of \(x^2\) are

\[
f_p(x)=3^m x^2+2p\,x+\mathrm{DZ}^m(p^2), \qquad p\in P_m.
\]

## Why BT may be relevant

Packed prefixes are the native state coordinate of the residual machine.
The colliding family on the superdiagonal is three constant-trit words
and the balanced expansion of \(((3^r-1)/2)^2\).

## Candidate operations / invariants

- \(\Phi_r\) / `phi_k` — exact \(\equiv_r\) type. **PROVED** (existing).
- Degree-\(\le 2\) coefficient triple mod \(3^r\). **PROVED** (`BTA-quad-mod`).
- Unrestricted census \(C_F(m,r)\). **COMPUTATIONALLY VERIFIED** through
  \(m,r\le 7\).
- Band law \(C_{x^2}(m,r)=3^m\) for \(r\ge m\), and
  \(C_{x^2}(m,m-1)=3^m-3\) for \(m\ge 2\). **PROVED**.
- Remaining-horizon clock `levelled_mealy_count`. Excluded as a type
  predicate: it grows on \(F(x)=x\).

## Experiments

`research.residual_complexity.triage` with \(m,r\le 7\), polynomials
`x` and `x^2`. Tests live in
`tests/research/residual_complexity/test_triage.py`. Safety counts are
imported only as a contrast.

## Conjectures

None registered. Interior cells \(0<r<m-1\) are not conjectured.

## Counterexamples

1. **Not a remaining-horizon clock.** `levelled_mealy_count(x,k)=k` for
   \(k\ge 0\), while \(C_x(m,r)=1\). Witness in
   `test_identity_has_one_unrestricted_type`.
2. **Not \(3^{\min(m,r)}\).** \(C_{x^2}(2,1)=6\neq 3\).
3. **Not the coefficient cap \(\min(3^m,3^{2r})\).** \(C_{x^2}(2,1)=6\neq 9\).
4. **Not the safety census.** Horizon-7 live counts
   \(1,3,7,16,33,66,131,260\); unrestricted
   \(1,3,9,27,81,243,729,2187\).

## Formalization

None. No `sorry`. Lean is not opened on this gate.

## Results

### Linear control

**EXACT — HUMAN PROOF.** \(C_x(m,r)=1\) for every \(m,r\ge 0\).

Every residual of \(x\) is \(x\) itself, so there is one polynomial and
one right language. This is the Ahmed–Savchuk linear case (`KNOWN`) and
is why the census is not a remaining-horizon clock.

### Triangle \(r\ge m\)

**EXACT — HUMAN PROOF.** \(C_{x^2}(m,r)=3^m\) whenever \(r\ge m\ge 0\).

At depth \(m\) the leading coefficient is \(3^m\) for every prefix.
Degree \(\le 2\) gives \(\equiv_r\) iff coefficients agree modulo \(3^r\)
(`BTA-quad-mod`). Then \(3^r\mid 2(p-q)\) with \(2\) a unit forces
\(p\equiv q\pmod{3^r}\). Prefixes in \(P_m\) satisfy \(|p-q|\le 3^m-1\),
so \(r\ge m\) implies \(p=q\). Novelty: `KNOWN` as the same-depth case of
the \(M_k(x^2)\) layer-injectivity already used to sum
\(M_k=(3^k-1)/2\); recorded here because it is one slice of \(C_F\).

### Superdiagonal \(r=m-1\)

**EXACT — HUMAN PROOF** (`BTR-x2-C-band`). For \(m\ge 2\),

\[
C_{x^2}(m,m-1)=3^m-3.
\]

The deficit is exactly three doubletons. Write \(r=m-1\). Two depth-\(m\)
residuals can merge at horizon \(r\) only if they share the same packed
prefix modulo \(3^r\), i.e. they are two of the three one-trit extensions
of a common word \(\alpha\in P_r\). For each \(\sigma\in\{-1,0,+1\}\) let
\(u_\sigma=\sigma^r\). The two extensions of \(u_\sigma\) by a trit other
than \(\sigma\) are \(\equiv_r\)-equivalent, and every other pair of
distinct length-\(m\) prefixes is distinguished.

*Proof.* Same-\(\alpha\) is necessary because \(B=2p\) and \(2\) is a
unit modulo \(3^r\). Write \(p_\varepsilon=\alpha+\varepsilon 3^r\).
The integers \(C_\varepsilon=\mathrm{DZ}^{r+1}(p_\varepsilon^2)\) are
the constant terms. They satisfy
\(p_\varepsilon^2=3^{r+1}C_\varepsilon+\mathrm{low}_{r+1}(p_\varepsilon^2)\)
with \(\lvert\mathrm{low}\rvert\le(3^{r+1}-1)/2\), so
\(\lvert C_\varepsilon-p_\varepsilon^2/3^{r+1}\rvert<1/2\). If
\(\lvert p_\varepsilon^2-p_\delta^2\rvert/3^{r+1}\ge 1\), the two
integers \(C_\varepsilon,C_\delta\) differ.

The rational gaps are
\(\lvert 4\alpha/3\rvert\), \(\lvert 2\alpha/3+3^{r-1}\rvert\), and
\(\lvert -2\alpha/3+3^{r-1}\rvert\). The first is \(<1\) only at
\(\alpha=0\). For \(r=1\) one has \(P_1=\{-1,0,1\}\), all three special
values below. For \(r\ge 2\) the bound
\(\lvert 2\alpha/3+3^{r-1}\rvert<1\) holds in \(P_r\) only at
\(\alpha=-(3^r-1)/2\), and the symmetric bound only at
\(\alpha=(3^r-1)/2\). Thus every non-special \(\alpha\) has three
distinct types.

The three special collisions are direct. If \(\alpha=0\) then
\(p_{\pm 1}=\pm 3^r\) have equal squares, while
\(\mathrm{DZ}^{r+1}(3^{2r})=3^{r-1}\not\equiv 0=\mathrm{DZ}^{r+1}(0)\pmod{3^r}\).
If \(\alpha=\pm(3^r-1)/2\), the two squares in the colliding pair differ
by \(3^r\). The balanced expansion of \(s_r^2\) with \(s_r=(3^r-1)/2\)
is \((+,-)^{r/2}\mathbin{\smallfrown}(-,+)^{r/2}\) for even \(r=2k\) and
\((+,-)^k\mathbin{\smallfrown}(+,0)\mathbin{\smallfrown}(-,+)^k\) for odd
\(r=2k+1\). Both pack to \(s_r^2\) (geometric series). Digit \(r\) is
\(0\) or \(-1\), never \(+1\), so adding \(3^r\) does not carry into
\(\mathrm{DZ}^{r+1}\). ∎

### Interior \(0<r<m-1\)

**COMPUTATIONALLY VERIFIED** through \(m,r\le 7\). Table \(C_{x^2}(m,r)\):

```text
m\r   0  1   2    3     4     5     6     7
0     1  1   1    1     1     1     1     1
1     1  3   3    3     3     3     3     3
2     1  6   9    9     9     9     9     9
3     1  9  24   27    27    27    27    27
4     1  9  50   78    81    81    81    81
5     1  9  77  212   240   243   243   243
6     1  9  81  463   694   726   729   729
7     1  9  81  711  1885  2156  2184  2187
```

The coefficient cap \(C_{x^2}(m,r)\le\min(3^m,3^{2r})\) holds (at
horizon \(r\ge 1\) and \(m\ge r\), leading coefficients vanish modulo
\(3^r\), so types inject into \((B,C)\bmod 3^r\)). Saturation at
\(3^{2r}\) is visible for \(r=1\) (\(m\ge 3\)) and \(r=2\) (\(m\ge 6\)),
not proved for general \(r\). No low-degree two-parameter formula
(\(3^{\min(m,r)}\), \(\min(3^m,3^{2r})\), or the cap minus a constant
on \(m=r+1\)) fits the interior. The interior is **OPEN** and is not
claimed.

Cubic \(M_k(x^3)\) counting is not this table.

### Literature classification

- `KNOWN`: \(C_x=1\); unrestricted \(x^2\) infinite-state;
  \(C_{x^2}(m,r)=3^m\) for \(r\ge m\) as same-depth layer injectivity of
  \(M_k(x^2)\).
- `REPARAMETERIZATION`: none of the surviving new statements.
- `PROJECT-SPECIFIC`: the superdiagonal law \(C_{x^2}(m,m-1)=3^m-3\)
  with the three constant-trit doubletons; the two-parameter census as
  a measurement distinct from the safety table.
- `OPEN`: the interior \(0<r<m-1\).

## Open questions

The interior image size of
\(p\mapsto\bigl(p\bmod 3^r,\,\mathrm{DZ}^m(p^2)\bmod 3^r\bigr)\)
for \(0<r<m-1\). Not opened as a follow-up in this phase.

Section entropy versus dynamical entropy, and solenoid / adelic
packaging, remain unopened pending ideas of the safety gate. They are
not this gate.

## Decision

`PROMOTE`. The identity stays at \(1\), so the census is not a
remaining-horizon clock. The safety table is a different sequence. On
the band \(r\ge m-1\) the two-parameter count is exact:
\(C_{x^2}(m,r)=3^m\) for \(r\ge m\), and \(C_{x^2}(m,m-1)=3^m-3\) for
\(m\ge 2\) by three explicit constant-trit doubletons. That is the
promotion criterion. The interior is a table, not a closed form, and is
left open. The branch is not an Ahmed–Savchuk restatement, not a safety
reparameterization, and not a cubic-stratum reopen. No CLI, Lean, or
numbered milestone is added.

Best next question: for \(0<r<m-1\), does \(C_{x^2}(m,r)\) saturate at
\(3^{2r}\) by an explicit threshold \(m_0(r)\), or does the image of
\(\mathrm{DZ}^m(p^2)\bmod 3^r\) still require width-\(\Theta(m-r)\)
enumeration?

## Publication assessment

Status: `STRUCTURAL`.

The superdiagonal collision family is exact and short. It is a gate
theorem for one band of the two-parameter grid, not a paper-scale
classification of \(C_F\) for all \(F\) and all \((m,r)\).
