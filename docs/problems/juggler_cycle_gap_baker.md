# Juggler cycle-gap Baker transfer

Status: **ARCHIVED**

Standalone application phase on the Juggler floor-power map, on the
**cycle half** of the `cycles_or_escapes` split. It maps the unused
second half of Simons–de Weger — Rhin / linear forms on
\(\lvert 3^o-2^L\rvert\) — into the already-proved finance inequality.
It is not a halt theorem, not a no-cycle-of-any-length theorem, not a
floor raise, and not the Baker/Thue/Mordell campaign on \(x^3-y^2\)
parked in `odd_sharp_suffix` and `sequential_mordell`.

## Problem

Cycle finance gives

\[
n\log n\le C\cdot L\cdot\frac{3^o}{3^o-2^L}
\]

on a hypothetical cycle minimum. Near-convergent lengths have a tiny
gap, so the right-hand side is large and one verified floor only kills
those lengths one convergent at a time. Does a published
transcendence lower bound on the same gap exclude every leftover
near-convergent at once?

## Exact statement

Write \(\theta=(3^o-2^L)/3^o\) and
\(\Lambda=\lvert L\log 2-o\log 3\rvert\), so \(\theta=1-e^{-\Lambda}\)
whenever \(2^L<3^o\). Finance at a verified floor \(n_0\) forces any
surviving cycle to satisfy \(\theta\le\tfrac65 L/(n_0\log n_0)\).
Rhin, as packaged by Simons–de Weger Lemma 12, gives
\(\Lambda>e^{-13.3(0.46057+\log H)}\) with \(H=\max(L,o)\).

**Dominance (EXACT — HUMAN PROOF).** Any correct lower bound
\(\delta\le 3^o-2^L\) produces a finance \(n_{\max}\) at least as
large as the exact-gap \(n_{\max}\). No gap lower bound can exclude a
length that exact finance keeps at the same floor.

**Squeeze failure (COMPUTATIONALLY VERIFIED).** On the leftover
record lengths \(19,84,569,1054,25781,50508\) the Rhin lower bound
never exceeds the finance upper bound at floors \(53\), \(10^6\), or
\(10^9\). On the dense table \(L\le 2000\), Rhin excludes no leftover
length at those floors.

**Slogan refutation (EXACT — HUMAN PROOF).** The exact gap at the
first leftover near-convergent is \(3^{12}-2^{19}=7153\), so
\(n_{\max}(19)=297>53\). The strongest possible lower bound already
fails at the Lean floor. Along the convergents of \(\log 2/\log 3\),
exact \(n_{\max}\) grows without bound, so no fixed floor plus any
correct gap bound kills every near-convergent.

**Missing Collatz ingredient (EXACT — HUMAN PROOF).**
Simons–de Weger obtain \(\Lambda<C_m\,2^{-c(m)K}\) from \(m\)-cycle
geometry. That exponential-in-\(K\) upper bound is what makes Rhin’s
polynomial lower bound contradictory for large \(K\). Juggler finance
only gives \(\Lambda\le\tfrac65 L/(n\log n)\), which grows in \(L\)
at a fixed floor. The second half does not transfer.

This says nothing about totality.

## Current literature

- Cycle finance inequality —
  **EXACT — LEAN VERIFIED**
  (`cycleMin_finance`,
  [juggler_cycle_finance.md](juggler_cycle_finance.md)).
- Collatz \(m\)-cycle exclusion by financing-versus-gap plus
  Rhin/LMN bounds on \(\lvert 2^L-3^o\rvert\) — **known**
  (`simons-de-weger-2005-collatz-m-cycles`). The first half
  transferred; this branch tests the second half and **refutes**
  the transfer slogan.
- Rhin effective measure for \(x\log 2+y\log 3\) — **known**
  (`rhin-1987-pade-irrationality`); SdW Lemma 12 is the packaged
  form used here.
- Laurent–Mignotte–Nesterenko two-logarithms — **known**
  (`laurent-mignotte-nesterenko-1995-two-logarithms`); SdW records
  that Rhin is sharper for this specific form, so no generic LMN
  constant is instantiated.
- Baker/Thue/Mordell on \(x^3-y^2\) —
  **PARK** / do not start
  ([juggler_odd_sharp_suffix.md](juggler_odd_sharp_suffix.md),
  [juggler_sequential_mordell.md](juggler_sequential_mordell.md)).
  That campaign is a different Diophantine object.

Project relationship: **refuted** as a wholesale killer of
near-convergents; the published bounds themselves remain **known**.

## Branch budget

```text
Mathematical target     Does a published lower bound on |3^o - 2^L|
                        (Rhin / SdW Lemma 12) exclude leftover
                        Juggler near-convergent lengths at floors
                        53, 10^6, or 10^9, or produce a finite
                        period bound as in Collatz m-cycles?
Novelty hypothesis      A transcendence lower bound on the finance
                        gap kills every near-convergent at once,
                        instead of chasing floors one convergent
                        at a time.
Falsifier               Rhin theta never exceeds the finance cap on
                        leftover lengths; the exact gap of L=19
                        already fails at floor 53, so no correct
                        lower bound can do better at that floor.
Existing machinery      cycleMin_finance, exact gap table, floors
                        53 (Lean) and 10^6 (Python), SdW Lemma 12.
Maximum Phase-0 scope   Map Rhin/SdW into finance; compare to the
                        exact gap on records and L<=2000; no Baker
                        solver, no Lean import, no x^3-y^2 code.
Promotion criterion     A published bound excludes a leftover
                        near-convergent at a realistic floor, or
                        the squeeze yields a finite K bound.
Stop criterion          Dominance plus squeeze failure, or the
                        slogan is false because the exact gap of
                        a leftover already survives the floor.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Finance inequality \(n\log n\cdot(3^o-2^L)\le L\cdot 3^o\) —
  **EXACT — LEAN VERIFIED** (`cycleMin_finance`)
- Exact relative gap \(\theta=(3^{o_{\min}}-2^L)/3^{o_{\min}}\) —
  **EXACT — HUMAN PROOF** (integer arithmetic)
- Rhin/SdW lower bound
  \(\Lambda>e^{-13.3(0.46057+\log H)}\) — **KNOWN**
- Dominance of the exact gap over any correct lower bound —
  **EXACT — HUMAN PROOF**
- Rhin excludes a leftover length at floors \(53\), \(10^6\),
  \(10^9\) — **REFUTED**
- “Kill every near-convergent at once” —
  **REFUTED**
  (`juggler_baker_kills_near_convergents`)
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_gap_baker`
- Records: [juggler_cycle_gap_baker.md](../research/juggler_cycle_gap_baker.md),
  [juggler_cycle_gap_baker.json](../research/juggler_cycle_gap_baker.json)
- Dataset: `data/research/juggler/cycle_gap_baker/`
- Tests: `tests/research/juggler_sequence/test_cycle_gap_baker.py`

Science window: exact versus Rhin on \(L\le 2000\) and on the finance
record lengths \(1,3,11,19,84,569,1054,25781,50508\); squeeze at
floors \(53\), \(10^6\), \(10^9\). No CLI. No new Lean. Paper A is
unchanged.

## Conjectures

`juggler_baker_kills_near_convergents` — **REFUTED**.

## Counterexamples

- \(L=19\), \(o=12\): exact gap \(7153\) gives \(n_{\max}=297>53\).
  The strongest possible lower bound fails at the Lean floor.
- Rhin/SdW Lemma 12 never beats the finance cap on any leftover
  record length at floors \(53\), \(10^6\), or \(10^9\).
- Record lengths \(84,569,1054,25781,50508\) have growing exact
  \(n_{\max}\), tracking convergents of \(\log 2/\log 3\).

## Formalization

None. The finance inequality is already in `CycleFinance.lean`.
No `Baker.lean`, no `CycleGapBaker.lean`, no Rhin import, and no
`sorry`. Paper A is unchanged. Not a halt theorem.

## Results

Classification **CYCLE_GAP_BAKER_CLOSED**. Regenerate with
`python -m research.juggler_sequence.cycle_gap_baker`.

- Rhin is strictly weaker than the exact gap on every tested
  length (**COMPUTATIONALLY VERIFIED**). At \(L=19\), Rhin
  \(n_{\max}\) hits the cap \(10^{18}\) against exact \(297\).
- Rhin excludes **zero** leftover lengths on \(L\le 2000\) and
  on the record list, at floors \(53\), \(10^6\), and \(10^9\).
- The Rhin floor that would exclude \(L=19\) is at least
  \(10^{18}\). Exact finance already excludes it at \(298\).
- The Collatz second half uses an exponentially small upper
  bound on \(\Lambda\) that Juggler finance does not supply.

## Open questions

Stop on Baker / linear forms as a wholesale killer of Juggler
near-convergents. Do not import Rhin into Lean. Do not start
the \(x^3-y^2\) campaign. The leftover \(L=19\) remains a floor
question, not a transcendence question.

## Decision

**CLOSE**. The slogan is false: a transcendence lower bound on
\(\lvert 3^o-2^L\rvert\) cannot exclude a length that the exact
gap keeps, and the exact gap of the first leftover near-convergent
already survives the Lean floor. The Collatz squeeze needs an
exponentially small upper bound on \(\Lambda\) that finance does
not give. This is not a halt theorem and not a reason to raise
the floor inside this branch.

Best next question: can the residual floor be raised past \(297\)
so that finance kills \(L=19\)?

## Publication assessment

Status: `ARCHIVED`.

A negative transfer: the unused Simons–de Weger half does not
become a Juggler theorem. The obstruction is exact (dominance
plus the missing exponential upper bound), and the numerical
comparison is finite. Not a paper candidate and not a Juggler
totality result.
