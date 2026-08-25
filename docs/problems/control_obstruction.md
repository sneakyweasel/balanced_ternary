# Generic control-word obstruction calculus

Status: **EXPLORATORY**

This module is an engine-capability experiment. It is not a Collatz
solver and does not reopen [collatz.md](collatz.md). It consumes
`control_word` certificates only. There is no
`research.control_obstruction` package.

## Problem

Can exact symbolic constraints from certified control-word composition
yield generic arithmetic obstructions that exclude a *class* of control
configurations, not merely individual enumerated words?

## Exact statement

Given a prior `control_word` result — composed relations
\(A x_m = B x_0 + C\) and cycle constraints \((A-B)x=C\) — does
`control_obstruction` derive divisibility, gcd, modular, bound, sign,
or domain contradictions, distinguish `WORD` from `CLASS` scope, and
refuse to treat a finite search miss as `IMPOSSIBLE`?

## Current literature

- Length-one Collatz/Syracuse cycle conditions
  \((2^k-3)x=1\) and the finite list of candidate \(k\): **KNOWN**.
- Integer solvability of \(ax=b\): **KNOWN**.
- Control-word composition in this laboratory:
  [control_word_composition.md](control_word_composition.md).

Project relationship: **new generic engine capability**. Syracuse
identities obtained as instances are not new mathematics.

## Branch budget

```text
Mathematical target     Can exact composed constraints yield class-level
                        arithmetic obstructions?
Novelty hypothesis      Constraint-to-obstruction calculus, not a new
                        cycle theorem.
Falsifier               Seeded moduli; search failure billed as
                        IMPOSSIBLE; AffineSystem injection.
Existing machinery      control_word; (A-B)x=C; subsequent_k_impossible.
Maximum Phase-0 scope   control_obstruction + synthetics A–F + Lean of
                        generic non-divisibility; Syracuse as consumer.
Promotion criterion     At least one class-level obstruction proved
                        generically and Lean-certified.
Stop criterion          Only word-level refutations; Collatz escalation.
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
- Length-1 family \((b^k-p)x=r\): possible \(k\) are a finite divisor
  class. **EXACT** on \(\mathbb{Z}\) for the relation, not a map theorem.

## Experiments

- `tests/research_engine/core/test_control_obstruction.py`
- Syracuse consumer: `tests/research/syracuse/test_syracuse.py`

## Conjectures

None opened.

## Counterexamples

- Finite-window miss of the even-branch candidate \(x=100\) for
  \(x\mapsto 2x+(x\bmod 2)-100\) is not an obstruction (synthetic F).
- A divisor-class claim is `REFUTED` if an enumerated word outside the
  predicted \(k\)-set still divides.

## Formalization

`formal/Problems/Engine/ControlObstruction.lean`. Thin Syracuse
instance `syracuse_len_one_cycle_dvd`. No `sorry`. No ledger row.

## Results

### A. New generic attack

`control_obstruction` after `control_word`. Consumes family, composed
relations, cycle constraints, realizability, and the existing quotient.
Does not inspect target names. `AttackContext.affine` is not injected.
`ControlWord` source is unchanged.

### B. Obstruction classes

divisibility, gcd, modular, bound, sign, domain. Scope `WORD` or
`CLASS`. Statuses `REFUTED` / `SEARCH_SUPPORTED` / `OBSTRUCTION_CANDIDATE`
/ `PROVED` / `LEAN_CERTIFIED` stay separate from realizability.

### C. Synthetic validation

| Target | Ground truth | Discovered |
|--------|--------------|------------|
| A power-clear | length-1 cycle only for \(k=1\) | CLASS divisibility, `possible_k=(1,)` |
| B parity-carry | length-2 needs \((A-B)\mid C\) | CLASS modular; blocked and allowed words |
| C odd-prime clear | no length-1 cycle | CLASS divisibility, `empty=True` |
| D later \(k=0\) | coprime images | CLASS domain |
| E positive double | candidate \(-1\) off domain | WORD sign |
| F large parity | even-branch candidate \(100\) off window | not classified impossible |

### D. Control-word interaction

Summaries are *discovered* from composed coefficients (whether \(A\) is
a power of the family base with exponent \(\sum k_i\), whether \(B=p^m\)).
Obstructions run once per \((A,B,C)\) quotient class.

### E. Family-level versus word-level

CLASS: divisor complement of length-1 cycles; modular condition on all
length-\(m\) words with fixed \((A,B)\); later-parameter domain class.
WORD: a single composed triple fails to divide, or its candidate is
outside `legal_controls`. Search miss remains `UNKNOWN`.

### F. Syracuse

Consumer only. Length-1 cycle requires
\((2^k-3)\mid 1\), hence \(k\in\{1,2\}\) as a divisor class. **KNOWN**.
Engine status: class obstruction `PROVED` / `LEAN_CERTIFIED`. Not a
global cycle theorem. Outcome A as *capability*; mathematics is known.

### G. Genericity

Odd-prime clear (\(3^k y=x+1\)) has an empty length-1 divisor class.
The same attack, no Syracuse constants.

### H. Lean

`exists_mul_eq_iff_dvd`, `not_dvd_of_abs_gt`, `cycle_constraint_dvd`.
Syracuse: `syracuse_len_one_cycle_dvd`.

### I. ResearchLoop

Non-core `latent_control_obstruction`: `NONE|CANDIDATE|PROVED`.
Capability `control_obstruction_calculus`. Digit-fold cores unchanged.
Engine `CONTINUE` when a class obstruction is proved; map globality
empirical. Dossier `PARK`.

### J. ComplexityProfile

Unchanged. Counts on evidence: `class_count`, `word_count`,
`certificate_count`.

### K. Prior art

| Class | Item |
|-------|------|
| KNOWN MATHEMATICS | \(ax=b\) iff \(a\mid b\); length-one Syracuse candidates \(k=1,2\) |
| ENGINE REDISCOVERY | those identities from a generic divisor class |
| NEW GENERIC ENGINE CAPABILITY | constraint \(\to\) class obstruction with WORD/CLASS split |
| POTENTIALLY NEW MATHEMATICS | none claimed |

### L. Final research decision

```text
CONTINUE
```

Dossier mapping: `PARK`. Not `ESCALATE`. Not `ENGINE_LIMITATION`.

## Open questions

Can class-level obstructions for \(m\ge 2\) be proved symbolically in
the remainder \(C(\mathbf{k})\) without enumerating words?

## Decision

`PARK`. The engine can eliminate whole exponent classes for length-one
cycles from a certified family. Longer-word family emptiness is still
mostly word-level or modular-on-enumerated-C. Do not auto-continue.
Do not reopen `research.collatz`.

Best next question: can the remainder of a composed word be summarized
well enough to prove emptiness of an infinite \(m\ge 2\) class?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as number theory.
