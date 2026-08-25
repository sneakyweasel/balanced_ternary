# Research Engine diagnosis loop

Problem-independent diagnosis sits on top of the existing v2 attack
planner. It does not replace `AttackPlanner`, does not change attack
order, and does not inject invariants, quotients, Lyapunov functions,
moduli, cycles, or attractors into a `ProblemSpec`.

## Why this layer exists

SignedP0, digit-sum dynamics, and weight dynamics independently closed
as finite-contracting integer maps with dummy controls. The planner
could execute attacks, but it could not *say* they were the same
regime, nor discourage a fourth mechanically similar target. That
comparison is a reusable property of dynamical experiments, not a
problem-specific theorem.

## Loop

```text
exact target
  → generic diagnosis (RegimeFingerprint, StructuralDelta, FamilyStatus,
    CapabilityCoverage)
  → attack planner (unchanged)
  → certificate / refutation
  → ResearchDecision
  → ExpectedResearchValue for a prospective sketch
```

Diagnosis uses only interface probes, `PlannerReport` evidence, and
optional integer 1-D censuses (magnitude and residue samples). Fields
that were not observed stay `UNOBSERVED`. The target name is never a
feature.

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

`ResearchDecision` is not dossier `PROMOTE|PARK|CLOSE` and not
hypothesis `DecisionKind`. Mapping: `CLOSE` and `FAMILY_SATURATED` →
branch `CLOSE`; `ESCALATE` → `PROMOTE`; `CONTINUE` and
`ENGINE_LIMITATION` → `PARK`.

`ENGINE_LIMITATION` is reserved for mixed magnitude under a singleton
control with truncated reachability and no affine/block/spectral
language. “No theorem found” is not that status.

## No-ops

- `ComplexityProfile` is unchanged. Growth, valuation, and contraction
  frequency live on the fingerprint until a later generic need appears.
- No piecewise-affine or \(v_2\) reconstruction attack.
- No Syracuse-specific engine types.
- `balanced_ternary_weight_drift` is not extended; it is a closed
  expanding negative control and must not join the finite-contracting
  family.

## Home

Python: `research_engine.diagnosis`. CLI: `btlab research analyze`
prints a diagnosis block after the planner report.
