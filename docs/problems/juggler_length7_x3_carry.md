# Juggler length-7 X3 / Q/R3 carry

Status: **PARK**. Theorem X and density \(57/64\) stay
**CONJECTURE**. The slogan that Lemma X3 plus the
Theorem Q / R3 carry closes \(e(uw^{3/2})\) is
**REFUTED**. Paper B stays frozen at \(13/16\).

Phase-37 desk classification of the actual \(\theta_p\)
inventory sum. Child of
[juggler_engine_harvest.md](juggler_engine_harvest.md).
Not a \(K_3\) attack and not a Paper B edit.

## Problem

Phase 35 closed the isolated monomials
\(e(un^{27/16})\) and \(e(Cn^{3/2})\). The inventory
object is \(e(uw^{3/2})\). On Lemma X3 runs,
\(w=w_0+Jt+\kappa_w\). Does the existing Q/R3 carry
pattern absorb \(\kappa_w\) and close the sum inside
\(P^{23/24}\) without a new decoration class?

## Exact statement

For odd \(n\sim P\), \(1\le\lvert k\rvert\le P^{1/24}\),
and \(\lvert u\rvert\le P^{85/96}\), does
\(\lvert\sum e(u w^{3/2})\rvert\ll P^{23/24}\) follow
from Lemma X3 plus Theorem Q / Lemma R3 / Theorem C
carry bookkeeping, using only the existing classes
(D1), (D3), Stage 2, and Lemma X5?

## Current literature

- Lemma X3 (`w_gap_freeze_scan`) — **EXACT — HUMAN
  PROOF**. Freezes \(J=\lfloor\Delta U\rfloor\), not
  \(\kappa_w\). **reproduced**.
- Lemma X5 (`J-length7-vdc3-chirps`) — **EXACT — HUMAN
  PROOF**. Isolated monomials, not this sum.
  **independent**.
- Theorem Q engine line \(c'\asymp 1\) — **EXACT —
  HUMAN PROOF**. **reproduced**.
- Phase-5 wall (coefficient \(>n\), derivative
  \(\gg 1\)) — **REFUTED** as an engine route.
  **reproduced**.
- Theorem T passenger slogan
  (`J-length7-passenger-theorem-t`) — **REFUTED**.
  **reproduced**.
- Theorem X (`J-depth7-engine-contracting`) —
  **CONJECTURE**. **extended** by a named method
  failure.

## Branch budget

```text
Mathematical target     Does ∑ e(u w^{3/2}) on X3-runs,
                        with κ_w treated by Q/R3, close
                        inside P^{23/24} without a new
                        decoration class?
Novelty hypothesis      Phase 35 closed the affine
                        interpolant; Q/R3 might absorb
                        the 0-1 carry as an indicator.
Falsifier               κ_w has run length O(1), or the
                        sawtooth coefficient
                        (3u/2) U^{1/2} exceeds n, or
                        leftovers need a new class.
Existing machinery      Lemma X3, X5; Theorem Q engine
                        line; Lemma R3; Phase-5 wall.
Maximum Phase-0 scope   Desk estimate of the three Q/R3
                        readings plus a κ-run-length
                        seal. No Theorem X retag, no
                        Lemma 3.11, no length-8, no
                        Paper B, no new CLI.
Promotion criterion     The inventory sum ≪ P^{23/24}
                        with only existing classes.
Stop criterion          A named Q/R3 margin dies, or a
                        new decoration class is
                        required (PARK X).
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Isolated \(\sum e(un^{27/16})\) (`J-length7-vdc3-chirps`)
  — **EXACT — HUMAN PROOF**
- \(J=\lfloor\Delta U\rfloor\) freeze (Lemma X3) —
  **EXACT — HUMAN PROOF**
- “X3 plus Q/R3 closes \(e(uw^{3/2})\)”
  (`J-length7-x3-qr3-carry`) — **REFUTED**
- Theorem X / density \(57/64\) — **CONJECTURE**
- Length-8 \(E'\) — **CONJECTURE** (untouched)
- \(K_3\) bound — **PARK** (BB/GG/JJ)

## Experiments

Runner: `w_carry_run_scan` in
`research.juggler_sequence.two_step_parity`.
At \(P=10^4,10^5,10^6\) on \(400\) OOEO terms: \(J\)
covers the window, \(\kappa\in\{0,1\}\), mean
\(\kappa\)-run \(2.26\), \(1.64\), \(1.88\). Tests:
`test_length7_x3_qr3_carry`.

## Conjectures

None new. `J-depth7-engine-contracting` and
`J-seven-step-descent-density` stay conjectures.

## Counterexamples

None for the counts. The method counterexamples are
mean \(\kappa\)-run \(O(1)\) on X3-interiors and the
spawned amplitude \(P^{45/32}>n\).

## Formalization

None added.

## Results

- **Proposition X-carry (REFUTED,
  `J-length7-x3-qr3-carry`).**
  Lemma X3 plus Q/R3 does not close
  \(\sum e(uw^{3/2})\) inside \(P^{23/24}\) without a
  new decoration class. Proof: lemma Part XXI.

## Open questions

Answered in Phase 38
([juggler_length7_integer_w.md](juggler_length7_integer_w.md)):
the integer-\(w\) block is the same Phase-5 wall.
Length 8 stays behind \(E'\). Do not reopen
\(e(uw^{3/2})\) and do not rewrite \(45/32\).

## Decision

**PARK** Theorem X. The existing-toolkit route for
the \(\theta_p\) inventory is closed: \(\kappa_w\) is
not frozen on the \(A\)-process window, and the
sawtooth form has coefficient \(>n\). Isolated
Lemma X5 stands. Do not write Lemma 3.11. Best next
question: the integer-\(w\) block at
\(\xi\asymp n^{45/32}\).

## Publication assessment

Status: `EXPLORATORY` (negative knowledge). Not a
Paper B edit. Paper B already refuses densities
beyond \(13/16\).
