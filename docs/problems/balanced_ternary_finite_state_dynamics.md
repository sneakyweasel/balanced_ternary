# Balanced-ternary finite-state dynamics

Status: **STRUCTURAL**

Which balanced-ternary digit transformations admit finite residual
closure? Phase 0 asks this of one exact system: normalize the
LSD-first doubled trit stream `2 d_i` with `d_i ∈ {-1,0,1}`.

## Problem

Model existing balanced-ternary normalization as finite-control
integer dynamics, discover the residual closure with the generic
research engine, and identify the mechanism that makes the system
finite-state. Then perturb one ingredient until that mechanism
fails.

## Exact statement

Let `d_i ∈ {-1,0,1}` and let `c_0 = 0`. The existing bounded
normalizer `BoundedNormalizeTransducer(2)` defines

\[
(c_{i+1}, r_i) = \operatorname{step}(c_i, 2 d_i),
\qquad
c_i + 2 d_i = 3 c_{i+1} + r_i,\quad r_i\in\{-1,0,1\}.
\]

The reachable residual set is exactly `{-1,0,1}`. After the input
ends, one flush step `d=0` sends every box carry to `0`. The same
remainder map with synthetic gain `λ=3`, namely
`T_3(c,d)=3\cdot DZ(c+2d)`, is unbounded along the all-`+1` word
(`c_n=3n`).

## Current literature

- Unique canonical balanced-ternary expansions are `KNOWN`
  (`BT-encode-unique`, `BTN-nf`).
- Finite-state classification of coefficient normalization by a
  fixed alphabet bound `[-B,B]` is `KNOWN`
  (`bt.normtheory.locality`, `BTN-carry-bound`).
- This branch does not claim a new representation theorem. It tests
  whether the research engine rediscovers that carry bound on a
  genuinely different arithmetic system from Ostrowski, and whether
  a one-parameter gain perturbation destroys it.

## Branch budget

- **Target:** exact carry closure and minimal subsequential
  transducer for doubled-trit normalization.
- **Novelty hypothesis:** radix-3 division plus bounded forcing, not
  representation uniqueness, is the finite-state mechanism, and
  `λ=3` is a controlled counterexample.
- **Falsifier:** the adapter disagrees with
  `BoundedNormalizeTransducer(2)`, or the engine cannot certify
  exhaustive closure without problem-specific proof logic.
- **Existing machinery:** `balanced_divmod`, the bounded Mealy
  normalizer, `ProblemSpec`, typed attacks, Mealy partition
  refinement, Lean `DZ`/`lsdZ`.
- **Maximum Phase-0 scope:** one doubled-trit system; exact
  closure/invariant/minimality; the family `λ∈{1,2,3}`. No
  D-operator benchmark, symbolic control, or generic order-`(m)`
  work.
- **Promotion criterion:** an exact Python certificate and a
  zero-sorry Lean theorem for the closure/mechanism, plus the `λ=3`
  witness, with the engine reproducing both fingerprints.
- **Stop criterion:** semantic mismatch, adapter-parity failure, or
  a need for a second framework.

## Balanced-ternary formulation

Digits are the existing trits `{-1,0,1}`. Words are LSD-first
coefficient streams. The adapter never reimplements
`balanced_divmod`; it calls `BoundedNormalizeTransducer(2).step`.
Gain `λ≠1` is labelled synthetic and is not a value-preserving
normal form.

## Why BT may be relevant

The laboratory already has the unique encoder and the bounded
normalizer. The question is whether finite-control integer dynamics
recovers that structure as residual closure, and what algebraic
change destroys it.

## Candidate operations / invariants

- Residual step `c ↦ DZ(c+2d)`. **EXACT — LEAN VERIFIED**
- Box invariant `|c|≤1`. **EXACT — LEAN VERIFIED**
- Lyapunov `V(c)=|c|` strictly decreases for `|c|≥2`. **EXACT — LEAN VERIFIED**
- Sign equivariance `T(-c,-d)=-T(c,d)`. **EXACT — LEAN VERIFIED**
- Three distinct Mealy output signatures. **EXACT — LEAN VERIFIED**
- Gain `λ=3` unbounded. **EXACT — LEAN VERIFIED**

The step is piecewise balanced division, not one integer-affine map
`As+b(d)`. Modular/spectral attacks are inapplicable.

## Experiments

- `btlab research analyze|attack|reproduce|report balanced_ternary`
- Adapter tests in `tests/research/balanced_ternary/`
- Attack records in `experiments/balanced_ternary/`
- Carry-gain family `λ∈{1,2,3}` in
  `research.balanced_ternary.perturbation`

## Conjectures

None opened. Finite-horizon stabilization is not a conjecture and
is not promoted.

## Counterexamples

- Global Lyapunov `|c|` is not nonincreasing on the start layer
  (`0 → 1`). The decrease is outside `[-1,1]`.
- `λ=3` along all-`+1`: `c_n=3n`.

## Formalization

`formal/Problems/BalancedTernary/FiniteStateDynamics.lean`. No
`sorry`. Minimality in Lean is the distinct-output-signature
witness, not a general Myhill–Nerode development.

## Results

- `R_∞={-1,0,1}` for doubled-trit normalization.
- Raw residual states: 3. Sign orbits: 2. Minimal Mealy classes: 3.
- `λ=1` and `λ=2` are finite; `λ=3` is not.
- Engine reconnaissance remains `OBSERVED`/`BOUNDED`. Exhaustive
  closure is `EXACT` by queue exhaustion at the frozen input phase.

## Open questions

Does the integer operator `D(n)=3n-lsd(n)` have finite residual
closure in the same engine coordinates? That is the next question,
not part of this phase.

## Decision

`PROMOTE` the doubled-trit adapter, the exact residual-closure
theorem, the Lyapunov mechanism, and the `λ=3` boundary. The
statements are not a reparameterization of Ostrowski: the engine
had to treat a non-affine balanced-division step, and a one-line
gain change destroys finiteness.

Best next question: can the same attack stack rediscover the known
structure of `D` automatically?

## Publication assessment

Status: `STRUCTURAL`.

Unique balanced-ternary representation is `KNOWN`. The promoted
content is the engine certificate, the explicit Lyapunov mechanism,
and the controlled finite-to-infinite boundary. That is not a
`PAPER_CANDIDATE` by itself.
