# Balanced-ternary weight dynamics

Status: **ARCHIVED**

Control experiment against the closed digit-sum regime: replace signed
digit aggregation by nonlinear sign-erasing aggregation
`W(n)=∑ d_i²`. Does not reopen signed-digit, Collatz, primes, jets,
Ostrowski, `{S,N,D,W}`, `N∘I_0∘D`, polynomial `s_bal(P(n))`, or
digit-sum dynamics.

CLI `btlab research analyze|attack|reproduce|report balanced_ternary_weight_dynamics`
(aliases `weight`, `btw`, `wd_dynamics`).

## Problem

Does v2 diagnose a dynamical regime for `W` that is genuinely different
from the finite-contracting digit-fold regime of `SignedP0` and `s(n)`?

## Exact statement

### A. Target definition

For the canonical expansion `n=∑ d_i 3^i`, `d_i∈{-1,0,+1}`,

`W(n)=∑_i d_i²`,

equivalently `W(0)=0` and `W(n)=lsd(n)²+W(D(n))`. The system is
`n_{t+1}=W(n_t)`.

## Current literature

- `oeis-A005812`: weight of balanced-ternary `n≥0`. `KNOWN`.
- `ruskey-sawada-2009-digital-sum-gf`: nonzero-count analogue `c_k` of
  the digit sum. `KNOWN`.
- `oeis-A134452` / `oeis-A065363`: iterated *signed* digit sum, the
  closed reference regime. `KNOWN`.
- Iteration of Hamming weight / nonzero-count is the digital-root
  architecture with a nonnegative attractor. `KNOWN` as a class;
  the BT instance is a `NEW FORMULATION` of iterating A005812.

## Branch budget

```text
Mathematical target     Does v2 diagnose a regime for W(n)=∑ d_i² that
                        differs from the finite-contracting digit-fold
                        already seen for SignedP0 and s(n)?
Novelty hypothesis      Either a new quotient/recurrent/compression
                        mechanism, or a successful regime-replication
                        CLOSE.
Falsifier               The adapter is fed Hamming weight, an attractor,
                        Lyapunov, modulus, or length bound; or W rewrites
                        to n, -n, 3n+a, or D(n).
Existing machinery      ProblemSpec, AttackPlanner, CertificateKind,
                        ComplexityProfile; lsd, D, bt_weight; closed
                        SignedP0 and digit-sum dossiers.
Maximum Phase-0 scope   One integer adapter; generic planner; bounded
                        seeds; one Lean theorem if an identity survives.
Promotion criterion     A structurally new invariant, quotient, recurrent
                        class, or reusable engine abstraction.
Stop criterion          Same finite-contracting architecture as s(n);
                        machinery gravity; or INCONCLUSIVE with no compact
                        residual.
```

## Balanced-ternary formulation

`W` is the fold of squared local trits. Observation is the integer
state. Controls are a dummy singleton.

## Why BT may be relevant

The local operators are the calculus. Sign-erasure is the control
against the signed fold `s`.

## Candidate operations / invariants

- `W(n)=lsd(n)²+W(D(n))`. **EXACT — LEAN VERIFIED** (`weightZ_rec`)
- `W(-n)=W(n)`. **EXACT — LEAN VERIFIED** (`weightZ_even`)
- `|W(n)|<|n|` for `|n|≥2`. **REFUTED** (`W(2)=2`)
- `|W(n)|<|n|` for `|n|≥3`. **EXACT — LEAN VERIFIED**
- `W(n)=n` iff `n∈{0,1,2}`. **EXACT — LEAN VERIFIED**
- every orbit reaches `|n|≤2` in at most `|n|` steps. **EXACT — LEAN VERIFIED**
- `V(n)=n` is a Lyapunov. **REFUTED** (`W(0)=0`)
- `W²=W`. **REFUTED** (`W(5)=3`, `W(3)=1`)
- identity observation merges orbit points. **REFUTED**
- `ℤ` is one finite residual. **REFUTED** (orbits of 4 and 5)

## Experiments

- `btlab research analyze|attack|reproduce|report balanced_ternary_weight_dynamics`
- Discovery: `src/research/balanced_ternary_weight_dynamics/discovery.py`
- Tests: `tests/research/balanced_ternary_weight_dynamics/test_weight_dynamics.py`
- Records in `experiments/balanced_ternary/weight_dynamics/`

### B. Adapter

Integer state `(n,)`, dummy control `0`, identity observation
`obs(n)=n`, transition the `lsd²`/`D` fold. No reverse preimages, no
symmetry candidates, no `affine_system`, no `raw_contribution`.
Candidate box `|n|≤2` is a generic envelope probe. Horizon-only
accepting predicate.

### C. Planner trace

| attack | status | reason |
|--------|--------|--------|
| reconnaissance | OBSERVATION | bounded census |
| closure | SUPPORTED EXACT | seed orbit of 4 has size 2 |
| functional | OBSERVATION | sample bound, not a Lyapunov |
| affine | OBSERVATION | box `|n|≤2` has no live one-step leak |
| separation | EXACT | 4 and 2 distinguished by identity observation |
| quotient | SUPPORTED EXACT | `M=\|R\|=2` |
| modular, spectral, block, factorization, reverse, symmetry | skipped | inapplicable |
| symbolic | skipped | not implemented |

## Conjectures

None opened.

## Counterexamples

### E. Falsification record

- `|W(n)|<|n|` for `|n|≥2`: `W(2)=2` and `W(-2)=2`.
- `W²=W`: `W(5)=3≠1=W(W(5))`.
- `V(n)=n` strictly decreases: `W(0)=0`.
- Global finite residual: `{4,2}` and `{5,3,1}` are disjoint.
- Identity merge: `4` and `2` separate immediately.
- Oddness `W(-n)=-W(n)`: `W(-1)=1≠-1`.
- Evenness and `|n|≥3` contraction: no counterexample on `|n|≤80`.

## Formalization

`formal/Problems/BalancedTernary/WeightDynamics.lean`. No `sorry`.
Theorems `weightZ_rec`, `weightZ_even`, `weightZ_natAbs_lt`,
`weightZ_eq_self_iff`, `weightIterate_reaches_le_two`.

No theorem-ledger row: iterating A005812 is `KNOWN` digital-root
architecture (`REPARAMETERIZATION` of nonzero-count iteration).

## Results

### D. Discovered structure

- Per-seed residual is finite; `ℤ` is not one finite residual.
- Seed `4` closes as `{4,2}`.
- Box `|n|≤2` does not leak; it contains the recurrent points
  `{0,±1,±2}` mapped into `{0,1,2}`.
- Identity observation yields `M=|R|`.
- Reverse/block/modular/spectral/factorization/symmetry inapplicable.
- The `|n|≥2` contraction of `s(n)` fails; contraction holds for
  `|n|≥3`. Image is nonnegative. The map is even.

### F. Comparative diagnosis

`W` **reproduces the finite-contracting digit-fold regime**. The
architectural pipeline is identical to `s(n)`: recursive local fold →
magnitude compression → finite per-seed closure → identity observation
with no merge → reverse inapplicable → no engine change. The only
structural deltas are the even/nonnegative image and the recurrent set
`{0,1,2}` versus `{-1,0,1}` for `s`, plus the failure of the `|n|≥2`
contraction at the fixed point `2`. Those are parameter changes inside
the same regime, not a new v2 class.

| Dimension | `SignedP0` | `s(n)` | `W(n)` |
|-----------|------------|--------|--------|
| Transition type | word `N∘I_0∘D` | signed digit fold | squared-trit fold |
| Compression mechanism | `F²=P_0`; orbits ≤3 | `|s|<\|n\|` for `|n|≥2` | `|W|<\|n\|` for `|n|≥3` |
| Exact image behavior | `im F ⊆ 3ℤ` | signed, odd map | nonnegative, even map |
| Per-seed orbit size (seed 4) | 3 | 3 | 2 |
| Recurrent structure | `{n,F(n),P_0(n)}`; fp `{0}` | `{-1,0,1}` | `{0,1,2}` |
| Transient complexity | at most 2 steps | at most `|n|` steps | at most `|n|` steps |
| Behavioral quotient | sign merge `M=2<\|R\|=3` | identity `M=\|R\|` | identity `M=\|R\|` |
| Separation depth | 1 (sign) | 0–1 (identity) | 0–1 (identity) |
| Applicable attacks | recon, closure, functional, affine, reverse, sep, quotient | recon, closure, functional, affine, sep, quotient | same as `s(n)` |
| ComplexityProfile (seed 4) | R=3, M=2, EXACT_CLOSURE | R=3, M=3, EXACT_CLOSURE | R=2, M=2, EXACT_CLOSURE |
| Lean result | `signedP0_sq_eq_P0` | `digitSumZ_natAbs_lt` | `weightZ_natAbs_lt` |

### G. Lean certification

If `|n|≥3` then `|W(n)|<|n|`; `W` is even; `W` iterated `|n|` times has
absolute value at most 2. File
`Problems.BalancedTernary.WeightDynamics`.

### H. Prior-art checkpoint

`W` on `ℕ` is A005812. Nonzero-count generating functions are in
Ruskey–Sawada. Iterated Hamming weight is the classical digital-root
pattern. Engine rediscovery: per-seed closure, evenness, contraction
threshold 3. New formalization in this repository: `weightZ_*`. Not
new mathematics.

### I. ComplexityProfile

Seed `4`: controls 1; raw contribution unset; envelope 5; reachable 2;
Mealy 2; diameter 1; closure `EXACT_CLOSURE`. Finite-horizon exact for
the seed orbit; universal exact for contraction/evenness (Lean).

### J. Infrastructure verdict

```text
NO ENGINE CHANGE
```

### K. Branch decision

```text
CLOSE
```

Scalar digit-statistic maps (`s` and `W`) do not presently expose a
new v2 dynamical regime. Do not enumerate another digit statistic.

## Open questions

Nothing on this line.

## Decision

`CLOSE`. Regime-replication control: `W` is the same finite-contracting
digit-fold architecture as `s(n)`, with a nonnegative even image and
attractor `{0,1,2}`. The benchmark succeeds as a boundary: the next
experiment should leave scalar digit statistics.

Best next question: none on this line; do not start another digit
statistic.

## Publication assessment

Status: `ARCHIVED`.

Supporting evidence that v2 classifies a nonlinear digit fold as the
same regime, not a literature-separated theorem.
