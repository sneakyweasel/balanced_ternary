# Juggler flight anchor-period law (conditional bounds past the blocker)

Status: **PROMOTE** (instance certified: anchor \(3.5\cdot 10^8\)
forces eventual-cycle period \(\ge 780239\))

Successor of the flight walk-divergence branch
([juggler_flight_walk_divergence.md](juggler_flight_walk_divergence.md)),
answering its best next question: does the dichotomy plus the fan
structure give a flight-side statement at the blocker
\(L=478245\) without a new floor? Not a halt theorem, not a floor
raise (no descent verification is run), not a new *unconditional*
period bound, and not a reopen of the REFUTED uniform
\(B/\theta\) or Baker claims.

## Problem

The walk-charge program's unconditional period bound \(\ge 478245\)
is blocked: killing \(L=478245\) needs floor
\(n^*(478245)=3.48\cdot 10^8\) (DK break-even,
`J-cyclemin-walk-competition-law`), and raising the *certified*
floor there would cost a descent campaign
(\(\sim 1.9\cdot 10^8\) further odd starts); further campaigns are
PARK. The competition branch computed the whole break-even
schedule but flagged every floor beyond \(162849448\) as
"hypothetical — no period bound claimed."

The flight walk-divergence dichotomy changes the accounting: a
bounded-walk descent-free flight from anchor \(n\) enters a
nontrivial cycle whose minimum is \(\ge n\) *by hypothesis*. The
floor is free. Can the hypothetical schedule point at
\(3.48\cdot 10^8\) be upgraded to a conditional theorem about
flights?

## Exact statement

**Anchor-transfer lemma (EXACT — HUMAN PROOF).** Let a
descent-free flight from anchor \(n\) have bounded exponent walk.
By the dichotomy (`J-flight-walk-divergence`) it enters a
nontrivial cycle with minimum \(m\ge n\). Every cycle kill whose
right-hand side is strictly decreasing in the floor persists from
any floor \(\le n\) upward; both the parity finance RHS
(\(\propto o/(n\ln n)+\dots\)) and the DK envelope RHS
(\(\propto (C_*(n')+2s(L)/L)\,L/(n'\ln n')\), \(n'=ne^{-D}\)
increasing in \(n\), \(C_*\) decreasing) are strictly decreasing.
Hence the kill tables evaluated at floor \(n\) apply to the
eventual cycle — no certified descent below \(n\) is needed.

*Uniqueness reading.* Determinism gives a unique preperiod before
the first repetition, and then a closed cycle. Descent-freeness
puts **both** pieces above the anchor: every preperiod state
satisfies \(x_i\ge n\) and \(x_i\neq x_j\) for \(i\neq j<r\), and
the cycle minimum is also \(\ge n\). The cycle cannot slip below
the floor to escape the conditional DK argument. The lemma is
therefore “first repetition \(\Rightarrow\) unique preperiod +
closed cycle, with the flight anchor a floor for both,” not merely
“bounded walk \(\Rightarrow\) some cycle above \(n\).”

**Instance (COMPUTATIONALLY VERIFIED,
`J-flight-anchor-period`).** Any descent-free flight from anchor
\(n\ge 3.5\cdot 10^8\) with bounded exponent walk enters a
nontrivial cycle of period \(\ge 780239=176251+2\cdot 301994\)
(the \(k=2\) fan member). Combined with walk-divergence: every
descent-free flight from \(n\ge 3.5\cdot 10^8\) either has
unbounded states or an eventual cycle of period \(\ge 780239\).

*Certification.* Lengths \(<478245\): killed at the certified
floor \(162849448\) (`J-cycle-period-four-hundred-seventy-eight-thousand`),
persisting upward by the lemma. Lengths in \([478245,780239]\) at
anchor floor \(3.5\cdot 10^8\): all \(301995\) scanned —
\(301883\) parity-killed by a conservative float bound with a
\(10\times\) safety factor (float error on \(\delta\) \(<10^{-9}\)
against decided values \(\ge 10^{-5}\)), \(112\) near-resonant
lengths resolved with exact big-integer \(\theta\)
(\(101\) parity-killed), \(11\) parity survivors priced by the
census-free DK envelope (valid upper bound on the walk charge via
the DK/Ostrowski theorem plus Lean `hug_charge_maximal`). The ten
below \(780239\) all die: blocker \(478245\) margin
\(\mathbf{1.0053}\) (anchor just above its break-even
\(3.48\cdot 10^8\)), the nine near-convergent combinations
(\(504026=478245+25781\), \(654496=478245+176251\), …) at margins
\(1.48\)–\(7.82\). First survivor \(780239\) (margin \(0.6048\),
its own break-even lies higher). All margins monotone up from the
certified floor (numerical mirror of the lemma). Same trust
boundary as Theorem 4.6: exact integer sandwiches plus guarded
float comparisons; deep \(x\)-sandwich certified
(width \(4.31\cdot 10^{-17}\)).

## Current literature

- Flight walk-divergence dichotomy — **EXACT — HUMAN PROOF**
  (`J-flight-walk-divergence`,
  [juggler_flight_walk_divergence.md](juggler_flight_walk_divergence.md))
- DK break-even floors and the 61-level schedule — **COMPUTATIONALLY
  VERIFIED** / **OBSERVATION**
  ([juggler_cycle_walk_competition.md](juggler_cycle_walk_competition.md));
  explicitly "no period bound claimed" — this branch supplies the
  missing hypothesis conditionally
- Certified period bound \(\ge 478245\) at floor \(162849448\) —
  **COMPUTATIONALLY VERIFIED**
  (`J-cycle-period-four-hundred-seventy-eight-thousand`)
- DK/Ostrowski envelope and hug maximality — **EXACT — HUMAN
  PROOF** / **EXACT — LEAN VERIFIED** (`hug_charge_maximal`)
- Parity finance table and guards — **COMPUTATIONALLY VERIFIED**
  (`J-cycle-parity-finance-instance`)
- Further \(N_0\) campaigns — PARK (unchanged; nothing here is a
  floor raise)

Project relationship: **extended** (first conditional period law
whose floor input is the flight's own anchor).

## Branch budget

```text
Mathematical target    does the dichotomy convert the walk-charge
                       schedule into a conditional anchor-period law —
                       concretely: bounded flights from n >= 3.5e8 have
                       eventual-cycle period >= 780239, contiguously?
Novelty hypothesis     the flight's anchor replaces the certified floor:
                       hypothetical schedule points become theorems
                       about flights, with no descent campaign
Falsifier              a non-fan parity leftover in (478245, 780239)
                       survives DK pricing at floor 3.5e8, or the kills
                       fail floor-monotonicity
Existing machinery     flight dichotomy, exact theta/o_min, DK envelope,
                       break-even n*(478245) = 3.48e8, parity table
Maximum Phase-0 scope  one probe (contiguous scan + DK pricing at one
                       anchor), dossier, ledger, journal; no floor
                       raise, no Lean, no Paper A edit, no schedule
                       rebuild at higher levels
Promotion criterion    contiguous conditional bound past the blocker
Stop criterion         a surviving non-fan leftover below 780239, or
                       the statement degenerates to the schedule restated
```

## Balanced-ternary formulation

None required. The law lives on the exponent lattice and the
convergents of \(\log 2/\log 3\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Anchor-transfer lemma (min \(\ge\) anchor, RHS monotone in the
  floor) — **EXACT — HUMAN PROOF** (this dossier)
- Conservative float prefilter \(\theta\ge 1-2^{-(\delta-\epsilon)}\)
  with \(10\times\) safety — sound against the exact resolution of
  every near-resonant length — **COMPUTATIONALLY VERIFIED**
- Census-free DK pricing of parity survivors — reused
  (`cycle_walk_competition.dk_price`)
- The general anchor-period law \(P(n)\) along all 61 schedule
  levels — **not claimed** (contiguity verified at this instance
  only; higher levels stay rows-only in the competition branch)
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.flight_anchor_period`
  (runtime \(\approx 4.5\) min: \(301995\) lengths, \(112\) exact
  \(\theta\), \(11\) DK prices)
- Artifact: `data/research/juggler/flight_anchor_period/summary.json`
- Tests: `tests/research/juggler_sequence/test_flight_anchor_period.py`

## Conjectures

None new. The competition conjecture
(`juggler_walk_finance_competition`) is unchanged; this branch
consumes its certified rows and adds the missing contiguity at one
anchor.

## Counterexamples

None. The predicted falsifier (a surviving non-fan leftover below
\(780239\)) did not fire: all nine intermediate near-convergent
combinations die with margins \(\ge 1.48\).

## Formalization

None new. The kill evaluations are guarded float comparisons on
exact integer sandwiches (the Theorem 4.6 trust boundary); the
Lean components consumed are `hug_charge_maximal` (DK dominates
the walk DP) and the walk-divergence components already recorded.
Certified rational kill tables remain PARKed
(certificate-size obstruction, see
[juggler_cycle_walk_charge.md](juggler_cycle_walk_charge.md)).

## Results

Classification **ANCHOR_PERIOD_GREEN**.

- **Instance:** bounded-walk descent-free flights from
  \(n\ge 3.5\cdot 10^8\) enter cycles of period \(\ge 780239\) —
  a \(1.63\times\) conditional extension past the unconditional
  \(478245\), with zero descent verification. The uniqueness
  reading: the anchor floors both the injective preperiod and the
  closed cycle; the cycle cannot return below \(n\).
- **Structure:** the parity leftovers in \((478245,780239)\) are
  exactly the near-convergent combinations
  \(478245+\{25781,50508(\pm 1054\text{-offsets}),176251,\dots\}\);
  all die under DK at the anchor. The next blocker is the \(k=2\)
  fan member \(780239\) itself (margin \(0.6048\); its break-even
  is the next schedule point).
- **Monotonicity mirror:** every DK margin increased from floor
  \(162849448\) to the anchor, as the formulas require.
- The anchor-period law turns the competition branch's 61-level
  hypothetical schedule into a ladder of *conditional* statements;
  each level needs its own contiguity scan (only this instance is
  certified here).

## Open questions

- Automating the contiguity scan along the remaining schedule
  levels (fan \(k=3,\dots\), seeds \(16785921\), \(85137581\))
  would give the full conditional ladder up to period
  \(\sim 10^8\) at anchor \(2.64\cdot 10^{13}\); each level is a
  \(\sim\)minutes-scale arithmetic scan. Deferred — no new
  mathematical mechanism, machinery gravity applies.
- The mid-fan minimum of required improvement (\(1.0735\)) is the
  competition branch's open question, unchanged.

## Decision

**PROMOTE.** The promotion criterion is met: a contiguous
conditional period bound past the blocker, powered by the
dichotomy plus floor-monotonicity, with the predicted falsifier
tested and dead. Ledger row `J-flight-anchor-period`. The ladder
automation is named and deferred; the divergent-orbit case and
the unconditional frontier are untouched.

## Publication assessment

A short section for Paper A's successor alongside the dichotomy:
"conditional period laws with the flight anchor as floor" — the
first bridge from the cycle program to the termination frontier
that consumes hypothetical floors without certifying them. Tags:
instance COMPUTATIONALLY VERIFIED, lemma EXACT — HUMAN PROOF.
