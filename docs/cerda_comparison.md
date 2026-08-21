# Comparison with the Cerdá Collatz preprints

Miguel Cerdá Bennassar's papers cited here are self-published preprints,
not peer-reviewed sources:

- [I. 2-adic Structure of Tails and Survival Sets in the Collatz Dynamics,
  version 1.1](https://doi.org/10.5281/zenodo.18831439);
- [II. Cylinder collision, bit non-reuse and effective non-degeneracy in
  the 2-adic Collatz dynamics, version 1.1](https://doi.org/10.5281/zenodo.18831527).

The local formulas below are exact and agree with this repository. The
global non-reuse, survival-measure, and convergence claims are not treated
as established here because the posted proofs contain apparent defects.
This is a mathematical scope audit, not a claim about the author's intent.

## Common local formulas

Write

\[
D(p)=\frac{3p+1}{2^{v_2(3p+1)}}
\]

on odd \(p\), and let \(C_k=\{p:v_2(3p+1)=k\}\).

### Exact valuation class

For every \(k\ge1\), \(C_k\) is one residue class modulo \(2^{k+1}\).
Cerdá writes its odd representative as

\[
e_k=
\begin{cases}
(2^k-1)/3,&k\text{ even},\\
(5\cdot2^k-1)/3,&k\text{ odd},
\end{cases}
\pmod {2^{k+1}}.
\]

This is **PROVED** directly: \(3e_k+1\) is respectively \(2^k\) or
\(5\cdot2^k\), so its exact valuation is \(k\). It is the one-step case of
the repository's exact valuation-cylinder construction.

### Affine branch coordinate

Writing

\[
p=e_k+2^{k+1}r,\qquad
A_k=\frac{3e_k+1}{2^k}
=\begin{cases}1,&k\text{ even},\\5,&k\text{ odd},\end{cases}
\]

gives the **PROVED** local identity

\[
\boxed{D(p)=A_k+6r.}
\]

For \(k\ge2\), \(A_k\equiv1\pmod4\). Hence

\[
r\text{ odd}\Longleftrightarrow D(p)\equiv3\pmod4
\Longleftrightarrow v_2(3D(p)+1)=1.
\]

If \(r=2s\), then with

\[
B_k=\frac{3A_k+1}{4}\in\{1,4\}
\]

one obtains

\[
3D(p)+1=4(B_k+9s),\qquad
v_2(3D(p)+1)=2+v_2(B_k+9s).
\]

These local congruences and the corresponding one-step Haar bisections are
valid comparisons. They do not by themselves establish independence after
iteration.

## Relation to this repository

The Cerdá parameter \(r\) is a local free coordinate inside one exact
valuation branch. The repository instead tracks a complete exponent prefix
\(\mathbf{k}\), cumulative budget \(K=\sum k_i\), its unique refined start
representative \(R\bmod2^{K+1}\), and exact affine constant \(C\).

For a fixed prefix, this repository proves:

\[
T^m(n)=\frac{3^mn+C}{2^K},\qquad
R\equiv(2^K-C)3^{-m}\pmod {2^{K+1}}.
\]

Different finite exponent words define exact nested cylinders. That fact
does not imply that each successive “survival” predicate contributes an
independent bit, nor that a measure-zero infinite intersection is empty.

## Apparent defect in the convergence reduction

Paper I defines a restricted survival set by requiring the orbit to avoid
the next valuation \(1\), then claims for the initial class \(C_2\) that
emptiness of the infinite survival set is equivalent to convergence. The
reverse implication says that entering the \(k'=1\) branch “leads to strict
descents until \(1\) is reached.”

That implication is false. If \(v_2(3p+1)=1\), then

\[
D(p)=\frac{3p+1}{2}>p\qquad(p>1).
\]

For example, \(D(3)=5\) and \(D(7)=11\). Entering \(C_1\) is an expanding
odd-to-odd step, not a proof of eventual convergence. A hypothetical
nonconvergent orbit could revisit \(C_1\), so a set restricted to avoiding
\(C_1\) does not capture every possible nonconvergent orbit. Consequently,
the stated equivalence with the Collatz conjecture is not established by
the posted argument.

## Apparent defects in the bit-non-reuse proof

Paper II changes Paper I's effective non-degeneracy conjecture into a
claimed theorem. Several internal statements prevent this repository from
adopting that upgrade.

### Inconsistent hypothesis in the valuation-cylinder lemma

Paper II defines \(B_k=(3A_k+1)/4\in\{1,4\}\), but Lemma 8.5 begins by
assuming \(B\) is odd and the subsequent application treats every \(B_k\)
as satisfying that hypothesis. The case \(B_k=4\) is even. An odd affine
slope is enough to prove suitable congruence statements after a corrected
case analysis, but the lemma as stated does not cover all branches to which
the paper applies it.

### Cylinder count mismatch

Definition 8.1 gives a level-\(N\) cylinder in the normalized \(r_0\)
coordinate measure \(2^{-N}\). Proposition 8.3 then assumes
\(|A_N|=2^N\), computes the union's measure as
\(|A_N|2^{-N}=1\), but concludes a relative measure \(2^{-N}\).
For a disjoint union of level-\(N\) cylinders, the target measure
\(2^{-N}\) would require one cylinder, not \(2^N\). The proposition and
its claimed equivalence with the conjecture are arithmetically
inconsistent as written.

### False lemma for nested cylinders

Lemma 9.16 claims that distinct cylinders of levels at most \(N\) have no
common residue modulo \(2^N\). A counterexample is

\[
0+2\mathbb Z_2\quad\text{and}\quad0+4\mathbb Z_2.
\]

They are distinct, nested cylinders and share the residue \(0\bmod4\).
More generally, the cylinder of an extended itinerary is necessarily a
subcylinder of its prefix cylinder. Paper II itself acknowledges this
nesting and then incorrectly concludes that a strict prefix and its
extension determine distinct residues.

As a result, the claimed map

\[
\text{itinerary}\longmapsto r_0\bmod2^N
\]

is not even single-valued for a cylinder whose level is below \(N\): it
determines a set of residues at that resolution. The global injectivity
corollaries and the subsequent exact-measure factorization therefore do
not follow from the posted proof.

### Local bisection does not repair the global gap

On a fixed branch, an affine map with odd slope preserves Haar measure,
and one additional parity condition halves that branch. This local fact is
**PROVED**. To sum over all iterated branches, however, one still needs a
correct measurable partition and a valid treatment of nested versus
disjoint cylinders. The false cylinder lemma is used precisely at that
global step.

## Version conflict

Paper I version 1.1 labels exact effective non-degeneracy a conjecture and
explicitly identifies variable-scale accumulated correlation as the open
obstacle. Paper II version 1.1 claims to prove it, but relies on the
counting inconsistency and false nesting lemma above. Zenodo descriptions
also present a changing series organization and titles across records.
For reproducibility, any citation should include the exact DOI and version,
not merely “the Cerdá series.”

## Adopted status

- The formulas for \(e_k\), \(A_k\), \(D(p)=A_k+6r\), and
  \(k'=2+v_2(B_k+9s)\) are **PROVED** local identities.
- Finite numerical censuses in the preprints are **COMPUTATIONAL**.
- The posted global bit-non-reuse and exact iterated measure law are
  **NOT ESTABLISHED HERE**.
- The claimed survival-set equivalence with convergence is
  **NOT ESTABLISHED** and uses a false branch implication.
- Measure zero would not imply emptiness in any case.

The repository's **Milestone 6 verified baseline**—exact cylinders,
realizers, lift digits, and finite compatibility states—does not depend on
these global preprint claims. See
[collatz_dual_coding.md](collatz_dual_coding.md) and
[literature_comparison.md](literature_comparison.md).
