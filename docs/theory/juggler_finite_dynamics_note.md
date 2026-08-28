---
title: Finite-word contraction and short descent certificates for the Juggler map
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

For every finite parity word \(w\) realized at \(n\), the iterate satisfies
the power envelope
\[
J^{|w|}(n)^{2^{|w|}}\le n^{3^{\#O(w)}}.
\]
Hence \(3^{\#O(w)}<2^{|w|}\) forces \(J^{|w|}(n)<n\) whenever \(n\ge2\).
An exact global-defect identity records the floor slack in this comparison.
These statements are conditional on a realized word: they do not say that
every orbit meets a contracting word.

A start \(n\ge2\) has a *descent certificate* if some realized finite word
sends it strictly below \(n\). Every even start, and every odd start whose
first image is even, has a uniform one- or two-step certificate. A classical
discrepancy bound
\[
\bigl|S_O(N)\bigr|\ll N^{5/6},\qquad
S_O(N)=\sum_{\substack{n\le N\\n\ {\rm odd}}}
(-1)^{\lfloor n^{3/2}\rfloor},
\]
implies that the complementary odd-to-odd starts have density \(1/4\), so
the uniform short-certificate class has density \(3/4\). This is not a
density of all descent certificates, and it is not a density of starts that
reach \(1\). Odd-to-odd starts expand on the first step and may still
descend later. The bound itself is ambient: it does not transfer to sparse
Juggler-generated image sets.

The remaining question, analogue of Terras's almost-all stopping-time
theorem, is whether almost every odd-to-odd start has some finite descent.
No such theorem is proved here.

## 1. Introduction

The Juggler sequence was introduced by Pickover [1]; see also Weisstein
[2] and OEIS A007320 [3]. Universal arrival at \(1\) remains open. In this
repository every start \(n\le4000\) reaches \(1\), as an exact finite
computation. That check is not a proof.

The map combines a contracting even branch with an expanding odd branch,
\[
E(n)=\lfloor n^{1/2}\rfloor,\qquad
O(n)=\lfloor n^{3/2}\rfloor.
\]
A word of length \(k\) with \(o\) odd letters has ideal exponent
\(3^o/2^k\). Floors are applied after every letter, and a word is available
only when the orbit realizes those parities. The paper records the exact
finite-word comparison, the exact slack, the uniform short certificates,
and the density of the class those certificates cover.

The contribution is a short exact-arithmetic note, not a survey of failed
compressions and not a description of the computational atlas used in the
surrounding laboratory. We do not prove a Collatz theorem, and we do not
transfer Collatz stopping-time results to \(J\).

### 1.1 Evidence discipline

- **EXACT — LEAN VERIFIED:** a theorem checked by Lean in the software
  archive named in Section 7.
- **EXACT — HUMAN PROOF:** a mathematical argument not packaged in Lean.
  Theorem 5.1 is of this kind.
- **COMPUTATIONALLY VERIFIED:** an exact finite computation under stated
  bounds.
- **OBSERVATION:** a descriptive pattern in finite data.
- **REFUTED:** a universal candidate killed by a certificate.

A finite check is never called a termination proof.

### 1.2 Related maps

The nearest published comparison is the Collatz problem. Lagarias [4,5]
surveys parity words, stopping times, and almost-all statements that stop
short of totality. Terras [6] and Everett [7] proved that almost every
positive integer has a finite Collatz stopping time — some return below
the start — without proving that every orbit reaches \(1\). Tao [8] later
showed that almost all Collatz orbits attain almost bounded values.

Those results are cited as methodological cousins, not as theorems about
\(J\). The uniform short certificates below cover a set of density
\(3/4\) by a one- or two-step argument. Terras and Everett prove that
almost every Collatz start has *some* finite stopping time. Those are
different statements. The Juggler analogue of Terras would be an almost-all
descent theorem on the odd-to-odd class. It is not proved here.

Crandall [9] and Matthews–Watts [10] treat piecewise-affine
Hasse–Syracuse maps. Juggler is not piecewise affine: the branches are
floor powers. Prasad and Prasad [12] estimate excursion and stopping
constants for juggler-like random walks; Section 6 keeps that comparison
descriptive.

## 2. Finite words, envelope, and defect

Let \(\mathcal B=\{E,O\}\). A finite word \(w\in\mathcal B^*\) is
*realized* at \(n\in\mathbb N\) when the successive parities of the orbit
of \(n\) are exactly the letters of \(w\). Write \(J^{|w|}(n)\) for the
endpoint after those letters, and \(\#O(w)\) for the number of odd
letters.

The identities in this section are formalized in Lean
(`follows_iff_word`, `image_eq_iterate`, `image_append`,
`image_monotone_of_follows`, `power_bound_word`,
`power_bound_contracts`, `global_defect_identity`). The proofs below are
the ordinary integer arguments.

**Theorem 2.1 (fixed-word monotonicity; EXACT — LEAN VERIFIED).**
If \(n\le m\) and both realize \(w\), then
\(J^{|w|}(n)\le J^{|w|}(m)\).

The realizing set of a fixed word need not be an interval.

**Theorem 2.2 (finite-word power envelope; EXACT — LEAN VERIFIED).**
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

**Corollary 2.3 (exponent-gap contraction; EXACT — LEAN VERIFIED).**
If \(n\ge2\), \(w\) is realized at \(n\), and
\(3^{\#O(w)}<2^{|w|}\), then \(J^{|w|}(n)<n\).

*Proof.* Let \(m=J^{|w|}(n)\) and \(k=|w|\). Theorem 2.2 gives
\(m^{2^k}\le n^{3^{\#O(w)}}\). The exponent gap and \(n\ge2\) give
\(n^{3^{\#O(w)}}<n^{2^k}\), so \(m^{2^k}<n^{2^k}\). Since \(m\ge1\), one
has \(m<n\). \(\square\)

The corollary includes familiar contracting blocks such as \(OOOEE\). It
does not prove that every start realizes some contracting word.

The floor slack is exact. For a single branch,
\[
x^e=J(x)^2+\rho(x),\qquad
e=\begin{cases}1,&x\ {\rm even},\\3,&x\ {\rm odd},\end{cases}
\]
with \(0\le\rho(x)<2J(x)+1\). Lifting these remainders through a word
gives a nonnegative global defect \(\Delta_w(n)\).

**Theorem 2.4 (global defect identity; EXACT — LEAN VERIFIED).**
If \(w\) is realized at \(n\) and \(m=J^{|w|}(n)\), then
\[
n^{3^{\#O(w)}}=m^{2^{|w|}}+\Delta_w(n),\qquad\Delta_w(n)\ge0.
\]

The identity names the slack in Theorem 2.2. It does not supply a
state-independent positive tax: persistent expanding blocks can have
arbitrarily small observed normalized slack at large scale.

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
An odd fiber contains at most one integer
(`odd_cell_unique`; EXACT — LEAN VERIFIED). An even fiber is a
parity-restricted square interval and may contain many predecessors.

A nonempty realized word \(w\) with \(J^{|w|}(n)=n\) is a cycle word.

**Theorem 3.1 (cycle exponent condition; EXACT — LEAN VERIFIED).**
Every cycle word at \(n\ge2\) satisfies
\[
2^{|w|}<3^{\#O(w)}.
\]

Thus a contracting word cannot close a nontrivial cycle. The cycle
minimum is odd and the cycle maximum is even; these are necessary
restrictions. They do not exclude every nontrivial cycle. In particular
the length-six orientations \(OOOEOE\) and \(OOOOEE\) remain open.

## 4. Short descent certificates

A start \(n\ge2\) has a *descent certificate* if there exists a realized
finite word \(w\) with \(J^{|w|}(n)<n\), or with image \(1\). In the Lean
development this predicate is called `FiniteProgress`. It is existential
over all finite words, not only over words of length one or two.

**Theorem 4.1 (uniform short certificates; EXACT — LEAN VERIFIED).**
Let \(n\ge2\).

1. If \(n\) is even, then the one-letter word \(E\) is a descent
   certificate: \(J(n)=\lfloor\sqrt n\rfloor<n\).
2. If \(n\) is odd and \(J(n)\) is even, then the two-letter word \(OE\)
   is a descent certificate.

**Theorem 4.2 (unresolved starts are odd-to-odd; EXACT — LEAN VERIFIED).**
If \(n\ge2\) has no descent certificate, then \(n\) is odd and \(J(n)\)
is odd.

The converse is false. Theorem 4.2 does not say that odd-to-odd starts
lack descent certificates. Many of them descend after a longer word.

If every start above \(1\) has some descent certificate, ordinary strong
induction yields arrival at \(1\) (`reachesOne_of_all_finiteProgress`).
The hypothesis is not proved. A certificate at \(n\) only reduces the
problem to a strictly smaller positive integer, which may itself be
odd-to-odd.

Lean also certifies a finite landing class
(`reachesOne_of_lt_twelve`, `even_lt_sq_twelve_reachesOne`):

**Theorem 4.3 (small residuals; EXACT — LEAN VERIFIED).**
Every \(y\in\{1,\ldots,11\}\) reaches \(1\). Consequently every even
residual strictly below \(144=12^2\) reaches \(1\).

This enlarges the set of fatal landings for a hypothetical minimal
counterexample. It does not cover all odd-to-odd starts, and it does not
prove that every even start reaches \(1\).

Independently, an exact computation gives:

**Proposition 4.4 (window totality; COMPUTATIONALLY VERIFIED).**
Every start \(1\le n\le4000\) reaches \(1\).

This is a finite check, not a bound on all starts.

On the complementary odd-to-odd class, first return below the start is
frequent at a short horizon, but not automatic.

**Proposition 4.5 (odd-to-odd first return; OBSERVATION).**
For starts \(2\le n\le N\) and horizon \(20\), write \(\mathrm{OO}\) for
the odd-to-odd starts in that range. The exact census is:

| \(N\) | \(\#\mathrm{OO}\) | OO first return \(\le20\) | all starts, first return \(\le20\) |
|------:|------------------:|--------------------------:|-----------------------------------:|
| \(10^3\) | \(252\) | \(0.877\) | \(0.969\) |
| \(10^4\) | \(2504\) | \(0.887\) | \(0.972\) |
| \(10^5\) | \(24984\) | \(0.896\) | \(0.974\) |
| \(10^6\) | \(249926\) | \(0.895\) | \(0.974\) |

At \(N=10^6\), \(26{,}243\) odd-to-odd starts have no return below the
start in \(20\) steps. None of these rows is a Lean descent certificate,
and none is an almost-all theorem.

## 5. Ambient discrepancy and the short-certificate class

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
\{x/2\}\ge\tfrac12.
\]
For odd \(n=2r+1\) set
\[
g(r)=\frac{(2r+1)^{3/2}}2.
\]
Then \(s(n)=-1\) if and only if \(\{g(r)\}\ge1/2\), and \(S_O(N)\) is
twice the interval discrepancy of the sequence \(\{g(r)\}\) against
\([1/2,1)\).

The following two lemmas are classical; see Kuipers–Niederreiter [11,
Ch. 1–2].

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

**Theorem 5.1 (ambient odd-input discrepancy; EXACT — HUMAN PROOF).**
\[
|S_O(N)|\ll N^{5/6}.
\]
This argument is not packaged in Lean.

*Proof.* The second derivative is
\[
g''(r)=\tfrac32(2r+1)^{-1/2}.
\]
It is positive and decreasing. On a dyadic block \(r\asymp M\) one has
\(g''(r)\asymp M^{-1/2}\). For the \(h\)-th Fourier mode take
\(f=hg\), so \(\lambda\asymp hM^{-1/2}\). Lemma 5.A gives
\[
\Bigl|\sum_{r\asymp M}e(hg(r))\Bigr|
\ll h^{1/2}M^{3/4}+h^{-1/2}M^{1/4}.
\]
Lemma 5.B, with \(R\asymp M\) and the relation between \(S_O\) and
interval discrepancy, yields
\[
|S_O|\ll
\frac{M}{H}+M^{3/4}H^{1/2}+M^{1/4}
\]
on that block: the middle term is
\(\sum_{h\le H}h^{-1}\cdot h^{1/2}M^{3/4}\ll M^{3/4}H^{1/2}\), and the
last term is
\(\sum_{h\le H}h^{-1}\cdot h^{-1/2}M^{1/4}\ll M^{1/4}\).
The choice \(H\asymp M^{1/6}\) balances the first two terms at
\(M^{5/6}\). Summing dyadic blocks up to \(N\) preserves the exponent.
The floor sign is not replaced by a single exponential; the exponential
sums are those of the sequence \(\{g(r)\}\). \(\square\)

**Corollary 5.2 (short-certificate class; EXACT — HUMAN PROOF).**
The odd-to-odd starts have natural density \(1/4\):
\[
\bigl|\operatorname{OO}(N)-N/4\bigr|\ll N^{5/6}.
\]
Equivalently, the starts that admit the uniform one- or two-step
certificates of Theorem 4.1 — every even start together with every
odd-to-even start — have natural density \(3/4\).

This is a counting corollary of Theorem 5.1, not a Lean cardinality
theorem. It is a density of a *uniform short-certificate class*. It is
not the density of all starts that possess some descent certificate, and
it is not a density of starts that reach \(1\).

The exact census through \(N=10^7\) has
\(\operatorname{OO}(N)/N=0.2499896\). Through \(N=10^6\) one has
\(S_O(N)=146\) and running maximum \(256\), at \(n=985351\). A spot
computation at \(10^7\) has running maximum \(459\). The observed growth
is much smaller than \(N^{5/6}\). The descriptive \(N^{1/3}\)-scale
envelope is not promoted to a theorem.

The bound does not transfer from intervals to Juggler images. For a
general interval \(I=[A,B]\) the variation of \(S_O\) depends on the
right endpoint, not only on \(|I|\). The expanding image
\(Y=J_O(O(I))\) is a sparse gap set. At source bound \(10^6\), recorded
consecutive gaps in \(Y\) range from \(4\) to \(3000\). A certified
finite concentration is the run of \(52\) consecutive odd sources of
equal sign on \([952525,952627]\). Therefore ambient interval
cancellation does not imply orbit or image-set cancellation. This is a
boundary for the present argument, not a proof that no sparse-sequence
estimate can exist.

## 6. The remaining gap

Theorem 4.1 and Corollary 5.2 together say that a uniform one- or
two-step argument covers a set of density \(3/4\). The first odd-to-odd
image expands, so ordinary strong induction cannot fire on that class.
Proposition 4.5 shows that most odd-to-odd starts in a finite window
still return below the start inside twenty steps. That is an
observation, not Terras's theorem for \(J\).

A mixed-parity heuristic, ignoring floors, gives mean log-log drift
\(\tfrac12\log(3/4)<0\). Finite ensembles sit near this value; hard
paths are more odd-rich. This agrees qualitatively with the
juggler-like random-walk model of Prasad and Prasad [12]. Fair parity
is an assumption, not a dynamical theorem, and typical negative drift
is not pointwise contraction.

The gap is therefore:

> No theorem forces every exact integer state into a contracting
> prefix. In particular, it is open whether almost every odd-to-odd
> start has a finite descent certificate.

That is the Juggler form of the Terras question. It is the next
mathematical target. It is not answered by enlarging the finite-word
atlas, by another residual quotient, or by a sharper ambient
discrepancy exponent.

## 7. Software archive

Lean proofs of the exact-arithmetic theorems, the computational checks,
and the laboratory notes live at
[https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).
The archive is not required to read the arguments above. The
discrepancy bound is a human proof; Lean does not certify it.

From a clone, the formal layer and the focused records are

```text
pip install -e ".[dev]"
cd formal && lake build
python tools/render_theorem_ledger.py --check
python -m pytest tests/unit/test_theorem_ledger.py
python -m pytest tests/research/juggler_sequence/test_progress_coverage.py
python -m pytest tests/research/juggler_sequence/test_odd_image_discrepancy.py
python -m pytest tests/research/juggler_sequence/test_global_defect.py
```

A Word Atlas used in the laboratory records bounded realizers and
persistent-expanding blocks through length \(20\) and starts
\(n\le10^8\). It is infrastructure, not a theorem of this note. Absence
of a word in that census means only that the word was not observed
inside the search bound.

## Acknowledgments

I used large language models extensively while drafting and revising the
text, organizing companion notes, and as an interactive assistant for
Lean statements, tests, and literature records. The models are not
authors. Lean theorems and named computations are the certificates for
those claims. The discrepancy bound (Theorem 5.1) is a human proof using
classical analytic inequalities; it is not Lean-certified. I take full
responsibility for the contents.

## References

1. C. A. Pickover, *Computers and the Imagination: Visual Adventures Beyond
   the Edge*, St. Martin's Press, New York, 1991, ch. 40, p. 232.
2. E. W. Weisstein, “Juggler Sequence,” *MathWorld*,
   https://mathworld.wolfram.com/JugglerSequence.html
   (accessed 28 August 2026).
3. OEIS Foundation Inc., “Number of steps needed for juggler sequence
   (A094683) started at \(n\) to reach 1,” Sequence A007320 in *The
   On-Line Encyclopedia of Integer Sequences*,
   https://oeis.org/A007320 (accessed 28 August 2026).
4. J. C. Lagarias, “The \(3x+1\) problem and its generalizations,”
   *Amer. Math. Monthly* 92 (1985), 3–23.
   [doi:10.1080/00029890.1985.11971528](https://doi.org/10.1080/00029890.1985.11971528).
5. J. C. Lagarias (ed.), *The Ultimate Challenge: The \(3x+1\) Problem*,
   American Mathematical Society, Providence, RI, 2010.
6. R. Terras, “A stopping time problem on the positive integers,”
   *Acta Arith.* 30 (1976), 241–252.
   [doi:10.4064/aa-30-3-241-252](https://doi.org/10.4064/aa-30-3-241-252).
7. C. J. Everett, “Iteration of the number-theoretic function
   \(f(2n)=n\), \(f(2n+1)=3n+2\),” *Adv. Math.* 25 (1977), 42–45.
   [doi:10.1016/0001-8708(77)90087-1](https://doi.org/10.1016/0001-8708(77)90087-1).
8. T. Tao, “Almost all orbits of the Collatz map attain almost bounded
   values,” *Forum Math. Pi* 10 (2022), e12.
   [doi:10.1017/fmp.2022.8](https://doi.org/10.1017/fmp.2022.8).
9. R. E. Crandall, “On the ``\(3x+1\)'' problem,” *Math. Comp.* 32
   (1978), 1281–1292.
   [doi:10.1090/S0025-5718-1978-0480321-3](https://doi.org/10.1090/S0025-5718-1978-0480321-3).
10. K. R. Matthews and A. M. Watts, “A generalization of Hasse's
    generalization of the Syracuse algorithm,” *Acta Arith.* 43 (1984),
    167–175.
    [doi:10.4064/aa-43-2-167-175](https://doi.org/10.4064/aa-43-2-167-175).
11. L. Kuipers and H. Niederreiter, *Uniform Distribution of Sequences*,
    Wiley-Interscience, New York, 1974.
12. V. Prasad and M. A. Prasad, “Estimates of the maximum excursion
    constant and stopping constant of juggler-like sequences,”
    ResearchGate preprint, 2025.
    [doi:10.13140/RG.2.2.14110.04168](https://doi.org/10.13140/RG.2.2.14110.04168).
