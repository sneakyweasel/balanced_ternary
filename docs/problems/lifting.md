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

## Open questions

- Is deep-regime valuation determinacy of the unordered shape a theorem?
- Does the local determinacy horizon give anything the global bound
  `k0 = O(d²(log C + log d))` does not?
- Is there a class of `f` where the `Φ_r` state count is small enough to
  matter, as opposed to merely bounded?

## Decision

`PARK`, with the multivariate sub-branch `CLOSE`d. The identification
theorem and the sharp `Φ_r` determinacy are exact and Lean-backed, so
the line is not dead, but the core translation is a
**REPARAMETERIZATION** of known lifting theory and the one
`PROJECT-SPECIFIC` ingredient — sharp finite-horizon determinacy — has
no known consequence. Multivariate systems stay closed:
`dwivedi-saxena-2024-systems-non-fields` already covers `n + k`
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
