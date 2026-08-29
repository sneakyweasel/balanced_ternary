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
bound for that kernel, by double Weyl differencing over an exact
carry-branch decomposition, with a targeted third differencing for the
mixed pieces (Lemma 5.2).

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
   We prove \(K_c(P)\ll P^{1-1/72+\varepsilon}\) by double Weyl
   differencing over an exact carry-branch decomposition
   (Lemma 5.1), with a targeted third differencing for the mixed
   pieces (Lemma 5.2). This is the hardest result of the paper, and
   Section 5 is written so that it can be checked without reference to
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
The next lemma collects the exact reductions behind its treatment:
the kernel phase is the level-2 local floor defect; the second
difference of the level-2 integer obeys an exact floor identity; and
on an explicit carry-branch decomposition that second difference is
a smooth function with a frozen floor.

**Lemma 5.1 (level-2 defect, double gap, and branch freeze).**
Fix shifts \(d_1=2h_1\), \(d_2=2h_2\) and write \(\Delta_1\),
\(\Delta_2\), \(\Delta\Delta\) for the corresponding difference
operators in \(n\), and \(W=\Delta_1Y\).

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
\(m+b_1+\kappa_1\), \(m+b_2+\kappa_2\), \(m+b_{12}+\kappa_{12}\). On
each \(b\)-run intersection and carry branch,
\[
\Delta\Delta Y=F_{\boldsymbol\kappa}(m),
\qquad
F_{\boldsymbol\kappa}(m)=(m{+}b_{12}{+}\kappa_{12})^{3/2}
-(m{+}b_1{+}\kappa_1)^{3/2}-(m{+}b_2{+}\kappa_2)^{3/2}+m^{3/2}
\]
exactly. The net offset
\(j=(b_{12}{+}\kappa_{12})-(b_1{+}\kappa_1)-(b_2{+}\kappa_2)\)
satisfies \(|j|\le3\) for \(h_1h_2\le P^{1/2}/3\), and
\[
F_{\boldsymbol\kappa}\asymp\tfrac32|j|P^{3/4}+h_1h_2P^{1/4},
\qquad
F_{\boldsymbol\kappa}'(m)\asymp|j|P^{-3/4}+h_1h_2P^{-5/4}<1,
\]
so \(\lfloor F_{\boldsymbol\kappa}(X(n))\rfloor\) is constant on runs
of length \(\asymp\min(P^{1/4}/|j|,\,P^{3/4}/(h_1h_2))\). The branch
indicator is a finite union of arcs in the single variable \(\theta\)
with slowly moving endpoints (drifts \(\asymp hP^{-1/2}\)): exactly
the moving-endpoint pattern of Step 4 of Theorem 4.4, absorbed by the
same exact shift device at \(O(\log P)\) mode-mass cost.

*Proof.* (i) Taylor of \((v+\theta_2)^{3/2}\) at \(v\), with
\(Y^{3/2}=m^{9/4}\). (ii) The gap identity of Lemma 4.3(ii) applied
twice — to \(Y\) at shift \(d_1\), then to the real sequence
\(n\mapsto W(n)\) at shift \(d_2\), with \(\Delta_2W=\Delta\Delta Y\);
the sawtooth form of the carry is the Lean-verified floor-carry
identity rearranged. (iii) The corner identities are Lemma 4.3(ii) at
the three shifts. The offset bound follows from
\(|\Delta\Delta X|\le4h_1h_2\sup|X''|=3h_1h_2P^{-1/2}\). The
derivative bound is the mean value theorem on the second difference
of \(\tfrac32m^{1/2}\) plus \(\tfrac34j(m+\xi)^{-1/2}\). \(\square\)

One warning, essential to the organization: \(\lfloor\Delta\Delta
Y\rfloor\) itself is *not* frozen. The level-1 carry toggles at
essentially every step and shifts \(\Delta\Delta Y\) by
\(\tfrac32j_1m^{1/2}\), a jump of size \(\asymp P^{3/4}\). The branch
decomposition of (iii), which carries the flicker inside the
indicator over the eight carry branches, is therefore forced: no
decomposition conditioning on the *values* of the level-1 gaps
produces sets on which the second difference is smooth.

The proof of the kernel theorem classifies the differenced pieces
into four classes; three are handled by standard tests, and the
fourth — a frozen floor multiplied by a large regenerated mode — is
the genuinely new difficulty. We isolate it as a standalone lemma
with its own differencing, so that it can be checked independently.

**Lemma 5.2 (the mixed-piece bound).**
Let \(P\ge2\), \(k\le P^{1/24}\), \(|j|\le3\), and \(h_1,h_2\ge1\)
with \(kh_1h_2\le P^{1/8}\). Let \(c\) be as in Theorem 5.3, let
\(F=F_{\boldsymbol\kappa}\) be a branch function of Lemma 5.1(iii)
with offset \(j\), let \(r\) be an integer with \(1\le r\le P^{1/16}\),
let \(s\in\mathbb R\) with \(|s|\asymp rP^{3/4}\), and let \(\varphi\)
be smooth with \(|\varphi''|\ll kh_1h_2P^{-5/8}\) and
\(|\varphi'''|\ll kh_1h_2P^{-13/8}\). Then
\[
U:=\sum_{\substack{n\sim P\\ n\ \mathrm{odd}}}
e\bigl(s\,X(n)-c(n)\lfloor F(X(n))\rfloor+\varphi(n)\bigr)
\;\ll\; r^{1/6}\,P^{7/8+\varepsilon}.
\]

*Proof.* Apply one further Weyl differencing with shift \(2h_3\),
\(h_3\le H_3:=\lceil r^{-1/3}P^{1/4}\rceil\):
\[
|U|^2\ll\frac{P^2}{H_3}
+\frac P{H_3}\sum_{1\le h_3\le H_3}|U_3(h_3)|,
\qquad
U_3=\sum_n e\bigl(\Delta_3\Phi(n)\bigr),
\]
where \(\Phi\) is the phase of \(U\) and \(\Delta_3\) is the
difference at shift \(2h_3\). We show
\(|U_3|\ll(rh_3)^{1/2}P^{5/8+\varepsilon}\) for each \(h_3\); the
lemma then follows from
\[
|U|^2\ll\frac{P^2}{H_3}+r^{1/2}H_3^{1/2}P^{13/8+\varepsilon}
\ll r^{1/3}P^{7/4+\varepsilon}
\quad\text{at}\quad H_3=r^{-1/3}P^{1/4}.
\]

*The main curvature.* \(\Delta_3(sX)''=s\,\Delta_3(X'')\), and since
\(X'''=-\tfrac38n^{-3/2}\) has fixed sign,
\(|\Delta_3(sX)''|\asymp|s|h_3P^{-3/2}\asymp rh_3P^{-3/4}\) with a
single sign determined by the signs of \(s\) and \(X'''\). It is
sub-unit: \(rH_3P^{-3/4}=r^{2/3}P^{-1/2}\le P^{-1/2+1/24}<1\).

*The floor content.* Split \(\lfloor F\rfloor=F-\{F\}\), so
\[
\Delta_3\bigl(c\lfloor F\circ X\rfloor\bigr)
=\Delta_3\bigl(cF\circ X\bigr)
-c\,\Delta_3\{F\circ X\}
-(\Delta_3c)\,\{F(X(n{+}2h_3))\}.
\]
Each of the three terms is handled in turn; throughout, write
\(F\) for \(F\circ X\), a slow function: \(F'\ll|j|P^{-1/4}
+h_1h_2P^{-3/4}\) and \(F''\ll|j|P^{-5/4}\).

(a) *The smooth term.* \((cF)''\asymp k|j|P^{-1/8}+kh_1h_2P^{-5/8}\)
and \((cF)'''\asymp k|j|P^{-9/8}+kh_1h_2P^{-13/8}\), so
\(|(\Delta_3(cF))''|\ll h_3\sup|(cF)'''|\ll h_3k|j|P^{-9/8}\ll
k|j|P^{-7/8}\). Against the main curvature \(rh_3P^{-3/4}\ge
P^{-3/4}\), the ratio is \(\ll k|j|P^{-1/8}\le3P^{1/24-1/8}\to0\):
dominated. The same computation with \(\varphi\) in place of \(cF\)
uses the hypothesis on \(\varphi'''\) and is smaller still.

(b) *The differenced sawtooth.* \(\Delta_3\{F\}=\Delta_3F
-\Delta_3\lfloor F\rfloor\), and by the gap identity
(Lemma 4.3(ii) applied to the sequence \(F\)),
\(\Delta_3\lfloor F\rfloor=\lfloor\Delta_3F\rfloor+\kappa_F\) with
\(\kappa_F\in\{0,1\}\). Here \(|\Delta_3F|\ll h_3(|j|P^{-1/4}
+h_1h_2P^{-3/4})\ll P^{1/4}\cdot P^{-1/4}=O(1)\), so
\(\lfloor\Delta_3F\rfloor\) takes \(O(1)\) values, on level sets
whose boundaries move with the slow function \(\Delta_3F\) (drift
per step \(\ll h_3\sup|(F\circ X)''|\ll h_3|j|P^{-5/4}\le3P^{-1}\));
the term \(c\,\Delta_3F\) is smooth
with third-derivative ratio to the main curvature \(\to0\) as in
(a); the term \(c\lfloor\Delta_3F\rfloor\) contributes, per level
set, the phase \(-qc(n)\) with \(q=O(1)\), of curvature
\(\ll kP^{-7/8}\le P^{1/24-7/8}\ll P^{-3/4}\): dominated. The carry
\(\kappa_F=\{F\}+\{\Delta_3F\}-\{F+\Delta_3F\}\) is a difference of
unit sawtooths in slow variables (drifts \(<1\) per step by the
bounds on \(F'\)); each expands by Lemma 3.5 at truncation
\(P^{1/16}\) (majorant cost \(P^{1-1/16}\), inside the target) into
modes \(e(q'F)\) with \(O(\log P)\) mass, and each mode phase
\(q'F\) has curvature \(q'\,|(F\circ X)''|\ll P^{1/16}|j|P^{-5/4}
\ll P^{-3/4}\): dominated.

(c) *The coefficient term.* \(\Delta_3c\asymp kh_3P^{1/8}\) may
exceed \(1\), but its derivative \((\Delta_3c)'\asymp kh_3P^{-7/8}\)
is sub-unit, so \(\Delta_3c\) drifts by at most \(1\) on windows of
length \(P^{7/8}/(kh_3)\), of which there are \(\asymp kh_3P^{1/8}\).
On each window, freeze \(\Delta_3c\) at its centre value \(B_0\);
the residual \(e(-(\Delta_3c-B_0)\{F\})\) has total variation
\(O(1)\) on the window and is removed by partial summation. Expand
\(e(-B_0\{F\})\) in Fourier modes of \(F\) (Vaaler truncation
\(|q''+B_0|\le P^{1/16}\), majorant cost \(P^{1-1/16}\) summed over
windows): each retained mode phase \(q''F\) has curvature
\(\ll(kh_3P^{1/8}+P^{1/16})\,|j|P^{-5/4}
\ll P^{1/24+1/4+1/8}\cdot3P^{-5/4}\ll P^{-3/4}\): dominated.

*Conclusion.* After (a)–(c), every piece of \(U_3\) is an
exponential sum whose second derivative is
\(\asymp rh_3P^{-3/4}\) with a single sign (the main curvature, with
every competitor smaller by a fixed power of \(P\)), possibly
multiplied by \(O(\log P)\)-mass mode weights and \(O(1)\)-variation
window factors. Lemma 3.3 over the full block gives, per piece,
\[
\ll P\,(rh_3P^{-3/4})^{1/2}+(rh_3P^{-3/4})^{-1/2}
\ll(rh_3)^{1/2}P^{5/8}+P^{3/8},
\]
and the mode masses and majorant costs multiply this by
\(P^{\varepsilon}\) and add \(P^{1-1/16}\), both inside the claimed
bound. \(\square\)

The reader may check the balance: with the trivial bound
\(|U_3|\le P\) the differencing would return \(|U|\ll P/H_3^{1/2}\),
i.e. nothing beyond the choice of \(H_3\); the content of the lemma
is that the floor and coefficient bookkeeping in (a)–(c) survives the
third differencing with the main curvature intact, which is what
fails if one attempts the third-derivative test per frozen run
instead (the run length \(P^{1/4}\) is too short: the test's second
term, summed over \(P^{3/4}\) runs, returns the trivial bound). That
failure is why the differencing must be *targeted at the piece*, not
applied per run.

**Theorem 5.3 (kernel cancellation).**
Let \(c\) be smooth on \((P,2P]\) with \(c^{(r)}\asymp kP^{9/8-r}\)
for \(r=0,\ldots,4\), derivative signs following the monomial pattern
(e.g. \(c=\tfrac{3k}4n^{9/8}\)). Then
\[
K_c(P)\ll P^{1-\delta+\varepsilon},
\qquad
\delta=\tfrac1{64}\ \text{for}\ k\ll P^{\varepsilon},
\qquad
\delta=\tfrac1{72}\ \text{uniformly for}\ k\le P^{1/24}.
\]

*Proof.* Work on a dyadic block \(n\sim P\), odd.

*Step 1 (double Weyl differencing).* With \(H_1=P^a\), \(H_2=P^b\)
chosen in Step 6,
\[
|K_c|^2\ll\frac{P^2}{H_1}+\frac P{H_1}\sum_{h_1\le H_1}|T_1(h_1)|,
\qquad
|T_1|^2\ll\frac{P^2}{H_2}+\frac P{H_2}\sum_{h_2\le H_2}|T_2(h_1,h_2)|,
\]
where \(T_2=\sum_ne(\varphi_2)\) and
\(\varphi_2=\Delta\Delta(c\,\theta_2)
=\Delta\Delta(cY)-\Delta\Delta(cv)\): an exact split into a
real-analytic block and an integer block.

*Step 2 (exact product rule).* For both blocks,
\[
\Delta\Delta(cf)=c_{11}\,\Delta\Delta f
+(\Delta_2c)(n{+}d_1)\,\Delta_1f
+(\Delta_1c)(n{+}d_2)\,\Delta_2f
+(\Delta\Delta c)\,f,
\]
with \(\Delta_ic\asymp kh_iP^{1/8}\) and
\(\Delta\Delta c\asymp kh_1h_2P^{-7/8}\). Here \(c_{11}\) denotes the
doubly shifted weight.

*Step 3 (the \(Y\)-block).* Split into the \(O((h_1{+}h_2)P^{1/2})\)
cell intersections of Lemma 4.3(ii); within a cell every shifted
\(Y\)-value is a smooth function of the single variable
\(m=X-\theta\), so no \(\Delta\theta\) cross-terms arise.

- \((\Delta\Delta c)\,Y\): smooth part of curvature
  \(\asymp kh_1h_2P^{-5/8}\); the \(\theta\)-coefficient
  \(\tfrac32(\Delta\Delta c)X^{1/2}\asymp kh_1h_2P^{-1/8}\) is
  sub-unit under the standing constraint
  \[
  \text{(C1)}\qquad kh_1h_2\le P^{1/8},
  \]
  so the sawtooth is expanded in Fourier modes of \(\theta\) at
  multiplicative mode-mass cost \(O(\log P)\), not absorbed.
- \((\Delta_2c)\,\Delta_1Y\) and its mirror: on the cell
  \(\Delta_1Y=(m{+}G_1)^{3/2}-m^{3/2}\); the \(\theta\)-coefficient
  is \(\asymp(\Delta_2c)\,G_1X^{-1/2}\asymp kh_1h_2P^{-1/8}<1\)
  under (C1), the smooth curvature \(\asymp kh_1h_2P^{-5/8}\).
- \(c_{11}\,\Delta\Delta Y\): split over the branches of
  Lemma 5.1(iii). Per branch with net offset \(j\), the smooth part
  \(c\,F_{\boldsymbol\kappa}(X)\) has curvature
  \(\asymp k|j|P^{-1/8}+kh_1h_2P^{-5/8}<1\) and combines with the
  frozen floor of Step 4 into the per-run phase of class (i) below;
  the \(\theta\)-content \(cF'\theta\) has coefficient
  \(\asymp k|j|P^{3/8}+kh_1h_2P^{-1/8}\) with window drift
  \((cF')'\asymp k|j|P^{-5/8}<1\), so a shifted-window expansion
  produces \(X\)-modes of size \(s\asymp k|j|P^{3/8}\) with curvature
  \(sX''\asymp k|j|P^{-1/8}<1\), handled by Lemma 3.3.

*Step 4 (the \(v\)-block).* \(v\) is an integer, so no fractional
part of \(c\) is ever split off.

- \((\Delta\Delta c)\,v=(\Delta\Delta c)(Y-\theta_2)\): the
  \(Y\)-part as in Step 3; the \(\theta_2\)-part has coefficient
  \(\asymp kh_1h_2P^{-7/8}<1\).
- \((\Delta_2c)\,\Delta_1v\): by Lemma 4.3(ii) applied to \(Y\),
  \(\Delta_1v=\lfloor W\rfloor+\kappa_2=W-\{W\}+\kappa_2\). The
  piece \((\Delta_2c)\,W\) is smooth per cell (curvature
  \(\asymp kh_1h_2P^{-5/8}\), \(\theta\)-coefficient
  \(\asymp kh_1h_2P^{-1/8}<1\)). The sawtooth
  \(-(\Delta_2c)\,\{W\}\) has window drift
  \((\Delta_2c)'\asymp kh_2P^{-7/8}<1\) and expands into \(W\)-modes
  \(r\lesssim kh_2P^{1/8}\), each again smooth per cell
  (\(\theta\)-coefficient \(\asymp rh_1P^{-1/4}\le
  kh_1h_2P^{-1/8}<1\), curvature \(\asymp kh_1h_2P^{-5/8}\)). The
  carry factor \(e((\Delta_2c)\kappa_2)=1+\kappa_2
  (e(\Delta_2c)-1)\) is an indicator weight times a smooth factor;
  \(\kappa_2=\{Y\}+\{W\}-\{Y{+}W\}\) (Lemma 5.1(ii)) expands into
  unit sawtooths of \(Y\)-, \(W\)-, and \(Y{+}W\)-forms with
  \(O(1)\) coefficients — Vaaler windows \(|r|\le R\),
  \(R=P^{\rho}\), majorant error \(P/R\) per layer. The \(Y\)-modes
  linearize (Lemma 4.3(i) with base \(Y\)) to \(X\)-modes of size
  \(s\asymp rP^{3/4}\) and curvature \(sX''\asymp rP^{1/4}\gg1\):
  pieces without a frozen-floor factor take the third-derivative
  test over full ranges (\(\lambda_3=sX'''\asymp rP^{-3/4}<1\),
  saving \(P^{1/8}/r^{1/6}\)); pieces riding a frozen floor are the
  mixed class, Lemma 5.2.
- \(c_{11}\,\Delta\Delta v=c_{11}\,\Delta_2g_2\): Lemma 5.1(ii). Per
  branch of Lemma 5.1(iii), the frozen integer
  \(J_F=\lfloor F_{\boldsymbol\kappa}(X(n))\rfloor\) (boundary
  toggles are slow-sawtooth indicators in \(\{F(X)\}\) and
  \(\theta\)) combines with the \(c_{11}\Delta\Delta Y\)-content of
  Step 3 into the smooth per-run phase
  \(c\,(F_{\boldsymbol\kappa}-J_F)\), of curvature
  \(\asymp k|j|P^{-1/8}+kh_1h_2P^{-5/8}<1\), single-signed per
  branch (class (i)); per frozen run and summed over runs this
  gives
  \[
  \ll(k|j|)^{1/2}P^{15/16}+|j|^{3/2}k^{-1/2}P^{13/16}
  \quad(j\ne0),
  \qquad
  \ll(kh_1h_2)^{1/2}P^{11/16}+(h_1h_2/k)^{1/2}P^{9/16}
  \quad(j=0).
  \]
  The carries \(\kappa''\) (\(W\)- and \(\Delta W\)-content only:
  slow modes, class (ii)) and \(\Delta_2\kappa_2\)
  (\(\theta_2\)-content: classes (iii)–(iv)) are indicator weights
  times \(e(\mp c)\), the latter smooth of curvature
  \(c''\asymp kP^{-7/8}\).

*Step 5 (dominance and mode assembly).* The final pieces fall into
four classes.

- **(i) Pure smooth pieces**, curvature
  \(\lambda_2\asymp k|j|P^{-1/8}\) or \(kh_1h_2P^{-5/8}\): the
  leading curvature per branch is a genuine double difference of a
  single smooth function per run (the \(c_{11}\Delta\Delta Y\)- and
  \(-c\lfloor\Delta\Delta Y\rfloor\)-contents combine per run into
  \(c\,(F_{\boldsymbol\kappa}-J_F)\)), so the double mean value
  theorem gives a single sign. For the monomial-pattern family the
  composite sign check is
  \(\alpha(\alpha{-}1)(\alpha{+}\beta{-}2)(\alpha{+}\beta{-}3)>0\)
  at \(\alpha=\tfrac98\) with \(\beta=\tfrac34\) (offset branches,
  \(cF\asymp k\,|j|\,n^{15/8}\)) and \(\beta=\tfrac14\) (zero-offset
  composites, \(cF\asymp kh_1h_2n^{11/8}\)): the composite exponents
  \(\tfrac{15}8,\tfrac{11}8\notin\{0,1,2\}\), so no factor
  vanishes. Per-run application of Lemma 3.3 is legitimate because
  \(\lambda_2^{-1/2}\asymp P^{1/16}\ll P^{1/4}\asymp\) run length;
  the saving is \(\ge P^{1/16}/(k|j|)^{1/2}\).
- **(ii) Slow-mode pieces** (\(W\)-, \(\Delta W\)-, \(F\)-modes and
  small \(\theta\)-modes, no \(\theta_2\)-content): Lemma 3.3 over
  full ranges at the dominant curvature scale. Dominance is clean
  because the only curvature scale that could collide,
  \(s^*\asymp kP^{3/8}\), lies outside every mode window: window
  centres exceed window widths by construction, and the small-mode
  truncations are capped at \(P^{1/16}\ll kP^{3/8}\).
- **(iii) Mixed pieces** — a frozen-floor factor times a large
  \(X\)-mode \(s\asymp rP^{3/4}\) regenerated by the
  \(\theta_2\)-carries: Lemma 3.3 fails there
  (\(\lambda_2\asymp rP^{1/4}\gg1\)) and the per-run
  third-derivative test returns only the trivial bound. This class
  is exactly Lemma 5.2, with saving \(P^{1/8}/r^{1/6}\).
- **(iv) Carry-mode pieces without a frozen floor**: the
  third-derivative test over full ranges,
  \(\lambda_3\asymp rP^{-3/4}\), saving \(P^{1/8}/r^{1/6}\).

*Step 6 (assembly).* Sub-unit sawtooths cost multiplicative
mode-mass \(O(\log P)\) only; mode masses multiply over at most four
expansion layers plus the targeted differencing of Lemma 5.2:
\(P^{\varepsilon}\) in total. Majorant truncations cost \(P/R\) per
layer. With \(R=P^{\rho}\), \(\rho=\tfrac1{16}\), the savings
\(P^{1/16}/(k|j|)^{1/2}\) (class (i)), \(P^{1/8-\rho/6}\) (classes
(iii)–(iv) at \(r\le R\)), and the truncation loss \(P^{-\rho}\)
balance at
\[
|T_2|\ll P^{1-1/16+\varepsilon}
\qquad\text{under (C1) and } h_1h_2\le P^{1/2}/3 .
\]
Unwinding the two differencings: with \(k\le P^{\kappa_0}\) and
\(a+b\le\tfrac18-\kappa_0\) (so that (C1) holds for all
\(h_1\le H_1\), \(h_2\le H_2\)),
\[
|K_c|\ll P\bigl(P^{-a/2}+P^{-b/4}+P^{-1/64}\bigr).
\]
For \(\kappa_0=\varepsilon\): \(a=\tfrac1{32}\), \(b=\tfrac1{16}\),
\(\delta=\tfrac1{64}\). For \(\kappa_0=\tfrac1{24}\):
\(a=\tfrac1{36}\), \(b=\tfrac1{18}\), \(\delta=\tfrac1{72}\).
Exponents deliberately unoptimized. \(\square\)

**Corollary 5.4 (low-exponent families).**
The bound of Theorem 5.3 holds for every monomial-pattern family
\(c^{(r)}\asymp kP^{\alpha-r}\) with \(0<\alpha\le\tfrac98\),
uniformly for \(k\le P^{1/24}\).

*Proof.* Every constraint in the proof is monotone in \(\alpha\) on
\((0,\tfrac98]\): (C1) relaxes to \(kh_1h_2\le P^{5/4-\alpha}\);
every curvature and window drift shrinks; the sign-dominance product
\(\alpha(\alpha{-}1)(\alpha{+}\beta{-}2)(\alpha{+}\beta{-}3)>0\)
holds at \(\beta\in\{\tfrac14,\tfrac34\}\) throughout the interval;
the assembly exponents only improve. \(\square\)

## 6. Applications: depth four complete, and deeper contracting words

**Theorem 6.1 (the OOO\* splits; depth four complete).**
For \(w\in\{OOOE,OOOO\}\),
\[
\#\{n\le N\ \text{odd}:\ \mathrm{word}_4(n)=w\}
=\tfrac N{16}+O\bigl(N^{1-1/72+\varepsilon}\bigr).
\]
Hence **every** itinerary word class of depth at most four satisfies
\(\#\{n\le N\}=2^{-|w|}N+O(N^{1-\delta_w})\) with explicit
\(\delta_w>0\): depth-4 parity equidistribution is complete.

*Proof.* The class indicator expands (Lemma 3.6, then Lemma 3.5 at
truncation \(J_3=P^{1/24}\), error \(P/J_3\)) into mode sums
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
difference into the Step-3 classes (their \((\Delta\Delta\mu)m\)
content is sub-unit under (C1), the crosses are smooth per cell, and
\(\mu\,\Delta\Delta m\) produces the bounded-offset branch phases of
Step 3 with curvature \(\asymp k|j|P^{-1/8}\), single-signed by the
same monomial-exponent check); the \(\tfrac i2X\)- and
\(\tfrac j2Y\)-passengers difference to curvatures
\(\ll ih_1h_2P^{-5/2}\) and \(\asymp jh_1h_2P^{-5/4}\), each smaller
than every retained curvature scale of Step 5 by a fixed power of
\(P\); and the kernel factor is handled by Steps 2–5 of Theorem 5.3
without change, since those steps use only the derivative pattern of
\(c\), not its specific form. Assembly and summation over
\(k\le J_3\) with \(1/k\)-weights give
\(\sum_k\tfrac1kP^{1-1/72}+P^{1-1/24}\ll P^{1-1/72+\varepsilon}\);
dyadic blocks sum to \(N^{1-1/72+\varepsilon}\). \(\square\)

The certified-descent density stays \(13/16\) at four steps —
\(OOO*\) is non-contracting at depth 4 (\(3^3>2^4\)) — but the
kernel theorem opens the contracting words at depths five, seven,
and eight.

**Theorem 6.2 (the length-5 contracting splits).**
\[
\#\mathrm{OOOEE}(N),\ \#\mathrm{OOOEO}(N)
=\tfrac N{32}+O\bigl(N^{1-1/72+\varepsilon}\bigr),
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
=\tfrac N{128}+O\bigl(N^{43/48+\varepsilon}\bigr).
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
\(\asymp P^{5/16}\). Same exponent. \(\square\)

**Theorem 6.4 (the length-8 engine quartet).**
The four contracting length-8 classes satisfy
\[
\#\mathrm{OOEOOEOE}(N),\ \#\mathrm{OOEOOOEE}(N),\
\#\mathrm{OOOEOEOE}(N),\ \#\mathrm{OOOEOOEE}(N)
=\tfrac N{256}+O\bigl(N^{1-1/48+\varepsilon}\bigr).
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
\(P/J_8\) at \(J_8=P^{13/384}\) gives \(P^{1-13/384}\), stated
unoptimized as \(N^{1-1/48+\varepsilon}\). Letters one through
seven ride as passengers with the budgets of
Theorems 6.1–6.3. \(\square\)

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
