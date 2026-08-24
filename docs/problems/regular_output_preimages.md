# Regular-output preimages of nonlinear 3-adic polynomials

## Problem

Whether a regular output constraint can force the input preimage of a
nonlinear polynomial residual system to be sofic, even though the
unrestricted transducer is infinite-state.

## Exact statement

Let `F(x) = x^2 ∈ Z[x]` and let `Y = {0,+}^ω` be the infinite output
language that never emits `-1`. Write `X = F^{-1}(Y)` for the set of
3-adic inputs whose residual output word lies in `Y`. Equivalently, on
finite words, `L` is the language of trit words `w` such that every
output trit of the residual machine of `x^2` along `w` lies in `{0,+}`.

Question: is `L` regular (equivalently, is `X` sofic)?

## Current literature

- `ahmed-savchuk-2020-polynomial-tree-endomorphisms`: an integer
  polynomial induces a finite-state rooted-tree endomorphism if and
  only if it is linear. Unrestricted `x^2` is infinite-state. `KNOWN`.
  Infinite-state does not, by itself, name a regular output language
  whose preimage is non-regular.
- `anashin-2012-automata-finiteness`,
  `grigorchuk-savchuk-2023-solenoidal-maps`: finite-Mealy criteria for
  1-Lipschitz maps. `KNOWN`.
- Zero-output preimages are the lifting tree
  (`docs/problems/lifting.md`, `BTL-zero-output`). That language is a
  proper subset of `L` and is not the target.

## Branch budget

```text
Mathematical target     For F(x)=x² and the infinite regular output constraint Y={0,+}^ω, is X=F⁻¹(Y) a sofic input language despite F having infinitely many polynomial sections?
Novelty hypothesis      A regular output restriction may close a finite residual subsystem even though the unrestricted nonlinear transducer is infinite-state.
Falsifier               The reachable constrained residual types grow with an explicit infinite distinguishing family, or any finite closure is only a fixed-depth/zero-output artifact.
Existing machinery      residual rho/delta/output_along, IntPoly sections, exact finite-horizon equivalence, generic DFA concepts, Ahmed–Savchuk finite-state boundary.
Maximum Phase-0 scope   One nonlinear map x², one safety language forbidding output −, linear control x, exact depths m,r≤7, one dossier/module/test set.
Promotion criterion     A proved finite constrained quotient/sofic presentation, or a proved infinite distinguishing family showing non-regularity for this exact pair.
Stop criterion          Bounded counts only, manufactured countdown states, reduction to zero-output lifting, or a direct restatement of known nonlinear infinite-state theory.
```

## Balanced-ternary formulation

The residual machine `F --[a / ρ_a(F)]--> 𝔇_a F` is producted with the
two-state safety automaton that dies on output `-1`. A word is in `L`
when every output trit stays in `{0,+}`.

The residual of `x^2` along the live prefix `(1, 0^m)` is

`g_m(x) = 3^{m+1} x^2 + 2x`.

## Why BT may be relevant

Balanced digits are the native output alphabet. The packing identity
`pack((-1)^k) = -(3^k-1)/2` and the expansion `1-3^k = (+, 0^{k-1}, -)`
make the distinguishing words exact rather than sampled.

## Candidate operations / invariants

- Safety product `(g, q)` — Phase-0 object.
- Remaining-horizon acceptance signatures — exact right languages.
- Census `C(m,r)` — types at input depth `m` and horizon `r`.
  **COMPUTATIONALLY VERIFIED** through `m,r ≤ 7`.
- Family `g_m` with words `w_m = (-1)^{m+1} 0` — **EXACT — HUMAN PROOF** infinite
  Myhill–Nerode family.
- Zero-output subtree — proper subset, not the target.

## Experiments

`research.regular_output_preimages.triage` with `m,r ≤ 7`, polynomials
`x` and `x^2`, and the family `g_m`. Tests live in
`tests/research/regular_output_preimages/test_triage.py`.

## Conjectures

`x2_safety_nonsific` (**EXACT — HUMAN PROOF**): ledger
`BTR-x2-safety-nonsific`.

## Counterexamples

1. **The safety language is not the lifting language.** The words
   `(+)` and `(−)` are safe for `x^2` (first outputs are `+`) and are
   not all-zero. Witness in `zero_output_is_proper_subset`.
2. **The novelty hypothesis is false for this pair.** The prefixes
   `10^m` are pairwise distinguishable, so no finite constrained
   quotient exists for `Y = {0,+}^ω`.

## Formalization

Master record: [regular_output_preimages.md](../theory/regular_output_preimages.md).
Ledger row `BTR-x2-safety-nonsific`. Lean is deferred. No `sorry`.

## Results

### Linear control

`F(x)=x` has a single live residual. `C(m,r)=1` for every tested
`m,r`. The preimage is `{0,+}^*`, which is regular. This is the
Ahmed–Savchuk linear case and is `KNOWN`.

### Census for `x^2`

Horizon-7 type counts of live residuals at depths `0..7`:

`1, 3, 7, 16, 33, 66, 131, 260`.

The two-parameter table `C(m,r)` is nondecreasing in both arguments
and is not a remaining-horizon clock: the identity map stays at `1`.

### Non-regularity theorem

**EXACT — HUMAN PROOF** (`BTR-x2-safety-nonsific`). For `m ≥ 0` let `g_m(x) = 3^{m+1} x^2 + 2x`
and `w_m = (-1)^{m+1} 0`. Then `w_m` is accepted by `g_m` and
rejected by every `g_n` with `n > m`. Consequently the prefixes
`10^m` are pairwise Myhill–Nerode inequivalent in `L`, so `L` is not
regular and `X` is not sofic.

*Proof.* Write `p_k = pack((-1)^k) = -(3^k-1)/2`. Then
`g_m(p_k) = 2 p_k + 3^{m+1} p_k^2 = (1-3^k) + 3^{m+1} p_k^2`.
The first `k` balanced digits of `1-3^k` are `(+, 0^{k-1})`. The
correction `3^{m+1} p_k^2` has valuation `m+1`, so it does not
affect those `k` digits whenever `k ≤ m+1`. Thus every prefix
`(-1)^k` with `k ≤ m+1` is safe for `g_m`. The next digit is
`[D^k(g_m(p_k))]_3`. For `k ≤ m` one has
`D^k(g_m(p_k)) = -1 + 3^{m+1-k} p_k^2 ≡ -1 (mod 3)`, so the letter
`0` is forbidden. For `k = m+1` one has
`D^{m+1}(g_m(p_k)) = -1 + p_k^2` and `p_k ≡ -1 (mod 3)`, hence
`p_k^2 ≡ 1 (mod 3)` and the residue is `0`, so `0` is allowed.
Therefore `g_m` accepts `w_m`. For `n > m` the same word is a
prefix `(-1)^{m+1}` of a safe path for `g_n` (because `m+1 ≤ n`),
after which the residue is `-1` and `0` is forbidden. ∎

The argument is not a restatement of “nonlinear ⇒ infinite-state”.
It names one regular output language and one explicit packing
witness.

### Literature classification

- `KNOWN`: unrestricted `x^2` is infinite-state; the identity is
  finite-state; lifting equals the zero-output subtree.
- `REPARAMETERIZATION`: none of the surviving statements.
- `PROJECT-SPECIFIC`: the pair `(x^2, {0,+}^ω)` is not sofic, via
  the family `10^m` / `w_m`.
- `OPEN`: none retained.

## Open questions

None retained on this branch. In particular, other output languages
are not opened automatically.

PENDING IDEA — NOT OPENED (not a decision, not a claim tag):

- exact laws for the two-parameter full residual complexity `C_F(m,r)`
  of unrestricted (not safety-constrained) residuals;
- section entropy versus dynamical entropy;
- solenoid / adelic packaging and bi-infinite words.

## Decision

`PROMOTE`. The novelty hypothesis is false for this pair, and the
falsifier is a theorem: an explicit infinite Myhill–Nerode family
shows that `F^{-1}({0,+}^ω)` is not sofic. That is the promotion
criterion. The result is not a restatement of Ahmed–Savchuk, not a
zero-output lifting fact, and not a bounded census. Ledger row
`BTR-x2-safety-nonsific` records the surviving theorem. No CLI, Lean,
or numbered milestone is added.

Best next question: none on this branch; the gate is closed by a
theorem.

## Publication assessment

Status: `STRUCTURAL`.

The non-regularity proof is exact and short. It is a gate theorem
for one pair, not a paper-scale classification of output languages.
