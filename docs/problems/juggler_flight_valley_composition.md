# Juggler flight valley composition (occupancy, not height)

Status: **CLOSE** (the named exclusion reading is answered: comparable-scale
occupancy is the existing pigeonhole or hug-hugging; terminating-side
re-anchor cannot exclude a descent-free flight; the packing reduction
was a conservative deferral, not a remaining attack)

The uniqueness/packing pass's standing deferral: a genuine sparsity
contradiction on the divergent branch would need envelope windows at
comparable scales to be over-occupied, and that slogan was pointed at
the flight-envelope PARK (re-anchored excursion envelope) without
opening it. Answer: the occupancy inequality splits into four existing
statements and supplies no exclusion. Not a halt theorem, not a
divergent-orbit exclusion, not a reopen of the \(19.6\%\)
terminating-side height-law PARK, and not a Paper A edit.

## Problem

The flight program describes divergent descent-free flights
(injectivity, pointwise divergence, log-log walk rate, recurrent hug
domination, return quantization) and does not exclude them. State
packing — uniqueness plus recurrent hug plus the envelope making
\([n,\infty)\) too thin for an infinite injective trajectory — was
PARK'd and reduced to "quantitative valley composition." Does that
PARK supply a comparable-scale occupancy law that kills an infinite
injective `AboveAnchor` trajectory, or is every such inequality
already recorded?

## Exact statement

**Theorem (valley-composition split; EXACT — HUMAN PROOF, components
Lean).** The PARKed re-anchored excursion envelope does not supply a
comparable-scale occupancy inequality that excludes divergent
flights. The slogan splits as follows.

**(Occupancy inequality.)** Let \(x_0=n\ge 2\), \(x_{k+1}=T(x_k)\) be
a descent-free flight that is not eventually periodic. From any
internal record \(m\) (a tail minimum; `J-flight-divergent-structure`,
point 5) the tail is itself `AboveAnchor`, so the two-sided envelope
(`aboveAnchor_flight_envelope`) places each later state in a window

\[
W_k=\bigl[m^{w_k(1-\Delta_k/\log m)},\,m^{w_k}\bigr],
\qquad
\Delta_k=\frac{1.05\,e_k}{m}+\frac{0.7\,o_k}{m\sqrt m}.
\]

If a finite index set \(K\) has \(\bigcup_{k\in K}W_k\subset S\) for
some \(S\subset\mathbb Z\), injectivity forces \(\lvert K\rvert\le
\lvert S\rvert\). A comparable-scale occupancy *kill* is a choice of
\(K\) with \(S\) sitting in a band of bounded relative width (one
record scale, or two records with \(m'/m\) bounded) and
\(\lvert K\rvert>\lvert S\rvert\).

Pointwise divergence already implies every *fixed* bounded \(S\) is
occupied only finitely often (`J-flight-divergent-structure`, point
1). So the only possible kill is a finite sojourn longer than
\(\lvert S\rvert\). Those sojourns classify as follows.

**(1. Bounded-walk sojourn — REPARAMETERIZATION of
`J-flight-walk-divergence`.)** If the walk stays \(\le B\) for \(N\)
steps from record \(m\), then
\(S\subset[m,m^{2^B}]\) by `power_bound_word` /
`follows_log_le_walkWeight`. The inequality \(N\le\lvert S\rvert\) is
the existing pigeonhole, re-anchored: the tail is `AboveAnchor`, and a
sojourn longer than the window is eventually periodic, hence the
whole flight is. This kills bounded-walk stretches. It does not kill
divergent flights, which have unbounded walk.

**(2. Equal-\(w\) thin slices — already cycle-exclusive.)** Near
\(w=1\) the integer width of \(W_k\) is \(O(k)\):
\(\lvert W_k\rvert\approx m^w\cdot w\Delta_k\), and \(\Delta_k=O(k/m)\).
Many consecutive steps sharing nearly the same walk weight is
hug-hugging. Unbounded hug-hugging is already cycle-exclusive
(`J-flight-walk-divergence`). Finite hug after a record is *allowed*:
the structure theorem's sharpness says a flight may hug from each
record for arbitrarily long stretches without contradiction, so slow
(e.g. polylog-in-\(k\)) state growth is not excluded. A hug-band
sojourn (\(B\sim\log_2 3\), states in \([m,m^3)\)) at the frontier
anchor \(m\ge 3.5\cdot 10^8\) would need more than \(m^3\sim
4\cdot 10^{25}\) steps to overfill — not a laboratory kill, and not
an infinite-orbit contradiction because the flight is allowed to
leave.

**(3. Record-scale composition — REPARAMETERIZATION of
`J-flight-record-composition`.)** Records strictly increase, so later
valleys draw from a fresh half-line rather than a shared finite pool.
Later high-walk peaks occupy larger scales (`J-flight-height-law`).
Composing two comparable-scale sojourns *enlarges* \(S\) (a union of
windows), it does not shrink it; occupancy cannot accumulate across
increasing records. Jump-width composition is already the per-pair
quantization law at a wide record pair (the lattice
\(\{o\log_2 3-p\}\) is an additive monoid). Hug cylinders are filled
at the \(2^{-L}\) scale (`juggler_hug_prefix_realization`, CLOSE):
hug domination constrains words, not a thin static subset of
\(\mathbb Z\).

**(4. Terminating-side re-anchor — different object.)** After a first
descent \(x_k<n\), the original `AboveAnchor` lower bound dies.
Re-anchoring at a valley \(v<n\) restores a two-sided price for a
later peak. That is the flight-envelope PARK: \(1964/9999\) odd
starts through \(2\cdot 10^4\) peak after first descent, and the
question is whether composed per-excursion envelopes yield a
whole-trajectory *height* law. A descent-free flight never has
\(x_k<n\). The height-law PARK is not an exclusion lemma and is not
opened here.

So the packing reduction to "quantitative valley composition" was a
conservative deferral. The exclusion reading is a false reopen: every
occupancy inequality is (1)–(3), and (4) is a different object. No
mechanism for excluding divergent flights is supplied.

No cycle of any length, and no exclusion of divergent flights, is
claimed.

## Current literature

- Flight envelope (two-sided transport on `AboveAnchor`) —
  **EXACT — LEAN VERIFIED** (`J-flight-envelope-transport`,
  `aboveAnchor_flight_envelope`)
- Walk-height law — **EXACT — LEAN VERIFIED** (`J-flight-height-law`)
- Walk-divergence and the dichotomy — **EXACT — HUMAN PROOF**
  (`J-flight-walk-divergence`); the pigeonhole is uniqueness on a
  finite envelope window
- Divergent structure (pointwise laws, recurrent records, sharpness)
  — **EXACT — HUMAN PROOF** (`J-flight-divergent-structure`)
- Record composition — **REPARAMETERIZATION**
  (`J-flight-record-composition`); widths compose, constraints do
  not multiply
- Hug-cylinder fills at the \(2^{-L}\) scale — **CLOSE**
  (`juggler_hug_prefix_realization`)
- Uniqueness trichotomy / packing PARK — journal consolidation
  2026-09-01; no conjecture id (no precise packing conjecture was
  stated)
- Flight DK split — **CLOSE** (`juggler_flight_dk_pricing`); pricing
  without closure, kill needs \(x_L=n\); not re-tested
- Cycle peak–valley composition — **CLOSE**
  (`juggler_cycle_peak_valley_composition`); a different object
  (necklace \(P>P\)/\(P<P\)), not this branch
- Terminating-side re-anchored height law — **PARK** (flight-envelope
  branch; untouched as a height question)
- Every start reaches 1 — not claimed

Project relationship: **extended** (answers the packing pass's
named deferral; packages existing Lean/human theorems, no new
mechanism).

## Branch budget

```text
Mathematical target     Does the PARKed re-anchored excursion envelope
                        supply a comparable-scale occupancy inequality
                        that can exclude an infinite injective
                        AboveAnchor trajectory?
Novelty hypothesis      Composed two-sided windows at successive
                        records (or across a peak-valley-peak) stay
                        thin enough, at comparable scales, to beat
                        |window|
Falsifier               every such inequality is the existing
                        bounded-walk pigeonhole, hug-hugging (already
                        cycle-exclusive), or record-composition
                        reparameterization; the original envelope PARK
                        prices post-descent peaks on orbits that leave
                        AboveAnchor and so cannot exclude flights
Existing machinery      J-flight-envelope-transport, J-flight-height-law,
                        J-flight-walk-divergence, J-flight-divergent-structure
                        (sharpness: arbitrary-length hug after a record),
                        J-flight-record-composition,
                        juggler_hug_prefix_realization (CLOSE)
Maximum Phase-0 scope   distill only: dossier, journal, branch-ledger
                        line, packing-paragraph updates; no probe, no
                        Lean, no ledger row, no Paper A, no N0, no
                        atlas expansion, no 19.6% height-law census
Promotion criterion     a composed occupancy law not implied by the
                        existing pigeonhole or record composition
Stop criterion          the split is recorded and the exclusion reading
                        is a reparameterization or a false reopen
```

## Balanced-ternary formulation

None required. The objects are the exponent walk, the envelope
windows, and the integer orbit.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Occupancy inequality \(\lvert K\rvert\le\lvert S\rvert\) on a union
  of envelope windows — **EXACT — HUMAN PROOF** (injectivity +
  `aboveAnchor_flight_envelope`)
- Bounded-walk sojourn pigeonhole — **REPARAMETERIZATION** of
  `J-flight-walk-divergence`
- Equal-\(w\) thin slices / hug-hugging — **EXACT — HUMAN PROOF**
  (existing; cycle-exclusive)
- Record-scale composition of windows — **REPARAMETERIZATION** of
  `J-flight-record-composition` plus `J-flight-height-law`
  (composition enlarges \(S\))
- Terminating-side re-anchor after \(x_k<n\) — **PARK** (envelope
  branch height law; not an exclusion invariant)
- Flight-side occupancy kill of a divergent orbit — not claimed;
  the target of this branch, answered negatively

## Experiments

None. The four-way split is an implication from recorded theorems;
a census of realized (terminating) multi-valley prefixes would
measure the \(19.6\%\) height-law PARK, which is a different object,
and cannot exclude a descent-free flight.

## Conjectures

None new. No packing or valley-composition conjecture is recorded,
because the exclusion mechanism is identified as missing rather
than empirically false.

## Counterexamples

None. Negative knowledge honored: the REFUTED Koksma \(+1/L\) slogan
was not re-tested; hug-cylinder fills were not re-censused; record
composition and the DK split were not re-proved; the \(19.6\%\)
height-law PARK was not implemented.

## Formalization

None new. Consumed Lean:

- `aboveAnchor_flight_envelope`, `aboveAnchor_transport`,
  `follows_log_le_walkWeight`, `aboveAnchor_height_of_walk`
  (`WalkTransport.lean`)
- `power_bound_word`, `cycle_strict_envelope` (`Envelope.lean`)
- `aboveAnchor_prefix_odds_ge_hug`, `aboveAnchor_prefix_pow_le`
  (`AboveAnchorWalk.lean` / `CycleCore.lean`)
- `hugOdds_pow_ge`, `hugOdds_pow_lt` (hug band)

The human glue is the occupancy inequality and the four-way split —
the same infinite-orbit idiom as `J-flight-walk-divergence`.

## Results

Classification **VALLEY_COMPOSITION_EXCLUSION_CLOSED**.

- **Occupancy is the existing pigeonhole.** A finite sojourn whose
  windows sit in \(S\) cannot outrun \(\lvert S\rvert\); if the walk
  is bounded this is `J-flight-walk-divergence` re-anchored at the
  record. Pointwise divergence forbids infinite occupation of any
  fixed bounded \(S\).
- **Thin equal-\(w\) slices are hug-hugging**, already
  cycle-exclusive; long hug after a record is allowed (structure
  theorem sharpness).
- **Composition across records enlarges \(S\)**, it does not shrink
  it. Jump widths are `J-flight-record-composition`.
- **Terminating-side re-anchor is a different object** (orbits that
  leave `AboveAnchor`) and is not an exclusion lemma. That PARK
  stays with the flight-envelope branch as a height question.
- No new period bound, no divergent-orbit exclusion, no ledger row:
  the components are existing theorems. The packing reduction to
  valley composition was a false reopen.

## Open questions

- The terminating-side height law (does re-anchoring at valleys
  after first descent compose into a whole-trajectory \(\Phi\) law
  for the \(19.6\%\) peak-after-descent class?) remains **PARK**
  with [juggler_flight_envelope.md](juggler_flight_envelope.md).
  It is not an exclusion question and is not opened from here.
- No occupancy remainder is visible from the proved layers.
  Searching for a fifth case is a reopen of the pigeonhole.
  Not opened.

## Decision

**CLOSE.** The standing deferral is answered by a split, not by a
new mechanism: comparable-scale occupancy is the walk-divergence
pigeonhole or hug-hugging, record-scale composition cannot
accumulate occupancy, and the original envelope PARK prices
post-descent peaks on orbits that leave `AboveAnchor`. The
statements are existing Lean and human theorems; the last named
flight-side reopen on the divergent branch is therefore not a
theorem and not a PARK. Best next question: none in the flight
program; the two named frontiers (the cycle Diophantine blocker
\(L=478245\); pointwise emptiness of infinite odd towers) are not
opened from here. The terminating-side height-law PARK is a
different question and is not that next question.

## Publication assessment

Status: `EXPLORATORY`. A one-paragraph clarification for the flight
extract §7 (“valley-composition exclusion is the existing
pigeonhole; the height-law PARK is a different object”). Not a
paper candidate. No Paper A/B edit.
