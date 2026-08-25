# Research engine v2 report

## Architecture changes

Observation, raw contribution, invariant envelope, exact reachability, pair-state separation, and Mealy quotient are optional layers next to `ProblemSpec`. They do not replace the seven theorem-ledger tags. `CertificateKind` is engine-only.

## New generic abstractions

- `CertificateKind` on `AttackResult`
- `observe` / `ObservableSpec`
- `check_control_factorization`
- `InvariantEnvelopeResult` vs `ExactReachabilityResult`
- `BehavioralSeparationAttack`
- engine `mealy_partition` / `BehavioralQuotientResult`
- `ComplexityProfile`
- `SymmetryResult`
- counterexample leak attacks
- `PriorArtStatus` on session hypotheses

## Migrated adapters

`SignedDigitResidualSpec`, `ExpandingDResidueSpec`, `ProductResidualSpec`, `DAddResidualSpec`, `SieveSpec`/`PrimeSpec`. Collatz `ShortcutSpec` has no output; bounded reconnaissance stays an observation and cap-hit closure stays `INCONCLUSIVE`.

## New attacks

`factorization`, `separation`, `quotient`, `symmetry`, plus explicit leak attacks. They are appended after the original eight planner attacks and skip when inapplicable.

## Research planner changes

`PROMOTE` requires a populated prior-art field. Skipped stages still use `SkipRecord` with a reason.

## Regression results

Fast `pytest` passed, including `tests/research_engine/regression/test_research_methodology.py`.

## Performance comparison

Pair-state BFS returns on the first witness. Closure queue behavior is unchanged. Observations are cached per `(state, control, phase)`.

## Lean build result

No Lean files were changed. `lake build Problems` was not required.

## Known compatibility issues

Signed-digit and multiplicative YAML records gained extra fields (`certificate_kind`, `prior_art_status`). CLI first-line attack status strings are unchanged.

## What remains problem-specific?

The `v_3(s-t)+1` predictor, signed-digit `D`/`lsd` step, Collatz all-odd family, and the prime predicate.

## What became generic?

Observation, factorization through `h`, envelope holes vs reachable sets, pair-state separation, Mealy counts, complexity profiles, and exact-vs-bounded certificates.

## What new research question can now be expressed cleanly?

Which new integer dynamics can be compared to signed-digit residual using only `ComplexityProfile` and `CertificateKind`?
