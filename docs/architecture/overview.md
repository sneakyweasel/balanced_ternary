# Architecture overview

This repository is the **Balanced Ternary Mathematical Laboratory**: a
problem-independent balanced-ternary core (`bt`) plus independent research
applications (`research.*`).

Balanced ternary mathematics is **core**. Research problems are
**applications**. Core modules must never import research modules.

This page is the architectural contract. It does not change any
mathematical definition.

## Layers

```text
cli, visualization          application edges
research.*                  problem-specific mathematics
research_engine             problem-independent experimental dynamics
bt.*                        problem-independent BT mathematics
```

- `bt.*` may import only `bt.*` (and the Python standard library). It must not import `research_engine`.
- `research_engine` may import only the Python standard library. It must not import `bt.*` or `research.*`.
- `research.*` may import `bt.*`, `research_engine`, and explicitly shared utilities
  (`research.experiments`, conjecture/literature registries).
- `cli` and `visualization` may import both layers.

## Package names

| Role | Import | Notes |
|------|--------|-------|
| Distribution | `balanced-ternary-prime` | `pip install -e ".[dev,ui]"` |
| Command | `btprime` | preserved |
| Core | `bt` | new canonical root |
| Experimental dynamics | `research_engine` | integer affine/block/trajectory, R/K/L search, algebra, and typed attacks; R5 |
| Research | `research` | new canonical root |
| CLI | `cli` | new implementation home |
| Compatibility | `balanced_ternary`, `collatz`, `automata` | re-export shims |
| UI | `visualization` | optional extra; not part of the math core |

## Old → new module map

| Old public import | New canonical import |
|-------------------|----------------------|
| `balanced_ternary.representation` | `bt.representation` |
| `balanced_ternary.features` | `bt.metrics` |
| `balanced_ternary.metrics` | `bt.metrics` |
| `balanced_ternary.invariants` | `bt.metrics` / `bt.representation` |
| `balanced_ternary.arithmetic` (trial helpers) | `bt.arithmetic` |
| `collatz.bt_arithmetic` | `bt.arithmetic` |
| `balanced_ternary.operators` | `bt.operators` |
| `balanced_ternary.oeis_maps` (canonical sequences) | `bt.sequences` / `bt.operators` |
| `balanced_ternary.polynomials` (core `P_n`) | `bt.polynomials` |
| `balanced_ternary.polynomials` (Mahler scans) | `research.sparse_polynomials` |
| `balanced_ternary.additive_sets` (support) | `bt.support` |
| `balanced_ternary.additive_sets` (A_k/B_k/C_k) | `research.additive_combinatorics` |
| `balanced_ternary.additive_sets` (sparse powers) | `research.perfect_powers` |
| `balanced_ternary.additive_sets` (sparse primes) | `research.primes` |
| `balanced_ternary.operator_algebra` | `research.operator_dynamics` |
| — | `bt.calculus` |
| — | `research.residuals` |
| `balanced_ternary.sequences` (dossiers) | `research.operator_dynamics` |
| `balanced_ternary.transducer_zoo` | `bt.transducers` |
| `automata.modular` | `bt.automata` |
| `collatz.languages.dfa_minimize` | `bt.automata` |
| `collatz.transducers.doubling` | `bt.transducers.doubling` |
| `collatz.transducers.divide_by_two` | `bt.transducers.divide_by_two` |
| `collatz.transducers.divide_by_two_power` | `bt.transducers.divide_by_two_power` |
| `collatz.*` (problem-specific) | `research.collatz` |
| `balanced_ternary.cli` | `cli.main` |

Compatibility shims keep the old import paths working.

## Phase gates

After each refactor phase:

1. `pytest` (fast suite; `pytest --runslow` before a release)
2. `cd formal && lake build`

Do not continue past a red gate. Mathematical behaviour must not change.

## Related pages

- [Core](core.md)
- [Research modules](research_modules.md)
- [Experiments](experiments.md)
- [Conjectures](conjectures.md)
- [Formalization](formalization.md)
- [Literature](literature.md)
