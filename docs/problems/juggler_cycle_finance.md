# Juggler cycle finance inequality

Status: **THEOREM**

Standalone application phase on the Juggler floor-power map, on the
**cycle half** of the `cycles_or_escapes` split. It is not a halt
theorem, not an escape/divergence statement, not a corridor
extension past depth 13, not a reopen of any windowed population
census, and not a claim that every positive integer reaches 1.

The census line (`no_cycle_word_length_le_eight`) excludes cycle
words length by length. This phase asks a transversal question:
does the exact defect bookkeeping around a hypothetical cycle bound
the cycle **minimum** as a function of the cycle **length**, so that
one verified floor kills every length at once outside an explicit
exceptional set?

## Problem

For a hypothetical Juggler cycle of length \(L\) with \(o\) odd
letters, the word is formally expanding
(\(2^L<3^o\), `cycle_word_formally_expanding`), yet the orbit
returns exactly. The multiplicative surplus must be financed
entirely by the floor defects, which are relatively tiny. How much
does that force?

## Exact statement

**Cycle finance inequality (EXACT — HUMAN PROOF, proof below).**
Let \(x_0\to x_1\to\cdots\to x_L=x_0\) be a cycle of the Juggler map
\(T\) with every state \(\ge 12\), word length \(L\ge 1\), and
\(o\) odd letters. Let \(n=\min_i x_i\). Then

\[
1-\frac{2^L}{3^o}
\;\le\;\frac65\sum_{i=1}^{L}\frac{1}{x_i\ln x_i}
\;\le\;\frac65\cdot\frac{L}{n\ln n},
\qquad\text{i.e.}\qquad
n\ln n\;\le\;\frac65\cdot\frac{L\cdot 3^{o}}{3^{o}-2^{L}}.
\]

The right side is worst (largest) at the minimal admissible
\(o_{\min}(L)=\min\{o:3^o>2^L\}\). Define

\[
B(L)=\frac65\cdot\frac{L\cdot 3^{o_{\min}}}{3^{o_{\min}}-2^{L}},
\qquad
n_{\max}(L)=\max\{n\in\mathbb N: n\ln n\le B(L)\}.
\]

**Per-length exclusion corollary.** If every \(2\le n\le N_0\)
reaches \(1\), then no state of a cycle can be \(\le N_0\) (a
periodic state never reaches 1), so no Juggler cycle of length
\(L\) exists whenever \(n_{\max}(L)\le N_0\).

### Proof of the finance inequality

Every state satisfies \(x_{i+1}=\lfloor\sqrt{x_i^{e_i}}\rfloor\)
with \(e_i=1\) (even) or \(e_i=3\) (odd). Hence the exact step
identity

\[
x_{i+1}^2=x_i^{e_i}-d_i,\qquad 0\le d_i\le 2x_{i+1},
\]

because \(x_i^{e_i}<(x_{i+1}+1)^2=x_{i+1}^2+2x_{i+1}+1\). (This is
the local defect of `Defect.lean`; composing it around a word is the
Lean `global_defect_identity`.) The relative defect

\[
\delta_i=\frac{d_i}{x_i^{e_i}}\le\frac{2x_{i+1}}{x_{i+1}^2}
=\frac{2}{x_{i+1}}\le\frac16
\]

using \(x_i^{e_i}\ge x_{i+1}^2\) and \(x_{i+1}\ge 12\). Write
\(t_i=\ln x_i\) and \(\varepsilon_i=-\tfrac12\ln(1-\delta_i)\ge0\);
taking logarithms of the step identity,

\[
t_{i+1}=\frac{e_i}{2}\,t_i-\varepsilon_i .
\]

On \([0,\tfrac16]\) the function
\(g(\delta)=\tfrac65\delta+\ln(1-\delta)\) has \(g(0)=0\) and
\(g'(\delta)=\tfrac65-\tfrac1{1-\delta}\ge0\), so
\(-\ln(1-\delta)\le\tfrac65\delta\) and

\[
\varepsilon_i\le\frac35\,\delta_i\le\frac{6/5}{x_{i+1}} .
\]

Let \(P_k=\prod_{j<k}(e_j/2)\), so \(P_L=3^o/2^L\). Unrolling the
recursion,

\[
t_L=P_L\,t_0-\sum_{i=0}^{L-1}\frac{P_L}{P_{i+1}}\,\varepsilon_i,
\]

and periodicity \(t_L=t_0\) gives the financing identity

\[
t_0\,(P_L-1)=\sum_{i=0}^{L-1}\frac{P_L}{P_{i+1}}\,\varepsilon_i .
\]

Since every \(\varepsilon_j\ge0\), dropping them in the unroll gives
\(t_{i+1}\le P_{i+1}t_0\), i.e. \(P_{i+1}\ge t_{i+1}/t_0\), so
\(P_L/P_{i+1}\le P_L\,t_0/t_{i+1}\). Dividing the financing identity
by \(P_L\,t_0\):

\[
1-\frac1{P_L}
\;\le\;\sum_{i=0}^{L-1}\frac{\varepsilon_i}{t_{i+1}}
\;\le\;\frac65\sum_{i=0}^{L-1}\frac1{x_{i+1}\ln x_{i+1}}
\;\le\;\frac65\cdot\frac{L}{n\ln n}. \qquad\blacksquare
\]

The state floor \(x_i\ge12\) is available: every \(n\le11\) reaches
\(1\) (Lean `reachesOne_of_lt_twelve`), and a periodic state never
reaches \(1\).

## Current literature

- Collatz m-cycle exclusion by financing-versus-gap plus bounds on
  \(|2^L-3^o|\) — **known**
  (`simons-de-weger-2005-collatz-m-cycles`); this branch is the
  floor-power adaptation, **independent** of that proof's details.
  The structural difference: Juggler per-step defects are relatively
  \(O(1/x)\) in logarithms, versus \(O(1)\) for Collatz, so the
  financing constraint is far more lopsided here.
- Small-cycle census — **EXACT — LEAN VERIFIED**
  (`no_cycle_word_length_le_eight`,
  [juggler_length_eight_cycles.md](juggler_length_eight_cycles.md))
- Formal expansion of cycle words — **EXACT — LEAN VERIFIED**
  (`cycle_word_formally_expanding`)
- Global defect identity — **EXACT — LEAN VERIFIED**
  (`global_defect_identity`,
  [juggler_global_defect.md](juggler_global_defect.md))
- Peak-block financing at the cycle maximum — **EXACT — LEAN
  VERIFIED** (`cycle_peak_finance`); local to the peak, distinct
  from the whole-cycle log financing used here
- Residual landing class \(\{1,\dots,11\}\) reaches 1 — **EXACT —
  LEAN VERIFIED** (`reachesOne_of_lt_twelve`)
- Every start reaches 1 — not claimed

Project relationship: **extended**.

## Branch budget

```text
Mathematical target     Does the exact defect-financing identity around a cycle force
                        n·ln n <= (6/5)·L·3^o/(3^o − 2^L), and does this, combined with
                        exact min|3^o − 2^L|, the length-<=8 census, and a verified
                        floor, exclude all Juggler cycles outside a finite set of
                        near-convergent lengths?
Novelty hypothesis      A Simons–de Weger-style cycle elimination for the Juggler map.
                        Nothing in the ledger combines the global defect identity with
                        two-power/three-power gap lower bounds.
Falsifier               Financing slack measured on real orbit segments violates the
                        per-step bound eps_i <= (6/5)/x_{i+1}, or the min bound stays
                        above any reachable floor for infinitely many lengths in a way
                        that is not confined to near-convergent L.
Existing machinery      globalDefect identity, pathDefectSum/pathPows, cycle_word_
                        formally_expanding, cycle_peak_finance, CycleDiophantine, census
                        <= 8, reachesOne_of_lt_twelve, Python juggler tooling.
Maximum Phase-0 scope   Derivation note + one computational probe: exact gap table
                        L <= 10^5, min-bound tabulation, floor verification by descent
                        induction to 10^6, per-step slack stress test. No new Lean.
Promotion criterion     Inequality verified with clean L-independent constants AND the
                        exceptional-length set is finite/structured so that finance +
                        census + a realistic floor raise covers all L -> PROMOTE to Lean.
Stop criterion          Constant degrades with L, or exceptional lengths require floors
                        beyond feasible computation -> PARK with the quantitative
                        frontier recorded. Inequality falsified on orbit data -> CLOSE.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Step identity \(x_{i+1}^2=x_i^{e_i}-d_i\), \(0\le d_i\le
  2x_{i+1}\) — **KNOWN** (integer form of `Defect.lean`)
- Whole-cycle log financing identity
  \(t_0(P_L-1)=\sum_i(P_L/P_{i+1})\varepsilon_i\) — **EXACT — HUMAN
  PROOF** (this dossier)
- Finance inequality \(n\ln n\le\frac65 L\,3^o/(3^o-2^L)\) —
  **EXACT — HUMAN PROOF** (this dossier)
- Per-length exclusion given a verified floor —
  **COMPUTATIONALLY VERIFIED** at the Phase-0 window (below)
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_finance`
- Records: [juggler_cycle_finance.md](../research/juggler_cycle_finance.md),
  [juggler_cycle_finance.json](../research/juggler_cycle_finance.json)
- Dataset: `data/research/juggler/cycle_finance/`
- Tests: `tests/research/juggler_sequence/test_cycle_finance.py`

Science window: gap table \(L\le 10^5\) with exact bignum
arithmetic; floor verification by first-passage descent induction
for all \(2\le n\le 10^6\); slack stress on named hard seeds
(including \(30817\)). Tests use \(L\le 400\) and floor \(2000\).
No CLI. No new Lean.

## Conjectures

None opened. (The statement "no Juggler cycle of any length" is a
target, not a conjecture entered in `conjectures/`.)

## Counterexamples

None. The per-step bound \(\varepsilon_i\le(6/5)/x_{i+1}\) held at
every measured step; see Results.

## Formalization

None added in Phase 0. The inequality is designed to sit on
existing Lean structures: the step identity is `Defect.lean`, the
composed identity is `global_defect_identity`, and the cycle-side
bookkeeping is `pathDefectSum`/`pathPows` in `CycleExtrema.lean`.
A Lean port needs `Real.log` arithmetic on top of these. No
`CycleFinance.lean` exists. No `sorry`. Paper A is unchanged.

## Results

Classification **CYCLE_FINANCE_GREEN**. Regenerate with
`python -m research.juggler_sequence.cycle_finance`; records in
[juggler_cycle_finance.md](../research/juggler_cycle_finance.md)
and `data/research/juggler/cycle_finance/`.

- **Finance inequality** — **EXACT — HUMAN PROOF** (above). The
  per-step ingredient \(\varepsilon_i\le(6/5)/x_{i+1}\) held at
  every measured orbit step with relative margin \(\ge 0.17\); the
  unrolled log identity reproduced every orbit exactly (relative
  error \(\le 2\cdot10^{-16}\)); real orbits use only \(0.22\)–
  \(0.47\) of the financing budget (mean defect ratio
  \(d/(2x')\approx 0.5\)).
- **Floor** — **COMPUTATIONALLY VERIFIED**: every
  \(2\le n\le 10^6\) has a finite first passage below its start,
  hence by strong induction reaches \(1\). Max first-passage length
  \(253\) steps (seed \(78901\)); peak intermediate value
  \(6{,}342{,}922\) bits (\(\approx 1.9\cdot10^6\) digits). Exact
  integer arithmetic throughout.
- **Per-length exclusion** — **COMPUTATIONALLY VERIFIED** (exact
  gap table \(L\le10^5\), conservative rounding): with the floor
  \(N_0=10^6\), **no Juggler cycle of length \(L\le 1053\)
  exists**, and no cycle of any length \(L\le 10^5\) outside an
  explicit set of \(397\) exceptional lengths. The Lean census
  reaches \(L\le 8\); the finance route multiplies the excluded
  range by \(\approx 130\) with one inequality and one floor.
- **Exceptional structure**: the \(397\) exceptions are exactly the
  near-convergent lengths — the \(94\) multiples of \(1054\) plus
  combinations such as \(23757=22\cdot1054+569\). The record
  (one-sided best-approximation) lengths in range are
  \(L=1,3,11,19,84,569,1054,25781,50508\) with
  \(n_{\max}=3,13,52,297,5599,58398,\approx2.0\cdot10^6,
  \approx6.7\cdot10^7,\approx4.2\cdot10^8\); they track the
  continued-fraction convergents of \(\ln 2/\ln 3\).
- **Floor sensitivity**: a floor of \(10^9\) would leave **zero**
  exceptions below \(L=10^5\) (the worst requirement in range is
  \(n_{\max}(50508)\approx4.2\cdot10^8\)).
- **Census cross-check**: at \(L\le 8\) the finance bound plus the
  Lean residual floor (\(n\le11\) reaches 1) independently kill
  \(L\in\{1,2,4,5,7,8\}\); \(L\in\{3,6\}\) (the near-tight
  \(2^3<3^2\) and its double) remain census-only — consistent with
  and transversal to `no_cycle_word_length_le_eight`.

## Open questions

- The exceptional near-convergent lengths need either a larger
  verified floor (each factor of \(10^3\) in floor pushes the
  frontier roughly one convergent out), a Baker-type lower bound on
  \(3^o-2^L\), or near-tight rigidity (`NearTightScale.lean`) to
  cover all \(L\) simultaneously; the finance inequality bounds the
  minimum per length, not the length itself.

## Decision

**PROMOTE**. The finance inequality is new exact structure: it is
the first mechanism in the laboratory that excludes cycle lengths
wholesale (all \(L\le1053\), versus \(L\le8\) from the census) and
it reduces the cycle half of `cycles_or_escapes` to a quantitative
frontier — verified floor versus convergent denominators of
\(\ln2/\ln3\) — with clean, \(L\)-independent constants that real
orbits satisfy with a factor-two margin. The falsifier did not
fire. Promotion is to Lean formalization of the inequality on top
of `pathDefectSum`/`global_defect_identity` (with `Real.log`),
which would make the wholesale length exclusion
`EXACT — LEAN VERIFIED` modulo a Lean-checked floor.

Best next question: can the finance inequality be formalized in
`formal/Problems/Juggler/` (log-free rational form or `Real.log`
form over `pathDefectSum`), so that `no cycle of length <= 1053`
becomes Lean-verified once a Lean-checked floor replaces the
Python descent induction?

## Publication assessment

Status: `THEOREM`. One exact inequality with a genuinely new
consequence (wholesale cycle-length exclusion) and a clear
literature distinction: the Simons–de Weger financing-versus-gap
template transferred to a floor-power map where defects are
relatively \(O(1/x)\) in logarithms. Not a totality result; the
escape half is untouched.
