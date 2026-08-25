# Balanced-Monna endpoint preservation and jump-depth spectra

## Problem

Whether balanced-Monna endpoint pairs of `x^3` have a closed arithmetic
divergence-depth law, and which maps preserve Monna equivalence.

## Exact statement

The balanced Monna map is

`B(∑_{i≥0} a_i 3^i) = ∑_{i≥0} a_i 3^{-i-1}`, `a_i ∈ {-1,0,+1}`.

Two 3-adic integers form an *endpoint pair* when they have a common
finite prefix, one boundary digit, and opposite infinite tails, so
that `B(u)=B(v)` with `u ≠ v`. In values this is
`u = ζ + 2·3^n`, `v = ζ − 2·3^n`, hence `u − v = 4·3^n`.

For `F(x)=x^3`, decide whether `B(F(u))=B(F(v))` and compute
`t = v_3(F(u)−F(v))`. Keep that depth separate from the Euclidean
jump `|B(F(u))−B(F(v))|`.

## Current literature

- `monna-1952-digit-reversal`: the classical digit-reversal map.
  The balanced form is an affine conjugate. `KNOWN`.
- Real plots of automata / 1-Lipschitz maps after Monna transport
  are `KNOWN`. Discontinuity at ambiguous expansions is the generic
  phenomenon.
- Residual graph recursion
  `Γ_F = ∪_a S_{a,ρ_a(F)}(Γ_{𝔇_a F})` is a `REPARAMETERIZATION` of
  the residual Mealy machine.
- This branch does not reopen `M_k(x^3)` counting
  (`docs/problems/residuals.md`).
- Collatz 3-adic endpoints and `bt_reverse` are different objects
  and are not used.

## Branch budget

```text
Mathematical target     For F(x)=x³, classify balanced-Monna endpoint pairs, determine whether F preserves their equivalence, and derive the exact output divergence-depth spectrum.
Novelty hypothesis      Endpoint midpoint valuations may produce a closed arithmetic spectrum beyond the generic fact that Monna transport can be discontinuous.
Falsifier               The spectrum is already a standard Monna real-plot theorem, collapses to one generic depth, or is only residual congruence in different notation.
Existing machinery      balanced residues, IntPoly evaluation, v₃, residual output words, cubic algebra, exact rational arithmetic.
Maximum Phase-0 scope   Endpoint normal form, x³ plus affine controls, exact census through n≤5, one literature record, one dossier/module/test set.
Promotion criterion     A literature-separated preservation classification or closed jump-depth distribution with an exact proof.
Stop criterion          Coordinate restatement, finite table without a law, or any return to the closed M_k(x³) counting problem.
```

## Balanced-ternary formulation

Kind `plus` after a prefix of length `n`: tails `(+, −−−…)` versus
`(0, +++…)`. Kind `minus`: tails `(0, −−−…)` versus `(−, +++…)`.
These are the only real collisions of `B`: a first-digit difference
of `±1` with an opposite infinite tail of difference `∓2`.

`B` and all 3-adic values are computed in `fractions.Fraction`.
No floating point is used.

## Why BT may be relevant

The polar alphabet makes the two tails digitwise negations, and the
cubic difference factors through the midpoint `ζ = (u+v)/2` in the
balanced window.

## Candidate operations / invariants

- Endpoint preservation: `B(F(u))=B(F(v))`.
- p-adic divergence depth: `t = v_3(F(u)−F(v))`.
- Euclidean jump: `|B(F(u))−B(F(v))|`, zero iff preservation.
- Endpoint normal form of the image pair `(F(u),F(v))` — strictly
  stronger than a valuation match.

## Experiments

`research.monna_endpoint_spectra.triage` enumerates every prefix and
both kinds through `n ≤ 5` (728 pairs), plus the controls `x`, `-x`,
`0`, `1`, `x+1`, `2x+1`. Tests live in
`tests/research/monna_endpoint_spectra/test_triage.py`.

## Conjectures

None registered.

## Counterexamples

1. **`x^3` preserves no endpoint pair** through `n ≤ 5`, and the
   algebraic identity shows `u^3 ≠ v^3` for every pair, so there is
   no hidden infinite-precision collision.
2. **`2x+1` preserves no pair.** The difference becomes `8·3^n`,
   which is not of the form `±4·3^k`.
3. **`x+1` fails exactly on kind `plus` with the all-`+` prefix**,
   including the empty prefix at `n=0`. That is the carry-through
   of `+1` into the boundary. All other pairs through `n ≤ 5` are
   preserved.

## Formalization

Master record: [monna_endpoint_spectra.md](../theory/monna_endpoint_spectra.md).
Ledger rows `BTM-balanced-monna`, `BTM-x3-depth`, `BTM-x3-spectrum`,
`BTM-x3-no-preserve`. `BTM-x3-depth` is `formal/BTCalculus/MonnaEndpointCube.lean`.
Spectrum and non-preservation remain human. No `sorry`.

## Results

Canonical statements: [monna_endpoint_spectra.md](../theory/monna_endpoint_spectra.md)
and the four `BTM-*` ledger rows.

### Normal form

**EXACT — HUMAN PROOF.** The two infinite expansions of a balanced
triadic real are exactly the pairs constructed above, and
`u − v = 4·3^n`. Verified on every pair through `n ≤ 5`.

`B` itself, and the graph recursion of `Γ_F`, remain `KNOWN` /
`REPARAMETERIZATION` (`BTM-balanced-monna`).

### Cubic identities

**EXACT — LEAN VERIFIED** (`BTM-x3-depth`). For every endpoint pair,

`u^3 − v^3 = 4·3^n (3ζ^2 + 4·3^{2n})`,

and therefore

`t = v_3(u^3 − v^3) = n + min(1 + 2 v_3(ζ), 2n)`,

or `t = 3n` when `ζ = 0`. The two arguments of the minimum have
opposite parity whenever `ζ ≠ 0`, so there is never a cancellation
tie. Verified on all 728 pairs through `n ≤ 5` (`formula_fails = 0`,
`depth_mismatches = 0`).

The Euclidean jump of `x^3` is nonzero on every pair. The image
pair `(u^3, v^3)` is never itself an endpoint pair
(`BTM-x3-no-preserve`). Valuation agreement with the formula is
not preservation.

### Closed spectrum

**EXACT — HUMAN PROOF** (`BTM-x3-spectrum`). At level `n = 0` both kinds have depth `0`.
For `n ≥ 1`:

- depth `3n` occurs twice (the zero prefix, both kinds);
- depth `n+1+2s` occurs `4 · 3^{n-s-1}` times for each
  `0 ≤ s < n` (exact midpoint valuation `s`, two signs, two kinds).

This matches the enumeration through `n ≤ 5`.

### Affine controls

- `x`, `-x`, and constants preserve every pair (`KNOWN` polarity /
  constancy).
- `x+1` preserves every pair except kind `plus` with prefix `+^n`.
- `2x+1` preserves none.

### Literature classification

- `KNOWN`: Monna map; endpoint ambiguity of radix-3 series; real
  plots of 1-Lipschitz maps; polarity of `-x`.
- `REPARAMETERIZATION`: balanced digits as an affine conjugate of
  Monna's `{0,…,p-1}` map; `Γ_F` as the residual machine.
- `PROJECT-SPECIFIC`: the cubic valuation law, the closed spectrum,
  the exact `x+1` carry exception, and the proof that `x^3` never
  preserves an endpoint pair.
- `OPEN`: none retained.

## Open questions

None retained on this branch. In particular, `M_k(x^3)` is not
reopened.

PENDING IDEA — NOT OPENED (not a decision, not a claim tag):

- exact laws for the two-parameter full residual complexity `C_F(m,r)`;
- section entropy versus dynamical entropy;
- solenoid / adelic packaging and bi-infinite words.

## Decision

`PROMOTE`. The cubic divergence-depth law and its spectrum are exact,
not a generic “nonlinear maps jump” slogan and not a finite table
without a formula. Preservation is classified for the stated controls.
The Monna map itself is not claimed as new. Ledger rows
`BTM-balanced-monna`, `BTM-x3-depth`, `BTM-x3-spectrum`, and
`BTM-x3-no-preserve` record the surviving theorems. No CLI, Lean,
cubic-count module, or numbered milestone is added.

Best next question: none on this branch; the gate is closed by a
theorem.

## Publication assessment

Status: `STRUCTURAL`.

The identities are short and exact. They are a coordinate theorem
about one polynomial on endpoint fibres, not a new 3-adic calculus.
