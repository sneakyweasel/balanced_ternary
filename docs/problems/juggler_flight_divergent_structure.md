# Juggler divergent flight structure (pointwise laws from proved layers)

Status: **PROMOTE** (pointwise structure theorem for divergent
flights recorded; exclusion not attempted, all-depth frontier not
touched)

The anchor-period branch's standing question: is there any statement
about *unbounded-state* (divergent) flights from the proved layers —
e.g. a minimum divergence rate — or is that frontier fully behind
all-depth equidistribution? Answer: the proved layers say a lot,
pointwise. Determinism plus the Lean upper envelope force every
divergent flight to diverge pointwise (not just in \(\limsup\)),
with a linear peak-growth law, a log-log lower rate for the
running-max walk, pointwise walk divergence, and recurrent hug
domination from infinitely many internal anchors. What stays behind
all-depth equidistribution is *exclusion* of divergent flights, not
their description. Not a halt theorem, not an exclusion claim, and
not a reopen of the PARKed re-anchored excursion envelope.

## Problem

By the flight dichotomy (`J-flight-walk-divergence`), a descent-free
flight from anchor \(n\) (necessarily \(n>162\,849\,448\)) is either
eventually periodic — the cycle program's jurisdiction, with the
conditional anchor-period ladder on top — or divergent
(\(\limsup_k x_k=\infty\)). The bounded case is fully described.
What do the proved layers say about the divergent case?

## Exact statement

**Theorem (divergent flight structure; EXACT — HUMAN PROOF,
components Lean).** Let \(x_0=n\ge 2\), \(x_{k+1}=T(x_k)\), be a
descent-free flight (\(x_k\ge n\) for all \(k\)) that is *not*
eventually periodic. Then:

1. **Injectivity and pointwise divergence.** All states are
   distinct, \(x_0=n\) is the global minimum, and
   \(x_k\to\infty\) pointwise (not just \(\limsup\)).

   *Proof.* A repeat \(x_i=x_j\) (\(i<j\)) forces eventual
   periodicity by determinism. Distinct integers \(\ge n\) visit
   every bounded set at most finitely often. Descent-freeness makes
   \(x_0\) the minimum. \(\square\)

2. **Linear peak growth.** \(\max_{j\le k}x_j\ge n+k\) for every
   \(k\) (the \(k+1\) states are distinct integers \(\ge n\)).

3. **Pointwise walk divergence with a log-log rate.** The exponent
   walk \(u_k=a_k\log_2 3-k\) satisfies
   \[u_k\;\ge\;\log_2\!\frac{\log x_k}{\log n}\;\longrightarrow\;\infty,\]
   by the anchor-free upper envelope \(\log x_k\le 2^{u_k}\log n\)
   (Lean `follows_log_le_walkWeight` / `power_bound_word`) and 1.
   With 2,
   \[\sup_{j\le k}u_j\;\ge\;\log_2\!\frac{\log(n+k)}{\log n}:\]
   the running-max walk grows at least like \(\log_2\log k\). This
   strengthens walk-divergence (\(\sup_k u_k=\infty\)) to a
   *pointwise* limit with a rate, in the divergent case.

4. **Hug-excess divergence.** \(a_k-\mathrm{hugOdds}(k)\to\infty\)
   pointwise (from 3 and the hug band
   \(u^{\mathrm{hug}}_k<\log_2 3\), Lean `hugOdds_pow_lt`).

5. **Recurrent hug domination.** There are infinitely many cofinal
   record indices \(i\) (tail minima: \(x_i\le x_j\) for all
   \(j\ge i\)) from which the tail is itself a descent-free flight
   with anchor \(x_i\); tail minima are attained because
   \(x_k\to\infty\), and they strictly increase by distinctness. At
   every record the tail satisfies hug domination
   (Lean `aboveAnchor_prefix_odds_ge_hug`) and inherits 1–4 with
   anchor \(x_i\). The word of a divergent flight is *recurrently
   hug-dominated*: the density constraint
   \(a\ge\mathrm{hugOdds}\) restarts from infinitely many positions,
   not only from \(0\). \(\square\)

**Sharpness.** The log-log rate in 3 is exactly attained at peaks of
realized ascents (envelope sharpness, `J-flight-envelope-transport`):
at every high-flyer peak the probe measures
\(u=\log_2(\log x/\log n)\) to the last float digit. No faster
pointwise lower rate follows from the proved layers: a flight may
hug from each record for arbitrarily long stretches without
contradiction, so slow (e.g. polylog-in-\(k\)) state growth is not
excluded here.

**Scope guard.** No exclusion of divergent flights is claimed or
attempted — that is the all-depth equidistribution frontier
(`J-equidistribution-implies-density-one`). The eventually-all-odd
subcase (an infinite odd tower, parity of iterated
\(\lfloor x^{3/2}\rfloor\) odd forever) is *not* ruled out: the
census observation "A odd starts not an odd tower" is finite data,
not a theorem. No upper growth rate beyond the envelope is claimed.
The quantitative composition of envelopes across valleys stays
PARKed with the flight-envelope branch (this theorem's point 5 is
qualitative recurrence, not envelope composition).

## Current literature

- Flight walk-divergence and the dichotomy — **EXACT — HUMAN
  PROOF** (`J-flight-walk-divergence`); walk-height law **EXACT —
  LEAN VERIFIED** (`J-flight-height-law`)
- Anchor-free upper envelope — **EXACT — LEAN VERIFIED**
  (`power_bound_word`, `follows_log_le_walkWeight`)
- Above-anchor hug domination — **EXACT — LEAN VERIFIED**
  (`aboveAnchor_prefix_odds_ge_hug`, `aboveAnchor_prefix_pow_le`)
- Hug band — **EXACT — LEAN VERIFIED** (`hugOdds_pow_ge`,
  `hugOdds_pow_lt`)
- Anchor-period ladder for the bounded case — conditional,
  `juggler_flight_anchor_period` (PROMOTE)
- Re-anchored excursion envelope (quantitative valley composition)
  — **PARK** (flight-envelope branch reopening key; untouched here)
- Odd-tower non-existence — **OBSERVATION** only
  (`juggler_excursions` census); open as a theorem

Project relationship: **extended** (answers the anchor-period
branch's best next question; completes the descriptive side of the
flight program).

## Branch budget

```text
Mathematical target    what do the proved layers say pointwise about
                       divergent descent-free flights?
Novelty hypothesis     injectivity + Lean envelope force pointwise
                       laws: x_k → ∞, u_k → ∞ with a log-log rate,
                       linear peak growth, recurrent hug domination
Falsifier              everything is a restatement of sup-form
                       walk-divergence (REPARAMETERIZATION → CLOSE)
Existing machinery     follows_log_le_walkWeight,
                       aboveAnchor_prefix_odds_ge_hug, hug band,
                       walk-divergence dichotomy, determinism
Maximum Phase-0 scope  prose theorem + light wiring probe
                       (all-anchor hug census, envelope mirror at
                       peaks); dossier, ledger, journal; no
                       exclusion attempt, no envelope composition,
                       no new Lean
Promotion criterion    a pointwise structure theorem with at least
                       one genuinely new rate or recurrence law
Stop criterion         nothing beyond recorded sup-statements
```

## Balanced-ternary formulation

None required. The statement lives on the exponent lattice and the
integer orbit.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Orbit injectivity on non-periodic flights (determinism) —
  **EXACT — HUMAN PROOF** (one line; drives 1 and 2)
- Pointwise envelope inversion \(u_k\ge\log_2(\log x_k/\log n)\) —
  **EXACT — LEAN VERIFIED** component + trivial inversion
- Tail-minimum records as internal anchors — **EXACT — HUMAN
  PROOF** (attainment from \(x_k\to\infty\); strict increase from
  distinctness)
- Recurrent hug domination — **EXACT — HUMAN PROOF** (records +
  Lean hug domination)
- Any pointwise lower rate for \(x_k\) itself (not peaks, not the
  running max) — not provable from these layers; not claimed

## Experiments

- Probe: `research.juggler_sequence.flight_divergent_structure`
- Artifact:
  `data/research/juggler/flight_divergent_structure/summary.json`
- Tests:
  `tests/research/juggler_sequence/test_flight_divergent_structure.py`

No divergent flight is known (none exists below the certified
floor), so the probe verifies the finite-word mirrors on realized
orbits, at *every* anchor rather than only at the start: for each
index \(i\) of each orbit (\(n\le 2000\)), the segment until the
first dip below \(x_i\) satisfies hug domination in every prefix and
the envelope inequality \(u\ge\log_2(\log x/\log x_i)\) at every
position. Result: \(21\,341\) anchored segments (max length
\(69\)), zero hug violations, zero envelope violations. Rate table
on the seven canonical high-flyers: the log-log bound is *exactly*
tight at every peak (slack \(0.0\) at peaks of \(3.2\cdot 10^6\) to
\(6.5\cdot 10^6\) bits).

## Conjectures

None active. The open exclusion questions already have named homes
(all-depth equidistribution; odd towers noted above as open, no new
record needed for a question this branch does not attack).

## Counterexamples

None. Negative knowledge honored: the ambient-to-orbit transfer
refutation was not re-tested; the PARKed excursion-envelope
composition was not reopened.

## Formalization

All quantitative components are Lean
(`follows_log_le_walkWeight`, `power_bound_word`,
`aboveAnchor_prefix_odds_ge_hug`, `aboveAnchor_prefix_pow_le`,
`hugOdds_pow_ge`, `hugOdds_pow_lt`). The human glue is the
infinite-orbit framing (injectivity, attainment of tail minima,
cofinality of records) — the same idiom boundary as
`J-flight-walk-divergence`; no new Lean file is needed for the
claim tag.

## Results

Classification **DIVERGENT_STRUCTURE_MIRRORS_CONFIRMED**.

- **Theorem:** divergent descent-free flights diverge pointwise
  with all states distinct; peaks grow at least linearly
  (\(\max_{j\le k}x_j\ge n+k\)); the walk diverges pointwise with
  \(u_k\ge\log_2(\log x_k/\log n)\) and running max
  \(\ge\log_2(\log(n+k)/\log n)\); the hug excess diverges; and hug
  domination restarts from infinitely many cofinal record indices.
- **Answer to the standing question:** the proved layers *do*
  describe divergent flights — with rates. Only their exclusion is
  behind all-depth equidistribution.
- **Sharpness:** the log-log walk rate is attained with equality at
  realized peaks (probe slack \(0.0\) on all seven high-flyers);
  no faster pointwise rate follows from these layers.
- Probe: all-anchor mirrors exact on \(21\,341\) segments, zero
  violations; Lean components wired.

## Open questions

- The eventually-all-odd subcase (infinite odd towers) is the
  cleanest named fragment of the divergent frontier: excluding it
  needs parity of iterated \(\lfloor x^{3/2}\rfloor\) at *all*
  depths for a single pattern — strictly weaker than full all-depth
  equidistribution, but still beyond Paper B's depth \(\le 4\).
- Whether recurrent hug domination (point 5) has any Diophantine
  consequence for the *word* of a divergent flight (a
  translation-recurrent density constraint is unusual) — no route
  visible from current layers.

## Decision

**PROMOTE.** The standing question is answered by an exact pointwise
structure theorem with a new rate (log-log running-max walk), a new
recurrence law (hug domination from every tail-minimum record), and
a sharpness certificate. With this, the flight program's descriptive
arc is complete: envelope (Lean), dichotomy, anchor-period ladder
for the bounded case, pointwise structure for the divergent case.
Ledger row `J-flight-divergent-structure`. Branch ends here; the
frontier returns to the two named programs (cycle Diophantine
blocker; all-depth equidistribution). Neither is auto-opened.

## Publication assessment

Below publication threshold on its own; candidate for a short
"divergent case" remark in any future flight-program write-up,
alongside the walk-divergence dichotomy. No Paper A/B edit.
