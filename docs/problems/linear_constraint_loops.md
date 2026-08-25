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
- Sum strip: \(-1\le x+x'\le 1\). Three integer successors at every
  \(x\); length-1 cycle at 0; length-2 cycle \(0\leftrightarrow 1\).
  **EXACT — LEAN VERIFIED** (`sumStripRel_three`, `sumStripRel_all`,
  `sumStrip_cycle_zero_one`, `sumStrip_fixed_zero`). **KNOWN**
  (Carelli Lemma 5.33). Existential, not universal.
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
- “The frozen 1-D census can represent overlapping legal affine
  domains.” **REFUTED** as an engine claim: `piecewise_affine` is
  inapplicable whenever `legal_controls(start)` is not a singleton.
- “Every legal path of the sum strip terminates.” **REFUTED** by an
  `EXISTENTIAL_WITNESS` cycle. That does not imply every legal path
  is cyclic (`UNKNOWN`).

## Formalization

`formal/Problems/Engine/LinearConstraintLoops.lean`: `rplusRel_unique`,
`rplusRel_clear`, `rplusRel_ediv`, `decrement_reaches_zero`,
`negation_period2`, `negation_fixed_iff_zero`, `sumStripRel_three`,
`sumStripRel_all`, `sumStrip_cycle_zero_one`, `sumStrip_fixed_zero`.
KNOWN integer consequences of the problem definitions. The sum-strip
lemmas are existential facts about the relation, not engine-discovered
branches and not universal termination. No `sorry`. No ledger row.

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

## Phase 2: nondeterministic one-variable SLC

```text
Mathematical target     Can frozen v2 represent, classify, and attack a
                        one-variable SLC when legal_controls contains
                        more than one control for a given state?
Novelty hypothesis      Existing closure, fingerprint, and probes already
                        support branching; the 1-D census/word/obstruction
                        stack may not.
Falsifier               Collapsing to a preferred successor; new attacks;
                        silent ∃/∀ collapse; implementing the involution
                        census fix from Phase 1.
Existing machinery      legal_controls on ProblemSpec; ExhaustiveClosure
                        BFS; RegimeFingerprint BRANCHING; 1-D census
                        singleton gate; ControlWord after ParameterDomain.
Maximum Phase-0 scope   Synthetics A–E + one Carelli-derived strip + Lean
                        for the exact legal relation / existential cycle
                        + dossier. No new attack.
Promotion criterion     Overlapping branches recovered by frozen census,
                        or a precise ENGINE_LIMITATION with quantifier
                        discipline.
Stop criterion          New attacks; census/quotient redesign; a
                        NondeterministicSLC solver.
```

### Quantifier discipline

Every Phase-2 claim is tagged `EXISTENTIAL`, `UNIVERSAL`,
`MIXED_QUANTIFIER`, or `UNKNOWN`.

| Label | Meaning |
|-------|---------|
| `EXISTENTIAL_WITNESS` | one verified legal path with the stated property |
| `NO PATH FOUND` | search miss, not `NO LEGAL PATH EXISTS` |
| `REFUTED` | a verified counterexample path to a universal claim |
| `CERTIFIED_ON_WINDOW` | every explored legal path from a finite window halted; not a \(\mathbb{Z}\)-theorem |
| `UNKNOWN` | truncation or bound; finite search does not certify the universal |

The frozen attacks themselves do not carry this vocabulary. It is
applied in post-run probes (`quantifier_report`) and in this dossier.

### K. Synthetic validation (tests only)

Hidden specs in `synthetics.py`. Ground truth never reaches a production
attack.

| Id | Relation | Census | Fingerprint | ∃ cycle | ∀ terminate |
|----|----------|--------|-------------|---------|-------------|
| A `two_affine` | \(x\rightsquigarrow 2x+1\) or \(x-2\) | skipped (`_singleton_integer`) | `BRANCHING` | `EXISTENTIAL_WITNESS` at \(-1\) (fixed point of \(2x+1\)) | `REFUTED` |
| B `stay_or_decrement` | \(x\rightsquigarrow x\) or \(x-1\) on \(x\ge 1\) | skipped | `BRANCHING` | `EXISTENTIAL_WITNESS` (stay) | `REFUTED`; `all_paths_cycle` remains `UNKNOWN` |
| C `dual_decrement` | \(x\rightsquigarrow x-1\) or \(x-2\) | skipped | `BRANCHING` | `NO PATH FOUND` | `CERTIFIED_ON_WINDOW` on \(\{0,\ldots,7\}\); `UNKNOWN` on a larger window (truncation is not a refutation) |
| D overlapping | A, and the real sum strip | skipped | `BRANCHING` | — | census did **not** force disjoint domains; it refused |
| E `decrement_or_double` | \(x\rightsquigarrow x-1\) or \(2x\) | skipped | `BRANCHING` | `EXISTENTIAL_WITNESS` \(1\leftrightarrow 2\) | `REFUTED` (cycle, and also a doubling ray) |

B is the required distinction: \(\exists\) cycle is true, \(\forall\)
paths cycle is not certified and is false. E is the false-universal
trap: most decrement paths halt, but a legal 2-cycle exists.

Finite branching with exact seed closure (`stay_or_decrement`,
`dual_decrement`) lets `closure` return `SUPPORTED`. The Mealy quotient
then runs, with alphabet equal to **the start state's** legal
successors. At other states those labels are typically illegal and
route to `__blocked__`. That is a valid Mealy machine on a global
alphabet, and a **semantic mismatch** for successor-as-control.

### L. Blind adapter

`RelationLoopSpec`: every legal integer successor **is** the control.
No preferred transition, no named branches, no Carelli language.
`spec.py` still does not import `scout.py`.

Real target: integer points of \(-1\le x+x'\le 1\) (`slc_sum_strip`).
Adapter exposes only the inequality via integer enumeration. Scout
name: Carelli Lemma 5.33 anti-diagonal strip, height 3. **Not** passed
to the engine.

### M. `slc_sum_strip` engine report

| Field | Engine |
|-------|--------|
| Decision (no override) | `CONTINUE` — “structurally distant non-finite regime with at least one exact certificate” |
| Semantic class | `INTEGER_1D\|BRANCHING\|MIXED_MAGNITUDE\|UNBOUNDED_SAMPLE` |
| `control_structure` / architecture | `BRANCHING` / `BRANCHING` (CORE; does not core-match digit-fold `SINGLETON`) |
| Piecewise / latent / domain | `UNOBSERVED` — census never ran |
| Structure origin | **GIVEN BY THE ADAPTER** (the inequality). Affine slices **not** `DISCOVERED` |
| Census | skipped. Failure boundary: `PiecewiseAffineCensusAttack.applicable` requires `len(legal_controls(start))==1` |
| ParameterDomain / ControlWord / obstruction | skipped as dependents |
| Closure | `INCONCLUSIVE`, cap 32, union size 33. BFS **does** follow every legal control. Truncation is not infinitude. Witnesses are a spanning tree; the full multi-graph is not exported |
| Reconnaissance | `OBSERVATION`, horizon 16, not \(L_n\) |
| Separation | `SUPPORTED`, length 0: identity observation separates distinct integers. This is the “exact certificate” behind `CONTINUE`. It is not a control identity |
| Quotient | `INCONCLUSIVE` (no finite reachable set) |
| Vector / matrix / modular / affine / … | skipped |
| ∃ cycle | `EXISTENTIAL_WITNESS` (post-run; e.g. \((-40,41)\), and Lean \(0\leftrightarrow 1\), \(0\mapsto 0\)) |
| ∀ terminate | `REFUTED` by that witness. Not a search miss |
| ∀ paths cycle | `UNKNOWN` |
| Result class | `EXISTENTIAL` |

`ENGINE_LIMITATION` (campaign record, not `decide_research` enum): the
frozen 1-D latent-control stack cannot represent legitimate overlapping
affine domains. `decide_research` reserves `ENGINE_LIMITATION` for
singleton + mixed magnitude + truncated + no piecewise, so a
`BRANCHING` spec is billed `CONTINUE` instead. Do not override.

### N. Failure boundary (frozen; not implemented)

```text
ENGINE_LIMITATION
```

```text
Problem              1-D census and its dependents assume a partial function
Affected component   PiecewiseAffineCensusAttack._singleton_integer;
                     _eval_map drops any state with len(controls)!=1;
                     ParameterDomain; ControlWord; control_obstruction
Semantic mismatch    Several affine laws may be simultaneously legal.
                     The census never starts, so it cannot recover
                     y=-x-1, y=-x, y=1-x on overlapping domains, and
                     it cannot incorrectly force those domains apart.
Minimal example      slc_sum_strip at any x; synthetics A–E
Mathematical importance  This is the generic one-variable nondeterministic SLC
Potential generic fix    Census of a relation (set-valued samples), then
                         overlapping ParameterDomain; legal-word language
                         L_m(x). Not in this experiment.
```

```text
Problem              Mealy quotient uses a global alphabet
Affected component   behavior.quotient.quotient_from_states
Semantic mismatch    alphabet = legal_controls(start). Successor-as-control
                     has a state-dependent letter set. Missing letters
                     become __blocked__, which is not the SLC relation.
Minimal example      stay_or_decrement: start alphabet {start, start-1};
                     at x=1 the legal set is {1,0}
Mathematical importance  Behavioral equivalence for nondeterministic SLC
                         is not the current Mealy quotient
Potential generic fix    State-dependent alphabets or relation bisimulation.
                         Do not invent a new quotient engine now.
```

```text
Problem              Closure witnesses are a spanning tree
Affected component   ExhaustiveClosureAttack
Semantic mismatch    Existential cycles off the BFS tree are absent from
                     witnesses; transition_rows counts the multi-graph
                     but does not export it
Minimal example      stay_or_decrement self-loop at the seed
Mathematical importance  Exact Post* union is still correct when complete
Potential generic fix    Export the adjacency table. Not in this experiment.
```

The Phase-1 involution-census fix remains unimplemented.

### O. Prior-art reconciliation (after the blind run)

| Layer | Content |
|-------|---------|
| Engine discovery | `BRANCHING`; mixed magnitude; unbounded sample; ∃ cycle witness; ∀ termination refuted; no affine census; no control words; no class obstruction |
| Paper's loop | Carelli Lemma 5.33: anti-diagonal strip \(-1\le x+x'\le 1\), height 3, three integer successors \(y\in\{-x-1,-x,1-x\}\) at every \(x\) |
| Known results | Length-1 cycle at 0; length-2 cycles including \(0\leftrightarrow 1\); Theorem 3.20 (cyclic trace \(\Rightarrow\) length \(\le 2\)); self-avoiding traces for height \(\ge 2\) |

| Carelli claim | Engine |
|---------------|--------|
| Three overlapping affine slices | **Not recovered.** Census skipped. Lean `sumStripRel_three` / `sumStripRel_all` package the **definition**, not engine discovery |
| Cycles of length 1 and 2 | **EXISTENTIAL_WITNESS** post-run / Lean. **KNOWN**. Not a control-word rediscovery |
| Theorem 3.20 length \(\le 2\) | **KNOWN ONLY FROM PRIOR ART.** Not an engine theorem. `all_paths_cycle` is `UNKNOWN` |
| Self-avoiding traces, height \(\ge 2\) | **Not recovered.** Closure truncated. Not claimed |
| Quantifier distinction (some traces cycle, some avoid) | Fingerprint does not state it. Post-run probes distinguish ∃ cycle from ∀ terminate and leave ∀ cycle `UNKNOWN` |

No recovery of Carelli's length-\(\le 2\) cyclic-trace result as engine
mathematics. That remains **KNOWN**.

### P. Mathematical yield (Phase 2)

```text
Known rediscoveries:     three-valued integer strip (definition);
                         ∃ cycles of length 1 and 2 (KNOWN Carelli);
                         BRANCHING as a core fingerprint
New exact results:       none beyond the problem definition
New counterexamples:     “the 1-D census can represent overlapping
                         legal affine domains” REFUTED as an engine claim;
                         “∀ legal paths of the strip terminate” REFUTED
New existential witnesses: post-run cycle on the strip; Lean 0↔1 and 0↦0
New universal statements: dual_decrement CERTIFIED_ON_WINDOW only;
                         no Z-theorem from the frozen stack
New conjectures:         none
Lean-certified results:  sumStripRel_three, sumStripRel_all,
                         sumStrip_cycle_zero_one, sumStrip_fixed_zero
                         (KNOWN; no sorry; no ledger)
Unresolved quantifier problems: ∀ paths cycle on the strip; ∀x∃
                         terminating legal word vs ∀x∀u; self-avoiding
                         traces; mixed quantifiers generally
Engineering limitations: recorded above; not implemented
```

Capability coverage: `branching_controls` and
`nontrivial_control_alphabet` are `EXERCISED`. Latent control, piecewise
census, and control-word obstruction are `NOT_TESTED` / skipped, not
refuted as mathematics.

ResearchLoop: `CONTINUE` on `slc_sum_strip` (BRANCHING core, unbounded
sample, trivial exact separation). No taste override. The campaign
decision below is `PARK`.

### Q. Answer to the Phase-2 question

How far can the frozen deterministic latent-control machinery already
reason about genuinely nondeterministic one-variable SLCs?

```text
multiple legal transitions
  → fingerprint BRANCHING, magnitude over all controls, closure BFS Post*
  → census / ParameterDomain / ControlWord / obstruction : STOP
  → existing composition/obstruction never runs
```

Nondeterministic mathematics is **diagnosed** and **existentially
sampled**. It is **not** consumed by the frozen 1-D control language.
That is a useful failure. Do not thaw the architecture to paper over it.

## Open questions

The Reachability instance \(T(x)=\lfloor 4x/3\rfloor\) remains open in
the literature. Do not assign it to the engine. Named limitations
(involution census; seed-closure vs contraction; singleton census gate;
start-local Mealy alphabet) wait for an engineering thaw, not for
implementation now.

## Decision

`PARK`. Phase 1 recovered KNOWN \(R^+\) residue structure and a named
involution-census limitation. Phase 2 showed that `legal_controls` with
cardinality greater than one is visible to fingerprint, probes, and
closure, and invisible to the 1-D census/word/obstruction stack.
Existential cycle witnesses are valid and were not promoted to universal
theorems. Overlapping affine domains were not recovered and were not
falsely partitioned. All identities remain **KNOWN**. Do not implement
a nondeterministic census, a legal-word language, or a new bisimulation
engine. Do not override ResearchLoop.

Best next question: which *other* frozen-engine mathematical target
should be consumed next, leaving the parked SLC limitations untouched?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as verification or
number theory. Value is a two-phase frozen-engine campaign whose
primary metric is mathematical yield against Carelli 2026, including a
precise semantic boundary on nondeterminism.
