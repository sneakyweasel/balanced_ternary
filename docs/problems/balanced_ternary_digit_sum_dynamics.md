# Balanced-ternary digit-sum dynamics

Status: **ARCHIVED**

First v2 benchmark of an integer map whose transition is a recursive
digit fold rather than a fixed operator word. Does not reopen
signed-digit, Collatz, primes, jets, Ostrowski, the archived
`{S,N,D,W}` census, `N∘I_0∘D`, or polynomial level sets of
`s_bal(P(n))`.

CLI `btlab research analyze|attack|reproduce|report balanced_ternary_digit_sum_dynamics`
(aliases `digit_sum`, `btds`, `ds_dynamics`).

## Problem

Can Research Engine v2 diagnose the global regime of
`T(n)=s(n)` from exact local digits `lsd` and `D` alone?

## Exact statement

### A. Target definition

For every integer `n` write the canonical balanced-ternary expansion
`n = ∑_{i≥0} d_i 3^i` with `d_i ∈ {-1,0,+1}`. Define

`s(n) = ∑_{i≥0} d_i`,

equivalently the recursive fold `s(0)=0` and
`s(n)=lsd(n)+s(D(n))` for `n≠0`. The dynamical system is
`n_{t+1} = s(n_t)`.

## Current literature

- `oeis-A065363`, `ruskey-sawada-2009-digital-sum-gf`: the sequence
  `s_bal` itself. `KNOWN`.
- `oeis-A134452`: balanced-ternary digital root, the iteration of
  A065363 until the value lies in `{-1,0,1}`. Comments record
  `|a(n)| = n mod 2`. Knuth, TAOCP Vol. 2. `KNOWN`.
- Ordinary digital roots (base `q`) are classical: iteration of the
  digit sum contracts to a residue modulo `q-1`. `KNOWN`.
- `docs/problems/balanced_digit_sum_polynomials.md`: level sets
  `s_bal(P(n))=0`. A different object; stays closed.

## Branch budget

Written before substantial implementation.

```text
Mathematical target     Can v2 diagnose the structural regime of T(n)=s(n)
                        from exact local digit semantics, without a
                        problem-specific theory in advance?
Novelty hypothesis      Either a new finite/observational class, or an
                        exact obstruction, or a correct CLOSE as the
                        known digital-root iteration of s_bal.
Falsifier               The adapter is fed an attractor, Lyapunov, modulus,
                        digit-length bound, or quotient; or T rewrites to
                        n, -n, 3n+a, or D(n).
Existing machinery      ProblemSpec, AttackPlanner, CertificateKind,
                        ComplexityProfile, envelope vs reachable,
                        separate_states, Mealy quotient; lsd, D, s_bal
                        already in bt; polynomial digit-sum dossier stays
                        closed.
Maximum Phase-0 scope   One integer adapter; generic planner; bounded
                        seeds; one proof if a concrete identity appears;
                        one Lean theorem.
Promotion criterion     Exact residual/orbit/obstruction theorem the
                        engine found, not a restatement of A134452.
Stop criterion          Rewrite collapse; machinery gravity; KNOWN
                        digital-root algebra; or INCONCLUSIVE with no
                        compact residual.
```

## Balanced-ternary formulation

`T` is the fold of the canonical word. Observation is the integer
state itself. Controls are a dummy singleton.

## Why BT may be relevant

The local operators are the calculus. The question is whether generic
attacks see the contraction geometry without being told a digital root.

## Candidate operations / invariants

- `s(n)=lsd(n)+s(D(n))`. **EXACT — LEAN VERIFIED** (`digitSumZ_rec`)
- `|s(n)| < |n|` for `|n|≥2`. **EXACT — LEAN VERIFIED**
- `s(n)=n` iff `|n|≤1`. **EXACT — LEAN VERIFIED**
- every orbit reaches `|n|≤1` in at most `|n|` steps. **EXACT — LEAN VERIFIED**
- `V(n)=n` is a Lyapunov. **REFUTED** (`T(0)=0`)
- `T²=T`. **REFUTED** (`T(4)=2`, `T(2)=0`)
- identity observation merges distinct orbit points. **REFUTED**
- `ℤ` is a single finite residual. **REFUTED** (orbits of 4 and 5)
- the box `|n|≤2` leaks. **REFUTED** as a leak claim; the 5-point box
  is closed. **EXACT** as a finite check, not a new class

## Experiments

- `btlab research analyze|attack|reproduce|report balanced_ternary_digit_sum_dynamics`
- Discovery: `src/research/balanced_ternary_digit_sum_dynamics/discovery.py`
- Tests: `tests/research/balanced_ternary_digit_sum_dynamics/test_digit_sum_dynamics.py`
- Records in `experiments/balanced_ternary/digit_sum_dynamics/`

### B. Adapter

Integer state `(n,)`, dummy control `0`, identity observation
`obs(n)=n`, transition the `lsd`/`D` fold. `affine_system()` is
`None`. No `raw_contribution`. No reverse preimages (infinitely many).
No symmetry candidates. Candidate box `|n|≤2` is a generic envelope
probe, not an installed attractor. Terminal/accepting uses only the
countdown horizon.

### C. Planner trace

| attack | status | reason |
|--------|--------|--------|
| reconnaissance | OBSERVATION | bounded census |
| closure | SUPPORTED EXACT | seed orbit of 4 has size 3, `EXACT_CLOSURE` |
| functional | OBSERVATION | sample bound, not a Lyapunov |
| affine | OBSERVATION | box `|n|≤2` has no live one-step leak |
| separation | EXACT | seed vs image distinguished by identity observation |
| quotient | SUPPORTED EXACT | `M=\|R\|=3` on the seed orbit |
| modular, spectral, block, factorization, reverse, symmetry | skipped | inapplicable |
| symbolic | skipped | not implemented |

## Conjectures

None opened.

## Counterexamples

### E. Falsification record

- `T²=T`: `T(4)=2 ≠ 0 = T(T(4))`.
- `V(n)=n` strictly decreases: `T(0)=0`.
- Global finite residual: orbits `{4,2,0}` and `{5,-1}` are disjoint.
- Identity-observation merge: `4` and `2` separate immediately.
- `|T(n)| ≥ |n|` for `|n|≥2`: no counterexample on `|n|≤80`; Lean
  `digitSumZ_natAbs_lt` is the universal statement.
- Interval leak of `|n|≤2`: none. Finite exhaustive check.

## Formalization

`formal/Problems/BalancedTernary/DigitSumDynamics.lean`. No `sorry`.
Theorems `digitSumZ_rec`, `digitSumZ_natAbs_lt`,
`digitSumZ_eq_self_iff`, `digitSumIterate_reaches_unit`.

No theorem-ledger row: the identities are the known digital root
(`KNOWN` / branch `REPARAMETERIZATION` of A134452).

## Results

### D. Discovered structure

v2 takes integer state, a dummy control, and identity observation.

- Per-seed residual is finite; `ℤ` is not one finite residual.
- Seed `4` closes as `{4,2,0}`.
- The box `|n|≤2` does not leak. The seed orbit is not that box
  (`4` is extra; `±1` are holes).
- Identity observation yields `M=|R|`; no behavioral merge.
- Reverse/block/modular/spectral/factorization/symmetry stay
  inapplicable. Infinite exact preimages are not a finite reverse map.
- Post-hoc, counterexample-first: `|T(n)|<|n|` for `|n|≥2` survives
  and is Lean-certified.

### F. Behavioral analysis

On the seed orbit of `4`, identity observation distinguishes every
state. Separation depth is `0` or `1` (the first output is the
state). This is exact for that finite Mealy system and is not a
universal quotient of `ℤ`.

### G. Dynamical classification

Infinite disjoint union of finite orbits that contract in magnitude
until `|n|≤1`. Near-projection (digital root), not expanding, not
`P_0`/`N` iteration, not a residual box fill. Primary observation is
the identity of the integer; it contributes no merge.

### H. Lean result

Strongest certified theorem: if `|n|≥2` then `|s(n)|<|n|`, and
`s^{|n|}(n)` has absolute value at most `1`.
File `Problems.BalancedTernary.DigitSumDynamics`, theorems
`digitSumZ_natAbs_lt` and `digitSumIterate_reaches_unit`.

### I. ComplexityProfile

Seed `4`:

- controls 1
- raw contribution unset
- candidate envelope 5 (`|n|≤2`)
- reachable 3
- behavioral / Mealy 3
- graph diameter 2
- max separation depth 0 or 1
- closure `EXACT_CLOSURE`

Versus the reference systems (structural, not numeric identification):

| system | regime |
|--------|--------|
| signed-digit residual | finite residual, interval fill |
| D+Add | finite 3-state carry residual |
| Collatz shortcut | integer BFS cap, expanding block |
| prime observation | sieve finite, primality not a residual |
| `N∘I_0∘D` | disjoint finite orbits, sign merge `M<\|R\|` |
| `T=s` | disjoint finite contracting orbits; identity observation `M=\|R\|` |

### J. Prior-art checkpoint

The map `s` is OEIS A065363. Its iteration to a unit is OEIS A134452,
the balanced-ternary digital root, with `|a(n)| = n \bmod 2`. That is
classical. The engine diagnosis (per-seed closure, non-leaking sample
box, identity Mealy equality, inapplicable reverse/block) is new
experimental evidence about v2, not a literature-separated theorem.

### K. Infrastructure decision

```text
NO ENGINE CHANGE
```

Generic v2 planner reused as-is. Infinite digit-sum preimages were
recorded as reverse inapplicability, not as a new engine primitive.

## Open questions

Nothing on this line. Do not enumerate other digit-fold maps.

## Decision

`CLOSE`. The map is the known balanced-ternary digital root
(A134452), the iteration of the known sequence `s_bal`. v2 diagnosed
finite per-orbit closure, a non-leaking interval sample, and
identity-observation equality `M=|R|` without being told the
attractor. The identities are corollaries of the digit fold, not a
new residual class.

Best next question: none on this line; do not start another digit-fold
word.

## Publication assessment

Status: `ARCHIVED`.

The operator identities were already recorded as A065363 / A134452.
The v2 diagnosis is supporting evidence that the engine classifies a
recursive digit fold, not a literature-separated theorem.
