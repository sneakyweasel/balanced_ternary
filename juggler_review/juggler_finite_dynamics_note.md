---
title: Power envelopes, exact defects, and cycle restrictions for the Juggler map
author: Philippe Cochin
date: 29 August 2026
subtitle: Publication draft. Not submitted.
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
first image is even has a uniform one- or two-step descent certificate;
the starts with no certificate at that horizon are exactly the
odd-to-odd class. The densities of itinerary word classes and of
certified-descent classes — the analytic side of the problem — are
developed in a companion manuscript [7]; no density result is stated
or used here.

All finite-word statements are conditional on the realized itinerary. The
remaining pointwise question is whether almost every odd-to-odd start has
some finite descent; no such theorem is proved here or in the companion.

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
The densities of the classes the certificates cover are the subject of
a companion manuscript [7], which imports from this paper only the
contraction criterion of Corollary 2.3.
We do not prove a Collatz theorem or transfer Collatz stopping-time
results to \(J\).

### 1.1 Verification convention

Every theorem in Sections 2--4 is proved both below and in Lean under
the names listed at the start of each section.
Proposition 4.4 is an exact Python-integer census,
not a theorem about an infinite set. The four-block chain named in
Section 5 is Lean-certified (`four_block_pe_1999`); the failed
reductions recorded there are exact-integer counterexamples, not
estimates. No finite computation is used as a termination proof.

### 1.2 Related maps

The nearest published comparison is the Collatz problem, surveyed by
Lagarias [3,4]. That literature is methodologically adjacent — parity
words, almost-all statements short of totality — but proves nothing
about \(J\); Crandall [5] and Matthews–Watts [6] treat
piecewise-affine Hasse–Syracuse maps, while the Juggler branches are
floor powers, not affine. The Juggler analogue of Terras's almost-all
stopping-time theorem would be an almost-all descent theorem on the
odd-to-odd class; the companion manuscript [7] develops the
parity-discrepancy program toward that statement and reviews the
analytic literature it builds on.

## 2. Finite words, envelope, and defect

Let \(\mathcal B=\{E,O\}\). A finite word \(w\in\mathcal B^*\) is
*realized* at \(n\in\mathbb N\) when the successive parities of the orbit
of \(n\) are exactly the letters of \(w\). Write \(J^{|w|}(n)\) for the
endpoint after those letters, and \(\#O(w)\) for the number of odd
letters.

The identities in this section are formalized in Lean
(`follows_iff_word`, `image_eq_iterate`, `image_append`,
`image_monotone_of_follows`, `power_bound_word`,
`power_bound_contracts`, `global_defect_identity`,
`global_defect_eq_zero_iff_localsTight`, `global_defect_append`,
`global_defect_eq_zero_implies_monochrome`,
`power_bound_eq_iff_extremal`, `image_eq_start_defectRatio`,
`one_plus_eta_lt_succ_sq`). The proofs below are the ordinary
integer arguments.

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
make every local remainder zero. This is the extremal classification
`power_bound_eq_iff_extremal`. \(\square\)

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
exactly (`image_eq_start_defectRatio`). A cycle burns its entire
formal surplus in floor losses.

*Proof.* Theorem 2.4 with \(m=n\). Nonnegativity of \(\Delta_w(n)\)
makes the difference a genuine one. \(\square\)

The identity does not supply a state-independent positive tax, and
none exists: the single-step slack is provably squeezed by the scale
of the state. For one realized letter at \(x\) with branch exponent
\(e\in\{1,3\}\),
\[
x^{e}<(J(x)+1)^2
\]
(`one_plus_eta_lt_succ_sq`), so the relative slack
\(1+\eta=x^{e}/J(x)^2\) satisfies
\[
\eta<\frac{2}{J(x)}+\frac{1}{J(x)^2},
\]
which tends to \(0\) as the state grows. A uniform per-step tax is
therefore impossible. The recorded extreme is an \(OOE\) block at
\(n=180370579261640036336071806107777\approx1.80\cdot10^{32}\) whose
relative slack satisfies \(0<q<10^{-30}\); this is an exact-integer
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
An odd fiber contains at most one integer (`odd_cell_unique`). Indeed,
suppose \(a<b\) lie in the same odd cell indexed by \(m\). Then
\((a+1)^3\le b^3<(m+1)^2\) and \(m^2\le a^3\). Subtracting the latter
lower bound from the former upper bound gives
\[
3a^2+3a+1=(a+1)^3-a^3<(m+1)^2-m^2=2m+1,
\]
and hence \(3a^2\le2m\). If \(a=0\), then \(m=0\) and the displayed
strict inequality is already impossible. If \(a>0\), squaring and using
\(m^2\le a^3\) gives \(9a^4\le4m^2\le4a^3\), contradicting
\(4a^3<9a^4\). An even fiber is a parity-restricted square interval and
may contain many predecessors.

A nonempty realized word \(w\) with \(J^{|w|}(n)=n\) is a cycle word.

The identities in this section are formalized in Lean
(`cycle_word_formally_expanding`, `cycleMin_not_end_odd`,
`square_scale_superquadratic`, `cycleMin_to_even_superquadratic`,
`no_cycle_word_oooeoe`, `no_cycle_word_ooooee`,
`no_cycle_word_length_le_six` with components
`no_cycle_word_replicate_odd`, `cycleWord_rotateWord`,
`cycleWord_exists_even_terminating`,
`no_cycle_word_length_four_ends_even`,
`no_cycle_word_length_five_ends_even`, `no_cycle_word_ooe`,
`no_cycle_odd_run_append_even`, `no_cycle_word_ooeooe`). The proofs
below are the ordinary integer arguments.

**Theorem 3.1 (cycle restrictions).**
Let \(w\) be a cycle word at \(n\ge2\).

(i) The word is formally expanding:
\[
2^{|w|}<3^{\#O(w)}
\]
(`cycle_word_formally_expanding`). A contracting word cannot close a
nontrivial cycle.

(ii) The cycle minimum is odd and the cycle maximum is even. A
minimum-based orientation cannot end in an odd letter
(`cycleMin_not_end_odd`).

(iii) A realized word \(v\) is *superquadratic* if
\[
3^{\#O(v)}\ge 2^{|v|+1}.
\]
Any realized path from a start \(n\ge2\) to a state at least \(n^2\)
is superquadratic (`square_scale_superquadratic`). On a cycle minimum
the path to any later even state is superquadratic
(`cycleMin_to_even_superquadratic`). The prefix \(OOE\) is expanding
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

These restrictions assemble into a complete census of short cycles.
Rotation reduces any cycle word to an even-terminating orientation,
the expanding filter of Theorem 3.1(i) and threshold arguments
eliminate every even-terminating word of length at most six except
\(OOOEOE\) and \(OOOOEE\), and those two survivors require an
individual argument, which uses the last-even cell together with a
coarse lower envelope. That argument is Lemma 3.2; the census is
Theorem 3.3. No exclusion of cycles of length seven or more is
claimed.

For \(n\ge1\),
\[
n<4\,\lfloor\sqrt n\rfloor^2,
\]
so an even step satisfies \(n\le 4\,J(n)^2\) and an odd step satisfies
\(n^3\le 4\,J(n)^2\). Composing along a realized word \(v\) of length \(k\) with odd count
\(o\) gives
\[
n^{3^{o}}\le D_v\,J^{k}(n)^{2^{k}}.
\]
The denominator starts at \(1\) and updates by
\(D\mapsto D\cdot 4^{2^{j}}\) on an even letter and
\(D\mapsto D^{3}\cdot 4^{2^{j}}\) on an odd letter, at step \(j\).
In particular \(D_{OOO}=2^{38}\) and \(D_{OOOO}=2^{130}\). If a cycle word ends
in an even letter, the last-even cell is
\(J^{|w|-1}(n)<(n+1)^2\).

**Lemma 3.2 (two length-six exclusions).**
Neither \(OOOEOE\) nor \(OOOOEE\) is a cycle word at any \(n\ge2\).

*Proof.* First, if \(n\ge256\), then
\[
n^{81}>2^{130}(n+1)^{64}.
\]
Indeed \(257^{64}<2\cdot256^{64}\) and \(256(n+1)\le257\,n\), so
\((n+1)^{64}<2n^{64}\). Then
\(2^{130}(n+1)^{64}<2^{131}n^{64}\). Since \(n\ge256=2^8\), one has
\(n^{17}\ge2^{136}\), and therefore
\(2^{131}n^{64}<2^{136}n^{64}\le n^{81}\).

For \(n<256\), neither word returns to its start. Lean checks both
itinerary-and-return tables by `native_decide` on `Fin 256`; the same
mechanism also verifies the finite numerical inequality
\(257^{64}<2\cdot256^{64}\) used at the cutoff.

Now suppose \(n\ge256\) realizes \(OOOOEE\), and write
\(z=J^4(n)\) for the image after the prefix \(OOOO\). The last two
even letters give \(J(z)<(n+1)^2\) and \(z<(J(z)+1)^2\), hence
\(z<(n+1)^4\). The lower envelope on \(OOOO\) is
\(n^{81}\le2^{130}z^{16}\), so
\(n^{81}<2^{130}(n+1)^{64}\), contradicting the tail inequality.

Finally suppose \(n\ge256\) realizes \(OOOEOE\). Write
\(z_3=J^3(n)\) and \(y=J(z_3)=\lfloor\sqrt{z_3}\rfloor\), so
\(z_3<(y+1)^2\). The lower envelope on \(OOO\) is
\(n^{27}\le2^{38}z_3^8<2^{38}(y+1)^{16}\). Cubing yields
\(n^{81}<2^{114}(y+1)^{48}\). The last letters \(OE\) give the odd-cell
bound \(y^3<(n+1)^4\). Write \(A=n+1\ge257\). Then
\((y+1)^3<2A^4\): if \(y\le A\), this follows from
\((A+1)^3<2A^4\); if \(y>A\), then \(y\ge4\) and
\((y+1)^3=y^3+3y^2+3y+1<A^4+4y^2\), while \(4y^2<A^4\) because
\(4y^3<4A^4\le yA^4\). Raising \((y+1)^3<2A^4\) to the sixteenth
power gives \((y+1)^{48}<2^{16}(n+1)^{64}\). Combining with the cubed
lower envelope produces again \(n^{81}<2^{130}(n+1)^{64}\). \(\square\)

**Theorem 3.3 (small-cycle census).**
No word of length at most six is a cycle word at any \(n\ge2\)
(`no_cycle_word_length_le_six`). Equivalently, a nontrivial Juggler
cycle, if one exists, has period at least seven.

*Proof.* Rotating a cycle word by one letter moves the base point one
step along the orbit and yields another cycle word
(`cycleWord_rotateWord`); every state of the cycle is at least \(2\),
because an orbit that reaches \(1\) stays at \(1\) and cannot return to
a start \(n\ge2\).

If every letter is odd, the start is odd, hence \(n\ge3\), and the odd
branch strictly increases there: \(J(x)>x\) for odd \(x\ge3\), since
\(x^3\ge(x+1)^2\). The orbit ascends strictly and never returns
(`no_cycle_word_replicate_odd`). Otherwise some letter is even, and a
rotation ending just after that letter produces an even-terminating
cycle word \(vE\) of the same length based at a cycle state \(m\ge2\)
(`cycleWord_exists_even_terminating`). It therefore suffices to exclude
even-terminating cycle words of length at most six.

By Theorem 3.1(i) a cycle word is formally expanding. No
even-terminating word of length one or two is expanding (\(2<3^0\) and
\(4<3\) both fail). For length three the only expanding candidate is
\(OOE\): for \(m\ge5\) the next-square threshold after \(OO\) gives
\(J^2(m)\ge(m+1)^2\), contradicting the last-even cell
\(J^2(m)<(m+1)^2\); the only smaller odd start is \(m=3\), where
\(J^2(3)=11\) is odd while the final even letter requires an even
state. For length four the expanding filter leaves only \(O^3E\), and
for length five only \(O^4E\); the threshold inherits along appended
odd letters, and the same last-even contradiction applies
(`no_cycle_word_length_four_ends_even`,
`no_cycle_word_length_five_ends_even`).

For length six the filter requires at least four odd letters among the
first five, leaving \(O^5E\), \(EOOOOE\), \(OEOOOE\), \(OOEOOE\),
\(OOOEOE\), and \(OOOOEE\). The odd-run threshold excludes \(O^5E\)
(`no_cycle_odd_run_append_even`). For \(OOEOOE\), a minimum-based
orientation meets the same next-square threshold at the internal even
letter after the prefix \(OO\), with starts below \(5\) checked
directly (`no_cycle_word_ooeooe`).
\(EOOOOE\) rotates one step onto \(OOOOEE\), and \(OEOOOE\) rotates two
steps onto \(OOOEOE\). The two remaining words are excluded by
Lemma 3.2. \(\square\)

The census stops at length six because length seven admits
even-terminating expanding words with two internal even letters that
none of the recorded thresholds reach; no exclusion at length seven is
claimed.

## 4. Short descent certificates

A start \(n\ge2\) has a *descent certificate* if there exists a realized
finite word \(w\) with \(J^{|w|}(n)<n\), or with image \(1\). Lean
packages this predicate as `FiniteProgress`, an abbreviation of
`DescentCertificate`. The four constructors of that type are proof forms
of the same predicate, not four different claims. The predicate is
existential over all finite words, not only over words of length one or
two.

The theorems in this section are formalized in Lean
(`even_finiteProgress`, `odd_even_finiteProgress`,
`unresolved_is_odd_odd`, `reachesOne_of_all_finiteProgress`,
`reachesOne_of_lt_twelve`, `even_lt_sq_twelve_reachesOne`). The proofs
below are the ordinary integer arguments. Proposition 4.4 is the exact
census of Section 1.1, not a Lean theorem.

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

**Theorem 4.2 (unresolved starts are odd-to-odd).**
If \(n\ge2\) has no descent certificate, then \(n\) is odd and \(J(n)\)
is odd.

*Proof.* Contrapositive of Theorem 4.1: an even start and an
odd-to-even start each carry a short certificate. \(\square\)

The converse is false: many odd-to-odd starts descend after a longer
word.

If every start above \(1\) has some descent certificate, ordinary strong
induction yields arrival at \(1\) (`reachesOne_of_all_finiteProgress`).
The hypothesis is not proved. A certificate at \(n\) only reduces the
problem to a strictly smaller positive integer, which may itself be
odd-to-odd.

Lean also certifies a finite landing class:

**Theorem 4.3 (small residuals).**
Every \(y\in\{1,\ldots,11\}\) reaches \(1\). Consequently every even
residual strictly below \(144=12^2\) reaches \(1\).

*Proof.* The orbits are finite and merge quickly:
\(2\to1\), \(4\to2\), \(6\to2\), \(8\to2\),
\(3\to5\to11\to36\to6\), \(7\to18\to4\),
\(9\to27\to140\to11\), and \(10\to3\). Each chain ends on a start
already settled, so every \(y\le11\) reaches \(1\). For the second claim, an even
\(y<144\) has \(J(y)=\lfloor\sqrt y\rfloor\le11\), which lands in the
verified set. (Lean evaluates the same finite orbits in
`reachesOne_of_lt_twelve` and `even_lt_sq_twelve_reachesOne`.)
\(\square\)

This enlarges the set of fatal landings for a hypothetical minimal
counterexample.

On the complementary odd-to-odd class, first return below the start is
frequent at a short horizon, but not automatic.

**Proposition 4.4 (odd-to-odd first-return census).**
For starts \(2\le n\le N\) and horizon \(20\), write \(\mathrm{OO}\) for
the odd-to-odd starts in that range. The exact census is:

| \(N\) | \(\#\mathrm{OO}\) | OO first return \(\le20\) | all starts, first return \(\le20\) |
|------:|------------------:|--------------------------:|-----------------------------------:|
| \(10^3\) | \(252\) | \(221/252\) (\(0.877\)) | \(968/999\) (\(0.969\)) |
| \(10^4\) | \(2504\) | \(2220/2504\) (\(0.887\)) | \(9715/9999\) (\(0.972\)) |
| \(10^5\) | \(24984\) | \(22379/24984\) (\(0.896\)) | \(97394/99999\) (\(0.974\)) |
| \(10^6\) | \(249926\) | \(223683/249926\) (\(0.895\)) | \(973756/999999\) (\(0.974\)) |

At \(N=10^6\), \(26{,}243\) odd-to-odd starts have no return below the
start in \(20\) steps. These rows use exact Python integer arithmetic with
no size cutoff through step \(20\); the unresolved count is zero in every
row. They are not Lean-certified and do not constitute an almost-all
theorem.

## 5. The remaining gap

Theorem 4.1 covers every even start and every odd-to-even start with a
uniform one- or two-step certificate, and Theorem 4.2 says the
unresolved starts are exactly the odd-to-odd class. The first
odd-to-odd image expands, so ordinary strong induction cannot fire on
the complement. Proposition 4.4 shows that most odd-to-odd starts in a
finite window still return below the start inside twenty steps; that
is an observation, not a theorem about an infinite set.

The gap resists the obvious finite-state attacks, and the failures are
exact computations on named witnesses, not estimates. Lean certifies a
chain of four consecutive expanding persistent residual blocks,
\[
1999\to5169\to50093\to193753\to887471
\]
(`four_block_pe_1999`), so no uniform run bound of four or less exists
for expanding blocks. Around such hard paths, five natural finite-state
reductions fail on exact-integer counterexamples: a uniform slack tax
per expanding block fails at the \(OOE\) block near \(1.80\cdot10^{32}\)
with relative slack below \(10^{-30}\) (Section 2); a compact state
built from the normalized landing position \(\theta\) fails because
\(\theta\) fills essentially all of \([0,1]\) on continuations and
predicts the next parity no better than a residue class; recognition
modulo \(2^m\) fails because every residue class modulo \(64\) both
continues and exits the iterated odd-landing sets; a \(2\)-adic
restriction from persistent-expanding history fails because the
endpoint \(763\) has \(v_2\bigl(y^3-J(y)^2\bigr)=1\); and the expanding
word grammar is not an independent obstruction because, on \(n\ge2\),
persistence already implies expansion, so that attack reduces to the
tautology \(J^{|w|}(n)>n\).

The analytic route — parity discrepancy for the nested floor powers,
counting itinerary word classes, and the densities of
certified-descent classes — is the subject of the companion
manuscript [7]. It imports from this note only the contraction
criterion of Corollary 2.3, and this note claims none of its results.

> No theorem forces every exact integer state into a contracting
> prefix. In particular, it is open whether almost every odd-to-odd
> start has a finite descent certificate, and open whether every
> start reaches \(1\).

## 6. Software archive

Lean proofs of the theorems of Sections 2--4 live at
[https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).
The archive is not required to read the arguments above. From a clone,
the review object is

```text
cd formal && lake build Problems.JugglerPaper
```

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
   2026.
