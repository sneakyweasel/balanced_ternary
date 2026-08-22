# Collatz (accelerated odd-only map)

Status: **STRUCTURAL**

This module does **not** claim a proof or disproof of the Collatz conjecture.

## Exact statement

Study \(T(n)=(3n+1)/2^{v_2(3n+1)}\) on positive odd integers through
exponent codes, cylinders, lift digits, affine centers, and BT observables.

## Why balanced ternary is relevant

BT represents the canonical realizer \(R\) and supplies word maps such as
\(W\). \(\operatorname{BT}(R)\) is determined by \(R\); it is not an
independent solving coordinate.

## Existing record

See [collatz_mathematics.md](../collatz_mathematics.md),
[collatz_research_questions.md](../collatz_research_questions.md), and the
milestone documents indexed from [docs/README.md](../README.md).

## Lean

`formal/Problems/Collatz/` with compatibility re-exports in `formal/CollatzDual/`.

## Conjectures / refutations

Registry ids include `Nk_state_count`, `n_star_le_n`,
`BT_R_suffix_determines_next_valuation`, `W_commutes_T`.
