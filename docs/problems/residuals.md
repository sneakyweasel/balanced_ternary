# Cubic residual Newton stratum

Status: **STRUCTURAL**

The dedicated \(x^3\) counting line is closed at Outcome C
([cubic_newton_stratum.md](../theory/cubic_newton_stratum.md) §8).
Same-depth counts \(C_{k,m}\) are exact. This module does **not** give
a single closed term for \(M_k(x^3)\).

## Exact statement

At horizon \(k\) and deficit \(r\) with \(r+1\le k\), count same-depth
Newton classes of \(F_k\) at depth \(m=k-1-r\) by the injective
\(v_3(p)<r\) region plus the joint core image
\((N_1,Q)\) on \(u\in P_{k-1-2r}\). Then \(M_k(x^3)\) is the
\(N_3\)-gated union of those images. The remaining arithmetic is the
vanishing locus of \(Q\) on \(P_W\) together with classified but
non-closed-form deep overlaps.

## Why balanced ternary is relevant

Residuals are the section-calculus Mealy machine of `bt.calculus`. Packed
prefixes are balanced-ternary words of length \(m\).

## Existing record

Canonical mathematics: [cubic_newton_stratum.md](../theory/cubic_newton_stratum.md).
Literature distinction: [residual_vs_classical.md](../theory/residual_vs_classical.md).

## Lean

`formal/BTCalculus/NewtonStratum.lean` and
`formal/BTCalculus/XCubeStateComplexity.lean`.

## Conjectures / refutations

No new conjecture. Layer-by-layer hypotheses that failed are recorded on
the theorem ledger (`BTA-x3-*` REFUTED rows).
