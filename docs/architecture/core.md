# Core package (`bt`)

The core is problem-independent balanced-ternary mathematics.

## Rule

`bt.*` must never import `research.*`, `collatz`, or `visualization`.

This is enforced by `tests/unit/test_core_import_graph.py`.
`research_engine` is a separate experimental-dynamics layer and is also
forbidden beneath `bt.*`.

## Modules

| Module | Responsibility |
|--------|----------------|
| `bt.representation` | encode, decode, canonicalize, validate, digit access |
| `bt.arithmetic` | exact word/integer arithmetic (`add`, `×3`, `+1`, `negate`, `×2`, `/2` on domain) and trial integer helpers |
| `bt.normalization` | carry / borrow rewrite and optional carry traces |
| `bt.operators` | first-class operators `S`, `N`, `D`, `I_{-1,0,+1}`, `W`, `W_tail`, `W_z`, `M2`, `H2`, `H3`, `K3` |
| `bt.metrics` | weight, length, digit sums, carry defect, `v3` |
| `bt.support` | support-set operations |
| `bt.polynomials` | signed ternary polynomial `P_n` with `P_n(3)=n` |
| `bt.automata` | generic residue automata and DFA minimization |
| `bt.transducers` | generic sequential transducers and the transducer zoo |
| `bt.sequences` | canonical reusable sequences (digit sum, length, palindrome) |
| `bt.calculus` | trit algebra, `D`/`I_a`/`P_a`, `cmp3`/`select3`, rewrite, VM, information profiles, `Z[x]` section derivative, jets, residual Myhill–Nerode automata, polynomial function congruence modulo `3^k`, and the closed Newton image `F_k` of `x^3` |
| `bt.normtheory` | integer coefficient words, abstract carry rewrite, strategies, FMA, FST-by-bound, `hat D` |

## What does not belong here

- Collatz valuation, exponent codes, cylinders, affine centers
- Cubic fibre / layer / `N1` / `N0` / mismatched-quotient censuses (`research.residuals`)
- Prime-specific or sparse-power searches
- Mahler-measure experiment scans
- Operator-composition censuses
- CLI and Streamlit UI

Those live under `research.*` or application edges.

Existing long-form mathematics remains in [docs/mathematics.md](../mathematics.md)
and the operator documents; this page is only the package contract.
