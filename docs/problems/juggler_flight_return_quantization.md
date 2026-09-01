# Juggler record-jump quantization (pricing flights without closure)

Status: **PROMOTE** (quantization theorem recorded; the closure
question is answered on both sides)

The odd-tower branch's standing question: does the recurrent hug
domination of divergent flights admit pricing by the certified
Ostrowski/DK blocks — a flight-side analogue of the walk-charge
envelope — or does DK pricing intrinsically require the closure
identity that only cycles provide? Answer: both halves sharpen.
Recurrent hug domination *alone* prices nothing (the refutation
half), but two-sided transport applied *at record pairs* — where
both endpoint states are known — replaces the closure identity with
the doubly-log jump \(\delta\) as an exact budget, quantizing every
record jump to the \(\log_2 3\)-lattice within the transport
deficit. Cycle pricing is recovered as the \(\delta=0\) boundary
slice. Not a halt theorem, not a divergence exclusion, not a claim
that any divergent flight or near-return exists, and not a DK-layer
extension.

## Problem

By `J-flight-divergent-structure` (point 5), a divergent
descent-free flight has infinitely many cofinal record indices
(tail minima) from which the tail is itself a descent-free flight.
The cycle program prices closed words through the finance identity.
What, if anything, prices these open, translation-recurrent,
hug-dominated words?

## Exact statement

**Theorem (record-jump quantization; EXACT — HUMAN PROOF,
components Lean).** Let \(i\) be a record index of a divergent
descent-free flight, with anchor \(m=x_i\ge 400\). Consider any
later position at distance \(p\), state \(M\), segment odd count
\(o\), and doubly-log jump
\(\delta=\log_2(\log M/\log m)\ge 0\). Then

\[\delta\;\le\;o\log_2 3-p\;\le\;\delta+\Delta',\qquad
\Delta'=-\log_2\!\Big(1-\frac{\Delta}{\ln m}\Big),\]

where \(\Delta\le 1.05\,p/m\) is the Paper A transport deficit of
the segment word.

*Proof.* The tail from a record is descent-free
(`J-flight-divergent-structure`), so its prefixes are
`AboveAnchor`. The anchor-free upper envelope (Lean
`follows_log_le_walkWeight`) gives \(\ln M\le w\ln m\) with
\(w=3^o/2^p\), i.e. \(2^\delta\le w\), the left inequality. The
transport lower bound (Lean `aboveAnchor_transport`, \(m\ge 400\))
gives \(\ln M\ge w(\ln m-\Delta)\), i.e.
\(2^\delta\ge w(1-\Delta/\ln m)\), the right inequality. \(\square\)

**Corollary 1 (jump rigidity).** For a given segment length \(p\),
the admissible jumps \(\delta\) lie in
\(\bigcup_{o\ge o_{\min}(p)}[\,o\log_2 3-p-\Delta',\,o\log_2 3-p\,]\)
— within \(\Delta'\) of a lattice of gap \(\log_2 3\): a measure
fraction \(\Delta'/\log_2 3=O(p/(m\ln m))\) (at the frontier anchor
\(3.5\cdot 10^8\): \(4\cdot 10^{-9}\) at \(p=19\), \(<10^{-3}\)
through \(p=10^6\)). The law is rigid for \(p\ll m\ln m\) and
honestly vacuous past \(p^*\approx 0.63\,m\ln m\)
(\(\approx 7\cdot 10^9\) steps at the frontier anchor).

**Corollary 2 (return-time quantization).** \(\delta\le\varepsilon\)
forces \(\theta_p=o_{\min}(p)\log_2 3-p\le\varepsilon+\Delta'\),
and \(\theta_p\) is exactly the *hug walk height* at \(p\). So
near-returns (in doubly-log scale) happen only at Ostrowski-quantized
times \(R_\varepsilon=\{p:\theta_p\le\varepsilon\}\): the shortest
is \(p=19\) (\(\theta_{19}=12\log_2 3-19=0.01955\)), the gaps of
\(R_\varepsilon\) take at most three values (three-gap theorem,
verified exactly on \(p\le 10^5\) at four \(\varepsilon\) scales),
and as \(\varepsilon\downarrow 0\) the spectrum passes through the
cycle program's survivor lengths (\(84\) at \(\varepsilon=0.005\),
\(1054\) at \(\varepsilon=0.001\)) — the same Diophantine skeleton
as cycle periods, now for open flights.

**Corollary 3 (the closure answer).** Cycle pricing is the
\(\delta=0\) slice: there the budget reduces to the finance deficit
alone and the certified kill tables apply (this is the
anchor-period law's regime). For \(\delta\) beyond deficit scale
the parity/DK tables constrain nothing about \(p\) — the constraint
transfers entirely into the quantization of \(\delta\). So DK/parity
pricing of *lengths* intrinsically requires (near-)closure;
recurrent hug domination alone admits no pricing; and what survives
without closure is the jump-rigidity law, with the jump budget
\(\delta+\Delta'\) exactly replacing the finance identity.

**Scope guard.** No claim that divergent flights, or near-returns on
them, exist. No DK-layer (hug-charge) extension is attempted: the
DK kill of fan survivors needs budgets at deficit scale
(\(\sim 10^{-3}\)), which any \(\delta\) above that scale swamps.
No realizability claims for words.

## Current literature

- Two-sided flight transport — **EXACT — LEAN VERIFIED**
  (`J-flight-envelope-transport`: `aboveAnchor_transport`,
  `follows_log_le_walkWeight`, `WalkTransport.lean`)
- Recurrent hug domination at records — **EXACT — HUMAN PROOF**
  (`J-flight-divergent-structure`, point 5)
- Hug walk height \(\theta_p\) machinery — **EXACT — LEAN
  VERIFIED** components (`hugOdds_pow_ge/lt`); \(o_{\min}\)/\(\theta\)
  tables throughout the cycle program
- Anchor-period law (the \(\delta\approx 0\) conditional regime) —
  `J-flight-anchor-period` (PROMOTE)
- Three-gap (Steinhaus/Slater) structure of rotation return times —
  KNOWN classical; used here as a verified structural check, not as
  a new claim
- Cycle survivor lengths \(84, 1054, 25781,\dots\) — the walk-charge
  and survivor-lattice branches; reappearing here as the
  \(\varepsilon\downarrow 0\) return-time spectrum

Project relationship: **extended** (first quantitative law for the
time structure of divergent flights; unifies the cycle fan and the
flight frontier under one lattice).

## Branch budget

- **Target:** does DK/parity pricing extend from cycles to record
  segments of divergent flights, or does it intrinsically need the
  closure identity?
- **Novelty hypothesis:** transport at record pairs quantizes
  record jumps to the \(\log_2 3\)-lattice within the deficit;
  closure is the \(\delta\approx 0\) slice; near-return times are
  Ostrowski-quantized with shortest time \(19\).
- **Falsifier:** \(\Delta'\ge\) lattice gap on all useful windows
  (vacuous), or the law restates the envelope row with no new
  consequence.
- **Existing machinery:** `aboveAnchor_transport` (Lean), recurrent
  hug domination, `hugOdds` table, \(o_{\min}\)/\(\theta\) machinery.
- **Maximum Phase-0 scope:** one light exact probe
  (\(R_\varepsilon\) sets + three-gap check + all-anchor two-sided
  transport mirror), dossier, ledger row, journal; no new Lean, no
  DK-layer extension, no realizability claims.
- **Promotion criterion:** a quantization law with explicit new
  constants (shortest near-return time, admissible-jump measure).
- **Stop criterion:** \(\Delta'\) analysis shows vacuity → CLOSE.

## Balanced-ternary formulation

None required. The lattice \(\{o\log_2 3-p\}\) lives on the
exponent walk.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Doubly-log jump \(\delta=\log_2(\log M/\log m)\) at record pairs
  — the new coordinate; strictly positive on divergent flights
  (distinct states)
- \(\theta_p=\) hug walk height \(=o_{\min}(p)\log_2 3-p\) —
  **REPARAMETERIZATION** of `hugOdds` (the identification is itself
  useful: near-return times are the near-zeros of the hug walk)
- Jump quantization \(\delta\le o\log_2 3-p\le\delta+\Delta'\) —
  **EXACT — HUMAN PROOF** (components Lean)
- Three-gap structure of \(R_\varepsilon\) — KNOWN classical,
  verified exactly on the probe window
- Any DK hug-charge pricing without near-closure — not claimed
  (shown to have no budget)

## Experiments

- Probe: `research.juggler_sequence.flight_return_quantization`
- Artifact:
  `data/research/juggler/flight_return_quantization/summary.json`
- Tests:
  `tests/research/juggler_sequence/test_flight_return_quantization.py`

Probe contents: exact \(R_\varepsilon\) enumeration on
\(p\le 10^5\) at \(\varepsilon\in\{0.001,0.005,0.02,0.05\}\) (all
three-gap, densities \(0.06\%\)–\(3.2\%\), first elements
\(1054/84/19/19\), float boundary guard \(>10^{-8}\)); rigidity
table at anchors \(3.5\cdot 10^8\) and \(10^{12}\); two-sided
transport mirror at every anchored-segment position (anchor
\(\ge 400\)) of every orbit \(n\le 2000\): \(20136\) positions,
zero violations on either side. Realized near-returns
(\(\delta\le 0.05\)) occur at lengths \(\{19{:}44,\ 38{:}7\}\) —
*only* the two shortest quantized times, with zero quantization
misses.

## Conjectures

None opened. The law is proved; existence of divergent flights or
of near-returns on them is not conjectured.

## Counterexamples

None. The falsifier did not fire: \(\Delta'\) is \(10^{-9}\)-scale
at the frontier anchor and the law adds consequences (return-time
spectrum, jump rigidity) beyond the envelope row.

## Formalization

Both inequalities are Lean (`aboveAnchor_transport`,
`follows_log_le_walkWeight`); the quantization statement is their
one-line combination at record pairs plus the record framing of
`J-flight-divergent-structure` (human, infinite-orbit idiom). No
new Lean file is needed for the claim tag.

## Results

Classification **RETURN_QUANTIZATION_CONFIRMED**.

- **Theorem:** record jumps of divergent flights are quantized to
  the \(\log_2 3\)-lattice within the transport deficit; admissible
  jumps have measure fraction \(O(p/(m\ln m))\).
- **Return-time law:** near-returns only at
  \(R_\varepsilon=\{p:\theta_p\le\varepsilon\}\), shortest \(19\);
  \(\theta_p\) is the hug walk height; the spectrum recovers the
  cycle survivor lengths as \(\varepsilon\downarrow 0\) and has
  three-gap structure at every scale.
- **Closure answer (the branch question):** pricing of segment
  *lengths* requires near-closure (the jump budget replaces the
  finance identity, and DK's charge budgets are swamped beyond
  deficit scale); recurrent hug domination alone prices nothing;
  what is unconditional is the jump-rigidity law.
- **Census mirror:** all realized near-returns land on \(\{19,38\}\)
  — the quantization is visible in real orbits, not only in the
  inequality.

## Open questions

- Whether the jump-rigidity law composes across consecutive record
  segments into a constraint on the *sequence* \((\delta_1,
  \delta_2,\dots)\) (sums of lattice points against total walk
  growth) with any Diophantine content — unexamined; risk of
  reparameterizing the envelope.
- The \(\delta=0\) slice at scale: automating the anchor-period
  ladder remains deferred (recorded there).

## Decision

**PROMOTE.** The branch question is answered exactly on both sides
(what survives without closure, and why length pricing cannot), the
law comes with new constants (shortest near-return \(19\),
admissible-jump measure \(O(p/(m\ln m))\), vacuity window
\(0.63\,m\ln m\)), and the census confirms the spectrum on realized
orbits. Ledger row `J-flight-return-quantization`. Branch ends
here; the composition question is named, not opened.

## Publication assessment

Status: `EXPLORATORY`. Candidate for a "flights" section alongside
the walk-divergence dichotomy in any future flight-program
write-up: the quantization law is the natural open-orbit analogue
of Paper A's finance identity. No Paper A/B edit.
