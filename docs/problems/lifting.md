# Polynomial congruences and 3-adic lifting trees

## Problem

Whether the balanced-ternary residual-state machinery exposes structure
in 3-adic lifting of polynomial congruences that ordinary coefficient
and derivative methods do not.

## Exact statement

For `f ∈ ℤ[x]` and `k ≥ 0`, study the tree whose level-`k` nodes are the
residues `x mod 3^k` with `f(x) ≡ 0 (mod 3^k)`, edges given by reduction
from level `k+1` to level `k`. Ask: is there a finite state, attached to
a node, that determines the whole depth-`r` subtree below it, and is that
state smaller than the residue itself?

## Current literature

`known` throughout for the objects and the algorithms.

- `zuniga-galindo-2003-igusa-univariate` — the tree of `p`-adic root
  approximations of a univariate `f`, and Igusa's zeta function as its
  generating function.
- `cheng-gao-rojas-wan-2019-root-counting` — a tree of ideals for
  counting roots in `Z/(p^t)`, partitioned by multiplicity so singular
  branches are explicit.
- `dwivedi-mittal-saxena-2019-root-count` — deterministic
  `poly(deg f, k log p)` root counting, including the first deterministic
  count of the lifts of a repeated root.
- `dwivedi-saxena-2020-igusa-univariate` — closed form for `N_k(f)` once
  `k ≥ k0 = O(d²(log C + log d))`, constant beyond `k0` when the
  discriminant is nonzero.
- `dwivedi-saxena-2024-systems-non-fields` — multivariate systems modulo
  `p^k`, with singular `F_p`-root lifting identified as the obstruction.
- `kempner-1921-polynomials-residue-systems` — the function-congruence
  kernel behind the `≡_r` invariant used here.

Consequence, fixed before any result was recorded: constructing a
lifting tree, separating singular from nonsingular branches, counting
lifts, and beating `3^k` are all known. No claim of novelty is available
on any of them.

## Branch budget

- **Target:** is there a finite state at a node that determines the whole
  depth-`r` subtree below it, smaller than the residue itself?
- **Novelty hypothesis:** the residual state carries more than the
  Taylor jet, and valuation data alone fixes the subtree.
- **Falsifier:** two nodes with equal valuation data and different
  subtrees; or the residual state turning out to be exactly the jet.
- **Existing machinery:** `bt.calculus` sections and residuals, the
  finite-horizon equivalence `≡_k`, the residual Mealy machine.
- **Maximum Phase-0 scope:** the 53-polynomial triage over words to
  depth 5 and levels to `k = 7`.
- **Promotion criterion:** a determinacy statement that is not a
  restatement of Hensel or Newton-polygon theory, or a complexity
  consequence.
- **Stop criterion:** everything reduces to known lifting theory, or
  state compression yields no complexity statement.

Both falsifiers fired: the residual state *is* the scaled Taylor jet,
and valuations do not determine the subtree (`x^2 ± 9`).

## Balanced-ternary formulation

A residue modulo `3^k` is a trit word `w = (a_0,…,a_{k-1})`, LSD-first,
with value `n_w = Σ a_i 3^i` ranging bijectively over
`[-(3^k-1)/2, (3^k-1)/2]`. A node carries the residual section state
`𝔇_w f ∈ ℤ[x]` and the output trits `ρ_0,…,ρ_{k-1}` emitted along `w`.

## Why BT may be relevant

The balanced digit set makes the partial output sum strictly smaller in
absolute value than the modulus, so divisibility of `f(n_w)` by `3^k`
becomes literal vanishing of every output trit rather than a congruence
on a digit range. That is what turns the lifting tree into an exact
sub-object of a machine the project already had.

## Candidate operations / invariants

- Zero-output subtree identification — **PROVED — LEAN**.
- Residual state as scaled Taylor jet — **PROVED**, and the
  **REPARAMETERIZATION** certificate for the whole translation.
- One-step trichotomy `0 / 1 / 3` for `k ≥ 1` — **PROVED — LEAN**,
  **KNOWN**.
- `Φ_r` determines the depth-`r` subtree — **PROVED**.
- Sharpness: `Φ_{r-1}` does not — **PROVED**.
- Deep linearization `𝔇_w f ≡_r f(n_w)/3^k + f'(n_w)x` for `k ≥ r` —
  **PROVED**.
- Deep minimal state: the two residues modulo `3^r` — **PROVED**.
- Valuation-only determinacy of the unordered deep shape —
  **VERIFIED COMPUTATIONALLY** for `r ≤ 4`, **OPEN** as a theorem.
- Valuation-only determinacy in general — **REFUTED**, with the smallest
  witness recorded.

Full statements and proofs:
[docs/theory/padic_lifting_trees.md](../theory/padic_lifting_trees.md).
Ledger rows: `BTL-*` in
[docs/theory/theorem_ledger.md](../theory/theorem_ledger.md).

## Experiments

`research.lifting.triage`, over the 53 polynomials of
`research.lifting.families`:

- `h1_identification` — output trits against divisibility against brute
  force, words to depth 5 and levels to `k = 7`;
- `h2_taylor_jet` — the scaled Taylor identity, words to depth 4;
- `h3_trichotomy` — child-count census at level `≥ 1`, plus the level-0
  census showing counts of 2 that the trichotomy forbids higher up;
- `phi_determinacy`, `phi_sharpness` — grouping by `Φ_r` and `Φ_{r-1}`;
- `valuation_determinacy`, `pair_determinacy` — by regime
  (`all`, `shallow`, `deep`);
- `linearization` — the deep congruence to the linear surrogate;
- `linear_state_determinacy` — exhaustive over linear states
  `|c| ≤ 121`, `|b| ≤ 40`;
- `state_census` — distinct `Φ_r` classes and distinct depth-`r`
  subtrees per level;
- `triage_report` — the whole payload plus the verdict.

CLI: `btprime congruence roots | lift | tree | classify | triage`.

## Conjectures

None registered. The one open statement — whether valuation data alone
determines the unordered deep-regime subtree — is recorded as OPEN in
the theory file rather than promoted to a conjecture, because the
supporting evidence is a bounded exhaustive check and a computational
observation is not a conjecture.

## Counterexamples

- Valuations do not determine lifting: the level-1 node `0` of `x^2 + 9`
  and of `x^2 - 9`. Identical `v_3(f)` and `v_3(f')`; six surviving
  grandchildren versus none. In
  `tests/unit/test_lifting.py::test_valuations_do_not_determine_the_subtree`.
- `Φ_{r-1}` insufficiency at `r = 2`: `x^2` against `x^2 - 3`. In
  `tests/unit/test_lifting.py::test_phi_r_minus_one_does_not_determine_depth_r_subtree`.
- The trichotomy fails at the root: `x^2 + x` has two children with a
  unit derivative. In
  `tests/unit/test_lifting.py::test_level_zero_escapes_the_trichotomy`.

## Formalization

`formal/BTCalculus/PadicLifting.lean`: iterated reconstruction, the
zero-output identification, reduction from level `k+1` to `k`, the lift
relation, nonsingular uniqueness, and the singular trichotomy. No
`sorry`, `admit`, or `axiom`.

## Results

Phase 0 verdict: **proceed**, on the strength of the identification
theorem, the sharp `Φ_r` determinacy, and the refutation of
valuation-only determinacy. The core translation is a
REPARAMETERIZATION and is labelled as one.

What was *not* obtained, and is not claimed:

- no improvement on known root counting or on effective lifting bounds;
- no complexity result — the state compression bounds the number of
  distinct depth-`r` subtrees independently of `k`, which is structure,
  not a speedup over `poly(deg f, k log 3)`;
- no new theorem about singular `p`-adic root finding;
- nothing about multivariate systems.

## Minimal-state phase

Phase 0 asked whether `Φ_r` suffices. It does. The follow-up asks
whether it is *minimal*: is the `Φ_r`-class the smallest local datum
that determines the next `r` lifting levels?

### Triage

```text
Mathematical target        the exact minimal finite state for r-step lifting, and how far below Φ_r it sits
Novelty hypothesis         L_r = Σ_{j≤r} 3^j + r is the exact deep-regime state complexity, refined to 3^{r-e} + e by v_3(f')
Falsifier                  the closed form fails at r = 6, or the quotient is a standard classical object, or no family attains L_r
Existing machinery         depth_r_shape(mode="digits") is the behavioural invariant; myhill_nerode has finite-horizon minimisation
Maximum scope              three theorems plus verification to r = 6; no CLI, explorer, or Lean until they land
Promotion criterion        all three proved, count attained by an explicit family, quotient not a standard object
Stop criterion             no proof beyond exhaustion, or the quotient is classical, forcing CLOSE as REPARAMETERIZATION
```

### Settled before implementation

Three facts were established by computation and short proof *before*
any module was written, and they redirected the phase:

- **`Φ_r` is not minimal.** On a surviving branch `ρ_a(g) = 0`, so
  `𝔇_a(λg) = λ 𝔇_a g` and survival is unchanged for `λ` coprime to 3.
  The whole ordered depth-`r` subtree is therefore invariant under
  `g ↦ λg` while `Φ_r` is not. Verified on 52 800 state/scalar/horizon
  combinations with zero failures; `Φ_r` differed in 40 121 of them.
- **The two-residue deep state is not minimal either.** For linear
  states `Φ_r` *is* the pair `(c, b)` modulo `3^r`, so the candidate
  "deep-regime minimal-state theorem" `S_r(A) = S_r(B) ⟺ A ∼_r B` is
  false. The behavioural counts are `5, 15, 43, 125, 369` for
  `r = 1,…,5` against `3^{2r} = 9, 81, 729, 6561, 59049`.
- **The exact deep count.** `L_r = (3^{r+1}-1)/2 + r = Σ_{j≤r} 3^j + r`,
  refining to `3^{r-e} + e` behaviours at `e = min(v_3(f'(n)), r)`. The
  unit-scaling quotient alone gives `2·3^r - 1 = 5, 17, 53, 161`, which
  is strictly larger from `r = 2`, so scaling is a proper intermediate
  quotient and not the whole answer.

The nonsingular half is Newton's method in balanced digits: the
behaviour depends only on `u = (f(n)/3^k)/f'(n) mod 3^r`, the surviving
path is the balanced expansion of `-u`, and the transition is `u ↦ 𝔇(u)`
emitting `-ρ(u)`. That identification is a `REPARAMETERIZATION`; the
count around it is exact.

### Interim outcome, superseded

The phase first parked with one gap: the general row `3^{r-e} + e` for
`1 < e < r` rested on exhaustion to `r = 6`, missing injectivity of
`d mod 3^{r-e} ↦ (B_{r-e}(d+s))_s`. That gap was an artefact of an
arithmetic error of ours, recorded here because the error is instructive.

### The shifted family, settled

The shift a word applies inside a ternary block is the **balanced value**
`packWord(w)`, not the digit sum: the constant after `j` steps is
`3^{e-j}(d + a_1 + 3a_2 + … + 3^{j-1}a_j)`. The earlier draft recorded the
digit sum, which shrinks the shift window from `3^e` values to the `2e+1`
values `|s| ≤ e`. That is the whole difficulty: with the digit sum the
separation is genuinely **false** — at `e = 2` every `d ≡ 3` and `d ≡ 6`
modulo 9 gives the same tuple `(∅,∅,T_1,∅,∅)` — whereas the true window is
a complete residue system modulo `3^e`, so exactly one leaf of each block
continues, and the induction on the horizon closes in a page.

With that fixed:

- **Separation holds** for every `e ≥ 1` and every `R ≥ 0`, by induction on
  `R` (`BTL-shift-separation`).
- **The rows are exact**: `3^{r-e} + e`, so `L_r = (3^{r+1}-1)/2 + r` is
  proved, not merely verified (`BTL-state-count`).
- **The minimal state has a normal form.** Scale `b` to `3^e`. Where the
  constant dominates, `v_3(c) < e`, the behaviour is the truncated tree
  `T_{v_3(c)}` and depends on `v_3(c)` alone: `r` classes. Everywhere else
  it is exactly the unit-scaling orbit, no further collapse:
  `(3^{r+1}-1)/2` classes (`BTL-minimal-normal-form`).

### Outcome

**CLOSE — REPARAMETERIZATION.** All four plan targets are proved and the
count is attained, so the PARK criterion is gone; but the promotion
criterion required the quotient *not* to be a standard classical object,
and the normal form shows it is one. "The unit-scaling orbit, degenerated
to `v_3(c)` where the constant dominates" is Newton-polygon dominance plus
Hensel rigidity in residual coordinates. The `3^{r-e} + e` rows and the
`C(r,2)` overlap are arithmetic bookkeeping over that description. The
exact count is new as a number; the object it counts is not new as an
object.

What survives as platform machinery: the block shift law (Lean), the
separation theorem, the normal form and `minimal_state_key`, and the
correction of our own earlier sufficiency-as-minimality claim.

Full statements: [docs/theory/lifting_state_complexity.md](../theory/lifting_state_complexity.md).
Experiments: `research.lifting.state_complexity`.

## Open questions

- Is deep-regime valuation determinacy of the unordered shape a theorem?
- Does the local determinacy horizon give anything the global bound
  `k0 = O(d²(log C + log d))` does not?
- Is there a class of `f` where the `Φ_r` state count is small enough to
  matter, as opposed to merely bounded?
- What is the minimal state in the shallow regime `k < r`, where the
  higher jet coefficients survive and the state space is unbounded in
  degree?

Answered and retired: whether `Φ_r` is minimal (no), the exact deep count
(`L_r`, proved), and whether the shifted family separates residues (yes).

## Decision

`PARK` for the dossier as a whole, with the multivariate and minimal-state
sub-branches `CLOSE`d. The identification theorem and the sharp `Φ_r`
determinacy are exact and Lean-backed, so the line is not dead, but the
core translation is a **REPARAMETERIZATION** of known lifting theory and
the one `PROJECT-SPECIFIC` ingredient — sharp finite-horizon determinacy —
has no known consequence. The minimal-state sub-branch closes for the same
reason, now demonstrated rather than suspected: its normal form is
Newton-polygon dominance plus Hensel rigidity. Multivariate systems stay
closed: `dwivedi-saxena-2024-systems-non-fields` already covers `n + k`
constant, and there is no univariate theorem here strong enough to
justify a general solver. Do not open a numbered milestone for this line.

Best next question: is deep-regime valuation determinacy of the
unordered subtree shape a theorem?

## Publication assessment

Status: `EXPLORATORY`.

Not a `PAPER_CANDIDATE`. The exact statements are either classical or
reparameterizations of classical statements, and the one genuinely new
ingredient — the sharp finite-horizon determinacy of the subtree — is a
local refinement whose consequences are unknown. The multivariate phase
stays closed: `dwivedi-saxena-2024-systems-non-fields` already handles
`n + k` constant and identifies the obstruction, and this project has no
univariate theorem strong enough to justify a general solver.
