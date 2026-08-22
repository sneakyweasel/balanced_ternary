# Refactor report — Balanced Ternary Mathematical Laboratory

Architectural move-and-shim. Mathematical behaviour is intended to be
unchanged.

## 1. Final repository tree (source)

```
src/bt/                     core BT mathematics
src/research/               problem modules + registries + experiment I/O
src/cli/                    btprime implementation
src/balanced_ternary/       compatibility façade
src/collatz/                compatibility façade
src/automata/               compatibility façade
src/visualization/          optional Streamlit UI
formal/{Core,Representation,Operators,Problems/Collatz,CollatzDual,Automata}
conjectures/{active,proved,refuted,archived}
literature/
docs/{architecture,theory,problems}
tests/{unit,integration,research,regression}
experiments/                generated artifacts (gitignored)
```

## 2. Moved / consolidated modules

- Representation, features/metrics/invariants, operators, sequences, polynomials → `bt`
- Word arithmetic and `/2`, `×2`, `/2^k` transducers → `bt`
- DFA minimization → `bt.automata`
- Collatz package → `research.collatz`
- Additive sets / sparse powers / sparse primes split into research modules
- Operator algebra + dossiers → `research.operator_dynamics`
- Mahler scans → `research.sparse_polynomials`
- Experiment schema/table I/O → `research.experiments`
- CLI → `src/cli`
- Lean theorems grouped under Core / Representation / Operators / Problems/Collatz

## 3. Old → new import map

See [overview.md](overview.md). Shims keep `balanced_ternary`, `collatz`,
and `automata` importable.

## 4–5. Core and research architecture

See [core.md](core.md) and [research_modules.md](research_modules.md).
`bt` imports no research modules (enforced by tests).

## 6. Conjecture registry

JSON under `conjectures/`. API: `research.conjectures`. Seeded refuted
hypotheses (`W(3)=1`, `n=165`, BT suffix, …) and active/supported
entries (`N_k`, lift conjectures). Observations were not upgraded to
conjectures.

## 7. Literature registry

JSON under `literature/` (Kramer, Eliahou–Verger-Gaugry, Rozier–Terracol,
Cerdá, 2026 cycle preprints, OEIS A134028, …). Existing comparison docs
were not deleted.

## 8. CLI command map

Preserved: `encode`, `decode`, `analyze`, `residue`, `test-invariants`,
`reverse`, `reverse-tail`, `operators …`, `collatz …`.

Added: `bt …`, `primes`, `perfect-powers`, `additive`, `polynomials`,
`experiments`, `conjectures`, `literature`, `formal`, `status`.

Entry point: `cli.main:main` (shim `balanced_ternary.cli:main`).

## 9. Lean module map

See [formalization.md](formalization.md). `CollatzDual.*` re-exports the
new paths. Package name remains `collatz-dual-formal`.

## 10. Test counts

After: **390** tests collected (`pytest --collect-only`). The original
suite was kept (moved, not deleted). Added import-graph guards, registry
schema tests, regression witnesses, and a shared-primitive timing smoke.
Count did not drop.

## 11. Lean build

`lake build` succeeds. Grep finds no `sorry` or `admit`.

## 12. Compatibility shims

`balanced_ternary.*`, `collatz.*`, `automata.*`, and
`balanced_ternary.cli` / `cli_operators`.

## 13. Intentional debt

- `visualization` remains a sibling package
- Experiment runners are registered, not rewritten
- Lake package name unchanged
- `lower_bounds` and `noncontracting_dual` retained
- Milestone numbers 7–8 remain missing
- Trial `is_prime` remains an inspection helper
- No new CI workflow

## 14. Mathematical behaviour changed

None intended. Failures were treated as export/import bugs.

## 15. Strongest remaining research directions

1. Exceptional / non-contracting itinerary compatibility (`R_m→∞`).
2. Closed form / status of `/2^k` complexity `N_k` (and `A_k`).
3. Cycle languages beyond the bounded `(p≤6, k_i≤4)` census, without
   adopting 2026 preprint exclusions.

## 16. How to add a new open problem

Follow [docs/problems/TEMPLATE.md](../problems/TEMPLATE.md) and
`src/research/template/`. Do not edit `bt` arithmetic.
