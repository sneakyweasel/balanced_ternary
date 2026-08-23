# Cubic residual Newton stratum

Status: **STRUCTURAL**

The dedicated \(x^3\) counting line is `CLOSE`d
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
Sendable extract: [newton_stratum_note.md](../theory/newton_stratum_note.md).
Literature distinction: [residual_vs_classical.md](../theory/residual_vs_classical.md).

## Lean

`formal/BTCalculus/NewtonStratum.lean` and
`formal/BTCalculus/XCubeStateComplexity.lean`.

## Conjectures / refutations

No new conjecture. Layer-by-layer hypotheses that failed are recorded on
the theorem ledger (`BTA-x3-*` REFUTED rows).

## Branch budget

- **Target:** an exact formula or recurrence for the Myhill–Nerode count
  \(M_k(x^3)\).
- **Novelty hypothesis:** the Newton hierarchy \((N_2,N_1,N_0)\) reduces
  the fibres of \(F_k\) to a compact arithmetic count.
- **Falsifier:** a fibre family with no bounded classifier, or an
  overlap structure that still needs width-\(\Theta(k)\) enumeration.
- **Existing machinery:** `bt.calculus` sections and residuals,
  `research.residuals`, `formal/BTCalculus/NewtonStratum.lean`.
- **Maximum Phase-0 scope:** exact tables to \(k\le 14\) plus the
  same-depth criterion.
- **Promotion criterion:** a closed term \(M_k=F(k)\), or a polynomial
  algorithm.
- **Stop criterion:** a rigorous information-growth obstruction.

The falsifier fired twice: \(Q\) has no bounded residue / valuation /
\(B_t\) classifier, and the deep-image union still requires hashing
width-\(\Theta(k)\) intervals (`BTA-x3-M-obstruct`).

## Decision

`CLOSE` for the dedicated counting line, `PROMOTE` for the structural
Newton-stratum theory that came out of it. The stratum theorems — the
same-depth criterion, the \(N_2\) visibility law, the \(N_1\) valuation
stratification, the two-regime \(N_0\) reduction, and the \(Q\)
reconstruction criterion — are exact and largely Lean-verified. The
\(M_k\) table is a computational appendix, not a theorem. Do not invent
further fibre types and do not open another \(x^3\) counting milestone.

Best next question: does the Newton-stratum machinery say anything exact
about a polynomial family other than \(x^3\)?

## Publication assessment

Status: `STRUCTURAL`. The stratum theory is paper-worthy; the counting
line is not, and its obstruction is recorded rather than retried. The
short extract [newton_stratum_note.md](../theory/newton_stratum_note.md)
packages the unified theorem and the \(Q\) boundary. It is not a
`PAPER_CANDIDATE` elevation.
