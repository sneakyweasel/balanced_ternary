# Minimal finite-horizon state for 3-adic lifting

Exact record for the *minimal* local datum that determines the next `r`
levels of the lifting tree of `f(x) ≡ 0 (mod 3^k)`. Claim labels follow
[docs/README.md](../README.md). The sufficiency side — that `Φ_r`
determines the depth-`r` subtree — is in
[padic_lifting_trees.md](padic_lifting_trees.md); this file is about how
far below `Φ_r` the truth sits.

Root counting and the lifting tree itself are classical. Nothing here
improves the deterministic `poly(deg f, k log 3)` counting of
`dwivedi-mittal-saxena-2019-root-count`, and no complexity claim is made.
The object of study is the state space, not the count.

## The observable

Two residual states are **`r`-lifting-equivalent**, written `g ∼_r h`,
when their ordered, trit-labelled depth-`r` lifting subtrees coincide.
That subtree is already computed by
`bt.calculus.lifting.depth_r_shape(g, r, mode="digits")`, so `∼_r` is a
fibre of a function and needs no closure argument. The named wrapper is
`bt.calculus.lifting_state.behaviour_class`.

The quotient chain under study, in the deep regime `k ≥ r`:

| description | states at horizon `r` | `r = 1..5` |
|---|---|---|
| `Φ_r`, equivalently `(c, b) mod 3^r` | `3^{2r}` | 9, 81, 729, 6561, 59049 |
| unit-scaling orbits | `2·3^r − 1` | 5, 17, 53, 161, 485 |
| lifting behaviour `L_r` | `(3^{r+1}−1)/2 + r` | 5, 15, 43, 125, 369 |

Both surjections are strict from `r = 2` on.

The last row is now closed, and closing it produced a normal form rather
than only a count: after unit-scaling `b` to a power of `3`, the behaviour
is `v_3(c)` alone where the constant dominates the derivative, and the full
unit orbit everywhere else. See
[the normal form](#the-minimal-state-as-a-normal-form), which is also why
the branch closes as a reparameterization.

## Unit scaling collapses the jet

**PROVED.** Let `λ` be coprime to `3`. If the trit `a` survives at `g`,
that is `ρ_a(g) = 0`, then

\[
\mathfrak{D}_a(\lambda g)(x) = \frac{\lambda g(a+3x) - 0}{3}
 = \lambda\,\mathfrak{D}_a g(x),
\]

and `ρ_a(λg) = 0` iff `ρ_a(g) = 0` because `3 | λ g(a)` iff `3 | g(a)`.
So `g` and `λg` have the same children, and on every surviving child the
scaled state is again a unit multiple. By induction on `r` the entire
ordered, trit-labelled depth-`r` subtree is invariant under `g ↦ λg`. ∎

Note where the hypothesis is used: `𝔇_a(λg) = λ 𝔇_a g` holds *only* on a
surviving branch, since off the tree the subtracted residue `ρ_a(λg)` is
not `λ ρ_a(g)` in general. The invariance is a statement about the
lifting tree, not about the residual machine as a whole.

Lean: `BTCalculus.sectionDeriv_smul_of_root` for the linearity,
`BTCalculus.outputAlong_smul_iff` for the word-level invariance, and
`BTCalculus.isRootMod_smul_iff` for the lifting tree itself. A word
carries its own trits, so invariance of the surviving-word set *is*
invariance of the ordered trit-labelled subtree; no tree datatype is
needed.

**PROVED.** `Φ_r` is therefore not minimal. Smallest live witness, at
every `r`:

\[
g = x, \qquad h = -x .
\]

Both are live — the trit `0` survives at each — both have the single
all-zeros lifting path to every depth, and
`Φ_r(x) = (0, 1)` against `Φ_r(-x) = (0, 3^r - 1)`. This is the orbit of
`λ = -1`, and it is the smallest live witness over all linear states with
`|c|, |b| ≤ 13`.

The witness must be *live*. Two dead states share the empty behaviour
whatever their jets, so `1` against `-1` is also jet-redundant and means
nothing; any search that does not exclude dead states reports noise.
Recorded in `research.lifting.state_complexity.minimality_witness`.

**PROVED.** Unit scaling is nevertheless not the whole collapse. The
orbit count `2·3^r − 1` strictly exceeds `L_r` from `r = 2` on (17 against
15), so it is a proper intermediate quotient. Scaling explains the cause
of non-minimality, not its size.

## The linear transition law

**PROVED.** For a linear state and any `a ∈ ℤ`,

\[
\mathfrak{D}_a(c + bx) = D(c + ab) + b\,x,
\qquad D(m) = \frac{m - [m]_3}{3},
\]

and the trit `a` survives iff `3 | c + ab`, in which case the child is
`((c + ab)/3, b)`.

*Proof.* `(c + b(a+3x) - ρ)/3 = (c + ab - ρ)/3 + bx` with `ρ = [c+ab]_3`. ∎

Two immediate consequences, both used throughout below:

- **`b` is invariant along the whole tree**, so `e = min(v_3(b), r)` is a
  conserved quantity of a deep-regime branch.
- Linear states are closed under the section operators, so together with
  the deep-regime linearization of
  [padic_lifting_trees.md](padic_lifting_trees.md) the deep behaviour
  space is exactly the behaviour space of the pairs `(c, b) mod 3^r`.

Lean: `BTCalculus.sectionDeriv_linState`, with survival as
`BTCalculus.linState_root_iff`.

## The nonsingular row is Newton's method

**PROVED.** Let `3 ∤ b` and put `u = c·b^{-1} mod 3^r`. Then:

1. exactly one trit survives at each of the next `r` levels, so the
   depth-`r` behaviour is a single path;
2. the emitted trits are `-[u]_3, -[Du]_3, …`, that is the balanced
   expansion of `-u`, LSD first;
3. the behaviour depends only on `u`, all `3^r` values of `u` give
   distinct behaviours, and all `3^r` are realised.

*Proof.* Survival is `3 | c + ab` with `b` a unit modulo `3`, so
`a ≡ -cb^{-1} ≡ -u (mod 3)`, which pins `a = -[u]_3` uniquely among the
trits. In the normalised coordinate the child is
`u' = ((c+ab)/3)·b^{-1} = (u + a)/3 = (u - [u]_3)/3 = D(u)`, using
`b`-invariance. Iterating, the trit sequence is the balanced expansion of
`-u`, and the balanced expansion is a bijection between `ℤ/3^r` and trit
strings of length `r`, which gives both distinctness and surjectivity. ∎

**REPARAMETERIZATION.** Statement 2 *is* Hensel–Newton lifting. The
Newton correction at a nonsingular node is `-f(n)/f'(n)`, whose balanced
digits are read off one level at a time; `u ↦ D(u)` is the digit-shift
form of `x ↦ x - f(x)/f'(x)`. The count `3^r` and the minimality around
it are exact and project-specific, but the identification of the surviving
path adds nothing to classical Hensel lifting.

Lean: `BTCalculus.outputAlong_liftPath` for survival to any depth,
`BTCalculus.liftPath_unique` for uniqueness of the word, and
`BTCalculus.henselTrit_eq_newton` for the identification of the trit with
the balanced digit of `-c/b`.

## The singular rows

Fix `e = v_3(b)` with `1 ≤ e ≤ r`, and let `m = min(v_3(c), r)`. By unit
scaling we may take `b = 3^e` exactly, so a row is a one-parameter family
in `c mod 3^r`. Write `T_j` for the behaviour "fully ternary to depth
`min(j, r)`, then dead".

**PROVED (structure).** The row splits by `m`:

- **`m < e`.** Each child constant is `c/3 + a·3^{e-1}`, and
  `3^{e-1} ≡ 0 (mod 3)` forces all three children into the same class
  modulo 3. So branching is all-or-nothing: either every trit survives or
  none does, and the valuation drops by exactly one per level because the
  `a`-dependent term has strictly larger valuation than `c/3`. The
  behaviour is `T_m`. This contributes the `e` behaviours
  `T_0, …, T_{e-1}`.
- **`m ≥ e`.** Write `c = 3^e d`. After `j ≤ e` steps the constant is
  `3^{e-j}(d + a_1 + 3a_2 + … + 3^{j-1}a_j)`, so survival is automatic for
  `j < e` and the first `e` levels are fully ternary with `3^e` leaves.
  The leaf reached by a word `w` is the state `(d + packWord(w), 3^e)` at
  remaining depth `r - e`. The whole behaviour is therefore the function
  `w ↦ (depth-(r-e) behaviour of d + packWord(w))`, which depends only on
  `d mod 3^{r-e}`, giving at most `3^{r-e}` behaviours.

*Proof of the `m ≥ e` recursion.* Generalise to
`𝔇_w (3^j d + 3^{j+i} x) = (d + 3^i·packWord(w)) + 3^{j+i} x` for
`|w| = j`, which is an induction on `w`: one section step sends
`(3^{j+1}d, 3^{j+1+i})` to `(3^j(d + 3^i a), 3^{j+(i+1)})`, and
`packWord(a::w) = a + 3·packWord(w)` matches the shift. Set `i = 0`,
`j = e`. ∎ (Lean: `residualAlong_linState_pow`,
`residualAlong_linState_leaf`, `outputAlong_linState_pow`.)

**The shift is the balanced value of the word, not its digit sum.** An
earlier draft of this file recorded the digit sum, and the error was not
cosmetic: it changes the set of shifts from the `2e+1` values `|s| ≤ e` to
all `3^e` values, and the separation argument below needs a complete
residue system modulo `3^e`. With the digit sum the separation is false —
for `e = 2` every `d ≡ 3` and `d ≡ 6 (mod 9)` would give the identical
tuple `(∅,∅,T_1,∅,∅)` — which is why the row count looked unreachable.
`shift_law` in `research.lifting.state_complexity` keeps both candidates
in the record and refutes the digit sum.

**PROVED.** The row count is exactly

\[
N(r,e) = 3^{\,r-e} + e ,
\]

also verified exhaustively for `1 ≤ r ≤ 6` and every `0 ≤ e ≤ r`. The rows
for `r = 1..6`:

| `e` | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 0 | 3 | 9 | 27 | 81 | 243 | 729 |
| 1 | 2 | 4 | 10 | 28 | 82 | 244 |
| 2 | | 3 | 5 | 11 | 29 | 83 |
| 3 | | | 4 | 6 | 12 | 30 |
| 4 | | | | 5 | 7 | 13 |
| 5 | | | | | 6 | 8 |
| 6 | | | | | | 7 |

**PROVED (two rows exactly).** The extreme rows follow from the structure
theorem with no gap:

- `e = 0` is `3^r`, the nonsingular classification above.
- `e = r` is `r + 1`. Modulo `3^r` the derivative is `0`, so every trit
  survives iff `3 | c` and the child constant is `c/3` regardless of the
  trit. The behaviour is exactly `T_m`, and `m` ranges over `0, …, r`.
- `e = 1` is `3^{r-1} + 1`: the dead behaviour `T_0`, plus, for `3 | c`,
  a chain of tridents in which the three child constants `c/3 - 1`,
  `c/3`, `c/3 + 1` lie in distinct classes modulo 3, so exactly one
  continues. The behaviour is the sequence of continuing positions at
  levels `1, …, r-1`, giving `3^{r-1}` behaviours.

### Separation: the middle rows

For `1 < e < r` the structure theorem bounds the `m ≥ e` part by `3^{r-e}`.
Attainment needs injectivity of the *shifted family*

\[
\Phi_R : d \bmod 3^{R} \;\longmapsto\; \bigl(B_{R}(d+t)\bigr)_{t \in W_e},
\qquad R = r-e,
\]

where `B_R` is the depth-`R` behaviour map of the same row and
`W_e = [-(3^e-1)/2, (3^e-1)/2]` is the window of shifts from the block
shift law. The family is needed because `B_R` alone is far from injective:
every `d` with `3 ∤ d` gives the dead behaviour.

**PROVED.** `Φ_R` is injective for every `e ≥ 1` and every `R ≥ 0`.

*Proof.* Induction on `R`. For `R = 0` the domain is trivial.

`W_e` has `3^e` consecutive integers, so it is a complete residue system
modulo `3^e`; write `t_0` for its unique element with `3^e | d + t_0`.

If `R ≤ e`, then `B_R(x) = T_{min(v_3(x),R)}` for every `x`: either the
valuation is below `e` and the structure theorem gives `T`, or it is at
least `e ≥ R` and the block is fully ternary to depth `R`, which is `T_R`.
So the tuple records `min(v_3(d+t), R)` for all `t ∈ W_e`. For each
`j ≤ R ≤ e` the set `{t ∈ W_e : 3^j | d+t}` is nonempty and equals
`{t ∈ W_e : t ≡ -d}` modulo `3^j`, which pins `d mod 3^j`; take `j = R`.

If `R > e`, then every `t ≠ t_0` has `v_3(d+t) < e`, so its entry is
`T_{v_3(d+t)}`, of depth `< e`. The entry at `t_0` is fully ternary to
depth `e` and at least one of its leaves survives another step, since the
leaf shifts again cover every class modulo 3. So `t_0` is the unique index
whose entry has depth `≥ e`; reading it off gives `d mod 3^e`. Writing
`d + t_0 = 3^e d'`, the block shift law makes that entry the depth-`e`
ternary block carrying `Φ_{R-e}(d')`, so induction gives
`d' mod 3^{R-e}`, hence `d + t_0 mod 3^R`, hence `d mod 3^R`. ∎

The proof is exactly why the digit-sum error mattered: with a window of
`2e+1 < 3^e` shifts there is no `t_0` at all for most `d`, and the
induction has nothing to descend into.

Tests: `test_shifted_family_separates_residues` and
`test_the_recursing_leaf_is_the_unique_tall_one`, with the reproducible
experiment in `shifted_family_injectivity`.

## The total, and the overlap

**PROVED, given the rows.** The rows double-count exactly the truncated
trees. `T_j` occurs in row `e` iff `j < e`, together with `T_r` in row
`r`, so `T_j` occurs in `r - j` rows for `j < r` and once for `j = r`.
The excess over the `r` distinct truncated trees is

\[
\sum_{j<r} (r - j - 1) \;=\; \binom{r}{2},
\]

verified for `r ≤ 6`. Hence

\[
L_r \;=\; \sum_{e=0}^{r}\bigl(3^{\,r-e} + e\bigr) - \binom{r}{2}
 \;=\; \sum_{j=0}^{r} 3^{j} + \frac{r(r+1)}{2} - \frac{r(r-1)}{2}
 \;=\; \frac{3^{\,r+1} - 1}{2} + r .
\]

∎ Values: 5, 15, 43, 125, 369, 1099.

`L_r` inherits the classification of the rows it is summed from, which are
now **PROVED**; the count is also verified exhaustively to `r = 6`.

## Attainment

**PROVED.** `L_r` is attained by genuine lifting nodes, so it is the
exact number of deep-regime behaviours and not merely an upper bound.
For any target `(c, b)`,

\[
f_{c,b}(x) = 3^{r} c + b\,x
\]

has `f(0) = 3^r c` and `f'(0) = b`, so the origin is a level-`r` node of
its own lifting tree, and `𝔇_{0^r} f_{c,b} = c + bx` exactly, because
`ρ_0(3^j c) = 0` for `j ≥ 1`. Ranging `(c, b)` over `(ℤ/3^r)^2` realises
every counted behaviour.

The realisation is not an artefact of degree 1: adding `3^r x^2`
contributes `3^{2r} x^2` to the residual, invisible modulo `3^r`, and the
quadratic family attains `L_r` as well. Both checked in
`research.lifting.state_complexity.attainment`.

## The minimal state as a normal form

The count is a corollary of something more informative. Scale by a unit so
that `b ≡ 3^e` with `e = min(v_3(b), r)`, and split on whether the constant
or the derivative has the smaller valuation.

**PROVED.** The depth-`r` behaviour of `(c, b)` is

- **dominated**, `v_3(c) < e`: the fully ternary tree truncated at depth
  `v_3(c)`. The behaviour depends on `v_3(c)` and on nothing else — not on
  `e`, not on the rest of `c`. There are `r` such classes, `T_0, …, T_{r-1}`.
- **undominated**, `v_3(c) ≥ e`: exactly the unit-scaling orbit of
  `(c, b)` modulo `3^r`, with no further collapse. There are
  `(3^{r+1}-1)/2` such classes.

So the minimal state is *the unit orbit, degenerated to `v_3(c)` wherever
the constant dominates*, and

\[
L_r = \underbrace{r}_{\text{dominated}} + \underbrace{\frac{3^{r+1}-1}{2}}_{\text{undominated}} .
\]

The dominated case is the first bullet of the structure theorem; the
undominated case is the separation theorem, since on that stratum the
normalised pair `(e, c mod 3^r)` is precisely the orbit. Both halves are
verified as a bijection with the behaviour classes for `r ≤ 4`
(`normal_form`, `strata`, and `test_minimal_state_key_is_a_complete_invariant`).

This is also the sharpest statement of what the branch found, and of its
limits. The undominated half says unit scaling is the *only* collapse
there — the earlier "orbits are not minimal" result is entirely an artefact
of the dominated stratum. And both halves are recognisable classical
content: dominance is the Newton-polygon observation that a branch dies at
depth `v_3(c)` when the constant term wins, and orbit rigidity on the rest
is Hensel/Newton uniqueness. `minimal_state_key` is the invariant in code.

Forgetting the branch trits is a strictly coarser quotient, and that
quotient *is* valuation-determined: `U_r = T_m` if `m < e` and
`S(e, r)` otherwise. Proof and closed form live in
[padic_lifting_trees.md](padic_lifting_trees.md#valuations-are-not-enough).
That line is closed; do not reopen it from this file.

## The shallow regime

**OBSERVATION, no theorem claimed.** For `k < r` the higher jet
coefficients of `𝔇_w f` survive modulo `3^r`, so the state space is
unbounded in `deg f` and the deep analysis does not apply. Census over
the 53 polynomials of `research.lifting.families` up to level 4:

| `r` | shallow `Φ_r` | shallow behaviours | deep `Φ_r` | deep behaviours | `L_r` |
|---|---|---|---|---|---|
| 1 | 9 | 6 | 9 | 5 | 5 |
| 2 | 72 | 29 | 46 | 13 | 15 |
| 3 | 180 | 54 | 113 | 24 | 43 |

The shallow behaviour count already exceeds the deep bound at `r = 1`, in
one line: a level-0 state may have two children, which the trichotomy
forbids at every higher level. No family-independent description of the
shallow minimal state is offered.

## What is and is not new

The lifting tree, the singular/nonsingular split, and Hensel lifting are
classical. Against that:

- The nonsingular half of the classification is a
  **REPARAMETERIZATION** of Newton iteration in balanced digits.
- Unit-scaling invariance and the resulting non-minimality of `Φ_r` are
  exact and, as far as the recorded literature goes, not stated anywhere
  in this form — but they are also a two-line consequence of the
  definition, so the honest description is "a correction to our own
  earlier sufficiency claim", not a contribution.
- The block shift law and the separation theorem are exact and were the
  real content of the singular rows. The separation proof is a page.
- The closed form `L_r` is a genuine exact count of a finite quotient,
  attained and now fully proved. It is a statement about a state space and
  has no counting or complexity consequence.

The normal form is what settles the novelty question, and it settles it
against us. Once the quotient is written as "the unit-scaling orbit,
degenerated to `v_3(c)` on the dominated stratum", both ingredients are
standard: dominance in the Newton polygon, and Hensel rigidity. The
`3^{r-e} + e` rows and the `binom(r,2)` overlap are then arithmetic
bookkeeping over that description. The exact count is new as a number; the
object it counts is not new as an object.

The plausible published home for a minimal-state statement would be
automata minimisation applied to `p`-adic root lifting. The burden was to
show the minimal quotient is not bookkeeping about Newton's method, and
the normal form shows that it is. Branch decision: **CLOSE —
REPARAMETERIZATION**, with the exact statements retained as platform
machinery.

## Where the code is

- Core: `bt.calculus.lifting_state` (`behaviour_class`, `linear_step`,
  `newton_path`, `behaviour_count`,
  `behaviours_by_derivative_valuation`, `truncated_tree`,
  `block_shift`, `shift_window`, `minimal_state_key`, `is_dominated`,
  `valuation_unordered_shape`).
- Experiments: `research.lifting.state_complexity` (`shift_law`,
  `shifted_family_injectivity`, `normal_form`, `strata`).
- Lean: `formal/BTCalculus/PadicLiftingState.lean`.
- CLI: `btlab congruence state | distinguish`.
- Explorer: the minimal-state panel of the "Congruence / lifting" view.
