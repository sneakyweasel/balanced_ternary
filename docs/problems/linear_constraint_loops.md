# Frozen Engine campaign: one-variable linear-constraint loops

Status: **EXPLORATORY**

This is an engine-capability campaign against contemporary prior art
(Carelli, ICALP 2026). It does **not** claim a decision procedure for
SLC termination, a proof or refutation of the Reachability Conjecture,
or a Collatz theorem. Adapters live in
`research.linear_constraint_loops`. There is no `LinearConstraintAttack`
and no generalized-Collatz language on the `ProblemSpec`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Can frozen Research Engine v2, given only an exact one-variable
linear-constraint loop, independently reconstruct useful arithmetic
structure, certify it, attack long-term behaviour, and stop before the
open generalized-Collatz barrier?

## Exact statement

On hint-free `ProblemSpec` adapters for one-variable integer SLCs, does
unmodified `ResearchLoop`

1. recover affine branches and latent controls from the exact transition
   relation;
2. produce control-word cycle constraints and obstructions;
3. distinguish empirical / finite-domain / structural / universal
   termination;
4. then let `score_candidate` select a subsequent target from a mixed
   pool?

Window agreement is not a map theorem on \(\mathbb{Z}\). Seed-orbit
finiteness is not numerical contraction of the map. Carelli's theorems
are prior art, not discovery targets.

## Current literature

- Carelli, *Loop Termination and Generalized Collatz Sequences*, ICALP
  2026, LIPIcs 374, 175:1–175:21
  (`carelli-2026-loop-termination`). **KNOWN**.
- General SLC termination over \(\mathbb{Z}\), \(\mathbb{Q}\), and
  \(\mathbb{R}\) remains open. **THEOREM** (as a statement of the open
  problem).
- One-variable integer loops are tightly connected to generalized
  Collatz sequences. **THEOREM** (Carelli).
- Termination of those loops is tied to the Reachability Conjecture, a
  weakening of Matthews–Watts uniform distribution
  (`matthews-watts-1984-generalization-hasse`, `moller-1978-hasse-syracuse`).
  **CONJECTURE**.
- A cyclic trace implies a cyclic trace of length at most two
  (Carelli Theorem 3.20). **THEOREM**.
- Affine SLC termination is decidable over \(\mathbb{R}\) (Tiwari,
  `tiwari-2004-termination-linear-programs`), over \(\mathbb{Q}\)
  (Braverman, `braverman-2006-termination-integer-linear`), and over
  \(\mathbb{Z}\) (Hosseini–Ouaknine–Worrell,
  `hosseini-ouaknine-worrell-2019-termination-linear-loops`). **THEOREM**.
- Landscape: Ben-Amram–Genaim–Ouaknine–Worrell 2025 survey
  (`ben-amram-genaim-ouaknine-worrell-2025-termination-survey`). **KNOWN**.

Project relationship: **engine diagnosis / rediscovery**. No new
number-theory or verification theorem is claimed.

## Branch budget

```text
Mathematical target     Can frozen v2 reconstruct useful arithmetic
                        structure from hint-free one-variable SLCs,
                        then certify termination/cycle constraints
                        short of the open generalized-Collatz barrier?
Novelty hypothesis      Engine-discovered affine branches, control
                        words, and obstructions that are not adapter
                        hints; possibly a cycle restriction independent
                        of Carelli's length-(≤2) theorem.
Falsifier               Adapter seeds generalized-Collatz language,
                        residue classes, cycle bounds, or unpublished
                        affine formulas; new attack modules;
                        computational evidence billed as universal
                        termination.
Existing machinery      Unmodified ResearchLoop; census → domain →
                        word → obstruction; mx+r / Syracuse 1-D
                        templates.
Maximum Phase-0 scope   Three blind SLC adapters + scout dossiers kept
                        off the adapter + unmodified loop + Lean for
                        the strongest exact identity + ResearchLoop
                        selection + one campaign dossier.
Promotion criterion     Exact certificates not already in the problem
                        definition, or a precise ENGINE_LIMITATION.
Stop criterion          New attack types; claiming to resolve Carelli
                        or the Reachability Conjecture; infrastructure
                        expansion.
```

## Balanced-ternary formulation

None. The adapters use ordinary integer arithmetic.

## Why BT may be relevant

It is not required. Digit-fold cores remain a comparison cluster in the
seeded corpus.

## Candidate operations / invariants

- Decrement \(x'=x-1\) on \(x\ge 1\). **EXACT — LEAN VERIFIED**
  (`decrement_reaches_zero`). **KNOWN**.
- Negation \(x'=-x\). Period 2, fixed point iff \(x=0\).
  **EXACT — LEAN VERIFIED**. **KNOWN**.
- Strip \(R^+\): \(4x-2\le 3x'\le 4x-1\) and \(x\ge 3\). Unique integer
  successor; \(3x'\in\{4x-1,4x-2\}\); \(x'=(4x)/3\).
  **EXACT — LEAN VERIFIED** (`rplusRel_unique`, `rplusRel_clear`,
  `rplusRel_ediv`). **KNOWN** (Carelli Example 4.26).
- Engine census \(3y=4x-2\) on \(x\equiv 2\pmod{3}\) and \(3y=4x-1\) on
  \(x\equiv 1\pmod{3}\). **OBSERVATION** on the sample window;
  **DISCOVERED** (not adapter-given). Relation exactness as in
  ParameterDomain. Not a map theorem on \(\mathbb{Z}\).
- Control-word class obstruction: length-2 words with mixed residue
  controls cannot close. **EXACT** on the composed relation.
  **KNOWN** arithmetic via Engine lemmas.

## Experiments

- `tests/research/linear_constraint_loops/test_linear_constraint_loops.py`
- Runner: `research.linear_constraint_loops.runner.run_campaign`
- Scout (never imported by the adapter):
  `research.linear_constraint_loops.scout`

## Conjectures

None opened. Carelli Example 4.26 / Reachability for
\(T(x)=\lfloor 4x/3\rfloor\) remains literature-open and is not
re-stated as a project conjecture.

## Counterexamples

- “Every defined step of \(R^+\) strictly decreases.” **REFUTED** at
  seed 4: \(4\mapsto 5\).
- “Every defined step of \(R^+\) is a one-step contraction
  \(\lvert y\rvert<\lvert x\rvert\).” **REFUTED** at the same seed.
- “A global affine involution \(y=-x\) yields a complete finite census.”
  **REFUTED** as an engine claim: sign-first region inference covers
  only the nonnegative sample class and leaves the census
  `UNRESOLVED`, so control-word attacks never run.
- “Finite seed closure means the map is contracting.” **REFUTED** as a
  diagnosis: \(R^+\) expands whenever a successor exists, yet seed 8
  closes at 66 and is billed `FINITE_CONTRACTING`.

## Formalization

`formal/Problems/Engine/LinearConstraintLoops.lean`: `rplusRel_unique`,
`rplusRel_clear`, `rplusRel_ediv`, `decrement_reaches_zero`,
`negation_period2`, `negation_fixed_iff_zero`. KNOWN integer
consequences of the problem definitions. No `sorry`. No ledger row.

## Results

### A. Scout map

| Target | Loop | Saturation | Open |
|--------|------|------------|------|
| `slc_decrement` | `while x ≥ 1 do x := x-1` | Settled ranking function | None |
| `slc_negation` | `x' := -x` | Settled involution; cycles of length 1 and 2 | None |
| `slc_rplus` | Carelli \(R^+\): \(4x-2\le 3x'\le 4x-1\), \(x\ge 3\) | Integer graph known | Reachability for \(\lfloor 4x/3\rfloor\) |
| `slc_increment` (pool) | Carelli Example 2.11: `x'=x+1` | Settled nontermination without cycles | None |

Carelli baseline, classified and **not** passed to adapters:

- General SLC termination over \(\mathbb{Z}/\mathbb{Q}/\mathbb{R}\) remains open. **THEOREM** (open-problem statement).
- One-variable integer loops connect to generalized Collatz sequences. **THEOREM**.
- Termination is tied to the Reachability Conjecture. **CONJECTURE**.
- A cyclic trace implies a cyclic trace of length \(\le 2\). **THEOREM**.

### B. Blind packets

Each adapter exposes only: integer state; dummy control; identity
observation; `affine_system()=None`; the exact guard; the exact
transition.

- Decrement / negation / increment: the affine assignment **is** the
  original specification.
- \(R^+\): only the inequalities \(4x-2\le 3x'\le 4x-1\) and \(x\ge 3\).
  Successors are enumerated as integer points of that strip. No residue
  table, no \(\lfloor 4x/3\rfloor\) formula, no Carelli name.

Scout material lives in `scout.py` and this dossier. `spec.py` and
`adapter.py` do not import it.

### C. Target results

#### C.1 `slc_decrement`

| Field | Engine |
|-------|--------|
| Decision (isolated) | `CONTINUE` |
| Decision (seeded corpus) | `FAMILY_SATURATED` (core-matches digit-fold via seed closure) |
| Semantic class | `INTEGER_1D\|SINGLETON\|FINITE_CONTRACTING\|FINITE_SEED_CLOSURE` |
| Census | `FINITE_CENSUS`, branch \(y=x-1\), region `sign/nonneg` |
| Structure origin | **GIVEN BY THE ADAPTER** |
| Domain | `SAMPLE_SUPPORTED` / direction `EXACT` on the window |
| Control words | \((0)\), \((0,0)\), \((0,0,0)\): \(y=x-n\) |
| Obstruction | `WORD`: \(A=B\) and \(C\neq 0\) (no integer cycle) |
| Closure | exact residual size 9 from seed 8 |
| Skipped | `vector_affine`, `matrix_word_invariant`, `modular`, `affine`, `reverse`, `block`, `spectral`, `factorization`, `symmetry`, `symbolic` |
| Termination | **Universal termination theorem** (`decrement_reaches_zero`). Ranking function \(x\). Not a census theorem. |
| Cycle | none (engine obstruction + post-run search) |
| Research decision | `CLOSE` as mathematics; engine `FAMILY_SATURATED` on the seeded corpus because window census is not a \(\mathbb{Z}\)-theorem and the core matches digit-fold seed closure |

#### C.2 `slc_negation`

| Field | Engine |
|-------|--------|
| Decision (isolated) | `CONTINUE` |
| Decision (seeded corpus) | `FAMILY_SATURATED` (core-matches digit-fold via seed closure) |
| Semantic class | `INTEGER_1D\|SINGLETON\|FINITE_CONTRACTING\|FINITE_SEED_CLOSURE` |
| Census | `UNRESOLVED`. One sample-supported line \(y=-x\) truncated to `sign/nonneg` |
| Structure origin | **GIVEN BY THE ADAPTER** (the assignment); **not certified** as a complete cover |
| Domain / words / obstruction | skipped (`parameter_domain` inapplicable) |
| Closure | exact residual size 2 from seed 5: \(5\mapsto -5\) |
| Post-run cycles | length 1 at \(0\); length 2 on every \(\{x,-x\}\) with \(x\neq 0\) |
| Carelli \(\le 2\) | **KNOWN ONLY FROM PRIOR ART** / post-run search. **Not** `ENGINE REDISCOVERY` via control words |
| Research decision | `ENGINE_LIMITATION` (census), recorded; not implemented |

This is the campaign's useful failure: a global affine involution is
visible in I/O, yet sign-first region inference prevents a complete
cover, so the frozen control-word stack never runs.

#### C.3 `slc_rplus`

| Field | Engine |
|-------|--------|
| Decision (isolated) | `CONTINUE` |
| Decision (seeded corpus) | `FAMILY_SATURATED` (core-matches digit-fold via seed closure) |
| Semantic class | `INTEGER_1D\|SINGLETON\|FINITE_CONTRACTING\|FINITE_SEED_CLOSURE` |
| Census | `FINITE_CENSUS`, two branches |
| Structure origin | **DISCOVERED** |
| Branches | \(3y=4x-2\) on \(x\equiv 2\pmod{3}\); \(3y=4x-1\) on \(x\equiv 1\pmod{3}\) |
| Latent control | residue modulo 3, observed values \(\{1,2\}\) |
| Domain | both congruence domains `EXACT` after counterexample search |
| Control words | 14 composed words; mixed length-2/3 words realizable as paths |
| Obstruction | `CLASS`: length 2 requires \(7\mid C\); blocked words \((0,1),(1,0)\). Length 3 requires \(37\mid C\); six mixed words blocked. Allowed closing words are the constant words \((0^n)\) and \((1^n)\), with cycle candidates \(x=2\) and \(x=1\) **outside the guard** \(x\ge 3\) |
| Closure | seed 8 orbit \(8,10,13,17,22,29,38,50,66\) then halt (exact finite seed closure) |
| Termination | **Empirical** on the probe window. **Not** a universal termination theorem |
| Carelli \(\le 2\) | not recovered as a general cyclic-trace theorem. Per-word gcd constraints are **KNOWN** arithmetic. Cycle candidates of length 1 sit at \(x=1,2\), which Carelli excludes by \(x\ge 3\) |
| Generalized Collatz | engine representation \(3y=4x-r\) on two residue classes vs Carelli \(T(x)=\lfloor 4x/3\rfloor\) vs Matthews–Watts weak Collatz. Automatic reconstruction of the research language: **yes**, as a finite piecewise-affine census, **without** being handed the correspondence |
| Research decision | `PARK` at the open Reachability barrier |

Falsification on \(R^+\): monotone descent **REFUTED**; one-step
contraction **REFUTED**; no window cycle **holds**; every window seed
eventually loses its successor **holds as a probe**, not as a theorem.

### D. Regime fingerprints

All three one-variable loops were billed
`INTEGER_1D|SINGLETON|FINITE_CONTRACTING|FINITE_SEED_CLOSURE`.
That core is a **seed-orbit artefact**, the same coarseness recorded
in the first engine campaign for seed-27 \(T_5\).

| Target | Piecewise | Latent control | Domain | Algebra | Obstruction | Affine type |
|--------|-----------|----------------|--------|---------|-------------|-------------|
| decrement | `FINITE` | `FINITE` | `SAMPLE_SUPPORTED` | `EXPLOITABLE` | `WORD` | `SCALAR` |
| negation | `UNCERTAIN` | `UNCERTAIN` | `UNOBSERVED` | `UNOBSERVED` | `UNOBSERVED` | `UNOBSERVED` |
| \(R^+\) | `FINITE` | `FINITE` | `SAMPLE_SUPPORTED` | `EXPLOITABLE` | `CLASS` | `SCALAR` |

\(R^+\) expands on every defined step. It is not a digit-fold map. The
core fingerprint cannot say so because the default seed closes.

Nearest-target fields were empty on isolated runs (no corpus). In the
campaign runner they are compared against the seeded digit-fold /
Syracuse / mx+r memory.

### E. Mathematical yield

| Field | Campaign |
|-------|----------|
| Known results rediscovered | Decrement ranking; negation involution (post-run, not census); \(R^+\) integer graph \(3y=4x-1\) or \(4x-2\); length-1 cycle algebra at \(x=1,2\) |
| New exact identities | none beyond the problem definitions |
| New invariant candidates | none promoted |
| New exact invariants | none |
| New obstructions | engine WORD/CLASS certificates on composed relations; **KNOWN** divisibility |
| New counterexamples | monotone descent / contraction on \(R^+\); complete-census claim on \(y=-x\) |
| New conjectures | none opened |
| New Lean theorems | packaging of KNOWN identities; no ledger |
| Potentially new mathematics | none claimed |
| Engineering changes | **1** correctness fix: Mealy quotient now respects empty `legal_controls` instead of calling `transition` on deadlock states. No new attack |

Main metric: **mathematical yield per target is KNOWN rediscovery plus
one named engine limitation.** No target produced a new theorem.

Prior-art classes for major engine results:

| Result | Class |
|--------|-------|
| \(y=x-1\) on the decrement loop | A — known rediscovery (adapter-given) |
| \(3y=4x-r\) on two mod-3 classes | A — known rediscovery of Carelli's integer graph; **DISCOVERED** by the engine |
| \(x'=(4x)/3\) on \(R^+\) | A / B — known; Lean `rplusRel_ediv` is a new formalization of a known identity |
| WORD/CLASS cycle obstructions | A — known divisibility; engine certificate |
| No universal \(R^+\) termination | A — Carelli's open instance; engine correctly stops |
| Sign-truncated involution census | C — computational observation about the engine, not about the loop |

No E classification.

### F. Carelli reconciliation

| Carelli claim | Engine |
|---------------|--------|
| One-variable SLC termination connects to generalized Collatz | **DISCOVERED** intermediate structure on \(R^+\): residue-selected affine branches \(3y=4x-r\). Not handed the correspondence. |
| Reachability Conjecture remains the barrier | Engine did **not** prove or refute it. Empirical halt of window seeds is not a theorem. |
| Cyclic trace \(\Rightarrow\) cyclic trace of length \(\le 2\) | **Not** an engine rediscovery. Negation's 2-cycles were found by post-run search after the census failed. \(R^+\) control words constrain *which* words can close; they do not prove a universal length bound. Length-1 algebra recovers \(x=1,2\), which the paper already places outside \(R^+\). |

The capability test:

> Can the frozen engine independently recover useful intermediate
> structure that the paper's formulation makes conceptually relevant?

**Yes**, on \(R^+\): affine branches, residue control, composed words,
and class obstructions. **No**, it cannot cross the open barrier, and
it cannot state Carelli's length-\(\le 2\) theorem.

### G. Lean

Strongest exact results, all **KNOWN**:

- `rplusRel_unique` — the integer strip is a partial function.
- `rplusRel_clear` — \(3y=4x-1\) or \(3y=4x-2\).
- `rplusRel_ediv` — \(y=(4x)/3\) on the defined locus.
- `decrement_reaches_zero` — universal termination of the decrement loop.
- `negation_period2` / `negation_fixed_iff_zero`.

No ledger row.

### H. Engineering backlog

Not implemented.

```text
Missing capability     Complete-cover test for a global affine law
                       before sign/interval truncation; alternatively,
                       a "line holds on the whole sampled domain"
                       region kind.
Targets affected       slc_negation (this campaign); any odd map
                       y = ax+b that holds for both signs.
Mathematical importance High for cycle analysis of affine SLCs: the
                       missed involution is exactly Carelli's length-2
                       phenomenon.
Evidence of recurrence One high-value target in this campaign. Do not
                       implement on a single failure.
Potential reusable abstraction  Domain-complete affine cover, or
                       delaying sign regions until after a global-line
                       check.
Expected research value Would have run control-word obstruction on
                       x'=-x and possibly stated period 2 as ENGINE
                       REDISCOVERY.
```

A second, already known, diagnosis coarseness (not implemented):

```text
Missing capability     Distinguish finite seed closure from map
                       contraction in RegimeFingerprint core
                       dimensions.
Targets affected       slc_rplus, slc_decrement, earlier T_5 seed 27.
Mathematical importance High: expanding Collatz-like strips are billed
                       FINITE_CONTRACTING.
Evidence of recurrence Independent of this campaign (engine_campaign
                       Target B) and repeated here.
Potential reusable abstraction  Core contraction from a window
                       magnitude census, not from the default seed.
Expected research value Would stop clustering R+ with digit-fold cores.
```

Correctness fix that **was** implemented (not a new attack):
`research_engine.behavior.quotient` no longer calls `transition` on
states with empty `legal_controls`. Partial loops can be minimized.
This is a deadlock bug, not a new mathematical capability.

### I. ResearchLoop

After the first batch, `score_candidate` is run on five sketches with
**no taste override**:

- another linear-constraint loop (`slc_increment`);
- a generalized \((mx+r)\) map (`mx_plus_r_7_1`);
- a non-Collatz piecewise-affine system (`hidden_congruence_a`);
- a vector/matrix system (`hidden_vector_parity_shear`);
- an unrelated discrete system (`integer_polynomial_x2_minus_2`).

The winner is `hidden_vector_parity_shear` with
`ExpectedResearchValue=0.027`
(`distance=0.50`, `capability_gap=0.32`, `novelty=0.25`, `cost=1.50`,
nearest Syracuse, `delta=HIGH`, family `ACTIVE`). After the one-variable
loops were billed `FAMILY_SATURATED` against the finite-contracting
core, the loop preferred a structurally distant 2-D lattice map over
another 1-D increment loop or another \(mx+r\) map. No manual override.

### J. Overall assessment

Frozen Research Engine v2 **does** produce useful intermediate
mathematics on a contemporary one-variable linear-constraint-loop
problem: from the inequalities of Carelli's \(R^+\) alone it
reconstructed the two affine residue branches, certified their domains,
composed control words, and proved class-level cycle obstructions.
That is automatic reconstruction of the generalized-Collatz *language*,
not a solution of generalized Collatz.

It **does not** produce a universal termination theorem for \(R^+\),
**does not** rediscover Carelli's length-\(\le 2\) cyclic-trace
theorem as an engine result, and **does** fail to certify the obvious
involution \(x\mapsto -x\) as a complete census.

Yield is therefore **KNOWN REDISCOVERY** plus **ENGINE_LIMITATION**,
not new mathematics.

Campaign completion: three loops run; blind reports; post-run prior
art; latent control on \(R^+\); control-word obstruction on decrement
and \(R^+\); useful failure on negation; Lean for the strongest exact
identities; no new attack; ResearchLoop selects a subsequent target;
yield summarized above.

## Open questions

The Reachability instance \(T(x)=\lfloor 4x/3\rfloor\) remains open in
the literature. Do not assign it to the engine. The named census
limitation is recorded for a future engineering phase, not for
implementation now.

## Decision

`PARK`. The campaign answered the frozen-engine question against
Carelli 2026. Recovered identities are **KNOWN**. The involution-census
failure is a precise `ENGINE_LIMITATION` and is not patched. Do not
auto-continue into proving or refuting the Reachability Conjecture. Do
not add a residue-class attack.

Best next question: should the frozen stack next consume a
*nondeterministic* one-variable SLC (multiple integer successors),
where the 1-D census already requires a singleton control?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as verification or
number theory. Value is the first frozen-engine campaign whose primary
metric is mathematical yield against current prior art.
