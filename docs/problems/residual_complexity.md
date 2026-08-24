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

Previous phases promoted the band `BTR-x2-C-band` and parked the zero fibre `BTR-x2-C-interior`. This phase's budget is every interior fibre.

```text
Mathematical target     Does every fibre p≡α (mod 3^r) of the interior map fill (second coordinate all of Z/3^r Z) for all m≥3r, or at the observed m_sat(r), or is there a fibre that stays incomplete for all m?
Novelty hypothesis      A fill law for every fibre with an explicit threshold, or a named incomplete fibre, would be PROJECT-SPECIFIC. Zero-fibre squares at 2r and fill at 3r are already PROJECT-SPECIFIC. Ahmed–Savchuk infinite-state is KNOWN. Same-depth 3^m is KNOWN as M_k(x^2) layer injectivity.
Falsifier               Extra saturation table only; restating the zero fibre; safety reparameterization; Ahmed–Savchuk restatement; cubic reopen.
Existing machinery      residual_complexity.triage (interior_type, interior_image, zero_fibre_witness, FIRST_SATURATION), BTR-x2-C-band, BTR-x2-C-interior, bt.calculus.quadratic (import only).
Maximum Phase-0 scope   Exact types, no sampling. Prefer an explicit construction per fibre (or a named incomplete fibre) over a bigger saturation table. Small-r scans to hunt a stuck fibre, then prove or refute. No cubic, no CLI, no Lean.
Promotion criterion     A proved fill law for every fibre with an explicit threshold, or a proved fibre that stays incomplete for all m.
Stop criterion          Extra table only; restating the zero fibre; safety reparameterization; Ahmed–Savchuk restatement; cubic reopen.
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
  \(m,r\le 7\), with extra interior cells through \(r\le 6\) as recorded
  below.
- Band law \(C_{x^2}(m,r)=3^m\) for \(r\ge m\), and
  \(C_{x^2}(m,m-1)=3^m-3\) for \(m\ge 2\). **PROVED**.
- Zero fibre of the interior map: quadratic residues at \(m=2r\), and
  the full \(\mathbb Z/3^r\mathbb Z\) for \(m\ge 3r\). **PROVED**.
- Every fibre \(p\equiv\alpha\pmod{3^r}\): full second coordinate for
  all \(m\ge 5r\), via \(p=\alpha+u\,3^r+3^{m-r}\). **PROVED**.
- Remaining-horizon clock `levelled_mealy_count`. Excluded as a type
  predicate: it grows on \(F(x)=x\).

## Experiments

`research.residual_complexity.triage` with \(m,r\le 7\), polynomials
`x` and `x^2`, plus an exact integer image
\(p\mapsto(p\bmod 3^r,\,\mathrm{DZ}^m(p^2)\bmod 3^r)\) used past depth 7
only to test saturation and fibre fill. Tests live in
`tests/research/residual_complexity/test_triage.py`. Safety counts are
imported only as a contrast. Cubic fibres are not opened.

## Conjectures

None registered. The guess \(m_0(r)=3r\) as a *sharp* first-saturation
time is discarded (it is not a registered conjecture). The alternative
that some fibre never fills is discarded (`BTR-x2-C-fibre-fill`). Full
interior \(C_{x^2}(m,r)\) remains without a claimed closed form.

## Counterexamples

1. **Not a remaining-horizon clock.** `levelled_mealy_count(x,k)=k` for
   \(k\ge 0\), while \(C_x(m,r)=1\). Witness in
   `test_identity_has_one_unrestricted_type`.
2. **Not \(3^{\min(m,r)}\).** \(C_{x^2}(2,1)=6\neq 3\).
3. **Not the coefficient cap \(\min(3^m,3^{2r})\).** \(C_{x^2}(2,1)=6\neq 9\).
4. **Not the safety census.** Horizon-7 live counts
   \(1,3,7,16,33,66,131,260\); unrestricted
   \(1,3,9,27,81,243,729,2187\).
5. **Not the coefficient cap at width \(m=2r\).** The fibre
   \(p\equiv 0\pmod{3^r}\) realises only quadratic residues, so
   \(C_{x^2}(2r,r)<3^{2r}\). Witnesses: \(C(2,1)=6<9\), \(C(4,2)=50<81\).
6. **Not \(m_0(r)=3r\) as the first saturation time.** \(C_{x^2}(8,3)=729=3^6\)
   already, while \(3r=9\). Also \(C(10,4)=6561\) with \(3r=12\).
7. **Not a permanently incomplete fibre.** Every fibre fills for all
   \(m\ge 5r\) (`BTR-x2-C-fibre-fill`). The alternative of a 3-adic
   square/valuation obstruction that keeps some \(\alpha\) incomplete
   for all \(m\) is false.
8. **Not a single fixed high trit \(v=1\) at width \(m=3r\).** Varying
   only the low block \(u\) with \(p=\alpha+u\,3^r+3^{2r}\) misses at
   least one fibre for \(r=2\) (and likewise the \(v=1\) family at
   \(m=5r-1\) is not the proved filling family). Full saturation of a
   general fibre at the \(5r\) threshold uses the family
   \(p=\alpha+u\,3^r+3^{m-r}\) with \(u\) running through \(P_r\).

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
\(3^r\), so types inject into \((B,C)\bmod 3^r\), equivalently
\((p\bmod 3^r,\,\mathrm{DZ}^m(p^2)\bmod 3^r)\)). No low-degree
two-parameter formula (\(3^{\min(m,r)}\), \(\min(3^m,3^{2r})\), or the
cap minus a constant on \(m=r+1\)) fits every interior cell. Cubic
\(M_k(x^3)\) counting is not this table.

### Zero fibre of the interior map

**EXACT — HUMAN PROOF** (`BTR-x2-C-interior`). Write \(P_m\) for packed
length-\(m\) prefixes and, for \(r<m\),

\[
C_{x^2}(m,r)
=
\bigl\lvert
\bigl\{
\bigl(p\bmod 3^r,\,\mathrm{DZ}^m(p^2)\bmod 3^r\bigr)
:
p\in P_m
\bigr\}
\bigr\rvert.
\]

Restrict to the fibre \(p\equiv 0\pmod{3^r}\).

*Width \(m=2r\).* Every such \(p\) is \(p=t\,3^r\) with \(t\in P_r\).
Then \(p^2=t^2 3^{2r}\) has balanced remainder \(0\) at depth \(2r\), so
\(\mathrm{DZ}^{2r}(p^2)=t^2\). As \(t\) runs through all residues modulo
\(3^r\), the second coordinate runs exactly over the quadratic residues
in \(\mathbb Z/3^r\mathbb Z\). Distinct units \(1\not\equiv -1\pmod{3^r}\)
have the same square, so that fibre misses at least one class, and

\[
C_{x^2}(2r,r)<3^{2r}\qquad(r\ge 1).
\]

In particular the coefficient cap is not attained at extra width \(r\).
(This is the interior cell \(r=2\), \(m=4\) in the table, and also the
superdiagonal cell \(r=1\), \(m=2\).)

*Width \(m\ge 3r\).* For each \(v\in P_r\) the prefix
\(p=3^r+v\,3^{m-r}\) lies in \(P_m\) and is \(0\pmod{3^r}\). Writing
\(t=1+v\,3^{m-2r}\) one has \(p=t\,3^r\) and

\[
t^2=1+3^{m-2r}\bigl(2v+v^2 3^{m-2r}\bigr),
\]

so \(\mathrm{DZ}^{m-2r}(t^2)=2v+v^2 3^{m-2r}\) with remainder \(1\). Thus
\(\mathrm{DZ}^m(p^2)\equiv 2v\pmod{3^r}\) once \(m-2r\ge r\). The unit
\(2\) makes \(v\mapsto 2v\) bijective on \(\mathbb Z/3^r\mathbb Z\). The
zero fibre is therefore the full second coordinate for every \(m\ge 3r\).

This is not a closed form for \(C_{x^2}(m,r)\): it decides one fibre.

### Every fibre of the interior map

**EXACT — HUMAN PROOF** (`BTR-x2-C-fibre-fill`). For \(r\ge 1\) and
every \(m\ge 5r\), every fibre \(p\equiv\alpha\pmod{3^r}\) has second
coordinate all of \(\mathbb Z/3^r\mathbb Z\). In particular no fibre
stays incomplete for all \(m\).

*Construction.* Let \(\alpha,u\in P_r\) and
\(p=\alpha+u\,3^r+3^{m-r}\). Then
\(\lvert p\rvert\le(3^{2r}-1)/2+3^{m-r}\le(3^m-1)/2\), so \(p\in P_m\),
and \(p\equiv\alpha\pmod{3^r}\). Write \(q=\alpha+u\,3^r\in P_{2r}\), so
\(p=q+3^{m-r}\) and

\[
p^2=q^2+(2q+3^{m-r})\,3^{m-r}.
\]

The identity \(\mathrm{DZ}^k(a+b\,3^k)=\mathrm{DZ}^k(a)+b\) gives
\(\mathrm{DZ}^{m-r}(p^2)=\mathrm{DZ}^{m-r}(q^2)+2q+3^{m-r}\). For
\(m\ge 5r\) one has \(m-r\ge 4r\) and

\[
\lvert q^2\rvert\le\frac{(3^{2r}-1)^2}{4}=\frac{3^{4r}-2\cdot 3^{2r}+1}{4}
<\frac{3^{4r}-1}{2}\le\frac{3^{m-r}-1}{2},
\]

so \(\mathrm{DZ}^{m-r}(q^2)=0\). Thus
\(\mathrm{DZ}^{m-r}(p^2)=2q+3^{m-r}\). A second application, using
\(m-r\ge r\), yields

\[
\mathrm{DZ}^m(p^2)
=\mathrm{DZ}^r(2\alpha+2u\,3^r+3^{m-r})
=\mathrm{DZ}^r(2\alpha)+2u+3^{m-2r}.
\]

Since \(m-2r\ge 3r\ge r\), one has
\(\mathrm{DZ}^m(p^2)\equiv 2u+\mathrm{DZ}^r(2\alpha)\pmod{3^r}\). The
unit \(2\) makes \(u\mapsto 2u+\mathrm{DZ}^r(2\alpha)\) bijective on
\(\mathbb Z/3^r\mathbb Z\). ∎

The identity \(\mathrm{DZ}^k(a+b\,3^k)=\mathrm{DZ}^k(a)+b\) is the
balanced-quotient form of uniqueness of the remainder in
\([-(3^k-1)/2,(3^k-1)/2]\).

This is not a first-saturation time: \(m_{\mathrm{sat}}(r)<5r\) in the
table below, and already \(C_{x^2}(3,1)=9\) while \(5r=5\). It is not
the zero-fibre \(m=3r\) construction (that uses a varying high block
\(v\) at \(\alpha=0\)). A single fixed high trit \(v=1\) does *not*
fill every fibre at \(m=3r\), nor at \(m=5r-1\); the vanishing
\(\mathrm{DZ}^{m-r}(q^2)=0\) used above starts at extra width \(4r\).

**COMPUTATIONALLY VERIFIED** for \(r\le 3\): every fibre is already
full at \(m=3r\) (and at the observed \(m_{\mathrm{sat}}(r)\)). This is
not a proof of fill at \(3r\).

### Full saturation table (not a proved \(m_0(r)\))

**COMPUTATIONALLY VERIFIED** for \(r\le 6\). Let \(m_{\mathrm{sat}}(r)\)
be the least \(m\) with \(C_{x^2}(m,r)=3^{2r}\). Exact integer images
give

```text
r                 1  2  3   4   5   6
m_sat(r)          3  6  8  10  13  15
3r                3  6  9  12  15  18
C(m_sat-1, r)     6 77 711 6271 59039 531401
```

The count stays at the cap for several further \(m\) (through \(m=9\)
for \(r\le 2\), \(m=12\) for \(r=4\), \(m=16\) for \(r=6\)). The guess
\(m_0(r)=3r\) is an upper bound in this range and is **not** the first
saturation time for \(r\ge 3\). The alternatives \(2r+1\) and \(2r+2\)
fail as well (\(C(12,5)=59039<59049\), \(C(14,6)=531401<531441\)).

A single fixed low block \(u\) of \(t=u+v 3^r\), varying only \(v\in P_r\),
fills only a few fibres at \(m=3r\) (the zero fibre and a handful of
neighbours). The proved filling family for a general fibre at \(m\ge 5r\)
varies the low block \(u\) with high trit \(v=1\). No collision family
blocking \(3^{2r}\) for all large \(m\) appeared.

### Literature classification

- `KNOWN`: \(C_x=1\); unrestricted \(x^2\) infinite-state;
  \(C_{x^2}(m,r)=3^m\) for \(r\ge m\) as same-depth layer injectivity of
  \(M_k(x^2)\); the set of squares in \(\mathbb Z/3^r\mathbb Z\) is
  smaller than \(3^r\).
- `REPARAMETERIZATION`: none of the surviving new statements.
- `PROJECT-SPECIFIC`: the superdiagonal law \(C_{x^2}(m,m-1)=3^m-3\)
  with the three constant-trit doubletons; the two-parameter census as
  a measurement distinct from the safety table; the zero-fibre law at
  \(m=2r\) and \(m\ge 3r\); every fibre full for \(m\ge 5r\).
- `OPEN`: the full interior count \(C_{x^2}(m,r)\), including a proved
  first-saturation time \(m_{\mathrm{sat}}(r)\) and fill at \(m=3r\)
  for a general fibre.

## Open questions

The fill law \(m\ge 5r\) is proved. Remaining: the exact first time
each fibre fills (computationally \(\le 3r\) for \(r\le 3\), and
\(\le m_{\mathrm{sat}}(r)\) for the product), or a closed form for
\(C_{x^2}(m,r)\) itself. Do not reopen the safety gate or cubic
\(M_k(x^3)\).

Section entropy versus dynamical entropy, and solenoid / adelic
packaging, remain unopened pending ideas of the safety gate. They are
not this gate.

## Decision

`PROMOTE`. Every fibre \(p\equiv\alpha\pmod{3^r}\) of the interior map
is full for all \(m\ge 5r\), by the explicit prefixes
\(p=\alpha+u\,3^r+3^{m-r}\) giving
\(\mathrm{DZ}^m(p^2)\equiv 2u+\mathrm{DZ}^r(2\alpha)\pmod{3^r}\)
(`BTR-x2-C-fibre-fill`). The alternative that some \(\alpha\) has a
3-adic square/valuation obstruction keeping the fibre incomplete for
all \(m\) is false. The threshold \(5r\) is not the first saturation
time of \(C_{x^2}(m,r)\) and is not the zero-fibre \(3r\) law; a single
fixed high trit at \(m=3r\) does not fill every fibre. Band and
zero-fibre rows are unretagged. The branch is not an Ahmed–Savchuk
restatement, not a safety reparameterization, and not a cubic-stratum
reopen. No CLI, Lean, or numbered milestone is added.

Best next question: prove that every fibre is already full for all
\(m\ge 3r\) (as the \(r\le 3\) census suggests), or name the exact
first filling time per fibre.

## Publication assessment

Status: `STRUCTURAL`.

The superdiagonal collision family, the zero-fibre square/construction
law, and the every-fibre fill at \(m\ge 5r\) are exact and short. They
classify the fibres of the interior map, not \(C_F\) for all \(F\) and
all \((m,r)\). The first-saturation time of the product remains a
table.
