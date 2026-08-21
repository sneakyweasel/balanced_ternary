# Balanced ternary versus Collatz coding in the literature

This note separates three numeration systems that can look similar in
Collatz formulas but carry different information:

- canonical balanced base \(3\), with digits \(\{-1,0,+1\}\);
- rational base \(3/2\), with digits \(\{0,1,2\}\);
- binary/2-adic parity or valuation coding.

No identification between these systems is assumed.

## Two exact append laws

### Canonical balanced ternary

For every integer \(n\ne0\), this repository proves

\[
\boxed{\operatorname{BT}(3n+1)=\operatorname{BT}(n)\,+.}
\]

Multiplication by \(3\) shifts the balanced-ternary word and creates a
least-significant \(0\); adding \(1\) changes that \(0\) to \(+\) without
a carry. This describes the numerator \(3n+1\). The accelerated Collatz
step still requires division by
\(2^{v_2(3n+1)}\), which is not a base-\(3\) shift.

### Rational base \(3/2\)

Eliahou and Verger-Gaugry define digits by

\[
2n_i=3n_{i+1}+a_i,\qquad a_i\in\{0,1,2\}.
\]

Their exact result is

\[
\boxed{
\left\langle\frac{3n+1}{2}\right\rangle_{3/2}
=\langle n\rangle_{3/2}1
\quad(n\text{ odd}).
}
\]

Here the appended \(1\) represents the whole odd branch
\((3n+1)/2\) of the parity Collatz map. It is not the balanced-ternary
digit \(+\), and it does not by itself perform the additional halvings in
the accelerated odd-only map.

The analogy is therefore exact but limited:

\[
\begin{array}{c|c|c}
\text{coding} & \text{append operation} & \text{integer map}\\
\hline
\text{balanced base }3 & w\mapsto w+ & n\mapsto3n+1\\
\text{rational base }3/2 & w\mapsto w1 & n\mapsto(3n+1)/2
\end{array}
\]

Primary source:
[Eliahou–Verger-Gaugry (2025)](https://doi.org/10.5802/crmath.662).

## What balanced ternary contributes here

For an exponent prefix \(\mathbf{k}\), let \(R(\mathbf{k})\) be its refined
2-adic minimum realizer. The compatibility interface records the complete
word

\[
\operatorname{BT}(R(\mathbf{k}))
\]

and exact features of that word. This supplies:

- a canonical, signed-digit display of the forced positive representative;
- exact parity through
  \(R\equiv\operatorname{weight}(\operatorname{BT}(R))\pmod2\);
- exact \(3\)-adic divisibility from trailing balanced-ternary zeros;
- finite suffix, run, and digit-count partitions for computation.

These are useful coordinate views. They are not evidence of an additional
independent obstruction to Collatz compatibility.

## Dependence theorem and counterexample

**PROVED.** Once \(\mathbf{k}\) is fixed,

\[
C=C(\mathbf{k}),\qquad
R\equiv(2^K-C)3^{-m}\pmod {2^{K+1}},
\]

and canonical encoding fixes \(\operatorname{BT}(R)\) uniquely. Therefore
\(\operatorname{BT}(R)\) is deterministic from \(R\) and the code. It has
zero conditional information given the complete integer \(R\); it is not
an information-theoretically independent coordinate.

The stronger idea that the complete \(R\), or its balanced-ternary word,
determines future extension data is also false. The Milestone 6 exact
counterexample is

\[
R((1))=R((1,4))=3,\qquad\operatorname{BT}(3)=\texttt{+0},
\]

while the two prefixes have different canonical endpoints, different
zero-lift successors, and different lift digits for the same proposed
extension. Prefix state is indispensable.

## Why lossy balanced-ternary exposure can still help

Deterministic does not mean operationally useless. If a search retains
only \(R\bmod2^P\), a rounded real rate, or a bounded endpoint residue,
then a lossy balanced-ternary statistic can induce a different partition
of the finite sample. Such a statistic may improve indexing,
visualization, clustering, or counterexample search.

That benefit is relative to the other **lossy exposed states**. It does not
create arithmetic information absent from the pair \((R,\mathbf{k})\), and
an empirical separation is **VERIFIED COMPUTATIONALLY** or an
**OBSERVATION**, never a theorem about infinite trajectories.

## Automata-theoretic boundary

Fixed valuation classes and fixed-\(k\) division maps remain finite-state
objects in the repository's LSD-first balanced-ternary model. The
unrestricted odd-part map is not one rational transduction, as proved in
[collatz_mathematics.md](collatz_mathematics.md).

Dhiman and Pandey prove a different limitation: the full arbitrary-step
relation

\[
(x,z,2^j)\quad\text{with}\quad z=T_{q,d}^{\,j}(x)
\]

is not definable in \(BA_2\). Their theorem does not rule out the one-step,
fixed-step, fixed-valuation, or bounded precision-drop constructions used
here. See [literature_comparison.md](literature_comparison.md) for the
exact scope and primary citation.

## Status

The balanced-ternary claims above use the **Milestone 6 verified
baseline**. The literature comparison neither asserts a balanced-ternary
solution strategy nor treats finite feature behavior as a convergence
argument. The four-coordinate conclusion is exact: four views are exposed,
but they are coupled deterministic functions of one exponent code.

## Reproducible experiment record

The versioned `collatz-compatibility/v1` run used:

- exhaustive codes with \(1\le m\le4\) and \(1\le k_i\le4\);
- truncated 2-adic precisions \(P=1,2,3,4\);
- exact rational drift-band membership;
- 32 seeded random critical compositions of length 16 with seed 17;
- mechanical, fixed-budget permutation, and adversarial-order families.

It produced 340 information-content rows and 64 near-critical rows. Exact
selection used integer arithmetic; `d`, `rho_r`, and `rho_M` were labeled
natural-log estimates. The run recovered:

- \(S_0=(m,K)\) does not determine \(\operatorname{BT}(R)\) in the sample;
- \(S_1=(m,K,R)\) determines it globally, by theorem;
- full \(\operatorname{BT}(R)\) does not determine the next zero-lift
  valuation: \((1)\) and \((1,4)\) are an exact witness;
- no balanced-ternary-specific exact obstruction survived the dependence
  test.

The rows and manifests are generated by `btprime collatz information-test
--write` and `btprime collatz near-critical --seed 17 --write`. Generated
JSONL and Parquet artifacts are intentionally ignored by Git; their
manifests record parameters and claim status.
