---
title: Power envelopes, exact defects, and cycle restrictions for the Juggler map
author: Philippe Cochin
date: 29 August 2026
subtitle: Short note. Not submitted.
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
We do not prove that conjecture.

We develop an exact finite-word calculus for the Juggler map. For every
parity word \(w\) realized at \(n\), the endpoint satisfies the power envelope
\[
J^{|w|}(n)^{2^{|w|}}\le n^{3^{\#O(w)}}.
\]
Hence \(3^{\#O(w)}<2^{|w|}\) forces \(J^{|w|}(n)<n\) whenever \(n\ge2\).
Local floor remainders lift through later exponents to an exact global
defect. We prove its identity, vanishing classification, and composition
law: concatenation is a two-term power-gap, and zero defect gives precisely
the rigid monochrome towers. Exact inverse cells then yield necessary cycle
restrictions, including superquadratic prefixes from a cycle minimum to
later even states, and a small-cycle census: the Juggler map has no
nontrivial cycle of length at most six. Length seven remains open.

As a secondary application, every even start and every odd start whose
first image is even has a uniform one- or two-step descent certificate.
The starts not covered by those two certificates are exactly the
odd-to-odd class; many of those starts still descend after a longer
word. No density result is stated or used here.

All finite-word statements are conditional on the realized itinerary.

## 1. Introduction

The Juggler sequence was introduced by Pickover [1]; see also OEIS A094683
[2]. Universal arrival at \(1\) remains open.

The map combines a contracting even branch with an expanding odd branch,
\[
E(n)=\lfloor n^{1/2}\rfloor,\qquad
O(n)=\lfloor n^{3/2}\rfloor.
\]
A word of length \(k\) with \(o\) odd letters has ideal exponent
\(3^o/2^k\). Floors are applied after every letter, and a word is available
only when the orbit realizes those parities. The paper records the exact
finite-word comparison, the compositional slack, and the uniform short
certificates.

The main contribution is the exact power-envelope and defect calculus,
together with its inverse-cell and cycle consequences, chief among
them a small-cycle census: no nontrivial cycle has length at most six.
To the best of our knowledge, the global-defect identity and composition
law (Theorems 2.4 and 2.6) and the cycle census (Theorem 3.6) are new
for the exact Juggler map.
Section 2 records the envelope and defect calculus. Section 3 proves
the cycle restrictions and the census. Section 4 records the uniform
short certificates. Section 5 states the remaining gap.

### 1.1 Verification convention

The arguments of Sections 2--4 are written below and may be read
without Lean. Lean supplies an independent check of those arguments;
the corresponding names are collected in Appendix A. Lemma 3.5 uses a
table of \(254\) six-step evaluations for \(2\le n<256\); that table is
a finite computation, not a termination proof. The four-block chain
in Section 5 is Lean-certified.

### 1.2 Related work

The map is Pickover's [1]. The one-step sequence is OEIS A094683 [2];
the stopping-time table is A007320 [8]. We know of no published
exclusion of nontrivial cycles for \(J\). Prasad–Prasad [9] estimate
excursion and stopping constants for juggler-like maps by a
random-walk large-deviation model; those estimates do not apply to
the exact floor-power map. Small-cycle censuses are a standard first
layer for Collatz-like maps, surveyed by Lagarias [3,4]; those
results do not apply here, because the branches are floor powers
rather than affine maps (Crandall [5], Matthews–Watts [6]).
Itinerary-class densities are the subject of a companion manuscript
in preparation [7], which imports from this note only Corollary 2.3;
the present arguments do not use it.

## 2. Finite words, envelope, and defect

Let \(\mathcal B=\{E,O\}\). A finite word \(w\in\mathcal B^*\) is
*realized* at \(n\in\mathbb N\) when the successive parities of the orbit
of \(n\) are exactly the letters of \(w\). Write \(J^{|w|}(n)\) for the
endpoint after those letters, and \(\#O(w)\) for the number of odd
letters.

The identities in this section are formalized in Lean; names are in
Appendix A. The proofs below are the ordinary integer arguments.

**Theorem 2.1 (fixed-word monotonicity).**
If \(n\le m\) and both realize \(w\), then
\(J^{|w|}(n)\le J^{|w|}(m)\).

*Proof.* Induct on \(w\). The empty word is immediate. For the induction
step, the two current states realize the same next letter. On the even
branch, monotonicity follows from monotonicity of the integer square root;
on the odd branch it follows from monotonicity of \(x\mapsto x^3\) followed
by the integer square root. Apply the induction hypothesis to the prefix
and then the appropriate branch inequality. \(\square\)

The realizing set of a fixed word need not be an interval.

**Theorem 2.2 (finite-word power envelope).**
If \(w\) is realized at \(n\) and \(m=J^{|w|}(n)\), then
\[
m^{2^{|w|}}\le n^{3^{\#O(w)}}.
\]

*Proof.* Write \(k=|w|\) and \(o=\#O(w)\). The empty word is the equality
\(n\le n\). Suppose the bound holds at a realized prefix ending at
\(x\), and the next letter is realized.

If the next letter is even, then \(J(x)=\lfloor\sqrt x\rfloor\), so
\(J(x)^2\le x\). Raising the inductive bound to the second power gives
\[
J(x)^{2^{k+1}}=(J(x)^2)^{2^k}\le x^{2^k}\le n^{3^o}.
\]
The odd count is unchanged.

If the next letter is odd, then \(J(x)=\lfloor x^{3/2}\rfloor\), so
\(J(x)^2\le x^3\). Therefore
\[
J(x)^{2^{k+1}}=(J(x)^2)^{2^k}\le x^{3\cdot 2^k}=(x^{2^k})^3
\le\bigl(n^{3^o}\bigr)^3=n^{3^{o+1}}.
\]
This is the claimed bound after one more odd letter. \(\square\)

**Corollary 2.3 (exponent-gap contraction).**
If \(n\ge2\), \(w\) is realized at \(n\), and
\(3^{\#O(w)}<2^{|w|}\), then \(J^{|w|}(n)<n\).

*Proof.* Let \(m=J^{|w|}(n)\) and \(k=|w|\). Theorem 2.2 gives
\(m^{2^k}\le n^{3^{\#O(w)}}\). The exponent gap and \(n\ge2\) give
\(n^{3^{\#O(w)}}<n^{2^k}\), so \(m^{2^k}<n^{2^k}\). Since \(m\ge1\), one
has \(m<n\). \(\square\)

The corollary includes familiar contracting blocks such as \(OOOEE\). It
does not prove that every start realizes some contracting word.

The floor slack is exact, and it is not an additive path sum. For a
single branch,
\[
x^e=J(x)^2+\rho(x),\qquad
e=\begin{cases}1,&x\ {\rm even},\\3,&x\ {\rm odd},\end{cases}
\]
with \(0\le\rho(x)<2J(x)+1\). Write
\[
\operatorname{gap}(a,\rho,e)=(a+\rho)^e-a^e,
\]
so \(a^e+\operatorname{gap}(a,\rho,e)=(a+\rho)^e\). If \(e\ge1\), then
\(\operatorname{gap}(a,\rho,e)=0\) if and only if \(\rho=0\), and
\(\rho^e\le\operatorname{gap}(a,\rho,e)\).

Along a realized word \(w\), write \(x_0=n\) and \(x_{j+1}=J(x_j)\), and
let \(\rho_j=\rho(x_j)\). Define a running slack by \(D_0=0\) and
\[
D_{j+1}=
\begin{cases}
D_j+\operatorname{gap}(x_{j+1}^2,\rho_j,2^j),
& \text{next letter even},\\[4pt]
\operatorname{gap}(x_{j+1}^2,\rho_j,2^j)
+\operatorname{gap}(x_j^{2^j},D_j,3),
& \text{next letter odd}.
\end{cases}
\]
The *global defect* is \(\Delta_w(n)=D_{|w|}\). An even letter keeps the
old slack and lifts the new remainder through \(2^j\). An odd letter
first cubes the running slack and then lifts the new remainder. In
particular \(\Delta\) is not the sum of the local remainders.

**Theorem 2.4 (global defect identity).**
If \(w\) is realized at \(n\) and \(m=J^{|w|}(n)\), then
\[
n^{3^{\#O(w)}}=m^{2^{|w|}}+\Delta_w(n),\qquad\Delta_w(n)\ge0.
\]
Theorem 2.2 is the inequality \(\Delta_w(n)\ge0\).

*Proof.* The empty word is \(n=n+0\). Suppose a realized prefix of
length \(k\) with odd count \(o\) ends at \(x\) and satisfies
\(n^{3^o}=x^{2^k}+D\).

If the next letter is even, then \(x=J(x)^2+\rho(x)\), so
\[
n^{3^o}
=(J(x)^2+\rho(x))^{2^k}+D
=J(x)^{2^{k+1}}+D+\operatorname{gap}(J(x)^2,\rho(x),2^k).
\]
The odd count is unchanged, and the new slack is the even update.

If the next letter is odd, then \(x^3=J(x)^2+\rho(x)\). Cubing the
inductive identity gives
\[
n^{3^{o+1}}=(x^{2^k}+D)^3
=x^{3\cdot 2^k}+\operatorname{gap}(x^{2^k},D,3).
\]
The leading term is
\[
x^{3\cdot 2^k}
=(J(x)^2+\rho(x))^{2^k}
=J(x)^{2^{k+1}}+\operatorname{gap}(J(x)^2,\rho(x),2^k),
\]
which is the odd update. \(\square\)

For a one-letter illustration, take \(n=3\) and \(w=O\). Then
\(J(3)=5\) and \(3^3=27=5^2+2\), so \(\Delta_O(3)=2\). The local
remainder is \(\rho=2\), and the global defect equals that remainder
only because the word has length one; after a later letter the lift
is a power-gap, not a sum of remainders.

**Theorem 2.5 (vanishing).**
If \(w\) is realized at \(n\), the following are equivalent.

1. \(\Delta_w(n)=0\).
2. Every local remainder along \(w\) vanishes.
3. \(J^{|w|}(n)^{2^{|w|}}=n^{3^{\#O(w)}}\).

In that case \(w\) is monochrome. More precisely, either \(w=E^k\) and
\(n=a^{2^k}\) for an even \(a\), or \(w=O^k\) and \(n=a^{2^k}\) for an
odd \(a\). A realized mixed word therefore has \(\Delta_w(n)>0\).

*Proof.* The identity of Theorem 2.4 gives (1)\(\Leftrightarrow\)(3).
For (1)\(\Leftrightarrow\)(2), use the recurrence. If \(e\ge1\), a
power-gap vanishes if and only if its addend vanishes. The even update
is a sum of two nonnegative terms, and the odd update is a sum of two
power-gaps; either vanishes only when the incoming slack and the new
remainder both vanish. Thus \(D_{|w|}=0\) forces \(D_0=0\) and every
\(\rho_j=0\). The converse is immediate.

If every remainder vanishes, an even step satisfies
\(x_j=x_{j+1}^2\), while an odd step satisfies
\(x_j^3=x_{j+1}^2\). In either case \(x_j\) and \(x_{j+1}\) have the
same parity, so the itinerary is monochrome. If \(w=E^k\), repeated
substitution gives \(n=x_k^{2^k}\); writing \(a=x_k\), its parity is
even. If \(w=O^k\), unique factorization applied to
\(x_j^3=x_{j+1}^2\) shows that every prime valuation of \(x_j\) is
divisible by \(2\). Iterating this valuation relation shows that every
prime valuation of \(n=x_0\) is divisible by \(2^k\), hence
\(n=a^{2^k}\) for an odd \(a\). Conversely, these even and odd towers
make every local remainder zero. \(\square\)

**Theorem 2.6 (composition).**
If \(u\) is realized at \(n\) and \(v\) is realized at
\(m=J^{|u|}(n)\), then
\[
\Delta_{uv}(n)
=
\operatorname{gap}\bigl(m^{2^{|u|}},\,\Delta_u(n),\,3^{\#O(v)}\bigr)
+
\operatorname{gap}\bigl(J^{|v|}(m)^{2^{|v|}},\,\Delta_v(m),\,2^{|u|}\bigr).
\]
In particular
\(\Delta_v(m)^{2^{|u|}}\le\Delta_{uv}(n)\). Every local remainder
satisfies \(\rho_j^{2^j}\le\Delta_w(n)\).

*Proof.* Write \(o_u=\#O(u)\) and \(o_v=\#O(v)\). Theorem 2.4 on \(u\)
and on \(uv\) gives
\[
n^{3^{o_u+o_v}}
=\bigl(m^{2^{|u|}}+\Delta_u(n)\bigr)^{3^{o_v}}
=J^{|uv|}(n)^{2^{|uv|}}+\Delta_{uv}(n).
\]
The first power expands as
\[
m^{2^{|u|}\cdot 3^{o_v}}
+\operatorname{gap}\bigl(m^{2^{|u|}},\,\Delta_u(n),\,3^{o_v}\bigr).
\]
Theorem 2.4 on \(v\) at \(m\) rewrites the leading term as
\[
\bigl(J^{|v|}(m)^{2^{|v|}}+\Delta_v(m)\bigr)^{2^{|u|}},
\]
which expands as the second gap plus \(J^{|uv|}(n)^{2^{|uv|}}\).
Comparing the two expressions for \(n^{3^{o_u+o_v}}\) yields the
identity. The suffix inequality is
\(\rho^e\le\operatorname{gap}(a,\rho,e)\) on the second summand. For a
local remainder at index \(j\), split \(w\) after \(j\) letters: the
suffix defect is at least \(\rho_j\), and raising through \(2^j\) gives
the stated bound. \(\square\)

Composition is polynomial, not additive: later odd letters raise the
prefix slack to the third power, and later letters of either parity
raise a suffix slack through \(2^{|u|}\). The naive recurrence
\(\Delta\leftarrow\Delta+\rho\) is false.

**Corollary 2.7 (cycle surplus).**
If \(w\) is a cycle word at \(n\), that is \(J^{|w|}(n)=n\), then
\[
\Delta_w(n)=n^{3^{\#O(w)}}-n^{2^{|w|}}
\]
exactly. A cycle burns its entire formal surplus in floor losses.

*Proof.* Theorem 2.4 with \(m=n\). Nonnegativity of \(\Delta_w(n)\)
makes the difference a genuine one. \(\square\)

The identity does not supply a state-independent positive tax, and
none exists: the single-step slack is provably squeezed by the scale
of the state. For one realized letter at \(x\) with branch exponent
\(e\in\{1,3\}\),
\[
x^{e}<(J(x)+1)^2
\]
so the relative slack
\(1+\eta=x^{e}/J(x)^2\) satisfies
\[
\eta<\frac{2}{J(x)}+\frac{1}{J(x)^2},
\]
which tends to \(0\) as the state grows. A uniform per-step tax is
therefore impossible. The recorded extreme is an \(OOE\) block at
\(n=180370579261640036336071806107777\approx1.80\cdot10^{32}\) whose
word-relative slack
\[
q_w(n)=\frac{n^{3^{\#O(w)}}}{J^{|w|}(n)^{2^{|w|}}}-1
\]
satisfies \(0<q_{OOE}(n)<10^{-30}\); this is an exact-integer
computation, not an estimate. The inequality
\(\Delta_w(n)>n^{3^{\#O(w)}}-n^{2^{|w|}}\) on a formally expanding word
is exactly \(J^{|w|}(n)<n\), so it does not forbid mixed expanding
prefixes.

## 3. Inverse cells and cycles

The exact one-step fibers are
\[
J(n)=q\iff q^2\le n<(q+1)^2
\quad(n\ {\rm even})
\]
and
\[
J(n)=m\iff m^2\le n^3<(m+1)^2
\quad(n\ {\rm odd}).
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
and hence \(3a^2\le2m\). If \(a=0\), then \(m=0\) and the displayed
strict inequality is already impossible. If \(a>0\), squaring and using
\(m^2\le a^3\) gives \(9a^4\le4m^2\le4a^3\), contradicting
\(4a^3<9a^4\). \(\square\)

A nonempty realized word \(w\) with \(J^{|w|}(n)=n\) is a cycle word.
The identities in this section are formalized in Lean; names are in
Appendix A. The proofs below are the ordinary integer arguments.

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
exponents gives \(2^{|w|}\le3^{\#O(w)}\); equality is impossible because
the two sides have different prime divisors and \(|w|\ge1\).

Every state on such a cycle is at least \(2\): once an orbit reaches \(1\),
it remains there and cannot return to a start \(n\ge2\). An even state
\(x\ge2\) satisfies \(J(x)<x\), so a cycle minimum cannot be even. An odd
state \(x\ge3\) satisfies \(J(x)>x\), so a cycle maximum cannot be odd.
This proves the first assertion of (ii). For the final-letter assertion,
let \(x\) be the predecessor of a minimum-oriented return \(n\). If the
last letter were odd, the odd return cell would give
\(n^2\le x^3<(n+1)^2\). Minimality gives \(x\ge n\), hence
\(n^3<(n+1)^2\), impossible for \(n\ge3\); and the minimum is odd, so
\(n\ge3\).

For (iii), let a realized word \(v\) send \(n\) to \(y\ge n^2\).
Theorem 2.2 gives
\[
n^{2^{|v|+1}}=(n^2)^{2^{|v|}}
\le y^{2^{|v|}}\le n^{3^{\#O(v)}}.
\]
Since \(n\ge2\), comparison of exponents proves the superquadratic
inequality. On a cycle minimum, if a later state \(y\) is even, its
successor is at least \(n\). Thus \(n\le J(y)=\lfloor\sqrt y\rfloor\),
so \(n^2\le y\), and the preceding argument applies to that prefix.
\(\square\)

**Lemma 3.3 (coarse lower envelope).**
For \(n\ge1\), write \(q=\lfloor\sqrt n\rfloor\). Then
\(q^2\le n<(q+1)^2\). For \(q\ge1\) one has
\((q+1)^2\le4q^2\), and the second inequality is strict for \(q\ge2\),
while for \(q=1\) one has \(n<4\). In all cases
\[
n<4\,\lfloor\sqrt n\rfloor^2.
\]
Thus an even step satisfies \(n\le 4\,J(n)^2\) and an odd step
satisfies \(n^3\le 4\,J(n)^2\). Composing along a realized word \(v\) of
length \(k\) with odd count \(o\) gives
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
(i) If \(q\ge5\) realizes \(OO\), then \(J^2(q)\ge(q+1)^2\).
(ii) If \(q\ge3\) realizes \(OOO\), then \(J^3(q)\ge(q+1)^2\).
(iii) If a realized word \(v\) satisfies \(J^{|v|}(q)\ge(q+1)^2\) and
the next realized letter is odd, then
\(J^{|v|+1}(q)\ge(q+1)^2\).
(iv) If \(vE\) is a cycle word at \(n\), then
\(J^{|v|}(n)<(n+1)^2\).

*Proof.* For (i), write \(m=\lfloor q^{3/2}\rfloor\). The bound
\(J^2(q)\ge(q+1)^2\) follows from \(m^3\ge(q+1)^4\), because then
\(\lfloor m^{3/2}\rfloor\ge(q+1)^2\). If \(q=5\), then
\(11^2=121\le125=5^3<144=12^2\), so \(m=11\), and
\(11^3=1331\ge6^4=1296\). If \(q\ge7\), then \(m\ge q^{3/2}-1\), so it
is enough that \((q^{3/2}-1)^3\ge(q+1)^4\). Expanding the left side
and dropping the positive remainder \(3q^{3/2}-1\) reduces this to
\(q^{9/2}-3q^3\ge(q+1)^4\), or equivalently
\(\sqrt q-3/q\ge(1+1/q)^4\). The left side increases for \(q\ge7\) and
the right side decreases, so the case \(q=7\) suffices:
\[
\sqrt7-\frac37>\frac52-\frac37=\frac{29}{14}
  >\frac{4096}{2401}=\left(\frac87\right)^4,
\]
where \(\sqrt7>5/2\) follows from \(25/4<7\).

For (ii), the orbit \(3\to5\to11\to36\) gives \(J^3(3)=36\ge16\). If
\(q\ge5\) realizes \(OOO\), then it realizes \(OO\), so (i) gives
\(J^2(q)\ge(q+1)^2\). The third letter is odd, hence
\(J^3(q)=J(J^2(q))\ge J^2(q)\).

For (iii), the image after \(v\) is odd and at least \((q+1)^2\ge4\),
so the odd branch does not decrease it.

For (iv), the last letter is even, so the preimage \(z=J^{|v|}(n)\)
is even and satisfies \(n^2\le z<(n+1)^2\). \(\square\)

**Lemma 3.5 (two length-six exclusions).**
Neither \(OOOEOE\) nor \(OOOOEE\) is a cycle word at any \(n\ge2\).

*Proof.* First, if \(n\ge256\), then
\[
n^{81}>2^{130}(n+1)^{64}.
\]
Indeed \(257^{64}<2\cdot256^{64}\) because
\((1+1/256)^{64}<e^{64/256}=e^{1/4}<2\), and
\(256(n+1)\le257\,n\), so \((n+1)^{64}<2n^{64}\). Then
\(2^{130}(n+1)^{64}<2^{131}n^{64}\). Since \(n\ge256=2^8\), one has
\(n^{17}\ge2^{136}\), and therefore
\(2^{131}n^{64}<2^{136}n^{64}\le n^{81}\).

For \(2\le n<256\), neither word returns to its start. This is a
table of \(254\) evaluations of a six-step integer map and a return
test. The complete exact check is the following pseudocode, where
`isqrt` denotes the integer square root:

```python
from math import isqrt

def J(x):
    return isqrt(x) if x % 2 == 0 else isqrt(x**3)

for w in ("OOOEOE", "OOOOEE"):
    for n in range(2, 256):
        x = n
        realized = True
        for b in w:
            if ("E" if x % 2 == 0 else "O") != b:
                realized = False
                break
            x = J(x)
        assert not realized or x != n
```

Now suppose \(n\ge256\) realizes \(OOOOEE\), and write
\(z=J^4(n)\) for the image after the prefix \(OOOO\). Lemma 3.4(iv)
gives \(J(z)<(n+1)^2\), and the preceding even letter gives
\(z<(J(z)+1)^2\), hence \(z<(n+1)^4\). Lemma 3.3 on \(OOOO\) gives
\(n^{81}\le2^{130}z^{16}\), so
\(n^{81}<2^{130}(n+1)^{64}\), contradicting the tail inequality.

Finally suppose \(n\ge256\) realizes \(OOOEOE\). Write
\(z_3=J^3(n)\) and \(y=J(z_3)=\lfloor\sqrt{z_3}\rfloor\), so
\(z_3<(y+1)^2\). Lemma 3.3 on \(OOO\) gives
\(n^{27}\le2^{38}z_3^8<2^{38}(y+1)^{16}\). Cubing yields
\(n^{81}<2^{114}(y+1)^{48}\). The last letters \(OE\) give the odd-cell
bound \(y^3<(n+1)^4\). Write \(A=n+1\ge257\). We claim
\((y+1)^3<2A^4\). If \(y\le A\), this is \((A+1)^3<2A^4\). If
\(y>A\), then \(y\ge4\) and
\((y+1)^3=y^3+3y^2+3y+1<A^4+4y^2\), while \(4y^2<A^4\) because
\(4y^3<4A^4\le yA^4\). Raising \((y+1)^3<2A^4\) to the sixteenth
power gives \((y+1)^{48}<2^{16}(n+1)^{64}\). Combining with the cubed
lower envelope produces again \(n^{81}<2^{130}(n+1)^{64}\). \(\square\)

**Theorem 3.6 (small-cycle census).**
No word of length at most six is a cycle word at any \(n\ge2\).
Equivalently, a nontrivial Juggler cycle, if one exists, has period at
least seven.

*Proof.* Rotating a cycle word by one letter moves the base point one
step along the orbit and yields another cycle word; every state of
the cycle is at least \(2\), because an orbit that reaches \(1\) stays
at \(1\) and cannot return to a start \(n\ge2\).

If every letter is odd, the start is odd, hence \(n\ge3\), and the odd
branch strictly increases there: \(J(x)>x\) for odd \(x\ge3\), since
\(x^3\ge(x+1)^2\). The orbit ascends strictly and never returns.
Otherwise some letter is even, and a rotation ending just after that
letter produces an even-terminating cycle word \(vE\) of the same
length based at a cycle state \(m\ge2\). It therefore suffices to
exclude even-terminating cycle words of length at most six.

By Theorem 3.2(i) a cycle word is formally expanding. No
even-terminating word of length one or two is expanding (\(2>3^0\) and
\(4>3\)).

Length three: the only expanding candidate is \(OOE\). If \(m\ge5\)
realizes \(OO\), Lemma 3.4(i) gives \(J^2(m)\ge(m+1)^2\), contradicting
Lemma 3.4(iv). The only smaller odd start is \(m=3\), where
\(J^2(3)=11\) is odd, so the final even letter is not realized.

Length four: the expanding filter requires three odd letters among the
first three, leaving only \(O^3E\). Lemma 3.4(ii) and (iv) give
\(J^3(m)\ge(m+1)^2\) and \(J^3(m)<(m+1)^2\).

Length five: the filter requires four odd letters among the first
four, leaving only \(O^4E\). Lemma 3.4(ii) and (iii) give
\(J^4(m)\ge(m+1)^2\), again contradicting (iv).

Length six: the filter requires at least four odd letters among the
first five, leaving \(O^5E\), \(EOOOOE\), \(OEOOOE\), \(OOEOOE\),
\(OOOEOE\), and \(OOOOEE\). For \(O^5E\), Lemma 3.4(ii) and (iii)
give \(J^5(m)\ge(m+1)^2\), contradicting (iv). The word \(EOOOOE\)
rotates one step onto \(OOOOEE\), and \(OEOOOE\) rotates two steps
onto \(OOOEOE\); both are excluded by Lemma 3.5.

It remains to exclude \(OOEOOE\). Let this word be a cycle word at
some start, and rotate to a cycle minimum \(m\ge2\). The three
alignments of the two even letters are \(OOEOOE\), \(OEOOEO\), and
\(EOOEOO\). The last starts even, so it cannot be a minimum, by
Theorem 3.2(ii). The middle starts \(OE\): the first image is even
and strictly below \(m^2\), whereas every even state after a cycle
minimum is at least \(m^2\), as proved in Theorem 3.2(iii). Thus the minimum
orientation is \(OOEOOE\). In particular \(m\) is odd, so \(m\ge3\).
The prefix \(OOE\) must be realized. If \(m=3\), then
\(3\to5\to11\) and \(11\) is odd, so \(OOE\) is not realized. Hence
\(m\ge5\). Write \(y=J^3(m)\) for the state after \(OOE\). Then
\(y\ge m\) by minimality, so \(y\ge5\). The suffix \(OO\)
is realized at \(y\), and Lemma 3.4(i) gives
\(J^2(y)\ge(y+1)^2\ge(m+1)^2\). The last letter is even, so
Lemma 3.4(iv) gives \(J^2(y)<(m+1)^2\). \(\square\)

No exclusion of cycles of length seven or more is claimed. The census
stops at length six because length seven admits even-terminating
expanding words with two internal even letters that none of the
recorded thresholds reach; no exclusion at length seven is claimed.

## 4. Short descent certificates

A start \(n\ge2\) has a *descent certificate* if there exists a realized
finite word \(w\) with \(J^{|w|}(n)<n\). The predicate is existential
over all finite words, not only over words of length one or two.

**Theorem 4.1 (uniform short certificates).**
Let \(n\ge2\).

1. If \(n\) is even, then the one-letter word \(E\) is a descent
   certificate: \(J(n)=\lfloor\sqrt n\rfloor<n\).
2. If \(n\) is odd and \(J(n)\) is even, then the two-letter word \(OE\)
   is a descent certificate.

*Proof.* For (1), \(\lfloor\sqrt n\rfloor\le\sqrt n<n\) for \(n\ge2\).
For (2), the word \(OE\) is realized by hypothesis, and
\[
J^2(n)=\bigl\lfloor\sqrt{\lfloor n^{3/2}\rfloor}\bigr\rfloor
\le n^{3/4}<n
\]
for \(n\ge2\). \(\square\)

The starts not covered by Theorem 4.1 are exactly the odd-to-odd
starts: \(n\) odd and \(J(n)\) odd. In particular, if \(n\ge2\) has no
descent certificate of any length, then \(n\) is odd-to-odd. The
converse is false: many odd-to-odd starts descend after a longer word.

If every start above \(1\) has some descent certificate, ordinary strong
induction yields arrival at \(1\). The hypothesis is not proved. A
certificate at \(n\) only reduces the problem to a strictly smaller
positive integer, which may itself be odd-to-odd.

## 5. The remaining gap

Theorem 4.1 covers every even start and every odd-to-even start with a
uniform one- or two-step certificate. The first odd-to-odd image
expands, so ordinary strong induction cannot fire on the complement.

The gap resists a uniform run bound on expanding blocks. Lean
certifies a chain of four consecutive expanding blocks,
\[
1999\xrightarrow{OOE}5169
\xrightarrow{OOOOEE}50093
\xrightarrow{OOE}193753
\xrightarrow{OOE}887471.
\]
Thus expanding runs of length four occur. A uniform slack tax
per expanding block is likewise impossible: the relative slack of a
single letter tends to \(0\) with the state (Section 2), and the
\(OOE\) example recorded there near \(1.80\cdot10^{32}\) has relative
slack below \(10^{-30}\).

> No theorem forces every exact integer state into a contracting
> prefix. In particular, it is open whether every start reaches
> \(1\), and open whether a nontrivial cycle of length seven or more
> exists.

## 6. Software archive

Lean proofs of the theorems of Sections 2--4 are in the
[project repository](https://github.com/sneakyweasel/balanced_ternary/).
The archive is not required to read the arguments above. From a clone,
the review object for this note is

```text
cd formal && lake build Problems.JugglerPaper
```

That barrel imports only the modules named by this note (Appendix A).

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
| Theorem 3.2 | `cycle_word_formally_expanding`, `cycleMin_not_end_odd`, `square_scale_superquadratic`, `cycleMin_to_even_superquadratic` |
| Lemma 3.3 | `lower_growth_word` |
| Lemma 3.4 | `oo_suffix_threshold`, `ooo_suffix_threshold`, `threshold_inherits_odd_append` |
| Lemma 3.5 | `no_cycle_word_oooeoe`, `no_cycle_word_ooooee` |
| Theorem 3.6 | `no_cycle_word_length_le_six` |
| Theorem 4.1 | `even_finiteProgress`, `odd_even_finiteProgress` |
| no certificate \(\Rightarrow\) odd-to-odd | `no_finiteProgress_implies_odd_odd` |
| induction to \(1\) | `reachesOne_of_all_finiteProgress` |
| four-block chain | `four_block_pe_1999` |

## Acknowledgments

I used large language models extensively while drafting and revising the
text, organizing companion notes, and as an interactive assistant for
Lean statements, tests, and literature records. The models are not
authors. Lean theorems and named computations are the certificates for
the claims of Sections 2--4. I take full responsibility for the
contents.

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
4. J. C. Lagarias (ed.), *The Ultimate Challenge: The \(3x+1\) Problem*,
   American Mathematical Society, Providence, RI, 2010.
5. R. E. Crandall, “On the ``\(3x+1\)'' problem,” *Math. Comp.* 32
   (1978), 1281–1292.
   [doi:10.1090/S0025-5718-1978-0480321-3](https://doi.org/10.1090/S0025-5718-1978-0480321-3).
6. K. R. Matthews and A. M. Watts, “A generalization of Hasse's
    generalization of the Syracuse algorithm,” *Acta Arith.* 43 (1984),
    167–175.
    [doi:10.4064/aa-43-2-167-175](https://doi.org/10.4064/aa-43-2-167-175).
7. P. Cochin, “Parity equidistribution of nested floor powers, with
   descent applications to the Juggler map,” companion manuscript,
   in preparation, 2026.
8. OEIS Foundation Inc., “Number of steps needed for n to reach 1 in
   the juggler sequence,” Sequence A007320 in *The On-Line
   Encyclopedia of Integer Sequences*,
   https://oeis.org/A007320 (accessed 29 August 2026).
9. V. Prasad and M. A. Prasad, “Estimates of the maximum excursion
   constant and stopping constant of juggler-like sequences,”
   preprint, 2025.
   [doi:10.13140/rg.2.2.14110.04168](https://doi.org/10.13140/rg.2.2.14110.04168).
