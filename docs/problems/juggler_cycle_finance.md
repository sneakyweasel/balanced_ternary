# Juggler cycle finance inequality

Status: **THEOREM**

Standalone application phase on the Juggler floor-power map, on the
**cycle half** of the `cycles_or_escapes` split. It is not a halt
theorem, not an escape/divergence statement, not a corridor
extension past depth 13, not a reopen of any windowed population
census, and not a claim that every positive integer reaches 1.

The census line (`no_cycle_word_length_le_nineteen`) excludes cycle
words length by length through \(19\). This phase asks a
transversal question:
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

**Cycle finance inequality (EXACT — LEAN VERIFIED,
`cycleMin_finance`).**
Let \(x_0\to x_1\to\cdots\to x_L=x_0\) be a cycle of the Juggler map
\(T\) taken at a `CycleMin` start \(n\ge 2\), word length \(L\ge 1\),
and \(o\) odd letters. Then

\[
n\log n\cdot(3^o-2^L)\;\le\;L\cdot 3^o.
\]

The Lean form uses the dyadic-cell bound \(\log z\le 2\log y+2/y\)
(\(\log(1+1/y)\le 1/y\)) and has constant \(1\). The Phase-0
computational table used the weaker constant \(6/5\) below, which
remains valid and is the source of the \(L\le 10^5\) exclusions.

**Weaker computational form (EXACT — HUMAN PROOF, proof below).**
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

**Eliahou leftover (EXACT — LEAN VERIFIED implication
`cycle_word_eliahou_leftover`; instance COMPUTATIONALLY
VERIFIED).** If a nontrivial cycle word exists at \(n\ge 2\), and
every length in \([30,10^5)\) outside a named list of
near-convergents is already excluded, then the period is \(84\),
or belongs to that list, or is at least \(10^5\). This is
bookkeeping on `cycle_word_length_eighty_four_or_ge_eighty_five`
plus the finance table: not a new inequality. The instance at the
Python floor \(N_0=10^6\) is the existing family of \(397\)
near-convergent lengths. Length \(84\) is the Lean-named leftover
and is computationally already excluded; height finance further
requires at least three odd-runs
(`cycle_word_length_eighty_four_m_ge_three_or_ge_eighty_five`).
Lengths \(19\), \(38\), \(57\), and \(76\) die at the Lean
residual floor \(261\).

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
- Eliahou leftover packaging for Collatz — **known** (period
  \(\ge X\), or one of a named convergent family). The Juggler
  analogue is `cycle_word_eliahou_leftover`: period \(84\), or a
  listed near-convergent, or \(\ge 10^5\).
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
  PROOF** (this dossier; Lean uses the equivalent cell unroll
  `cycleMin_log_envelope`)
- Finance inequality \(n\log n\cdot(3^o-2^L)\le L\cdot 3^o\) —
  **EXACT — LEAN VERIFIED** (`cycleMin_finance`)
- Weaker form \(n\ln n\le\frac65 L\,3^o/(3^o-2^L)\) —
  **EXACT — HUMAN PROOF** (Phase-0 computational table)
- No cycle word of length \(\le 19\) —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_length_le_nineteen`)
- Period is \(84\) or \(\ge 85\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_word_length_eighty_four_or_ge_eighty_five`);
  the cheap leftovers \(57\) and \(76\) die at the floor \(261\);
  \(L=84\) is the next record near-convergent
- Period is \(84\) with at least three odd-runs, or \(\ge 85\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_word_length_eighty_four_m_ge_three_or_ge_eighty_five`)
- Period is \(57\) or \(\ge 58\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_word_length_fifty_seven_or_ge_fifty_eight`), the
  weaker leftover before the two extra odd seeds
- Period is \(38\) or \(\ge 39\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_word_length_thirty_eight_or_ge_thirty_nine`), the
  weaker leftover before the \(61/11\) certificate
- Period is \(19\) or \(\ge 30\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_word_length_nineteen_or_ge_thirty`), the weaker
  floor-\(53\) leftover
- Eliahou leftover: period \(84\), or a listed near-convergent, or
  \(\ge 10^5\) —
  **EXACT — LEAN VERIFIED** as the implication
  `cycle_word_eliahou_leftover`; the \(397\)-family instance is
  **COMPUTATIONALLY VERIFIED**
- Period is \(\ge 14\) —
  **EXACT — LEAN VERIFIED** (`cycle_word_length_ge_fourteen`),
  a corollary of the stronger leftover
- Residual floor \(n<261\) reaches \(1\) —
  **EXACT — LEAN VERIFIED**
  (`reachesOne_of_lt_two_hundred_sixty_one`)
- Residual floor \(n<257\) reaches \(1\) —
  **EXACT — LEAN VERIFIED**
  (`reachesOne_of_lt_two_hundred_fifty_seven`)
- Residual floor \(n<53\) reaches \(1\) —
  **EXACT — LEAN VERIFIED** (`reachesOne_of_lt_fifty_three`)
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
No CLI. Lean: `CycleFinance.lean` (`cycleMin_finance`,
`cycle_finance_min_two_hundred_fifty_seven`,
`no_cycle_word_length_le_nineteen`,
`cycle_word_length_eighty_four_or_ge_eighty_five`,
`cycle_word_eliahou_leftover`), `CycleHeightFinance.lean`
(`cycle_word_length_eighty_four_m_ge_three_or_ge_eighty_five`),
`TerminationFloor257.lean`
(`reachesOne_of_lt_two_hundred_fifty_seven`), and
`Termination.lean` (`reachesOne_of_lt_fifty_three`). Paper A is
unchanged.

## Conjectures

None opened. (The statement "no Juggler cycle of any length" is a
target, not a conjecture entered in `conjectures/`.)

## Counterexamples

None. The per-step bound \(\varepsilon_i\le(6/5)/x_{i+1}\) held at
every measured step; see Results.

## Formalization

`CycleFinance.lean` sits on `CycleCore` and `LengthEightCensus`.
The cell logarithm bound is `log_le_two_log_add`; the unrolled
envelope is `cycleMin_log_envelope`; the inequality is
`cycleMin_finance`. The residual floor `257`
(`reachesOne_of_lt_two_hundred_fifty_seven`) gives
`cycle_finance_min_two_hundred_sixty_one`, hence
`no_cycle_word_length_le_nineteen` and the length leftover
`cycle_word_length_eighty_four_or_ge_eighty_five`. Lengths `19`
and `30`–`83` die by finance at floors `257` and `261`. The
floor-`261` comparison uses \(261\log 257>15921/11\); \(L=84\)
survives the uniform bound. `CycleHeightFinance.lean` keeps the
inv-sum defects and excludes every length-`84` word with at most
two odd-runs, so the laboratory leftover is
`cycle_word_length_eighty_four_m_ge_three_or_ge_eighty_five`.
Eliahou packaging `cycle_word_eliahou_leftover` still rewrites
the length leftover plus the finance table as period `84`, or
a listed near-convergent, or at least `10^5`. There is no theorem named
`no_cycle_word_length_eleven`: that name is reserved by the
parked leftover-word probes. No `sorry`. Paper A is unchanged.
Not a halt theorem and not `no_cycle_word_any_length`.
The Python floor \(N_0=10^6\) is still
**COMPUTATIONALLY VERIFIED**, not Lean.

## Results

Classification **CYCLE_FINANCE_GREEN**. Regenerate with
`python -m research.juggler_sequence.cycle_finance`; records in
[juggler_cycle_finance.md](../research/juggler_cycle_finance.md)
and `data/research/juggler/cycle_finance/`.

- **Finance inequality** — **EXACT — LEAN VERIFIED**
  (`cycleMin_finance`): \(n\log n\cdot(3^o-2^L)\le L\cdot 3^o\).
  The Phase-0 per-step ingredient \(\varepsilon_i\le(6/5)/x_{i+1}\)
  held at every measured orbit step with relative margin
  \(\ge 0.17\); the unrolled log identity reproduced every orbit
  exactly (relative error \(\le 2\cdot10^{-16}\)); real orbits use
  only \(0.22\)–\(0.47\) of the financing budget (mean defect
  ratio \(d/(2x')\approx 0.5\)).
- **Lean residual floor \(261\)** — **EXACT — LEAN VERIFIED**
  (`reachesOne_of_lt_two_hundred_sixty_one`): two extra odd
  seeds \(257\) and \(259\) (five steps, \(13\)-bit peaks)
  raise the floor past the exact-log barrier at \(257\)
  (\(257\ln 257\approx1426<1430.8=n_{\mathrm{need}}(57)\)).
  Combined with \(261\log 257>15921/11\) this excludes the
  cheap leftovers \(57\) and \(76\).
- **Lean residual floor \(257\)** — **EXACT — LEAN VERIFIED**
  (`reachesOne_of_lt_two_hundred_fifty_seven`): every
  \(1\le n<257\) reaches \(1\). Evens below \(2809\) already
  reduce to \(\{1,\dots,52\}\); the odd seeds \(53,55,\dots,255\)
  are finite orbit certificates (the longest is \(193\),
  seventy-three steps). Combined with `cycleMin_finance` this
  excludes length \(19\). The tighter certificate
  \(\log 257>61/11\) also excludes length \(38\). The Python
  \(6/5\) table has \(n_{\max}(19)=297\); the Lean constant
  \(1\) only needs \(n\ln n>1411.63\), so the smallest such
  \(n\) is \(255\).
- **Lean residual floor \(53\)** — **EXACT — LEAN VERIFIED**
  (`reachesOne_of_lt_fifty_three`): every \(1\le n<53\) reaches
  \(1\). Evens below \(144\) already reduce to \(\{1,\dots,11\}\);
  the odd seeds \(13,15,\dots,51\) are finite orbit certificates
  (the longest is \(37\), seventeen steps, peak
  \(\approx 2.5\cdot10^{13}\)).
- **Lean census extension** — **EXACT — LEAN VERIFIED**: no cycle
  word of length \(\le 19\); lengths \(30\)–\(83\) die at floors
  \(257\) and \(261\); any remaining cycle has period \(84\) with
  at least three odd-runs, or \(\ge 85\). The cheap leftovers
  \(57\) and \(76\) die at floor \(261\)
  (`finance_excludes_length_fiftyseven`,
  `finance_excludes_length_seventysix`). Uniform finance leaves
  \(L=84\) open (\(\tfrac{15921}{11}\), need \(\approx 40269\));
  height finance kills \(m\le 2\).
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
  explicit set of \(397\) exceptional lengths.   The Lean census now reaches \(L\le 83\) except the leftover
  \(84\) (finance at \(9\)–\(11\), \(14\)–\(19\), and
  \(20\)–\(83\)); the computational finance route multiplies the
  excluded range by \(\approx 130\) with one inequality and one
  Python floor.
- **Eliahou leftover** — **EXACT — LEAN VERIFIED** implication
  (`cycle_word_eliahou_leftover`): period \(84\), or a listed
  near-convergent, or \(\ge 10^5\). The instance at floor
  \(10^6\) is **COMPUTATIONALLY VERIFIED** (the existing \(397\)
  near-convergents). Length \(84\) is kept as the Lean-named
  leftover; the Python floor already excludes it. Lengths
  \(19\), \(38\), \(57\), and \(76\) are no longer Lean leftovers.
  Not a new inequality.
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

- The Lean leftover is \(L=84\) with at least three odd-runs, or
  \(L\ge 85\); Eliahou packaging still names the length leftover
  as \(84\), or a listed near-convergent, or \(\ge 10^5\).
  Cheap \(19\)-gap cousins \(95,114,\ldots\) sit in the
  \(\ge 85\) bucket. Global finance kills \(L=84\) only at residual
  floor \(4756\) (constant \(1\); Python \(n_{\max}=5599\)). That
  campaign is **PARK**: \(2247\) new odd certificates, peak
  \(19694\) bits at \(n=2183\), and \(4756>53^2\). Joint-minima
  and the height law kill every \(m\) first, at floor \(1981\)
  (constant \(1\)), still \(859\) odds with a \(900\)-bit peak.
  Height kills \(L=84\) as a 1-cycle or 2-cycle at the live floor
  \(261\), now **EXACT — LEAN VERIFIED**. The hypothesis that
  \(4756\) is the cheapest kill is **REFUTED**
  (`conjectures/refuted/juggler_cycle_finance_l84_floor_4756.json`).
  Length \(84\) with \(m\ge 3\) is the remaining named leftover.
- The exceptional near-convergent lengths need a larger verified
  floor (each factor of \(10^3\) in floor pushes the frontier
  roughly one convergent out). The finance inequality bounds the
  minimum per length, not the length itself. A Baker / Rhin lower
  bound on \(\lvert 3^o-2^L\rvert\) does **not** kill leftover
  near-convergents
  ([juggler_cycle_gap_baker.md](juggler_cycle_gap_baker.md),
  **CLOSE**). Near-tight rigidity (`NearTightScale.lean`) does
  **not** cover leftover \(L\) simultaneously
  ([juggler_cycle_near_tight.md](juggler_cycle_near_tight.md),
  **CLOSE**): cycle \(1+q=n^{3^o-2^L}\) is the opposite of
  open-orbit \(q\to 0\). Christoffel / mechanical-word unique
  maximizers do **not** reduce leftover-word or CycleMin
  candidates to a one-parameter necklace
  ([juggler_cycle_christoffel.md](juggler_cycle_christoffel.md),
  **CLOSE**).

## Decision

**PROMOTE**. Two extra odd seeds (\(257\), \(259\); five steps
each) raise the residual floor to \(261\) and exclude the cheap
leftovers \(57\) and \(76\). The length leftover is the record
convergent: period \(84\) or \(\ge 85\). Height finance then
kills every length-\(84\) word with at most two odd-runs, so the
laboratory leftover is period \(84\) with \(m\ge 3\), or
\(\ge 85\). Eliahou packaging still rewrites the length leftover
as period \(84\), or a listed near-convergent, or \(\ge 10^5\).
Exact \(\log 257\) cannot kill \(57\). This is not a leftover-word
census. The Python floor \(N_0=10^6\) remains
**COMPUTATIONALLY VERIFIED**. Paper A is unchanged.

The residual-floor campaign past \(\approx 4756\) is **PARK**.
Joint/height kill every \(m\) at \(1981\), still machinery
gravity.

Best next question: exclude length \(84\) at \(m\ge 3\) by a
different argument at floor \(261\), or stop and write the
finance theorem as it stands.

## Publication assessment

Status: `THEOREM`. One exact inequality (`cycleMin_finance`,
**EXACT — LEAN VERIFIED**) with a genuinely new consequence
(wholesale cycle-length exclusion: Lean leftover \(84\) with
\(m\ge 3\) or \(\ge 85\), Eliahou leftover \(84\) or a listed
near-convergent or \(\ge 10^5\), computational prefix
\(\le1053\)) and a clear literature distinction: the Simons–de
Weger financing-versus-gap template transferred to a floor-power
map where defects are relatively \(O(1/x)\) in logarithms. Not a
totality result; the escape half is untouched.
