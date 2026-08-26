# Research Engine diagnosis loop

Problem-independent diagnosis sits on top of the existing v2 attack
planner. It does not replace `AttackPlanner` and does not inject
invariants, quotients, Lyapunov functions, moduli, cycles, or
attractors into a `ProblemSpec`. Existing attack semantics and relative
order are unchanged. `piecewise_affine` is appended after
`reconnaissance`; `parameter_domain` immediately after that;
`control_word` immediately after the domain certificate;
`control_obstruction` immediately after control-word composition;
`vector_affine` immediately after that, and only for dimension ≥ 2;
`matrix_word_invariant` immediately after `vector_affine`. After the
matrix-word invariant experiment the attack order is **frozen**
(package **0.2.1**).

## Why this layer exists

SignedP0, digit-sum dynamics, and weight dynamics independently closed
as finite-contracting integer maps with dummy controls. The planner
could execute attacks, but it could not *say* they were the same
regime, nor discourage a fourth mechanically similar target. That
comparison is a reusable property of dynamical experiments, not a
problem-specific theorem.

Syracuse then showed mixed magnitude under a dummy control with no
affine language. `PiecewiseAffineCensus` is the generic follow-up: infer
latent affine branches from exact I/O without being told the partition.

## Loop

```text
exact target
  → generic diagnosis (RegimeFingerprint, StructuralDelta, FamilyStatus,
    CapabilityCoverage)
  → attack planner (reconnaissance, piecewise_affine, parameter_domain, control_word, control_obstruction, vector_affine, then existing order)
  → certificate / refutation
  → ResearchDecision
  → ExpectedResearchValue for a prospective sketch
```

Diagnosis uses only interface probes, `PlannerReport` evidence, and
optional integer 1-D censuses (magnitude and residue samples). Fields
that were not observed stay `UNOBSERVED`. The target name is never a
feature. The census does not mutate `AttackContext.affine`.

## New types

| Type | Role |
|------|------|
| `RegimeFingerprint` | certified structural summary |
| `RegimeSimilarity` / `StructuralDelta` | comparison of populated fields; core dimensions dominate HIGH/LOW |
| `FamilyStatus` | `ACTIVE` … `SATURATED` from accumulated records, not from names |
| `CapabilityCoverage` | `EXERCISED` / `NOT_TESTED` / `INAPPLICABLE` |
| `ResearchDecision` | `CLOSE` / `CONTINUE` / `ESCALATE` / `FAMILY_SATURATED` / `ENGINE_LIMITATION` |
| `ResearchCorpus` | session memory of `ExperimentRecord`s |
| `ExpectedResearchValue` | `(distance × capability_gap × novelty × failure_learning) / cost`; `failure_learning` is 1.0 unless a `ResearchMemory` is supplied |
| `AffineBranch` / `BranchRegion` / `LatentControl` | piecewise-affine census objects |
| `PiecewiseAffineCensus` | finite vs parameterized cover from samples |
| `AffineFamily` / `ParameterDomain` / `DomainCertificate` | arithmetic predicates for a reconstructed family |
| `ControlWord` / `ComposedAffineRelation` | symbolic composition of a certified family |
| `ControlObstructionCertificate` | class- or word-level arithmetic contradiction |
| `VectorAffineBranch` / `VectorAffineFamily` / `VectorAffineCensus` | multi-D latent \(y=A_u x+b_u\) from I/O |
| `MatrixWordInvariant` | recursive predicate on composed \((M_i,c_i)\) |
| `ResearchMemory` | persistent post-run store; not an attack |
| `FailureRecord` / `FailureClass` | what a failure means mathematically |
| `GreyLoot` | reusable unsuccessful or partial evidence |
| `MathematicalYield` | research output vs capability validation |
| `DecisionReason` | structured reason alongside `ResearchDecision` |

v2.2 research memory (`research_engine.memory`) wraps completed
experiments. It does not change attack order, `decide_research`
strings, or `score_candidate` when no memory store is passed.
`FailureLearningValue` is an optional multiplier. Scout, attack, grey
loot, and certified machinery occupy isolated lanes. A single failure
never justifies a new attack; `PROMOTE_TO_NEXT_VERSION` is guidance
only. Dossier: [engine_memory.md](../problems/engine_memory.md).
The v2.2 target board (`ResearchTarget`, `PriorArtDossier`, named
failure clusters, `RecommendedCampaignOrder`) is scout-lane content
ingested by `score_candidate` / `ResearchLoop` as `CandidateSketch`
objects only. It does not add adapters or thaw the planner. Dossier:
[research_target_board.md](../problems/research_target_board.md).
Package **0.2.2** tags the memory layer; the attack stack remains the
frozen 0.2.1 order.

v2.4 research control (`research_engine.control`, package **0.2.7**)
wraps completed campaigns without thawing attacks. It freezes
`RESEARCH_ENGINE_V2_3_BASELINE`, assigns a primary close tag and an
independent mathematical status, emits exactly three non-executable
attack proposals, and replays selected v2.2 targets with historical
results excluded from the blind track. A Phase-0 ranking-function
falsifier (`research_engine.control.ranking`) enumerates a tiny exact
template family on frozen v2.3 transitions; Phase-1 enriches that
probe; Phase-2 (`research_engine.control.symbolic_composition`) asks
whether the juggler `T^2` ranking signal is an exact two-step lemma.
Phase-4 (`research_engine.control.reverse_add_composition`) tests two-step
reverse-add identities; Phase-5 (`research_engine.control.reverse_add_carry`)
tests the one-step carry of `x+W(x)`; Phase-6
(`research_engine.control.reverse_add_pair_interaction`) tests the
pre-normalization digit pairing of `encode(x)` with `encode(W(x))`;
Phase-7 (`research_engine.control.reverse_add_weighted_pair`) tests
positional dominance of those pair sums; Phase-8
(`research_engine.control.reverse_add_involution`) tests whether the
reversal involution itself yields a reverse-specific law.
None of these is an attack and none changes `DEFAULT_ATTACK_ORDER`.
A gated experimental attack `restricted_symbolic_composition` /
`odd_even_two_step_decrease` may be opted into via
`enable_restricted_symbolic_composition`; it is not in the flood order.
Dossier:
[research_engine_v24.md](../problems/research_engine_v24.md). Records:
[ranking_phase0.md](../research/ranking_phase0.md),
[ranking_phase1.md](../research/ranking_phase1.md),
[symbolic_composition_phase2.md](../research/symbolic_composition_phase2.md),
[symbolic_composition_phase3.md](../research/symbolic_composition_phase3.md),
[reverse_add_composition_phase4.md](../research/reverse_add_composition_phase4.md),
[reverse_add_carry_phase5.md](../research/reverse_add_carry_phase5.md),
[reverse_add_pair_interaction_phase6.md](../research/reverse_add_pair_interaction_phase6.md),
[reverse_add_weighted_pair_phase7.md](../research/reverse_add_weighted_pair_phase7.md),
[reverse_add_involution_phase8.md](../research/reverse_add_involution_phase8.md).

Non-core fingerprint fields: `piecewise_affine_structure`,
`latent_control` (`NONE|FINITE|PARAMETERIZED|UNCERTAIN|UNOBSERVED`),
`parameter_domain` (`UNOBSERVED|SAMPLE_SUPPORTED|EXACT|UNCERTAIN`),
`latent_control_algebra`
(`UNOBSERVED|FORMALLY_COMPOSED|EXPLOITABLE|UNCERTAIN`),
`latent_control_obstruction`
(`UNOBSERVED|NONE|WORD|CLASS|SYMBOLIC_CLASS|RECURSIVE_INVARIANT`), and
`affine_control_type`
(`UNOBSERVED|SCALAR|VECTOR|MATRIX_PARAMETERIZED`).
They do not join `CORE_DIMENSIONS`. `latent_control` is discovery;
`latent_control_algebra` is composition; `latent_control_obstruction`
is word-, class-, or symbolic-class contradiction;
`affine_control_type` distinguishes scalar vs vector recovered language.
`matrix_word_invariant` may raise `latent_control_obstruction` to
`RECURSIVE_INVARIANT` without a new fingerprint dimension.

`ResearchDecision` is not dossier `PROMOTE|PARK|CLOSE` and not
hypothesis `DecisionKind`. Mapping: `CLOSE` and `FAMILY_SATURATED` →
branch `CLOSE`; `ESCALATE` → `PROMOTE`; `CONTINUE` and
`ENGINE_LIMITATION` → `PARK`.

`ENGINE_LIMITATION` is reserved for mixed magnitude under a singleton
control with truncated reachability and no recovered piecewise-affine
language. A sample-supported parameterized family yields `CONTINUE`,
not that status. Algebraic `EXACT` on the reconstructed *relation* is
not a map theorem on \(\mathbb{Z}\) and not a Collatz theorem. “No
theorem found” is not an engine limitation. Vector I/O uses the same
latent-control fields when `vector_affine` recovers a census;
`piecewise_affine` stays 1-D.

## No-ops

- `ComplexityProfile` is unchanged. Census, domain, and control-word
  counts live on `AttackResult.evidence`.
- The census does not install controls, moduli, or `AffineSystem` on
  the spec. Domain certification and control-word composition consume
  `prior_results`, not an injected affine system. `vector_affine` is
  appended after `control_obstruction` and does not split the 1-D
  census/domain/word/obstruction chain. `matrix_word_invariant` is
  appended after `vector_affine`. **ATTACK ARCHITECTURE FROZEN** for the
  flood order. Gated `restricted_symbolic_composition` is opt-in and is
  not in `DEFAULT_ATTACK_ORDER`.
- No Syracuse-specific engine types. Coefficient search is a documented
  integer box, not a seeded \(3x+1\) rule. Composition is cleared-form
  algebra, not a hard-coded Syracuse product formula. Maximal exponent
  is a divisibility conjunction, not a hard-coded valuation hint.
- `balanced_ternary_weight_drift` is not extended; it is a closed
  expanding negative control and must not join the finite-contracting
  family.

## Home

Python: `research_engine.diagnosis`, `research_engine.memory`,
`research_engine.control`, and
`research_engine.attacks.piecewise_affine`,
`research_engine.attacks.parameter_domain`,
`research_engine.attacks.control_word`,
`research_engine.attacks.control_obstruction`,
`research_engine.attacks.vector_affine`,
`research_engine.attacks.matrix_word_invariant`. CLI: `btlab research analyze`
prints a diagnosis block after the planner report. Hidden synthetics:
`research_engine.benchmarks.hidden_piecewise`,
`research_engine.benchmarks.hidden_vector_affine`, and
`research_engine.benchmarks.hidden_matrix_invariants`.
