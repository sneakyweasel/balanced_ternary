# Local \(\Phi_r\) versus global root-count bounds

Literature triage for whether the residual horizon \(\Phi_r\) improves
the known threshold after which \(N_k(f) := \#\{x \bmod 3^k : f(x)\equiv 0\}\)
admits a closed description. Claim labels follow
[docs/README.md](../README.md). This page does not reopen the ordered or
unordered lifting-state line.

## The candidate

The previous lifting branch proved that \(\Phi_r(\mathfrak{D}_w f)\)
determines the next \(r\) levels of the lifting tree at the node \(n_w\).
The global literature gives a threshold
\(k_0 = O(d^2(\log C + \log d))\) after which \(N_k(f)\) has a closed
form. The question is whether the local state predicts stabilization
earlier, or more adaptively, than that bound.

## A. What \(k_0\) actually guarantees

Source: Dwivedi–Saxena, *Computing Igusa's local zeta function of
univariates in deterministic polynomial-time*, Open Book Series 4 (2020),
197–214, [arXiv:2006.08926](https://arxiv.org/abs/2006.08926)
(`dwivedi-saxena-2020-igusa-univariate`).

Let \(f\in\mathbb{Z}[x]\) have degree \(d\) and coefficient bound \(C\).
Write \(\mathrm{rad}(f)\) for the squarefree kernel, and

\[
\Delta := v_p\bigl(D(\mathrm{rad}(f))\bigr).
\]

\(\Delta\) is finite because the roots of \(\mathrm{rad}(f)\) are distinct.
A Sylvester estimate gives \(\Delta = O\bigl(d(\log_p C + \log_p d)\bigr)\).
Set

\[
k_0 := d(\Delta+1)+1
 \;\le\; d(2d-1)(\log_p C + \log_p d)+1
 \;\le\; O\bigl(d^2(\log C + \log d)\bigr).
\]

The \(O(d^2(\log C+\log d))\) figure in the dossier is the *worst-case
envelope* of this \(k_0\), not an independent bound.

For \(k > d(\Delta+1)\) the paper proves (Theorem 19 / Corollary 2):

1. Every root of \(f\) modulo \(p^k\) lies in a unique neighbourhood of
   a \(\mathbb{Z}_p\)-root \(\alpha_i\) of \(f\) (or there are none).
2. Writing \(e_i\) for the multiplicity of \(\alpha_i\) and
   \(\nu_i := v_p(f_i(\alpha_i))\) for the cofactor,
   \[
   N_k(f)
   = \sum_{i=1}^{n} p^{\,k-\lceil(k-\nu_i)/e_i\rceil}.
   \]
3. If \(D(f)\ne 0\) (equivalently \(f\) squarefree, so every \(e_i=1\)),
   then \(N_k(f)=\sum_i p^{\nu_i}\) is *constant* for all \(k\ge k_0\).
4. If \(f\) is not squarefree, \(N_k\) need not be constant: the formula
   still depends on \(k\) through the ceiling.

So \(k_0\) is a threshold for an *exact closed form of the global count
\(N_k(f)\)*, and for a bijection between representative-root clusters and
\(\mathbb{Z}_p\)-roots. It is not a bound on “when lifts stop”, not a
complexity claim, and not a per-branch statement. Constancy of \(N_k\)
is a special case (squarefree).

Classification: **KNOWN**.

## B. Local bounds already exist

- *Simple Hensel.* If \(f(a)\equiv 0\pmod{p}\) and \(p\nmid f'(a)\), the
  root lifts uniquely to \(\mathbb{Z}_p\). The branch is a single path
  from level 1 on.
- *Strong Hensel* (Conrad, *Hensel's lemma*, Thm 4.1): if
  \(v_p(f(a))>2\,v_p(f'(a))\), there is a unique \(\alpha\in\mathbb{Z}_p\)
  with \(v_p(\alpha-a)=v_p(f(a)/f'(a))\) and \(v_p(f'(\alpha))=v_p(f'(a))\).
  This is already a *root-specific* unique-lift threshold, written in the
  same two valuations that the deep residual \((c,b)\) carries.
- *Newton polygon / Igusa.* Slope data determine the valuations of the
  roots and the generating function of the tree of lifts
  (`zuniga-galindo-2003-igusa-univariate`).
- *Dwivedi–Saxena is already local at the \(\mathbb{Z}_p\)-root.* Once
  \(k>d(\Delta+1)\), the contribution of each \(\alpha_i\) is
  \(p^{k-\lceil(k-\nu_i)/e_i\rceil}\), with \((e_i,\nu_i)\) attached to
  that root. The global \(k_0\) is only a uniformisation that works for
  every cluster at once, using the worst pairwise separation \(\Delta/2\).
- *Adaptive algorithms.* Cheng–Gao–Rojas–Wan (2019) grow a tree of ideals
  and terminate a branch when the local count becomes trivial. That is
  already a local, adaptive procedure, not a closed bound
  (`cheng-gao-rojas-wan-2019-root-counting`).
- *Deterministic counting.* \(N_k(f)\) itself is computable in
  \(\mathrm{poly}(d,k\log p)\) including repeated-root lifts
  (`dwivedi-mittal-saxena-2019-root-count`).

Classification: **KNOWN**. There is no missing “local bound” that
\(\Phi_r\) would be the first to supply.

## C. Global versus root-specific thresholds

Two different objects are easy to conflate.

| object | threshold | source |
|---|---|---|
| closed form for the *global* \(N_k(f)\) | \(k>d(\Delta+1)\) | Dwivedi–Saxena 2020 |
| worst-case envelope of that | \(O(d^2(\log C+\log d))\) | same, Sylvester bound on \(\Delta\) |
| unique lift of *one* simple root | from the first level it appears | Hensel |
| unique lift of *one* singular-looking root | \(v_p(f(a))>2v_p(f'(a))\) | strong Hensel |
| per-cluster count after separation | \((e_i,\nu_i)\) of that \(\mathbb{Z}_p\)-root | Dwivedi–Saxena 2020, Thm 19 |

An adaptive *computational* test “every current root has unit derivative”
detects the first level at which the squarefree part of the tree is a
union of Hensel paths. That test is Hensel applied to the current fibre,
not a new bound, and it says nothing about a multiple-root cluster
(where \(N_k\) never becomes constant).

Classification: the distinction is **KNOWN**. A local adaptive
stabilization threshold for a single branch is Hensel. A local adaptive
threshold for the *global* count is \(\Delta\), already in the 2020 paper.

## D. Finite-horizon jet determinacy

\(\Phi_r(\mathfrak{D}_w f)\) is the \(r\)-jet of \(f\) at \(n_w\), scaled
by the section operators. That the next \(r\) lifting levels are
determined by that jet is the Taylor identity

\[
f(n_w+3^k x)
 = f(n_w) + f'(n_w)\,3^k x + \cdots + 3^{kr}(\cdots),
\]

read modulo \(3^{k+r}\). The previous branch recorded this as
`BTL-taylor-jet` / `BTL-phi-determinacy` and closed it as a
**REPARAMETERIZATION**. Nothing in the present search locates a gap:
every standard Hensel writeup already uses exactly this expansion.

Classification: **REPARAMETERIZATION**.

## E. What is actually open

Do not manufacture an open problem.

The candidate “can \(\Phi_r\) predict stabilization earlier or more
sharply than \(k_0\)?” splits into claims that are all already settled:

- *Earlier unique lift of one node.* Yes, whenever \(p\nmid f'(n)\).
  That is Hensel, **KNOWN**, and is not a statement about \(N_k\).
- *A smaller uniform \(k_0\) from \(\Phi_r\).* No. The obstruction in
  Dwivedi–Saxena is pairwise separation of \(\mathbb{Z}_p\)-roots, which
  is \(\Delta\). A finite jet at one node does not know \(\Delta\), and
  \(\Phi_r\) at a bounded horizon cannot certify that every cluster has
  been separated without an equivalent of that discriminant valuation.
- *An adaptive global threshold from residual states.* Already available:
  compute \(\Delta\) from the Sylvester matrix of \(\mathrm{rad}(f)\), or
  run the 2019/2020 counting algorithms. The residual machine does not
  improve the exponent.
- *Infinite future of a singular branch from a finite \(\Phi_r\).* No.
  The previous branch already showed that for \(k<r\) the state space is
  unbounded in \(\deg f\). A finite jet cannot certify the whole future
  of a multiple-root cluster.

Nothing remains that is **OPEN** and that this laboratory is positioned
to settle. The residue of the question is **PROJECT-SPECIFIC** only as a
measurement: on a given \(f\), the first Hensel-unique node can appear
strictly before \(N_k\) becomes constant. That divergence is the expected
multi-cluster picture, not a new bound.

## Witness that local uniqueness is not global constancy

Take \(f(x)=(x-1)(x^2-9)=x^3-x^2-9x+9\).

- At the residue \(1\), \(f'(1)=-8\), a 3-adic unit. Hensel: unique lift
  of this node from level 1 on. So \(\Phi_1\) at that node is a path, and
  the local branch has “stabilized”.
- At the residue \(0\), \(f(0)=9\) and \(f'(0)=-9\). The cluster of
  \(\pm 3\) is still singular. Measured \(N_k(f)\) for \(k=0,\ldots,6\):

  \[
  1,\;2,\;4,\;7,\;7,\;7,\;7.
  \]

  The simple node is unique from level 1; the count is not constant
  until level 3. Even after \(N_k\) has settled, the nodes near
  \(\pm 3\) remain singular as derivatives (\(3\mid f'(\pm 3)\)), so
  “every current node is Hensel-nonsingular” is a third, still
  different, predicate.

So a local residual/Newton state can be uniquely determined forever
while the global count is still moving. That is exactly why \(\Phi_r\)
cannot replace \(k_0\): they answer different questions.

Recorded in `research.stabilization.triage`.

## Decision

**CLOSE.** Every precise reading of the candidate is **KNOWN** or a
**REPARAMETERIZATION**. A branch whose statements are all of those two
kinds is a close, however much machinery it could produce. No CLI, no
explorer, no Lean.

Best next question: none on this line. Return to a problem whose
statements are not already in Hensel / Newton-polygon / Igusa /
Dwivedi–Saxena.
