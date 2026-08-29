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

As a secondary application, every even start and every odd start whose first
image is even has a uniform one- or two-step descent certificate. A classical
discrepancy estimate
\[
\bigl|S_O(N)\bigr|\ll N^{5/6},\qquad
S_O(N)=\sum_{\substack{n\le N\\n\ {\rm odd}}}
(-1)^{\lfloor n^{3/2}\rfloor},
\]
implies that this uniform short-certificate class has density \(3/4\).
An exact-linearization calculus for the nested floor powers extends the
discrepancy method down the orbit: **every** itinerary word class of
depth at most four has cardinality \(2^{-|w|}N+O(N^{1-\delta_w})\) with
explicit exponents. The last and hardest case, the \(OOO*\) split, rests
on a kernel theorem proved here: the exponential sum of the level-2
floor defect against smooth weights of scale \(n^{9/8}\) exhibits a
power saving, obtained by double Weyl differencing over an exact
carry-branch decomposition. The same engine counts the contracting
words of lengths five and seven, so the class of starts carrying a
uniform descent certificate of length at most four, five, seven has
natural density \(13/16\), \(7/8\), \(57/64\) respectively. An
unconditional counting argument shows that parity equidistribution at
all depths would give the set of starts with some finite descent
certificate density one; the base cases of depth at most four are now
unconditional. The remaining obstacle is the level-3 kernel — the same
sum one nesting deeper, where the weight scale \(n^{27/16}\) exceeds
\(n\) — stated here as an open problem together with a proved
almost-every-shift form and a precise record of what blocks the
deterministic case. None of these densities is a density of starts
that reach \(1\).

All finite-word statements are conditional on the realized itinerary. The
remaining pointwise question is whether almost every odd-to-odd start has
some finite descent; no such theorem is proved here.

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
finite-word comparison, the compositional slack, the uniform short
certificates, and the densities of the classes those certificates cover:
all of itinerary depth four, and the contracting words of lengths five
and seven.

The main contribution is the exact power-envelope and defect calculus,
together with its inverse-cell and cycle consequences, chief among
them a small-cycle census: no nontrivial cycle has length at most six.
The certified-descent densities — \(3/4\) at two steps, \(13/16\) at
four, \(7/8\) at five, \(57/64\) at seven — are secondary corollaries.
We do not prove a Collatz theorem or transfer Collatz stopping-time
results to \(J\).

### 1.1 Verification convention

Theorems in Sections 2--4 are proved both below and in Lean under the names
listed at the start of each section. The analytic estimates of Sections 5
and 6 (Theorems 5.1, 5.4, 5.7, 5.8, 5.11, 5.13--5.15, 6.4,
Propositions 5.5, 6.1, Corollaries 5.12 and 5.16) are ordinary human
proofs and are not formalized; the exact floor reductions beneath them
— the parity bridge \(\lfloor x\rfloor\) odd iff \(\{x/2\}\ge1/2\), the
gap-cell identity, and the double-gap identity used by the kernel
theorem — are Lean-verified (`floor_odd_iff_half_le_fract_half`,
`floor_gap_eq_carry`, `seq_floor_gap`, `seq_floor_gap_second` in
`GapCells.lean`). The exact-linearization lemmas of
Sections 5 and 6 are additionally validated by scaled-integer computations
recorded in the repository; those validations are checks, not proofs.
Proposition 4.4 is an exact Python-integer census,
not a theorem about an infinite set. The four-block chain named in
Section 6 is Lean-certified (`four_block_pe_1999`); the failed
reductions there are exact-integer counterexamples, not estimates. No
finite computation is used as a termination proof.

### 1.2 Related maps

The nearest published comparison is the Collatz problem. Lagarias [3,4]
surveys parity words and almost-all statements short of totality. Terras [5]
and Everett [6] proved that almost every positive integer has a finite
Collatz stopping time; Tao [7] later showed that almost all Collatz orbits
attain almost bounded values. Those results are methodological cousins, not
theorems about \(J\). The Juggler analogue of Terras would be an almost-all
descent theorem on the odd-to-odd class.

Crandall [8] and Matthews–Watts [9] treat piecewise-affine Hasse–Syracuse
maps; the Juggler branches are floor powers, not affine. Prasad and Prasad
[12] estimate excursion and stopping constants for juggler-like random
walks; Section 6 keeps that comparison descriptive.

The discrepancy calculus of Section 5 concerns nested floor powers
\(\lfloor\lfloor n^{c}\rfloor^{d}\rfloor\). A literature check (August
2026) found no equidistribution result for such nested sequences: the
Piatetski–Shapiro corpus covers single floors, intersections, and
pseudo-polynomials. The tools themselves are classical — Vaaler's
trigonometric approximation to the sawtooth [13] and van der Corput's
second-derivative test in the form presented by Graham and Kolesnik
[14].

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

## 5. Parity discrepancy and certified-descent densities

This section counts itinerary word classes. It proves the ambient
depth-1 estimate (Theorem 5.1) with its density-\(3/4\) corollary, then
extends the method through itinerary depth four by exact linearization
of the nested floor powers: depth 2 and 3 completely (Theorem 5.4,
Proposition 5.5), depth 4 except the \(OOO*\) split (Theorems 5.7 and
5.8), giving the certified-descent density \(13/16\) (Corollary 5.9);
then the \(OOO*\) split itself through a kernel theorem for the level-2
floor defect (Theorems 5.11 and 5.13), completing depth 4; and finally
the contracting words of lengths five and seven (Theorems 5.14 and
5.15), raising the certified density to \(7/8\) and \(57/64\)
(Corollary 5.16). All estimates here are human proofs; the exact floor
reductions beneath them are Lean-verified (Section 1.1).

For odd \(n\) write \(s(n)=(-1)^{\lfloor n^{3/2}\rfloor}\) and
\[
S_O(N)=\sum_{\substack{n\le N\\n\ {\rm odd}}}s(n).
\]
Let \(M(N)\) be the number of odd integers \(n\le N\), and let
\[
\operatorname{OO}(N)=\#\{n\le N:\ n\ \mathrm{odd},\ J(n)\ \mathrm{odd}\}.
\]
Then \(s(n)=-1\) if and only if \(J(n)\) is odd, and
\[
S_O(N)=M(N)-2\operatorname{OO}(N).
\]
Also \(M(N)=N/2+O(1)\).

The floor sign has an exact fractional-part form. Write
\(x=\lfloor x\rfloor+\{x\}\). If \(\lfloor x\rfloor\) is even then
\(\{x/2\}<1/2\); if \(\lfloor x\rfloor\) is odd then
\(\{x/2\}\ge1/2\). Thus
\[
\lfloor x\rfloor\ \text{is odd}
\quad\Longleftrightarrow\quad
\{x/2\}\ge\tfrac12
\]
(Lean: `floor_odd_iff_half_le_fract_half`).
For odd \(n=2r+1\) set
\[
g(r)=\frac{(2r+1)^{3/2}}2.
\]
Then \(s(n)=-1\) if and only if \(\{g(r)\}\ge1/2\). For \(R\) points
\(x_0,\ldots,x_{R-1}\) and an interval \(I\subset[0,1)\), define the
unnormalized interval discrepancy
\[
\mathcal D_R(I)=\#\{0\le r<R:\{x_r\}\in I\}-R|I|.
\]
Taking \(R=M(N)\), the odd integers at most \(N\) are exactly
\(2r+1\) for \(0\le r<R\), and therefore
\(S_O(N)=-2\mathcal D_R([1/2,1))\) for \(x_r=g(r)\).

The following two lemmas are classical. The derivative estimate is the
\(k=2\) case of Iwaniec--Kowalski [11, Thm. 8.20, Sec. 8.3,
pp. 204--213]. The discrepancy inequality is
Kuipers--Niederreiter [10, Ch. 2, Sec. 2, Thm. 2.5, pp. 112--115].

**Lemma 5.A (van der Corput, second-derivative form).**
Let \(f\) be twice differentiable on an interval of length \(M\), with
\(\lambda\le|f''|\le\alpha\lambda\) for some \(\alpha\ge1\). Then
\[
\Bigl|\sum e(f)\Bigr|\ll_\alpha M\lambda^{1/2}+\lambda^{-1/2},
\]
where the sum runs over the integers in the interval and
\(e(t)=e^{2\pi it}\).

**Lemma 5.B (Erdős–Turán).**
The discrepancy of \(R\) points \(x_j\in\mathbb R/\mathbb Z\) against an
interval satisfies
\[
D
\ll
\frac{R}{H}+\sum_{h=1}^H\frac1h\Bigl|\sum_{j=1}^R e(hx_j)\Bigr|
\]
for every cutoff \(H\ge1\).

**Theorem 5.1 (ambient odd-input discrepancy).**
\[
|S_O(N)|\ll N^{5/6}.
\]
This argument is not packaged in Lean.

*Proof.* The second derivative is
\[
g''(r)=\tfrac32(2r+1)^{-1/2}.
\]
It is positive and decreasing. Separate the initial term \(r=0\), then
partition \(1\le r<R\) into blocks
\([M,\min(2M,R))\), where \(M\) runs over powers of \(2\). On such a
block \(g''(r)\asymp M^{-1/2}\). For the \(h\)-th Fourier mode take
\(f=hg\), so \(\lambda\asymp hM^{-1/2}\). Lemma 5.A gives
\[
\Bigl|\sum_{r\asymp M}e(hg(r))\Bigr|
\ll h^{1/2}M^{3/4}+h^{-1/2}M^{1/4}.
\]
Lemma 5.B, with \(R\asymp M\), bounds that block's contribution to
\(S_O(N)\) by
\[
\frac{M}{H}+M^{3/4}H^{1/2}+M^{1/4}.
\]
Here the middle term is
\(\sum_{h\le H}h^{-1}\cdot h^{1/2}M^{3/4}\ll M^{3/4}H^{1/2}\), and the
last term is
\(\sum_{h\le H}h^{-1}\cdot h^{-1/2}M^{1/4}\ll M^{1/4}\).
For bounded \(M\), the trivial estimate is absorbed into the constant.
Otherwise choose \(H=\lfloor M^{1/6}\rfloor\), which balances the first
two terms at \(M^{5/6}\). The initial term contributes \(O(1)\), and the
geometric sum of the block bounds is
\(\sum_{M\le R}O(M^{5/6})=O(R^{5/6})=O(N^{5/6})\).
The floor sign is not replaced by a single exponential; the exponential
sums are those of the sequence \(\{g(r)\}\). \(\square\)

**Corollary 5.2 (short-certificate class).**
The odd-to-odd starts have natural density \(1/4\):
\[
\bigl|\operatorname{OO}(N)-N/4\bigr|\ll N^{5/6}.
\]
Equivalently, the starts that admit the uniform one- or two-step
certificates of Theorem 4.1 — every even start together with every
odd-to-even start — have natural density \(3/4\).

This is a density of the uniform short-certificate class of Theorem 4.1,
not of all descent certificates and not of starts that reach \(1\).

The exact census through \(N=10^7\) has
\(\operatorname{OO}(N)/N=0.2499896\). Through \(N=10^6\) one has
\(S_O(N)=146\) and running maximum \(256\), at \(n=985351\). A spot
computation at \(10^7\) has running maximum \(459\). The observed growth
is much smaller than \(N^{5/6}\): the recorded maxima at \(10^6\) and
\(10^7\) sit near the scale \(N^{1/3}\). That empirical scale is an
observation, not a theorem.

Theorem 5.1 concerns consecutive source intervals. It supplies no transfer
theorem for orbit samples or sparse image sets, so it cannot by itself
control the odd-to-odd dynamics after the first step. The remainder of
this section does not transfer Theorem 5.1 to image sets; it attacks the
nested sums directly, by removing the inner floors exactly before any
analytic step.

For the rest of the section, \(n\) is odd, \(X=n^{3/2}\),
\(m=\lfloor X\rfloor=\operatorname{isqrt}(n^3)\), and
\(\theta=X-m\in[0,1)\). At the second level, \(Y=m^{3/2}\),
\(v=\lfloor Y\rfloor\), \(\theta_2=Y-v\); on the \(OE\) branch (\(m\)
even), \(U=m^{1/2}\), \(w=\lfloor U\rfloor=J^2(n)\), and
\(\theta_w=U-w\). Write \(\psi(x)=(-1)^{\lfloor x\rfloor}\). The first
image parity of an odd start is \((-1)^m=\psi(n^{3/2})\); the next
letters are the parities of \(v\) (after an odd image) or \(w\) (after
an even image). Each \(\psi\)-factor below is evaluated
unconditionally; the indicator algebra of the corollaries only ever
weights it on the branch where it computes the true itinerary letter,
and these branch-consistency identities are machine-checked exactly on
verification windows.

**Lemma 5.3 (exact linearization and gap cells).**
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

**Theorem 5.4 (nested parity discrepancy).**
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
cylinder refines one letter deeper than Theorem 5.1.

*Proof.* Work on dyadic blocks \(n\in(P,2P]\), odd, with truncations
\(J_1=J_2=P^{1/24}\) (wave modes), \(H=P^{1/12}\) (differencing), and
\(R=P^{1/4}\) (cell modes).

*Step 1 (wave expansion).* By Vaaler's theorem [13] applied to the
period-2 square wave, \(\psi(x)=V_J(x/2)+O(\Delta_J(x/2))\), where
\(V_J(t)=\sum_{0<|q|\le J}a_qe(qt)\) with \(|a_q|\le\min(1,2/|q|)\) and
\(\Delta_J\ge0\) is a trigonometric polynomial of degree \(J\) with
constant term and coefficients \(O(1/J)\). For the product,
\(|\psi_1\psi_2-V_1V_2|\le\Delta_1+\Delta_2+\Delta_1\Delta_2\), and
each error term is again a nonnegative trigonometric polynomial of the
same shape. Expanding both factors reduces the theorem to bounds,
uniform in the mode pair, for
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

*Step 2 (linearization).* By Lemma 5.3(i), replacing
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
Lemma 5.3(ii). On a cell, \(g=G+\kappa\) with \(G\) constant and
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
ratio across a cell; van der Corput II [14] on a cell of length
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
slack. The observed cancellation is far stronger (envelope exponent
\(\approx0.28\) in exact censuses), which the proof does not claim.

**Proposition 5.5 (OE-branch third letter).**
For \(a\in\{0,1\}\),
\[
\Bigl|\sum_{n\le N,\ n\ \mathrm{odd}}\bigl((-1)^m\bigr)^a\,
\psi\bigl(m^{1/2}\bigr)\Bigr|\ll_\varepsilon N^{7/8+\varepsilon},
\]
and consequently
\(\#\mathrm{OEO}(N),\ \#\mathrm{OEE}(N)=N/8+O(N^{7/8+\varepsilon})\).
Together with Theorem 5.4 this makes depth 3 complete: each of
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
single-signed and van der Corput II gives
\(\ll i^{1/2}P^{3/4}+i^{-1/2}P^{1/4}\); for \(i=0\),
\(\varphi''\asymp lP^{-5/4}\) gives
\(\ll l^{1/2}P^{3/8}+l^{-1/2}P^{5/8}\). Vaaler majorants, truncation
tails, and dyadic assembly are as in Theorem 5.4, and every bound is
\(\ll P^{7/8}\) after summing mode weights. Branch consistency: the
\((1+(-1)^m)/2\) factor vanishes exactly on odd \(m\), where \(J^2\)
takes the \(3/2\)-power branch, so the unconditional
\(\psi(m^{1/2})\) is only weighted where it computes the true third
letter. \(\square\)

**Lemma 5.6 (fourth-letter linearization).**
For every odd \(n\ge3\),
\[
v^{1/2}=n^{9/8}+D(n),
\qquad
-\tfrac34\,n^{-3/8}-n^{-9/8}\le D(n)\le0 .
\]

*Proof.* Two applications of the Lemma 5.3(i) pattern. With
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

**Theorem 5.7 (triple parity discrepancy).**
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

*Proof.* The \(c=0\) cases are Theorem 5.4 and Theorem 5.1. For
\(c=1\), wave-expand all present sign factors as in Step 1 of
Theorem 5.4, with truncations \(J_1=J_2=J_3=P^{1/24}\), and bound
\[
S_{i,j,k}(P)=\sum_{n\in(P,2P],\ n\ \mathrm{odd}}
e\bigl(\tfrac i2n^{3/2}+\tfrac j2m^{3/2}+\tfrac k2v^{1/2}\bigr)
\]
uniformly for \(|i|\le2J_1\), \(|j|\le2J_2\), \(1\le|k|\le2J_3\). By
Lemma 5.6, replacing \(\tfrac k2v^{1/2}\) by \(\tfrac k2n^{9/8}\)
costs \(\ll|k|P^{5/8}\le P^{2/3}\), before any differencing.

If \(j=0\), the remaining sum is a single smooth exponential sum with
phase \(\tfrac i2n^{3/2}+\tfrac k2n^{9/8}\). Both curvature terms are
positive for positive modes, and for mixed signs with \(|i|\ge1\) the
first dominates by \(P^{3/8-1/24}\); van der Corput II gives
\(\ll P^{5/8}\) for \(i=0\) and \(\ll|i|^{1/2}P^{3/4}+P^{1/4}\)
otherwise, both \(\ll P^{23/24}\).

If \(j\ne0\), the phase is exactly the Theorem 5.4 phase plus the
smooth passenger \(\tfrac k2n^{9/8}\). Steps 2–6 run verbatim; the
passenger modifies the smooth part of the differenced phase by
\(\tfrac k2[(n{+}2h)^{9/8}-n^{9/8}]\), whose second derivative
\(\ll|k|hP^{-15/8}\) is smaller than the retained cell curvature
\(jhP^{-3/4}\) and the \(r\)-mode curvature \(|r|P^{-1/2}\) by powers
of \(P\). Every sign-dominance check of Theorem 5.4 holds with these
margins. \(\square\)

**Theorem 5.8 (the OE\*\* splits).**
\[
\#\mathrm{OEOE}(N),\ \#\mathrm{OEOO}(N)
=\tfrac N{16}+O\bigl(N^{7/8+\varepsilon}\bigr),
\qquad
\#\mathrm{OEEE}(N),\ \#\mathrm{OEEO}(N)
=\tfrac N{16}+O\bigl(N^{13/16+\varepsilon}\bigr).
\]
Together with Theorems 5.4 and 5.7 this proves every depth-4
itinerary word class except \(OOO*\).

*Proof.* On the \(OE\) branch \(m\) is even and \(w=\lfloor
U\rfloor\), \(U=m^{1/2}\). The \(w\)-level linearization is Lemma
5.3(i) verbatim with base \(U\): since \(Um^{1/4}=m^{3/4}\) exactly,
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
For \(i\ne0\) the last term dominates and van der Corput II gives
\(\ll i^{1/2}P^{3/4}+i^{-1/2}kP^{5/8}\) after summing intervals. For
\(i=0\), \((T+J_2)P^{-5/4}\ll kP^{-7/8}\) because
\(T=P^{5/16}\ll kP^{3/8}\) for every \(k\ge1\), so
\(\lambda\asymp kn^{-7/8}\) is single-signed; van der Corput II per
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

**Corollary 5.9 (depth-4 census and certified-descent density).**
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

*Proof.* For \(OOEE\), the indicator algebra gives
\(\#OOEE=\tfrac18\sum_{n\le N\ \mathrm{odd}}
(1-\psi_1)(1+\psi_2)(1+\psi_3)\) with
\(\psi_1=\psi(n^{3/2})\), \(\psi_2=\psi(m^{3/2})\),
\(\psi_3=\psi(v^{1/2})\); expanding gives the main term and seven
sign sums bounded by Theorem 5.7. The factor \((1+\psi_2)\) vanishes
precisely where \(J^3\) would take the odd branch, so the
unconditional \(\psi_3\) is only weighted where it computes the true
fourth letter. Every \(OOEE\) start descends within four steps by the
power envelope: \(3^2<2^4\), so Corollary 2.3 applies. The even class
and the \(OE\) class carry the certificates of Theorem 4.1, and the
three classes are disjoint. The remaining depth-\(\le4\) prefixes are
Theorem 5.1 (depth 1), Theorem 5.4 and Proposition 5.5 (depths 2–3),
and Theorems 5.7–5.8 (depth 4). \(\square\)

The density \(13/16\) is the exact ceiling of this one-growing-layer
machinery: a word contracts iff \(3^{o}<2^{\ell}\), the method so far
proves letters at positions 1–3 of any word plus further letters along
even branches only, and the contracting minimal words with all odd
letters at positions \(\le2\) are exactly \(E\), \(OE\), and \(OOEE\),
of total density \(\tfrac12+\tfrac14+\tfrac1{16}=\tfrac{13}{16}\). Any
further certified density requires the \(OOO*\) split — a second
growing layer, where the fourth-letter phase coefficient
\(W\asymp kn^{9/8}\) crosses integers within single steps and no
drift-1 interval exists. The rest of this section closes that split
and harvests the contracting words it unlocks.

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

**Lemma 5.10 (level-2 defect, double gap, and branch freeze).**
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
the moving-endpoint pattern of Step 4 of Theorem 5.4.

*Proof.* (i) Taylor of \((v+\theta_2)^{3/2}\) at \(v\), with
\(Y^{3/2}=m^{9/4}\). (ii) The gap identity of Lemma 5.3(ii) applied
twice — to \(Y\) at shift \(d_1\), then to the real sequence
\(n\mapsto W(n)\) at shift \(d_2\), with \(\Delta_2W=\Delta\Delta Y\);
the sawtooth form of the carry is the Lean-verified floor-carry
identity rearranged. (iii) The corner identities are Lemma 5.3(ii) at
the three shifts. The offset bound follows from
\(|\Delta\Delta X|\le4h_1h_2\sup|X''|=3h_1h_2P^{-1/2}\). The
derivative bound is the mean value theorem on the second difference
of \(\tfrac32m^{1/2}\) plus \(\tfrac34j(m+\xi)^{-1/2}\). \(\square\)

One warning, recorded as negative knowledge: \(\lfloor\Delta\Delta
Y\rfloor\) itself is *not* frozen. The level-1 carry toggles at
essentially every step and shifts \(\Delta\Delta Y\) by
\(\tfrac32j_1m^{1/2}\); in exact windows its mean run length is
\(1.5\) with jumps of size \(\tfrac32P^{3/4}\). The branch
organization of (iii), which carries the flicker inside the
indicator, is forced.

**Theorem 5.11 (kernel cancellation).**
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
\(\Delta\Delta c\asymp kh_1h_2P^{-7/8}\).

*Step 3 (the \(Y\)-block).* Split into the \(O((h_1{+}h_2)P^{1/2})\)
cell intersections of Lemma 5.3(ii); within a cell every shifted
\(Y\)-value is a smooth function of the single variable
\(m=X-\theta\), so no \(\Delta\theta\) cross-terms arise. The
\((\Delta\Delta c)Y\) and \((\Delta_ic)\Delta_jY\) pieces have smooth
curvature \(\asymp kh_1h_2P^{-5/8}\) and \(\theta\)-coefficients
\(\asymp kh_1h_2P^{-1/8}<1\) under the constraint (C1)
\(kh_1h_2\le P^{1/8}\); sub-unit sawtooths are expanded in Fourier
modes of \(\theta\) at multiplicative mode-mass \(O(\log P)\). The
\(c_{11}\Delta\Delta Y\) piece splits over the branches of
Lemma 5.10(iii): per branch the smooth part
\(c\,F_{\boldsymbol\kappa}(X)\) has curvature
\(\asymp k|j|P^{-1/8}+kh_1h_2P^{-5/8}<1\), and the \(\theta\)-content
\(cF'\theta\) has coefficient \(\asymp k|j|P^{3/8}\) with window
drift \((cF')'\asymp k|j|P^{-5/8}<1\); a shifted-window expansion
produces \(X\)-modes of size \(s\asymp k|j|P^{3/8}\) with curvature
\(sX''\asymp k|j|P^{-1/8}<1\), handled by van der Corput II.

*Step 4 (the \(v\)-block).* \(v\) is an integer, so no fractional
part of \(c\) is ever split off. The \((\Delta\Delta c)v\) piece
reduces to Step 3 plus a \(\theta_2\)-coefficient
\(\asymp kh_1h_2P^{-7/8}<1\). The \((\Delta_2c)\Delta_1v\) piece is
\(\Delta_2c\,(W-\{W\})\) plus a carry: \(\Delta_2c\cdot W\) is smooth
per cell; the sawtooth \(-\Delta_2c\,\{W\}\) has window drift
\((\Delta_2c)'\asymp kh_2P^{-7/8}<1\) and expands into \(W\)-modes
\(r\lesssim kh_2P^{1/8}\), each again smooth per cell; the carry
weight \(\kappa_2=\{Y\}+\{W\}-\{Y{+}W\}\) (Lemma 5.10(ii)) expands
into unit sawtooths of \(Y\)- and \(W\)-forms with Vaaler windows
\(|r|\le R=P^{\rho}\) at majorant cost \(P/R\) per layer; the
\(Y\)-modes linearize (Lemma 5.3(i) pattern) to \(X\)-modes
\(s\asymp RP^{3/4}\) of curvature \(sX''\asymp RP^{1/4}\gg1\) —
pieces without a frozen-floor factor take the third-derivative test
over full ranges (\(\lambda_3=sX'''\asymp RP^{-3/4}<1\), saving
\(P^{1/8}/R^{1/6}\)); pieces riding a frozen floor are the mixed
class of Step 5. The main piece
\(c_{11}\Delta\Delta v=c_{11}\Delta_2g_2\) is Lemma 5.10(ii): per
branch the frozen integer
\(J_F=\lfloor F_{\boldsymbol\kappa}(X(n))\rfloor\) combines with the
\(c_{11}\Delta\Delta Y\)-content into the smooth per-run phase
\(c(F_{\boldsymbol\kappa}-J_F)\), of curvature
\(\asymp k|j|P^{-1/8}+kh_1h_2P^{-5/8}\), single-signed per branch;
the carries \(\kappa''\) and \(\Delta_2\kappa_2\) are indicator
weights times \(e(\mp c)\).

*Step 5 (dominance and mode assembly).* The final pieces fall into
four classes. (i) *Pure smooth pieces*: van der Corput II per frozen
run; the leading curvature per branch is a double difference of one
smooth function, so the double mean value theorem gives a single
sign — for the monomial family the composite check is
\(\alpha(\alpha{-}1)(\alpha{+}\beta{-}2)(\alpha{+}\beta{-}3)>0\) at
\(\alpha=\tfrac98\), \(\beta\in\{\tfrac14,\tfrac34\}\), with
composite exponents \(\tfrac{15}8,\tfrac{11}8\notin\{0,1,2\}\).
Per-run application is legitimate because
\(\lambda_2^{-1/2}\asymp P^{1/16}\ll P^{1/4}\asymp\) run length;
saving \(\ge P^{1/16}/(k|j|)^{1/2}\). (ii) *Slow-mode pieces*: van
der Corput II over full ranges; dominance is clean because the
colliding curvature scale \(s^*\asymp kP^{3/8}\) lies outside every
mode window. (iii) *Mixed pieces* — a frozen-floor factor times a
large \(X\)-mode \(s\asymp rP^{3/4}\): van der Corput II fails there
(\(\lambda_2\gg1\)) and the per-run third-derivative test returns
only the trivial bound. The repair is one *targeted third Weyl
differencing* (shift \(2h_3\), \(h_3\le H_3\)) followed by the split
\(J_F=F-\{F\}\): the differenced coefficient
\(\Delta_3c\asymp kh_3P^{1/8}\) has window drift \(<1\) against the
*slow* sawtooth \(\{F(X)\}\) (drift \(\asymp P^{-1/4}\)), so the
shifted-window expansion applies with no run segmentation;
\(\Delta_3\lfloor F\rfloor\) is bounded with slow indicators; and
the differenced mode curvature
\(s(\Delta_3X)''\asymp rh_3P^{-3/4}<1\) is single-signed and
dominant. Van der Corput II over full ranges and the balance
\(H_3=r^{-1/3}P^{1/4}\) recover the class-(iv) saving. (iv)
*Carry-mode pieces without a frozen floor*: the third-derivative
test over full ranges, \(\lambda_3\asymp rP^{-3/4}\), saving
\(P^{1/8}/r^{1/6}\).

*Step 6 (assembly).* Sub-unit sawtooths cost multiplicative
mode-mass \(O(\log P)\) only; mode masses multiply over at most four
expansion layers plus the targeted differencing:
\(P^{\varepsilon}\). With \(R=P^{1/16}\), the savings
\(P^{1/16}/(k|j|)^{1/2}\) and \(P^{1/8-1/96}\) and the truncation
\(P^{-1/16}\) balance at \(|T_2|\ll P^{1-1/16+\varepsilon}\) under
(C1) and \(h_1h_2\le P^{1/2}/3\). Unwinding the two differencings:
with \(k\le P^{\kappa_0}\) and \(a+b\le\tfrac18-\kappa_0\),
\(|K_c|\ll P(P^{-a/2}+P^{-b/4}+P^{-1/64})\). For
\(\kappa_0=\varepsilon\): \(a=\tfrac1{32}\), \(b=\tfrac1{16}\),
\(\delta=\tfrac1{64}\). For \(\kappa_0=\tfrac1{24}\):
\(a=\tfrac1{36}\), \(b=\tfrac1{18}\), \(\delta=\tfrac1{72}\).
Exponents deliberately unoptimized. \(\square\)

The proof was re-derived adversarially step by step; exact-phase
probes at the first, second, and third differenced levels show
square-root cancellation throughout (repository), far stronger than
the bound claims.

**Corollary 5.12 (low-exponent families).**
The bound of Theorem 5.11 holds for every monomial-pattern family
\(c^{(r)}\asymp kP^{\alpha-r}\) with \(0<\alpha\le\tfrac98\),
uniformly for \(k\le P^{1/24}\).

*Proof.* Every constraint in the proof is monotone in \(\alpha\) on
\((0,\tfrac98]\): (C1) relaxes to \(kh_1h_2\le P^{5/4-\alpha}\);
every curvature and window drift shrinks; the sign-dominance product
\(\alpha(\alpha{-}1)(\alpha{+}\beta{-}2)(\alpha{+}\beta{-}3)>0\)
holds at \(\beta\in\{\tfrac14,\tfrac34\}\) throughout the interval;
the assembly exponents only improve. \(\square\)

**Theorem 5.13 (the OOO\* splits; depth four complete).**
For \(w\in\{OOOE,OOOO\}\),
\[
\#\{n\le N\ \text{odd}:\ \mathrm{word}_4(n)=w\}
=\tfrac N{16}+O\bigl(N^{1-1/72+\varepsilon}\bigr).
\]
Hence **every** itinerary word class of depth at most four satisfies
\(\#\{n\le N\}=2^{-|w|}N+O(N^{1-\delta_w})\) with explicit
\(\delta_w>0\): depth-4 parity equidistribution is complete.

*Proof.* The class indicator expands (Vaaler, truncation
\(J_3=P^{1/24}\), error \(P/J_3\)) into mode sums
\(S_{ijk}=\sum_ne(\tfrac i2X+\tfrac j2Y+\tfrac k2v^{3/2})\) over
dyadic blocks. Three applications of the Taylor pattern of
Lemma 5.3(i), taken to second order, give the exact identity (odd
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
the family of Theorem 5.11; the \(vm\)- and \(vm^2\)-cross terms
reduce to the same family by \(\xi vm=\xi X\,v-\xi\theta\,v\) and
\(\xi_2vm^2=\xi_2X^2\,v-2\xi_2X\theta\,v+\xi_2\theta^2v\), whose
\(\theta\)-cross coefficients are sub-unit and whose smooth
\(v\)-coefficients \(\xi X,\xi_2X^2\asymp kP^{9/8}\) are family
members. Writing \(v=Y-\theta_2\) splits each family term into a
smooth-in-\(m\) part and a kernel factor \(e(-c\,\theta_2)\). The
double differencing of Theorem 5.11 applied to the whole mode phase
carries the passengers along: the pure-\(m\) polynomial phases
difference into the Step-3 classes; the \(\tfrac i2X\)- and
\(\tfrac j2Y\)-passengers difference to curvatures
\(\ll ih_1h_2P^{-5/2}\) and \(\asymp jP^{-5/4}\), subdominant in the
established hierarchy; the kernel factor is handled by Steps 2–5
verbatim. Assembly and summation over \(k\le J_3\) with
\(1/k\)-weights give
\(\sum_k\tfrac1kP^{1-1/72}+P^{1-1/24}\ll P^{1-1/72+\varepsilon}\);
dyadic blocks sum to \(N^{1-1/72+\varepsilon}\). \(\square\)

The certified-descent density stays \(13/16\) at four steps —
\(OOO*\) is non-contracting at depth 4 (\(3^3>2^4\)) — but the
kernel theorem opens the contracting words at depths five and
seven.

**Theorem 5.14 (the length-5 contracting splits).**
\[
\#\mathrm{OOOEE}(N),\ \#\mathrm{OOOEO}(N)
=\tfrac N{32}+O\bigl(N^{1-1/72+\varepsilon}\bigr),
\qquad
\#\mathrm{OOEOE}(N),\ \#\mathrm{OOEOO}(N)
=\tfrac N{32}+O\bigl(N^{43/48+\varepsilon}\bigr).
\]

*Proof.* *OOOE\(*\).* The class indicator is the Theorem-5.13
indicator times \(\tfrac12(1\pm\psi(z^{1/2}))\), \(z=J^3(n)\):
branch-consistent because on the OOOE cylinder \(z\) is even, so the
fifth letter is the even-branch value. Vaaler-expand the fifth wave
at truncation \(P^{1/24}\). The Lemma 5.3(i) pattern along the chain
replaces \(\tfrac l2z^{1/2}\) by
\(\tfrac l2n^{27/16}-\tfrac{9l}{16}n^{3/16}\theta\) at absorbable
decaying cost. The \(\theta\)-sawtooth has coefficient
\(\asymp lP^{3/16}<P\); its shifted-window expansion (drift-1 length
\(P^{13/16}/l\), window \(T=P^{1/8}\ll lP^{3/16}\)) produces
\(X\)-modes of size \(\asymp lP^{3/16}\) — ordinary first-letter
passengers within Theorem 5.13's budget — and the smooth chirp
\(e(\tfrac l2n^{27/16})\) has curvature \(\asymp lP^{-5/16}\),
subdominant to every retained scale. Theorem 5.13 applies verbatim.

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
(1+o(1))\asymp kn^{-5/16}\), single-signed since
\(-0.290k+0.211k\ne0\). Van der Corput II on each interval gives
\(\ll k^{-1/2}P^{9/32}\); over \(\asymp kP^{9/16}\) intervals,
\(S_k\ll k^{1/2}P^{27/32+\varepsilon}\). Balancing
\(J_5^{1/2}P^{27/32}=P/J_5\) at \(J_5=P^{5/48}\) gives
\(P^{43/48}\); dyadic blocks sum to \(N^{43/48+\varepsilon}\).
\(\square\)

**Theorem 5.15 (the length-7 engine splits).**
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
content is a chirp of curvature \(\asymp n^{17/32}\) (van der
Corput II); the leading \(\theta_2\)-content has coefficient
\(\asymp n^{33/32}\) — a family of Corollary 5.12 at
\(\alpha=\tfrac{33}{32}<\tfrac98\); the remaining
\(\theta_2\)-amplitudes are \(O(n^{9/32})\), inside the engine. The
integer block \(e(\xi w)\) with \(\xi\asymp n^{45/32}\) is handled
on frozen gap runs: on the OOEO cylinder \(U=v^{1/2}\) has
\(U''\asymp P^{-7/8}<1\), so \(\lfloor\Delta U\rfloor\) is constant
on runs of length \(\asymp P^{7/8}/h\), and per run
\(\Delta w=J_U+\kappa_w\) with \(J_U\) frozen, \(e(\xi J_U)\) a
smooth chirp, and \(\kappa_w\) an indicator weight — the
Lemma 5.10(iii) pattern one level up. The sawtooth \(\theta_p\)
expands on drift-1 intervals of length \(P^{5/32}\) with window
\(T\ll P^{27/32}\), producing \(X\)-modes within Theorem 5.14's
budget. The seventh letter is the even-branch square root of
\(q=\lfloor p^{3/2}\rfloor\), with decaying amplitudes only.
Theorem 5.14 applies as a passenger theorem.

*OOOEO\(**\).* The analogous rearrangement at base \(z^{1/2}\)
(\(s=\lfloor z^{1/2}\rfloor\):
\(s^{3/2}=-\tfrac12z^{3/4}+\tfrac32s\,z^{1/4}+E\)) plus the
\(z^{3/4}\to n^{81/32}\) linearization chain gives the same four
classes of terms — chirp, Corollary-5.12 family at
\(\alpha=\tfrac{33}{32}\), engine sawtooths, and an integer-\(s\)
block on \(\lfloor\Delta z^{1/2}\rfloor\)-runs of length
\(\asymp P^{5/16}\). Same exponent. \(\square\)

**Corollary 5.16 (certified-descent densities \(7/8\) and \(57/64\)).**
The class of starts carrying a uniform power-envelope descent
certificate of length at most five — evens, \(OE\), \(OOEE\),
\(OOOEE\), \(OOEOE\) — has natural density \(7/8\); adding the
length-7 words \(OOEOOEE\) and \(OOOEOEE\) raises the density of the
length-\(\le7\) certified class to \(57/64\).

*Proof.* Densities
\(\tfrac12+\tfrac14+\tfrac1{16}+\tfrac1{32}+\tfrac1{32}=\tfrac78\)
and \(\tfrac78+\tfrac1{128}+\tfrac1{128}=\tfrac{57}{64}\). The
cylinders are disjoint, and each new cylinder is counted with a
power saving by Theorems 5.14 and 5.15. Contraction is
Corollary 2.3: \(3^3=27<32=2^5\) on the length-5 words and
\(3^4=81<128=2^7\) on the length-7 words. \(\square\)

The leftover \(\tfrac7{64}\) is the \(OOOO*\) tree (uncounted)
together with the expanding siblings of the counted words. Every
uncounted contracting word now passes through \(OOOO*\), whose
fifth letter carries the level-3 kernel isolated in Section 6; the
first such contractor is \(OOOOEEE\).

As with Corollary 5.2, these are densities of uniform
certificate classes. They are not densities of all descent
certificates and not densities of starts that reach \(1\).

## 6. The remaining gap

Theorem 4.1 and Corollary 5.2 say that a uniform one- or two-step
argument covers a set of density \(3/4\); Corollaries 5.9 and 5.16
raise the uniformly certified class to \(13/16\) at four steps,
\(7/8\) at five, and \(57/64\) at seven. The first odd-to-odd image
expands, so ordinary strong induction cannot fire on the complement.
Proposition 4.4 shows that most odd-to-odd starts in a finite window
still return below the start inside twenty steps. That is an
observation, not Terras's theorem for \(J\).

The depth-by-depth counting of Section 5 does assemble into a
conditional Terras-style statement, and the reduction is unconditional:

**Proposition 6.1 (equidistribution implies density-one descent).**
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
Corollary 2.3. Consequently, if \(E_d(N)=O_d(N^{1-\delta_d})\) with
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
bounds. Section 5 now proves it *unconditionally at every depth
\(d\le4\)* (Theorems 5.4–5.13), so the base cases of Proposition 6.1
are theorems. The first open case is depth 5: the \(OOOO*\) split.
It has an exact shape, one nesting deeper than Theorem 5.11. Write
\(Z=v^{3/2}\), \(z=\lfloor Z\rfloor\), \(\theta_3=Z-z\); after four
odd letters the fifth is the parity of \(\lfloor z^{3/2}\rfloor\).

**Lemma 6.2 (level-3 kernel reformulation).**
For odd \(n\ge5\),
\[
\tfrac12\bigl(v^{9/4}-z^{3/2}\bigr)-\tfrac34\,z^{1/2}\theta_3=R_3,
\qquad
0\le R_3\le\tfrac3{16}\,z^{-1/2}.
\]
Consequently the fifth-letter phase is, up to \(kR_3\ll kn^{-27/16}\)
per term, the exponential sum of the level-3 local floor defect, with
coefficient \(c=\tfrac{3k}4z^{1/2}\asymp kn^{27/16}\): Lemma 5.10(i)
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

**Conjecture 6.3 (level-3 kernel cancellation).**
\(K_3(P)\ll P^{1-\delta}\) for some \(\delta>0\), uniformly over the
family above with \(k\le P^{\varepsilon}\). Exact-phase probes show
square-root cancellation (\(|K_3|\approx30.1,\ 59.5,\ 423.7\) on
\(2.5\cdot10^3,\ 2.5\cdot10^4,\ 10^5\) terms), but no proof is
claimed.

The boundary between Theorem 5.11 and Conjecture 6.3 is quantitative
and sharper than a derivative count. The smooth model iterates: where
Theorem 5.11 used two Weyl differencings against
\(Y''\asymp P^{1/4}\gg1>P^{-3/4}\asymp Y'''\), the level-3 model
\(n^{27/8}\) has \(G'''\asymp P^{3/8}\gg1>P^{-5/8}\asymp G^{(4)}\)
and predicts three. But the prediction does not descend to the nested
floors. The kernel weight now has \(c'\asymp kP^{11/16}\gg1\), so no
drift-1 interval exists for any expansion of the weight itself; the
branch decomposition of Lemma 5.10(iii) has no analogue at the
\(v\)-level, because \(v\) jumps by \(\asymp n^{5/4}\) per step and
the branch set is a *product* of two carry lattices, not a copy of
one; and the forced inner linearization
\(v^{3/2}=m^{9/4}-\tfrac32m^{3/4}\theta_2+E_2\) trades \(\theta_3\)
for a sawtooth family at coefficient scale \(kn^{45/16}\), *above*
the \(9/4\) threshold where every method of this paper stops. Three
routes — a scale-invariant copy of Theorem 5.11, differencing the
increment first, and absorbing the leftover into a freezing integer
— fail at exactly characterized points; the failures are recorded in
the repository as exact statements, not anecdotes.

What survives at the frontier is a model problem and one theorem
about it. Stripping every Juggler-specific structure (carries,
defects, nesting) from \(K_3\) leaves the *amplitude-product* sums
\[
S=\sum_{t\le L}e\bigl(A(t)\,\{B(t)\}\bigr),
\qquad
1\ll A'\ll A,
\]
with smooth monomial-type \(A,B\) (the Juggler instance has
\(A\asymp P^{27/16}\), \(A'\asymp P^{11/16}\)). For \(A'\ll1\)
partial summation makes the amplitude a tame passenger and the
classical Piatetski–Shapiro machinery applies; for \(A'\gg1\) we
know of no nontrivial deterministic bound by any method. The generic
statement, however, is a theorem — and its proof uses no harmonic
analysis at all:

**Theorem 6.4 (shift-averaged square-root cancellation).**
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
per step — is exactly what makes the shift average trivial. The
theorem also forces the empirical profile: censuses of
\(R=|S|^2/L\) for the Juggler instance at \(P=10^6\)–\(10^{10}\)
show a textbook \(\mathrm{Exp}(1)\) distribution, now explained
rather than merely observed. What remains of Conjecture 6.3 after
Theorem 6.4 is a de-randomization: the deterministic sum is the
single shift \(\lambda=0\) in a family that cancels almost surely.

**Conjecture 6.5 (the pure amplitude-product model).**
\(|S|\le L^{1-\delta}\) for some \(\delta>0\), for smooth
monomial-type \(A,B\) with \(1\ll A'\ll A\) as above.

Three structural facts locate the difficulty of the
de-randomization, each a short rigorous argument recorded in the
repository. No second averaging variable exists: amplitude
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
\(1/A_{\max}\) (\(\asymp P^{-27/16}\) in the instance, confirmed by
measurement), and an almost-all-\(\lambda\) theorem leaves
\(\asymp\varepsilon A_{\max}\) exceptional cells among
\(\asymp A_{\max}\) — no measure argument pins \(\lambda=0\). The
deterministic content of Conjecture 6.5 is a
specific-point-in-metric-theory problem, the same species as the
normality of \(\sqrt2\): a class whose known successes all use
special arithmetic. The instance does carry arithmetic the model
forgets — \(A^2=\tfrac9{16}k^2z\) with \(z\) integer, coupled to the
argument through \(\theta_3=v^{3/2}-z\) — but its natural
exploitations (a pure-phase identity, quadratic-field periodicity)
re-enter the harmonic toolkit and fail at the recorded points.

A mixed-parity heuristic, ignoring floors, gives mean log-log drift
\(\tfrac12\log(3/4)<0\). Finite ensembles sit near this value; hard
paths are more odd-rich. This agrees qualitatively with the
juggler-like random-walk model of Prasad and Prasad [12]. Fair parity
is an assumption, not a dynamical theorem, and typical negative drift
is not pointwise contraction.

The gap also resists the obvious finite-state attacks, and the
failures are recorded, not anecdotal. Lean certifies a chain of four
consecutive expanding persistent residual blocks,
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
tautology \(J^{|w|}(n)>n\). Each failed reduction is an exact
computation on named witnesses.

The analytic routes around Conjecture 6.3 fail at recorded points as
well. Composing gap cells across two levels fails: on a cell where
the first-level gap is constant, the second-level gap takes a new
value at essentially every point (distinct-value ratio \(1.0000\) in
exact windows), so no usable sub-cell survives. Reindexing by the
image \(m\) (each \(m\) has at most one odd preimage) strips one
nesting level but introduces a fiber indicator of density
\(\asymp m^{-1/3}\), whose sawtooth produces mode sums that must beat
the sparsity exponent \(1/3\) while the engine saves only \(1/24\);
already the first mode is fatal. At level 3, every character
expansion of the kernel product has its Fourier window centred at
the amplitude \(kc(t)\), which drifts by \(kc'\asymp kP^{11/16}\)
harmonics per step, so inner sums at fixed harmonic are shorter than
one step at every block length; and every algebraic re-form —
floor-splitting, the pure-phase identity, differencing at any order,
interval-splitting — transfers the \(P^{27/16}\) amplitude instead
of destroying it. All routes are parked as negative knowledge, not
retried.

The gap is therefore:

> No theorem forces every exact integer state into a contracting
> prefix. In particular, it is open whether almost every odd-to-odd
> start has a finite descent certificate. By Proposition 6.1 that
> would follow from all-depth parity equidistribution, which is now
> a theorem through depth four; the first open case is the
> \(OOOO*\) kernel of Conjecture 6.3, whose model form cancels for
> almost every shift (Theorem 6.4) and whose deterministic instance
> is Conjecture 6.5.

![The theorem flow of the note. Exact finite-word identities yield contraction, rigidity, and cycle restrictions; the discrepancy calculus with the kernel theorem counts every itinerary class through depth four and the contracting words of lengths five and seven (certified density 57/64), leaving the level-3 kernel — generically cancelling by the shift-average theorem — and with it almost-all descent, open.](figures/juggler_frontier.png){width=100%}

That is the Juggler form of the Terras question. A sharper ambient
discrepancy exponent does not answer it; by Proposition 6.1 the
question now rests on equidistribution at growing depth, beginning
with Conjecture 6.3.

## 7. Software archive

Lean proofs of the exact-arithmetic theorems live at
[https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).
The archive is not required to read the arguments above. The analytic
estimates of Sections 5 and 6 are human proofs; Lean certifies only
the exact floor reductions beneath them (`GapCells.lean`, including
the double-gap identity `seq_floor_gap_second` used by Theorem 5.11)
and the exact-arithmetic theorems of Sections 2–4. The scaled-integer
validators for the linearization lemmas, the kernel probes, and the
shift-average and pure-model censuses live in
`src/research/juggler_sequence/two_step_parity.py` with pinned tests.

From a clone, the review object is

```text
cd formal && lake build Problems.JugglerPaper
```

## Acknowledgments

I used large language models extensively while drafting and revising the
text, organizing companion notes, and as an interactive assistant for
Lean statements, tests, and literature records. The models are not
authors. Lean theorems and named computations are the certificates for
those claims. The discrepancy estimates of Sections 5 and 6,
including the kernel theorem, and Proposition 6.1 are human proofs
using classical analytic inequalities; they are not Lean-certified.
I take full responsibility for the contents.

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
5. R. Terras, “A stopping time problem on the positive integers,”
   *Acta Arith.* 30 (1976), 241–252.
   [doi:10.4064/aa-30-3-241-252](https://doi.org/10.4064/aa-30-3-241-252).
6. C. J. Everett, “Iteration of the number-theoretic function
   \(f(2n)=n\), \(f(2n+1)=3n+2\),” *Adv. Math.* 25 (1977), 42–45.
   [doi:10.1016/0001-8708(77)90087-1](https://doi.org/10.1016/0001-8708(77)90087-1).
7. T. Tao, “Almost all orbits of the Collatz map attain almost bounded
   values,” *Forum Math. Pi* 10 (2022), e12.
   [doi:10.1017/fmp.2022.8](https://doi.org/10.1017/fmp.2022.8).
8. R. E. Crandall, “On the ``\(3x+1\)'' problem,” *Math. Comp.* 32
   (1978), 1281–1292.
   [doi:10.1090/S0025-5718-1978-0480321-3](https://doi.org/10.1090/S0025-5718-1978-0480321-3).
9. K. R. Matthews and A. M. Watts, “A generalization of Hasse's
    generalization of the Syracuse algorithm,” *Acta Arith.* 43 (1984),
    167–175.
    [doi:10.4064/aa-43-2-167-175](https://doi.org/10.4064/aa-43-2-167-175).
10. L. Kuipers and H. Niederreiter, *Uniform Distribution of Sequences*,
    Wiley-Interscience, New York, 1974.
11. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, American
    Mathematical Society Colloquium Publications 53, Providence, RI, 2004.
12. V. Prasad and M. A. Prasad, “Estimates of the maximum excursion
    constant and stopping constant of juggler-like sequences,”
    ResearchGate preprint, 2025.
    [doi:10.13140/RG.2.2.14110.04168](https://doi.org/10.13140/RG.2.2.14110.04168).
13. J. D. Vaaler, “Some extremal functions in Fourier analysis,”
    *Bull. Amer. Math. Soc. (N.S.)* 12 (1985), 183–216.
    [doi:10.1090/S0273-0979-1985-15349-2](https://doi.org/10.1090/S0273-0979-1985-15349-2).
14. S. W. Graham and G. Kolesnik, *Van der Corput's Method of
    Exponential Sums*, London Mathematical Society Lecture Note
    Series 126, Cambridge University Press, Cambridge, 1991.
