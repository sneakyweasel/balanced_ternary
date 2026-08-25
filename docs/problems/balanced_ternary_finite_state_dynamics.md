# Balanced-ternary finite-state dynamics

Status: **STRUCTURAL**

Which balanced-ternary digit transformations admit finite residual
closure? Phase 0 treats doubled-trit normalization. Phase 1 treats
the expanding section `T(n)=3n-lsd(n)` as an LSD-observable
quotient. Phase 2 asks whether that finite structure lifts to the
existing length-2 integer jet `J₂`. Phase 3 asks how many input
digits `T` remembers on the length-3 jet `J₃`.

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
- Expanding `T(n)=3n-lsd(n)`: `lsd(T(n))=-lsd(n)`. **EXACT — LEAN VERIFIED**
- `DZ(T(n))=n`. **EXACT — LEAN VERIFIED**
- `T(I_a(x))=9x+2a`. **EXACT — LEAN VERIFIED**
- Magnitude contraction of `T`. **REFUTED**
- `lsd(T_2(n))=lsd(n)`, `lsd(T_3(n))=0`. **EXACT — LEAN VERIFIED**
- `J₂(T(n))=(-lsd(n), lsd(n))`. **EXACT — LEAN VERIFIED**
- `J₂` orbit requires a third digit. **REFUTED**
- `J₂(T_2(n))=(lsd(n),0)`, `J₂(T_3(n))=(0,0)`. **EXACT — LEAN VERIFIED**
- `J₃(T(n))=(-a,a,b)` factors through `J₂`. **EXACT — LEAN VERIFIED**
- `J₃(T(n))` is a function of `lsd(n)` alone. **REFUTED**
- `J₃(T_2(n))=(a,0,b)`, `J₃(T_3(n))=(0,0,b)`. **EXACT — LEAN VERIFIED**

The step is piecewise balanced division, not one integer-affine map
`As+b(d)`. Modular/spectral attacks are inapplicable.

## Experiments

- `btlab research analyze|attack|reproduce|report balanced_ternary`
- Adapter tests in `tests/research/balanced_ternary/`
- Attack records in `experiments/balanced_ternary/`
- `btlab research analyze|attack|reproduce|report expanding_d`
- `btlab research analyze|attack|reproduce|report expanding_j2`
- `J₂` records in `experiments/balanced_ternary/expanding_j2/`
- `btlab research analyze|attack|reproduce|report expanding_j3`
- `J₃` records in `experiments/balanced_ternary/expanding_j3/`

## Phase 1 — expanding `T(n)=3n-lsd(n)`

Laboratory `D` is unchanged: `DZ(n)=(n-lsd(n))/3`. The Phase-1
operator is the existing section

\[
T(n)=3n-\operatorname{lsd}(n)=I_{-\operatorname{lsd}(n)}(n).
\]

If `n=3q+r` with `r=lsd(n)`, then `T(n)=9q+2r`. Question A (finite
integer orbit) fails: `|T(n)|>|n|` for `n≠0`. Question B
(observational residual) is exact:

\[
\operatorname{lsd}(T(n))=-\operatorname{lsd}(n),\qquad
\operatorname{lsd}(T^k(n))=(-1)^k\operatorname{lsd}(n).
\]

The three LSD classes are pairwise distinguishable. Higher windows
`n \bmod 3^k` for `k≥2` refine the integer but not the observation;
`n=1` and `n=4` separate “need mod 9”. Bounded reconnaissance is
an `OBSERVATION`, not a Myhill–Nerode proof. The exact statement
is Lean `lsdZ_iterate_expandingD`.

`ExpandingDResidueSpec` uses that discovered state. Controls are
`I_a` and a `T`-tick. The step is not one `Ax+b`. Exhaustive
closure is `R_∞={-1,0,1}`. Integer-state BFS hits the cap and is
not labelled infinitude. Perturbations `λ=2,3` change the residue
map and keep a 3-state LSD residual.

## Phase 2 — length-2 integer jet

`J₂(n)` is the existing `integer_jet(n, 2)=(lsd(n), lsd(D(n)))`.
Because `DZ(T(n))=n`,

\[
J_2(T(n))=(-a,a)\qquad\text{if }a=\mathrm{lsd}(n).
\]

The second digit is required to emit `J₂(n)`, then discarded. A
third digit does not affect the orbit: `n=1` and `n=10` share
`J₂=(1,0)`. Raw states: 9 trit pairs. `T`-image: 3. Full-sequence
classes: 9. Next-output Mealy: 3. Reconnaissance is `OBSERVATION`.
Lean: `jet2_expandingD`, `jet2_residue_closure`.

`T_2` is invisible at order 1 and visible at order 2:
`J₂(T_2(n))=(a,0)`. `T_3` collapses to `(0,0)`. Both stay finite.

This is a forgetful digit-window jet, analogous to
`J₂(I_c(n))=(c,lsd(n))`, not a classical polynomial derivative.

## Phase 3 — length-3 integer jet and memory depth

`J₃(n)` is the existing `integer_jet(n, 3)=(a,b,c)` with LSD-first
indexing. Storage orientation matches the mathematical tuple:
`a=lsd(n)`, `b=lsd(DZ(n))`, `c=lsd(DZ²(n))`. From the Phase-1
identities `lsd(T(n))=-a` and `DZ(T(n))=n`,

\[
J_3(T(n))=(-a,a,b)=(-a)\mathbin{\|} J_2(n).
\]

The third input digit `c` is discarded. The second digit `b`
survives as the third output coordinate. The factorization
`J₃∘T=F∘J₂` is exact; `J₁` is not sufficient (`n=1` vs `n=4`).
Same `J₂` and different `c` do not separate the next `J₃`
(`n=1` vs `n=10`). The prefix square commutes:
`J₂(T(n))` is the first two coordinates of `J₃(T(n))`.

Counts, kept separate:

- raw trit triples: 27
- reachable residual states (`I`/`T` from `(0,0,0)`): 27
- `T`-image: 9 states of the form `(-a,a,b)`
- full-sequence classes: 27
- next-output Mealy: 9 (states with the same `(a,b)` merge)

Reconnaissance is `OBSERVATION`. Exhaustive closure is `EXACT` by
queue exhaustion. Lean: `jet3_expandingD`, `jet3_factors_through_jet2`,
`jet3_residue_closure`.

Perturbations (no sweep): `J₃(T_2(n))=(a,0,b)` and
`J₃(T_3(n))=(0,0,b)`. `T_3` collapses `J₁` and `J₂` but does not
collapse `J₃`: `b` survives. Memory structure still forgets `c`.

Memory depth at this order: `J₃∘T` factors through `J₂` (`m=2`),
not through `J₁`. The concatenation law is the natural recursive
pattern from `DZ∘T=id`; this phase does not launch `J₄`.

## Conjectures

None opened. Finite-horizon stabilization is not a conjecture and
is not promoted.

## Counterexamples

- Global Lyapunov `|c|` is not nonincreasing on the start layer
  (`0 → 1`). The decrease is outside `[-1,1]`.
- `λ=3` along all-`+1`: `c_n=3n`.
- Magnitude contraction of expanding `T`: `|T(1)|=2>1`.
- Finite-window residual `n mod 9` as a necessary LSD state:
  `n=1` and `n=4` have the same `T`-LSD stream.
- `J₂(T(n))` depends on the second digit: `n=1` and `n=4` have
  distinct `J₂` but `J₂(T(n))=(-1,1)` for both.
- A third digit is required for the `J₂`-orbit: `n=1` and `n=10`.
- `J₃(T(n))` depends only on `lsd(n)`: `n=1` and `n=4` share
  `a=1` but `J₃(T(1))=(-1,1,0)` and `J₃(T(4))=(-1,1,1)`.
- `J₂` fails to determine `J₃(T(n))`: no witness. `n=1` and
  `n=10` share `J₂=(1,0)` and `J₃(T)=(-1,1,0)`.

## Formalization

`formal/Problems/BalancedTernary/FiniteStateDynamics.lean` and
`formal/Problems/BalancedTernary/ExpandingD.lean`. No `sorry`.
Minimality in Lean is the distinct-output-signature witness, not
a general Myhill–Nerode development.

## Results

- `R_∞={-1,0,1}` for doubled-trit normalization.
- Raw residual states: 3. Sign orbits: 2. Minimal Mealy classes: 3.
- `λ=1` and `λ=2` are finite; `λ=3` is not.
- Engine reconnaissance remains `OBSERVED`/`BOUNDED`. Exhaustive
  closure is `EXACT` by queue exhaustion at the frozen input phase.
- Expanding `T`: integer orbits expand; LSD observational quotient
  is 3 states; `DZ∘T=id`; `T(I_a(x))=9x+2a`.
- `T_2` preserves LSD; `T_3` sends LSD to `0`. Observational
  finiteness survives both perturbations.
- `J₂` of `T` is the 9 trit pairs with exact law `(-a,a)`. Raw 9,
  `T`-image 3, next-output Mealy 3, full-sequence classes 9.
- `T_2` erases the second jet digit; `T_3` collapses `J₂` to `(0,0)`.
- `J₃` of `T` is the 27 trit triples with exact law `(-a,a,b)`.
  Raw 27, reachable 27, `T`-image 9, next-output Mealy 9,
  full-sequence classes 27.
- `T_2` and `T_3` still forget `c`; `T_3` keeps `b` at order 3.

## Open questions

None opened by this phase. Do not auto-start another milestone.

## Decision

Phase 0: `PROMOTE` the doubled-trit adapter, the exact residual-closure
theorem, the Lyapunov mechanism, and the `λ=3` boundary.

Phase 1: `PROMOTE` the expanding-`T` LSD residual, the section
identities, the magnitude-contraction refutation, and the `λ=2,3`
residue maps.

Phase 2: `PROMOTE` the exact `J₂` transformation law, the 9-state
window residual, the third-digit refutation, and the order-2
visibility of `T_2`. Finite-horizon stabilization was not treated
as proof.

Phase 3: `PROMOTE` the exact `J₃` law `(-a,a,b)`, the factorization
through `J₂`, the `J₁`-insufficiency witness, and the survival of
`b` under `T_3`. Do not auto-start `J₄`.

Best next question: does `J_k(T)=(-lsd(n))\mathbin{\|} J_{k-1}(n)`
hold for every `k`, or is there a first order at which the last
digit survives?

## Publication assessment

Status: `STRUCTURAL`.

Unique balanced-ternary representation is `KNOWN`. Phase 0 promoted
the doubled-trit engine certificate and the gain boundary. Phase 1
promoted the LSD observational quotient of expanding `T`. Phase 2
promoted the length-2 integer jet of `T`. Phase 3 promoted the
length-3 jet law and its exact memory depth `m=2`. That is not a
`PAPER_CANDIDATE` by itself.
