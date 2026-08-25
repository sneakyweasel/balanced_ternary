# Prime residual complexity in balanced ternary

Status: **ARCHIVED**

This module does **not** claim a primality test, a Collatz result, or a
new theorem that the primes are non-automatic.

CLI `btlab research analyze primes` is this adapter. The parked sparse-prime
enumerator in [primes.md](primes.md) is a different module.

## Problem

When the laboratory's LSD-first section machinery is applied to
primality, what exact residual complexity replaces the finite closure
found for carry dynamics?

## Exact statement

Let `I_a(x)=3x+a` for `a∈{-1,0,1}` be the existing sections. For a
finite sieve `S` with `M=∏_{p∈S}p`, write `P_M(n)=1[gcd(n,M)=1]`. For
the prime predicate write `Prime(n)`. Two residual arguments `x,y` are
distinguished at horizon `H` if some trit word `w` of length at most `H`
has `Prime(I_w(x))≠Prime(I_w(y))`.

Questions:

1. Is `P_M` a finite residual of the trit automaton `δ(n,a)=I_a(n) mod M`?
2. Does a length-`L` LSD jet (equivalently `n mod 3^L`) determine Prime
   continuations?
3. Does `P_M` equal Prime as a residual?
4. What is `R_H(L)`, the number of distinct Prime signatures of
   length-`L` windows at horizon `H`, for `L≤6` and `H≤3`?

## Current literature

Non-automaticity of the primes in a fixed integer base is `KNOWN`
(Cobham / automatic-sequence literature). Finite-modulus coprimality is
a regular language, also `KNOWN`. Dirichlet's theorem supplies primes in
coprime residue classes; this phase does not use it as a proof, only as
background. The parked enumerator [primes.md](primes.md) is unrelated.

This branch `reproduced` the finite-sieve control and `refuted` two
compressions of Prime by explicit section witnesses. It did not extend
the automaticity lower-bound literature.

## Branch budget

- **Target:** growth of the Prime residual under `I_a`, versus the
  finite residual of a fixed modular sieve.
- **Novelty hypothesis:** a BT-native complexity law, a constructive
  family of pairwise distinguishable section-states, or an exact
  sieve-to-prime refinement that is not Cobham restated.
- **Falsifier:** only `n mod 3^k` occupancy, only known
  non-automaticity, or an `R(L)` table with no arithmetic mechanism.
- **Existing machinery:** `ProblemSpec`, `AttackPlanner`, `AffineSystem`
  (`x'=3x+a`), `ExhaustiveClosureAttack`, `minimize_dfa`, `I` /
  `integer_jet` / `encode`, `is_prime` as an inspection helper.
- **Maximum Phase-0 scope:** LSD-first adapter; sieve
  `S={2},{2,3},{2,3,5},{2,3,5,7}`; `R_H(L)` for `L≤6`, `H≤3`;
  counterexample-first jet/sieve compressions; Lean of the strongest
  local lemma only.
- **Promotion criterion:** exact nontrivial `R(L)≥f(L)`, a new
  distinguishable family, or a theorem linking sections to prime-language
  residual refinement beyond modulus arithmetic.
- **Stop criterion:** known non-automaticity restated; unstructured
  growth; ad hoc witnesses only; or pure modulus arithmetic with no BT
  section contribution. Then `PARK` or `CLOSE`.

## Balanced-ternary formulation

Canonical words stay in `bt.representation`. A length-`L` window is
`integer_jet(n,L)`, LSD-first. Continuations prepend new LSD digits by
existing `I_a`. Ordinary ternary `{0,1,2}` is not used.

## Why BT may be relevant

Carry dynamics in this laboratory close on three states. Primality is
the opposing control: an infinite arithmetic predicate. The question is
whether sections `I_a` organise that failure, not whether a finite
automaton for all primes exists.

## Candidate operations / invariants

- Sieve DFA `δ(n,a)=(3n+a) mod M`, accept `gcd(n,M)=1`.
  **EXACT — LEAN VERIFIED** for the congruence law; minimized counts
  **COMPUTATIONALLY VERIFIED**.
- `Prime∘I_0` versus `Prime∘I_{±1}`. `I_0(x)=3x` is composite for
  `|x|>1`. **EXACT — LEAN VERIFIED**. Novelty prose: `KNOWN`.
- Equal length-`L` jets imply equal Prime continuations. **REFUTED**:
  `x=1`, `y=1+3^L`, word `(0,)`.
- Sieve residual equals Prime residual. **REFUTED**: `x=1`, `y=1+M`,
  word `(0,)`, Lean witness `M=210`.
- Integer `n` as a finite Prime residual. Integer-state BFS hits the
  cap (`INCONCLUSIVE`).

## Experiments

- `btlab research analyze|attack|reproduce|report primes`
  (aliases `prime_residual`, `prime_residual_complexity`, `prc`).
  `--remaining` is section depth `L`, default 4, cap 6.
- Adapter tests:
  `tests/research/prime_residual_complexity/test_prime_residual.py`
- Records: `experiments/balanced_ternary/primes/`
- Sieve chain `S={2} ⊂ {2,3} ⊂ {2,3,5} ⊂ {2,3,5,7}` only. No prime-modulus
  sweep.

Sieve census (`COMPUTATIONALLY VERIFIED`):

| `S` | `M` | raw | reachable | minimized | `φ(M)/M` |
|-----|-----|-----|-----------|-----------|----------|
| `{2}` | 2 | 2 | 2 | 2 | 1/2 |
| `{2,3}` | 6 | 6 | 6 | 3 | 2/6 |
| `{2,3,5}` | 30 | 30 | 30 | 14 | 8/30 |
| `{2,3,5,7}` | 210 | 210 | 210 | 94 | 48/210 |

`R_H(L)` among all `3^L` length-`L` windows (`OBSERVATION`, `BOUNDED`;
not a growth law):

| `H\\L` | 1 | 2 | 3 | 4 | 5 | 6 |
|--------|---|---|---|---|---|---|
| 1 | 2 | 5 | 7 | 7 | 7 | 7 |
| 2 | 3 | 6 | 14 | 31 | 48 | 49 |
| 3 | 3 | 6 | 15 | 42 | 122 | 360 |

Horizon-1 signatures saturate at 7 for `L≥3`. Horizon-3 is still growing
at `L=6` (`360` of `729` windows). No asymptotic is fitted.

## Conjectures

None opened.

## Counterexamples

- Jet compression: `n=1` and `n=4` share `integer_jet(-,1)=(1,)`;
  `I_0(1)=3` is prime and `I_0(4)=12` is composite. Same pattern for
  every `L≥1` with `y=1+3^L`.
- Sieve compression: `n=1` and `n=211` share residue `1 mod 210`;
  `I_0(1)=3` is prime and `I_0(211)=633` is composite.
- One-step Lyapunov `V(n)=n` on sections: `|I_1(n)|` expands.

## Formalization

`formal/Problems/Primes/Residual.lean`. No `sorry`. Wraps existing
`IZ`. Does not embed the Python search. Does not formalize Dirichlet or
non-automaticity.

## Results

- `SieveSpec` reuses the generic planner with `AffineSystem` `A=((3,),)`,
  translations `b_a=(a,)`. Modular forcing gcd is `1` (no primality
  residue law). Spectral companion of `A` is not a monic cubic.
- Sieve closure from `0` on `Z/210Z` is `EXACT` size 210. Integer Prime
  closure hits the cap (`INCONCLUSIVE`).
- The distinguishing mechanism is the zero section: `I_0` forces
  divisibility by 3. That is elementary, not a new residual calculus.
- Claim level: Control A (finite sieve) succeeded. Control B (Prime)
  produced exact separators that are `KNOWN` arithmetic. No
  `R(L)≥f(L)` law.

## Open questions

None opened by this phase. Do not auto-start a second prime phase.

## Decision

`CLOSE`. The engine reused the generic attack stack and produced an
exact finite sieve residual together with constructive Prime separators
`x=1`, `y=1+M` (or `y=1+3^L`) via `I_0`. Those statements are `KNOWN`
elementary divisibility, packaged in section language. The `R_H(L)`
table is a bounded observation without a mechanism. A branch whose
surviving exact statements are `KNOWN` or `REPARAMETERIZATION` of
modulus arithmetic is a `CLOSE`. Non-automaticity of primes was not
re-proved and is not claimed.

Best next question: none from this branch. The parked sparse-prime
enumerator remains PARK; do not grow it from this CLOSE.

## Publication assessment

Status: `ARCHIVED`. Not a `PAPER_CANDIDATE`. The Lean lemmas are exact
and independently checkable; their novelty is `KNOWN`.
