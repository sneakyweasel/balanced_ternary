# Juggler fan successor rigidity

Status: **ARCHIVED** (Phase 0 decided)

Successor of the flight-anchor scan
([juggler_flight_anchor_period.md](juggler_flight_anchor_period.md))
and the fan-minimum reduction
([juggler_cycle_walk_fan_minimum.md](juggler_cycle_walk_fan_minimum.md)).
Asks whether the step \(478245\to 780239\) is an exact
semiconvergent-block theorem, rather than a 301995-length census.
Not a halt theorem, not a floor raise, not a Baker import, not a
\(0.999\,\theta\) weakening, not a Paper A edit, and not a
reopen of the unbounded-partial-quotient question.

## Problem

The flight-anchor branch observed that the only DK survivor in
\([478245,780239]\) at floor \(3.5\cdot 10^8\) is the \(k=2\) fan
member \(780239=176251+2\cdot 301994\). The eleven parity leftovers
look like the Paper A survivor lattice translated by one fan step.
Is that an explicit finite class forced by continued-fraction
classification, and is \(k=2\) a structurally distinct Juggler
object?

## Exact statement

Write \(\theta=1-2^L/3^o\) at \(o=o_{\min}(L)\), and write
\(x=\log 2/\log 3\). The leftover criterion at floor \(n\) is at
most as strong as crude finance
\(\theta\le\tfrac65 L/(n\ln n)\). Legendre’s theorem classifies
\(L\) as a convergent once \(\theta<(\ln 3)/(2L)\); Dirichlet
semiconvergents need \(\theta<(\ln 3)/L\).

**Completeness fails (EXACT — HUMAN PROOF; instance
COMPUTATIONALLY VERIFIED).** At the flight anchor
\(n=3.5\cdot 10^8\),

\[
\frac{\tfrac65 L/(n\ln n)}{(\ln 3)/L}
=
36.28\quad(L=478245),\qquad
96.57\quad(L=780239).
\]

The leftover \(\varepsilon\) is thirty-six to ninety-seven times
too coarse for Dirichlet, and twice that against Legendre. Classical
best-approximation theorems do not list the leftovers. The
301995-length scan remains the completeness proof.

**Cone observation (COMPUTATIONALLY VERIFIED; not a lemma).**
The stored eleven leftovers sit in the nonnegative cone

\[
478245+a\cdot 25781+b\cdot 50508+c\cdot 176251+d\cdot 301994,
\]

with odd counts adding the pairs
\((16266,31867,111202,190537)\). All forty-six cone points in the
interval are \(o\)-minimal. Thirty-five extras are not parity
leftovers. The first extra \(529807=478245+2\cdot 25781\) has
\(\theta\approx 5.45\cdot 10^{-5}\), still below the crude leftover
cap \(8.33\cdot 10^{-5}\) at the blocker — even “cone plus crude
\(\varepsilon\)” is larger than the leftover set.

**Defect product (EXACT — HUMAN PROOF; instance
COMPUTATIONALLY VERIFIED).** On an additive pair,
\(3^{o+o'}/2^{L+L'}=(3^o/2^L)(3^{o'}/2^{L'})\), hence

\[
\theta(L+M)=\theta(L)+\theta(M)-\theta(L)\theta(M).
\]

Recovering generator \(\theta\) from the four one-step stored sums
and predicting the six multi-generator leftovers matches the stored
\(\theta\) to relative error \(<10^{-11}\). Combinations have
\(\theta\sim\theta_*+\theta_{\mathrm{seed}}\gg\theta_*\). The fan
step uses \(p_{13}=190537\), not \(o_{\min}(301994)=190538\), and
carries a tiny negative defect \(\approx -6.45\cdot 10^{-8}\).

**Successor is not a new shape (COMPUTATIONALLY VERIFIED).**
\(\theta(780239)/\theta(478245)=0.9818\); DK margins at the
anchor are \(1.0053\to 0.6048\); digit sums \(2\) and \(3\). The
next admissible fan member is the same dangerous approximation,
one step on, with a worse margin. Hug type stays
\(\mathtt{OE}/\mathtt{OOE}\) (already recorded through \(176251\)).

**Slogan.** The leftovers in \([478245,780239]\) form an explicit
Ostrowski / lattice class forced by classical CF bounds, so
\(k=2\) is forced without a scan and is structurally distinct —
**REFUTED**.

No cycle of any length — not claimed.

## Current literature

- Flight-anchor scan, eleven leftovers, first survivor
  \(780239\) — **COMPUTATIONALLY VERIFIED**
  ([juggler_flight_anchor_period.md](juggler_flight_anchor_period.md))
- Fan-minimum balance law and CF reduction —
  **COMPUTATIONALLY VERIFIED** / **CONJECTURE**
  ([juggler_cycle_walk_fan_minimum.md](juggler_cycle_walk_fan_minimum.md));
  unbounded dangerous partial quotients stay classical **OPEN**;
  no successor is opened here
- Run-survivor lattice — **EXACT — LEAN VERIFIED**
  (`RunSurvivorLattice.lean`; Paper A Proposition 4.9)
- Fan multipoint (two forced approximations) — **REFUTED**
  ([juggler_cycle_fan_multipoint.md](juggler_cycle_fan_multipoint.md))
- Affine \(n\)-gap / \(0.999\,\theta\) — **REFUTED**
  ([juggler_cycle_affine_n_gap.md](juggler_cycle_affine_n_gap.md))
- DK-arch free-kill of \(478245\) — **REFUTED**
  ([juggler_cycle_walk_arch.md](juggler_cycle_walk_arch.md))
- Baker / Rhin leftover-killer — **REFUTED**
  ([juggler_cycle_gap_baker.md](juggler_cycle_gap_baker.md))
- Legendre / Dirichlet best approximations — **KNOWN**
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a completeness lemma and as
a structurally new successor. The scan and the fan-minimum law
remain **known**.

## Branch budget

```text
Mathematical target     At the leftover ε of one fixed floor (flight
                        anchor 3.5e8, already priced), is every parity
                        leftover in [478245, 780239] a member of the
                        explicit cone generated by the leftover seeds,
                        so that k=2 is forced as the unique DK survivor
                        without scanning 301995 lengths?
Novelty hypothesis      Completeness is an Ostrowski / three-gap
                        classification of {L : 1-{L x} small}, not a
                        new DK constant and not the fan-minimum law
Falsifier               A leftover in the stored 11-list lies off the
                        cone; or the leftover ε is too weak for any
                        classical best-approximation theorem to reach
                        (then the scan remains the completeness proof)
Existing machinery      theta_exact / o_min_exact / fan_thetas / dk_price
                        (cycle_walk_competition); greedy_digits
                        (cycle_walk_ostrowski); RunSurvivorLattice;
                        flight_anchor_period summary (11 leftovers,
                        DK margins); fan-minimum R_k (do not reopen)
Maximum Phase-0 scope   One arithmetic probe reading stored artifacts;
                        enumerate the cone; check the exact defect law;
                        attempt one completeness bound; dossier +
                        conjecture + tests + journal. No census, no
                        floor, no Lean, no Paper A edit, no Baker,
                        no 0.999 theta, no schedule rebuild
Promotion criterion     A lemma that the leftovers in the block are
                        among an explicit finite list, plus exact
                        pricing of the combinations — a theorem about
                        the whole k=1 semiconvergent block, not a
                        longer kill table
Stop criterion          Completeness does not reach the leftover ε
                        (CLOSE: scan stays necessary; k=2 is not a
                        new shape); or the statements are all KNOWN /
                        REPARAMETERIZATION of flight-anchor + lattice
                        + fan-minimum
```

Closed doors: Baker / Rhin, DK-arch free-kill, affine \(n\) /
\(0.999\,\theta\), fan multipoint, fan-minimum unbounded-PQ
question, \(N_0\) raise, Paper A, another period census, the
61-level ladder.

## Balanced-ternary formulation

None required. The objects live on the exponent lattice
\((L,o)\) and the continued fraction of \(\log 2/\log 3\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Leftover \(\varepsilon\) versus Dirichlet / Legendre —
  **EXACT — HUMAN PROOF** (the finance-to-\(\lvert x-o/L\rvert\)
  conversion); instance **COMPUTATIONALLY VERIFIED**
- Defect product \(\theta(L+M)=\theta(L)+\theta(M)-\theta(L)\theta(M)\)
  — **EXACT — HUMAN PROOF**; multi-step instances
  **COMPUTATIONALLY VERIFIED**
- Stored leftovers \(\subset\) leftover-seed cone —
  **COMPUTATIONALLY VERIFIED** (observation; 35 extras)
- \(k=2\) structurally distinct — **REFUTED**
- Completeness without a scan — **REFUTED**
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_walk_fan_successor`
- Artifacts: `data/research/juggler/cycle_walk_fan_successor/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_walk_fan_successor.py`

Reads the stored flight-anchor leftovers. Enumerates the cone with
`o_min_exact`. No length census, no floor work, no Lean, no CLI,
no Paper A edit.

## Conjectures

`juggler_fan_successor_rigidity` — **REFUTED**.

## Counterexamples

- At \(n=3.5\cdot 10^8\), leftover/Dirichlet \(=36.28\) at
  \(L=478245\) and \(96.57\) at \(L=780239\); Legendre is twice
  as far
- Cone has 46 \(o\)-minimal points against 11 leftovers; extra
  \(529807=478245+2\cdot 25781\) still beats crude finance
- \(\theta(780239)/\theta(478245)=0.9818\); DK margin drops
  \(1.0053\to 0.6048\)

## Formalization

None. The defect identity is one line of unique factorization
and is not new Lean. `RunSurvivorLattice.lean` already has the
unimodular basis. No `sorry`. Paper A is unchanged.

## Results

Classification **FAN_SUCCESSOR_CLOSED**.

- Completeness: leftover \(\varepsilon\) misses Dirichlet by
  \(36\times\)–\(97\times\)
- Cone contains the stored eleven leftovers and 35 extra
  \(o\)-minimal lattice points
- Defect product predicts the six multi-generator leftovers to
  relative \(<10^{-11}\)
- Fan-step defect \(\approx -6.45\cdot 10^{-8}\)
  (\(p_{13}=190537\), not \(o_{\min}\))
- \(k=2\) is the same \(\theta\)-scale with a worse margin
- No new period bound, no floor, no fan-minimum reopen

## Open questions

None from this formulation. Do not iterate the cone over
\(k=3,\dots,54\) (machinery gravity; the flight dossier already
deferred the 61-level ladder). The cycle frontier remains the
fan-minimum CF reduction. Unconditional kill of \(478245\) still
needs floor \(3.48\cdot 10^8\) (PARK).

## Decision

**CLOSE.** Completeness does not reach the leftover \(\varepsilon\),
so the 301995-length scan remains the only proof that the eleven
leftovers are all the leftovers. The cone observation and the
defect product are reparameterizations of the flight-anchor
census plus the \(r\)-product identity. \(k=2\) is not a new
Juggler shape. The statements that could have been new are
REFUTED or KNOWN.

Best next question: none from this formulation.

## Publication assessment

Status: `ARCHIVED`.

A one-page discharge of successor rigidity. The completeness
gap is exact (finance versus Dirichlet). Not a paper candidate
and not a halt theorem.
