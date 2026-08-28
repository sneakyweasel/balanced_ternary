---
title: Power envelopes, exact defects, and cycle restrictions for the Juggler map
author: Philippe Cochin
date: 28 August 2026
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
discrepancy method one level down the orbit: every itinerary word class
of depth at most four except \(OOO*\) has cardinality
\(2^{-|w|}N+O(N^{1-\delta_w})\) with explicit exponents, and consequently
the class of starts carrying a uniform descent certificate of length at
most four has natural density \(13/16\). An unconditional counting
argument shows that parity equidistribution at all depths would give the
set of starts with some finite descent certificate density one; the
precise remaining obstacle at depth four is an explicit exponential-sum
kernel, stated here as an open problem. None of these densities is a
density of starts that reach \(1\).

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
certificates, and the densities of the classes those certificates cover,
through itinerary depth four.

The main contribution is the exact power-envelope and defect calculus,
together with its inverse-cell and cycle consequences, chief among
them a small-cycle census: no nontrivial cycle has length at most six.
The certified-descent densities — \(3/4\) at two steps, \(13/16\) at
four — are secondary corollaries. We do not prove a Collatz theorem or
transfer Collatz stopping-time results to \(J\).

### 1.1 Verification convention

Theorems in Sections 2--4 are proved both below and in Lean under the names
listed at the start of each section. The analytic estimates of Section 5
(Theorems 5.1, 5.4, 5.7, 5.8, Proposition 5.5) and Proposition 6.1 are
ordinary human proofs and are not formalized; the exact floor reductions
beneath them — the parity bridge \(\lfloor x\rfloor\) odd iff
\(\{x/2\}\ge1/2\), and the gap-cell identity — are Lean-verified
(`floor_odd_iff_half_le_fract_half`, `floor_gap_eq_carry`,
`seq_floor_gap` in `GapCells.lean`). The exact-linearization lemmas of
Section 5 are additionally validated by scaled-integer computations
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
Proposition 5.5), and depth 4 completely except the \(OOO*\) split
(Theorems 5.7 and 5.8), giving the certified-descent density \(13/16\)
(Corollary 5.9). All estimates here are human proofs; the exact floor
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

The density \(13/16\) is the exact ceiling of this machinery: a word
contracts iff \(3^{o}<2^{\ell}\), the method proves letters at
positions 1–3 of any word plus further letters along even branches
only, and the contracting minimal words with all odd letters at
positions \(\le2\) are exactly \(E\), \(OE\), and \(OOEE\), of total
density \(\tfrac12+\tfrac14+\tfrac1{16}=\tfrac{13}{16}\). Any further
certified density requires the \(OOO*\) split — a second growing
layer — whose precise obstruction is isolated in Section 6.

As with Corollary 5.2, these are densities of uniform
certificate classes. They are not densities of all descent
certificates and not densities of starts that reach \(1\).

## 6. The remaining gap

Theorem 4.1 and Corollary 5.2 say that a uniform one- or two-step
argument covers a set of density \(3/4\); Corollary 5.9 raises the
uniformly certified class to density \(13/16\) at four steps. The
first odd-to-odd image expands, so ordinary strong induction cannot
fire on the complement. Proposition 4.4 shows that most odd-to-odd
starts in a finite window still return below the start inside twenty
steps. That is an observation, not Terras's theorem for \(J\).

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
bounds — exactly what Section 5 proves through depth 4, except
\(OOO*\). The hypothesis beyond that is open, and its first open
case has an exact shape. Differencing the \(OOO*\) phase funnels, in
every reorganization tried, into one object: for smooth \(c\) with
\(c\asymp kP^{9/8}\) and \(c'\asymp kP^{1/8}\) on \(n\sim P\),
\[
K_c(P)=\sum_{\substack{n\sim P\\ n\ \mathrm{odd}}}
e\bigl(c(n)\,\{\lfloor n^{3/2}\rfloor^{3/2}\}\bigr).
\]

**Conjecture 6.2 (kernel cancellation).**
\(K_c(P)\ll P^{1-\delta}\) for some \(\delta>0\), uniformly over the
family above. Exact-phase probes show square-root cancellation
(\(|K|\approx51.9,\ 124.4,\ 1017.5\) on \(5\cdot10^3,\ 5\cdot10^4,\
5\cdot10^5\) terms), but no proof is claimed.

The boundary is quantitative: the Section 5 engine reaches every
itinerary letter whose phase coefficient grows slower than \(n\)
(the \(OE\!*\!*\) coefficient \(B\asymp kn^{3/8}\) crosses integers
every \(\asymp P^{5/8}/k\) steps, so drift-1 intervals exist), while
the \(OOO*\) coefficient \(W\asymp kn^{9/8}\) crosses integers within
single steps (\(W'\asymp kn^{1/8}\gg1\)) and no drift-1 interval
exists. Bounding \(K_c\) is the precise remaining obstacle to the
\(OOO*\) split, hence to any certified density beyond \(13/16\)
through this program. \(K_c\) is a bilinear correlation between the
fractional parts of one nested-floor layer and a smooth weight at the
scale of the next layer; we found no treatment of such an object in
the nested-floor literature.

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

Two analytic routes around Conjecture 6.2 also fail, and the failures
are recorded. Composing gap cells across two levels fails: on a cell
where the first-level gap is constant, the second-level gap takes a
new value at essentially every point (distinct-value ratio
\(1.0000\) in exact windows), so no usable sub-cell survives.
Reindexing by the image \(m\) (each \(m\) has at most one odd
preimage) strips one nesting level but introduces a fiber indicator
of density \(\asymp m^{-1/3}\), whose sawtooth produces mode sums
that must beat the sparsity exponent \(1/3\) while the engine saves
only \(1/24\); already the first mode is fatal. Both routes are
parked as negative knowledge, not retried.

The gap is therefore:

> No theorem forces every exact integer state into a contracting
> prefix. In particular, it is open whether almost every odd-to-odd
> start has a finite descent certificate. By Proposition 6.1 that
> would follow from all-depth parity equidistribution, whose first
> open case is the \(OOO*\) kernel of Conjecture 6.2.

![The theorem flow of the note. Exact finite-word identities yield contraction, rigidity, and cycle restrictions; the discrepancy calculus counts the uniform certificate classes through depth four (density 13/16) but leaves the OOO* kernel, and with it almost-all descent, open.](figures/juggler_frontier.png){width=100%}

That is the Juggler form of the Terras question. A sharper ambient
discrepancy exponent does not answer it; by Proposition 6.1 the
question now rests on equidistribution at growing depth, beginning
with Conjecture 6.2.

## 7. Software archive

Lean proofs of the exact-arithmetic theorems live at
[https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).
The archive is not required to read the arguments above. The analytic
estimates of Section 5 and Proposition 6.1 are human proofs; Lean
certifies only the exact floor reductions beneath them
(`GapCells.lean`) and the exact-arithmetic theorems of Sections 2–4.
The scaled-integer validators for the linearization lemmas live in
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
those claims. The discrepancy estimates of Section 5 and
Proposition 6.1 are human proofs using classical analytic
inequalities; they are not Lean-certified. I take full
responsibility for the contents.

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
