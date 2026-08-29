---
title: Parity equidistribution of nested floor powers, with descent applications to the Juggler map
author: Philippe Cochin
date: 29 August 2026
subtitle: Working draft. Not submitted.
---

## Abstract

For odd \(n\) set \(m=\lfloor n^{3/2}\rfloor\), \(v=\lfloor m^{3/2}\rfloor\),
and so on: the integer chains obtained by iterating \(x\mapsto\lfloor
x^{3/2}\rfloor\) and \(x\mapsto\lfloor\sqrt x\rfloor\) in a prescribed
pattern. We prove parity equidistribution, with power savings, for every
pattern of depth at most four, and for selected deeper patterns. The
obstacle at depth two and beyond is that the naive expansion of
\(m^{3/2}\) leaves the sawtooth \(\{n^{3/2}\}\) with an amplitude that
grows like \(n^{3/4}\), which defeats the classical van der Corput
method. Two devices remove it. An *exact linearization* kills the inner
floor identically — \(m^{3/2}=\tfrac32mn^{3/4}-\tfrac12n^{9/4}+O(n^{-3/4})\)
with a one-signed remainder — so that the non-smooth integer \(m\)
enters the phase linearly with a smooth coefficient. Deeper patterns
then funnel into a single *kernel*: the exponential sum of the level-2
floor defect \(\{\lfloor n^{3/2}\rfloor^{3/2}\}\) against smooth weights
of scale \(n^{9/8}\). The central result (Theorem 5.3) is a power-saving
bound for that kernel, \(K_c\ll P^{1-1/96+\varepsilon}\), by double Weyl
differencing over an exact carry-branch decomposition and master
identity, with a targeted third differencing for the exact level-2 wave
pieces (Lemma 5.2).

The sequences arise as the itineraries of the Juggler map
\(J(n)=\lfloor\sqrt n\rfloor\) (\(n\) even), \(\lfloor n^{3/2}\rfloor\)
(\(n\) odd), whose finite exact theory is developed in a companion
manuscript [22]. As corollaries, the classes of starts carrying a
uniform power-envelope descent certificate of length at most four,
five, seven, and eight have natural densities \(13/16\), \(7/8\),
\(57/64\), and \(29/32\); an unconditional counting argument shows that
parity equidistribution at *all* depths would give density one to the
set of starts with some finite descent certificate. None of these is a
density of starts that reach \(1\), and no statement about the Juggler
conjecture itself is claimed. The remaining obstacle is the level-3
kernel, where the weight scale \(n^{27/16}\) exceeds \(n\); we state it
as an open problem, prove an almost-every-shift form of its model, and
record precisely what blocks the deterministic case.

## 1. Introduction

Equidistribution questions for a *single* floor of a smooth function —
the Piatetski–Shapiro tradition — are classical and well developed.
This paper concerns the *composition* of floors:
\[
m=\lfloor n^{3/2}\rfloor,\qquad
v=\lfloor m^{3/2}\rfloor,\qquad
w=\lfloor m^{1/2}\rfloor,\qquad
z=\lfloor v^{3/2}\rfloor,\ \ldots
\]
and, specifically, the joint distribution of the *parities* along such
chains. Fix a pattern (an *itinerary word*) \(w_1w_2\cdots w_d\) over
the alphabet \(\{E,O\}\), where an \(O\) applies
\(x\mapsto\lfloor x^{3/2}\rfloor\) and an \(E\) applies
\(x\mapsto\lfloor\sqrt x\rfloor\). The question is whether the \(2^d\)
parity classes of the resulting chain equidistribute over odd starts
\(n\le N\), with a power saving.

The difficulty is genuinely one of composition. Writing
\(\theta=\{n^{3/2}\}\), the naive expansion
\(m^{3/2}=n^{9/4}-\tfrac32\theta n^{3/4}+O(n^{-3/4})\) leaves a
sawtooth of *growing* amplitude \(n^{3/4}\) inside the phase. No
estimate for exponential sums with smooth monomial phases applies; the
phase is not smooth, and the sawtooth cannot be discarded. All results
in the single-floor literature stop before this point (Section 2).

Two ideas carry the paper.

1. **Exact linearization** (Lemma 4.3). The identity
   \(m^{3/2}=\tfrac32mn^{3/4}-\tfrac12n^{9/4}+E(n)\) with
   \(0\le E(n)\le\tfrac12n^{-3/4}\) eliminates the inner floor
   *exactly*: the integer \(m\) enters linearly, multiplied by a smooth
   coefficient, and the only non-smooth object left is \(m\) itself,
   which is handled by differencing and by an exact gap-cell
   decomposition. This device, iterated along the chain with one-signed
   Taylor remainders at every level, is what makes depth \(\ge2\)
   accessible.

2. **The kernel theorem** (Theorem 5.3). Every reorganization of the
   depth-4 pattern \(OOO*\) funnels into one object, the exponential
   sum of the level-2 floor defect
   \[
   K_c(P)=\sum_{\substack{n\sim P\\ n\ \mathrm{odd}}}
   e\bigl(c(n)\,\{\lfloor n^{3/2}\rfloor^{3/2}\}\bigr),
   \qquad c\asymp kP^{9/8}.
   \]
   We prove \(K_c(P)\ll P^{1-1/96+\varepsilon}\), uniformly for
   \(k\le P^{1/24}\), by double Weyl differencing over an exact
   carry-branch decomposition and master identity (Lemma 5.1), with a
   targeted third differencing for the level-2 wave pieces
   (Lemma 5.2). This is the hardest result of the paper, and
   Section 5 is written at full length — every estimate displayed
   with its constant — so that it can be checked without reference to
   anything outside this manuscript.

With the kernel theorem, depth-4 parity equidistribution is complete
(Theorem 6.1), and the same engine counts selected contracting
patterns of lengths five, seven, and eight (Theorems 6.2–6.4).

The chains are not chosen at random: they are the itineraries of the
Juggler map
\[
J(n)=
\begin{cases}
\lfloor\sqrt n\rfloor,&n\ \text{even},\\
\lfloor n^{3/2}\rfloor,&n\ \text{odd},
\end{cases}
\]
introduced by Pickover [1] (OEIS A094683 [2]); universal arrival at
\(1\) is open. The map is niche; the nested-floor sums must stand on
their own, and the paper is organized so that they do. The exact
finite-word calculus of \(J\) — the power envelope
\(J^{|w|}(n)^{2^{|w|}}\le n^{3^{\#O(w)}}\), the defect identity, and a
small-cycle census — is a companion manuscript [22]; here we import
only the contraction criterion (Proposition 3.1). The dynamical payoff
of the counting theorems is a sequence of *certified-descent
densities*: the set of starts guaranteed to drop below their starting
value within four, five, seven, eight steps has natural density
\(13/16\), \(7/8\), \(57/64\), \(29/32\) (Corollaries 4.9 and 6.5),
and equidistribution at all depths would give the set of starts with
*some* finite descent certificate density one (Proposition 7.1). We
state plainly what these corollaries are not: they are not densities
of starts that reach \(1\), and they do not touch the Juggler
conjecture, whose analogue of Terras's almost-all theorem for Collatz
[4, 5, 6] remains open.

Section 7 states the frontier precisely. One nesting deeper, the same
kernel reappears with weight scale \(n^{27/16}>n\) (Conjecture 7.3),
and every method of this paper stops below that scale. What survives
is a clean model problem — the amplitude-product sums
\(\sum e(A(t)\{B(t)\})\) with \(1\ll A'\ll A\) — for which we prove
two-sided square-root cancellation for almost every shift of the
fractional argument (Theorem 7.4), by direct integration and with no
harmonic analysis; the deterministic instance (Conjecture 7.5) is
open, and we record in three sentences why the obvious shortcuts
fail.

### 1.1 Verification and evidence conventions

Every theorem in this paper is an ordinary human proof from the stated
classical inequalities; none is machine-checked. The exact floor
identities beneath the analysis — the parity bridge
\(\lfloor x\rfloor\) odd iff \(\{x/2\}\ge1/2\), the gap-cell identity,
and the double-gap identity used by the kernel theorem — are
formalized in Lean in the companion repository
(`floor_odd_iff_half_le_fract_half`, `floor_gap_eq_carry`,
`seq_floor_gap`, `seq_floor_gap_second`), as are the finite-word
theorems of the companion manuscript [22]. Scaled-integer validations
of the linearization identities exist in the same repository; they are
checks, not proofs, and no numerical computation is used as a step in
any proof below. Densities of certificate classes are never densities
of starts that reach \(1\).

## 2. Related work

**Single floors.** The distribution of \(\lfloor n^c\rfloor\)
(\(c>1\), \(c\notin\mathbb N\)) in arithmetic progressions and among
primes goes back to Piatetski–Shapiro [12]; Leitmann [13] treated
general smooth \(\lfloor f(n)\rfloor\), and the prime exponent for
\(\lfloor n^c\rfloor\) has a long refinement history, e.g.
Rivat–Sargos [14] and Rivat–Wu [15]. All of these concern a single
floor of a smooth function; the analytic core is an exponential sum
with smooth monomial phase, estimated by van der Corput's method in
the form presented by Graham–Kolesnik [11].

**Digital and parity properties of \(\lfloor n^c\rfloor\).**
Mauduit–Rivat [16] established \(q\)-multiplicative equidistribution
along \(\lfloor n^c\rfloor\) for \(c\) in an explicit range, and
Morgenbesser [17] proved the analogous statements for the sum of
digits of \(\lfloor n^c\rfloor\) in residue classes. Parity of
\(\lfloor n^{3/2}\rfloor\) — our depth-1 statement, Theorem 4.1 — is
the simplest instance of this circle and is classical; we include the
short proof to fix constants and notation.

**Arithmetic of Piatetski–Shapiro sequences.** Baker, Banks, Brüdern,
Shparlinski, and Weingartner [18] study squarefree values, prime
factors, and Carmichael numbers along \(\lfloor n^c\rfloor\);
Glasscock [21] studies linear equations whose unknowns range over
Piatetski–Shapiro sequences. These results intersect a
Piatetski–Shapiro sequence with other arithmetic sets; none composes
two floors.

**Beatty sequences.** For the linear case \(\lfloor\alpha n\rfloor\)
the discrepancy theory is governed by the continued fraction of
\(\alpha\) (three-distance/Ostrowski structure); see Abercrombie [19]
and, for character sums along Beatty sequences, Banks–Shparlinski
[20]. The linear case admits exact self-similar structure that the
convex case \(n^{3/2}\) does not.

**What is not covered.** We know of no published equidistribution or
parity result for *nested* floor powers
\(\lfloor\lfloor n^{c}\rfloor^{d}\rfloor\) with \(c,d>1\), nor any
treatment of the level-2 defect sums \(K_c(P)\) of Section 5. The
obstruction is structural, not incremental: after one floor the
argument of the second floor is an integer sequence, not a smooth
function, and its fractional defect enters later phases with growing
amplitude. The exact-linearization device of Lemma 4.3 and the
carry-branch decomposition of Lemma 5.1 are, to our knowledge, new.
A literature check was last refreshed in August 2026; we would welcome
pointers to anything missed.

**Dynamical context.** For the Collatz map, Terras [4] and Everett [5]
proved that almost every start has finite stopping time, and Tao [6]
proved that almost all orbits attain almost bounded values. These are
methodological cousins — density statements through parity-word
counting — and motivate Proposition 7.1; they prove nothing about
\(J\), whose branches are floor powers rather than affine maps.
Prasad–Prasad [7] estimate excursion constants for juggler-like random
walks; we use that comparison only descriptively.

## 3. Preliminaries

Throughout, \(n\) denotes an odd integer, \(e(t)=e^{2\pi it}\),
\(\{x\}\) the fractional part, and \(\psi(x)=(-1)^{\lfloor x\rfloor}\).
On a dyadic block \(n\in(P,2P]\) we write \(n\sim P\). For the chains,
\[
X=n^{3/2},\quad m=\lfloor X\rfloor,\quad \theta=X-m;\qquad
Y=m^{3/2},\quad v=\lfloor Y\rfloor,\quad \theta_2=Y-v;
\]
and on even \(m\), \(U=m^{1/2}\), \(w=\lfloor U\rfloor\),
\(\theta_w=U-w\). An itinerary word of depth \(d\) at \(n\) is the
sequence of parities \(\mathrm{word}_d(n)\) of
\(n,J(n),\ldots,J^{d-1}(n)\).

**Proposition 3.1 (power-envelope contraction; companion [22]).**
If the word \(w\) is realized at \(n\ge2\) (the orbit's parities are
the letters of \(w\)) and \(3^{\#O(w)}<2^{|w|}\), then
\(J^{|w|}(n)<n\).

*Proof.* Induction along the word gives
\(J^{|w|}(n)^{2^{|w|}}\le n^{3^{\#O(w)}}\): an even letter squares to
at most the state, an odd letter squares to at most the cube. The
exponent gap and \(n\ge2\) force \(J^{|w|}(n)^{2^{|w|}}<n^{2^{|w|}}\).
(Lean: `power_bound_word`, `power_bound_contracts` in the companion
repository.) \(\square\)

A word \(w\) with \(3^{\#O(w)}<2^{|w|}\) is *contracting*; realizing a
contracting word is a *descent certificate* of length \(|w|\).
Contracting words used below: \(E\), \(OE\), \(OOEE\), \(OOOEE\),
\(OOEOE\), \(OOEOOEE\), \(OOOEOEE\), and the length-8 quartet of
Theorem 6.4. Every even start realizes \(E\), and every odd start with
even image realizes \(OE\); those two certificates cover all starts
except the odd-to-odd class, which is where the counting problem
lives.

**Lemma 3.2 (parity bridge).**
\(\lfloor x\rfloor\) is odd if and only if \(\{x/2\}\ge\tfrac12\).
(Lean: `floor_odd_iff_half_le_fract_half`.)

*Proof.* Write \(x=\lfloor x\rfloor+\{x\}\) and split by the parity of
\(\lfloor x\rfloor\). \(\square\)

**Lemma 3.3 (van der Corput, second-derivative form [11]).**
Let \(f\) be twice differentiable on an interval of length \(M\), with
\(\lambda\le|f''|\le\alpha\lambda\) for some \(\alpha\ge1\). Then
\[
\Bigl|\sum e(f)\Bigr|\ll_\alpha M\lambda^{1/2}+\lambda^{-1/2},
\]
the sum over the integers of the interval.

**Lemma 3.4 (Erdős–Turán [8]).**
The discrepancy of \(R\) points \(x_j\in\mathbb R/\mathbb Z\) against
an interval satisfies, for every \(H\ge1\),
\[
D\ll\frac RH+\sum_{h=1}^H\frac1h\Bigl|\sum_{j\le R}e(hx_j)\Bigr|.
\]

**Lemma 3.5 (Vaaler [10]).**
For every \(J\ge1\) there are trigonometric polynomials
\(V_J(t)=\sum_{0<|q|\le J}a_qe(qt)\) with
\(|a_q|\le\min(1,\tfrac2{|q|})\) and a nonnegative trigonometric
polynomial \(\Delta_J\ge0\) of degree \(J\) with constant term and
coefficients \(O(1/J)\), such that the period-2 square wave satisfies
\(\psi(x)=V_J(x/2)+O(\Delta_J(x/2))\). For products,
\(|\psi_1\psi_2-V^{(1)}V^{(2)}|\le\Delta^{(1)}+\Delta^{(2)}
+\Delta^{(1)}\Delta^{(2)}\), and each error term is again a
nonnegative trigonometric polynomial of the same shape.

The class indicators below are products of half-wave factors
\(\tfrac12(1\pm\psi)\) evaluated along *formal* chains — chains whose
branches are dictated by the target word, not by the orbit. The next
lemma is the exact identity that justifies this; it replaces any
appeal to sampled verification.

**Lemma 3.6 (branch consistency).**
Let \(d\ge1\) and let \(w=w_1\cdots w_d\) be a word with \(w_1=O\).
For odd \(n\), define the formal chain \(x_1=n\) and, for
\(1\le t<d\),
\[
\xi_t=
\begin{cases}
x_t^{3/2},&w_t=O,\\
x_t^{1/2},&w_t=E,
\end{cases}
\qquad
x_{t+1}=\lfloor\xi_t\rfloor,
\]
and set \(\sigma_t=+1\) if \(w_t=E\), \(\sigma_t=-1\) if \(w_t=O\).
Then, for every odd \(n\),
\[
\prod_{t=1}^{d-1}\tfrac12\bigl(1+\sigma_{t+1}\,\psi(\xi_t)\bigr)
=\bigl[\mathrm{word}_d(n)=w\bigr].
\]

*Proof.* Induct on \(d\). For \(d=1\) both sides are \(1\). Let
\(\Pi_{d-1}\) be the product over \(t\le d-2\); by induction
\(\Pi_{d-1}=[\mathrm{word}_{d-1}(n)=w_1\cdots w_{d-1}]\). If
\(\Pi_{d-1}=0\), both sides vanish, since every factor lies in
\([0,1]\). If \(\Pi_{d-1}=1\), then the orbit realizes
\(w_1\cdots w_{d-1}\), and a second induction along the chain gives
\(x_t=J^{t-1}(n)\) for \(t\le d-1\): assuming \(x_t=J^{t-1}(n)\), the
true parity of \(x_t\) is \(w_t\), so \(J\) applies exactly the
\(w_t\)-branch and \(J^t(n)=\lfloor\xi_t\rfloor=x_{t+1}\). Hence
\(\xi_{d-1}\) is the true real image with
\(\lfloor\xi_{d-1}\rfloor=J^{d-1}(n)\), and the last factor
\(\tfrac12(1+\sigma_d\psi(\xi_{d-1}))\) equals \(1\) exactly when the
parity of \(J^{d-1}(n)\) is \(w_d\), else \(0\). \(\square\)

Each \(\psi(\xi_t)\) is defined for *every* odd \(n\), which is what
permits the unconditional Vaaler expansion of the product: off the
cylinder, the vanishing of an earlier factor kills the term, and on
the cylinder every factor computes the true letter.

The last three preliminaries are the remaining analytic tools of
Section 5: the third-derivative test, a finite Fourier expansion for
sawtooth phases whose coefficient may exceed \(1\), and a
second/third-derivative test for two-term monomial phases that is
applied where two curvature scales can collide.

**Lemma 3.7 (van der Corput, third-derivative form [11, Thm. 2.6]).**
Let \(f\) be three times differentiable on an interval of length
\(M\), with \(\lambda_3\le|f'''|\le\alpha\lambda_3\). Then
\[
\Bigl|\sum e(f)\Bigr|\ll_\alpha M\lambda_3^{1/6}+M^{1/2}\lambda_3^{-1/6},
\]
the sum over the integers of the interval.

**Lemma 3.8 (finite Fourier expansion with a shifted window).**
Let \(B\in\mathbb R\), and let \(T,J\) be integers with \(J\ge1\) and
\(T\ge8(1+|B|)\). There exist coefficients \((b_u)_{|u|\le T}\) with
\[
|b_u|\le\min\Bigl(2,\tfrac1{\pi|u+B|}\Bigr)
+\min\Bigl(2,\tfrac1{\pi|u|}\Bigr),
\qquad
\sum_{|u|\le T}|b_u|\ll\log(2+|B|),
\]
and coefficients \((v_q)_{0<|q|\le J}\) with
\(|v_q|\le\min(2,2\pi|B|)/|q|\), such that for every \(t\in\mathbb R\)
\[
\Bigl|e(-B\{t\})-\sum_{|u|\le T}b_ue(ut)
-\sum_{0<|q|\le J}v_qe(qt)\Bigr|
\le\min(2,2\pi|B|)\,\Delta_J(t)+\frac{8(1+|B|)}T,
\]
where \(\Delta_J\ge0\) is a trigonometric polynomial of degree \(J\)
with constant term and coefficients at most \(1/(J+1)\).

*Proof.* Write \(f(t)=e(-B\{t\})\) and
\(\sigma(t)=\tfrac12-\{t\}\), the sawtooth with jump \(+1\) at the
integers. The jump of \(f\) at the integers is \(1-e(-B)\), so
\(g:=f-(1-e(-B))\,\sigma\) is continuous, \(1\)-periodic, and
piecewise \(C^1\). Its Fourier coefficients are, for \(u\ne0\),
\[
\hat g(u)=\frac{1-e(-B)}{2\pi i}
\Bigl(\frac1{u+B}-\frac1u\Bigr)
=-\frac{(1-e(-B))\,B}{2\pi i\,u(u+B)},
\qquad
|\hat g(u)|\le\frac{\min(2,2\pi|B|)}{2\pi}\,\frac{|B|}{|u||u+B|},
\]
together with \(|\hat g(0)|\le1\); in particular
\(|\hat g(u)|\le\min(2,\tfrac1{\pi|u+B|})+\min(2,\tfrac1{\pi|u|})\)
and, by partial fractions,
\(\sum_u|\hat g(u)|\ll\log(2+|B|)\): the series converges absolutely,
so \(g\) equals its Fourier series everywhere, and the tail beyond
\(|u|\le T\ge8(1+|B|)\) satisfies (using \(|u+B|\ge|u|/2\) there)
\[
\sum_{|u|>T}|\hat g(u)|
\le\frac{2|B|}{\pi}\sum_{|u|>T}\frac1{u^2}\cdot2
\le\frac{8|B|}{\pi T}\le\frac{8(1+|B|)}T .
\]
Take \(b_u=\hat g(u)\). For the sawtooth part, Vaaler's theorem in
its original form [10] provides a trigonometric polynomial
\(V^*_J(t)=\sum_{0<|q|\le J}a^*_qe(qt)\) with \(|a^*_q|\ll1/|q|\) and
\(|\sigma(t)-V^*_J(t)|\le\Delta_J(t)\) with \(\Delta_J\) as stated;
multiply by \(1-e(-B)\), whose modulus is
\(2|\sin\pi B|\le\min(2,2\pi|B|)\), and set
\(v_q=(1-e(-B))a^*_q\). \(\square\)

When the lemma is applied with \(t=G(n)\) along a block, the
\(\Delta_J\)-term is a nonnegative majorant: its sum over the block
is \(P/(J+1)\) plus \(J\)-truncated mode sums of \(G\) with
coefficients \(\le1/(J+1)\), and the flat term contributes
\(8(1+|B|)P/T\). Both costs are displayed at each application below.

**Lemma 3.9 (two-term monomial test).**
Let \(E\subset\mathbb Q\cap[-4,4]\) be a fixed finite set disjoint
from \(\{0,1,2,3\}\), let \(\alpha\ne\beta\) lie in \(E\), let
\(I\subseteq(P,2P]\), and let
\[
f(n)=a\,n^\alpha+b\,n^\beta+g(n),
\qquad
M:=\max\bigl(|a|P^{\alpha-2},\,|b|P^{\beta-2}\bigr)\le1,
\quad ab\neq0,
\]
where the perturbation satisfies, for every \(n\in I\),
\[
|g''(n)|\le\rho\,\bigl(|a|n^{\alpha-2}+|b|n^{\beta-2}\bigr),
\qquad
|g'''(n)|\le\rho\,\bigl(|a|n^{\alpha-3}+|b|n^{\beta-3}\bigr),
\]
with \(\rho\le\rho_0(E)\) sufficiently small in terms of \(E\) alone.
Then
\[
\Bigl|\sum_{n\in I}e(f(n))\Bigr|
\ll_E |I|\,M^{1/2}+M^{-1/2}
+|I|\,(M/P)^{1/6}+|I|^{1/2}\,(M/P)^{-1/6}.
\]

*Proof.* Write \(A(n)=a\,\alpha(\alpha-1)\,n^{\alpha-2}\) and
\(B(n)=b\,\beta(\beta-1)\,n^{\beta-2}\), so that
\[
f''=A+B+g'',
\qquad
n\,f'''=(\alpha-2)A+(\beta-2)B+n\,g''' .
\]
On the block, \(|A(n)|\asymp_E|a|P^{\alpha-2}\) and
\(|B(n)|\asymp_E|b|P^{\beta-2}\). The ratio
\(|A/B|=|a\alpha(\alpha-1)/(b\beta(\beta-1))|\,n^{\alpha-\beta}\) is
strictly monotone in \(n\), so for any threshold \(K=K(E)\ge3\) the
block splits into at most three consecutive intervals: \(I_1\) where
\(|A/B|\ge K\), \(I_2\) where \(|A/B|\le1/K\), and a middle
\(I_0\).

On \(I_1\): \(|f''|\ge(1-\tfrac1K)|A|-|g''|\ge\tfrac12|A|
\gg_EM\)-scale, with \(\sup|f''|/\inf|f''|\le C(E)\); Lemma 3.3
gives \(\ll_E |I|M^{1/2}+M^{-1/2}\). Symmetrically on \(I_2\).

On \(I_0\), \(|A|\asymp_K|B|\). If \(A\) and \(B\) have the same
sign there, \(|f''|\ge|A|+|B|-|g''|\ge|A|\) and Lemma 3.3 applies
as before. If they have opposite signs, write \(B=-sA\) with
\(s=s(n)\in[1/K,K]\), monotone in \(n\). Then
\[
f''=A\,(1-s)+g'',
\qquad
n\,f'''=A\,\bigl((\alpha-2)-s(\beta-2)\bigr)+n\,g''' .
\]
The two affine functions \(s\mapsto1-s\) and
\(s\mapsto(\alpha-2)-s(\beta-2)\) have distinct zeros: \(s=1\) and
\(s=(\alpha-2)/(\beta-2)\ne1\) (here \(\alpha\ne\beta\) and
\(\beta\ne2\) are used). Hence
\[
c_6(E):=\min_{s>0}\ \max\bigl(|1-s|,\;|(\alpha-2)-s(\beta-2)|\bigr)>0,
\]
so at every \(n\in I_0\) either \(|f''|\ge\tfrac12c_6|A|\) or
\(|n f'''|\ge\tfrac12c_6|A|\), after absorbing \(g\) by
\(\rho_0(E)\le c_6/8\). Since \(s(n)\) is monotone, the set where
\(|1-s(n)|\ge c_6\) is the complement of a single interval, so
\(I_0\) splits into at most three consecutive intervals, each either
entirely second-derivative-good (Lemma 3.3 at scale
\(\gg_EM\)-normalized: \(\ll |I|M^{1/2}+M^{-1/2}\)) or entirely
third-derivative-good (Lemma 3.7 at scale
\(|f'''|\gg_EM/P\)-normalized:
\(\ll |I|(M/P)^{1/6}+|I|^{1/2}(M/P)^{-1/6}\)).
Summing the \(O_E(1)\) contributions proves the lemma. \(\square\)

The proof's only content is that the second and third derivatives of
a two-term monomial phase cannot both be small on the same
subinterval — the linear system with matrix
\(\bigl(\begin{smallmatrix}1&1\\ \alpha-2&\beta-2\end{smallmatrix}\bigr)\)
is invertible — so the interval splits into boundedly many pieces on
which one of the two classical tests runs at full scale. All
applications in Section 5 use exponent pairs from
\(E=\{\tfrac34,\tfrac{11}8,\tfrac32,\tfrac{15}8\}\). One corner of
Section 5 (three curvature scales meeting on a zero-offset branch)
needs the three-term extension, with the fourth-derivative test as
the final fallback.

**Lemma 3.10 (three-term monomial test).**
Let \(E\) be as in Lemma 3.9 and let \(\alpha,\beta,\gamma\in E\) be
pairwise distinct, \(I\subseteq(P,2P]\), and
\[
f(n)=a\,n^\alpha+b\,n^\beta+c\,n^\gamma+g(n),
\qquad
M:=\max\bigl(|a|P^{\alpha-2},|b|P^{\beta-2},|c|P^{\gamma-2}\bigr)
\le1,
\]
with \(abc\ne0\) and \(g\) satisfying the analogues of the
perturbation bounds of Lemma 3.9 for the second, third, *and fourth*
derivatives, at some \(\rho\le\rho_0(E)\). Then
\[
\Bigl|\sum_{n\in I}e(f(n))\Bigr|
\ll_E |I|\,M^{1/2}+M^{-1/2}
+|I|\,(M/P)^{1/6}+|I|^{1/2}\,(M/P)^{-1/6}
+|I|\,(M/P^2)^{1/14}+|I|^{3/4}\,(M/P^2)^{-1/14}.
\]

*Proof.* As in Lemma 3.9, with the \(2\times2\) system replaced by
the \(3\times3\) system
\[
f''=A+B+C+g'',\quad
nf'''=(\alpha{-}2)A+(\beta{-}2)B+(\gamma{-}2)C+ng''',
\]
\[
n^2f''''=(\alpha{-}2)(\alpha{-}3)A+(\beta{-}2)(\beta{-}3)B
+(\gamma{-}2)(\gamma{-}3)C+n^2g'''',
\]
where \(A,B,C\) are the three curvature terms. The coefficient
matrix is the Vandermonde-type matrix in the distinct values
\(\alpha{-}2,\beta{-}2,\gamma{-}2\) (rows \(1\), \(x\),
\(x(x{-}1)\)), hence invertible with inverse bounded in terms of
\(E\): at every point,
\(\max(|f''|,\,|nf'''|,\,|n^2f''''|)\ge c_7(E)\max(|A|,|B|,|C|)
\ge c_7(E)\,\tilde M\), \(\tilde M\asymp_EM\)-normalized, after
absorbing \(g\) by \(\rho_0\le c_7/8\). The ratios \(A/B\), \(B/C\),
\(A/C\) are monotone, so \(I\) splits into \(O_E(1)\) consecutive
intervals on each of which one fixed derivative order
\(r\in\{2,3,4\}\) is good at full scale; Lemma 3.3
(\(r=2\)), Lemma 3.7 (\(r=3\)), or the fourth-derivative test
[11, Thm. 2.6, \(k=4\)]
\(\bigl(\ll|I|\lambda_4^{1/14}+|I|^{3/4}\lambda_4^{-1/14}\) at
\(\lambda_4\asymp_EM/P^2\bigr)\) finishes each piece. \(\square\)

## 4. Exact linearization and depths one to four

For odd \(n\) write \(s(n)=\psi(n^{3/2})=(-1)^m\) and
\(S_O(N)=\sum_{n\le N,\ n\ \mathrm{odd}}s(n)\). Let \(M(N)\) be the
number of odd \(n\le N\) and
\(\operatorname{OO}(N)=\#\{n\le N:n\ \text{odd},\ J(n)\ \text{odd}\}\),
so \(S_O(N)=M(N)-2\operatorname{OO}(N)\). By Lemma 3.2, with
\(g(r)=\tfrac12(2r+1)^{3/2}\), \(s(2r+1)=-1\) iff
\(\{g(r)\}\ge\tfrac12\), and \(S_O(N)\) is (twice) an interval
discrepancy of the sequence \(\{g(r)\}\).

**Theorem 4.1 (depth one; classical).**
\(|S_O(N)|\ll N^{5/6}\).

*Proof.* This is the standard van der Corput estimate for the
monomial \(g\), included for completeness. \(g''(r)=\tfrac32
(2r+1)^{-1/2}\) is positive and decreasing. Partition \(1\le r<R\)
into dyadic blocks \([M,\min(2M,R))\); on a block
\(g''\asymp M^{-1/2}\), so for the \(h\)-th mode \(f=hg\) has
\(\lambda\asymp hM^{-1/2}\) and Lemma 3.3 gives
\(|\sum_{r\asymp M}e(hg(r))|\ll h^{1/2}M^{3/4}+h^{-1/2}M^{1/4}\).
Lemma 3.4 with \(H=\lfloor M^{1/6}\rfloor\) bounds the block's
discrepancy by \(\ll M^{5/6}\), and the dyadic sum is
\(O(R^{5/6})=O(N^{5/6})\). \(\square\)

**Corollary 4.2 (density of the odd-to-odd class).**
\(\bigl|\operatorname{OO}(N)-N/4\bigr|\ll N^{5/6}\). Equivalently,
the starts covered by the uniform one- or two-step certificates
(\(E\) and \(OE\)) have natural density \(3/4\).

This is a density of a certificate class, not of starts that reach
\(1\). Theorem 4.1 concerns consecutive source intervals; it supplies
no transfer theorem for orbit samples or sparse image sets, so it
cannot by itself control the odd-to-odd dynamics after the first step.
The rest of the paper does not transfer it; it attacks the nested sums
directly, by removing the inner floors exactly before any analytic
step.

**Lemma 4.3 (exact linearization and gap cells).**
(i) For every odd \(n\ge3\),
\[
m^{3/2}=\tfrac32\,m\,n^{3/4}-\tfrac12\,n^{9/4}+E(n),
\qquad
0\le E(n)\le\tfrac38\,(n^{3/2}-1)^{-1/2}\le\tfrac12\,n^{-3/4}.
\]
(ii) For \(h\ge1\) and odd \(n\), let \(g(n)=m(n+2h)-m(n)\) and
\(\delta(n)=(n+2h)^{3/2}-n^{3/2}\). Then
\[
g(n)=\lfloor\delta(n)\rfloor+\kappa(n),
\qquad
\kappa(n)=\bigl[\{n^{3/2}\}\ge1-\{\delta(n)\}\bigr]\in\{0,1\}.
\]

*Proof.* (i) Let \(f(t)=(X-t)^{3/2}\) on \([0,\theta]\), so
\(f(\theta)=m^{3/2}\). Taylor with Lagrange remainder at \(0\) gives
\(f(\theta)=X^{3/2}-\tfrac32X^{1/2}\theta
+\tfrac38(X-\xi)^{-1/2}\theta^2\) for some \(\xi\in(0,\theta)\).
Substituting \(\theta=X-m\) in the linear term yields
\(-\tfrac12X^{3/2}+\tfrac32mX^{1/2}=-\tfrac12n^{9/4}+\tfrac32mn^{3/4}\),
and the remainder lies in \([0,\tfrac38(X-1)^{-1/2}]\), with
\((X-1)^{-1/2}\le\tfrac43X^{-1/2}\) already for \(n\ge3\). (ii)
\(g=\lfloor X+\delta\rfloor-\lfloor X\rfloor
=\lfloor\delta\rfloor+\lfloor\{X\}+\{\delta\}\rfloor\), and the last
floor is \(1\) precisely when \(\{X\}+\{\delta\}\ge1\) (Lean:
`floor_gap_eq_carry`, `seq_floor_gap`). \(\square\)

The point of (i): the non-smooth integer \(m\) enters the phase
*linearly*, multiplied by a smooth coefficient; no fractional part of
growing amplitude survives. The naive expansion
\(m^{3/2}=n^{9/4}-\tfrac32\theta n^{3/4}+O(n^{-3/4})\) instead leaves
the sawtooth \(\theta\) with the growing amplitude \(n^{3/4}\), which
defeats the van der Corput method directly. For (ii), since
\(\delta\) is smooth and increasing with
\(\delta'\asymp hn^{-1/2}\), the level sets of
\(\lfloor\delta\rfloor\) partition a dyadic block \(n\in(P,2P]\) into
\(O(hP^{1/2})\) cells of length \(\asymp P^{1/2}/h\) on which the
integer part of the gap is constant.

**Theorem 4.4 (nested parity discrepancy).**
For every \(\varepsilon>0\) and every
\((a,b)\in\{0,1\}^2\setminus\{(0,0)\}\),
\[
\Bigl|\sum_{n\le N,\ n\ \mathrm{odd}}
\psi(n^{3/2})^{a}\,\psi(m(n)^{3/2})^{b}\Bigr|
\ll_\varepsilon N^{23/24+\varepsilon}.
\]
Consequently each of the four joint parity classes of
\((m,\lfloor m^{3/2}\rfloor)\) on odd \(n\le N\) has cardinality
\(\tfrac N8+O(N^{23/24+\varepsilon})\); in particular the odd-to-odd
cylinder refines one letter deeper than Theorem 4.1.

*Proof.* Work on dyadic blocks \(n\in(P,2P]\), odd, with truncations
\(J_1=J_2=P^{1/24}\) (wave modes), \(H=P^{1/12}\) (differencing), and
\(R=P^{1/4}\) (cell modes).

*Step 1 (wave expansion).* By Lemma 3.5 applied to each factor,
expanding both waves reduces the theorem to bounds, uniform in the
mode pair, for
\[
S_{\mu,\nu}(P)=\sum_{n\in(P,2P],\ n\ \mathrm{odd}}
e\bigl(\mu\,n^{3/2}+\nu\,m^{3/2}\bigr),
\qquad
|\mu|\le J_1,\ \tfrac12\le|\nu|\le J_2,
\]
with \(\mu,\nu\in\tfrac12\mathbb Z\); the pure first-factor majorant
sums are \(\ll P/J_1+P^{5/6+\varepsilon}\ll P^{23/24+\varepsilon}\) by
the depth-1 machinery, and mode weights sum to \(O(\log^2P)\). Write
\(i=2\mu\), \(j=2\nu\).

*Step 2 (linearization).* By Lemma 4.3(i), replacing
\(\tfrac j2m^{3/2}\) by \(\tfrac{3j}4mn^{3/4}-\tfrac j4n^{9/4}\)
changes \(S_{\mu,\nu}\) by at most
\(2\pi\tfrac j4\sum_{n\sim P}n^{-3/4}\ll jP^{1/4}\le P^{7/24}\).

*Step 3 (van der Corput A-process).* With \(H=P^{1/12}\),
\(|S_{\mu,\nu}|^2\le\tfrac{2P}H\sum_{0\le h<H}|T_h|\), where \(T_h\)
sums \(e(\Phi(n{+}2h)-\Phi(n))\) over the overlap and \(\Phi\) is the
linearized phase. The exact rewrite
\(m(n{+}2h)(n{+}2h)^{3/4}-m(n)n^{3/4}
=g(n)(n{+}2h)^{3/4}+m(n)[(n{+}2h)^{3/4}-n^{3/4}]\) with
\(m(n)=n^{3/2}-\theta_n\) gives
\[
\Phi(n{+}2h)-\Phi(n)=A_h(n)
+\tfrac{3j}4\,g(n)\,(n{+}2h)^{3/4}+O(jhP^{-1/4}),
\]
where \(A_h\) is smooth and the error is the
\(-\tfrac{3j}4\theta_n[(n{+}2h)^{3/4}-n^{3/4}]\) term. The two
\(n^{5/4}\)-scale contributions of \(A_h\) cancel at leading order,
leaving \(A_h''=\tfrac{81}{256}jh^2n^{-7/4}(1+o(1))\) plus an
\(i\)-part \(O(ihP^{-3/2})\), both \(o(jhP^{-3/4})\) in these ranges.

*Step 4 (cells).* Split \(T_h\) over the \(O(hP^{1/2})\) cells of
Lemma 4.3(ii). On a cell, \(g=G+\kappa\) with \(G\) constant and
\(\kappa(n)=[\{n^{3/2}\}\ge\rho(n)]\), \(\rho=1-\{\delta(n)\}\) smooth
and monotone there. Vaaler-expand \(\kappa\) with modes
\(e(rn^{3/2})\), \(0<|r|\le R\). The moving endpoint costs nothing:
since \(\rho(n)=1+G-\delta(n)\), the coefficient's \(n\)-dependent
piece contributes the exact smooth phase \(r\delta(n)\), and
\(e(rn^{3/2}+r\delta(n))=e(r(n{+}2h)^{3/2})\) up to a unimodular
constant. Every \(r\)-term therefore falls into one of the two smooth
families \(e(rn^{3/2})\), \(e(r(n{+}2h)^{3/2})\); the main term
\(\delta(n)-G\) has total variation exactly \(1\) per cell and is
absorbed by one Abel summation.

*Step 5 (second-derivative test per cell).* The remaining phases are
smooth. For the \(r=0\) parts,
\(|f''|\asymp\lambda_0=jhP^{-3/4}\) with a single sign and bounded
ratio across a cell; Lemma 3.3 on a cell of length
\(\ell\asymp P^{1/2}/h\) gives \(\ll\ell\lambda_0^{1/2}
+\lambda_0^{-1/2}\), hence over all cells
\(\ll(jh)^{1/2}P^{5/8}+j^{-1/2}h^{1/2}P^{7/8}\). For \(r\ne0\), the
curvature is dominated by the \(r\)-term \(\asymp|r|P^{-1/2}\) of
fixed sign (as \(jh\le P^{1/8}\ll P^{1/4}\)); the same test and the
\(1/|r|\) weights give \(\ll R^{1/2}P^{3/4}+hP^{3/4}\log P\), and the
majorant errors contribute \(O(P/R)=O(P^{3/4})\). In total
\(|T_h|\ll P^{7/8}(1+h^{1/2})\), uniformly in the modes.

*Step 6 (assembly).*
\(|S_{\mu,\nu}|^2\ll P^2/H+P^{15/8}H^{1/2}\ll P^{23/12}\) at
\(H=P^{1/12}\), so \(|S_{\mu,\nu}|\ll P^{23/24}\). Summing mode
weights, majorants, and dyadic blocks gives the theorem with
\(N^{23/24}\log^3N\). \(\square\)

The exponent \(23/24\) is deliberately unoptimized; every stage has
slack.

**Proposition 4.5 (OE-branch third letter).**
For \(a\in\{0,1\}\),
\[
\Bigl|\sum_{n\le N,\ n\ \mathrm{odd}}\bigl((-1)^m\bigr)^a\,
\psi\bigl(m^{1/2}\bigr)\Bigr|\ll_\varepsilon N^{7/8+\varepsilon},
\]
and consequently
\(\#\mathrm{OEO}(N),\ \#\mathrm{OEE}(N)=N/8+O(N^{7/8+\varepsilon})\).
Together with Theorem 4.4 this makes depth 3 complete: each of
\(OOO\), \(OOE\), \(OEO\), \(OEE\) has density \(1/8\) with a power
saving.

*Proof.* Taylor expansion of \((X-\theta)^{1/2}\) with both correction
terms one-signed gives
\[
m^{1/2}=n^{3/4}+D_1(n),
\qquad
-\tfrac12X^{-1/2}-\tfrac18(X-1)^{-3/2}\le D_1\le0 .
\]
\(D_1\) is decaying, so replacing \(\tfrac l2m^{1/2}\) by
\(\tfrac l2n^{3/4}\) inside a Vaaler mode costs
\(\ll l\sum_{n\sim P}n^{-3/4}\ll lP^{1/4}\), absorbable at
\(l\le2P^{1/24}\). The mode sums are then pure:
\(\sum_{n\sim P}e(\tfrac i2n^{3/2}+\tfrac l2n^{3/4})\) with
\(l\ne0\). For \(i\ne0\), \(\varphi''\asymp|i|P^{-1/2}\) is
single-signed and Lemma 3.3 gives
\(\ll i^{1/2}P^{3/4}+i^{-1/2}P^{1/4}\); for \(i=0\),
\(\varphi''\asymp lP^{-5/4}\) gives
\(\ll l^{1/2}P^{3/8}+l^{-1/2}P^{5/8}\). Vaaler majorants, truncation
tails, and dyadic assembly are as in Theorem 4.4, and every bound is
\(\ll P^{7/8}\) after summing mode weights. Branch consistency is
Lemma 3.6: the \((1+(-1)^m)/2\) factor vanishes exactly on odd \(m\),
where the true chain takes the \(3/2\)-power branch. \(\square\)

**Lemma 4.6 (fourth-letter linearization).**
For every odd \(n\ge3\),
\[
v^{1/2}=n^{9/8}+D(n),
\qquad
-\tfrac34\,n^{-3/8}-n^{-9/8}\le D(n)\le0 .
\]

*Proof.* Two applications of the Lemma 4.3(i) pattern. With
\(f(t)=(Y-t)^{1/2}\) on \([0,\theta_2]\):
\(v^{1/2}=m^{3/4}-\tfrac12\theta_2m^{-3/4}-E_2\),
\(0\le E_2\le\tfrac18(Y-1)^{-3/2}\). With \(f(t)=(X-t)^{3/4}\) on
\([0,\theta]\): \(m^{3/4}=n^{9/8}-\tfrac34\theta n^{-3/8}-E_3\),
\(0\le E_3\le\tfrac3{32}(X-1)^{-5/4}\). Every term is nonpositive
after the leading one, and
\(\tfrac12m^{-3/4}+E_3+E_2\le n^{-9/8}\) for \(n\ge3\). \(\square\)

Unlike the depth-2 layer, *every* non-smooth term now has decaying
amplitude: the cumulative phase cost of replacing
\(\tfrac k2v^{1/2}\) by the smooth \(\tfrac k2n^{9/8}\) over a dyadic
block is \(\ll kP^{5/8}\), negligible against the target.

**Theorem 4.7 (triple parity discrepancy).**
For every \(\varepsilon>0\) and every
\((a,b,c)\in\{0,1\}^3\setminus\{(0,0,0)\}\),
\[
\Bigl|\sum_{n\le N,\ n\ \mathrm{odd}}
\psi(n^{3/2})^{a}\,\psi(m^{3/2})^{b}\,\psi(v^{1/2})^{c}\Bigr|
\ll_\varepsilon N^{23/24+\varepsilon}.
\]
Consequently each of the eight sign classes of
\((\psi(n^{3/2}),\psi(m^{3/2}),\psi(v^{1/2}))\) on odd \(n\le N\) has
cardinality \(\tfrac N{16}+O(N^{23/24+\varepsilon})\).

*Proof.* The \(c=0\) cases are Theorem 4.4 and Theorem 4.1. For
\(c=1\), wave-expand all present sign factors as in Step 1 of
Theorem 4.4, with truncations \(J_1=J_2=J_3=P^{1/24}\), and bound
\[
S_{i,j,k}(P)=\sum_{n\in(P,2P],\ n\ \mathrm{odd}}
e\bigl(\tfrac i2n^{3/2}+\tfrac j2m^{3/2}+\tfrac k2v^{1/2}\bigr)
\]
uniformly for \(|i|\le2J_1\), \(|j|\le2J_2\), \(1\le|k|\le2J_3\). By
Lemma 4.6, replacing \(\tfrac k2v^{1/2}\) by \(\tfrac k2n^{9/8}\)
costs \(\ll|k|P^{5/8}\le P^{2/3}\), before any differencing.

If \(j=0\), the remaining sum is a single smooth exponential sum with
phase \(\tfrac i2n^{3/2}+\tfrac k2n^{9/8}\). Both curvature terms are
positive for positive modes, and for mixed signs with \(|i|\ge1\) the
first dominates by \(P^{3/8-1/24}\); Lemma 3.3 gives
\(\ll P^{5/8}\) for \(i=0\) and \(\ll|i|^{1/2}P^{3/4}+P^{1/4}\)
otherwise, both \(\ll P^{23/24}\).

If \(j\ne0\), the phase is exactly the Theorem 4.4 phase plus the
smooth passenger \(\tfrac k2n^{9/8}\). Steps 2–6 run verbatim; the
passenger modifies the smooth part of the differenced phase by
\(\tfrac k2[(n{+}2h)^{9/8}-n^{9/8}]\), whose second derivative
\(\ll|k|hP^{-15/8}\) is smaller than the retained cell curvature
\(jhP^{-3/4}\) and the \(r\)-mode curvature \(|r|P^{-1/2}\) by powers
of \(P\). Every sign-dominance check of Theorem 4.4 holds with these
margins. \(\square\)

**Theorem 4.8 (the OE\*\* splits).**
\[
\#\mathrm{OEOE}(N),\ \#\mathrm{OEOO}(N)
=\tfrac N{16}+O\bigl(N^{7/8+\varepsilon}\bigr),
\qquad
\#\mathrm{OEEE}(N),\ \#\mathrm{OEEO}(N)
=\tfrac N{16}+O\bigl(N^{13/16+\varepsilon}\bigr).
\]
Together with Theorems 4.4 and 4.7 this proves every depth-4
itinerary word class except \(OOO*\).

*Proof.* On the \(OE\) branch \(m\) is even and \(w=\lfloor
U\rfloor\), \(U=m^{1/2}\). The \(w\)-level linearization is Lemma
4.3(i) verbatim with base \(U\): since \(Um^{1/4}=m^{3/4}\) exactly,
\[
w^{3/2}=m^{3/4}-\tfrac32\,m^{1/4}\,\theta_w+E,
\qquad 0\le E\le\tfrac38(U-1)^{-1/2},
\]
and \(m^{3/4}=n^{9/8}\) up to one-signed corrections of scale
\(n^{-3/8}\). For a Vaaler mode \(k\ne0\), the phase is therefore
\(\varphi_1(n)-B(n)\theta_w(n)\) up to absorbable errors, with
\(\varphi_1=\tfrac i2n^{3/2}+\tfrac j2n^{3/4}+\tfrac k2n^{9/8}\) and
\(B=\tfrac{3k}4n^{3/8}(1+O(n^{-3/2}))\): a *single growing sawtooth*
of amplitude \(\asymp kn^{3/8}\) riding \(\theta_w=\{m^{1/2}\}\),
whose underlying integer increments once every \(\asymp\tfrac43
n^{1/4}\) steps. Truncations: \(J_1=J_2=J_3=P^{1/8}\).

*Drift-1 intervals.* \(B'\asymp kn^{-5/8}\), so \(B\) drifts by at
most \(1\) on intervals \(I\) of length \(L_0=P^{5/8}/k\); there are
\(\asymp kP^{3/8}\) of them. On \(I\), expand
\(e(-B\{U\})=\sum_ra_r(B)e(rU)\) (Fourier in \(U\), Vaaler truncation
\(|r+B|\le T=P^{5/16}\)); the coefficients satisfy
\(|a_r(B)|\le\min(1,|r+B|^{-1})\) with window mass \(O(\log T)\), and
their \(n\)-dependence through \(B(n)\) has total variation \(O(1)\)
per interval, removed by one partial summation per mode.

*Mode sums.* Smoothing \(rU\to rn^{3/4}\) costs \(kP^{5/8}\) in
total. Writing \(r=-B_0+t\), \(|t|\le T\), the curvature of the mode
phase is
\[
\varphi''=\tfrac{27k}{128}n^{-7/8}
-\tfrac3{16}\bigl(t+\tfrac j2\bigr)n^{-5/4}+\tfrac{3i}8n^{-1/2}.
\]
For \(i\ne0\) the last term dominates and Lemma 3.3 gives
\(\ll i^{1/2}P^{3/4}+i^{-1/2}kP^{5/8}\) after summing intervals. For
\(i=0\), \((T+J_2)P^{-5/4}\ll kP^{-7/8}\) because
\(T=P^{5/16}\ll kP^{3/8}\) for every \(k\ge1\), so
\(\lambda\asymp kn^{-7/8}\) is single-signed; Lemma 3.3 per
interval and summation over \(\asymp kP^{3/8}\) intervals give
\(S_k\ll k^{1/2}P^{13/16+\varepsilon}\). With Vaaler weights \(1/k\),
\(\sum_{k\le J_3}k^{-1/2}P^{13/16}=J_3^{1/2}P^{13/16}=P^{7/8}\),
balanced against the truncation error \(P/J_3=P^{7/8}\) at
\(J_3=P^{1/8}\). Total \(\ll P^{7/8+\varepsilon}\).

*OEE branch.* The fourth letter needs \(\psi(w^{1/2})\), and
\(w^{1/2}=U^{1/2}-\tfrac12\theta_wU^{-1/2}
-\tfrac18\theta_w^2(U-\xi)^{-3/2}\) has *decaying* amplitudes only,
with \(U^{1/2}=m^{1/4}\to n^{3/8}\) likewise. The pure modes
\(e(\tfrac l2n^{3/8})\) have \(\lambda\asymp lP^{-13/8}\), giving
\(l^{1/2}P^{3/16}+l^{-1/2}P^{13/16}\); the mixed cases sit in the
dominance hierarchy \(iP^{-1/2}\gg jP^{-5/4}\gg lP^{-13/8}\) with all
three second derivatives of the same sign. Total
\(\ll N^{13/16+\varepsilon}\). \(\square\)

**Corollary 4.9 (depth-4 census below the kernel; density \(13/16\)).**
Every itinerary word class of depth at most four except \(OOO*\)
satisfies
\(\#\{n\le N:\mathrm{word}(n)\ \text{has prefix}\ w\}
=2^{-|w|}N+O(N^{1-\delta_w})\) with the explicit exponents above. In
particular
\[
\#\{n\le N:n\ \text{odd},\ \text{itinerary }OOEE\}
=\tfrac N{16}+O(N^{23/24+\varepsilon}),
\]
and the class of starts with a certified descent within four steps —
evens (one step), \(OE\) (two steps), \(OOEE\) (four steps) — has
cardinality
\[
\tfrac N2+\tfrac N4+\tfrac N{16}+O(N^{23/24+\varepsilon})
=\tfrac{13N}{16}+O(N^{23/24+\varepsilon}).
\]

*Proof.* For \(OOEE\), Lemma 3.6 gives
\(\#OOEE=\tfrac18\sum_{n\le N\ \mathrm{odd}}
(1-\psi_1)(1+\psi_2)(1+\psi_3)\) with
\(\psi_1=\psi(n^{3/2})\), \(\psi_2=\psi(m^{3/2})\),
\(\psi_3=\psi(v^{1/2})\); expanding gives the main term and seven
sign sums bounded by Theorem 4.7. Every \(OOEE\) start descends
within four steps by Proposition 3.1: \(3^2<2^4\). The even class
and the \(OE\) class carry the one- and two-step certificates, and
the three classes are disjoint. The remaining depth-\(\le4\) prefixes
are Theorem 4.1 (depth 1), Theorem 4.4 and Proposition 4.5 (depths
2–3), and Theorems 4.7–4.8 (depth 4). \(\square\)

The density \(13/16\) is the exact ceiling of this one-growing-layer
machinery: a word contracts iff \(3^{o}<2^{\ell}\), the method so far
proves letters at positions 1–3 of any word plus further letters along
even branches only, and the contracting minimal words with all odd
letters at positions \(\le2\) are exactly \(E\), \(OE\), and \(OOEE\).
Any further certified density requires the \(OOO*\) split — a second
growing layer, where the fourth-letter phase coefficient
\(W\asymp kn^{9/8}\) crosses integers within single steps and no
drift-1 interval exists. Sections 5 and 6 close that split and
harvest the contracting words it unlocks.

## 5. The kernel theorem

Every reorganization of the \(OOO*\) phase funnels into one object:
for smooth weights \(c\) of scale \(kP^{9/8}\) on \(n\sim P\),
\[
K_c(P)=\sum_{\substack{n\sim P\\ n\ \mathrm{odd}}}
e\bigl(c(n)\,\{\lfloor n^{3/2}\rfloor^{3/2}\}\bigr).
\]
This section proves the kernel bound at full length: every estimate
that the proof uses is displayed, with its dependence on the mode
\(k\), the differencing shifts \(h_1,h_2,h_3\), the branch offset
\(j\), and the expansion frequencies made explicit, and with
numerical constants displayed at each of the sign-critical
dominance checks. The expansion corrects one estimate of the
earlier laboratory record and absorbs a second. First, the
correction: the mixed pieces were previously modelled as
\(e(sX)\) with a frozen real coefficient \(s\asymp qP^{3/4}\); in
exact form they are level-2 waves \(e(qY)\) times an optional
frozen-floor factor, and the frozen model silently discards the
sawtooth of amplitude \(\asymp qP^{3/4}\) hidden in
\(Y=(X-\theta)^{3/2}\). Treated exactly — by the same exact
linearization that proves Theorem 4.4 — the targeted third
differencing survives, but the honest bound is
\(q^{-1/6}P^{23/24+\varepsilon}\) (Lemma 5.2), not
\(q^{1/6}P^{7/8+\varepsilon}\): the mixed piece is a depth-2 object
and receives exactly depth-2 strength. The kernel saving therefore
drops from the formerly claimed \(\delta=\tfrac1{72}\) to
\(\delta=\tfrac1{96}\); every downstream exponent
\(1-\tfrac1{72}\) becomes \(1-\tfrac1{96}\), and no density
changes. Second, the absorbed observation: the pure smooth pieces
of Step 4 carry a factor \((k|j|)^{1/2}\) that the earlier record
did not display; since
\((k|j|)^{1/2}P^{15/16}\le P^{23/24}\) exactly on the standing
range \(k\le P^{1/24}\), this loss sits below the new mixed-piece
bottleneck and the corrected bound remains uniform in \(k\) on the
original range.

The next lemma collects the exact reductions behind the treatment:
the kernel phase is the level-2 local floor defect; the second
difference of the level-2 integer obeys an exact floor identity; on
an explicit carry-branch decomposition that second difference is a
smooth function with a frozen floor; and the doubly differenced
kernel phase decomposes exactly into four bounded pieces — the
master identity — with no growing smooth part left to estimate.

**Lemma 5.1 (level-2 defect, double gap, branch freeze, and the master identity).**
Fix shifts \(d_1=2h_1\), \(d_2=2h_2\) and write \(\Delta_1\),
\(\Delta_2\), \(\Delta\Delta\) for the corresponding difference
operators in \(n\), and \(W=\Delta_1Y\), \(W'=\Delta_2Y\).

(i) For odd \(n\ge3\),
\[
\tfrac34\,v^{1/2}\theta_2
=\tfrac12\bigl(m^{9/4}-v^{3/2}\bigr)-R,
\qquad 0\le R\le\tfrac3{16}\,v^{-1/2}.
\]
Hence for \(c=\tfrac{3k}4v^{1/2}\) the kernel phase \(c\,\theta_2\)
equals \(\tfrac k2(Y^{3/2}-v^{3/2})\) up to \(kR\ll kP^{-9/8}\) per
term: the kernel is the exponential sum of the level-2 local floor
defect.

(ii) Exactly, with \(g_2=\Delta_1v\),
\[
\Delta_2g_2=\lfloor\Delta\Delta Y\rfloor+\kappa''+\Delta_2\kappa_2,
\qquad
\kappa_2=\bigl[\theta_2\ge1-\{W\}\bigr],\quad
\kappa''=\bigl[\{W\}\ge1-\{\Delta\Delta Y\}\bigr],
\]
and every carry is a difference of unit sawtooths:
\(\bigl[\{A\}+\{B\}\ge1\bigr]=\{A\}+\{B\}-\{A{+}B\}\)
(Lean: `seq_floor_gap_second`).

(iii) Write \(b_1=\lfloor\Delta_1X\rfloor\),
\(b_2=\lfloor\Delta_2X\rfloor\), \(b_{12}=\lfloor\Delta_{12}X\rfloor\)
(shift \(d_1{+}d_2\)) — each constant on runs of length
\(\asymp P^{1/2}/h\) — and let
\(\boldsymbol\kappa=(\kappa_1,\kappa_2,\kappa_{12})\in\{0,1\}^3\) be
the level-1 carries, so that the shifted values of \(m\) are
\(m+\beta_1\), \(m+\beta_2\), \(m+\beta_{12}\) with
\(\beta_i=b_i+\kappa_i\). On each \(b\)-run intersection and carry
branch,
\[
\Delta\Delta Y=F_{\boldsymbol\kappa}(m),
\qquad
F_{\boldsymbol\kappa}(m)=(m{+}\beta_{12})^{3/2}
-(m{+}\beta_1)^{3/2}-(m{+}\beta_2)^{3/2}+m^{3/2}
\]
exactly. The net offset
\(j=\beta_{12}-\beta_1-\beta_2\)
satisfies \(|j|\le3\) for \(h_1h_2\le P^{1/2}/3\), and \(F\) splits
exactly into an offset term and a genuine second difference: for
some \(\xi_1\) between \(0\) and \(j\) and some
\(\xi_2\in(0,\beta_1+\beta_2)\),
\[
F_{\boldsymbol\kappa}(m)
=\tfrac32\,j\,(m+\beta_1+\beta_2+\xi_1)^{1/2}
+\tfrac34\,\beta_1\beta_2\,(m+\xi_2)^{-1/2}.
\]
Consequently, with \(G:=F_{\boldsymbol\kappa}\circ X\),
\[
\tfrac32|j|P^{3/4}\le\Bigl|\tfrac32j(\cdot)^{1/2}\Bigr|
\le2.6\,|j|P^{3/4},
\qquad
1.4\,h_1h_2P^{1/4}\le\tfrac34\beta_1\beta_2(\cdot)^{-1/2}
\le15\,h_1h_2P^{1/4},
\]
\[
|G'(n)|\le2|j|P^{-1/4}+20\,h_1h_2P^{-3/4}<1,
\qquad
|G''(n)|\le2|j|P^{-5/4}+25\,h_1h_2P^{-7/4},
\]
so \(\lfloor G(n)\rfloor\) is constant on runs of length
\(\ge\tfrac1{22}\min\bigl(P^{1/4}/(|j|{+}1),\,P^{3/4}/(h_1h_2)\bigr)\).
The branch indicator is a finite union of arcs in the single
variable \(\theta\) with slowly moving endpoints (drifts
\(\le1.5hP^{-1/2}\) per step): exactly the moving-endpoint pattern of
Step 4 of Theorem 4.4, absorbed by the same exact shift device at
\(O(\log P)\) mode-mass cost.

(iv) *(Master identity.)* With
\(\kappa_2=[\theta_2\ge1-\{W\}]\), \(\kappa_2'=[\theta_2\ge1-\{W'\}]\)
the level-2 carries at the two shifts, and \(\kappa''\),
\(\Delta_2\kappa_2\) as in (ii), the doubly differenced kernel phase
decomposes exactly:
\[
\Delta\Delta(c\,\theta_2)
=(\Delta\Delta c)\,\theta_2
+(\Delta_2c)(n{+}d_1)\,\bigl(\{W\}-\kappa_2\bigr)
+(\Delta_1c)(n{+}d_2)\,\bigl(\{W'\}-\kappa_2'\bigr)
+c_{11}\,\bigl(\{\Delta\Delta Y\}-\kappa''-\Delta_2\kappa_2\bigr),
\]
where \(c_{11}\) is the doubly shifted weight. Every bracket is
bounded by \(2\) in absolute value: no unbounded smooth part
survives the differencing.

*Proof.* (i) Taylor of \((v+\theta_2)^{3/2}\) at \(v\), with
\(Y^{3/2}=m^{9/4}\). (ii) The gap identity of Lemma 4.3(ii) applied
twice — to \(Y\) at shift \(d_1\), then to the real sequence
\(n\mapsto W(n)\) at shift \(d_2\), with \(\Delta_2W=\Delta\Delta Y\);
the sawtooth form of the carry is the Lean-verified floor-carry
identity rearranged. (iii) The corner identities are Lemma 4.3(ii)
at the three shifts, and the offset bound follows from
\(|\Delta\Delta X|\le4h_1h_2\sup|X''|=3h_1h_2P^{-1/2}<1\). For the
split, group
\(F=\bigl[(m{+}\beta_1{+}\beta_2{+}j)^{3/2}-(m{+}\beta_1{+}\beta_2)^{3/2}\bigr]
+\bigl[(m{+}\beta_1{+}\beta_2)^{3/2}-(m{+}\beta_1)^{3/2}
-(m{+}\beta_2)^{3/2}+m^{3/2}\bigr]\): the first bracket is
\(\tfrac32j(\cdot)^{1/2}\) by the mean value theorem, the second is
\(\beta_1\beta_2\,f''(m+\xi_2)\) for \(f=x^{3/2}\) by the double mean
value theorem. The displayed numerical bounds use
\(m\in(P^{3/2}{-}1,2^{3/2}P^{3/2}]\),
\(\beta_i\in[3h_iP^{1/2}{-}1,\,3\sqrt2\,h_iP^{1/2}{+}1]\)
(from \(\Delta_iX=2h_iX'(\xi)\) and (E1) below), and
\(G'=F'(X)X'\), \(G''=F''(X)X'^2+F'(X)X''\) with
\(F'=\tfrac34j(\cdot)^{-1/2}-\tfrac38\beta_1\beta_2(\cdot)^{-3/2}\),
\(F''=-\tfrac38j(\cdot)^{-3/2}+\tfrac9{16}\beta_1\beta_2(\cdot)^{-5/2}\).
(iv) By (ii) and the definitions:
\(\Delta_1\theta_2=\Delta_1Y-\Delta_1v=W-(\lfloor W\rfloor+\kappa_2)
=\{W\}-\kappa_2\) (Lemma 4.3(ii) applied to \(Y\)), likewise
\(\Delta_2\theta_2=\{W'\}-\kappa_2'\), and
\(\Delta\Delta\theta_2=\Delta\Delta Y-\Delta_2g_2
=\{\Delta\Delta Y\}-\kappa''-\Delta_2\kappa_2\) by (ii). Substitute
these into the exact product rule
\[
\Delta\Delta(cf)=c_{11}\,\Delta\Delta f
+(\Delta_2c)(n{+}d_1)\,\Delta_1f
+(\Delta_1c)(n{+}d_2)\,\Delta_2f
+(\Delta\Delta c)\,f .
\]
The identity is machine-validated on \(12{,}000\) exact
scaled-integer samples across shift pairs
\((h_1,h_2)\in\{(1,1),(2,3),(5,7)\}\)
(`master_identity_check`), on top of the Lean-anchored constituents
(`seq_floor_gap`, `seq_floor_gap_second`). \(\square\)

One warning, essential to the organization: \(\lfloor\Delta\Delta
Y\rfloor\) itself is *not* frozen. The level-1 carry toggles at
essentially every step and shifts \(\Delta\Delta Y\) by
\(\tfrac32j_1m^{1/2}\), a jump of size \(\asymp P^{3/4}\). The branch
decomposition of (iii), which carries the flicker inside the
indicator over the eight carry branches, is therefore forced: no
decomposition conditioning on the *values* of the level-1 gaps
produces sets on which the second difference is smooth.

### Standing estimates

All estimates of this section take place on a dyadic block
\(n\in(P,2P]\), \(n\) odd, under the standing constraints
\[
\text{(C1)}\quad kh_1h_2\le P^{1/8},
\qquad
\text{(C2)}\quad h_1h_2\le P^{1/2}/3,
\qquad
\text{(C3)}\quad 1\le k\le P^{1/24},
\]
and every displayed constant below is valid for
\(P\ge P_0\) with an absolute \(P_0\). The base derivatives are
\[
\text{(E1)}\quad
X'=\tfrac32n^{1/2}\in(1.5,2.13]\,P^{1/2},\quad
X''=\tfrac34n^{-1/2}\in[0.53,0.75)\,P^{-1/2},
\]
\[
\phantom{\text{(E1)}}\quad
-X'''=\tfrac38n^{-3/2}\in[0.13,0.375)\,P^{-3/2},\quad
X''''=\tfrac9{16}n^{-5/2}\le0.57\,P^{-5/2},
\]
and \(m=X-\theta\in(P^{3/2}-1,\,2.83\,P^{3/2}]\). Every gap is a
mean value: for any shift \(2h\),
\[
\text{(E2)}\quad
\Delta X=2hX'(\xi)\in(3hP^{1/2},\,4.3hP^{1/2}),
\qquad
\beta:=\lfloor\Delta X\rfloor+\kappa
\in(3hP^{1/2}-1,\,4.3hP^{1/2}+1),
\]
so that every level-1 gap integer at shift \(2h\) is
\(\asymp hP^{1/2}\) with the displayed constants. For the monomial
weight \(c=\tfrac{3k}4n^{9/8}\) (the general \(c\) of Theorem 5.3
changes only the absolute constants),
\[
\text{(E3)}\quad
c'=\tfrac{27}{32}kn^{1/8},\quad
c''=\tfrac{27}{256}kn^{-7/8},\quad
c'''=-\tfrac{189}{2048}kn^{-15/8},\quad
c''''=\tfrac{2835}{16384}kn^{-23/8},
\]
\[
\text{(E4)}\quad
\Delta_ic=2h_ic'(\xi)\in(1.68,1.85)\,kh_iP^{1/8},
\qquad
\Delta\Delta c=4h_1h_2c''(\xi)\in(0.22,0.43)\,kh_1h_2P^{-7/8}.
\]
On the level-2 side, with \(\beta_i\) as in Lemma 5.1(iii),
\[
\text{(E5)}\quad
W=\Delta_1Y\in(4.4,11)\,h_1P^{5/4},
\qquad
\bigl|(W\circ\text{cell})'\bigr|
=\bigl|W_1'(m)\,X'\bigr|\in(2.2,10.4)\,h_1P^{1/4},
\]
where \(W_1(m)=(m+\beta_1)^{3/2}-m^{3/2}\), so \(\{W\}\) is a *fast*
sawtooth (its argument moves by \(\gg1\) per step), while \(\theta\),
\(\{\Delta_iX\}\), and \(\{\Delta\Delta Y\}\) are slow. The branch
bounds of Lemma 5.1(iii) give, per branch with offset \(j\),
\[
\text{(E6)}\quad
\bigl|(cF)''\bigr|
=\tfrac{945}{512}\,k|j|\,n^{-1/8}\,(1+O(P^{-1/4}))
+O\bigl(kh_1h_2P^{-5/8}\bigr),
\]
the two shapes being the composite monomials \(kjn^{15/8}\)
(offset branches) and \(kh_1h_2\)-scale \(n^{11/8}\) (zero-offset),
with sign product
\(\alpha(\alpha-1)(\alpha+\beta-2)(\alpha+\beta-3)>0\) at
\(\alpha=\tfrac98\), \(\beta\in\{\tfrac34,\tfrac14\}\). Finally, the
run and cell inventories: level-1 gap cells at shift \(2h\) number
at most \(1.5hP^{1/2}+1\) with lengths in
\([\tfrac23,\,0.95]\,P^{1/2}/h\), and the frozen-floor runs of
\(\lfloor F_{\boldsymbol\kappa}(X)\rfloor\) number at most
\(22(|j|+1)P^{3/4}\) by the derivative bound of Lemma 5.1(iii).

Throughout, "\(A\) is dominated by \(B\) at margin \(P^{-\rho}\)"
means \(\sup|A|/\inf|B|\le CP^{-\rho}\) with the displayed \(C\):
the composite second derivative then keeps the sign and, up to the
factor \(1+CP^{-\rho}\), the size of \(B\), so Lemma 3.3 applies at
\(B\)'s scale.

The proof of the kernel theorem classifies the differenced pieces
into four classes; three are handled by standard tests, and the
fourth — an exact level-2 wave \(e(qY)\), possibly riding a frozen
floor — is the genuinely new difficulty. We isolate it as a
standalone lemma with its own differencing, so that it can be
checked independently.

**Lemma 5.2 (level-2 waves: the mixed-piece bound).**
Assume (C1)–(C3), write \(\mathcal D=\{0,d_1,d_2,d_1{+}d_2\}\), and
call a *decoration* any sum \(\rho\) of at most four terms of the
classes

- (D1) \(q'\,\Delta_{2h}\Delta_{2h'}Y(n{+}d')\) with
  \(|q'|\le P^{1/16}\), \(1\le h'\le P^{1/24}\),
  \(d'\in\mathcal D\);
- (D2) \(-\Delta_{2h}\bigl(c\,\lfloor
  F_{\boldsymbol\kappa}(X)\rfloor\bigr)(n)\), with
  \(F_{\boldsymbol\kappa}\) a branch function of Lemma 5.1(iii),
  offset \(|j|\le3\);
- (D3) a smooth \(\varphi\) with \(|\varphi''|\le3kh_1h_2P^{-5/8}\)
  and \(|\varphi'''|\le3kh_1h_2P^{-13/8}\);

here \(2h\) is the shift of part (i), and in part (ii) the
decorations are read after the differencing there. Then, for sums
over \(n\in(P,2P]\), \(n\) odd:

(i) *(differenced wave)* for all integers \(u,h\ge1\) with
\(h\le P^{1/8}\), \(uh\le P^{1/2}\), and \(d\in\mathcal D\),
\[
V:=\Bigl|\sum_n
e\bigl(u\,\Delta_{2h}Y(n{+}d)+\rho(n)\bigr)\Bigr|
\;\ll\;
\Bigl((uh)^{1/2}P^{5/8}+(h/u)^{1/2}P^{7/8}+P^{7/8}\Bigr)
P^{\varepsilon};
\]

(ii) *(wave)* for all integers \(q,q'\) with
\(|q|,|q'|\le P^{1/16}\) and \(t:=q+q'\ne0\), all
\(d\ne d'\in\mathcal D\), \(\varepsilon_0\in\{0,1\}\), and \(\varphi\)
of class (D3),
\[
U:=\Bigl|\sum_n
e\bigl(q\,Y(n{+}d)+q'\,Y(n{+}d')
-\varepsilon_0\,c(n)\lfloor F_{\boldsymbol\kappa}(X(n))\rfloor
+\varphi(n)\bigr)\Bigr|
\;\ll\;|t|^{-1/6}\,P^{23/24+\varepsilon}.
\]

Part (ii) is the mixed-piece bound proper: the level-2 wave
\(e(qY)\), possibly riding a frozen floor. Part (i) is the engine
that (ii)'s targeted differencing feeds, and is also used directly
for the \(\{W\}\)-content of the kernel proof. The exponent
\(\tfrac{23}{24}\) is not an accident: written exactly, the wave
\(e(qY)\) is the depth-2 object of Theorem 4.4, and part (ii)
recovers exactly the depth-2 strength — no more. The earlier
laboratory record modelled \(U\) as \(e(sX)\) with \(s\) frozen of
size \(qP^{3/4}\) and claimed \(q^{1/6}P^{7/8+\varepsilon}\); that
model discards the sawtooth \(-\tfrac32qX^{1/2}\theta\) of amplitude
\(\asymp qP^{3/4}\) inside \(qY=q(X-\theta)^{3/2}\), and the claim
does not survive the exact treatment.

*Proof of (ii) from (i).* Replacing the summand by its conjugate we
may take \(t\ge1\). Write, exactly,
\[
qY(n{+}d)+q'Y(n{+}d')
=t\,Y(n{+}d)+q'\,\Delta_{|d'-d|}Y(n{+}\min(d,d')),
\]
so the second term is a decoration seed. Weyl differencing at shift
\(2h_3\), \(1\le h_3\le H_3:=\lceil t^{1/3}P^{1/12}\rceil\):
\[
|U|^2\le\frac{P^2}{H_3}
+\frac{2P}{H_3}\sum_{h_3=1}^{H_3}
\bigl|V_{h_3}\bigr|,
\qquad
V_{h_3}
=\sum_ne\bigl(t\,\Delta_{2h_3}Y(n{+}d)+\rho_{h_3}(n)\bigr),
\]
where \(\rho_{h_3}\) collects
\(q'\Delta_{2h_3}\Delta_{|d'-d|}Y\) (class (D1) with
\(h'=|d'-d|/2\le h_1{+}h_2\le P^{1/24}\cdot2\)),
\(-\varepsilon_0\Delta_{2h_3}(c\lfloor F(X)\rfloor)\) (class (D2)),
and \(\Delta_{2h_3}\varphi\) (class (D3):
\(|(\Delta_{2h_3}\varphi)''|\le2h_3\sup|\varphi'''|
\le6kh_1h_2h_3P^{-13/8}\le3kh_1h_2P^{-5/8}\) since
\(h_3\le P^{1/4}\)). The hypothesis of (i) holds:
\(th_3\le t\cdot2t^{1/3}P^{1/12}=2t^{4/3}P^{1/12}
\le2P^{1/12+1/12}\le P^{1/2}\). Part (i) gives
\[
|U|^2\le\frac{P^2}{H_3}
+\Bigl(4t^{1/2}H_3^{1/2}P^{13/8}
+4t^{-1/2}H_3^{1/2}P^{15/8}
+4P^{15/8}\Bigr)P^{\varepsilon},
\]
and at \(H_3=\lceil t^{1/3}P^{1/12}\rceil\) the four terms are, in
order, \(\le t^{-1/3}P^{23/12}\);
\(\le6t^{2/3}P^{5/3}=6\,(tP^{-1/4})\,t^{-1/3}P^{23/12}
\le6P^{1/16-1/4}\cdot t^{-1/3}P^{23/12}\);
\(\le6t^{-1/3}P^{1/24}P^{15/8}=6t^{-1/3}P^{23/12}\); and
\(\le4\,(t^{1/3}P^{-1/24})\,t^{-1/3}P^{23/12}
\le4P^{1/48-1/24}\,t^{-1/3}P^{23/12}\). Hence
\(|U|^2\ll t^{-1/3}P^{23/12+\varepsilon}\), which is (ii).

*Proof of (i).* Six stages; write \(\nu=n+d\) (a shift of the block
by at most \(d_1{+}d_2\le P^{1/2}\), harmless in every estimate) and
\(\Delta=\Delta_{2h}\).

*Stage 1 (the \(m\)-linear form).* By Lemma 4.3(i) at the bases
\(\nu\) and \(\nu{+}2h\),
\[
u\,\Delta Y
=u\,A_h(\nu)
+\tfrac{3u}2\,g(\nu)\,(\nu{+}2h)^{3/4}
-\tfrac{3u}2\,\theta_\nu\,\Delta(\nu^{3/4})
+u\,\Delta E,
\]
with \(g=m(\nu{+}2h)-m(\nu)\), \(|u\Delta E|\le uP^{-3/4}\) (total
cost over the block \(\le2\pi uP^{1/4}\le2\pi P^{3/4}\)), and
\[
A_h(\nu)=\tfrac32\nu^{3/2}\Delta(\nu^{3/4})
-\tfrac12\Delta(\nu^{9/4})
=-\tfrac{27}8h^2\nu^{1/4}\bigl(1+O(hP^{-1})\bigr):
\]
the two \(\nu^{5/4}\)-scale contributions cancel exactly at leading
order (both equal \(\tfrac94h\nu^{5/4}\)), leaving
\(|uA_h''|\le0.64\,uh^2P^{-7/4}\). The sawtooth coefficient is
\[
B(\nu):=\tfrac{3u}2\,\Delta(\nu^{3/4})
=\tfrac94\,uh\,\xi^{-1/4}\in(1.89,2.25]\,uhP^{-1/4}.
\]

*Stage 2 (gap cells and the exact shift device).* Split into the
level sets of \(\lfloor\delta_h\rfloor\),
\(\delta_h(\nu)=(\nu{+}2h)^{3/2}-\nu^{3/2}\): at most
\(1.5hP^{1/2}+1\) cells of length in
\([\tfrac23,\,0.95]\,P^{1/2}/h\) (E1). On a cell \(g=G+\kappa\) with
\(G=\lfloor\delta_h\rfloor\) frozen and
\(\kappa=[\theta_\nu\ge1-\{\delta_h\}]\); Vaaler-expand \(\kappa\)
at truncation \(R_0=P^{1/4}\) (majorant cost \(\le4P/R_0=4P^{3/4}\)).
The moving endpoint costs nothing: as in Theorem 4.4, Step 4, the
endpoint's smooth part contributes the exact phase
\(r\delta_h(\nu)\), and
\(e(r\nu^{3/2}+r\delta_h(\nu))=e(r(\nu{+}2h)^{3/2})\), so every
\(r\)-term falls into the two smooth families \(e(r\nu^{3/2})\),
\(e(r(\nu{+}2h)^{3/2})\), \(0<|r|\le R_0\), with weights
\(\le1/|r|\); the in-cell variation of the coefficient is exactly
\(1\) and one Abel summation absorbs it at a factor \(\le2{+}2\pi\).

*Stage 3 (the \(\theta\)-sawtooth).* Two regimes.
(s1) If \(uh\le P^{3/16}\) then \(|B|\le2.25P^{-1/16}<\tfrac12\) for
\(P\ge P_0\): Lemma 3.8 with \(T=P^{1/2}\), \(J=R_0\) expands
\(e(-B_0\{\nu^{3/2}\}\dots)\) per window (here one window: the total
drift of \(B\) is \(\le0.6uhP^{-1/4}\le0.6P^{-1/16}<1\)) into the
same two mode families at coefficient factor
\(\min(2,2\pi|B|)\le14P^{-1/16}\), mass \(O(\log P)\), flat cost
\(\le12P^{1/2}\), majorant \(\le14P^{-1/16}\cdot4P^{3/4}\).
(s2) If \(P^{3/16}<uh\le P^{1/2}\) then \(|B|\le2.25P^{1/4}\) and
\(B\) drifts by at most \(1\) on windows of length
\(\ge P^{5/4}/(0.6uh)\ge1.2P^{3/4}\): at most \(0.6P^{1/4}+1\)
windows. Per window Lemma 3.8 at the centre \(B_0\)
(\(T=P^{1/2}\): flat cost \(\le8(1{+}2.25P^{1/4})P^{1/2}
\le27P^{3/4}\) in total) produces modes \(e(w\nu^{3/2})\) whose
coefficients decay as
\(\min(2,\tfrac1{\pi|w+B_0|})+\min(2,\tfrac1{\pi|w|})\); the
window-boundary cost is, using \(uh>P^{3/16}\),
\(\le(0.6P^{1/4}{+}1)\cdot1.83\,(0.30\,uh)^{-1/2}P^{3/8}
\le2.1\,P^{1/4-3/32+3/8}=2.1\,P^{17/32}\le P^{5/8}\). Modes with
\(|w|\) in the collision window are treated in Stage 5.

*Stage 4 (the main curvature, \(r=w=0\)).* On a cell the remaining
phase is \(\tfrac{3u}2G(\nu{+}2h)^{3/4}+uA_h+(\text{smooth
decorations})\), with second derivative
\[
-\tfrac9{32}\,uG\,(\nu{+}2h)^{-5/4}
\in-[0.30,\,1.35]\,uh\,P^{-3/4}
\qquad(\text{E2}),
\]
single-signed with in-cell ratio \(\sup/\inf\le4.5\); this is the
composite whose two contributions
\(-\tfrac{27}{32}\beta n^{-5/4}\) and \(+\tfrac9{16}\beta n^{-5/4}\)
(net \(-\tfrac9{32}\beta n^{-5/4}\), margin \(3{:}2\)) are
machine-validated (`kernel_margin_scan`, gate m1). The competitor
\(uA_h''\) has ratio
\(\le0.64uh^2P^{-7/4}/(0.30uhP^{-3/4})\le2.2hP^{-1}\le2.2P^{-3/4}\);
decoration competitors are bounded in Stage 6. Lemma 3.3 per cell
and summation give
\[
\sum_{\text{cells}}
\Bigl(\ell_i\lambda^{1/2}+\lambda^{-1/2}\Bigr)
\le2.3\,(uh)^{1/2}P^{5/8}
+2.8\,(h/u)^{1/2}P^{7/8}.
\]

*Stage 5 (nonzero modes and collisions).* A mode \(w\ne0\) (or
\(r\ne0\); identical treatment with weight \(1/|r|\)) adds the phase
\(w\nu^{3/2}\) of curvature \(\ge0.53|w|P^{-1/2}\).
If \(0.53|w|P^{-1/2}\ge4\cdot1.35uhP^{-3/4}\), i.e.
\(|w|\ge10.2\,uhP^{-1/4}\), the mode curvature dominates at margin
\(\ge4\): Lemma 3.3 over the full block gives
\(\le1.4|w|^{1/2}P^{3/4}+1.4|w|^{-1/2}P^{1/4}\), and the
coefficient-weighted sums are
\(\le3R_0^{1/2}P^{3/4}\log P=3P^{7/8}\log P\) (families of Stage 2,
regime (s1)) and \(\le CP^{7/8}\log P\) (regime (s2) tails). If
\(|w|\le0.1\,uhP^{-1/4}\) the main curvature dominates at margin
\(\ge4\) and the mode rides along at Stage 4's scale, weight
summable to \(O(\log P)\). In the remaining collision window
\(0.1\,uhP^{-1/4}\le|w|\le10.2\,uhP^{-1/4}\) (nonempty only in
regime (s2)), the two curvatures can cancel: there the phase is the
two-term monomial
\(a\nu^{3/4}+w\nu^{3/2}\) with \(a=\tfrac{3u}2G\asymp uh P^{1/2}\)
plus perturbations already shown \(\rho_0\)-small, and Lemma 3.9
with \((\alpha,\beta)=(\tfrac34,\tfrac32)\) applies per window with
\(M\le1.35uhP^{-3/4}\le1.35P^{-1/4}\):
\[
\le|I_w|M^{1/2}+M^{-1/2}
+|I_w|(M/P)^{1/6}+|I_w|^{1/2}(M/P)^{-1/6},
\]
which, summed over windows with the \(O(\log P)\) collision-window
coefficient mass, is
\(\le C\bigl((uh)^{1/2}P^{5/8}+(uh)^{1/6}P^{17/24}
+(uh)^{-1/6}P^{19/24}+P^{5/8}\bigr)\log P\le CP^{7/8}\log P\)
(using \(uh\le P^{1/2}\)).

*Stage 6 (decorations).* Each class is dominated at a displayed
margin against the Stage-4 curvature
\(\ge0.30uhP^{-3/4}\).

- (D1). On the branch decomposition of Lemma 5.1(iii) at the shift
  pair \((h_3\text{-role }h,\,h')\): the arcs are absorbed by the
  shift device (log mass); the \(b\)-run boundaries add
  \(\le1.5(h{+}2h')P^{1/2}+2\) cells, at boundary cost
  \(\le1.5(h{+}2h')P^{1/2}\cdot1.83(0.30uh)^{-1/2}P^{3/8}
  \le5.1(h/u)^{1/2}P^{7/8}+10.3\,h'(uh)^{-1/2}P^{7/8}\)
  (the second term is what the \(H_3\)-averaging of part (ii)
  absorbs: it contributes
  \(\le2h't^{-2/3}P^{43/24}\le P^{1/24-1/8}\,t^{-1/3}P^{23/12}\)
  there). The \(\theta\)-coefficient of the decoration is
  \(\le|q'|\bigl(2|j'|P^{-1/4}+20hh'P^{-3/4}\bigr)
  \le6P^{1/16-1/4}+20P^{1/16+1/4+1/24-3/4}<1\): sub-unit, expanded
  in the Stage-2 families. Its smooth curvature has ratio
  \(\le|q'|\bigl(2|j'|P^{-5/4}+25hh'P^{-7/4}\bigr)
  /(0.30uhP^{-3/4})\le20P^{1/16}P^{-1/2}+84P^{1/16+1/24}P^{-1}
  \le P^{-1/4}\): dominated.
- (D2). Write
  \(\Delta(c\lfloor F\rfloor)
  =(\Delta c)\lfloor F\rfloor+c_+\Delta\lfloor F\rfloor\)
  with \(c_+=c(\cdot{+}2h)\).
  (a) \((\Delta c)\lfloor F\rfloor=(\Delta c)F-(\Delta c)\{F\}\):
  the smooth part has curvature
  \(\le\bigl((\Delta c)F\bigr)''\le7kh|j|P^{-9/8}
  +28khh_1h_2P^{-13/8}\), ratio to the main curvature
  \(\le24k|j|P^{-3/8}/u\le72P^{1/24-3/8}\): dominated. The sawtooth
  part has coefficient
  \(\Delta c\in(1.68,1.85)\,khP^{1/8}\), handled per windows of
  drift \(\le1\): at most \(2khP^{1/8}{+}1\) windows, at boundary
  cost
  \(\le2khP^{1/8}\cdot1.83\,(0.30\,uh)^{-1/2}P^{3/8}
  \le7k\,(h/u)^{1/2}P^{1/2}\). Per window, Lemma 3.8 at
  \(T=P^{1/2}\) yields modes \(e(q''(F\circ X))\) of curvature
  \(\le(2khP^{1/8}{+}P^{1/2})\cdot3|j|P^{-5/4}\le18P^{-3/4}
  \cdot P^{-1/16}\), ratio to the main curvature
  \(\le60P^{-1/16}\): dominated. The flat cost is, per point,
  \(8(1{+}B_0)/T\), so in total
  \(\le8\bigl(1{+}1.85khP^{1/8}\bigr)P^{1/2}
  \le8P^{1/2}+15\,khP^{5/8}\le23\,P^{1/24+1/8+5/8}
  =23\,P^{19/24}\le P^{7/8}\), using \(h\le P^{1/8}\) and (C3).
  (b) \(c_+\Delta\lfloor F\rfloor\): by the gap identity applied to
  the sequence \(F\circ X\),
  \(\Delta\lfloor F\rfloor=\lfloor\Delta F\rfloor+\kappa_F\).
  \(\Delta F\) has total drift
  \(\le P\cdot2h\sup|(F\circ X)''|\le P\cdot2h(2|j|P^{-5/4}
  +25h_1h_2P^{-7/4})\le13hP^{-1/4}+50h\,h_1h_2P^{-3/4}<1\), so
  \(\lfloor\Delta F\rfloor\) takes at most two values, on at most
  two intervals; per value the phase \(-q_0c_+\) (\(|q_0|\le
  2{+}6hP^{-1/4}\le3\)) has curvature \(\le0.4kP^{-7/8}\), ratio
  \(\le1.4kP^{-1/8}/(uh)\le1.4P^{1/24-1/8}\): dominated. The carry
  \(\kappa_F=\{F\}+\{\Delta F\}-\{F{+}\Delta F\}\) is a sum of unit
  sawtooths in slow variables (all drifts \(<1\) per step): Lemma
  3.5 at truncation \(P^{1/8}\) (majorant \(\le3\cdot4P^{7/8}\))
  gives modes \(e(q''(F\circ X))\)-type of curvature
  \(\le P^{1/8}\cdot3|j|P^{-5/4}\le9P^{-9/8}\), ratio
  \(\le30P^{-3/8}\): dominated.
- (D3). Ratio
  \(\le2h\sup|\varphi'''|/(0.30uhP^{-3/4})
  \le20kh_1h_2P^{-7/8}/u\le20P^{1/8-7/8}\): dominated.

*Totals.* Stages 1–6 bound \(V\) by
\[
C\Bigl((uh)^{1/2}P^{5/8}+(h/u)^{1/2}P^{7/8}+P^{7/8}
+k\,(h/u)^{1/2}P^{1/2}\Bigr)\log^3P,
\]
and the fourth term is \(\le P^{1/24}\cdot(h/u)^{1/2}P^{1/2}\), 
absorbed by the second. This is (i) up to the stated
\(P^{\varepsilon}\). \(\square\)

The balance to keep in mind: with the trivial bound
\(|V_{h_3}|\le P\), part (ii)'s differencing returns nothing beyond
the choice of \(H_3\); the content of the lemma is that the floor,
coefficient, and carry bookkeeping of Stages 3–6 survives the
targeted differencing with the Stage-4 curvature intact. What is
*not* available is the frozen-coefficient shortcut: per frozen run
the run length \(P^{1/4}\) is shorter than
\(\lambda^{-1/2}\asymp(uh)^{-1/2}P^{3/8}\) for small \(uh\), and the
run-boundary cost \((h/u)^{1/2}P^{7/8}\), summed against the
\(H_3\)-average, is exactly what pins the final exponent at
\(\tfrac{23}{24}\).

**Theorem 5.3 (kernel cancellation).**
Let \(c\) be smooth on \((P,2P]\) with \(c^{(r)}\asymp kP^{9/8-r}\)
for \(r=0,\ldots,4\), derivative signs following the monomial pattern
(e.g. \(c=\tfrac{3k}4n^{9/8}\)), and \(1\le k\le P^{1/24}\). Then
\[
K_c(P)\ll P^{1-1/96+\varepsilon},
\]
uniformly in \(k\).

*Proof.* Work on a dyadic block \(n\sim P\), odd.

*Step 1 (double Weyl differencing).* Set \(H_1=P^{1/48}\),
\(H_2=P^{1/24}\). The classical inequality
\(|\sum_na_n|^2\le\tfrac{P+2H}{H}\sum_{|h|<H}
(1-\tfrac{|h|}H)\sum_na_{n+2h}\overline{a_n}\) applied twice gives
\[
|K_c|^2\le\frac{2P^2}{H_1}+\frac{4P}{H_1}
\sum_{h_1=1}^{H_1}|T_1(h_1)|,
\qquad
|T_1|^2\le\frac{2P^2}{H_2}+\frac{4P}{H_2}
\sum_{h_2=1}^{H_2}|T_2(h_1,h_2)|,
\]
with \(T_2=\sum_ne(\varphi_2)\),
\(\varphi_2=\Delta\Delta(c\,\theta_2)\). For all
\(h_1\le H_1\), \(h_2\le H_2\), \(k\le P^{1/24}\):
\(kh_1h_2\le P^{1/24+1/48+1/24}=P^{5/48}\le P^{1/8}\), so
(C1)–(C3) hold with room \(P^{-1/48}\). We prove
\[
|T_2|\ll P^{23/24+\varepsilon}
\quad\text{uniformly in }h_1,h_2,k;
\]
then \(|T_1|\ll P^{1-1/48+\varepsilon}\) and
\(|K_c|\ll P^{1-1/96+\varepsilon}\), the three savings balancing
exactly at the chosen \(H_1,H_2\).

*Step 2 (master identity; the trivial piece).* By Lemma 5.1(iv),
exactly,
\[
\varphi_2=\underbrace{(\Delta\Delta c)\,\theta_2}_{M_1}
+\underbrace{(\Delta_2c)(n{+}d_1)(\{W\}-\kappa_2)}_{M_2}
+\underbrace{(\Delta_1c)(n{+}d_2)(\{W'\}-\kappa_2')}_{M_3}
+\underbrace{c_{11}(\{\Delta\Delta Y\}-\kappa''
-\Delta_2\kappa_2)}_{M_4}.
\]
By (E4), \(|M_1|\le0.43\,kh_1h_2P^{-7/8}\), so
\(|e(M_1)-1|\le2.7\,kh_1h_2P^{-7/8}\) and deleting \(M_1\) changes
\(T_2\) by at most \(2.7\,kh_1h_2P^{1/8}\le2.7\,P^{1/4}\) by (C1).
No growing smooth part remains: every other bracket is bounded
by \(2\).

*Step 3 (the expansion inventory).* The three remaining pieces are
expanded as follows; all truncations, masses, and error costs are
displayed here once and summed in Step 6.

(3a) *\(M_2\), sawtooth part \((\Delta_2c)(n{+}d_1)\{W\}\).* The
coefficient \(B(n)=\Delta_2c(n{+}d_1)\in(1.68,1.85)kh_2P^{1/8}\)
drifts by \(|B'|\le0.22kh_2P^{-7/8}\) per step: freeze it on at most
\(2kh_2P^{1/4}{+}1\) windows on which it moves by \(\le P^{-1/8}\)
(residual cost
\(\sum_n|e((B{-}B_0)\{W\})-1|\le6.3P^{-1/8}\cdot P=6.3P^{7/8}\)).
Per window, Lemma 3.8 at the centre \(B_0\) with
\(T=P^{1/2}/(2h_1)\), \(J=P^{1/4}\): flat cost in total
\(\le8(1{+}1.85kh_2P^{1/8})\cdot2h_1P^{1/2}
\le16h_1P^{1/2}+30\,kh_1h_2P^{5/8}\le46P^{3/4}\) by (C1); the
majorant \(\Delta_J\)-part costs \(\le2\cdot4P/J=8P^{3/4}\) plus
\(J\)-mode sums at coefficients \(\le1/(J{+}1)\); modes \(e(uW)\)
with mass \(\le C\log P\) and \(u\le1.85kh_2P^{1/8}+P^{1/2}/(2h_1)\),
so that \(uh_1\le1.85P^{1/4}+P^{1/2}/2\le P^{1/2}\): every mode is a
Lemma 5.2(i) object at shift \(h_1\le P^{1/48}\). Window boundaries
cost \(\le2kh_2P^{1/4}\cdot3.4P^{3/8}\le7P^{17/24}\).

(3b) *\(M_2\), carry part \((\Delta_2c)(n{+}d_1)\kappa_2\).* Here
\(\kappa_2\in\{0,1\}\) is an integer, so exactly
\(e(-(\Delta_2c)\kappa_2)=1+\kappa_2\bigl(e(-\Delta_2c)-1\bigr)\):
the large coefficient never multiplies a sawtooth inside an
exponential. The factor \(e(-\Delta_2c(n{+}d_1))\) is a smooth phase
with \(|(\Delta_2c)''|\le2h_2\sup|c'''|\le0.19kh_2P^{-15/8}\):
class (D3). The weight \(\kappa_2=\{Y\}+\{W\}-\{Y{+}W\}\)
(Lemma 5.1(ii)) is expanded *additively* as real numbers, each unit
sawtooth by finite Fourier (Lemma 3.5) at truncation
\(J_2=P^{1/24}\), coefficients \(\le1/(\pi|q|)\), majorant cost
\(\le4P/J_2=4P^{23/24}\) per layer plus \(J_2\)-mode averages. Since
\(Y{+}W=Y(n{+}d_1)\) exactly, the resulting modes are \(e(qY(n))\),
\(e(qY(n{+}d_1))\) — Lemma 5.2(ii) objects — and \(e(qW)\) —
Lemma 5.2(i) objects.

(3c) *\(M_3\).* The mirror of (3a)–(3b) with \(h_1\leftrightarrow
h_2\), producing \(e(qY(n{+}d_2))\), \(e(qW')\)-modes.

(3d) *\(M_4\), carries.* \(\kappa''=\{W\}+\{\Delta\Delta Y\}
-\{W{+}\Delta\Delta Y\}\) with \(W{+}\Delta\Delta Y=W(n{+}d_2)\)
exactly, and \(\Delta_2\kappa_2=\kappa_2(n{+}d_2)-\kappa_2(n)\) with
each \(\kappa_2\) expanded as in (3b) at its base. The smooth
factors \(e(\mp c_{11})\) have \(|c''|\le0.11kP^{-7/8}\): class
(D3). New mode species: \(e(q\{\Delta\Delta Y\}\)-content\()\) —
slow modes, treated in Step 5 — and \(e(qY(n{+}d))\) for
\(d\in\{0,d_2,d_1{+}d_2\}\), \(e(qW(n{+}d_2))\): Lemma 5.2 objects
again.

(3e) *\(M_4\), the anchor.* The factor
\(e(c_{11}\{\Delta\Delta Y\})\) is never expanded away. On the
branch decomposition of Lemma 5.1(iii) (arcs absorbed by the exact
shift device at \(O(\log P)\) mass and \(4P^{3/4}\) majorant, as in
Theorem 4.4, Step 4), \(\{\Delta\Delta Y\}=G-J_F\) with
\(G=F_{\boldsymbol\kappa}(X{-}\theta)\) and
\(J_F=\lfloor G\rfloor\) frozen on the runs of (E6). The anchor
phase \(c_{11}(G-J_F)\) is present in **every** final piece; its
curvature scale ((E6), gate m2) is what orders the whole
classification of Step 5.

After (3a)–(3e), every final piece of \(T_2\) has the exact form
\[
e\Bigl(\ \underbrace{c_{11}(G-J_F)}_{\text{anchor}}
+\underbrace{\textstyle\sum_iq_iY(n{+}e_i)}_{\text{waves},\
e_i\in\mathcal D}
+\underbrace{u\,W\text{- and }u'W'\text{-modes}}_{\text{differenced
waves}}
+\underbrace{\text{slow modes}+\varphi}_{\text{(D3)-smooth}}\Bigr)
\]
with at most one mode from each expansion layer (three layers), and
piece weights whose total mass is \(O(\log^3P)\) beyond the
displayed majorant and flat costs.

*Step 4 (pieces with wave content: Lemma 5.2(ii)).* Let
\(t=\sum_iq_i\) be the total wave frequency,
\(|t|\le3J_2\le P^{1/16}\).

If \(t\ne0\): telescoping,
\(\sum_iq_iY(n{+}e_i)=t\,Y(n{+}e_1)+\sum_{i\ge2}q_i\,
\Delta_{e_i-e_1}Y(n{+}\min(e_1,e_i))\), and after the targeted
differencing of Lemma 5.2(ii) the differenced-wave remainders and
the \(u,u'\)-modes become (D1) decorations, the anchor becomes the
(D2) decoration, and the smooth content is (D3): Lemma 5.2(ii)
applies and gives \(\ll|t|^{-1/6}P^{23/24+\varepsilon}\) per piece.
The weight sum is
\[
\sum_{t\ne0}\ \sum_{q_1+q_2+q_3=t}
\frac1{\pi^3\max(1,|q_1|)\max(1,|q_2|)\max(1,|q_3|)}
\,|t|^{-1/6}
\ll\sum_{t\ge1}\frac{\log^2(2{+}t)}{t^{7/6}}\ll1,
\]
so the total wave-piece contribution is
\(\ll P^{23/24+\varepsilon}\).

If \(t=0\): the wave content collapses exactly to differenced
waves — e.g. \(q(Y(n{+}d_2)-Y(n))=q\,W'(n)\) — i.e. to
(D1)-type resonant decorations of the remaining piece; these are
handled in Step 5. This exactness is the reason no near-resonant
analysis is ever needed for the wave frequencies: the resonant
combination is an identity, not an approximation.

*Step 5 (pieces without wave content: the anchor classes).*
The remaining pieces carry the anchor, at most two differenced-wave
modes \(u\,W\), \(u'W'\) (including the resonant remnants of
Step 4, which by Lemma 5.1(iii) are smooth-per-branch with sub-unit
\(\theta\)-coefficients), slow modes, and (D3)-smooth content.
Split by the anchor branch type.

**(5a) Offset branches (\(j\ne0\)).** The anchor curvature is,
by (E6) and the window-centre composite,
\[
\lambda_a=\tfrac{729}{512}\,k|j|\,n^{-1/8}\,(1+O(P^{-1/8}))
\ \in\ [1.2,\,1.5]\,k|j|P^{-1/8},
\]
where \(\tfrac{729}{512}=\tfrac{945}{512}-\tfrac{27}{64}\) is the
sum of the smooth part \((cF)''\) and the window-centre mode
\(uX''\) at \(u=-B(n_0)\): single-signed with ratio
\(\tfrac{945}{512}:\tfrac{27}{64}=4.375\) (machine gate m2 of
`kernel_margin_scan`). Every competitor is dominated at a displayed
margin: differenced-wave modes
\(\le0.84\,uh_1P^{-3/4}\le0.51P^{-1/4}\) (since \(uh_1\le0.6P^{1/2}\)),
ratio \(\le0.43P^{-1/8}\) against \(\lambda_a\ge1.2P^{-1/8}\);
resonant (D1) content \(\le6\,|q'|P^{-5/4}\cdot P^{1/16}\)-scale,
ratio \(\le5P^{-9/16}\); slow modes
\(\le3J_2|j|P^{-5/4}\), ratio \(\le8P^{1/24-9/8}\); (D3) content,
ratio \(\le3h_1h_2P^{-1/2}\le P^{-1/4}\). The \(\theta\)-sawtooth of
the anchor has coefficient \(\tfrac9{16}k|j|P^{3/8}\)-scale with
per-step drift \(\le0.2k|j|P^{-5/8}<1\): at most
\(1.2k|j|P^{3/8}{+}1\) windows of length \(\ge0.8P^{5/8}/(k|j|)\),
window-boundary cost
\(\le1.2k|j|P^{3/8}\cdot0.92(k|j|)^{-1/2}P^{1/16}
\le1.1(k|j|)^{1/2}P^{7/16}\). Off the collision band, window modes
\(w\) are dominated at margin \(\ge4\) either way and ride along or
are estimated by Lemma 3.3 at their own scale with \(1/|w{+}B_0|\)
weights (\(\ll P^{7/8}\log P\) in total); on the collision band
\(|wX''|\in[\tfrac14,4]\lambda_a\), Lemma 3.9 with
\((\alpha,\beta)=(\tfrac{15}8,\tfrac32)\) and
\(M\le1.5k|j|P^{-1/8}\) gives, per window and summed with the
\(O(\log P)\) band mass,
\(\ll\bigl((k|j|)^{1/2}P^{15/16}+(k|j|)^{-1/2}P^{1/16}
\cdot k|j|P^{3/8}+(k|j|)^{1/6}P^{1-3/16}
+(k|j|)^{-1/6}P^{1/2+3/16}\bigr)\log P
\ll(k|j|)^{1/2}P^{15/16}\log P\).
The main estimate is Lemma 3.3 per frozen run at scale
\(\lambda_a\): run lengths \(\ge\tfrac1{22}P^{1/4}/(|j|{+}1)\)
(Lemma 5.1(iii)), and
\(\lambda_a^{-1/2}\le0.92(k|j|)^{-1/2}P^{1/16}\ll\) run length, so
\[
\sum_{\text{runs}}\bigl(\ell\lambda_a^{1/2}+\lambda_a^{-1/2}\bigr)
\le1.3\,(k|j|)^{1/2}P^{15/16}
+21\,(|j|{+}1)|j|^{-1/2}k^{-1/2}P^{13/16}.
\]
Summed over the eight carry branches and \(|j|\le3\) with the
\(O(\log^3P)\) piece masses:
\(\ll(k)^{1/2}P^{15/16+\varepsilon}
\le1.8\,P^{1/48}P^{15/16+\varepsilon}=1.8\,P^{23/24+\varepsilon}\)
at \(k\le P^{1/24}\) — the absorbed \((k|j|)^{1/2}\) loss, exactly
at the bottleneck.

**(5b) Zero-offset branches (\(j=0\)).** Anchor curvature
\(\lambda_0\in[0.2,0.9]\,kh_1h_2P^{-5/8}\) (composite exponent
\(\tfrac{11}8\)), runs of length
\(\ge\tfrac1{22}P^{3/4}/(h_1h_2)\). Let
\(\mu=0.84\max(uh_1,u'h_2)P^{-3/4}\) be the strongest
differenced-wave scale present. Three regimes.

- *Anchor-dominant* (\(60\mu\le\lambda_0\)): Lemma 3.3 per run at
  \(\lambda_0\), all else dominated at margin \(\ge20\):
  \(\le1.3(kh_1h_2)^{1/2}P^{11/16}
  +49\,(h_1h_2/k)^{1/2}P^{9/16}\).
- *Mode-dominant* (\(\mu\ge60\lambda_0\), i.e.
  \(uh_1\ge60\,kh_1h_2P^{1/8}\)-form): Lemma 5.2(i) with the
  undifferenced anchor as decoration: its run boundaries number
  \(\le22h_1h_2P^{1/4}\le22P^{5/16}\), cost
  \(\le22P^{5/16}\cdot3.4(uh_1)^{-1/2}P^{3/8}\le75P^{11/16}\); its
  smooth part is dominated at margin \(\ge20\) by hypothesis; its
  \(\theta\)-coefficient \(\le1.2kh_1h_2P^{3/8}\le1.2P^{1/2}\)
  produces at most \(1.2P^{1/2}\) windows (boundary cost
  \(\le1.2P^{1/2}\cdot3.4(uh_1)^{-1/2}P^{3/8}\le4.1P^{7/8}
  (uh_1)^{-1/2}\)) whose centre modes \(w\) are treated exactly as
  in Lemma 5.2(i), Stage 5. Total
  \(\ll\bigl((uh_1)^{1/2}P^{5/8}+(h_1/u)^{1/2}P^{7/8}
  +P^{7/8}\bigr)P^{\varepsilon}\).
- *Middle band* (\(\tfrac1{60}\le\mu/\lambda_0\le60\); coefficient
  mass \(O(1)\) per layer): here up to three curvature scales meet
  — the \(u\)- and \(u'\)-modes merge into a single
  \(\nu^{3/4}\)-term with frozen coefficient
  \(\tfrac32(uG_1{+}u'G_2)\) per cell intersection (at most
  \(1.5(h_1{+}h_2)P^{1/2}{+}2\) cells), the anchor is the
  \(\nu^{11/8}\)-term, and the window modes are
  \(\nu^{3/2}\)-terms. Lemma 3.10 with
  \((\alpha,\beta,\gamma)=(\tfrac34,\tfrac{11}8,\tfrac32)\) and
  \(M\ge0.2kh_1h_2P^{-5/8}\ge0.2P^{-5/8}\) gives, per cell and
  summed,
  \[
  \ll\Bigl(P\,M^{1/2}
  +(h_1{+}h_2)P^{1/2}M^{-1/2}
  +P(M/P)^{1/6}+P^{1/2}(M/P)^{-1/6}
  +P(M/P^2)^{1/14}+P^{3/4}(M/P^2)^{-1/14}\Bigr)\log P,
  \]
  and with \(M\in[0.2P^{-5/8},1.35P^{-1/4}]\) every term is
  \(\le1.3P^{15/16}\): in order,
  \(\le1.2P^{7/8}\); \(\le2.3(h_1{+}h_2)P^{1/2+5/16}\le
  5P^{1/24+13/16}\le5P^{7/8}\); \(\le P^{1-13/48}\);
  \(\le1.3P^{1/2+13/48}\le1.3P^{37/48}\); \(\le P^{1-3/16}\);
  \(\le1.2P^{3/4+3/16}=1.2P^{15/16}\).

In all three regimes the \(j=0\) pieces total
\(\ll P^{15/16+\varepsilon}\ll P^{23/24}\).

*Step 6 (assembly).* Additive costs: the \(M_1\) deletion
(\(2.7P^{1/4}\)); majorants (\(\le3\) sawtooth layers at
\(4P/J_2=4P^{23/24}\) each, plus \(8P^{3/4}\), \(46P^{3/4}\), and
the displayed window residuals \(\le7P^{7/8}\)); flat costs
(\(\le46P^{3/4}\) per layer). Multiplicative costs: mode masses over
at most three expansion layers plus the shift devices,
\(O(\log^3P)=P^{\varepsilon}\). Piece totals: Step 4,
\(\ll P^{23/24+\varepsilon}\); Step 5a,
\(\le1.8P^{23/24+\varepsilon}\); Step 5b,
\(\ll P^{15/16+\varepsilon}\); slow modes and (D3) remnants,
\(\ll P^{7/8+\varepsilon}\). Hence
\(|T_2|\ll P^{23/24+\varepsilon}\), and by Step 1
\[
|T_1|^2\le2P^{2-1/24}+CP^{1+23/24+\varepsilon}
\ \Rightarrow\ |T_1|\ll P^{1-1/48+\varepsilon},
\qquad
|K_c|^2\le2P^{2-1/48}+CP^{2-1/48+\varepsilon},
\]
so \(|K_c|\ll P^{1-1/96+\varepsilon}\). Exponents deliberately
unoptimized. \(\square\)

Two remarks on the constants. First, the \(k\)-range is sharp for
this assembly: the class-(5a) loss \((k|j|)^{1/2}P^{15/16}\) meets
the wave-piece bottleneck \(P^{23/24}\) exactly at \(k=P^{1/24}\),
which is why the theorem is uniform on the original range with no
\(k\)-explicit statement needed. Second, the exponent
\(\tfrac1{96}=\tfrac14\cdot\tfrac1{24}\) traces entirely to the
depth-2 strength \(P^{23/24}\) of the exact level-2 waves
(Lemma 5.2(ii)); any improvement of the wave bound improves
\(\delta\) proportionally.

**Corollary 5.4 (low-exponent families).**
Fix a finite set
\(\mathcal A\subset(0,\tfrac98]\setminus\{\tfrac14,\tfrac34\}\).
The bound of Theorem 5.3 holds, with constants depending on
\(\mathcal A\), for every monomial-pattern family
\(c^{(r)}\asymp kP^{\alpha-r}\) with \(\alpha\in\mathcal A\),
uniformly for \(k\le P^{1/24}\).

*Proof.* Every constraint of the proof is monotone in \(\alpha\) on
\((0,\tfrac98]\): (C1) relaxes to \(kh_1h_2\le P^{5/4-\alpha}\), and
every coefficient size, window drift, and flat cost shrinks. The
anchor composites have exponents \(\alpha{+}\tfrac34\) (offset
branches) and \(\alpha{+}\tfrac14\) (zero-offset); the single-sign
requirement is \((\alpha{+}\tfrac34)(\alpha{-}\tfrac14)\ne0\) resp.
\((\alpha{+}\tfrac14)(\alpha{-}\tfrac34)\ne0\), i.e.
\(\alpha\notin\{\tfrac14,\tfrac34\}\). Where the window-centre
composite margin degenerates (the analogue of
\(\tfrac{945}{512}-\tfrac{27}{64}\) can vanish at one interior
\(\alpha_0=(\sqrt{10}-1)/4\)), the collision is covered by Lemma 3.9
with the pair \((\alpha{+}\tfrac34,\tfrac32)\), valid since
\(\alpha{+}\tfrac34\ne\tfrac32\) on \(\mathcal A\); Lemma 3.10 runs
with \((\tfrac34,\alpha{+}\tfrac14,\tfrac32)\), pairwise distinct
for \(\alpha\notin\{\tfrac14,\tfrac34\}\). The exponent sets
\(E\) of Lemmas 3.9–3.10 are enlarged to include
\(\alpha{+}\tfrac34\), \(\alpha{+}\tfrac14\) for
\(\alpha\in\mathcal A\), a finite set. \(\square\)

## 6. Applications: depth four complete, and deeper contracting words

**Theorem 6.1 (the OOO\* splits; depth four complete).**
For \(w\in\{OOOE,OOOO\}\),
\[
\#\{n\le N\ \text{odd}:\ \mathrm{word}_4(n)=w\}
=\tfrac N{16}+O\bigl(N^{1-1/96+\varepsilon}\bigr).
\]
Hence **every** itinerary word class of depth at most four satisfies
\(\#\{n\le N\}=2^{-|w|}N+O(N^{1-\delta_w})\) with explicit
\(\delta_w>0\): depth-4 parity equidistribution is complete.

*Proof.* The class indicator expands (Lemma 3.6, then Lemma 3.5 at
truncation \(J_3=P^{1/96}\), error \(P/J_3=P^{1-1/96}\)) into mode
sums
\(S_{ijk}=\sum_ne(\tfrac i2X+\tfrac j2Y+\tfrac k2v^{3/2})\) over
dyadic blocks. Three applications of the Taylor pattern of
Lemma 4.3(i), taken to second order, give the exact identity (odd
\(n\ge5\))
\[
v^{3/2}=-\tfrac5{64}n^{27/8}+\tfrac9{32}mn^{15/8}
-\tfrac{45}{64}m^2n^{3/8}+\tfrac{15}{64}vn^{9/8}
+\tfrac{45}{32}vmn^{-3/8}-\tfrac9{64}vm^2n^{-15/8}
+\mathrm{err},
\]
\(|\mathrm{err}|\le\tfrac34n^{-9/8}\): the fourth-letter phase is a
polynomial of degree \((2,1)\) in the integer pair \((m,v)\) with
smooth coefficients. Its \(v\)-linear part is \(vW\) with \(W\) in
the family of Theorem 5.3; the \(vm\)- and \(vm^2\)-cross terms
reduce to the same family by \(\xi vm=\xi X\,v-\xi\theta\,v\) and
\(\xi_2vm^2=\xi_2X^2\,v-2\xi_2X\theta\,v+\xi_2\theta^2v\), whose
\(\theta\)-cross coefficients are sub-unit and whose smooth
\(v\)-coefficients \(\xi X,\xi_2X^2\asymp kP^{9/8}\) are family
members. Writing \(v=Y-\theta_2\) splits each family term into a
smooth-in-\(m\) part and a kernel factor \(e(-c\,\theta_2)\). The
double differencing of Theorem 5.3 applied to the whole mode phase
carries the passengers along: the pure-\(m\) polynomial phases
difference into the anchor classes of Step 5 (their
\((\Delta\Delta\mu)m\) content is sub-unit under (C1), the crosses
are smooth per cell, and \(\mu\,\Delta\Delta m\) produces the
bounded-offset branch phases with curvature
\(\asymp k|j|P^{-1/8}\), single-signed by the same
monomial-exponent check); the \(\tfrac i2X\)- and
\(\tfrac j2Y\)-passengers difference to curvatures
\(\ll ih_1h_2P^{-5/2}\) and \(\asymp jh_1h_2P^{-5/4}\), each smaller
than every retained curvature scale of Step 5 by a fixed power of
\(P\), and the differenced \(\tfrac j2Y\)-passenger's wave content
is exactly a (D1) decoration; and the kernel factor is handled by
Steps 2–6 of Theorem 5.3 without change, since those steps use only
the derivative pattern of \(c\), not its specific form. Assembly and
summation over \(k\le J_3\) with \(1/k\)-weights give
\(\sum_k\tfrac1kP^{1-1/96}+P^{1-1/96}\ll P^{1-1/96+\varepsilon}\);
dyadic blocks sum to \(N^{1-1/96+\varepsilon}\). \(\square\)

The certified-descent density stays \(13/16\) at four steps —
\(OOO*\) is non-contracting at depth 4 (\(3^3>2^4\)) — but the
kernel theorem opens the contracting words at depths five, seven,
and eight.

**Theorem 6.2 (the length-5 contracting splits).**
\[
\#\mathrm{OOOEE}(N),\ \#\mathrm{OOOEO}(N)
=\tfrac N{32}+O\bigl(N^{1-1/96+\varepsilon}\bigr),
\qquad
\#\mathrm{OOEOE}(N),\ \#\mathrm{OOEOO}(N)
=\tfrac N{32}+O\bigl(N^{43/48+\varepsilon}\bigr).
\]

*Proof.* *OOOE\(*\).* The class indicator is the Theorem-6.1
indicator times \(\tfrac12(1\pm\psi(z^{1/2}))\), \(z=J^3(n)\):
branch-consistent by Lemma 3.6, since on the OOOE cylinder \(z\) is
even, so the fifth letter is the even-branch value. Vaaler-expand
the fifth wave at truncation \(P^{1/24}\). The Lemma 4.3(i) pattern
along the chain replaces \(\tfrac l2z^{1/2}\) by
\(\tfrac l2n^{27/16}-\tfrac{9l}{16}n^{3/16}\theta\) at absorbable
decaying cost. The \(\theta\)-sawtooth has coefficient
\(\asymp lP^{3/16}<P\); its shifted-window expansion (drift-1 length
\(P^{13/16}/l\), window \(T=P^{1/8}\ll lP^{3/16}\)) produces
\(X\)-modes of size \(\asymp lP^{3/16}\) — ordinary first-letter
passengers within Theorem 6.1's budget — and the smooth chirp
\(e(\tfrac l2n^{27/16})\) has curvature \(\asymp lP^{-5/16}\),
subdominant to every retained scale. Theorem 6.1 applies with these
passengers.

*OOEO\(*\).* On the OOEO cylinder the fifth-letter phase is
\(\tfrac k2w^{3/2}\) with \(w=J^3(n)\) odd. Exact linearization
writes it as \(\tfrac k2n^{27/16}-C\theta-B\theta_w\) with
\(B=\tfrac{3k}4v^{1/4}\asymp kn^{9/16}\),
\(C=\tfrac{9k}{16}n^{3/16}\), and \(\theta_w=\{v^{1/2}\}\). Expand
\(e(-B\theta_w)\) on drift-1 intervals of length \(P^{7/16}/k\)
(there are \(\asymp kP^{9/16}\) of them; window \(T_w=P^{1/4}\ll
kP^{9/16}\), majorant \(P^{3/4}\)). At frequency \(-B+t\),
\(|t|\le T_w\), the combined phase is
\(-\tfrac k4v^{3/4}+t\,v^{1/2}\) plus passengers; linearizing both
powers, the \(\theta\)-coefficients cancel at the window centre up
to a residual \(\asymp kn^{3/16}\), leaving one slow
\(\theta\)-sawtooth, expanded on the same intervals (window
\(P^{1/8}\), majorant \(P^{7/8}\)). The resulting smooth phase has
curvature
\(\lambda_2=(-\tfrac{297}{1024}+\tfrac{27}{128})k\,n^{-5/16}
(1+o(1))\asymp kn^{-5/16}\), single-signed since the two rational
coefficients do not cancel. Lemma 3.3 on each interval gives
\(\ll k^{-1/2}P^{9/32}\); over \(\asymp kP^{9/16}\) intervals,
\(S_k\ll k^{1/2}P^{27/32+\varepsilon}\). Balancing
\(J_5^{1/2}P^{27/32}=P/J_5\) at \(J_5=P^{5/48}\) gives
\(P^{43/48}\); dyadic blocks sum to \(N^{43/48+\varepsilon}\).
\(\square\)

**Theorem 6.3 (the length-7 engine splits).**
All eight classes
\[
\#\mathrm{OOEOO}{*}{*}(N),\ \#\mathrm{OOOEO}{*}{*}(N)
=\tfrac N{128}+O\bigl(N^{1-1/96+\varepsilon}\bigr).
\]

*Proof.* *OOEOO\(**\).* With \(w=J^3(n)\) odd,
\(p=\lfloor w^{3/2}\rfloor\), \(\theta_p=\{w^{3/2}\}\), the exact
rearrangement
\[
p^{3/2}=-\tfrac54v^{9/8}+\tfrac94w\,v^{5/8}
-\tfrac32w^{3/4}\theta_p+E,
\qquad
0\le E\le\tfrac38p^{-1/2}+\tfrac{45}{32}v^{1/8},
\]
obtained from two Taylor steps and the identity
\(\theta_w=v^{1/2}-w\), eliminates the supercritical naive
coefficient \(\tfrac94v^{5/8}\asymp n^{45/32}>n\) of \(\theta_w\);
the remaining sawtooth \(\theta_p\) has coefficient
\(\asymp n^{27/32}<n\) and derivative \(<1\). Expanding the smooth
powers of \(v\) by the linearization pattern: the first-letter
content is a chirp of curvature \(\asymp n^{17/32}\) (Lemma 3.3);
the leading \(\theta_2\)-content has coefficient
\(\asymp n^{33/32}\) — a family of Corollary 5.4 at
\(\alpha=\tfrac{33}{32}<\tfrac98\); the remaining
\(\theta_2\)-amplitudes are \(O(n^{9/32})\), inside the engine. The
integer block \(e(\xi w)\) with \(\xi\asymp n^{45/32}\) is handled
on frozen gap runs: on the OOEO cylinder \(U=v^{1/2}\) has
\(U''\asymp P^{-7/8}<1\), so \(\lfloor\Delta U\rfloor\) is constant
on runs of length \(\asymp P^{7/8}/h\), and per run
\(\Delta w=J_U+\kappa_w\) with \(J_U\) frozen, \(e(\xi J_U)\) a
smooth chirp, and \(\kappa_w\) an indicator weight — the
Lemma 5.1(iii) pattern one level up. The sawtooth \(\theta_p\)
expands on drift-1 intervals of length \(P^{5/32}\) with window
\(T\ll P^{27/32}\), producing \(X\)-modes within Theorem 6.2's
budget. The seventh letter is the even-branch square root of
\(q=\lfloor p^{3/2}\rfloor\), with decaying amplitudes only.
Theorem 6.2 applies as a passenger theorem.

*OOOEO\(**\).* The analogous rearrangement at base \(z^{1/2}\)
(\(s=\lfloor z^{1/2}\rfloor\):
\(s^{3/2}=-\tfrac12z^{3/4}+\tfrac32s\,z^{1/4}+E\)) plus the
\(z^{3/4}\to n^{81/32}\) linearization chain gives the same four
classes of terms — chirp, Corollary-5.4 family at
\(\alpha=\tfrac{33}{32}\), engine sawtooths, and an integer-\(s\)
block on \(\lfloor\Delta z^{1/2}\rfloor\)-runs of length
\(\asymp P^{5/16}\). Same classes of terms. In both cases the
binding budget is the Corollary-5.4 family (and, for the
\(OOOEO\)-prefix, the parent kernel budget of Theorem 6.1), i.e.
\(N^{1-1/96+\varepsilon}\); the engine's own \(N^{43/48}\) sits
below it. \(\square\)

**Theorem 6.4 (the length-8 engine quartet).**
The four contracting length-8 classes satisfy
\[
\#\mathrm{OOEOOEOE}(N),\ \#\mathrm{OOEOOOEE}(N),\
\#\mathrm{OOOEOEOE}(N),\ \#\mathrm{OOOEOOEE}(N)
=\tfrac N{256}+O\bigl(N^{1-1/96+\varepsilon}\bigr).
\]

*Proof.* These are exactly the contracting length-8
children of the classes counted by Theorem 6.3 (appending \(E\)
to the four five-odd words; the six-odd words need length
\(\ge10\)). Write \(x_1=n\) and \(x_{t+1}=\lfloor
x_t^{3/2}\rfloor\) or \(\lfloor x_t^{1/2}\rfloor\) as the letters
dictate; the eighth-letter wave has phase argument \(X_7\), the
real number with \(x_8=\lfloor X_7\rfloor\). On each of the four
parents, applying the two-term Taylor identity with one-signed
remainder at every one of the seven levels gives the exact chain
\[
X_7=n^{243/128}-\sum_iB_i(n)\,\theta_i+E,\qquad|E|<1
\ \ (n\ge51),
\]
with \(\theta_i\in[0,1)\) the level-\(i\) floor defect and every
coefficient subcritical: the complete inventory of growing
coefficients over the four words is
\(\tfrac{27}{16}x_3^{11/32}\asymp n^{99/128}\),
\(\tfrac32x_6^{1/4}\asymp n^{81/128}\),
\(\tfrac{81}{64}n^{51/128}\), and
\(\tfrac98x_4^{3/16}\) resp.\ \(\tfrac98x_4^{1/16}\asymp
n^{27/128}\); all other coefficients decay. The interleaved even
letters keep every intermediate state below the scale \(n^{9/4}\)
at which an odd letter would produce a supercritical
(kernel-class) coefficient — no letter of the quartet sees a
kernel. Every sawtooth has coefficient drift \(\le n^{-29/128}<1\):
expand each on drift-1 windows with budget \(T=P^{1/16}\)
(majorant \(P^{15/16}\)); the window-centre values recombine with
the smooth chirp \((k/2)n^{243/128}\), and the residual modes
carry curvature \(\le Tn^{-7/8}\), subdominant to the chirp
curvature \(\lambda\asymp kn^{-13/128}\). On the intersected
windows (length \(\ge n^{29/128}\gg\lambda^{-1/2}\)) Lemma 3.3
gives \(\ll k^{1/2}n^{45/256}\) per window, hence
\(S_k\ll k^{1/2}P^{243/256}\); balancing the Vaaler majorant
\(P/J_8\) at \(J_8=P^{13/384}\) gives \(P^{1-13/384}\) for the
eighth-letter wave. Letters one through seven ride as passengers
with the budgets of Theorems 6.1–6.3, and the parent budget
\(N^{1-1/96+\varepsilon}\) dominates. \(\square\)

**Corollary 6.5 (certified-descent densities \(7/8\), \(57/64\), and \(29/32\)).**
The class of starts carrying a uniform power-envelope descent
certificate of length at most five — evens, \(OE\), \(OOEE\),
\(OOOEE\), \(OOEOE\) — has natural density \(7/8\); adding the
length-7 words \(OOEOOEE\) and \(OOOEOEE\) raises the density of the
length-\(\le7\) certified class to \(57/64\); adding the length-8
quartet of Theorem 6.4 raises the length-\(\le8\) certified class
to \(29/32\).

*Proof.* Densities
\(\tfrac12+\tfrac14+\tfrac1{16}+\tfrac1{32}+\tfrac1{32}=\tfrac78\),
\(\tfrac78+\tfrac1{128}+\tfrac1{128}=\tfrac{57}{64}\), and
\(\tfrac{57}{64}+\tfrac4{256}=\tfrac{29}{32}\). The
cylinders are disjoint, and each new cylinder is counted with a
power saving by Theorems 6.2–6.4. Contraction is
Proposition 3.1: \(3^3=27<32=2^5\) on the length-5 words,
\(3^4=81<128=2^7\) on the length-7 words, and
\(3^5=243<256=2^8\) on the length-8 words. \(\square\)

The leftover \(\tfrac3{32}\) decomposes exactly: the \(OOOO*\)
tree (\(\tfrac1{16}\), blocked at its root by the level-3 kernel
of Section 7, first contracting word \(OOOOEEE\)), the expanding
\(O\)-children of the quartet splits (\(\tfrac4{256}\)), and the
two six-odd trees \(OOEOOOO*\), \(OOOEOOO*\) (\(\tfrac4{256}\)).
The split is structural: an odd letter applied at state scale
\(n^\sigma\) produces a letter-phase coefficient \(\asymp
n^{\sigma/2}\), the engine and Corollary 5.4 cover
\(\sigma\le9/4\), and even letters halve \(\sigma\) while odd
letters multiply it by \(3/2\). The non-\(OOOO\) leftover
therefore keeps thinning at every depth by further engine
theorems with diminishing increments, while the \(OOOO\) tree is
monolithically blocked by the level-3 kernel.

As with Corollary 4.2, these are densities of uniform
certificate classes. They are not densities of all descent
certificates and not densities of starts that reach \(1\).

## 7. The Terras-style reduction and the frontier

The depth-by-depth counting assembles into a conditional
Terras-style statement, and the reduction is unconditional:

**Proposition 7.1 (equidistribution implies density-one descent).**
Let \(d\ge1\) and suppose that for every itinerary word \(w\) of
length \(d\) (over all starts, first letter the parity of \(n\)),
\[
\bigl|\#\{n\le N:\mathrm{word}_d(n)=w\}-2^{-d}N\bigr|\le E_d(N).
\]
Then the starts with no contracting prefix of length \(\le d\) number
at most
\[
e^{-cd}\,N+2^dE_d(N),
\qquad
c=2\Bigl(\tfrac{\log2}{\log3}-\tfrac12\Bigr)^2>0.0342 .
\]
Every other start \(n\ge2\) satisfies \(J^t(n)<n\) for some
\(t\le d\) with the uniform power-envelope certificate of
Proposition 3.1. Consequently, if \(E_d(N)=O_d(N^{1-\delta_d})\) with
\(\delta_d>0\) for every \(d\), the set of starts admitting a finite
descent certificate has natural density \(1\).

*Proof.* A word \(w\) of length \(d\) has a contracting prefix iff
\(3^{o_t}<2^t\) for some \(t\le d\), where \(o_t\) counts odd letters
among the first \(t\). If \(w\) has no contracting prefix then
\(3^{o_d}\ge2^d\), i.e. \(o_d\ge\beta d\) with
\(\beta=\log2/\log3=0.6309\ldots\) The number of such words is at
most \(2^d\Pr[\mathrm{Bin}(d,\tfrac12)\ge\beta d]\le
2^de^{-2(\beta-1/2)^2d}\) by Hoeffding's inequality. Each word class
has at most \(2^{-d}N+E_d(N)\) members; summing over the
non-contracting words gives the count. The density-one statement
follows by letting \(d\to\infty\) slowly with \(N\) (any
\(d(N)\to\infty\) with \(2^dE_d(N)/N\to0\)). \(\square\)

Every E-rooted word has a contracting prefix at length one
(\(3^0<2\)), so the hypothesis only ever consumes O-rooted class
bounds. Sections 4–6 prove it *unconditionally at every depth
\(d\le4\)*, so the base cases of Proposition 7.1 are theorems. The
first open case is depth 5: the \(OOOO*\) split. It has an exact
shape, one nesting deeper than Theorem 5.3. Write
\(Z=v^{3/2}\), \(z=\lfloor Z\rfloor\), \(\theta_3=Z-z\); after four
odd letters the fifth is the parity of \(\lfloor z^{3/2}\rfloor\).

**Lemma 7.2 (level-3 kernel reformulation).**
For odd \(n\ge5\),
\[
\tfrac12\bigl(v^{9/4}-z^{3/2}\bigr)-\tfrac34\,z^{1/2}\theta_3=R_3,
\qquad
0\le R_3\le\tfrac3{16}\,z^{-1/2}.
\]
Consequently the fifth-letter phase is, up to \(kR_3\ll kn^{-27/16}\)
per term, the exponential sum of the level-3 local floor defect, with
coefficient \(c=\tfrac{3k}4z^{1/2}\asymp kn^{27/16}\): Lemma 5.1(i)
with \((m,v)\) replaced by \((v,z)\).

*Proof.* Taylor of \((z+\theta_3)^{3/2}\) at \(z\), with
\(Z^{3/2}=v^{9/4}\). \(\square\)

For smooth \(c\) with \(c\asymp kP^{27/16}\) and
\(c'\asymp kP^{11/16}\) on \(n\sim P\) (the \(z^{1/2}\)-shaped
family), define
\[
K_3(P)=\sum_{\substack{n\sim P\\ n\ \mathrm{odd}}}
e\bigl(c(n)\,\{\lfloor\lfloor
n^{3/2}\rfloor^{3/2}\rfloor^{3/2}\}\bigr).
\]

**Conjecture 7.3 (level-3 kernel cancellation).**
\(K_3(P)\ll P^{1-\delta}\) for some \(\delta>0\), uniformly over the
family above with \(k\le P^{\varepsilon}\).

The boundary between Theorem 5.3 and Conjecture 7.3 is quantitative
and sharper than a derivative count. The smooth model iterates: where
Theorem 5.3 used two Weyl differencings against
\(Y''\asymp P^{1/4}\gg1>P^{-3/4}\asymp Y'''\), the level-3 model
\(n^{27/8}\) has \(G'''\asymp P^{3/8}\gg1>P^{-5/8}\asymp G^{(4)}\)
and predicts three. But the prediction does not descend to the nested
floors. The kernel weight now has \(c'\asymp kP^{11/16}\gg1\), so no
drift-1 interval exists for any expansion of the weight itself; the
branch decomposition of Lemma 5.1(iii) has no analogue at the
\(v\)-level, because \(v\) jumps by \(\asymp n^{5/4}\) per step and
the branch set is a *product* of two carry lattices, not a copy of
one; and the forced inner linearization
\(v^{3/2}=m^{9/4}-\tfrac32m^{3/4}\theta_2+E_2\) trades \(\theta_3\)
for a sawtooth family at coefficient scale \(kn^{45/16}\), *above*
the \(9/4\) threshold where every method of this paper stops.

What survives at the frontier is a model problem and one theorem
about it. Stripping every problem-specific structure (carries,
defects, nesting) from \(K_3\) leaves the *amplitude-product* sums
\[
S=\sum_{t\le L}e\bigl(A(t)\,\{B(t)\}\bigr),
\qquad
1\ll A'\ll A,
\]
with smooth monomial-type \(A,B\) (the instance above has
\(A\asymp P^{27/16}\), \(A'\asymp P^{11/16}\)). For \(A'\ll1\)
partial summation makes the amplitude a tame passenger and the
classical single-floor machinery applies; for \(A'\gg1\) we
know of no nontrivial deterministic bound by any method. The generic
statement, however, is a theorem — and its proof uses no harmonic
analysis at all:

**Theorem 7.4 (shift-averaged square-root cancellation).**
Let \(A_1<\cdots<A_L\) be reals with
\(|A_t-A_{t'}|\ge A'_{\min}|t-t'|\) for some \(A'_{\min}\ge1\), and
let \(x_1,\ldots,x_L\) be arbitrary reals. For
\(S_\lambda=\sum_{t\le L}e\bigl(A_t\{x_t+\lambda\}\bigr)\),
\[
\Bigl|\int_0^1|S_\lambda|^2\,d\lambda-L\Bigr|
\le\frac6\pi\,\frac L{A'_{\min}}\,(\log L+1).
\]
In particular \(|S_\lambda|\le\sqrt{L/\varepsilon}\) outside a shift
set of measure \(\varepsilon(1+o(1))\): two-sided square-root
cancellation for almost every shift of the fractional argument,
regardless of the sequence \(B\).

*Proof.* Expand the square; the diagonal gives \(L\). For
\(t\ne t'\), the function
\(\varphi(\lambda)=A_t\{x_t+\lambda\}-A_{t'}\{x_{t'}+\lambda\}\) is
piecewise linear on \([0,1)\) with *real* slope \(A_t-A_{t'}\) on at
most three arcs (jumps at \(1-\{x_t\}\) and \(1-\{x_{t'}\}\)); on
each arc \(|\int e(\varphi)\,d\lambda|\le1/(\pi|A_t-A_{t'}|)\).
Summing,
\(\sum_{t\ne t'}3/(\pi A'_{\min}|t-t'|)
\le(6/\pi)(L/A'_{\min})(\log L+1)\). \(\square\)

The mechanism deserves note: the amplitude separation \(A'\gg1\) —
the very property that defeats every character expansion, since a
Fourier window centred at the amplitude drifts by \(A'\) harmonics
per step — is exactly what makes the shift average trivial. What
remains of Conjecture 7.3 after Theorem 7.4 is a de-randomization:
the deterministic sum is the single shift \(\lambda=0\) in a family
that cancels almost surely.

**Conjecture 7.5 (the pure amplitude-product model).**
\(|S|\le L^{1-\delta}\) for some \(\delta>0\), for smooth
monomial-type \(A,B\) with \(1\ll A'\ll A\) as above.

Three structural facts locate the difficulty of the
de-randomization. No second averaging variable exists: amplitude
separation forces any two sample points with \(|A(p)-A(q)|\le1\) to
coincide, and every family average available in the application
re-enters either the differenced-kernel class or the
amplitude-product class itself. The inverse theory is self-similar:
any concentration or discrepancy inverse for \(A\{B\}\bmod1\) is a
statement about \(\sum e(jA\{B\})\) — the same class with amplitude
\(jA\) — so the class is closed under its own inverse theorems and
no bootstrapping is possible. And the metric statement does not
transfer: \(|dS_\lambda/d\lambda|\le2\pi A_{\max}L\) almost
everywhere, so \(S_\lambda\) decorrelates at shift scale
\(1/A_{\max}\), and an almost-all-\(\lambda\) theorem leaves
\(\asymp\varepsilon A_{\max}\) exceptional cells among
\(\asymp A_{\max}\) — no measure argument pins \(\lambda=0\). The
deterministic content of Conjecture 7.5 is a
specific-point-in-metric-theory problem, the same species as the
normality of \(\sqrt2\): a class whose known successes all use
special arithmetic.

Two analytic shortcuts around Conjecture 7.3 fail at recorded
points, and we state them once: composing gap cells across two
levels fails because on a cell where the first-level gap is constant
the second-level gap still takes a new value at essentially every
point, so no usable sub-cell survives; and reindexing by the image
\(m\) strips one nesting level but introduces a fiber indicator of
density \(\asymp m^{-1/3}\), whose sawtooth requires savings beyond
the exponent \(1/3\) while the engine saves only \(1/24\). A fuller
account of parked routes lives in the companion repository, not
here.

The open question, stated once:

> It is open whether almost every odd-to-odd start has a finite
> descent certificate. By Proposition 7.1 that would follow from
> all-depth parity equidistribution, which is now a theorem through
> depth four; the first open case is the \(OOOO*\) kernel of
> Conjecture 7.3, whose model form cancels for almost every shift
> (Theorem 7.4) and whose deterministic instance is Conjecture 7.5.

![The theorem flow of the paper. The exact finite-word calculus of the companion manuscript feeds the contraction certificates; the discrepancy calculus with the kernel theorem counts every itinerary class through depth four and the contracting words of lengths five through eight (certified density 29/32), leaving the level-3 kernel — generically cancelling by the shift-average theorem — and with it almost-all descent, open.](figures/juggler_frontier.png){width=100%}

## 8. Software note

A repository accompanies the paper:
[https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).
It is not required to read or check any proof above. It contains Lean
formalizations of the exact floor identities cited in Section 1.1 and
of the companion manuscript's finite-word theorems, scaled-integer
validations of the linearization identities of Lemmas 4.3, 4.6, 5.1,
and 7.2 and of the eighth-letter chain of Theorem 6.4, and exact-phase
numerical probes of the sums \(K_c\), \(K_3\), and the differenced
sums of Lemma 5.2 and Theorem 5.3, all of which exhibit cancellation
at square-root scale — stronger than the theorems claim and stronger
than they need. Probes and validations are checks, not proofs, and no
statement in this paper depends on them.

## Acknowledgments

I used large language models extensively while drafting and revising
the text, organizing companion notes, and as an interactive assistant
for Lean statements, tests, and literature records. The models are
not authors. The theorems of this paper are human proofs from the
cited classical inequalities; the Lean certificates cover only the
exact floor identities and the companion's finite-word theorems. I
take full responsibility for the contents.

## References

1. C. A. Pickover, *Computers and the Imagination: Visual Adventures Beyond
   the Edge*, St. Martin's Press, New York, 1991, ch. 40, p. 232.
2. OEIS Foundation Inc., “Juggler sequence: if \(n\) even then
   \(\lfloor\sqrt n\rfloor\) else \(\lfloor n^{3/2}\rfloor\),”
   Sequence A094683 in *The On-Line Encyclopedia of Integer Sequences*,
   https://oeis.org/A094683 (accessed 28 August 2026).
3. J. C. Lagarias, “The \(3x+1\) problem and its generalizations,”
   *Amer. Math. Monthly* 92 (1985), 3–23.
   [doi:10.1080/00029890.1985.11971528](https://doi.org/10.1080/00029890.1985.11971528).
4. R. Terras, “A stopping time problem on the positive integers,”
   *Acta Arith.* 30 (1976), 241–252.
   [doi:10.4064/aa-30-3-241-252](https://doi.org/10.4064/aa-30-3-241-252).
5. C. J. Everett, “Iteration of the number-theoretic function
   \(f(2n)=n\), \(f(2n+1)=3n+2\),” *Adv. Math.* 25 (1977), 42–45.
   [doi:10.1016/0001-8708(77)90087-1](https://doi.org/10.1016/0001-8708(77)90087-1).
6. T. Tao, “Almost all orbits of the Collatz map attain almost bounded
   values,” *Forum Math. Pi* 10 (2022), e12.
   [doi:10.1017/fmp.2022.8](https://doi.org/10.1017/fmp.2022.8).
7. V. Prasad and M. A. Prasad, “Estimates of the maximum excursion
   constant and stopping constant of juggler-like sequences,”
   ResearchGate preprint, 2025.
   [doi:10.13140/RG.2.2.14110.04168](https://doi.org/10.13140/RG.2.2.14110.04168).
8. L. Kuipers and H. Niederreiter, *Uniform Distribution of Sequences*,
   Wiley-Interscience, New York, 1974.
9. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, American
   Mathematical Society Colloquium Publications 53, Providence, RI, 2004.
10. J. D. Vaaler, “Some extremal functions in Fourier analysis,”
    *Bull. Amer. Math. Soc. (N.S.)* 12 (1985), 183–216.
    [doi:10.1090/S0273-0979-1985-15349-2](https://doi.org/10.1090/S0273-0979-1985-15349-2).
11. S. W. Graham and G. Kolesnik, *Van der Corput's Method of
    Exponential Sums*, London Mathematical Society Lecture Note
    Series 126, Cambridge University Press, Cambridge, 1991.
12. I. I. Piatetski-Shapiro, “On the distribution of prime numbers in
    sequences of the form \(\lfloor f(n)\rfloor\),” *Mat. Sb.* 33
    (1953), 559–566.
13. D. Leitmann, “The distribution of prime numbers in sequences of
    the form \(\lfloor f(n)\rfloor\),” *Proc. London Math. Soc. (3)*
    35 (1977), 448–462.
14. J. Rivat and P. Sargos, “Nombres premiers de la forme
    \(\lfloor n^c\rfloor\),” *Canad. J. Math.* 53 (2001), 414–433.
15. J. Rivat and J. Wu, “Prime numbers of the form
    \(\lfloor n^c\rfloor\),” *Glasg. Math. J.* 43 (2001), 237–254.
16. C. Mauduit and J. Rivat, “Propriétés \(q\)-multiplicatives de la
    suite \(\lfloor n^c\rfloor\), \(c>1\),” *Acta Arith.* 118 (2005),
    187–203.
17. J. F. Morgenbesser, “The sum of digits of
    \(\lfloor n^c\rfloor\),” *Acta Arith.* 148 (2011), 367–393.
    [doi:10.4064/aa148-4-4](https://doi.org/10.4064/aa148-4-4).
18. R. C. Baker, W. D. Banks, J. Brüdern, I. E. Shparlinski, and
    A. J. Weingartner, “Piatetski-Shapiro sequences,” *Acta Arith.*
    157 (2013), 37–68.
19. A. G. Abercrombie, “Beatty sequences and multiplicative number
    theory,” *Acta Arith.* 70 (1995), 195–207.
20. W. D. Banks and I. E. Shparlinski, “Short character sums with
    Beatty sequences,” *Math. Res. Lett.* 13 (2006), 539–547.
21. D. Glasscock, “Solutions to certain linear equations in
    Piatetski-Shapiro sequences,” *Acta Arith.* 177 (2017), 39–52.
22. P. Cochin, “Power envelopes, exact defects, and cycle
    restrictions for the Juggler map,” companion manuscript, 2026.
