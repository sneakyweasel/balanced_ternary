# Generic control-word composition

Status: **EXPLORATORY**

This module is an engine-capability experiment. It is not a Collatz
solver and does not reopen [collatz.md](collatz.md). Certified one-step
families are consumed as abstract certificates. There is no
`research.control_word` application package.

## Problem

Can a certified latent affine family

\[
A(k)\,y = B(k)\,x + C(k)
\]

with an exact parameter domain become a reusable multi-step reasoning
language, without being told the map law, the parameter meaning, or a
cycle equation?

## Exact statement

Given a prior `parameter_domain` certificate, does `control_word`
compose symbolic parameter sequences into an exact cleared relation
\(A x_m = B x_0 + C\), distinguish algebraic composition from
realizability, propagate later-step obstructions, and derive a
necessary cycle constraint \((A-B)x=C\) that is not existence of a
cycle? Window search is not a \(\mathbb{Z}\)-theorem. A cycle
constraint is not a periodic orbit.

## Current literature

- Accelerated clearing \(2^k S(n)=3n+1\): ledger `C-T-welldefined`,
  Lean `acceleratedT_mul`. **KNOWN**.
- Classical Collatz/Syracuse cycle equations obtained by composing
  affine branches or parity vectors: Lagarias survey
  (`lagarias-2010-3x+1-survey`), Terras encoding, Bernstein–Lagarias
  2-adic parity analysis. **KNOWN**. Engine rediscovery of
  \((2^K-3^m)x=C(\mathbf{k})\) is not a new identity.
- Control-sequence / parity-vector methods and 2-adic symbolic
  dynamics for \(T\): **KNOWN** for Collatz-type maps.
- Integer affine words \(x\mapsto Ax+b_u\) already exist as
  `AffineSystem`. Cleared form \(a y = b x + c\) is the object here
  because a parameterized family is not an integer `AffineSystem`.

Project relationship: **new generic engine capability**. Syracuse
consumes the certificate; it does not seed the composer.

## Branch budget

```text
Mathematical target     Can v2 compose a certified one-step family into
                        exact multi-step constraints without map hints?
Novelty hypothesis      Control becomes a reasoning layer, not a
                        prettier description of a known identity.
Falsifier               Syracuse composition law or cycle equation is
                        hard-coded; AffineSystem is injected; a cycle
                        constraint is billed as a cycle.
Existing machinery      PiecewiseAffineCensus, ParameterDomain,
                        AttackPlanner prior_results, diagnosis loop.
Maximum Phase-0 scope   Generic composer + synthetics A–F + Syracuse
                        as consumer; Lean of compose_two_affine.
Promotion criterion     Certified control unlocks mathematics the
                        previous engine could not reach.
Stop criterion          Collatz escalation; machinery gravity; only
                        KNOWN cycle algebra with no reusable layer.
```

## Balanced-ternary formulation

None required. Composition is ordinary integer algebra.

## Why BT may be relevant

It is not required. The question is whether latent control, once
certified, can be consumed.

## Candidate operations / invariants

- Cleared composition
  \((A,B,C)\circ(a,b,c)=(Aa,\,bB,\,bC+cA)\).
  **EXACT — LEAN VERIFIED** (`compose_two_affine`). **KNOWN** algebra.
- Cycle constraint \((A-B)x=C\). **EXACT — LEAN VERIFIED**
  (`cycle_of_composed`). Necessary, not existence.
- Later-step obstruction: if every residue coprime to the family base,
  modulo \(b^{k+1}\), has valuation \(\neq k\), then that \(k\) cannot
  occur after the first step. **OBSERVATION** / exact on that
  finite residue check.
- Control-word quotient: words with identical \((A,B,C)\).
  **OBSERVATION** on the enumerated window.
- Involution \(x\mapsto 1-x\) has period 2.
  **EXACT — LEAN VERIFIED** (`hiddenInvolutionE_period2`). Engine
  synthetic E uses a finite even/odd toggle with the same period-2
  phenomenon, so the census can recover branches.

Do not treat `FORMALLY_COMPOSED` as `REALIZABLE`.

## Experiments

- `tests/research_engine/core/test_control_word.py`
- Hidden specs in `research_engine.benchmarks.hidden_piecewise`
- Syracuse consumer: `tests/research/syracuse/test_syracuse.py`
- CLI: `btlab research analyze|attack … control_word`

## Conjectures

None opened. The Collatz conjecture is not a conjecture of this branch.

## Counterexamples

- Algebraically valid word \((k,0)\) on the power-clear family
  \(2^k y=x+1\): later \(k=0\) is impossible on coprime images.
- Positive double \(x\mapsto 2x+1\): algebraic cycle candidate \(x=-1\)
  misses the nonnegative domain.
- Syracuse word length 2 with \(A\neq B\): unique candidate (e.g.
  \((1,1)\) gives \(x=-1\)) is not a positive odd orbit.

## Formalization

`formal/Problems/Engine/ControlWord.lean`: `compose_two_affine`,
`cycle_of_composed`, `hiddenInvolutionE_period2`. Syracuse
specialization `syracuse_compose_two` applies the generic lemma.
No `sorry`. No ledger row (KNOWN elementary algebra / KNOWN clearing
composition).

## Results

### A. Generic capability

Attack `control_word` immediately after `parameter_domain`. Types:
`ControlWord`, `ComposedAffineRelation`, `ControlWordConstraint`,
`ControlComposition`. Input is the prior certificate: affine relation,
parameter symbol, domain predicate, certificate status. The attack
does not know that a problem is Syracuse, that \(k\) is a valuation,
or that \(A(k)=2^k\). Evidence statuses stay separate:
`ALGEBRAICALLY_COMPOSED`, `LEAN_CERTIFIED`, `REALIZABLE`,
`CYCLE_CONSTRAINT_PROVED`. `AttackContext.affine` is not injected.
Non-core fingerprint field `latent_control_algebra`
(`UNOBSERVED|FORMALLY_COMPOSED|EXPLOITABLE|UNCERTAIN`) distinguishes
latent control discovered from algebra exploitable. Capability
`control_word_composition`. `cycle_obstruction` is exercised when a
cycle constraint is produced. `ComplexityProfile` is not forked;
`word_count`, `queries`, `quotient_size` live on evidence.

### B. Synthetic validation

Ground truth is in tests, not on the specs.

| Target | Ground truth | Discovered |
|--------|--------------|------------|
| A finite alphabet | \(x\mapsto 2x+(x\bmod 2)\) | two branches composed; \((A,B,C)\) matches generic compose |
| B unbounded | power-clear \(2^k y=x+1\) | family consumed; symbolic \(k\) remain |
| C domain-coupled | same map; \(k=v_2(x+1)\) | later-step domain used |
| D impossible | word \((\ast,0)\) | `IMPOSSIBLE` after coprime images |
| E cycle-bearing | even \(\leftrightarrow\) odd toggle | length-2 identity on the matching word; seeds \(\{0,1\}\) |
| F non-cycle on domain | \(x\mapsto 2x+1\) on \(x\ge 0\) | candidate \(-1\); no nonnegative seed is that point |

### C. Composition

Start from identity \((1,1,0)\). Each step \((a,b,c)\) updates
\(A'=Aa\), \(B'=bB\), \(C'=bC+cA\). For a power family this *derives*
\(b^{\sum k_i}x_m = p^m x_0 + C(\mathbf{k})\) without hard-coding \(b\)
or \(p\). Length \(\le 2\) cites `compose_two_affine`.

### D. Domain propagation

One-step domains stay on the certificate. Later parameters that are
impossible on every residue coprime to the base (modulus \(b^{k+1}\))
are marked `IMPOSSIBLE` on suffixes. Failure to prove impossibility
is `UNKNOWN`, not `IMPOSSIBLE`. Full quantifier elimination is not
attempted.

### E. Realizability

`FORMALLY_COMPOSED` \(\neq\) `REALIZABLE`. Sample-window hits are
`REALIZABLE_FOR_SOME_SEED`. Empty window search is `UNKNOWN`. Coprime
suffix obstruction is `IMPOSSIBLE`.

### F. Cycle constraints

Substitute \(x_m=x_0\) into \(A x_m = B x_0 + C\) to get
\((A-B)x_0=C\). If \(A=B\) and \(C\neq 0\), a cycle is `IMPOSSIBLE`.
If \(A\neq B\) and \(A-B\) does not divide \(C\), `IMPOSSIBLE`. If it
divides, a unique candidate is recorded; that is not a cycle theorem.
Modulus \(|A-B|\) with residue is a necessary congruence, not a seeded
Collatz modulus.

### G. Modular consequences

The modulus comes from the composed relation. No power of two or three
is seeded. Syracuse word \((1,1)\) yields candidate \(x=-1\) and
modulus \(5\) as a corollary of \((4-9)x=5\), which is **KNOWN** cycle
algebra.

### H. Control-word quotient

Words are grouped by identical \((A,B,C)\). On the enumerated window
the interesting systems typically have trivial quotient: different
words give different remainders. No finite minimization theorem is
claimed.

### I. Syracuse

Hint-free adapter. The composer receives the already-certified family
\(2^k y=3x+1\), \(k=v_2(3x+1)\), and does not rediscover it. Symbolic
words of observed \(k\) compose to
\(2^{\sum k_i}x_m = 3^m x_0 + C(\mathbf{k})\). Cycle constraints are
the classical Diophantine conditions. Realizable short words exist on
the odd sample window (e.g. length-1 \(k=1\) at \(x=3\)). Block,
modular, reverse, and spectral stay inapplicable in the same pass:
cleared form is not an integer `AffineSystem`. No Collatz escalation.

### J. Attack activation

Newly applicable: `control_word` (and `cycle_obstruction` coverage).
Still inapplicable without injection: `block`, `modular`, `spectral`,
`affine`. Q6 is therefore mixed: latent control is now consumable by
composition and cycle constraints, but it does not silently turn
`AffineSystem` attacks on. That limitation is preserved rather than
patched with a Syracuse-specific solver.

### K. Lean

Generic: `Problems.Engine.compose_two_affine`,
`Problems.Engine.cycle_of_composed`,
`Problems.Engine.hiddenInvolutionE_period2`.
Syracuse: `syracuse_compose_two` (instance of the generic lemma).
No ledger row.

### L. Prior art

| Class | Item |
|-------|------|
| KNOWN MATHEMATICS | clearing composition; Collatz/Syracuse cycle equations; parity-vector encodings |
| ENGINE REDISCOVERY | the same identities from a generic certificate |
| NEW GENERIC ENGINE CAPABILITY | certified family \(\to\) symbolic word \(\to\) exact multi-step algebra \(\to\) obstruction statuses |
| POTENTIALLY NEW MATHEMATICS | none claimed |

### M. ComplexityProfile

Unchanged schema. Control-word costs on evidence: `word_count`,
`queries`, `quotient_size`. No Collatz-specific metrics.

### N. ResearchLoop decision

```text
CONTINUE
```

Reason: latent parameterized family recovered, the arithmetic domain
is certified, and control-word algebra is exploitable; map globality
on \(\mathbb{Z}\) remains empirical. Dossier mapping: `PARK`. Not
`ESCALATE`. Not `ENGINE_LIMITATION`. Digit-fold family remains
`SATURATED`.

## Open questions

Can a composed cleared relation be consumed by a generic obstruction
engine that still does not inject an `AffineSystem` and still does not
attempt Collatz?

## Decision

`PARK`. Certified latent control is now a reasoning layer: compose,
constrain, refute some impossible words, derive necessary cycle
equations. The Syracuse identities obtained this way are **KNOWN**.
The engine capability is new. Do not auto-continue. Do not reopen
`research.collatz`.

Best next question: can those exact multi-step constraints feed a
generic obstruction attack that remains map-agnostic?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as number theory. The
value is the generic control calculus.
