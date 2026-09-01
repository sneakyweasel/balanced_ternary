# Juggler record composition (widths compose, constraints do not multiply)

Status: **CLOSE** (composition is a reparameterization of the
per-segment quantization law; the one real gain — re-anchored
widths, unbounded rigidity range — is recorded as a
REPARAMETERIZATION ledger row)

The quantization branch's standing question: does the jump-rigidity
law compose across consecutive record segments (sums of near-lattice
jumps against total walk growth) into any constraint with
Diophantine content beyond the envelope, or is composition a pure
reparameterization? Answer: a reparameterization, for a structural
reason worth recording — the lattice \(\Lambda=\{o\log_2 3-p\}\) is
closed under addition, so composed constraints are the same law at
wide record pairs; only the *width* improves. Not a halt theorem,
not a new pricing mechanism, and not a reopen of the PARKed
terminating-side (valley-crossing) envelope composition.

## Problem

`J-flight-return-quantization` pins each record segment of a
divergent flight: \(\delta\le o\log_2 3-p\le\delta+\Delta'\). Does
summing this along consecutive record segments produce new
arithmetic (constraints on the jump *sequence*), or only a
restatement?

## Exact statement

**Composed law (REPARAMETERIZATION of
`J-flight-return-quantization`).** For records \(j<J\) of a
divergent descent-free flight with anchors
\(m_j<m_{j+1}<\dots<m_J\), segment data \((p_k,o_k,\delta_k)\), and
totals \(P=\sum p_k\), \(O=\sum o_k\),
\(U=\log_2(\log m_J/\log m_j)=\sum\delta_k\):

\[U\;\le\;O\log_2 3-P\;\le\;U+\sum_{k}\Delta'_k .\]

*Proof.* Sum the per-segment inequalities; the jumps telescope
exactly. \(\square\)

**Why this is a reparameterization.** \((i_j,i_J)\) is itself an
anchor–position pair covered by the per-pair law ("any later
position"), and \(O\log_2 3-P\in\Lambda\) because \(\Lambda\) is an
additive monoid: composition cannot create a new constraint type.
The composed statement is the existing law at the wide pair.

**What composition does add (width only).** The re-anchored width
never exceeds the direct one:
\(\sum_k-\log_2(1-x_k)=-\log_2\prod_k(1-x_k)\le-\log_2(1-\sum_kx_k)\)
with \(x_k=\Delta_k/\ln m_{k-1}\), and every intermediate anchor
exceeds \(m_j\), so \(\sum_k\Delta'_k\le\Delta'_{\mathrm{direct}}\).
Consequently, on flights whose record spacings stay below each
segment's vacuity window (\(p_k\ll m_{k-1}\ln m_{k-1}\), deficits
summable), the quantization holds with *bounded width at all
distances* — past the direct law's hard cutoff at
\(0.63\,m_j\ln m_j\). Uniform-range arithmetic rigidity, but implied
by finitely many applications of the existing row.

**Scope guard.** No claim that divergent flights exist, that record
deficits are summable on any flight, or that any flight class is
excluded. The terminating-side composition across valleys (the
flight-envelope branch's remaining height-law PARK) involves defect
descents and is not an exclusion lemma: the occupancy reading is
CLOSE (`juggler_flight_valley_composition`). The divergent side
composes cleanly only because records give descent-free tails for
free (`J-flight-divergent-structure`, point 5).

## Current literature

- Per-segment quantization — **EXACT — HUMAN PROOF**
  (`J-flight-return-quantization`), components Lean
- Recurrent hug domination at records — **EXACT — HUMAN PROOF**
  (`J-flight-divergent-structure`)
- Re-anchored excursion envelope across valleys — exclusion
  reading **CLOSE** (`juggler_flight_valley_composition`);
  height-law PARK stays with the flight-envelope branch

Project relationship: **extended** (closes the composition question
raised by the quantization branch).

## Branch budget

- **Target:** does summing the jump-quantization law across record
  segments yield Diophantine content beyond the per-segment law?
- **Novelty hypothesis:** re-anchored budgets extend the rigidity
  window unboundedly; possibly an all-time word-height
  identification.
- **Falsifier:** the composed inequality is implied by finitely
  many applications of the per-segment row (pure
  REPARAMETERIZATION).
- **Existing machinery:** `J-flight-return-quantization`,
  `J-flight-divergent-structure`, two-sided transport (Lean).
- **Maximum Phase-0 scope:** analysis only; dossier, ledger row,
  journal; no probe, no Lean, no reopening of the PARKed
  valley-crossing composition.
- **Promotion criterion:** a composed constraint not implied by
  finitely many per-segment applications, or new arithmetic
  rigidity at composed scale.
- **Stop criterion:** composition = telescoping → CLOSE.

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Composed law with re-anchored width — **REPARAMETERIZATION**
  (recorded; the width comparison
  \(\sum\Delta'_k\le\Delta'_{\mathrm{direct}}\) is exact)
- "Quantization dissolves under summation" — **false** (near-miss
  during analysis, worth recording): \(\Lambda\) is an additive
  monoid, so sums of near-lattice jumps are near-lattice; the
  arithmetic rigidity of the per-segment law is already the
  wide-pair rigidity
- Constraints on the jump *sequence* beyond totals — none: the
  state side (ratios of logs of integers) realizes any lattice
  window at achievable resolutions (\(\sim 10^{-9}\) spacing at
  frontier anchors, far below \(\Delta'\)), so no additional
  tension exists between consecutive jumps

## Experiments

None. The composed law's computational content is the per-segment
mirror already verified by
`tests/research/juggler_sequence/test_flight_return_quantization.py`
(20136 positions, zero violations); summation adds nothing testable.

## Conjectures

None opened.

## Counterexamples

None. The falsifier fired as an implication, not as a tested
refutation.

## Formalization

None new. The composed inequality is a finite sum of the Lean-backed
per-segment inequalities.

## Results

- Composed law recorded (REPARAMETERIZATION,
  `J-flight-record-composition`): same lattice constraint at wide
  record pairs, width improved from \(\Delta'_{\mathrm{direct}}\) to
  \(\sum\Delta'_k\), rigidity range unbounded on deficit-summable
  flights.
- Structural insight: the lattice is an additive monoid, so
  composition can sharpen widths but cannot multiply constraints —
  the per-segment quantization is the maximal Diophantine statement
  at record scale.
- The jump sequence carries no constraint beyond its totals at
  achievable state resolutions.

## Open questions

- None specific to composition. The flight program's descriptive
  arc (envelope, dichotomy, anchor-period, divergent structure,
  quantization, composition) is terminal: further flight-side
  progress requires either the cycle program's Diophantine frontier
  or the all-depth equidistribution program.

## Decision

**CLOSE.** The composed statement is implied by finitely many
applications of the existing row — exactly the branch's falsifier —
and the one real gain (re-anchored widths) is recorded as a
REPARAMETERIZATION ledger row to prevent re-derivation. The flight
program is hereby terminal on the descriptive side. Best next
question: should the flight arc (walk-divergence dichotomy,
anchor-period ladder, divergent structure, return quantization) be
consolidated into a laboratory note — a flight-side companion to
Paper A's cycle sections — now that the arc is closed, and if so,
which results meet the note's bar?

## Publication assessment

Status: `EXPLORATORY`. A closure record; the composed width remark
would appear, if anywhere, inside a future flight-program note, not
alone.
