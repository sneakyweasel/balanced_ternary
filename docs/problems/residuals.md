# Cubic residual Newton stratum

Status: **STRUCTURAL**

This module does **not** give a closed formula for \(M_k(x^3)\).

## Exact statement

At horizon \(k\) and deficit \(r\) with \(r+1\le k\), classify same-depth
fibres of \(F_k\) at depth \(m=k-1-r\) by \(N_2\) visibility, \(N_1\)
valuation, and the mismatched \(N_0\) quotient \(Q_{t,K,W}\).

## Why balanced ternary is relevant

Residuals are the section-calculus Mealy machine of `bt.calculus`. Packed
prefixes are balanced-ternary words of length \(m\).

## Existing record

Canonical mathematics: [cubic_newton_stratum.md](../theory/cubic_newton_stratum.md).
Literature distinction: [residual_vs_classical.md](../theory/residual_vs_classical.md).

## Lean

`formal/BTCalculus/NewtonStratum.lean`, composing existing cubic modules.

## Conjectures / refutations

No new conjecture. Layer-by-layer hypotheses that failed are recorded on
the theorem ledger (`BTA-x3-*` REFUTED rows).
