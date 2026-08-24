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

The live publication task is `research.rewrite_calculus`. Send the
reviewer packet with the draft. The cubic Newton stratum is the last
promoted mathematical theory; it is not a new-math frontier.

## Seeded modules

| Module | Status | Contents |
|--------|--------|----------|
| `research.rewrite_calculus` | `PAPER_CANDIDATE` | unary `{D,I_a,S,N}`; `add_not_DLocal`; ready for review |
| `research.residuals` | `STRUCTURAL` | cubic Newton-stratum fibres; \(x^4\) visibility `CLOSE` |
| `research.collatz` | `STRUCTURAL` | accelerated `T`, cylinders, dual codes, affine geometry, cycles, warp |
| `research.regular_output_preimages` | `STRUCTURAL` | regular output of \(x^2\); sofic obstruction |
| `research.monna_endpoint_spectra` | `STRUCTURAL` | balanced-Monna endpoint spectra; gate closed |
| `research.lifting` | `EXPLORATORY` | lifting trees; lifting-state / \(k_0\) lines closed |
| `research.additive_combinatorics` | `EXPLORATORY` | `A_k`, `B_k`, `C_k`, sumsets |
| `research.perfect_powers` | `EXPLORATORY` | sparse squares and cubes |
| `research.primes` | `EXPLORATORY` | sparse-prime helpers already in the repo |
| `research.sparse_polynomials` | `EXPLORATORY` | Mahler / factor scans |
| `research.operator_dynamics` | `EXPLORATORY` | composition census, dossiers |
| `research.balanced_digit_sum_polynomials` | `EXPLORATORY` | nonlinear \(s_{\mathrm{bal}}\); `CLOSE` as reparameterization |
| `research.erdos_distinct_subset_sums` | `EXPLORATORY` | Erdős #1 signed-relation gate |
| `research.ostrowski` | `STRUCTURAL` | order-3 \(B_{\min}\); NP \(K\) unbounded; \(L_0\) PARK; dynamics helpers and planner delegate to `research_engine` |
| `research.kabelian_complexity` | `ARCHIVED` | k-abelian residual signatures; block-coding close |
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
