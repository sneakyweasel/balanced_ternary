---
title: Lower bounds for nontrivial cycles of the Juggler map
author: Philippe Cochin
date: 31 August 2026
keywords:
  - Juggler map
  - Juggler sequence
  - floor-power maps
  - integer dynamics
  - cycles
header-includes:
  - \AtBeginDocument{\author{Philippe Cochin \\ \texttt{philippe@cochin.fr}}}
---

## Abstract

The Juggler map is the nonlinear integer map
\[
J(n)=
\begin{cases}
\lfloor\sqrt n\rfloor,&n\ \text{even},\\
\lfloor n^{3/2}\rfloor,&n\ \text{odd}.
\end{cases}
\]
It is conjectured that every positive integer eventually reaches \(1\).
This note does not prove that conjecture, and it does not exclude
every cycle. It restricts the possible periods of a hypothetical
nontrivial cycle.

A realized parity word obeys a power envelope, so a cycle word is
formally expanding. Floor remainders must finance the surplus
\(3^o-2^L\). At a cycle minimum this yields
\[
n\log n\cdot(3^o-2^L)\le L\cdot 3^o.
\]
Combined with the published verification that every start through
\(10^6\) reaches \(1\), there is no nontrivial cycle of length at
most \(1053\). Through length \(10^5\), only an explicit set
\(\mathcal E\) of \(397\) lengths remains admissible to the bound.
A separate finite-word analysis shows that every nontrivial cycle
has at least four even letters and hence period at least eleven.

**2020 Mathematics Subject Classification.** 11B83, 37P99, 11Y55.

## 1. Introduction

The Juggler sequence was introduced by Pickover [1,2]. The one-step
map is OEIS A094683 [3]; the stopping-time table is A007320 [4]. The
orbit of \(3\) is \(3,5,11,36,6,2,1\). The orbit of \(37\) already
peaks at \(24906114455136\). Universal arrival at \(1\) remains the
open conjecture of the subject.

The map combines a contracting even branch with an expanding odd
branch,
\[
E(n)=\lfloor n^{1/2}\rfloor,\qquad
O(n)=\lfloor n^{3/2}\rfloor.
\]
A word of length \(k\) with \(o\) odd letters has ideal exponent
\(3^o/2^k\). Floors are applied after every letter, and a word is
available only when the orbit realizes those parities.

The note has one architecture:
\[
\text{local word obstructions}
\quad+\quad
\text{global finance}
\quad\Rightarrow\quad
\text{a cycle-length lower bound}.
\]
Section 3 excludes every cycle word with fewer than four even
letters, so the period is at least eleven. Section 4 turns the
formal surplus \(3^o-2^L\) into a bound on the cycle minimum.
With the known descent floor through \(10^6\), that bound
excludes every period at most \(1053\).

The \(10^6\) floor is Weisstein's published verification [5],
recomputed here by exact first-passage. It is not a new
computational record. The contribution is the implication
\[
\text{finance}+\text{floor }10^6
\quad\Rightarrow\quad
L\ge 1054.
\]

Throughout, \(\mathbb N=\{1,2,3,\ldots\}\). Write \(J^k\) for the
\(k\)-fold iterate. A nonempty realized word \(w\) with
\(J^{|w|}(n)=n\) is a *cycle word*. The unique fixed point is \(1\);
a cycle is *nontrivial* when it contains some \(n\ge 2\). A cycle
word at \(n\) is *minimum-based* when \(n\) is a cycle minimum:
\(J^j(n)\ge n\) for every \(0\le j<|w|\). Every cycle word has a
minimum-based rotation.

### 1.0 Main results

**Theorem A (period lower bound).**
There is no nontrivial Juggler cycle of length at most \(1053\).
Equivalently, any nontrivial cycle has period at least \(1054\).

**Theorem B (admissible lengths through \(10^5\)).**
If a nontrivial cycle has period \(L\le 10^5\), then \(L\) belongs
to an explicit set \(\mathcal E\) of \(397\) lengths. Membership
in \(\mathcal E\) means only that the finance inequality at the
floor \(10^6\) does not exclude \(L\). It does not mean that a
cycle of that length exists, or that the length is dynamically
plausible.

**Theorem C (even-count).**
Every nontrivial cycle word has at least four even letters, and
hence period at least eleven.

Theorem C is an exact word-shape bound and does not use a descent
floor (Theorem 3.22 and Corollary 3.23). Theorems A and B are
Theorem 4.6: the finance inequality of Theorem 4.4, in the
conservative \(6/5\) form of Corollary 4.5, at the published
floor \(N_0=10^6\). These results give no control over the
remaining lengths in \(\mathcal E\), and they do not imply
termination.

### 1.1 Related work

Pickover's later exposition is Chapter 45 of [2]. Weisstein [5]
records the map, the stopping-time sequences A094670, A094679,
A095908, and a verification of arrival at \(1\) through \(10^6\).
That published floor is the input to Theorem 4.6; the
first-passage run of Appendix B recomputes it and is not a new
record. OEIS
A094716 [6] records extreme heights, including the start \(48443\)
whose peak has \(972\,463\) digits. Those height records do not
bound the period.

We found no published theorem excluding nontrivial cycles for the
exact floor-power Juggler map. Prasad--Prasad [7] estimate excursion
and stopping constants for juggler-like maps by a random-walk
large-deviation model; those estimates do not apply to exact
cycles. Small-cycle censuses are a standard first layer for
Collatz-like maps, surveyed by Lagarias [8,9]. Those results do not
transfer: the branches of \(J\) are floor powers rather than affine
maps (Crandall [10], Matthews--Watts [11]). In particular there is
no identity of the form \(n(2^K-3^p)=C\).

The financing-versus-gap template of Section 4 follows Simons and
de Weger [12] on Collatz \(m\)-cycles. That paper uses Diophantine
approximation and linear forms in logarithms. The argument below is
elementary and independent of those tools: floor-power defects are
relatively \(O(1/x)\) in logarithms, so one residual floor excludes
every length that is not admissible for Theorem 4.4. What is new is
the Juggler-specific realization — the exact floor-power
recurrence, the \(n\log n\) inequality, and the resulting
admissible set \(\mathcal E\) — not the financing method itself.
The leftover packaging, period at least \(X\) or a named admissible
family, follows Eliahou [13]. For this nonlinear floor-power map,
the elementary log-envelope plus the published floor \(10^6\)
already forces \(L\ge 1054\).

### 1.2 Verification

The arguments of Sections 2, 3, and 4 may be read without machine
assistance. A Lean formalization of those arguments is recorded in
Appendix A. The finite tables used by Lemmas 3.5, 3.7, 3.11 and
Theorems 3.12--3.20 are `native_decide` evaluations in the modules
named there. They are finite computations, not a termination proof.

Theorem 4.6 uses an exact-integer first-passage run through
\(10^6\), together with an exact gap table of lengths up to
\(10^5\). The floor itself is Weisstein's published verification
[5]; the first-passage run is an independent recomputation of that
same floor, not a new record. Checksums and regeneration commands
are in Appendix B.

```text
Repository:  https://github.com/sneakyweasel/balanced_ternary
Commit:      7802f78bec58c68cec92a2efb3db4a502f916277
Lean:        leanprover/lean4:v4.33.0
Mathlib:     v4.33.0 (lake-manifest rev db584cd6d46c92f209a44c0f1c829460d327499d)
Build:       lake build Problems.JugglerPaper   (from formal/)
Computation: python -m research.juggler_sequence.cycle_finance
SHA-256:     Appendix B
```

The commit is the repository state that produced the finance
tables. A later editorial commit of this text does not change
those hashes.

## 2. Envelope and defect

Let \(\mathcal B=\{E,O\}\). A finite word \(w\in\mathcal B^*\) is
*realized* at \(n\in\mathbb N\) when the successive parities of the
orbit of \(n\) are exactly the letters of \(w\). Write \(J^{|w|}(n)\)
for the endpoint after those letters, and \(\#O(w)\) for the number
of odd letters. When \(w\) is realized, this endpoint is the
\(|w|\)-fold iterate.

**Theorem 2.1 (fixed-word monotonicity).**
If \(n\le m\) and both realize \(w\), then
\(J^{|w|}(n)\le J^{|w|}(m)\).

*Proof.* Induct on \(w\). The empty word is immediate. The images
after a common realized prefix remain ordered, and both current
states realize the same next letter. The even branch is the
monotone integer square root; the odd branch is \(x\mapsto x^3\)
followed by the integer square root. \(\square\)

The realizing set of a fixed word need not be an interval: \(OE\) is
realized at \(7\) and at \(11\) but not at \(9\).

**Theorem 2.2 (finite-word power envelope).**
If \(w\) is realized at \(n\) and \(m=J^{|w|}(n)\), then
\[
m^{2^{|w|}}\le n^{3^{\#O(w)}}.
\]

*Proof.* The empty word is the equality \(n\le n\). Suppose a
realized prefix of length \(\ell\) with odd count \(o\) ends at
\(x\) and satisfies \(x^{2^\ell}\le n^{3^o}\), and the next letter
is realized.

If the next letter is even, then \(J(x)^2\le x\). Raising the
inductive bound to the second power gives
\[
J(x)^{2^{\ell+1}}=(J(x)^2)^{2^\ell}\le x^{2^\ell}\le n^{3^o}.
\]
The odd count is unchanged.

If the next letter is odd, then \(J(x)^2\le x^3\), so
\[
J(x)^{2^{\ell+1}}=(J(x)^2)^{2^\ell}\le x^{3\cdot 2^\ell}
=(x^{2^\ell})^3\le\bigl(n^{3^o}\bigr)^3=n^{3^{o+1}}.
\]
This is the claimed bound after one more odd letter. \(\square\)

**Corollary 2.3 (exponent-gap contraction).**
If \(n\ge2\), \(w\) is realized at \(n\), and
\(3^{\#O(w)}<2^{|w|}\), then \(J^{|w|}(n)<n\).

*Proof.* Let \(m=J^{|w|}(n)\) and \(k=|w|\). Theorem 2.2 gives
\(m^{2^k}\le n^{3^{\#O(w)}}\). The exponent gap and \(n\ge2\) give
\(n^{3^{\#O(w)}}<n^{2^k}\), so \(m^{2^k}<n^{2^k}\). Since \(m\ge1\),
one has \(m<n\). \(\square\)

The corollary includes familiar contracting blocks such as \(OOOEE\).
It does not prove that every start realizes some contracting word.

The floor slack is exact. For a single branch,
\[
x^e=J(x)^2+\rho(x),\qquad
e=\begin{cases}1,&x\ \text{even},\\3,&x\ \text{odd},\end{cases}
\]
with \(0\le\rho(x)<2J(x)+1\). Write
\[
\operatorname{gap}(a,\rho,e)=(a+\rho)^e-a^e,
\]
so \(a^e+\operatorname{gap}(a,\rho,e)=(a+\rho)^e\). If \(e\ge1\), then
\(\operatorname{gap}(a,\rho,e)=0\) if and only if \(\rho=0\), and
\(\rho^e\le\operatorname{gap}(a,\rho,e)\).

Along a realized word \(w\), write \(x_0=n\) and \(x_{j+1}=J(x_j)\),
and let \(\rho_j=\rho(x_j)\). Define a running slack by \(D_0=0\) and
\[
D_{j+1}=
\begin{cases}
D_j+\operatorname{gap}((x_{j+1})^2,\rho_j,2^j),
& \text{next letter even},\\[4pt]
\operatorname{gap}((x_{j+1})^2,\rho_j,2^j)
+\operatorname{gap}(x_j^{2^j},D_j,3),
& \text{next letter odd}.
\end{cases}
\]
The *global defect* is \(\Delta_w(n)=D_{|w|}\). An even letter keeps
the old slack and lifts the new remainder through \(2^j\). An odd
letter first cubes the running slack and then lifts the new
remainder. In particular \(\Delta\) is not the sum of the local
remainders.

**Theorem 2.4 (global defect identity).**
If \(w\) is realized at \(n\) and \(m=J^{|w|}(n)\), then
\[
n^{3^{\#O(w)}}=m^{2^{|w|}}+\Delta_w(n),\qquad\Delta_w(n)\ge0.
\]
Theorem 2.2 is the inequality \(\Delta_w(n)\ge0\).

*Proof.* The empty word is \(n=n+0\). Suppose a realized prefix of
length \(\ell\) with odd count \(o\) ends at \(x\) and satisfies
\(n^{3^o}=x^{2^\ell}+D\).

If the next letter is even, then \(x=J(x)^2+\rho(x)\), so
\[
n^{3^o}
=(J(x)^2+\rho(x))^{2^\ell}+D
=J(x)^{2^{\ell+1}}+D+\operatorname{gap}(J(x)^2,\rho(x),2^\ell).
\]
The odd count is unchanged, and the new slack is the even update.

If the next letter is odd, then \(x^3=J(x)^2+\rho(x)\). Cubing the
inductive identity gives
\[
n^{3^{o+1}}=(x^{2^\ell}+D)^3
=x^{3\cdot 2^\ell}+\operatorname{gap}(x^{2^\ell},D,3).
\]
The leading term is
\[
x^{3\cdot 2^\ell}
=(J(x)^2+\rho(x))^{2^\ell}
=J(x)^{2^{\ell+1}}+\operatorname{gap}(J(x)^2,\rho(x),2^\ell),
\]
which is the odd update. \(\square\)

For a one-letter illustration, take \(n=3\) and \(w=O\). Then
\(J(3)=5\) and \(3^3=27=5^2+2\), so \(\Delta_O(3)=2\). After a later
letter the lift is a power-gap, not a sum of remainders.

**Theorem 2.5 (vanishing).**
If \(w\) is realized at \(n\), the following are equivalent.

1. \(\Delta_w(n)=0\).
2. Every local remainder along \(w\) vanishes.
3. \(\bigl(J^{|w|}(n)\bigr)^{2^{|w|}}=n^{3^{\#O(w)}}\).

In that case \(w\) is monochrome. More precisely, either \(w=E^k\) and
\(n=a^{2^k}\) for an even \(a\), or \(w=O^k\) and \(n=a^{2^k}\) for an
odd \(a\). A realized mixed word therefore has \(\Delta_w(n)>0\).

*Proof.* The identity of Theorem 2.4 gives (1)\(\Leftrightarrow\)(3).
For (1)\(\Leftrightarrow\)(2), use the recurrence. If \(e\ge1\), a
power-gap vanishes if and only if its addend vanishes. The even
update is a sum of two nonnegative terms, and the odd update is a
sum of two power-gaps; either vanishes only when the incoming slack
and the new remainder both vanish. Thus \(D_{|w|}=0\) forces
\(D_0=0\) and every \(\rho_j=0\). The converse is immediate.

If every remainder vanishes, an even step satisfies
\(x_j=x_{j+1}^2\), while an odd step satisfies
\(x_j^3=x_{j+1}^2\). In either case \(x_j\) and \(x_{j+1}\) have the
same parity, so the itinerary is monochrome. If \(w=E^k\), repeated
substitution gives \(n=x_k^{2^k}\); writing \(a=x_k\), its parity is
even. If \(w=O^k\), unique factorization applied to
\(x_j^3=x_{j+1}^2\) shows that every prime valuation of \(x_j\) is
even. Iterating this valuation relation shows that every prime
valuation of \(n=x_0\) is divisible by \(2^k\), hence
\(n=a^{2^k}\) for an odd \(a\). Conversely, these even and odd
towers make every local remainder zero. \(\square\)

**Theorem 2.6 (composition).**
If \(u\) is realized at \(n\) and \(v\) is realized at
\(m=J^{|u|}(n)\), then
\[
\Delta_{uv}(n)
=
\operatorname{gap}\bigl(m^{2^{|u|}},\,\Delta_u(n),\,3^{\#O(v)}\bigr)
+
\operatorname{gap}\bigl(\bigl(J^{|v|}(m)\bigr)^{2^{|v|}},\,\Delta_v(m),\,2^{|u|}\bigr).
\]
In particular
\(\Delta_v(m)^{2^{|u|}}\le\Delta_{uv}(n)\). Every local remainder
satisfies \(\rho_j^{2^j}\le\Delta_w(n)\).

*Proof.* Write \(o_u=\#O(u)\) and \(o_v=\#O(v)\). Theorem 2.4 on \(u\)
and on \(uv\) gives
\[
n^{3^{o_u+o_v}}
=\bigl(m^{2^{|u|}}+\Delta_u(n)\bigr)^{3^{o_v}}
=\bigl(J^{|uv|}(n)\bigr)^{2^{|uv|}}+\Delta_{uv}(n).
\]
The first power expands as
\[
m^{2^{|u|}\cdot 3^{o_v}}
+\operatorname{gap}\bigl(m^{2^{|u|}},\,\Delta_u(n),\,3^{o_v}\bigr).
\]
Theorem 2.4 on \(v\) at \(m\) rewrites the leading term as
\[
\Bigl(\bigl(J^{|v|}(m)\bigr)^{2^{|v|}}+\Delta_v(m)\Bigr)^{2^{|u|}},
\]
which expands as the second gap plus \(\bigl(J^{|uv|}(n)\bigr)^{2^{|uv|}}\).
Comparing the two expressions for \(n^{3^{o_u+o_v}}\) yields the
identity. The suffix inequality is
\(\rho^e\le\operatorname{gap}(a,\rho,e)\) on the second summand. For a
local remainder at index \(j\), split \(w\) after \(j\) letters: the
suffix defect is at least \(\rho_j\), and raising through \(2^j\)
gives the stated bound. \(\square\)

Composition is polynomial, not additive: later odd letters raise the
prefix slack to the third power. The naive recurrence
\(\Delta\leftarrow\Delta+\rho\) is false.

**Corollary 2.7 (cycle surplus).**
If \(w\) is a cycle word at \(n\), then
\[
\Delta_w(n)=n^{3^{\#O(w)}}-n^{2^{|w|}}
\]
exactly.

*Proof.* Theorem 2.4 with \(m=n\). \(\square\)

Call this the *total-versus-uniform* distinction: a mixed word has
strict total defect \(\Delta_w(n)>0\), but there is no
state-independent \(c>0\) such that every letter pays a relative
slack at least \(c\). Strict total defect is not a uniform local
tax. A naive “every step costs something” argument therefore
cannot bound the period, while an aggregate financing inequality
can. The exact recurrence of Theorems 2.4--2.6 is not used in
Section 4; the finance inequality uses only the envelope
(Theorem 2.2), the one-step cells, and \(\log(1+u)\le u\).

The identity does not supply a state-independent positive tax, and
none exists. For one realized letter at \(x\) with branch exponent
\(e\in\{1,3\}\),
\[
x^{e}<(J(x)+1)^2,
\]
so the relative slack \(1+\eta=x^{e}/J(x)^2\) satisfies
\[
\eta<\frac{2}{J(x)}+\frac{1}{J(x)^2},
\]
which tends to \(0\) as the state grows. The recorded extreme is an
\(OOE\) block at
\(n=180370579261640036336071806107777\approx 1.80\cdot 10^{32}\)
whose word-relative slack
\[
q_w(n)=\frac{n^{3^{\#O(w)}}}{\bigl(J^{|w|}(n)\bigr)^{2^{|w|}}}-1
\]
satisfies \(0<q_{OOE}(n)<10^{-30}\), by the exact integer comparison
\(0<(n^9-J^3(n)^8)\,10^{30}<J^3(n)^8\).

## 3. Inverse cells and the census

The exact one-step fibers are
\[
J(n)=q\iff q^2\le n<(q+1)^2
\quad(n\ \text{even})
\]
and
\[
J(n)=m\iff m^2\le n^3<(m+1)^2
\quad(n\ \text{odd}).
\]

**Lemma 3.1 (odd cells are unique).**
An odd fiber contains at most one integer. An even fiber is a
parity-restricted square interval and may contain many predecessors.

*Proof.* Suppose \(a<b\) lie in the same odd cell indexed by \(m\).
Then \((a+1)^3\le b^3<(m+1)^2\) and \(m^2\le a^3\). Subtracting the
latter lower bound from the former upper bound gives
\[
3a^2+3a+1=(a+1)^3-a^3<(m+1)^2-m^2=2m+1,
\]
hence \(3a^2+3a<2m\) and \(3a^2<2m\). If \(a=0\), then \(m=0\) and
the displayed strict inequality is already impossible. If \(a>0\),
squaring and using \(m^2\le a^3\) gives \(9a^4<4m^2\le 4a^3\),
contradicting \(4a^3<9a^4\). \(\square\)

**Theorem 3.2 (cycle restrictions).**
Let \(w\) be a cycle word at \(n\ge2\).

(i) The word is formally expanding:
\[
2^{|w|}<3^{\#O(w)}.
\]
A contracting word cannot close a nontrivial cycle.

(ii) The cycle minimum is odd and the cycle maximum is even. A
minimum-based orientation cannot end in an odd letter.

(iii) A realized word \(v\) is *superquadratic* if
\[
3^{\#O(v)}\ge 2^{|v|+1}.
\]
Any realized path from a start \(n\ge2\) to a state at least \(n^2\)
is superquadratic. On a cycle minimum the path to any later even
state is superquadratic. The prefix \(OOE\) is expanding
(\(9>8\)) but not superquadratic (\(9<16\)), so it cannot carry the
minimum to square scale.

*Proof.* For (i), Theorem 2.2 applied to a cycle endpoint gives
\(n^{2^{|w|}}\le n^{3^{\#O(w)}}\). Since \(n\ge2\), comparison of
exponents gives \(2^{|w|}\le 3^{\#O(w)}\); equality is impossible
because the two sides have different prime divisors and \(|w|\ge 1\).
Alternatively: a mixed cycle word has \(\Delta_w(n)>0\) by
Theorem 2.5, so the envelope is strict; a monochrome tower cannot
return for \(n\ge 2\).

Every state on such a cycle is at least \(2\): once an orbit reaches
\(1\), it remains there and cannot return to a start \(n\ge 2\). An
even state \(x\ge 2\) satisfies \(J(x)<x\), so a cycle minimum cannot
be even. An odd state \(x\ge 3\) satisfies \(J(x)>x\), so a cycle
maximum cannot be odd. This proves the first assertion of (ii). For
the final-letter assertion, let \(x\) be the predecessor of a
minimum-oriented return \(n\). If the last letter were odd, the odd
return cell would give \(n^2\le x^3<(n+1)^2\). Minimality gives
\(x\ge n\), hence \(n^3<(n+1)^2\), impossible for \(n\ge 3\); and the
minimum is odd, so \(n\ge 3\).

For (iii), let a realized word \(v\) send \(n\) to \(y\ge n^2\).
Theorem 2.2 gives
\[
n^{2^{|v|+1}}=(n^2)^{2^{|v|}}
\le y^{2^{|v|}}\le n^{3^{\#O(v)}}.
\]
Since \(n\ge 2\), comparison of exponents proves the superquadratic
inequality. On a cycle minimum, if a later state \(y\) is even, its
successor is at least \(n\). Thus \(n\le J(y)=\lfloor\sqrt y\rfloor\),
so \(n^2\le y\), and the preceding argument applies to that prefix.
\(\square\)

**Lemma 3.3 (coarse lower envelope).**
For \(n\ge 1\), write \(q=\lfloor\sqrt n\rfloor\). Then
\(q^2\le n<(q+1)^2\). For \(q\ge 1\) one has
\((q+1)^2\le 4q^2\), and the second inequality is strict for
\(q\ge 2\), while for \(q=1\) one has \(n<4\). In all cases
\[
n<4\,\lfloor\sqrt n\rfloor^2.
\]
Thus an even step satisfies \(n\le 4\,J(n)^2\) and an odd step
satisfies \(n^3\le 4\,J(n)^2\). Composing along a realized word \(v\)
of length \(k\) with odd count \(o\) gives
\[
n^{3^{o}}\le C_v\,J^{k}(n)^{2^{k}}.
\]
The constant starts at \(1\) and updates by
\(C\mapsto C\cdot 4^{2^{j}}\) on an even letter and
\(C\mapsto C^{3}\cdot 4^{2^{j}}\) on an odd letter, at step \(j\).
In particular \(C_{OOO}=2^{38}\) and \(C_{OOOO}=2^{130}\).

*Proof.* The comparison \(n<4q^2\) is the paragraph above. The
composition law is the same recurrence as the proof of Theorem 2.2,
with a factor \(4^{2^j}\) inserted at each letter. The values
\(C_{OOO}\) and \(C_{OOOO}\) are the result of that recurrence on
those two words. \(\square\)

**Lemma 3.4 (next-square thresholds).**
(i) If \(q\ge 5\) realizes \(OO\), then \(J^2(q)\ge(q+1)^2\).
(ii) If \(q\ge 3\) realizes \(OOO\), then \(J^3(q)\ge(q+1)^2\).
(iii) If a realized word \(v\) satisfies \(J^{|v|}(q)\ge(q+1)^2\) and
the next realized letter is odd, then
\(J^{|v|+1}(q)\ge(q+1)^2\).
(iv) If \(vE\) is a cycle word at \(n\), then
\(J^{|v|}(n)<(n+1)^2\).
(v) If \(a\ge 3\), then \(O^aE\) is not a cycle word at any
\(n\ge 2\).

*Proof.* For (i), write \(m=\lfloor q^{3/2}\rfloor\). The bound
\(J^2(q)\ge(q+1)^2\) follows from \(m^3\ge(q+1)^4\), because then
\(\lfloor m^{3/2}\rfloor\ge(q+1)^2\). If \(q=5\), then
\(11^2=121\le 125=5^3<144=12^2\), so \(m=11\), and
\(11^3=1331\ge 6^4=1296\). Since \(q\) realizes \(OO\), it is odd, so
the only remaining case is \(q\ge 7\). Then \(m\ge q^{3/2}-1\), so it
is enough that \((q^{3/2}-1)^3\ge(q+1)^4\). Expanding the left side
and dropping the positive remainder \(3q^{3/2}-1\) reduces this to
\(q^{9/2}-3q^3\ge(q+1)^4\), or equivalently
\(\sqrt q-3/q\ge(1+1/q)^4\). The left side increases for \(q>0\) and
the right side decreases, so the case \(q=7\) suffices:
\[
\sqrt7-\frac37>\frac52-\frac37=\frac{29}{14}
  >\frac{4096}{2401}=\left(\frac87\right)^4,
\]
where \(\sqrt7>5/2\) follows from \(25/4<7\).

For (ii), the orbit \(3\to 5\to 11\to 36\) gives \(J^3(3)=36\ge 16\).
If \(q\ge 5\) realizes \(OOO\), then it realizes \(OO\), so (i) gives
\(J^2(q)\ge(q+1)^2\). The third letter is odd, hence
\(J^3(q)=J(J^2(q))\ge J^2(q)\).

For (iii), the image after \(v\) is odd and at least \((q+1)^2\ge 4\),
so the odd branch does not decrease it.

For (iv), the last letter is even, so the preimage \(z=J^{|v|}(n)\)
is even and satisfies \(n^2\le z<(n+1)^2\).

For (v), suppose \(O^aE\) is a cycle word at \(n\ge 2\). The start
is odd, hence at least \(3\), and realizes \(O^a\). Parts (ii) and
(iii) give \(J^a(n)\ge(n+1)^2\), contradicting (iv). \(\square\)

**Lemma 3.5 (two length-six exclusions).**
Neither \(OOOEOE\) nor \(OOOOEE\) is a cycle word at any \(n\ge 2\).

*Proof.* First, if \(n\ge 256\), then
\[
n^{81}>2^{130}(n+1)^{64}.
\]
Indeed \(257^{64}<2\cdot 256^{64}\) because
\((1+1/256)^{64}<e^{64/256}=e^{1/4}<2\), and
\(256(n+1)\le 257\,n\), so \((n+1)^{64}<2n^{64}\). Then
\(2^{130}(n+1)^{64}<2^{131}n^{64}\). Since \(n\ge 256=2^8\), one has
\(n^{17}\ge 2^{136}\), and therefore
\(2^{131}n^{64}<2^{136}n^{64}\le n^{81}\).

For \(2\le n<256\), neither word returns to its start. This is a
table of \(254\) evaluations of each word: at every start, either
some letter fails to match the current parity, or the six-step image
differs from the start. The same finite check is the Lean
`native_decide` evaluation behind `no_cycle_word_oooeoe` and
`no_cycle_word_ooooee` (Appendix A).

Now suppose \(OOOOEE\) is a cycle word at \(n\ge 256\), and write
\(z=J^4(n)\) for the image after the prefix \(OOOO\). Lemma 3.4(iv)
gives \(J(z)<(n+1)^2\), and the preceding even letter gives
\(z<(J(z)+1)^2\), hence \(z<(n+1)^4\). Lemma 3.3 on \(OOOO\) gives
\(n^{81}\le 2^{130}z^{16}\), so
\(n^{81}<2^{130}(n+1)^{64}\), contradicting the tail inequality.

Finally suppose \(OOOEOE\) is a cycle word at \(n\ge 256\). Write
\(z_3=J^3(n)\) and \(y=J(z_3)=\lfloor\sqrt{z_3}\rfloor\), so
\(z_3<(y+1)^2\). Lemma 3.3 on \(OOO\) gives
\(n^{27}\le 2^{38}z_3^8<2^{38}(y+1)^{16}\). Cubing yields
\(n^{81}<2^{114}(y+1)^{48}\). The last letters \(OE\) give the odd-cell
bound \(y^3<(n+1)^4\). Write \(A=n+1\ge 257\). We claim
\((y+1)^3<2A^4\). If \(y\le A\), this is \((A+1)^3<2A^4\). If
\(y>A\), then \(y\ge 258\), so \(3y+1<y^2\) and hence
\((y+1)^3=y^3+3y^2+3y+1<A^4+4y^2\), while \(4y^2<A^4\) because
\(4y^3<4A^4\le yA^4\). Raising \((y+1)^3<2A^4\) to the sixteenth
power gives \((y+1)^{48}<2^{16}(n+1)^{64}\). Combining with the cubed
lower envelope produces again \(n^{81}<2^{130}(n+1)^{64}\). \(\square\)

**Theorem 3.6 (small-cycle census).**
No word of length at most six is a cycle word at any \(n\ge 2\).
Equivalently, a nontrivial Juggler cycle, if one exists, has period at
least seven.

*Proof.* Rotating a cycle word by one letter moves the base point one
step along the orbit and yields another cycle word; every state of
the cycle is at least \(2\), because an orbit that reaches \(1\) stays
at \(1\) and cannot return to a start \(n\ge 2\).

If every letter is odd, the start is odd, hence \(n\ge 3\), and the
odd branch strictly increases there: \(J(x)>x\) for odd \(x\ge 3\),
since \(x^3\ge(x+1)^2\). The orbit ascends strictly and never returns.
Otherwise some letter is even, and a rotation ending just after that
letter produces an even-terminating cycle word \(vE\) of the same
length based at a cycle state \(m\ge 2\). It therefore suffices to
exclude even-terminating cycle words of length at most six.

By Theorem 3.2(i) a cycle word is formally expanding. No
even-terminating word of length one or two is expanding (\(2>3^0\) and
\(4>3\)).

Length three: the only expanding candidate is \(OOE\). If \(m\ge 5\)
realizes \(OO\), Lemma 3.4(i) gives \(J^2(m)\ge(m+1)^2\), contradicting
Lemma 3.4(iv). The only smaller odd start is \(m=3\), where
\(J^2(3)=11\) is odd, so the final even letter is not realized.

Length four: the expanding filter requires three odd letters among the
first three, leaving only \(O^3E\), excluded by Lemma 3.4(v).

Length five: the filter requires four odd letters among the first
four, leaving only \(O^4E\), excluded by Lemma 3.4(v).

Length six: the filter requires at least four odd letters among the
first five, leaving \(O^5E\), \(EOOOOE\), \(OEOOOE\), \(OOEOOE\),
\(OOOEOE\), and \(OOOOEE\). Lemma 3.4(v) excludes \(O^5E\). The word
\(EOOOOE\) rotates one step onto \(OOOOEE\), and \(OEOOOE\) rotates
two steps onto \(OOOEOE\); both are excluded by Lemma 3.5.

It remains to exclude \(OOEOOE\). Let this word be a cycle word at
some start, and rotate to a cycle minimum \(m\ge 2\). The three
alignments of the two even letters are \(OOEOOE\), \(OEOOEO\), and
\(EOOEOO\). The last starts even, so it cannot be a minimum, by
Theorem 3.2(ii). The middle starts \(OE\): the first image is even
and strictly below \(m^2\), whereas every even state after a cycle
minimum is at least \(m^2\), as proved in Theorem 3.2(iii). Thus the
minimum orientation is \(OOEOOE\). In particular \(m\) is odd, so
\(m\ge 3\). The prefix \(OOE\) must be realized. If \(m=3\), then
\(3\to 5\to 11\) and \(11\) is odd, so \(OOE\) is not realized. Hence
\(m\ge 5\). Write \(y=J^3(m)\) for the state after \(OOE\). Then
\(y\ge m\) by minimality, so \(y\ge 5\). The suffix \(OO\)
is realized at \(y\), and Lemma 3.4(i) gives
\(J^2(y)\ge(y+1)^2\ge(m+1)^2\). The last letter is even, so
Lemma 3.4(iv) gives \(J^2(y)<(m+1)^2\). \(\square\)

Lemma 3.4(v) excludes every odd-run-then-even word \(O^aE\) with
\(a\ge 3\), of any length.

**Lemma 3.7 (two length-seven exclusions).**
Neither \(OOOOEOE\) nor \(OOOOOEE\) is a cycle word at any \(n\ge 2\).

*Proof.* First, if \(n\ge 14\), then
\[
n^{243}>2^{422}(n+1)^{128}.
\]
Indeed \(14(n+1)\le 15n\), so
\((n+1)^{128}\le(15/14)^{128}n^{128}\). The finite comparison
\(2^{422}15^{128}<14^{243}\) then yields
\(2^{422}(n+1)^{128}<14^{115}n^{128}\le n^{243}\).

For \(2\le n<14\), neither word is realized: at every such start,
some letter fails to match the current parity. The same finite check
is the Lean `native_decide` evaluation behind
`no_cycle_word_ooooeoe` and `no_cycle_word_oooooee` (Appendix A).

Now suppose \(OOOOOEE\) is a cycle word at \(n\ge 14\), and write
\(z=J^5(n)\) for the image after the prefix \(OOOOO\). Lemma 3.4(iv)
on the last even letter, together with the preceding even letter,
gives \(z<(n+1)^4\). Lemma 3.3 on \(OOOOO\) gives
\(n^{243}\le 2^{422}z^{32}\), so
\(n^{243}<2^{422}(n+1)^{128}\), contradicting the tail inequality.

Finally suppose \(OOOOEOE\) is a cycle word at \(n\ge 14\). Write
\(z_4=J^4(n)\) and \(y=J(z_4)=\lfloor\sqrt{z_4}\rfloor\), so
\(z_4<(y+1)^2\). Lemma 3.3 on \(OOOO\) gives
\(n^{81}\le 2^{130}z_4^{16}<2^{130}(y+1)^{32}\). Cubing yields
\(n^{243}<2^{390}(y+1)^{96}\). The last letters \(OE\) give the odd-cell
bound \(y^3<(n+1)^4\). Write \(A=n+1\ge 15\). The same comparison
\((y+1)^3<2A^4\) as in Lemma 3.5 holds at this smaller scale. Raising
to the thirty-second power gives
\((y+1)^{96}<2^{32}(n+1)^{128}\). Combining with the cubed lower
envelope produces again \(n^{243}<2^{422}(n+1)^{128}\). \(\square\)

**Theorem 3.8 (small-cycle census through length seven).**
No word of length at most seven is a cycle word at any \(n\ge 2\).
Equivalently, a nontrivial Juggler cycle, if one exists, has period at
least eight.

*Proof.* The reduction of Theorem 3.6 applies at every length: an
all-odd word cannot return, and every mixed cycle word rotates to an
even-terminating cycle word based at a cycle state \(m\ge 2\).
Lengths at most six are Theorem 3.6. It remains to exclude
even-terminating cycle words of length seven.

By Theorem 3.2(i) a cycle word is formally expanding. The
even-terminating expanding length-seven words are exactly
\(O^6E\), \(EO^5E\), \(OEO^4E\), \(OOEO^3E\), \(O^3EO^2E\),
\(O^4EOE\), and \(O^5EE\). Lemma 3.4(v) excludes \(O^6E\). The word
\(EO^5E\) rotates one step onto \(O^5EE\), and \(OEO^4E\) starts
\(OE\), so it cannot be a cycle minimum (Theorem 3.2(iii)) and
rotates two steps onto \(O^4EOE\); both leftovers are excluded by
Lemma 3.7.

It remains to exclude \(OOEO^3E\) and \(O^3EO^2E\). Rotate either
word to a cycle minimum \(m\ge 2\). For \(OOEO^3E\) the minimum
orientation retains the internal even letter followed by the suffix
\(OOO\). Then \(m\ge 3\), the prefix through that even letter is
realized, and Lemma 3.4(ii) at threshold \(3\) contradicts the last
even cell. For \(O^3EO^2E\) the same bootstrap applies with suffix
\(OO\) and threshold \(5\), once \(m=3\) is removed: at \(m=3\) the
state after \(OOO\) is even, so the next even letter is not
realized. \(\square\)

The census of Theorems 3.6 and 3.8 is a statement about period. The
same cells organise leftover words by even-count. Write
\[
e_a=2\bigl(3^a-2^a\bigr)
\]
for \(a\ge 0\).

**Lemma 3.9 (trailing even run).**
If a cycle word based at \(n\) ends with \(r\ge 1\) even letters,
the state immediately before that run is strictly less than
\((n+1)^{2^r}\).

*Proof.* The case \(r=1\) is Lemma 3.4(iv). Suppose the claim holds
for some \(r\ge 1\), and let \(vE^{r+1}\) be a cycle word at \(n\).
Write \(z=J^{|v|}(n)\). The inductive hypothesis applied to the
suffix \(E^r\) after the first of those even letters gives
\(J(z)<(n+1)^{2^r}\). The state \(z\) is even, so
\(z<(J(z)+1)^2\le\bigl((n+1)^{2^r}\bigr)^2=(n+1)^{2^{r+1}}\).
\(\square\)

**Lemma 3.10 (odd-run lower envelope).**
If \(n\ge 1\) realizes \(O^a\), then
\[
n^{3^a}\le 2^{e_a}\,J^a(n)^{2^a}.
\]

*Proof.* Lemma 3.3 supplies a multiplicative constant \(C_v\) along
any realized word, with \(C_\varepsilon=1\),
\(C\mapsto C\cdot 4^{2^j}\) on an even letter, and
\(C\mapsto C^3\cdot 4^{2^j}\) on an odd letter, at step \(j\). On
the pure odd word \(O^a\) every letter is odd, so
\(C_{O^{a+1}}=C_{O^a}^3\cdot 4^{2^a}\). Writing
\(C_{O^a}=2^{e_a}\) with \(e_0=0\) yields the recurrence
\(e_{a+1}=3e_a+2^{a+1}\), because \(4^{2^a}=2^{2^{a+1}}\). The closed
form \(e_a=2(3^a-2^a)\) satisfies the recurrence and the initial
value. \(\square\)

**Lemma 3.11 (seven-odd window).**
No integer \(n\) with \(2\le n<256\) realizes the word \(O^7\).

*Proof.* This is a table of \(254\) seven-step evaluations: at every
such start, some letter fails to match the current parity. The same
finite check is the Lean `native_decide` evaluation behind
`no_follows_seven_odds_of_lt256` (Appendix A). \(\square\)

**Theorem 3.12 (two-even leftover families).**
Let \(k\ge 6\) and \(n\ge 2\). Neither \(O^{k-2}EE\) nor
\(O^{k-3}EOE\) is a cycle word at \(n\).

*Proof.* First, if \(n\ge 256\), then
\[
n^{3^{k-2}}>2^{e_{k-2}}(n+1)^{2^k}.
\]
The case \(k=6\) is the tail inequality of Lemma 3.5. If the display
holds at some \(k\ge 6\), cubing both sides produces
\[
n^{3^{k-1}}
>
2^{3e_{k-2}}(n+1)^{3\cdot 2^k}.
\]
The recurrence of Lemma 3.10 gives \(e_{k-1}=3e_{k-2}+2^{k-1}\), so
the desired comparison at length \(k+1\) reduces to
\(2^{2^{k-1}}<(n+1)^{2^k}\). Equivalently \(2<(n+1)^2\), which holds
for every \(n\ge 256\).

Now suppose \(O^{k-2}EE\) is a cycle word at such an \(n\). Write
\(z=J^{k-2}(n)\). Lemma 3.9 with \(r=2\) gives \(z<(n+1)^4\).
Lemma 3.10 on the prefix \(O^{k-2}\) gives
\(n^{3^{k-2}}\le 2^{e_{k-2}}z^{2^{k-2}}\), hence
\(n^{3^{k-2}}<2^{e_{k-2}}(n+1)^{2^k}\), contradicting the tail.

Finally suppose \(O^{k-3}EOE\) is a cycle word at such an \(n\).
Write \(z=J^{k-3}(n)\) and \(y=\lfloor\sqrt z\rfloor\), so
\(z<(y+1)^2\). Lemma 3.10 on \(O^{k-3}\) and cubing produce
\(n^{3^{k-2}}<2^{3e_{k-3}}(y+1)^{3\cdot 2^{k-2}}\). The last letters
\(OE\) give the odd-cell bound \(y^3<(n+1)^4\). The comparison
\((y+1)^3<2(n+1)^4\) of Lemma 3.5 applies at this scale. Raising it
to the power \(2^{k-2}\) and using \(e_{k-2}=3e_{k-3}+2^{k-2}\)
recovers again \(n^{3^{k-2}}<2^{e_{k-2}}(n+1)^{2^k}\).

For \(2\le n<256\), the cases \(k=6\) and \(k=7\) are Lemmas 3.5
and 3.7. The remaining short words \(O^6EE\), \(O^5EOE\), and
\(O^6EOE\) fail to return on the same \(254\)-start window; this is
the Lean `native_decide` evaluation behind
`no_cycle_word_two_even_ee` and `no_cycle_word_two_even_eoe`
(Appendix A). Any longer leftover of either family begins with
seven consecutive odd letters, which Lemma 3.11 forbids on this
window. \(\square\)

A cycle word \(w\) at \(n\) is *minimum-based* when \(n\) is a
cycle minimum: \(J^j(n)\ge n\) for every \(0\le j<|w|\). The
remainder after a proper prefix of a cycle word need not itself be
a cycle word at the prefix endpoint. The next statement therefore
transports the tail inequality of Theorem 3.12, not the cycle-word
exclusion at a later start.

**Theorem 3.13 (first-even transport).**
Let \(n\ge 2\). No minimum-based cycle word at \(n\) has the form
\(O^aEO^bEE\) with \(a\ge 2\) and \(b\ge 4\), or the form
\(O^aEO^bEOE\) with \(a\ge 2\) and \(b\ge 3\).

*Proof.* Write \(y=J^{a+1}(n)\) for the state after the first even
letter. Minimum-basedness gives \(y\ge n\). In the first family the
remainder after that letter is \(O^bEE\) with \(b+2\ge 6\); in the
second it is \(O^bEOE\) with \(b+3\ge 6\). The trailing-even and
last-odd cells of those remainders are measured against the cycle
start \(n\). Combined with Lemma 3.10 at the remainder start \(y\),
the same algebra as in Theorem 3.12 produces
\[
y^{3^{\ell-2}}
<
2^{e_{\ell-2}}(n+1)^{2^\ell}
\le
2^{e_{\ell-2}}(y+1)^{2^\ell},
\]
where \(\ell\) is the remainder length. If \(y\ge 256\), the first
paragraph of Theorem 3.12 supplies the opposite inequality at \(y\).

If \(y<256\), then \(n\le y<256\). A gapped leftover of total
length at least \(17\) has \(a\ge 7\) or \(b\ge 7\), so either the
prefix or the remainder realizes seven consecutive odd letters,
contradicting Lemma 3.11. The finitely many short-gap words with
\(2\le a\le 6\) and \(b\le 6\) fail to be minimum-based cycle words
on the window \(2\le n<256\); this is the Lean `native_decide`
evaluation behind `no_cycleMin_gapped_three_even_ee` and
`no_cycleMin_gapped_three_even_eoe` (Appendix A). \(\square\)

The hypothesis that the start is a cycle minimum is essential. If
\(y<n\), the leftover cell is measured against a larger start and
need not contradict the tail at \(y\). In particular, Theorem 3.13
does not assert that those words fail to be cycle words at a
non-minimum start. That upgrade is Theorem 3.21.

**Theorem 3.14 (three trailing evens).**
Let \(a\ge 6\) and \(n\ge 2\). The word \(O^aEEE\) is not a cycle
word at \(n\).

*Proof.* Write \(z=J^a(n)\). Lemma 3.9 with \(r=3\) gives
\(z<(n+1)^8\). Lemma 3.10 then yields
\(n^{3^a}<2^{e_a}(n+1)^{2^{a+3}}\) on any such cycle word. For
\(n\ge 128\) the opposite comparison
\[
n^{3^a}>2^{e_a}(n+1)^{2^{a+3}}
\]
holds. The case \(a=6\) is
\(n^{729}>2^{1330}(n+1)^{512}\). Indeed, for \(n\ge 128\) one has
\((n+1)^{512}<(129/128)^{512}n^{512}<e^4 n^{512}<64\,n^{512}\), so
the claimed bound reduces to \(n^{217}>2^{1336}\). Since
\(n\ge 128=2^7\), the left side is at least \(2^{1519}\). Cubing
the \(a=6\) comparison produces the general case: the recurrence of
Lemma 3.10 reduces the inductive step to \((n+1)^4>2\), which holds
for every \(n\ge 128\).

For \(2\le n<128\), the case \(a=6\) is a table of evaluations of
\(OOOOOOEEE\): at every such start the word fails to return. The
same finite check is the Lean `native_decide` evaluation behind
`no_cycle_word_ooooooeee` (Appendix A). For \(a\ge 7\) the prefix
contains seven consecutive odd letters, which Lemma 3.11 forbids
on this window. \(\square\)

**Theorem 3.15 (mixed bunched family \(EOEE\)).**
Let \(a\ge 5\) and \(n\ge 2\). The word \(O^aEOEE\) is not a cycle
word at \(n\).

*Proof.* First let \(n\ge 4\), and write \(z=J^a(n)\),
\(y=\lfloor\sqrt z\rfloor\), and \(p=J(y)\). Lemma 3.9 with
\(r=2\) after the prefix \(O^aEO\) gives \(p<(n+1)^4\). The letter
after \(y\) is odd, so Lemma 3.10 at length one yields
\(y^3\le 4p^2<4(n+1)^8\). For \(n\ge 4\) one has
\(4(n+1)^8<(n+1)^9\), hence \(y<(n+1)^3\). The even cell at \(z\)
then gives \(z<(y+1)^2\le(n+1)^6\). Combined with Lemma 3.10,
any such cycle word would satisfy
\[
n^{3^a}<2^{e_a}(n+1)^{6\cdot 2^a}.
\]

For \(a=5\) and \(n\ge 314\), the opposite comparison
\(n^{243}>2^{422}(n+1)^{192}\) holds. The base instance is the
finite inequality \(2^{422}315^{192}<314^{243}\). If the display
holds at some \(n\ge 1\), the elementary comparison
\(n(n+2)<(n+1)^2\) upgrades it to the same display at \(n+1\).
Cubing then produces the comparison at \(a+1\), once
\((n+1)^6>4\). In particular the case \(a=6\) already holds for
every \(n\ge 16\).

For \(2\le n<314\) and \(a=5\), and for \(2\le n<16\) and
\(a=6\), the word fails to return; these are the Lean
`native_decide` evaluations behind `no_cycle_word_three_even_eoee`
(Appendix A). For \(a\ge 7\) and \(n<256\), Lemma 3.11 applies. For
\(a\ge 6\) and \(n\ge 16\), the tail of the previous paragraph
applies. \(\square\)

**Theorem 3.16 (mixed bunched family \(EOOEE\)).**
Let \(a\ge 4\) and \(n\ge 2\). The word \(O^aEOOEE\) is not a
cycle word at \(n\).

*Proof.* First let \(n\ge 32\), and write \(z=J^a(n)\),
\(y=\lfloor\sqrt z\rfloor\), and \(p\) for the image after the
prefix \(O^aEOO\). Lemma 3.9 with \(r=2\) gives \(p<(n+1)^4\).
The two letters after \(y\) are odd, so Lemma 3.10 at length two
yields \(y^9\le 2^{10}p^4<2^{10}(n+1)^{16}\). For \(n\ge 32\) one
has \(2^{10}<(n+1)^2\), hence \(y<(n+1)^2\). The even cell at
\(z\) then gives \(z<(y+1)^2\le(n+1)^4\). Combined with
Lemma 3.10, any such cycle word would satisfy
\[
n^{3^a}<2^{e_a}(n+1)^{2^{a+2}}.
\]
For \(n\ge 256\) and \(a\ge 4\), this is the opposite of the
shared tail of Theorem 3.12 at length \(k=a+2\).

For \(2\le n<256\), the cases \(a=4,5,6\) fail to return on that
window; this is the Lean `native_decide` evaluation behind
`no_cycle_word_three_even_eooee` (Appendix A). For \(a\ge 7\),
Lemma 3.11 applies. \(\square\)

**Theorem 3.17 (mixed bunched family \(EOOOEE\)).**
Let \(a\ge 3\) and \(n\ge 2\). The word \(O^aEOOOEE\) is not a
cycle word at \(n\).

*Proof.* First let \(a\ge 4\) and \(n\ge 3\), and write
\(z=J^a(n)\), \(y=\lfloor\sqrt z\rfloor\), and \(p\) for the image
after the prefix \(O^aEOOO\). Lemma 3.9 with \(r=2\) gives
\(p<(n+1)^4\). The three letters after \(y\) are odd, so
Lemma 3.10 at length three yields
\(y^{27}\le 2^{38}p^8<2^{38}(n+1)^{32}\). For \(n\ge 3\) one has
\(2^{38}<(n+1)^{22}\), hence \(y<(n+1)^2\). The even cell at
\(z\) then gives \(z<(y+1)^2\le(n+1)^4\). Combined with
Lemma 3.10, any such cycle word would satisfy
\[
n^{3^a}<2^{e_a}(n+1)^{2^{a+2}}.
\]
For \(n\ge 256\) and \(a\ge 4\), this is the opposite of the
shared tail of Theorem 3.12 at length \(k=a+2\), already used in
Theorem 3.16.

Now let \(a=3\) and \(n\ge 256\). The same two-even cell gives
\(z<(y+1)^2\), so Lemma 3.10 at the prefix \(O^3\) yields
\(n^{27}<2^{38}(y+1)^{16}\). The three-odd envelope on \(y\) still
gives \(y^{27}<2^{38}(n+1)^{32}\).

If \(y<39\), then \(n^{27}<2^{38}\cdot 39^{16}\). The numerical
comparison \(2^{38}\cdot 39^{16}<24^{27}\) contradicts
\(n\ge 24\).

If \(y\ge 39\), the numerical comparison \(40^{27}<2\cdot 39^{27}\)
upgrades to \((y+1)^{27}<2y^{27}\), hence
\((y+1)^{27}<2^{39}(n+1)^{32}\). Cubing the prefix bound three
times produces \(n^{729}<2^{1026}(y+1)^{432}\). Raising the
successor bound to the sixteenth power produces
\((y+1)^{432}<2^{624}(n+1)^{512}\). Combining these displays
yields \(n^{729}<2^{1650}(n+1)^{512}\). The opposite comparison
holds at \(n=197\) and persists to every larger start by the
elementary comparison \(n(n+2)<(n+1)^2\) already used in
Theorem 3.15.

For \(2\le n<256\), the cases \(a=3,4,5,6\) fail to return on
that window; this is the Lean `native_decide` evaluation behind
`no_cycle_word_three_even_eoooee` (Appendix A). For \(a\ge 7\),
Lemma 3.11 applies. \(\square\)

**Theorem 3.18 (mixed bunched family \(EEOE\)).**
Let \(a\ge 5\) and \(n\ge 2\). The word \(O^aEEOE\) is not a
cycle word at \(n\).

*Proof.* First let \(n\ge 4\), and write \(z=J^a(n)\) and \(y\)
for the last odd letter of \(O^aEEOE\). The suffix \(EOE\) is a
cycle suffix, so the last-odd cube of Theorem 3.15 gives
\(y^3<(n+1)^4\). The two letters between \(z\) and \(y\) are
even, so \(z<(y+1)^4\). For \(n\ge 4\) the successor comparison
\((y+1)^3<2(n+1)^4\) upgrades this to \(z<(n+1)^6\). Combined
with Lemma 3.10, any such cycle word would satisfy the same
display as Theorem 3.15:
\[
n^{3^a}<2^{e_a}(n+1)^{6\cdot 2^a}.
\]
The opposite comparison is therefore the tail of Theorem 3.15:
it holds for \(a=5\) and \(n\ge 314\), and already for \(a=6\)
and \(n\ge 16\).

For \(2\le n<314\) and \(a=5\), and for \(2\le n<16\) and
\(a=6\), the word fails to return; these are the Lean
`native_decide` evaluations behind `no_cycle_word_three_even_eeoe`
(Appendix A). For \(a\ge 7\) and \(n<256\), Lemma 3.11 applies.
For \(a\ge 6\) and \(n\ge 16\), the tail of the previous
paragraph applies. \(\square\)

**Theorem 3.19 (mixed bunched family \(EOEOE\)).**
Let \(a\ge 4\) and \(n\ge 2\). The word \(O^aEOEOE\) is not a
cycle word at \(n\).

*Proof.* First let \(n\ge 32\), and write \(z=J^a(n)\),
\(w=\lfloor\sqrt z\rfloor\), and \(y\) for the last odd letter.
The suffix \(EOE\) again gives \(y^3<(n+1)^4\). The one-odd
envelope on \(w\) yields \(w^3\le 4s^2\), where \(s\) is the
image after \(O^aEO\). The last-odd cell and \(n\ge 32\) upgrade
this to \(w<(n+1)^2\), hence \(z<(w+1)^2\le(n+1)^4\). Combined
with Lemma 3.10, any such cycle word would satisfy
\[
n^{3^a}<2^{e_a}(n+1)^{2^{a+2}}.
\]
For \(n\ge 256\) and \(a\ge 4\), this is the shared tail already
used in Theorem 3.16.

For \(2\le n<256\), the cases \(a=4,5,6\) fail to return on that
window; this is the Lean `native_decide` evaluation behind
`no_cycle_word_three_even_eoeoe` (Appendix A). For \(a\ge 7\),
Lemma 3.11 applies. \(\square\)

**Theorem 3.20 (mixed bunched family \(EOOEOE\)).**
Let \(a\ge 3\) and \(n\ge 2\). The word \(O^aEOOEOE\) is not a
cycle word at \(n\).

*Proof.* First let \(a\ge 4\) and \(n\ge 4\), and write
\(z=J^a(n)\), \(u=\lfloor\sqrt z\rfloor\), and \(y\) for the last
odd letter. The suffix \(EOE\) gives \(y^3<(n+1)^4\), hence
\((y+1)^3<2(n+1)^4\). The two letters after \(u\) are odd, so
Lemma 3.10 at length two yields
\(u^9\le 2^{10}s^4<2^{10}(y+1)^8\). Cubing that display against
the last-odd successor bound produces
\(u^{27}<2^{38}(n+1)^{32}\). The same comparison as in
Theorem 3.17 then gives \(u<(n+1)^2\), hence
\(z<(u+1)^2\le(n+1)^4\). Combined with Lemma 3.10, any such
cycle word would satisfy the shared two-even tail of
Theorem 3.16.

Now let \(a=3\) and \(n\ge 256\). The prefix \(O^3\) against
\(z<(u+1)^2\) yields \(n^{27}<2^{38}(u+1)^{16}\), and the
two-odd plus last-odd geometry of the previous paragraph yields
\(u^{27}<2^{38}(n+1)^{32}\). These are the same two displays as
in the \(a=3\) case of Theorem 3.17, with \(u\) in place of
\(y\), and the same small/large split applies.

For \(2\le n<256\), the cases \(a=3,4,5,6\) fail to return on
that window; this is the Lean `native_decide` evaluation behind
`no_cycle_word_three_even_eooeoe` (Appendix A). For \(a\ge 7\),
Lemma 3.11 applies. \(\square\)

**Theorem 3.21 (gapped leftovers as cycle words).**
Let \(n\ge 2\). No cycle word at \(n\) has the form \(O^aEO^bEE\)
with \(a\ge 2\) and \(b\ge 4\), or the form \(O^aEO^bEOE\) with
\(a\ge 2\) and \(b\ge 3\).

*Proof.* Every cycle word has a minimum-based rotation. It is
therefore enough to check that every cyclic shift of either word
is an already-excluded cycle-minimum orientation.

Write \(w\) for the gapped word. In the first family,
\(\lvert w\rvert=a+b+3\). The rotation by \(k=0\) is the original
word, excluded as a cycle minimum by Theorem 3.13. The rotation
by \(k=a+1\) is the bootstrap word \(O^bEEO^aE\). That word has
an internal even letter and last gap at least \(2\). If
\(a\ge 3\), the last-gap threshold of Lemma 3.4 at \(OOO\) and
\(N=3\) excludes it. If \(a=2\), the same lemma at \(OO\) and
\(N=5\) excludes every start \(n\ge 5\); the remaining odd start
\(n=3\) does not realize four consecutive odd letters, so it
cannot follow \(O^b\) for \(b\ge 4\). The rotation by
\(k=a+b+2\) begins with the last even letter of \(w\), which
Theorem 3.2 forbids at a cycle minimum. Every other rotation
ends with an odd letter, likewise forbidden at a cycle minimum.

In the second family, \(\lvert w\rvert=a+b+4\). The same four
classes appear: the original word is Theorem 3.13; the rotation
by \(k=a+1\) is \(O^bEOEO^aE\), excluded by the same last-gap
thresholds, with the remaining start \(n=3\) and \(a=2\) either
failing to realize four odds or, when \(b=3\), reaching \(6\)
after \(OOOE\) and then meeting an odd letter; the rotation by
\(k=a+b+2\) begins \(OE\), forbidden by Theorem 3.2; and every
other rotation ends odd.

The original start need not be a cycle minimum. After rotation
the start is a minimum, so the hypothesis \(y<n\) that blocked
Theorem 3.13 does not arise. \(\square\)

Theorems 3.12--3.21 assemble into an even-count exclusion: no
cycle word has fewer than four even letters, so a nontrivial
cycle has period at least eleven (Theorem 3.22). Section 4
excludes later periods by financing.

A cycle minimum starts with two odd letters, ends with an even
letter, and is formally expanding (Theorem 3.2). Every integer
\(2\le n<12\) reaches \(1\), so a cycle minimum is at least
\(12\). Write \(e\) for the number of even letters.

**Lemma 3.21a (classification).**
Every minimum-based cycle word with at most three even letters
belongs to one of the families excluded by Lemma 3.4(v) and
Theorems 3.12--3.21.

*Proof.* Such a word starts \(OO\), ends \(E\), and is expanding.
If \(e=0\), the word is all-odd. If \(e=1\), it is \(O^aE\) with
\(a\ge 2\). If \(e=2\), it is \(O^aEO^cE\) with \(a\ge 2\); a last
run \(c\ge 2\) is the internal-even bootstrap of Lemma 3.4, and
the remaining shapes are the two-even families of Theorem 3.12.
If \(e=3\), it is \(O^aEO^bEO^cE\) with \(a\ge 2\); again
\(c\ge 2\) is the bootstrap, while \(c\in\{0,1\}\) is either a
gapped leftover (Theorem 3.21) or one of the seven bunched
families (Theorems 3.14--3.20). \(\square\)

**Theorem 3.22 (even-count).**
No word with fewer than four even letters is a cycle word at any
\(n\ge 2\). Equivalently, a nontrivial cycle word has at least
four even letters.

*Proof.* Every cycle word has a minimum-based rotation, with the
same even-count. Lemma 3.21a names the families. In detail:

If \(e=0\), the word is all-odd and cannot return, as in
Theorem 3.6.

If \(e=1\), the word is \(O^aE\) with \(a\ge 2\). The case
\(a=2\) is \(OOE\), excluded in Theorem 3.6. The cases
\(a\ge 3\) are Lemma 3.4(v).

If \(e=2\), the word is \(O^aEO^cE\) with \(a\ge 2\). A last
odd-run \(c\ge 2\) is an internal even letter followed by
\(OO\) or \(OOO\). Lemma 3.4 at the cycle minimum
(\(n\ge 12\)) contradicts the last-even cell. The remaining
shapes are \(O^aEE\) and \(O^aEOE\). Expansion forces
\(a\ge 4\) and \(a\ge 3\) respectively, so both are
Theorem 3.12.

If \(e=3\), the word is \(O^aEO^bEO^cE\) with \(a\ge 2\).
Again \(c\ge 2\) is the internal-even bootstrap. The remaining
last runs are \(c=0\) and \(c=1\). For \(c=0\) and
\(b\ge 4\) the word is a gapped leftover \(O^aEO^bEE\),
excluded by Theorem 3.21. For \(c=0\) and \(b\le 3\) the
word is one of \(O^aEEE\), \(O^aEOEE\), \(O^aEOOEE\),
\(O^aEOOOEE\), excluded by Theorems 3.14--3.17 once
expansion supplies the stated lower bounds on \(a\). For
\(c=1\) and \(b\ge 3\) the word is a gapped leftover
\(O^aEO^bEOE\), excluded by Theorem 3.21. For \(c=1\) and
\(b\le 2\) the word is one of \(O^aEEOE\), \(O^aEOEOE\),
\(O^aEOOEOE\), excluded by Theorems 3.18--3.20.

Thus \(e\le 3\) is impossible. \(\square\)

**Corollary 3.23.**
A nontrivial cycle, if one exists, has period at least eleven.

*Proof.* Theorem 3.22 gives four even letters, hence
\(o\le L-4\). Formal expansion is \(2^L<3^o\le 3^{L-4}\).
The comparison \(2^L<3^{L-4}\) first holds at \(L=11\).
\(\square\)

In particular there is no cycle of length eight, nine, or ten.
A single coarse successor power \((n+1)^K\) cannot exclude the
four families of Theorems 3.17--3.20 by the same cell used for
Theorems 3.15 and 3.16: at the first expanding prefix length,
the exponent \(K\cdot 2^a\) meets or exceeds \(3^a\) for those
four words, so those arguments use a tight last-odd cell.

## 4. Cycle finance

A cycle word is formally expanding (Theorem 3.2), yet the orbit
returns exactly. The multiplicative surplus \(3^o-2^L\) must be
financed by the floor remainders, which are relatively \(O(1/x)\)
in logarithms. The resulting bound on the cycle minimum excludes
every period that is not admissible for the inequality, once a
residual floor is known.

Throughout this section write \(L=|w|\) and \(o=\#O(w)\) for a
cycle word \(w\) based at a cycle minimum \(n\ge 2\). Natural
logarithms are written \(\log\). The unique one-step fibres of
Section 3 give, for every state \(x\ge 1\) with image
\(y=J(x)\),
\[
y^2\le x^e<(y+1)^2,
\qquad
e=\begin{cases}1,&x\text{ even},\\3,&x\text{ odd}.\end{cases}
\]

**Lemma 4.1 (dyadic-cell logarithm).**
If \(z,y\ge 1\) and \(z<(y+1)^2\), then
\(\log z\le 2\log y+2/y\).

*Proof.* The hypothesis gives \(\log z\le 2\log(y+1)\). The
inequality \(\log(1+u)\le u\) for \(u>0\) yields
\(\log(y+1)=\log y+\log(1+1/y)\le\log y+1/y\). \(\square\)

**Lemma 4.2 (one-step bounds).**
Let \(x\ge 2\) and \(y=J(x)\). If \(x\) is even, then
\(\log x\le 2\log y+2/y\). If \(x\) is odd, then
\(3\log x\le 2\log y+2/y\).

*Proof.* The even cell is \(y^2\le x<(y+1)^2\). The cell logarithm
lemma on \(z=x\) is the first claim. The odd cell is
\(y^2\le x^3<(y+1)^2\). The same lemma on \(z=x^3\) gives
\(\log(x^3)\le 2\log y+2/y\). \(\square\)

On a cycle minimum every proper prefix is non-contracting: a
prefix with \(3^{\#O}<2^{k}\) would satisfy
\(J^k(n)<n\) by Corollary 2.3, contradicting minimality. Thus
\(2^k\le 3^{o_k}\) for every prefix of length \(k\), where
\(o_k\) is the odd count of that prefix.

**Lemma 4.3 (unrolled envelope).**
Write \(x_k=J^k(n)\) and \(o_k\) for the odd count of the length-\(k\)
prefix. For every \(0\le k\le L\),
\[
3^{o_k}\log n
\le
2^k\log x_k
+\frac{k\,3^{o_k}}{n}.
\]

*Proof.* The case \(k=0\) is an equality. Suppose the claim holds
at \(k<L\), and write \(x=x_k\) and \(y=x_{k+1}\). Minimality gives
\(n\le y\), and the prefix law gives \(2^{k+1}\le 3^{o_{k+1}}\),
hence
\[
\frac{2^{k+1}}{y}\le\frac{3^{o_{k+1}}}{n}.
\]

If the next letter is even, then \(o_{k+1}=o_k\) and the one-step
bound gives \(\log x\le 2\log y+2/y\). Multiply by \(2^k\) and add the
inductive remainder:
\[
3^{o_k}\log n
\le
2^{k+1}\log y
+\frac{2^{k+1}}{y}
+\frac{k\,3^{o_k}}{n}
\le
2^{k+1}\log y
+\frac{(k+1)\,3^{o_k}}{n}.
\]

If the next letter is odd, then \(o_{k+1}=o_k+1\). Multiply the
inductive bound by \(3\) and apply the one-step bound in the form
\(3\log x\le 2\log y+2/y\):
\[
3^{o_k+1}\log n
\le
2^{k+1}\log y
+\frac{2^{k+1}}{y}
+\frac{k\,3^{o_k+1}}{n}
\le
2^{k+1}\log y
+\frac{(k+1)\,3^{o_k+1}}{n}.
\]
This is the claim at \(k+1\). \(\square\)

**Theorem 4.4 (finance).**
Let \(w\) be a cycle word of length \(L\) with \(o\) odd letters,
based at a cycle minimum \(n\ge 2\). Then
\[
n\log n\cdot(3^o-2^L)\le L\cdot 3^o.
\]

*Proof.* Apply Lemma 4.3 at \(k=L\). Periodicity gives
\(x_L=n\) and \(o_L=o\), so
\[
3^o\log n\le 2^L\log n+\frac{L\cdot 3^o}{n}.
\]
The word is formally expanding, so \(3^o>2^L\). Rearranging and
multiplying by \(n\) is the claim. \(\square\)

A cycle must expand under the idealized map, but the exact orbit
returns. The discrepancy between ideal and actual dynamics must
be paid for by floor errors. At large state size those errors
are too small to finance a non-negligible exponent surplus
\(3^o-2^L\). The only analytic input is \(\log(1+u)\le u\). The
Lean form is exactly Theorem 4.4 (constant \(1\)).

This is a floor-power realization of a financing method, not a
new method. The novelty is the \(n\log n\) inequality for \(J\)
and the admissible length set it produces.

The computational table of Theorem 4.6 uses a weaker per-step
bound, valid on every cycle because every start below \(12\)
reaches \(1\) (so every cycle state is at least \(12\)). For a
state \(x\) with image \(y=J(x)\ge 12\), the relative defect
\(\delta=(x^e-y^2)/x^e\) satisfies \(\delta\le 2/y\le 1/6\).
Writing \(\varepsilon=-\tfrac12\log(1-\delta)\) and using
\(-\log(1-\delta)\le\tfrac65\delta\) on \([0,1/6]\) gives
\(\varepsilon\le(6/5)/y\). Unrolling
\(t_{i+1}=(e_i/2)\,t_i-\varepsilon_i\) around the cycle then yields
\[
1-\frac{2^L}{3^o}
\le
\frac65\sum_{i=1}^{L}\frac{1}{x_i\log x_i}
\le
\frac65\cdot\frac{L}{n\log n}.
\]
This is Theorem 4.4 with an extra factor \(6/5\) on the right, so
it is conservative relative to constant \(1\).

The right-hand side is largest at the least admissible odd count
\(o_{\min}(L)=\min\{o:3^o>2^L\}\). Define
\[
\gamma(L)=\frac{3^{o_{\min}(L)}}{2^L}-1,
\qquad
B(L)=\frac65\cdot\frac{L\cdot 3^{o_{\min}(L)}}{3^{o_{\min}(L)}-2^L},
\qquad
n_{\max}(L)=\max\{n\in\mathbb N:n\log n\le B(L)\}.
\]
The quantity \(\gamma(L)\) is the one-sided relative gap of
\(L\log 2\) to the next multiple of \(\log 3\). It is small
precisely when \(o_{\min}/L\) is a good one-sided approximation
to \(\log 2/\log 3\). The ordinary continued-fraction
convergents
\[
1,\;3,\;11,\;19,\;84,\;569,\;1054,\;\ldots
\]
are the record minima of \(\gamma\), but they are not the whole
admissible set: multiples and sums of those lengths also make
\(\gamma\) small.

For a descent floor \(N_0\), write
\[
\mathcal E(N_0)=\bigl\{L:1\le L\le 10^5,\; n_{\max}(L)>N_0\bigr\}.
\]
A length lies in \(\mathcal E(N_0)\) if and only if it is
*admissible to this bound*: Corollary 4.5 does not exclude it
at that floor. The set is not the set of dynamically plausible
periods, and membership is not evidence for a cycle. The
printed instance is \(\mathcal E=\mathcal E(10^6)\), with
\(\lvert\mathcal E\rvert=397\).

**Corollary 4.5.**
If every integer \(2\le n\le N_0\) reaches \(1\), then no
nontrivial cycle of length \(L\) exists whenever
\(n_{\max}(L)\le N_0\).

*Proof.* A periodic state never reaches \(1\), so every cycle
state is at least \(N_0+1\). Theorem 4.4 in the \(6/5\) form
forces the minimum to satisfy \(n\log n\le B(L)\), hence
\(n\le n_{\max}(L)\). \(\square\)

Record values include
\(n_{\max}(19)=297\), \(n_{\max}(84)=5599\),
\(n_{\max}(569)=58398\), and \(n_{\max}(1054)=1997197\).

**Theorem 4.6 (computational leftover).**
Every integer \(2\le n\le 10^6\) reaches \(1\). Consequently:

(A) there is no nontrivial Juggler cycle of length at most
\(1053\);

(B) if a nontrivial cycle has period \(L\le 10^5\), then
\(L\in\mathcal E\), where \(\lvert\mathcal E\rvert=397\).

In particular, any nontrivial cycle has period at least \(1054\).
The first record length with \(n_{\max}>10^6\) is \(1054\). That
is a property of the bound, not evidence for a \(1054\)-cycle.

*Proof.* The floor is a first-passage descent induction: every
start \(2\le n\le 10^6\) realizes a finite word with image
strictly below the start, and strong induction on the image
reaches \(1\). The longest first passage in the window has
\(253\) steps (seed \(78901\)); every iterate is an exact
integer. Weisstein [5] records the same floor; the run here is
a recomputation of that published verification.

The gap table computes \(o_{\min}(L)\) and \(n_{\max}(L)\) by
exact integer arithmetic for every \(1\le L\le 10^5\). Corollary
4.5 at \(N_0=10^6\) excludes every \(L\) with
\(n_{\max}(L)\le 10^6\). The complementary set in that range is
exactly \(\mathcal E\). The contiguous excluded prefix is
\(L\le 1053\). The record (one-sided best-approximation)
lengths in range are
\[
1,\;3,\;11,\;19,\;84,\;569,\;1054,\;25781,\;50508,
\]
with
\(n_{\max}=3,13,52,297,5599,58398,1997197,67410774,420161535\).
The first six of those already satisfy \(n_{\max}\le 10^6\) and
are excluded. The first admissible record length is \(L=1054\).
The remaining elements of \(\mathcal E\) are multiples of
\(1054\) and combinations of the convergent lengths; the
defining algorithm and checksums are Appendix B.
\(\square\)

The former record lengths \(84\) and \(569\) are therefore not
admissible at this floor. Membership of \(1054\) in \(\mathcal E\)
means only that the present method does not exclude it.

## 5. Remarks

A start \(n\ge 2\) has a *descent certificate* if there exists a
realized finite word \(w\) with \(J^{|w|}(n)<n\). Even starts
realize \(E\): \(\lfloor\sqrt n\rfloor<n\). An odd start with even
image realizes \(OE\), and \(J^2(n)\le n^{3/4}<n\). The starts
not covered by those two words are exactly the odd-to-odd starts.
If every start above \(1\) has some descent certificate, ordinary
strong induction yields arrival at \(1\). That hypothesis is not
proved.

The first odd-to-odd image expands, so ordinary strong induction
cannot fire on the odd-to-odd class. A uniform run bound on
expanding blocks is likewise unavailable: four consecutive expanding
blocks occur already at
\[
1999\xrightarrow{OOE}5169
\xrightarrow{OOOOEE}50093
\xrightarrow{OOE}193753
\xrightarrow{OOE}887471,
\]
and the relative slack of a single letter tends to \(0\) with the
state (Section 2).

These results provide no control over the remaining lengths in
\(\mathcal E\), and in particular do not imply termination or
exclude all cycles. It is open whether every start reaches \(1\),
and open whether a cycle of an admissible leftover length exists.

Lean names for the theorems of Sections 2, 3, and 4 are in
Appendix A. The formalization and the finance tables are pinned
in Section 1.2. Theorem 4.6 is a named computation.

## Appendix A. Lean names

The proofs in the text are ordinary integer arguments. The following
names are the corresponding Lean theorems in
`formal/Problems/Juggler/`, imported by `Problems.JugglerPaper`.

| Text | Lean |
|---|---|
| itinerary semantics | `follows_iff_word`, `image_eq_iterate`, `image_append` |
| Theorem 2.1 | `image_monotone_of_follows` |
| Theorem 2.2 | `power_bound_word` |
| Corollary 2.3 | `power_bound_contracts` |
| Theorem 2.4 | `global_defect_identity` |
| Theorem 2.5 | `global_defect_eq_zero_iff_localsTight`, `global_defect_eq_zero_implies_monochrome`, `power_bound_eq_iff_extremal` |
| Theorem 2.6 | `global_defect_append` |
| Corollary 2.7 | `image_eq_start_defectRatio` |
| per-step slack | `one_plus_eta_lt_succ_sq` |
| Lemma 3.1 | `odd_cell_unique` |
| Theorem 3.2 | `cycle_word_formally_expanding`, `cycleMin_start_odd`, `cycleMax_start_even`, `cycleMin_not_end_odd`, `square_scale_superquadratic`, `cycleMin_to_even_superquadratic` |
| Lemma 3.3 | `lower_growth_word` |
| Lemma 3.4 | `oo_suffix_threshold`, `ooo_suffix_threshold`, `threshold_inherits_odd_append`, `cycle_last_even_interval`, `no_cycle_odd_run_append_even` |
| Lemma 3.5 | `no_cycle_word_oooeoe`, `no_cycle_word_ooooee` |
| Theorem 3.6 | `no_cycle_word_length_le_six` |
| Lemma 3.7 | `no_cycle_word_ooooeoe`, `no_cycle_word_oooooee` |
| Theorem 3.8 | `no_cycle_word_length_le_seven`, with `no_cycle_word_ooeoooe`, `no_cycle_word_oooeooe` |
| Lemma 3.9 | `cycle_trailing_evens_lt` |
| Lemma 3.10 | `lowerDenom_replicate_odd`, `odd_run_lower_growth` |
| Lemma 3.11 | `no_follows_seven_odds_of_lt256` |
| Theorem 3.12 | `no_cycle_word_two_even_ee`, `no_cycle_word_two_even_eoe` |
| Theorem 3.13 | `no_cycleMin_gapped_three_even_ee`, `no_cycleMin_gapped_three_even_eoe` |
| Theorem 3.14 | `no_cycle_word_three_even_eee`, with `no_cycle_word_ooooooeee` |
| Theorem 3.15 | `no_cycle_word_three_even_eoee` |
| Theorem 3.16 | `no_cycle_word_three_even_eooee` |
| Theorem 3.17 | `no_cycle_word_three_even_eoooee` |
| Theorem 3.18 | `no_cycle_word_three_even_eeoe` |
| Theorem 3.19 | `no_cycle_word_three_even_eoeoe` |
| Theorem 3.20 | `no_cycle_word_three_even_eooeoe` |
| Theorem 3.21 | `no_cycle_word_gapped_three_even_ee`, `no_cycle_word_gapped_three_even_eoe` |
| Theorem 3.22 | `no_cycle_word_even_count_le_three` |
| Corollary 3.23 | `cycle_word_length_ge_eleven` |
| Lemma 3.21a | the case split of Theorem 3.22 |
| Lemma 4.1 | `log_le_two_log_add` |
| Lemma 4.2 | `log_step_even`, `log_step_odd` |
| Lemma 4.3 | `cycleMin_log_envelope` |
| Theorem 4.4 | `cycleMin_finance` |
| short certificates (Section 5) | `even_finiteProgress`, `odd_even_finiteProgress` |
| no certificate \(\Rightarrow\) odd-to-odd | `no_finiteProgress_implies_odd_odd` |
| induction to \(1\) | `reachesOne_of_all_finiteProgress` |
| four-block chain | `four_block_pe_1999` |

## Appendix B. Admissible lengths

The record lengths of \(\gamma(L)\) through \(10^5\), with the
\(6/5\) bound \(n_{\max}\) of Section 4, are

| \(L\) | \(o_{\min}\) | \(n_{\max}\) |
|---:|---:|---:|
| \(1\) | \(1\) | \(3\) |
| \(3\) | \(2\) | \(13\) |
| \(11\) | \(7\) | \(52\) |
| \(19\) | \(12\) | \(297\) |
| \(84\) | \(53\) | \(5599\) |
| \(569\) | \(359\) | \(58398\) |
| \(1054\) | \(665\) | \(1997197\) |
| \(25781\) | \(16266\) | \(67410774\) |
| \(50508\) | \(31867\) | \(420161535\) |

At the floor \(N_0=10^6\) the first six rows are excluded. The
set \(\mathcal E=\mathcal E(10^6)\) is defined by the algorithm
of Section 4: for each \(1\le L\le 10^5\), compute
\(o_{\min}(L)\) and \(n_{\max}(L)\) by exact integer arithmetic,
and retain \(L\) if and only if \(n_{\max}(L)>10^6\). This
produces \(397\) lengths. The first few are
\[
1054,\;2108,\;3162,\;4216,\;5270,
\]
and a typical combination is \(23757=22\cdot 1054+569\). The
last is \(99729\). The complete list is the `lengths` array of
the object with `"floor": 1000000` in
`data/research/juggler/cycle_finance/exceptions.json`.
The SHA-256 of that array, serialized as a JSON list of integers
with no spaces, is
`6d2c75fb6165f41123164122bd799e598c6ce0ba79d79d3af909cf400551f72c`.
The SHA-256 of the whole file `exceptions.json` is
`31f589e2353a26b13503d9fba603565fe3e6319030f6e429d8a2fb440e063c0e`.
The SHA-256 of the first-passage file `floor.json` in the same
directory is
`5b1ce1eec61301cf5b4f969cd5b58954255194e5c7b21c08a518d71679af87fc`.
Both files are regenerated by
`python -m research.juggler_sequence.cycle_finance`.
The finite leftover tables of Section 3 are the Lean
`native_decide` evaluations named in Appendix A
(`LeftoverEval.lean`, `LeftoverShort.lean`,
`LeftoverFamilies.lean`).

## Acknowledgments

Computational and formal-assistant tools were used in the
development and verification of the manuscript; all mathematical
statements and code are the responsibility of the author.

## References

1. C. A. Pickover, *Computers and the Imagination: Visual Adventures
   Beyond the Edge*, St. Martin's Press, New York, 1991, ch. 40,
   p. 232.
2. C. A. Pickover, *The Mathematics of Oz: Mental Gymnastics from
   Beyond the Edge*, Cambridge University Press, Cambridge, 2002,
   ch. 45, pp. 102--106.
3. OEIS Foundation Inc., “Juggler sequence: if \(n\) even then
   \(\lfloor\sqrt n\rfloor\) else \(\lfloor n^{3/2}\rfloor\),”
   Sequence A094683 in *The On-Line Encyclopedia of Integer Sequences*,
   https://oeis.org/A094683 (accessed 28 August 2026).
4. OEIS Foundation Inc., “Number of steps needed for n to reach 1 in
   the juggler sequence,” Sequence A007320 in *The On-Line
   Encyclopedia of Integer Sequences*,
   https://oeis.org/A007320 (accessed 29 August 2026).
5. E. W. Weisstein, “Juggler Sequence,” *MathWorld*,
   https://mathworld.wolfram.com/JugglerSequence.html (accessed
   29 August 2026).
6. OEIS Foundation Inc., “Largest value in trajectory of n under the
   juggler map of A094683,” Sequence A094716 in *The On-Line
   Encyclopedia of Integer Sequences*,
   https://oeis.org/A094716 (accessed 29 August 2026).
7. V. Prasad and M. A. Prasad, “Estimates of the maximum excursion
   constant and stopping constant of juggler-like sequences,”
   ResearchGate preprint, 2025.
   https://doi.org/10.13140/RG.2.2.14110.04168.
8. J. C. Lagarias, “The \(3x+1\) problem and its generalizations,”
   *Amer. Math. Monthly* 92 (1985), 3--23.
   [doi:10.1080/00029890.1985.11971528](https://doi.org/10.1080/00029890.1985.11971528).
9. J. C. Lagarias (ed.), *The Ultimate Challenge: The \(3x+1\)
   Problem*, American Mathematical Society, Providence, RI, 2010.
10. R. E. Crandall, “On the ``\(3x+1\)'' problem,” *Math. Comp.* 32
    (1978), 1281--1292.
    [doi:10.1090/S0025-5718-1978-0480321-3](https://doi.org/10.1090/S0025-5718-1978-0480321-3).
11. K. R. Matthews and A. M. Watts, “A generalization of Hasse's
    generalization of the Syracuse algorithm,” *Acta Arith.* 43
    (1984), 167--175.
    [doi:10.4064/aa-43-2-167-175](https://doi.org/10.4064/aa-43-2-167-175).
12. J. L. Simons and B. M. M. de Weger, “Theoretical and
    computational bounds for \(m\)-cycles of the \(3n+1\)-problem,”
    *Acta Arith.* 117 (2005), 51--70.
    [doi:10.4064/aa117-1-3](https://doi.org/10.4064/aa117-1-3).
13. S. Eliahou, “The \(3x+1\) problem: new lower bounds on
    nontrivial cycle lengths,” *Discrete Math.* 118 (1993),
    45--56.
    [doi:10.1016/0012-365X(93)90052-U](https://doi.org/10.1016/0012-365X(93)90052-U).
