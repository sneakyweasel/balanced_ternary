# Signed-digit residual geometry

Status: **STRUCTURAL**

Inside the already classified finite phase of `F_{λ,U}(s,u)=λ·D(s+u)`,
what is the exact origin-reachable set, and does Mealy size follow that
geometry?

CLI `btlab research analyze signed_digit_residual_geometry` (aliases
`sdrg`, `sdr_geometry`). Reuses `SignedDigitResidualSpec`. It does not
reopen the finite/infinite law, Collatz, primes, T/jets, or Ostrowski.

## Problem

Characterize `R_{λ,U}` inside the sharp invariant envelope, and relate
it to `M(λ,U)`.

## Exact statement

For the symmetric family `U_m={-m,...,m}` in the finite regime:

- `λ=1`: `R_{1,U_m}=[-⌊m/2⌋,⌊m/2⌋]`, reached by the word
  `u=2,4,...,2|t|` (and its negative).
- `λ=2`: `R_{2,U_m}=2ℤ∩[-2(m-1)_+,2(m-1)_+]`, reached by
  `u=2,3,...,|h|+1` targeting `2h`.
- `λ=3`, `m=1`: `R={0}`.

The candidate `R_{λ,U}=λℤ∩ B^*` with `B^*` the symmetric invariant
interval holds for every `U_m` above and fails for one-sided `U`.
Smallest witness: `U={2}` at `λ=1` has `B^*=[-1,1]` and `R={0,1}`.
On these families `M(λ,U)=|R|`; sign symmetry does not merge states.

## Current literature

- Finite signed-digit adders / conversion transducers are `KNOWN`
  (`avizienis-1961-signed-digit`).
- The finite/infinite phase `λ≤2 ∨ max|u|≤1` is the previous laboratory
  theorem (`BTN-sdr-finite-condition`).
- Exact origin-reachable fill of the envelope, and the failure of
  lattice-in-box for sparse `U`, is `PROJECT-SPECIFIC`
  (`NEW FORMULATION`). It is not a new adder.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

- **Target:** exact `R_{λ,U}` inside the finite envelope, and whether
  `M` is determined by that geometry.
- **Novelty hypothesis:** for `U_m` the reachable set is the lattice
  intersection with the sharp box, filled by an explicit word; the
  same formula fails for one-sided `U`; `M=|R|` on these families.
- **Falsifier:** a hole in `U_m` at `λ=1` or `λ=2`; or lattice-in-box
  holding for `U={2}`; or sign symmetry halving Mealy size on `U_m`.
- **Existing machinery:** `signed_step`, `reachable_from`,
  `SignedDigitResidualSpec`, Mealy, invariant radius, Lean boxes.
- **Maximum Phase-0 scope:** `U_m` at `λ=1,2` and `(3,1)`; probes
  `{2}`, `{-2,0,2}`, `{0,1,2}`, `{-1,0,2}`; Lean of the filling words
  and the `U={2}` miss.
- **Promotion criterion:** exact `R` for `U_m` with both inclusion and
  reachability, plus a clean lattice-in-box counterexample.
- **Stop criterion:** holes with no short description; or the fill is
  only a restatement of bounded carry.

## Balanced-ternary formulation

The transition is existing `D`/`lsd`. Reachability is the orbit of `0`
under `s↦λ D(s+u)` for `u∈U`.

## Why BT may be relevant

The envelope was already a `D`-invariant. The remaining question is
which lattice points inside it are generated from the origin.

## Candidate operations / invariants

- `R_{1,U_m}=[-⌊m/2⌋,⌊m/2⌋]`. **EXACT — LEAN VERIFIED**
- `R_{2,U_m}=2ℤ∩[-2(m-1)_+,2(m-1)_+]`. **EXACT — LEAN VERIFIED**
- `R=λℤ∩ B^*` for every finite `U`. **REFUTED** (`U={2}`)
- Sign symmetry forces `M=|R|/2`. **REFUTED**
- `M=|R|` on `U_m` and the four probes. **COMPUTATIONALLY VERIFIED**
- `(3,1)` origin only. **EXACT — LEAN VERIFIED** (existing
  `origin_trit_forcing`)

## Experiments

- `btlab research analyze|attack|reproduce|report signed_digit_residual_geometry`
  (aliases `sdrg`, `sdr_geometry`)
- Tests in
  `tests/research/signed_digit_residual_geometry/test_signed_digit_residual_geometry.py`
- Records in `experiments/balanced_ternary/signed_digit_residual_geometry/`

Default planner system is `λ=1`, `U_2`.

## Conjectures

None opened.

## Counterexamples

- Lattice-in-box for general `U`: `U={2}`, `λ=1`, missing `-1`.
- `U={0,1,2}` and `U={-1,0,2}` likewise miss the negative ray.
- `U={-2,0,2}` matches `U_2` at `λ=1,2` (holes at `±1` are not needed
  to fill the envelope).
- Sign-halved Mealy: `U_2` has `M=|R|` at `λ=1` and `λ=2`.

## Formalization

`formal/Problems/BalancedTernary/SignedDigitResidualGeometry.lean`.
Reuses `signedNext` and `DZ_three_mul_add_two`. No `sorry`.

## Results

| `(λ,U)` | `B^*` | `R` | `M` |
|---------|-------|-----|-----|
| `(1,U_m)` | `[-⌊m/2⌋,⌊m/2⌋]` | the full interval | `\|R\|` |
| `(2,U_m)` | `[-2(m-1)_+, 2(m-1)_+]` | even lattice in the box | `\|R\|` |
| `(3,U_1)` | `{0}` | `{0}` | `1` |
| `(1,{2})` | `[-1,1]` | `{0,1}` | `2` |
| `(1,{0,1,2})` | `[-1,1]` | `{0,1}` | `2` |
| `(1,{-2,0,2})` | `[-1,1]` | `{-1,0,1}` | `3` |

`0` already lies in `λℤ`; no extra origin exception is required.

The missing restriction for general `U` is the semigroup orbit of `0`,
not a further modulus: `U={5}` at `λ=1` reaches `{0,2}` inside `[-2,2]`,
so `1` is a lattice point in the box that is never generated.

## Open questions

Answered by [signed_digit_residual_minimality.md](signed_digit_residual_minimality.md):
`M=|R|` for every nonempty `U` when `λ` is not divisible by 3, by a
constant word of length `v_3(s-t)+1`. Do not auto-start a general-radix
theorem.

## Decision

`PROMOTE` the exact fill of the `U_m` envelope at `λ=1` and `λ=2`, with
explicit admissible words both ways, and the refutation of
lattice-in-box for arbitrary `U`. Avizienis remains `KNOWN`. The
promoted content is origin-reachable geometry, not a carry transducer.

Best next question: answered by
[signed_digit_residual_minimality.md](signed_digit_residual_minimality.md).

## Publication assessment

Status: `STRUCTURAL`. Exact filling theorems exist. Not a
`PAPER_CANDIDATE`: the `λ=1` fill is the reachable carry set of
ordinary LSD-first conversion, reformulated as residual geometry.
