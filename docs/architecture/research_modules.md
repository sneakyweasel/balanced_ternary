# Research modules

Research problems are applications of the `bt` core. Each area is
independent and may import `bt.*` plus shared experiment/registry
utilities.

## Status labels

| Status | Meaning |
|--------|---------|
| `EXPLORATORY` | early computational or structural work |
| `STRUCTURAL` | exact theorems or a stable exact dictionary, no solution claim |
| `THEOREM` | a named exact result is the centre of the module |
| `PAPER_CANDIDATE` | at least one exact theorem or genuinely nontrivial computational result with a clear literature distinction |
| `ARCHIVED` | retained for history, not an active programme |

Do not mark a module `PAPER_CANDIDATE` merely because a census is large.

## Seeded modules

| Module | Status | Contents |
|--------|--------|----------|
| `research.collatz` | `STRUCTURAL` | accelerated `T`, cylinders, dual codes, affine geometry, cycles, warp |
| `research.residuals` | `STRUCTURAL` | cubic Newton-stratum fibres, \(N_1\)/\(N_0\), mismatched \(Q\), invariant obstruction |
| `research.additive_combinatorics` | `EXPLORATORY` | `A_k`, `B_k`, `C_k`, sumsets |
| `research.perfect_powers` | `EXPLORATORY` | sparse squares and cubes |
| `research.primes` | `EXPLORATORY` | sparse-prime helpers already in the repo |
| `research.sparse_polynomials` | `EXPLORATORY` | Mahler / factor scans |
| `research.operator_dynamics` | `EXPLORATORY` | composition census, dossiers |
| `research.rewrite_calculus` | `PAPER_CANDIDATE` | maximal unary TRS; Add/carry exclusion; dossier only |
| `research.stabilization` | `ARCHIVED` | local \(\Phi_r\) versus global \(k_0\); literature close |
| `research.padic_dynamics` | `ARCHIVED` | cycle-lift residual quotient; classical return-map close |
| `research.cerny_bt` | `ARCHIVED` | transition-closed residual quotient; linear/nonlinear close |
| `research.misere_quotients` | `ARCHIVED` | finite-context misere signatures; Plambeck–Siegel close |
| `research.open_problems` | registry | pointers, not a dumping ground |

Each module exposes a lightweight `problem.py` descriptor
(`id`, `title`, `status`, `statement`, `bt_relevance`, `docs`, `lean`,
`conjectures`). Collatz keeps its existing modules; they are not forced
into a deep framework.

The exploratory modules above are parked. They are not a second frontier
and are not developed in the laboratory consolidation. Do not delete them.

## Adding a problem

See [docs/problems/TEMPLATE.md](../problems/TEMPLATE.md). A new problem
must not edit core arithmetic.
