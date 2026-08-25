# Balanced-ternary weight-drift dynamics

Status: **ARCHIVED**

First v2 benchmark in which a balanced-ternary statistic **perturbs**
the integer state rather than replacing it. Does not reopen signed-digit,
Collatz, primes, jets, Ostrowski, `{S,N,D,W}`, `N∘I_0∘D`, digit-sum
dynamics, or weight dynamics.

CLI `btlab research analyze|attack|reproduce|report balanced_ternary_weight_drift`
(aliases `weight_drift`, `btdrift`, `wdr`).

## Problem

Can Research Engine v2 diagnose the structural regime of
`T(n)=n+W(n)` from exact local digits alone, without being told that
the statistic is an increment, a Lyapunov, or a Hamming weight?

## Exact statement

### A. Exact target

For the canonical expansion `n=∑ d_i 3^i`, `d_i∈{-1,0,+1}`,

`W(n)=∑_i d_i²`,

and

`F(n)=n+W(n)`,

equivalently `n_{t+1}=n_t+W(n_t)`.

## Current literature

- `oeis-A005812`: the statistic `W` on `ℕ`. `KNOWN`.
- `oeis-A062028`, Kaprekar self-numbers: the generator `n ↦ n+s(n)` in
  an ordinary base. `KNOWN` as a class.
- `oeis-A134452` / closed digit-sum and weight dossiers: replacement
  maps `n ↦ s(n)` and `n ↦ W(n)`, the finite-contracting regime this
  experiment is designed to leave. `KNOWN`.

The novelty question is the dynamical classification of `n ↦ n+W(n)`,
not the definition of `W`.

## Branch budget

```text
Mathematical target     Can v2 diagnose the regime of F(n)=n+W(n),
                        where W perturbs rather than replaces n?
Novelty hypothesis      A growth / sign-split / generator regime
                        distinct from digit-fold contraction; or a
                        CLOSE as Kaprekar-class reparameterization.
Falsifier               The adapter is fed monotonicity, a residue,
                        Hamming weight, an attractor, or a Lyapunov;
                        or F rewrites to W, s, or a contracting fold.
Existing machinery      ProblemSpec, AttackPlanner, CertificateKind,
                        ComplexityProfile; lsd, D, weightZ; closed
                        SignedP0, s(n), and W(n) dossiers.
Maximum Phase-0 scope   One integer adapter; generic planner; bounded
                        seeds; one Lean theorem if an identity survives.
Promotion criterion     A structurally new invariant, quotient, or
                        reusable engine abstraction beyond n+f(n).
Stop criterion          The map is the classical generator class
                        n ↦ n+f(n) with f a nonnegative digit statistic;
                        machinery gravity; or INCONCLUSIVE with no
                        compact residual and no exact identity.
```

## Balanced-ternary formulation

`W` is the fold of squared local trits. Observation is the integer
state. Controls are a dummy singleton. The digit vector is not state.

## Why BT may be relevant

The increment is computed from already-certified local operators. The
architectural change is state-preserving perturbation.

## Candidate operations / invariants

- `F(n)=n+W(n)`. **EXACT — LEAN VERIFIED** (`weightDriftZ`)
- `n ≠ 0 ⇒ n < F(n)`. **EXACT — LEAN VERIFIED** (`weightDriftZ_gt`)
- `n ≤ 0 ⇒ F(n) ≤ 0`. **EXACT — LEAN VERIFIED** (`weightDriftZ_nonpos`)
- `n < 0 ⇒ |F(n)| < |n|`. **EXACT — LEAN VERIFIED**
- `n ≤ 0 ⇒ F^{|n|}(n)=0`. **EXACT — LEAN VERIFIED**
- `n > 0 ⇒ n+k ≤ F^k(n)`. **EXACT — LEAN VERIFIED**
- unique fixed point `0`. **EXACT — LEAN VERIFIED**
- box `|n|≤2` invariant. **REFUTED** (`F(2)=4`)
- `V(n)=n` Lyapunov decrease. **REFUTED**
- `F` even. **REFUTED** (`F(-1)=0 ≠ 2=F(1)`)
- `F²=F`. **REFUTED**
- disjoint forward orbits. **REFUTED** (`4` and `5` meet at `8`)
- identity observation merges orbit points. **REFUTED**
- finite residual of seed `4`. **REFUTED**

## Experiments

- `btlab research analyze|attack|reproduce|report balanced_ternary_weight_drift`
- Discovery: `src/research/balanced_ternary_weight_drift/discovery.py`
- Tests: `tests/research/balanced_ternary_weight_drift/test_weight_drift.py`
- Records in `experiments/balanced_ternary/weight_drift/`

### B. Adapter

Integer state `(n,)`, dummy control `0`, identity observation
`obs(n)=n`, transition `n ↦ n+W(n)` via the `lsd²`/`D` fold. No reverse
preimages, no symmetry candidates, no `affine_system`, no
`raw_contribution`. Candidate box `|n|≤2` is a generic envelope probe.
Horizon-only accepting predicate. No monotonicity or Hamming-weight
name is installed.

### C. Planner trace

| attack | status | reason |
|--------|--------|--------|
| reconnaissance | OBSERVATION | bounded countdown census |
| closure | INCONCLUSIVE | residual BFS hits the state cap; not infinitude |
| functional | REFUTED | `|n|` increases on the start layer (`4 ↦ 6`) |
| affine | REFUTED | box `|n|≤2` leaks at `F(2)=4` |
| separation | EXACT | `4` and `6` distinguished by identity observation |
| quotient | INCONCLUSIVE | no exact finite reachable set |
| modular, spectral, block, factorization, reverse, symmetry | skipped | inapplicable |
| symbolic | skipped | not implemented |

## Conjectures

None opened.

## Counterexamples

- `|F(n)|<|n|` for `|n|≥2`: `F(2)=4`.
- Box `|n|≤2` invariant: `F(2)=4`.
- `F` even: `F(-1)=0 ≠ 2=F(1)`.
- `F²=F`: `F(1)=2 ≠ 2+2=F(2)`.
- Disjoint orbits: `4 ↦ 6 ↦ 8` and `5 ↦ 8`.
- `V(n)=n` strictly decreases: `F(0)=0`.
- Finite residual of seed `4`: `F(n)>n` for `n≠0`.

No counterexample to `n≠0 ⇒ F(n)>n` or to `n≤0 ⇒ F(n)≤0` on `|n|≤80`.

## Formalization

`formal/Problems/BalancedTernary/WeightDrift.lean`. No `sorry`.
Theorems `weightDriftZ_gt`, `weightDriftZ_nonpos`,
`weightDriftZ_natAbs_lt_of_neg`, `weightDriftIterate_reaches_zero`,
`weightDriftIterate_ge_add`.

No theorem-ledger row: `n ↦ n+W(n)` is the Kaprekar generator class
with `W=A005812` (`KNOWN` / `REPARAMETERIZATION`).

## Results

### D. Orbit analysis

- Seed `4`: `4,6,8,…` strictly increasing (finite-horizon exact prefix;
  universal exact by `weightDriftIterate_ge_add`).
- Seed `5`: `5,8,…`; meets the orbit of `4` at `8`.
- Seed `-4`: `-4,-2,0` then stays (`EXACT — LEAN VERIFIED`).
- Unique cycle `{0}`.

### E. Invariants and envelopes

- Nonpositive ray invariant; nonnegative ray invariant.
- Increment `F(n)-n=W(n)≥0`, and `≥1` off zero.
- Box `|n|≤2` is **not** invariant.

### F. Reachability

- Positive seed: residual BFS hits the cap (`complete=False`). Not a
  proof of infinitude by itself; infinitude is the Lean inequality.
- Distinct seeds may merge (finite-horizon exact: `4` and `5` at `8`).
- Identity observation still separates distinct integers immediately.

### G. Behavioral analysis

No finite exact quotient on the positive seed: quotient requires an
exact finite reachable set. Identity observation forbids a nontrivial
Mealy merge of distinct integers in any case.

### H. Block dynamics

Inapplicable (no affine system, singleton control). No block identity
was selected by the engine.

### I. Comparative diagnosis

`F(n)=n+W(n)` **leaves the finite-contracting digit-fold regime** on
positive seeds. The replacement architecture

```text
recursive digit fold → magnitude compression → finite per-seed closure
```

is replaced by

```text
recursive digit fold as increment → strict increase off 0
    → inconclusive residual closure on positives
    → finite contraction to 0 on nonpositives
```

| Dimension | `SignedP0` | `s(n)` | `W(n)` | `n+W(n)` |
|-----------|------------|--------|--------|----------|
| Transition type | word `N∘I_0∘D` | signed fold | squared-trit fold | state plus squared-trit fold |
| Compression | `F²=P_0` | `|s|<\|n\|` for `|n|≥2` | `|W|<\|n\|` for `|n|≥3` | none on `n>0`; `|F|<\|n\|` for `n<0` |
| Seed-4 closure | exact, size 3 | exact, size 3 | exact, size 2 | **INCONCLUSIVE** (cap) |
| Recurrent structure | orbits ≤3 | `{-1,0,1}` | `{0,1,2}` | unique fp `{0}`; positives unbounded |
| Functional `|n|` | observation | observation | observation | **REFUTED** (growth) |
| Box `|n|≤2` | leaks | invariant | invariant | **leaks** (`F(2)=4`) |
| Behavioral quotient | sign merge | identity `M=\|R\|` | identity `M=\|R\|` | no finite quotient (incomplete `R`) |
| Lean | `signedP0_sq_eq_P0` | `digitSumZ_natAbs_lt` | `weightZ_natAbs_lt` | `weightDriftZ_gt` |

v2 discovered the regime split without being told it: cap-inconclusive
closure, a refuted `|n|` bound, and a leaking box. The Lean theorems
are the universal certificate that the engine's cap is, in this case,
genuine divergence on positives and genuine contraction on negatives.

### J. Lean

If `n ≠ 0` then `n < n+W(n)`; if `n ≤ 0` then `F^{|n|}(n)=0`. File
`Problems.BalancedTernary.WeightDrift`.

### K. Prior art

`W` is A005812. The generator `n ↦ n+s(n)` is Kaprekar / A062028.
Engine rediscovery: inconclusive positive closure, orbit merge of `4`
and `5`, sign split. New formalization in this repository:
`weightDriftZ_*`. Not new mathematics.

### L. ComplexityProfile

Seed `4`: controls 1; raw contribution unset; envelope 5; reachable
prefix `state_cap+1`; closure `INCONCLUSIVE`. Finite-horizon exact for
the leaking box and the `4`/`5` merge; universal exact for increase and
nonpositive contraction (Lean). The cap is not an infinitude certificate.

### M. Infrastructure verdict

```text
NO ENGINE CHANGE
```

Hitting the residual cap is already documented as not infinitude. The
universal facts are elementary inequalities, not a missing generic
drift primitive.

### N. Branch decision

```text
CLOSE
```

A new v2 **diagnosis** relative to `SignedP0`/`s`/`W` (drift, not
fold-contraction), but the mathematics is the classical `n+f(n)`
generator class. Do not enumerate `n+s(n)` or another scalar
digit-statistic perturbation.

## Open questions

Nothing on this line.

## Decision

`CLOSE`. The experiment succeeded as a control: v2 reports
inconclusive closure and a refuted `|n|` bound when the statistic is
an increment. The exact theorems are Kaprekar-type generator facts for
`W=A005812`, not a new class. Next experiment should leave scalar
digit-derived maps.

Best next question: none on this line; do not start another
digit-statistic perturbation.

## Publication assessment

Status: `ARCHIVED`.
