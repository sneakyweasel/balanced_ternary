# Transition-closed residual quotients for Černý-type automata

## Problem

Whether the laboratory's residual polynomials admit a natural finite
transition-closed quotient that could later support a Černý-type
synchronization analysis. The Černý conjecture itself is not the
Phase-0 target.

## Exact statement

Let `f ∈ Z[x]` and write `D_a` for the balanced-ternary section
derivative. The raw residual closure is

`Cl(f) = { D_w f : w ∈ {-1,0,+1}^* }`.

Finite-horizon residual equivalence `≡_r` is the existing Myhill–Nerode
relation: `p ≡_0 q` always, and `p ≡_{r+1} q` if and only if
`ρ_a(p) = ρ_a(q)` and `D_a p ≡_r D_a q` for every trit `a`.

This relation is not generally a transition congruence. The coarsest
transition congruence contained in `≡_r` is

`p ≈_r q  ⇔  ∀ u ∈ {-1,0,+1}^*,  D_u p ≡_r D_u q`.

Question: for any interesting family of polynomials, is `Cl(f)/≈` finite
for a natural transition-closed `≈` that preserves residual output
behaviour?

## Current literature

The Černý conjecture remains open. The best general reset-threshold
upper bound is still cubic
(`volkov` survey status through 2026; Shitov
`≈ 0.1654 n^3 + o(n^3)`). Many structured classes have quadratic or
linear bounds. These facts are `KNOWN` background and were not
re-opened: no reset word is computed in this phase.

Polynomial residual systems are already classified as rooted-tree
endomorphisms.

- `ahmed-savchuk-2020-polynomial-tree-endomorphisms`: every
  `f ∈ Z[x]` induces an endomorphism of the `d`-ary rooted tree; sections
  remain polynomials of the same degree; the endomorphism is finite-state
  if and only if `f` is linear (Proposition 3.4). Distinct polynomials
  induce distinct endomorphisms (Proposition 3.1). For `d = 3` this is
  the classification of residual closures. `KNOWN`.
- `anashin-2012-automata-finiteness`: a 1-Lipschitz map on `Z_p` is
  finite-state if and only if its reduced van der Put coefficients form
  a `p`-automatic sequence of eventually periodic values. `KNOWN`.
- `grigorchuk-savchuk-2023-solenoidal-maps`: the same criterion for
  arbitrary `d`, with explicit Mealy/Moore conversion. `KNOWN`.
- Balanced digits in place of `{0,1,2}` are a `REPARAMETERIZATION` of
  the alphabet.

No source located in the gate states this project's `≈_r` notation.
New notation for the coarsest transition congruence inside a known
horizon relation is not evidence of novelty.

## Branch budget

```text
Mathematical target     Classify when the full residual closure of f in Z[x] has a natural finite transition-closed quotient preserving residual output behaviour.
Novelty hypothesis      A non-affine arithmetic family may admit a canonical finite congruence stricter than horizon truncation but coarser than raw equality.
Falsifier               The coarsest transition congruence preserving any positive finite-horizon behaviour is raw equality, while nonlinear polynomials have infinitely many distinct sections.
Existing machinery      IntPoly.rho/section_deriv, residual delta/output_along, exact ≡r signatures, distinguishing words, and existing rooted-tree/finite-state literature records.
Maximum Phase-0 scope   One congruence theorem, one polynomial finiteness classification, minimal exact witnesses for constant/affine/quadratic/cubic examples, and the dossier decision.
Promotion criterion     A canonical finite quotient for a genuinely non-affine family, with a proved transition law and a distinction from known finite-state rooted-tree results.
Stop criterion          Only affine finite-state sections survive, or every nonlinear finite quotient requires horizon/depth truncation or identifies behaviourally distinguishable states.
```

## Balanced-ternary formulation

The residual machine is the existing Mealy law

`f  --[a / ρ_a(f)]-->  D_a f`,    `a ∈ {-1,0,+1}`.

Three candidate state notions were compared and kept distinct:

1. raw residual equality of polynomials in `Z[x]`;
2. finite-horizon `≡_r`;
3. full Mealy/output semantic equivalence, i.e. equal output words on
   every finite trit word.

The relation `≈_r` is the coarsest transition congruence contained in
`≡_r`. For `r = 0` it is the universal relation. For `r ≥ 1` it is
semantic equivalence: after every prefix the next `r` outputs agree, so
all output words agree. Distinct polynomials in `Z[x]` are distinct
functions, and distinct polynomials induce distinct tree endomorphisms,
so semantic equivalence is raw equality.

A remaining-horizon clock `( [p]_r , r )` was excluded. It manufactures
a finite DFA by consuming the horizon rather than quotienting residual
states.

## Why BT may be relevant

The laboratory already has exact residual transitions and exact
`≡_r`. That makes the congruence and finiteness questions inexpensive
and canonical. Balanced ternary does not add a new finite-state
criterion: the linear/nonlinear dichotomy is classical for any base
`d ≥ 2`.

## Candidate operations / invariants

- Raw residual closure `Cl(f)` — `KNOWN` as the set of rooted-tree
  sections.
- Finite-horizon `≡_r` — `KNOWN` (existing Myhill–Nerode relation). It
  is not a transition congruence.
- `≈_r`, the coarsest transition congruence contained in `≡_r` —
  `REPARAMETERIZATION` of full Mealy equivalence for `r ≥ 1`.
- Semantic / output equivalence — `KNOWN`; on `Z[x]` it coincides with
  raw equality.
- Affine intercept bound `|c| ≤ max(|b|, |c_0|)` for residuals of
  `bx + c` — `KNOWN` (Ahmed–Savchuk linear case; slope invariant,
  intercept the balanced quotient of `c + a b`).
- Leading coefficient `LC(D_w f) = 3^{|w|(deg f - 1)} LC(f)` —
  `KNOWN` / already recorded in the section calculus. For
  `deg f ≥ 2` this is an infinite family of distinct polynomials.
- Clocked remaining-horizon automata — `PROJECT-SPECIFIC`
  implementation artefact, rejected as a candidate quotient.
- Reset words, ranks, pair compression, Černý bounds — not computed.

## Experiments

`research.cerny_bt.triage` implements only the quotient gate:

- exact affine residual closures by the intercept recurrence
  `c ↦ (c + a b - [c + a b]_3)/3`;
- a proved intercept bound, used as a termination certificate;
- the leading-coefficient formula versus observed residuals along
  concrete words;
- the smallest `≡_1` pair that fails to be transition-stable;
- a bounded sample check that `≈_r` agrees with raw equality on
  affine closures.

Affine corpus:

`0`, `1`, `-1`, `2`, `x`, `x+1`, `x-1`, `2x+1`, `2x-1`, `-x`,
`3x+1`, `-2x+1`.

Nonlinear corpus: `x^2`, `x^3`, `2x^2+1`.

Exact affine state counts: `x` and `-x` have one residual; `x±1` have
two; `2x±1`, `3x+1`, and `-2x+1` have three. Constants shrink by
balanced division and are finite. Nonlinear leading coefficients at
depths `0,1,2,3` are pairwise distinct and match the formula. These
are finite exact checks of proved identities, not extrapolated
formulas.

No CLI, visualization, Lean module, or reusable `bt.*`
synchronization API was added.

## Conjectures

None registered. The classification is classical.

## Counterexamples

1. **`≡_r` is not a transition congruence.** The pair `x` and `x+3`
   satisfies `x ≡_1 x+3` because both emit the input trit. For every
   letter `a`,    `D_a x = x` and `D_a(x+3) = x+1`, and `x ≢_1 x+1`.
   They agree on every length-1 word and first differ on `(-1,-1)`.
   Hence `x ≈_1 x+3` fails already on prefixes of length 1.

2. **Nonlinear residual closures are infinite.** For `f(x) = x^2`,
   `LC(D_w f) = 3^{|w|}`. Depths `0,1,2,3` give leading coefficients
   `1,3,9,27`. For `x^3` they are `1,9,81,729`. Any transition-closed
   quotient that retains these polynomials as distinct states is
   infinite. Identifying them requires either a horizon/depth clock or
   a collapse of behaviourally distinguishable states.

3. **The coarsest behaviour-preserving transition congruence is raw
   equality.** On every affine closure in the corpus, the bounded
   `≈_1` and `≈_2` checks agree with polynomial equality. Combined
   with Ahmed–Savchuk Proposition 3.1 this is the expected global
   statement, not a new quotient.

The witnesses are regression-tested in
`tests/research/cerny_bt/test_triage.py`.

## Formalization

None. No `sorry`. Lean is not opened on a closed literature-and-quotient
gate.

## Results

### Congruence

For `r ≥ 1`, `≈_r` is full Mealy equivalence. On `Z[x]` that is raw
polynomial equality. Finite-horizon `≡_r` is strictly coarser and is
not transition-stable. The remaining-horizon clock is a different
object and was not used.

### Finiteness

`Cl(f)` is finite if and only if `deg f ≤ 1`. Constants terminate by
balanced division. For `f(x) = b x + c` the slope is invariant and
every intercept stays inside `|c| ≤ max(|b|, |c|)`. For `deg f ≥ 2`
the leading coefficients `3^{m(deg f - 1)} LC(f)` are unbounded.

### Literature classification

- `KNOWN`: Černý background; polynomial tree endomorphisms; linear
  iff finite-state; Anashin / Grigorchuk–Savchuk finite-Mealy
  criteria; leading-coefficient growth; affine intercept contraction.
- `REPARAMETERIZATION`: balanced digits; `≈_r` as Mealy equality;
  the affine residual automata as the linear finite-state case of
  Ahmed–Savchuk.
- `PROJECT-SPECIFIC`: the exact affine census, the `x` versus `x+3`
  non-congruence witness, and the explicit refusal of clocked DFAs.
- `OPEN`: none promoted. Synchronization questions are not opened,
  because no canonical finite non-affine quotient exists.

### Gate verdict

`CLOSE`

Affine residual automata are the known finite-state linear family.
Every faithful nonlinear closure is infinite. Every finite nonlinear
model in this laboratory is a horizon or depth truncation. That is
exactly the stop criterion.

## Open questions

None retained on this branch. In particular, reset thresholds of the
affine family are ordinary finite-DFA computations on a class already
known to be finite-state, and do not reopen the branch.

## Decision

`CLOSE — REPARAMETERIZATION`. The primary gate was the existence of a
natural finite transition-closed quotient. For affine polynomials the
quotient is the raw residual closure, already classified as
finite-state linear tree endomorphisms. For every nonlinear polynomial
the behaviour-preserving transition congruence is raw equality and the
closure is infinite. Clocked remaining-horizon automata were excluded
by the gate. No Černý-type analysis is justified.

Best next question: none; the branch is not promoted.

## Publication assessment

Status: `ARCHIVED`.

The branch records a precise negative gate and reusable witnesses, but
contains no new theorem beyond the classical linear/nonlinear
finite-state dichotomy.
