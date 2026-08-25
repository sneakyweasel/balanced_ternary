# Generic control-word obstruction calculus

Status: **EXPLORATORY**

This module is an engine-capability experiment. It is not a Collatz
solver and does not reopen [collatz.md](collatz.md). It consumes
`control_word` certificates only. There is no
`research.control_obstruction` package.

## Problem

Can Research Engine v2 reason symbolically about the remainder
\(C(\mathbf{k})\) of a multi-step control word and use that structure
to eliminate an entire infinite class of configurations?

## Exact statement

Given a certified family and composed cycle constraint
\(D(\mathbf{k})x=C(\mathbf{k})\), prove
\(\forall\mathbf{k}\in\mathcal C\), no integer \(x\) satisfies the
constraint, where \(\mathcal C\) may be infinite, without enumerating
its members. Distinguish `WORD` / `CLASS` / `SYMBOLIC_CLASS` and never
infer impossibility from a finite search miss.

## Current literature

- Length-one Collatz/Syracuse cycle conditions
  \((2^k-3)x=1\) and the finite list of candidate \(k\): **KNOWN**.
- Growth \(|2^K-3^m|>|C|\) as a cycle obstruction: **KNOWN**.
- Integer solvability of \(ax=b\): **KNOWN**.
- Control-word composition in this laboratory:
  [control_word_composition.md](control_word_composition.md).

Project relationship: **new generic engine capability**. Syracuse
identities obtained as instances are not new mathematics.

## Branch budget

```text
Mathematical target     Can a symbolic remainder yield an infinite
                        class obstruction for m≥2?
Novelty hypothesis      Last-control independence plus |D|>|C| as a
                        generic class, not a new cycle theorem.
Falsifier               Enumeration billed as symbolic; total m=2
                        emptiness claimed despite dividing words;
                        Syracuse-specific remainder code.
Existing machinery      control_word composition; length-1 divisor
                        class; not_dvd_of_abs_gt.
Maximum Phase-0 scope   symbolic last-k class + synthetics A–F +
                        Lean remainder/bound; Syracuse as consumer.
Promotion criterion     Infinite class, genuinely symbolic, survives
                        counterexample-first, Lean-certified, reused
                        off Syracuse.
Stop criterion          Only enumerated C; Collatz escalation.
```

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(ax=b\) iff \(a\mid b\). **EXACT — LEAN VERIFIED**
  (`exists_mul_eq_iff_dvd`).
- \(\lvert a\rvert>\lvert b\rvert\) and \(b\neq 0\) imply \(a\nmid b\).
  **EXACT — LEAN VERIFIED** (`not_dvd_of_abs_gt`).
- Cycle constraint implies \((A-B)\mid C\). **EXACT — LEAN VERIFIED**
  (`cycle_constraint_dvd`).
- Last-step remainder \(C'=pC+rA\) is independent of the last
  multiplier. **EXACT — LEAN VERIFIED** (`last_step_remainder`).
- If \(|C|<|A-B|\) and \(C\neq 0\), no integer cycle solution.
  **EXACT — LEAN VERIFIED** (`cycle_abs_obstruction`).
- Length-1 family \((b^k-p)x=r\): possible \(k\) are a finite divisor
  class. **EXACT** on \(\mathbb{Z}\) for the relation, not a map theorem.

## Experiments

- `tests/research_engine/core/test_control_obstruction.py`
- Syracuse consumer: `tests/research/syracuse/test_syracuse.py`

## Conjectures

None opened.

## Counterexamples

- Finite-window miss of the even-branch candidate \(x=100\) for
  \(x\mapsto 2x+(x\bmod 2)-100\) is not an obstruction.
- “All length-2 words are impossible” on power-clear \(2^k y=x+1\) is
  `REFUTED` by \((k_0,k_1)=(1,1)\). The class is refined to last
  \(k\ge 2\) and \(C\neq 0\), not silently weakened.
- Prefixes with \(C=0\) are excluded from the last-\(k\) class: the
  constraint becomes \(Dx=0\).

## Formalization

`formal/Problems/Engine/ControlObstruction.lean`. Thin Syracuse
instances `syracuse_len_one_cycle_dvd`, `syracuse_last_step_remainder`,
`syracuse_cycle_abs_obstruction`. No `sorry`. No ledger row.

## Results

### A. Generic capability

`control_obstruction` after `control_word`. Consumes family, composed
relations, and cycle constraints. Does not duplicate composition: it
evaluates `compose_affine_steps` on the certified one-step law
\((b^k,p,r)\). Scopes:

```text
WORD | CLASS | SYMBOLIC_CLASS
```

`ControlWord` source is unchanged. `AttackContext.affine` is not
injected.

### B. Symbolic remainder

For a certified power family, after a prefix relation
\(A y=B x+C\), one more step \(a z=p y+r\) produces remainder
\(pC+rA\), independent of \(a\). That identity is the only symbolic
operation required by the benchmark. It is not a computer algebra
system.

### C. Control summaries

Discovered from composition, not seeded:

```text
ControlWordSummary
    variables: prefix, length (remainder independent of last k)
    exact relation: C(prefix+(k,)) = p*C_prefix + r*A_prefix
    evidence: compose_affine_steps on probed last values; Lean last_step_remainder
```

Whether \(A=b^{\sum k_i}\) and \(B=p^m\) is still inferred from
composed coefficients.

### D. Obstruction classes

| Mode | Mechanism |
|------|-----------|
| `WORD_DIVISIBILITY` | a single \((A,B,C)\) fails \(D\mid C\) |
| `CLASS_DIVISIBILITY` | length-1 divisor complement; modular length-\(m\) with fixed \((A,B)\) |
| `SYMBOLIC_DIVISIBILITY` | last \(k\ge k_{\min}\) and \(C\neq 0\) forces \(\lvert D\rvert>\lvert C\rvert\) |

Also: domain suffix, sign off-domain, bound. Statuses
`CANDIDATE` / `REFUTED` / `FINITE_RANGE_SUPPORTED` /
`SYMBOLICALLY_PROVED` / `PROVED` / `LEAN_CERTIFIED` stay separate from
`REALIZABLE` / `IMPOSSIBLE` / `UNKNOWN`.

### E. Synthetic validation

| Target | Ground truth | Discovered |
|--------|--------------|------------|
| A infinite last-\(k\) | \(2^k y=x+1\), \(m=2\), last \(k\ge 2\) empty | `SYMBOLIC_CLASS` bound, \(k_{\min}=2\) |
| B exceptions | \((1,1)\) divides; not in the last-\(k\) class | `REFUTED` total \(m=2\); exceptions outside class |
| C length parity | \(2^k y=1-x\): odd \(m=1\) empty, even \(m=2\) last-\(k\) | CLASS empty odd; `SYMBOLIC_CLASS` even |
| D summary | \(C\) independent of last \(k\) | `remainder_independent_of_last` |
| E trap | finite samples suggest total emptiness | `REFUTED` by \((1,1)\); class not claimed total |
| F realizable | \(2^k y=x\), \(C\equiv 0\) | no last-\(k\) obstruction |

Length-1 CLASS results from the previous phase remain: power-clear
`possible_k=(1,)`; odd-prime empty; later \(k=0\) domain; sign; window
miss is not impossibility.

### F. Counterexample record

- All length-2 impossible on \(2^k y=x+1\): **REFUTED**, witness
  \((1,1)\).
- Last-\(k\) class including \(C=0\): **REFUTED** by the identity
  \(Dx=0\). Class restricted to \(C\neq 0\).
- Window miss of candidate \(100\): not an obstruction.

### G. Syracuse

Consumer only. Same attack, no seeded moduli. Length-1 divisor class
\(k\in\{1,2\}\) remains. For \(m=2\), the generic last-\(k\) bound
gives \(k_{\min}=4\) on \(2^k y=3x+1\): an infinite class of last
controls is symbolically obstructed. **KNOWN** growth, not a Collatz
theorem. Fingerprint `SYMBOLIC_CLASS`. Outcome A as *capability*.
Does not exclude all nontrivial cycles.

### H. Lean

Generic: `last_step_remainder`, `two_step_remainder`,
`cycle_abs_obstruction`, plus the previous divisibility lemmas.
Syracuse: `syracuse_last_step_remainder`,
`syracuse_cycle_abs_obstruction`. No ledger: mathematics is **KNOWN**.

### I. ResearchLoop

Non-core `latent_control_obstruction`:
`UNOBSERVED|NONE|WORD|CLASS|SYMBOLIC_CLASS`.
Capabilities `control_obstruction_calculus` and
`symbolic_multi_step_obstruction`. Digit-fold cores unchanged.
`WeightDrift` remains outside that family. Syracuse remains `PARK`.
Engine `CONTINUE` when a symbolic class obstruction is proved; map
globality empirical. Dossier `PARK`.

### J. ComplexityProfile

Unchanged schema. Evidence carries `symbolic_count`, `k_min`,
`length`, `symbolic=True`. No new profile dimension.

### K. Prior art

| Class | Item |
|-------|------|
| KNOWN MATHEMATICS | \(ax=b\) iff \(a\mid b\); last-step remainder; \(\lvert D\rvert>\lvert C\rvert\Rightarrow D\nmid C\); length-one Syracuse \(k=1,2\); growth bounds on multi-step Collatz cycles |
| ENGINE REDISCOVERY | those identities from a certified family and composition |
| NEW GENERIC ENGINE CAPABILITY | symbolic remainder \(\to\) infinite last-\(k\) class without enumerating words |
| POTENTIALLY NEW MATHEMATICS | none claimed |

### L. Final research decision

```text
CONTINUE
```

Dossier mapping: `PARK`. Not `ESCALATE`. Not `ENGINE_LIMITATION`.
Not `CLOSE`: the last-\(k\) class is a real symbolic capability, but
gcd/modular projections of a fully symbolic \(C(\mathbf{k})\) and
recursive remainder invariants remain unbuilt.

## Open questions

Can \(\gcd(D(\mathbf{k}),C(\mathbf{k}))\) or a modular projection of
\(C\) be derived as a symbolic function of the whole word, not only
via last-control dominance?

## Decision

`PARK`. v2 can eliminate an infinite multi-step class from the
symbolic remainder of a certified family. The Syracuse instance is
**KNOWN** growth. Map globality, full cycle exclusion, and arbitrary
summaries of \(C\) are not proved. Do not auto-continue. Do not reopen
`research.collatz`.

Best next question: can a recursive remainder invariant obstruct a
class where \(\lvert D\rvert\) does not dominate \(\lvert C\rvert\)?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as number theory.
