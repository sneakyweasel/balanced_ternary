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
Quartic gate: `src/research/residuals/x4_stratum.py`.

## Lean

`formal/BTCalculus/NewtonStratum.lean` and
`formal/BTCalculus/XCubeStateComplexity.lean`.
General residual interface:
`formal/BTCalculus/NewtonKernel.lean` (`I_k` for every degree) and
`formal/BTCalculus/ResidualShift.lean` (`eval_residualAlong`).

## Conjectures / refutations

No new conjecture. Layer-by-layer hypotheses that failed are recorded on
the theorem ledger (`BTA-x3-*` REFUTED rows). The \(x^4\) visibility
hypothesis (some \(N_j\) sees \(p\bmod 3^r\)) is refuted at
\((k,r)=(4,1)\).

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

## \(x^4\) Phase 0

Range recorded separately from the verdict: same-depth fibres of
\(F_k\) for \(x^4\) at \(2\le k\le 7\) and \(r\in\{0,1\}\),
\(m=k-1-r\). Code: `research.residuals.x4_stratum`. Tests pin the
closed form against `residual_along` and the visibility verdict at
\(k\le 5\); the \(k\le 7\) scan is marked slow.

Counterexample to residue visibility: at \((k,r)=(4,1)\), every
\(N_j\) fails \(N_j(p)\equiv N_j(q)\iff p\equiv q\pmod 3\). The
would-be visible coordinate is \(N_3=6B+36A\) with
\(B=4p\,3^{2m}\), already \(0\bmod 3^k\).

## Decision

`CLOSE` for the dedicated counting line, `PROMOTE` for the structural
Newton-stratum theory that came out of it. The stratum theorems — the
same-depth criterion, the \(N_2\) visibility law, the \(N_1\) valuation
stratification, the two-regime \(N_0\) reduction, and the \(Q\)
reconstruction criterion — are exact and largely Lean-verified. The
\(M_k\) table is a computational appendix, not a theorem. Do not invent
further fibre types and do not open another \(x^3\) counting milestone.

`CLOSE` for the \(x^4\) visibility gate (Phase 0, \(k\le 7\), deficits
\(r\in\{0,1\}\)). The linear-in-\(p\) monomial of
\(D^m((p+3^m x)^4)\) is \(4p\,3^{2m}x^3\), valuation \(2m\) on units.
At \(m=k-1-r\) this is already \(\ge k\) for \(r\le 1\) and \(k\ge 3\),
so \(N_3\) and \(N_4\) vanish. No \(N_j\) satisfies
\(N_j(p)\equiv N_j(q)\iff p\equiv q\pmod{3^r}\) once \(|P_m|>3\)
(\(k\ge 4\) at \(r=1\)). The surviving coordinate is the square filter
\(N_2\equiv 4p^2 3^{k-1}\pmod{3^k}\), which is the cubic \(N_1\)
pattern, not residue visibility. The leftover on \(p=3^ru\) is the
two-regime \(D^{m-4r}(u^4)\) / \(3^{4r-m}u^4\) image — another unmatched
fourth-power quotient. \(N_1\) visibility at \((k,r)=(3,1)\) is a
width-\(3\) accident. Not a degree increment of the cubic tower
(\(N_2\mapsto N_3\), \(3r\mapsto 4r\) would have kept \(N_3\) visible).
Do not open \(x^5\), a quartic count, or a fibre taxonomy.

`PROMOTE` the degree-\(\le 3\) visibility class, `CLOSE` the
general-\(f\) classifier. At deficit \(r=1\) and \(k\in\{4,5\}\), a
polynomial of degree at most 3 has a Newton coordinate that sees
\(p\bmod 3\) if and only if \(v_3(a_3)=0\). The same one-line law
fails in degree 4 and 5: \(x^3+x^4\) is a same-valuation \(p^2\)
contamination, and \(x^5\) sees residues via \(p^3\equiv p\pmod 3\).
Do not start a degree-\(5\) fibre taxonomy.

`CLOSE` the residual-of-addition candidate. Along any word,
\(\mathrm{residual}(f+g)-\mathrm{residual}(f)-\mathrm{residual}(g)\)
is a constant, equal to the iterated trit carry
\((\rho(f)+\rho(g)-\rho(f+g))/3\). That is the rewrite-calculus carry,
not a new polynomial state.

`CLOSE` the Eisenstein dictionary. \(3\sim(1-\omega)^2\) and the Pólya
property of \(\mathbb Q(\omega)\) are **KNOWN**; translating \(N_2\)
into \((1-\omega)\)-adic language is a **REPARAMETERIZATION** of the
cubic law. See [residual_vs_classical.md](../theory/residual_vs_classical.md).

`PROMOTE` the one-state realization lemma, `CLOSE` the Mealy census.
The only residual machines with one state are the machines of
\(ax\) for \(a\in\{-1,0,+1\}\). There are \(3^6=729\) abstract
one-state trit/trit tables; three are realized. Two-state residual
graphs in the degree-\(\le 2\) coefficient box \(\{-2,\ldots,2\}\)
number 12. A general Mealy table with independent \(\rho\) and
\(\delta\) is not a residual machine: output is
\([f(a)]_3\) and the next state is \(\mathfrak D_a f\). That is the
definition of `residual_along`, not a new class. Do not enumerate
nine-state machines.

Best next question: none on monomial strata, Eisenstein rewrites, or
Mealy realization. The cubic tower is degree-\(3\) specific because
only then is the linear residual coefficient of valuation \(m\), and
the degree-\(\le 3\) class is exactly “cubic coefficient a unit.”

## Publication assessment

Status: `STRUCTURAL`. The stratum theory is paper-worthy; the counting
line is not, and its obstruction is recorded rather than retried. The
short extract [newton_stratum_note.md](../theory/newton_stratum_note.md)
packages the unified theorem and the \(Q\) boundary. It is not a
`PAPER_CANDIDATE` elevation. The \(x^4\) gate adds a named obstruction,
not a new theorem to elevate.
