# 3-adic polynomial cycle dynamics

## Problem

Whether finite-resolution residual states provide a genuinely new
description or compression of polynomial iteration over `Z_3`, beyond
classical return maps, multipliers, Taylor data, and cycle lifting.

## Exact statement

Let `f ∈ Z[x]`, let `C` be a cycle of exact length `q` modulo `3^k`,
and let `r ≥ 1`. A child of `C` is a cycle modulo `3^(k+1)` whose
reduction has primitive cycle `C`. The depth-`r` cycle-lift tree retains
the multiplicity of children and labels each edge by the ratio of child
period to parent period.

For two such cycle states, write

`C ≡dyn_r C'`

when their rooted, period-labelled cycle-lift trees are isomorphic
through depth `r`. The question is whether the quotient by `≡dyn_r`
has an exact description or consequence not already supplied by the
classical local return map `g = f^q`.

## Current literature

The classical baseline is `KNOWN`.

- `desjardins-zieve-2001-polynomial-mappings` constructs and studies
  cycle lifts across `p^n`; the cycle-lift tree itself is not new.
- `fan-liao-2011-minimal-decomposition` uses
  `a_k = g'(x)` and `b_k = (g(x)-x)/3^k`. The affine map
  `t ↦ b_k + a_k t (mod 3)` gives growing, splitting, growing-tail, and
  partial-splitting cycles. Valuations of `a_k-1` and `b_k` control later
  splitting, including the low-level exception at `p=3`.
- `pezda-1994-polynomial-cycles` gives the possible periods of periodic
  orbits over `Z_3`: `1, 2, 3, 4, 6, 9`.
- `morton-silverman-1995-periodic-points` supplies the periodic-point,
  multiplicity, and multiplier setting for roots of `f^q(x)-x`.
- `poonen-2014-padic-interpolation` gives analytic interpolation of
  sufficiently identity-like iterates.
- `anashin-2012-automata-finiteness`,
  `ahmed-savchuk-2020-polynomial-tree-endomorphisms`, and
  `grigorchuk-savchuk-2023-solenoidal-maps` cover digit transducers,
  rooted-tree sections, and finite-state criteria. Nonlinear polynomial
  section systems are generally infinite even though each bounded
  quotient is finite.

Myhill--Nerode minimization, finite-depth tree equivalence, and bounded
partition refinement are also `KNOWN` abstract constructions. No source
located in the gate states this project's exact `D_r(f,k)` notation, but
new notation for a standard bounded quotient is not evidence of novelty.

## Branch budget

- **Target:** determine whether the minimal depth-`r` cycle-lift
  behaviour contains a theorem-level quotient not determined by
  classical return-map data.
- **Novelty hypothesis:** a strict residual compression or missing
  invariant might survive the classical baseline.
- **Falsifier:** the residual is the classical truncated return function
  and its minimization is ordinary bounded tree equivalence.
- **Existing machinery:** exact integer polynomials, balanced residues,
  valuations, function congruence, lifting trees, and finite-horizon
  minimization.
- **Maximum Phase-0 scope:** literature records, one exact bounded
  prototype, tests, this dossier, and one journal entry.
- **Promotion criterion:** a proved nonclassical quotient, missing
  invariant, dynamical consequence, or sharp limitation.
- **Stop criterion:** close if higher Taylor data resolves every failure
  of coarse invariants and no theorem survives beyond classical cycle
  lifting plus standard behavioural minimization.

## Balanced-ternary formulation

Choose the canonical rotation of a cycle and its least nonnegative
representative `x`. For `t mod 3^r`, the normalized return displacement is

`R_(f,C,k,r)(t) =
  (f^q(x + 3^k t) - (x + 3^k t)) / 3^k mod 3^r`.

It is evaluated exactly by modular iteration, without expanding `f^q`.
The table of `R` is the finite polynomial-function class of the residual
of `f^q-id` at the cycle. Replacing ordinary digits by balanced trits
only changes the coordinates on `t`.

## Why BT may be relevant

The existing section calculus supplies exact finite-function classes and
distinguishing horizons, so it makes the comparison inexpensive and
canonical. It does not add information to the Taylor expansion of the
return map. Here BT is useful experimental machinery, not a new
dynamical invariant.

## Candidate operations / invariants

- Cycle enumeration modulo `3^k` — **KNOWN**.
- Cycle reduction and lift edges — **KNOWN**.
- Fan--Liao signature
  `(q, a mod 3^r, b mod 3^r, low Taylor correction)` — **KNOWN**.
- Residual return-function table `R_(f,C,k,r)` — **REPARAMETERIZATION**
  of the truncated local return map.
- Depth-`r` behavioural quotient `≡dyn_r` — **KNOWN** as bounded
  labelled-tree equivalence; its application and census here are
  **PROJECT-SPECIFIC**.
- `D_r(f,k)`, the number of observed `≡dyn_r` classes — **OBSERVATION**
  only. No closed form or nonclassical consequence was obtained.

The return-function table determines the cycle-lift tree: cycles of
`f` above `C` correspond to cycles of the induced return map on the
fibre coordinate `t`, and reduction of those cycles gives the next
level. Induction on `r` proves sufficiency. This is a
**REPARAMETERIZATION** of the classical return-map construction.

## Experiments

`research.padic_dynamics.triage` implements:

- exact functional graphs and canonical cycles modulo powers of 3;
- exact parent/child matching under reduction;
- classical multiplier, displacement, valuation, lift-type, and
  low-level Taylor signatures;
- the complete residual return-function table;
- canonical period-labelled depth-`r` behaviour;
- Searches A--D and smallest-witness extraction.

The fixed Phase-0 corpus consists of 28 maps:

`x^2+c`, `x^3+c`, `x^3-x+c`, and `x^4+c`,
for `c ∈ {-3,-2,-1,0,1,2,3}`.

At `k = 1,2,3` and `r = 3`:

- 180 cycle states were compared;
- periods were `1,2,3,6,9`;
- all four classical one-level lift types occurred;
- 148 residual return-function classes collapsed to 19 behavioural
  classes;
- 5 coarse classical classes and 6 valuation-only classes contained
  different futures;
- one affine-plus-quadratic class contained different futures;
- no residual class contained different futures;
- 13 behavioural classes contained multiple residual classes.

These are finite exact computations, not universal proofs.

## Conjectures

None registered. The census did not produce a statement strong enough
to justify an `OPEN` conjecture.

## Counterexamples

1. **Coarse multiplier/valuation data is insufficient.** At level 1,
   the fixed cycles `(1)` of `x^2-3` and `x^2+3` have the same
   `(q, lift type, v_3(a-1), v_3(b)) = (1, partial-split, 0, 0)` but
   different depth-2 futures. Their displacement residues differ, so
   this is already explained by classical affine data.

2. **Affine and quadratic data is insufficient at horizon 3.** For
   `f=x^3-x`, the fixed cycle `(0)` at levels 1 and 2 has the same
   `q=1`, `a=-1 mod 27`, `b=0 mod 27`, and scaled quadratic correction
   `0`, but different depth-3 trees. The normalized return maps contain
   cubic terms `9t^3` and `81t^3`; the first is visible modulo 27 and the
   second is not. Full Taylor/residual data distinguishes them. This is
   the smallest census witness that the affine signature is not a
   complete finite-horizon state.

3. **The residual state is not minimal for the chosen observable.** The
   period-2 cycle `(0,2)` modulo 3 for `x^2-1` and `x^2+2` has equal
   depth-2 cycle-lift behaviour but different residual return-function
   tables. This is strict compression, but it is exactly the quotient
   induced by forgetting distinctions outside the bounded tree
   observable.

The witnesses are regression-tested in
`tests/research/padic_dynamics/test_triage.py`.

## Formalization

No new Lean module was added. The exact residual/Taylor identification
for ordinary lifting is already formalized in
`formal/BTCalculus/PadicLifting.lean`; the Phase-0 cycle census yielded
no new theorem that justifies a dynamics formalization.

## Results

### Literature classification

- `KNOWN`: finite functional graphs, cycle-lift trees, multipliers,
  affine fibre maps, grow/split/tail/partial-split types, valuation
  recurrences, possible periods, analytic interpolation, transducers,
  and bounded tree minimization.
- `REPARAMETERIZATION`: the residual return-function table and its
  sufficiency for the cycle-lift tree.
- `PROJECT-SPECIFIC`: the exact corpus, canonical serialization, witness
  search, and measured `148 → 19` bounded compression.
- `OPEN`: none promoted.

### Gate verdict

`CLOSE`

The residual description is a convenient exact encoding of the
classical local return map. Coarse multiplier data fails only because
higher Taylor terms matter; the full residual supplies exactly those
terms. Minimizing the resulting finite tree gives substantial bounded
compression, but no normal form, complexity theorem, or dynamical
consequence beyond standard finite-depth behavioural equivalence.

## Open questions

None retained on this branch. In particular, the mere existence of
strict bounded compression is not promoted to a conjecture.

## Decision

`CLOSE — REPARAMETERIZATION`. The literature gate and the exact
falsification study agree: cycle lifting is governed by the classical
return map, while residual coordinates reproduce its truncated local
function. The only additional object is a standard bounded behavioural
quotient, and the census supplies no theorem-level reason to continue.

Best next question: none; the branch is not promoted.

## Publication assessment

Status: `ARCHIVED`.

The branch records useful negative knowledge and reusable tests, but
contains no new theorem or literature-separated computational result.
