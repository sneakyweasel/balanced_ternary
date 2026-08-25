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
matrix-word invariant experiment the attack order is **frozen**.

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
| `ExpectedResearchValue` | `(distance × capability_gap × novelty) / cost` |
| `AffineBranch` / `BranchRegion` / `LatentControl` | piecewise-affine census objects |
| `PiecewiseAffineCensus` | finite vs parameterized cover from samples |
| `AffineFamily` / `ParameterDomain` / `DomainCertificate` | arithmetic predicates for a reconstructed family |
| `ControlWord` / `ComposedAffineRelation` | symbolic composition of a certified family |
| `ControlObstructionCertificate` | class- or word-level arithmetic contradiction |
| `VectorAffineBranch` / `VectorAffineFamily` / `VectorAffineCensus` | multi-D latent \(y=A_u x+b_u\) from I/O |
| `MatrixWordInvariant` | recursive predicate on composed \((M_i,c_i)\) |

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
  appended after `vector_affine`. **ATTACK ARCHITECTURE FROZEN.**
- No Syracuse-specific engine types. Coefficient search is a documented
  integer box, not a seeded \(3x+1\) rule. Composition is cleared-form
  algebra, not a hard-coded Syracuse product formula. Maximal exponent
  is a divisibility conjunction, not a hard-coded valuation hint.
- `balanced_ternary_weight_drift` is not extended; it is a closed
  expanding negative control and must not join the finite-contracting
  family.

## Home

Python: `research_engine.diagnosis` and
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
