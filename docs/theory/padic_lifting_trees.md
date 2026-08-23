# 3-adic lifting trees and residual states

Exact record for solution trees of `f(x) ≡ 0 (mod 3^k)` with
`f ∈ ℤ[x]`. Claim labels follow [docs/README.md](../README.md).

The existence of these trees, the separation of singular from
nonsingular branches, and the counting and complexity questions are
**classical**; see [literature position](#literature-position). What is
recorded here is the exact dictionary between lifting and the residual
section calculus, and a sharp finite-horizon determinacy statement in
that language.

## Setup

A residue modulo `3^k` is a balanced-ternary word `w = (a_0,…,a_{k-1})`,
LSD-first, with value

\[
n_w = \sum_{i<k} a_i 3^i,
\qquad
n_w \in \left[-\tfrac{3^k-1}{2},\ \tfrac{3^k-1}{2}\right],
\]

and this is a bijection onto that interval. Write `ρ_a(f) = [f(a)]_3` and
`𝔇_a f(x) = (f(a+3x) - ρ_a(f))/3` for the residual section operators of
[balanced_ternary_calculus.md](balanced_ternary_calculus.md), `𝔇_w` for
the composite along `w`, and `ρ_i` for the output trit emitted at step
`i`.

## Iterated reconstruction

**PROVED — LEAN.** For every `f ∈ ℤ[x]` and every trit word `w` of
length `k`,

\[
f(n_w + 3^k x) \;=\; \sum_{i<k} \rho_i 3^i \;+\; 3^k\,(\mathfrak{D}_w f)(x).
\]

*Proof.* Induction on `k`. The case `k = 0` is trivial and `k = 1` is the
section reconstruction `f(a+3x) = ρ_a(f) + 3 𝔇_a f(x)`. Assuming the
identity for `w` of length `k` and appending a trit `a`, so that
`n_{wa} = n_w + a 3^k`,

\[
f(n_{wa} + 3^{k+1}x) = f\bigl(n_w + 3^k(a+3x)\bigr)
 = S_w + 3^k\bigl(\rho_a(\mathfrak{D}_w f) + 3\,\mathfrak{D}_a\mathfrak{D}_w f(x)\bigr),
\]

and `ρ_a(𝔇_w f)` is exactly the output trit at step `k`. ∎

Lean: `BTCalculus.iterated_reconstruction`.

## Lifting tree equals the zero-output subtree

**PROVED — LEAN.** `3^k` divides `f(n_w)` if and only if every output
trit along `w` is `0`.

*Proof.* Setting `x = 0` above gives `f(n_w) = S_w + 3^k c_0` with
`S_w = Σ_{i<k} ρ_i 3^i`. So `3^k | f(n_w)` iff `3^k | S_w`. Because the
`ρ_i` are trits, `|S_w| ≤ (3^k-1)/2 < 3^k`, hence `3^k | S_w` iff
`S_w = 0`, and by uniqueness of the balanced expansion that holds iff
every `ρ_i = 0`. ∎

The Lean statement needs no hypothesis that `w` consists of trits: the
*outputs* are trits whatever the sections are, and that is all the
packing bound uses. Trits are needed only for the separate fact that
length-`k` words enumerate the residues modulo `3^k` exactly once.

This is the point at which the balanced digit set does real work: for
digits in `{0,1,2}` the partial sum can equal `3^k - 1` without being
zero, and the equivalence would have to be stated modulo the ambient
digit range instead of as literal vanishing.

Two consequences. First, the set of solutions is prefix-closed
automatically, so it really is a tree. Second, the children of a node
are

\[
\{\,a \in \{-1,0,+1\} \;:\; \rho_a(\mathfrak{D}_w f) = 0 \,\},
\]

which depends only on the residual state. The lifting tree of `f` is the
zero-output subtree of the residual Mealy machine of `f`.

Lean: `BTCalculus.lift_iff_outputs_zero`.

## The residual state is the scaled Taylor jet

**PROVED.** For `j ≥ 1` the coefficient of `x^j` in `𝔇_w f` is

\[
3^{k(j-1)}\,\frac{f^{(j)}(n_w)}{j!},
\]

in particular the linear coefficient is exactly `f'(n_w)`, with no
scaling. On a node of the lifting tree the constant coefficient is
`f(n_w)/3^k`.

*Proof.* Expand `f(n_w + 3^k x) = Σ_j (f^{(j)}(n_w)/j!) 3^{kj} x^j` and
compare with the iterated reconstruction. For `j ≥ 1` the constant `S_w`
does not contribute, so dividing by `3^k` gives the claim; the `j = 0`
term gives `(f(n_w) - S_w)/3^k`, which is `f(n_w)/3^k` exactly when
`S_w = 0`. ∎

**REPARAMETERIZATION.** This is the certificate that the residual state
carries no information beyond the classical Taylor data at the node. Any
statement about lifting expressed through residual states can be
rewritten in derivatives and vice versa. The residual formulation is a
change of coordinates, not new information.

Verified computationally in `research.lifting.triage.h2_taylor_jet`.

## One-step trichotomy

**PROVED — LEAN, KNOWN.** For `k ≥ 1` and a node `w` of the tree at
level `k`, write `g = 𝔇_w f`. Since the coefficient of `x^j` in `g` is
divisible by `3^k` for `j ≥ 2`, we get `g(a) ≡ f(n_w)/3^k + a f'(n_w)
\pmod 3`, hence the child count is

- `1` if `3 ∤ f'(n_w)` — ordinary Hensel uniqueness;
- `3` if `3 | f'(n_w)` and `v_3(f(n_w)) ≥ k+1`;
- `0` if `3 | f'(n_w)` and `v_3(f(n_w)) = k`.

This is the classical count; it is recorded here only because it drops
out of the two statements above. The hypothesis `k ≥ 1` is not
cosmetic: at the root, `f = x^2 + x` has two children with a unit
derivative, a count the trichotomy forbids at every higher level.

Lean: `BTCalculus.lift_condition`, `BTCalculus.unique_lift_of_nonsingular`,
`BTCalculus.all_lifts_of_singular_deep`,
`BTCalculus.no_lift_of_singular_shallow`, and the three cases together as
`BTCalculus.lift_trichotomy`.

## Finite-horizon determinacy

Let `Φ_r` be the Newton residue invariant of
[polynomial_function_congruence.md](polynomial_function_congruence.md),
so that `Φ_r(g) = Φ_r(h)` iff `g ≡_r h` as functions modulo `3^r`.

**PROVED.** If `g ≡_r h` then the depth-`r` subtrees below `g` and `h`
agree, including the branch trits.

*Proof.* Induction on `r`. For `r ≥ 1`, `g ≡_r h` implies `g(a) ≡ h(a)
\pmod 3` for every trit, so `ρ_a(g) = ρ_a(h)` and the two states have the
same children. For the transition, `𝔇_a g - 𝔇_a h` evaluated at `x` is
`((g-h)(a+3x) - (ρ_a(g) - ρ_a(h)))/3 = (g-h)(a+3x)/3`, and `3^r` divides
`(g-h)(a+3x)`, so `𝔇_a g ≡_{r-1} 𝔇_a h`. Apply the inductive hypothesis
to each child. ∎

**PROVED.** The horizon is sharp: `Φ_{r-1}` does not determine the
depth-`r` subtree. Smallest witness at `r = 2`: `x^2` and `x^2 - 3` agree
as functions modulo `3`, but at depth `2` all three grandchildren of the
root survive for `x^2` while none survive for `x^2 - 3`.

So the answer to "can residual state predict the lifting tree from
finite local data" is yes, with `Φ_r` a sufficient horizon for depth `r`
and `r` the sharp *depth* at which a horizon is needed. Sharpness of the
horizon is not minimality of the state: `Φ_r` is strictly larger than
needed, quantified in
[lifting_state_complexity.md](lifting_state_complexity.md).
Since `Φ_r` ranges over a finite set depending only on `r` and
`deg f`, the number of distinct depth-`r` subtrees is bounded
independently of `k`, while the number of residues modulo `3^k` is
`3^k`. That is a compression statement about the tree, **not** a
complexity claim: deterministic `poly(deg f, k log 3)` root counting is
already known (`dwivedi-mittal-saxena-2019-root-count`).

## Deep regime: linearization

**PROVED.** For `k ≥ r`, every coefficient of `𝔇_w f` in degree `j ≥ 2`
is divisible by `3^{k(j-1)}` and hence by `3^r`, so

\[
\mathfrak{D}_w f \;\equiv_r\; \frac{f(n_w)}{3^k} + f'(n_w)\,x .
\]

Linear states are closed under the section operators: `𝔇_a(c + bx) =
D(c + ab) + bx`, so `b` is invariant along the tree and only the
constant moves. Combining with the determinacy statement, for `k ≥ r`
the depth-`r` subtree is determined by the two residues

\[
\bigl(f(n_w)/3^k \bmod 3^r,\ f'(n_w) \bmod 3^r\bigr).
\]

This is a *sufficient* state in the deep regime, and it is the classical
Newton-polygon picture in residual coordinates.

**Sufficiency only.** An earlier version of this section called the two
residues "the minimal state". That is false. On a surviving branch
`𝔇_a(λg) = λ 𝔇_a g` for every `λ` coprime to 3, so the whole ordered
depth-`r` subtree is invariant under unit scaling while `Φ_r` is not; the
smallest live witness is `x` against `-x`. The deep-regime state count
collapses from `3^{2r}` to `(3^{r+1}-1)/2 + r`, that is from 9, 81, 729 to
5, 15, 43. Every determinacy statement in this file remains true as
stated — they are all sufficiency claims — but none of them is a
minimality claim. See
[lifting_state_complexity.md](lifting_state_complexity.md).

The minimal state is now known exactly, and it stays inside the
Newton-polygon picture: after scaling `b` to a power of 3, the behaviour is
`v_3(c)` alone where `v_3(c) < v_3(b)`, and the full unit-scaling orbit
elsewhere.

## Valuations are not enough

**PROVED.** The candidate "lifting behaviour at level `k` is determined
by `v_3(f(n))` and `v_3(f'(n))`" is **false**, even for the bare tree
shape with sibling order discarded.

Smallest witness above the root: the level-1 node `0` of `x^2 + 9` and of
`x^2 - 9`. Both have `v_3(f(0)) = 2`, both have `f'(0) = 0`, so both
valuation data agree exactly; the residual states are `3 + 3x^2` and
`-3 + 3x^2`. At depth 2 the first has no surviving grandchildren and the
second has six, because `-1` is not a square modulo `3`. Recorded in
`tests/unit/test_lifting.py::test_valuations_do_not_determine_the_subtree`.

At the root the witness is smaller still and purely about existence:
`x^2 + 1` has no children, `x^2 - 1` has two, and both have the same
capped valuation pair.

**VERIFIED COMPUTATIONALLY.** In the deep regime `k ≥ r` the capped pair
`(min(v_3(f(n)/3^k), r), min(v_3(f'(n)), r))` does determine the
*unordered* depth-`r` subtree, i.e. the shape with sibling order
discarded, for `r ≤ 4`. Checked exhaustively over all linear states
`c + bx` with `|c| ≤ 121` and `|b| ≤ 40` — which by linearization is the
complete deep-regime state space up to `≡_r` — and over every node of the
53 test polynomials of `research.lifting.families` up to level 6. What
valuations do not fix is *which* branches survive; that needs the
residues.

**OPEN.** Is that a theorem? A proof would have to control the multiset
of `v_3` of the three children `c/3 + a·3^{e-1}u` of a linear state, and
the special child where cancellation occurs has unbounded valuation, so
the capping is doing real work. No proof and no counterexample is
recorded.

## Literature position

- The tree of lifts of a univariate polynomial, and its generating
  function, is `zuniga-galindo-2003-igusa-univariate`.
- Root counting modulo `p^t` through a tree of ideals that partitions by
  multiplicity, so singular branches are explicit, is
  `cheng-gao-rojas-wan-2019-root-counting`.
- Deterministic `poly(deg f, k log p)` root counting, including the lifts
  of a repeated root, is `dwivedi-mittal-saxena-2019-root-count`.
- A closed form for `N_k(f)` once `k ≥ k0 = O(d^2(\log C + \log d))`, and
  an elementary proof of Igusa rationality, is
  `dwivedi-saxena-2020-igusa-univariate`. Igusa rationality itself dates
  to 1974.
- The multivariate singular case being the genuine obstruction is stated
  in `dwivedi-saxena-2024-systems-non-fields`.

Nothing in this file improves any of those. The finite-horizon
determinacy statement is *local* — it bounds how much of one node's
state is needed for the next `r` levels — where the known bounds are
global in `k`. Whether the local form has any consequence the global
form does not already give is open and is not claimed.

## Where the code is

- Core objects: `bt.calculus.lifting` (`LiftNode`, `lift_tree`,
  `depth_r_shape`, `shape_widths`).
- Minimal state: `bt.calculus.lifting_state` and
  [lifting_state_complexity.md](lifting_state_complexity.md).
- Classification experiments: `research.lifting.triage`.
- Test polynomials: `research.lifting.families`.
- Lean: `formal/BTCalculus/PadicLifting.lean`.
- CLI: `btprime congruence roots | lift | tree | classify`.
- Explorer: the "Congruence / lifting" secondary view of the Residual
  explorer.
