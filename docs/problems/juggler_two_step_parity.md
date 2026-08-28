# Juggler multi-step itinerary-parity census

Status: **EXPLORATORY**

Phase-0 gate for iterating the one-step image-parity discrepancy bound
(Theorem 5.1 of the finite-dynamics note, \(|S_O(N)|\ll N^{5/6}\)) to
joint parity words of depth two through four on odd starts. Exact
integer counting only. Not a frequency theorem, not a predictive-state
claim, and not a termination claim.

## Problem

Do the joint parity words \((n, J(n), J^2(n), J^3(n)) \bmod 2\) on odd
starts converge to the product densities, and with what empirical
discrepancy exponent — i.e., is the depth-2 analytic lemma worth
attempting?

## Exact statement

For odd \(n\), let \(w(n)\) be the length-4 itinerary parity word
(first letter always `O`). For each word \(w\) of length
\(d\in\{2,3,4\}\), set

\[
D_w(N) = \#\{\text{odd } n \le N : w(n)\text{ has prefix } w\}
  - \frac{\#\{\text{odd } n \le N\}}{2^{d-1}}.
\]

Phase 0 asks whether every \(D_w(N) = o(N)\) empirically, with a
fitted envelope exponent clearly below 1, on \(N \le 10^7\). It does
not prove any bound.

## Current literature

- Theorem 5.1 (`J-odd-image-discrepancy`): the depth-1 odd-start sign
  sum satisfies \(|S_O(N)|\ll N^{5/6}\) — **EXACT — HUMAN PROOF**. Its
  dossier's recorded best next question was whether the bound
  iterates; this branch is that question's Phase 0.
- Parity discrepancy transfer — **REFUTED** (translation-uniform
  short-interval law). Avoided here: the summation variable stays
  \(n\), never the sparse image set.
- Landing-θ and residue predictive states — **CLOSE**/**REFUTED**.
  Not reopened: densities of word classes are counted, no state is
  claimed to predict the next letter.
- `ooe_cylinder_both_next_parities` — residue classes do not decide
  letter 3. Consistent with (and explains the need for) an
  Archimedean, not 2-adic, approach.
- Piatetski-Shapiro-type nested-floor equidistribution: the depth-2
  parity is the parity of \(\lfloor m^{3/2}\rfloor\) at
  \(m=\lfloor n^{3/2}\rfloor\), a nested floor outside the classical
  single-floor theory. Project relationship: **independent**.

## Branch budget

```text
Mathematical target     Do joint parities (J(n), J^2(n), J^3(n)) mod 2
                        on odd n equidistribute with power-saving
                        discrepancy, empirically, at depth <= 4?
Novelty hypothesis      Depth >= 2 classes have product densities; the
                        contracting OOEE class then carries a uniform
                        4-step certificate, lifting certified density
                        above 3/4 once a depth-2 lemma is proved.
Falsifier               A depth-2/3/4 class not converging to the
                        product density, or envelope exponent ~ 1.
Existing machinery      floor_power; Theorem 5.1; oo-descent census;
                        refuted transfer row (kept closed).
Maximum Phase-0 scope   One exact census module + pinned tests +
                        geometric envelope fit, N <= 10^7, depth <= 4.
                        No analytic proof, no Lean, no CLI, no plots.
Promotion criterion     All depth <= 4 classes converge with fitted
                        exponent clearly < 1.
Stop criterion          Persistent density bias, exponent ~ 1, or
                        machinery gravity.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Depth-4 itinerary word census over odd \(n \le 10^7\) —
  **COMPUTATIONALLY VERIFIED** (exact isqrt counting)
- All eight depth-4 classes at product density \(1/8\pm0.2\%\) —
  **OBSERVATION**
- Depth-2 envelope \(\max|D_w|=195\) at \(N=10^7\)
  (\(\approx N^{1/3}\) scale, fitted exponent \(0.28\)) —
  **OBSERVATION**
- Depth-3/4 fitted exponents \(0.63\) / \(0.66\) —
  **OBSERVATION**
- OOEE class fraction \(0.125039\) with zero four-step descent
  violations (guard for the exact contraction \(x^{16}\le n^9\)) —
  **COMPUTATIONALLY VERIFIED**
- Depth-2 analytic lemma — not claimed; `depth2_analytic_lemma_proved`
  stays `False`
- Global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.two_step_parity`
- Records: [juggler_two_step_parity.md](../research/juggler_two_step_parity.md),
  [juggler_two_step_parity.json](../research/juggler_two_step_parity.json)
- Tests: `tests/research/juggler_sequence/test_two_step_parity.py`
  (pinned exact counts at \(N=10^5\))

One CPU pass, 26 seconds at \(N=10^7\). No GPU, no Lean change, no
Research Engine modification.

## Conjectures

None opened. Envelope exponents are observations.

## Counterexamples

- None found on the window: no class bias, no descent violation.
- Prior refutations stand: residue classes do not decide letter 3;
  θ-bins do not predict the next landing; the short-interval transfer
  law is false. None were retested.

## Formalization

None added. The four-step OOEE certificate shape
\(T_w(n)^{16}\le n^9\) is an instance of the existing Lean power
envelope; no new file is warranted before the analytic lemma survives
review.

## Phase 1: the analytic lemma

Working document:
[juggler_two_step_parity_lemma.md](../research/juggler_two_step_parity_lemma.md).

- Literature check (August 2026): nested floor powers
  \(\lfloor\lfloor n^c\rfloor^d\rfloor\) are not covered by the
  Piatetski-Shapiro corpus (single floors, intersections,
  pseudo-polynomials only). Novelty annotation: **independent**.
- **Lemma A (exact linearization)** — **EXACT — HUMAN PROOF**:
  \(m^{3/2} = \tfrac32 m n^{3/4} - \tfrac12 n^{9/4} + E(n)\) with
  \(0 \le E(n) \le \tfrac12 n^{-3/4}\). The nested fractional part is
  eliminated exactly; the integer \(m\) enters the phase linearly.
  Validated by exact scaled-integer arithmetic through
  \(n = 10^{12}+1\); the observed worst ratio \(0.7494\) matches the
  theoretical supremum \(3/4\).
- **Lemma B (gap cells)** — **EXACT — HUMAN PROOF**:
  \(m(n{+}2h) - m(n) = \lfloor\delta(n)\rfloor + [\{n^{3/2}\} \ge
  1 - \{\delta(n)\}]\), giving \(O(hP^{1/2})\) cells of length
  \(\asymp P^{1/2}/h\) per dyadic block on which the gap is constant.
  Validated exactly at \(10^6\) and \(10^9\).
- **Theorem C (nested parity discrepancy, drafted)**: all four joint
  parity classes of \((m, \lfloor m^{3/2}\rfloor)\) on odd
  \(n \le N\) have cardinality \(N/8 + O(N^{23/24+\varepsilon})\).
  Proof chain: Vaaler waves, Lemma A substitution, one van der Corput
  A-process (\(H = N^{1/12}\)), Lemma B cells with a Vaaler-expanded
  \(\kappa\), second-derivative test per cell, assembly at
  \(J_1 = J_2 = N^{1/24}\). Drafted at full exponent bookkeeping in
  the working document, deliberately unoptimized, **pending the
  review pass** that Theorem 5.1 received. Not tagged, not in the
  ledger, not in the note. `depth2_analytic_lemma_proved` stays
  `False`.

## Results

At \(N=10^7\) (4,999,999 odd starts):

| depth | max \(|D_w|\) | \(\max|D|/N^{1/2}\) | fitted exponent |
| --- | --- | --- | --- |
| 2 | 195.0 | 0.062 | 0.28 |
| 3 | 1156.5 | 0.366 | 0.63 |
| 4 | 3020.75 | 0.955 | 0.66 |

All eight depth-4 counts lie in \([623915, 625551]\) against the
product value \(625000\). The OOEE class holds \(12.504\%\) of odd
starts (product density \(12.5\%\)) and every OOEE start satisfied
\(T^4(n)<n\). The depth-2 envelope is on the same \(N^{1/3}\) scale
as the proven depth-1 case. Labels: **COMPUTATIONALLY VERIFIED**
counts, **OBSERVATION** exponents.

## Open questions

Review Theorem C (the drafted proof) at the rigor level applied to
Theorem 5.1; only then import into the note and ledger. After that:
the depth-4 extension via the decaying-amplitude identity
\(m^{3/4} = \tfrac34 m n^{-3/8} + \tfrac14 n^{9/8} + O(n^{-15/8})\),
targeting the OOEE density \(1/16 + o(1)\) and a certified descent
class of density \(13/16\).

## Decision

**PROMOTE** (Phase 0, census gate): every depth \(\le 4\) class
converges to the product density with envelope exponents
\(0.28\)–\(0.66\); the falsifier did not fire.

**PROMOTE** (Phase 1, analytic lemma): the growing-amplitude
obstruction dissolved under the exact linearization (Lemma A), the
supporting cell structure is exact (Lemma B), and a complete draft
proof of the depth-2 power saving \(N^{23/24+\varepsilon}\)
(Theorem C) is written with explicit exponent bookkeeping. What is
promoted is the draft, not a ledger row: the next phase is the
dedicated review pass, and only after it survives do the note import,
the ledger row, and the depth-4 extension (OOEE density, certified
class \(13/16\)) open.

Best next question: does Theorem C survive a dedicated review pass at
the rigor level applied to Theorem 5.1?

## Publication assessment

Status: `EXPLORATORY`. A clean census supporting a concrete analytic
target; no theorem yet, not a paper candidate.
