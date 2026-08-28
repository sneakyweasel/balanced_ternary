# Juggler multi-step itinerary-parity census

Status: **THEOREM**

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
- Depth-2 analytic lemma — proved in Phase 1–2
  (`depth2_analytic_lemma_proved` is `True`)
- Even-branch depth-4 results — proved in Phase 3
  (`depth4_even_branch_proved` is `True`)
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
- **Theorem C (nested parity discrepancy)** —
  **EXACT — HUMAN PROOF** (`J-nested-parity-discrepancy`): all four
  joint parity classes of \((m, \lfloor m^{3/2}\rfloor)\) on odd
  \(n \le N\) have cardinality \(N/8 + O(N^{23/24+\varepsilon})\).
  Proof chain: Vaaler waves, Lemma A substitution, one van der Corput
  A-process (\(H = N^{1/12}\)), Lemma B cells with an exactly split
  moving-endpoint expansion, second-derivative test per cell,
  assembly at \(J_1 = J_2 = N^{1/24}\).

## Phase 2: review pass

Adversarial re-derivation of every step (record in the working
document). All estimates re-derived with constants; three
presentational repairs (exact moving-endpoint split replacing
smooth-weight partial summation; majorant-product bookkeeping;
half-integer mode coefficients). The delicate smooth cancellation was
pinned to its exact constant: \(A_h'' \to \tfrac{81}{256} jh^2
n^{-7/4}\), and the scaled-integer validator
`smooth_cancellation_check` returns \(0.3164 = 81/256\) across
\(n = 10^4\) to \(10^8\). No step failed. Ledger rows
`J-nested-parity-linearization` and `J-nested-parity-discrepancy`
added; `depth2_analytic_lemma_proved` flipped to `True`. Ambient
counting only: not an orbit transfer, not a frequency theorem along
trajectories, not a termination claim.

## Phase 3: the depth-4 extension

Same working document, Part II. The structural surprise: depth 4 is
*easier* than depth 2, because after Lemma A's pattern is applied
twice more, every non-smooth term of the fourth-letter phase has
decaying amplitude.

- **Lemma D (fourth-letter linearization)** — **EXACT — HUMAN PROOF**
  (`J-fourth-letter-linearization`): \(v^{1/2} = n^{9/8} + D(n)\) with
  \(-\tfrac34 n^{-3/8} - n^{-9/8} \le D(n) \le 0\), where
  \(v = \lfloor m^{3/2}\rfloor\). Smoothing the fourth letter costs
  only \(O(kN^{5/8})\) cumulatively, so it happens *before* any
  differencing. Validated exactly through \(n = 10^{12}+1\); worst
  ratio \(0.9970\) against supremum \(1\).
- **Theorem E (triple parity discrepancy)** — **EXACT — HUMAN PROOF**
  (`J-triple-parity-discrepancy`): all eight sign classes of
  \(((-1)^m, (-1)^v, (-1)^{\lfloor\sqrt v\rfloor})\) on odd
  \(n \le N\) have cardinality \(N/16 + O(N^{23/24+\varepsilon})\).
  Pure fourth-letter modes reduce to a single smooth exponential sum;
  mixed modes rerun the Theorem C machinery with a smooth passenger
  whose curvature is smaller than every retained scale by
  \(\ge N^{9/8-1/24}\).
- **Corollary F (four-step descent density)** — **EXACT — HUMAN
  PROOF** (`J-four-step-descent-density`):
  \(\#\mathrm{OOEE}(N) = N/16 + O(N^{23/24+\varepsilon})\), and the
  certified \(\le 4\)-step descent class (evens, OE, OOEE) has density
  \(13/16\) — up from the paper's \(3/4\). Branch consistency of the
  indicator algebra \((1-\psi_1)(1+\psi_2)(1+\psi_3)/8\) verified
  exactly (`ooee_indicator_identity_check`).

Review record in the working document (Phase-3 section): Lemma D's
remainder chain re-derived, the absorption order checked (smoothing
precedes differencing, so no \(\theta\)-dependence reaches the van
der Corput stage), curvature sign and dominance margins verified for
both mode cases, float sanity on \(|S_{0,0,1}|\). No step failed.

## Phase 4: beyond depth 4 — tier structure and the density-one program

Same working document, Part III. Scope: what generalizes, what the
ceiling is, the algebraic bricks for tier 2, route obstructions, and
the conditional density-one theorem. The tier-2 bound is not claimed.

- **Proposition I (one-growing-layer ceiling)** — **EXACT — HUMAN
  PROOF**: the machinery of Parts I–II certifies exactly \(E\),
  \(OE\), \(OOEE\) among contracting prefixes; \(13/16\) is the exact
  ceiling of the method. Every further certified start needs a second
  growing nesting layer (an odd letter at position \(\ge 3\)).
- **Lemma G (second-order exact linearization)** — **EXACT — HUMAN
  PROOF** (`J-second-order-linearization`): exact quadratic-in-\(m\)
  forms of \(m^{3/4}\) and \(m^{9/4}\) with decaying remainders, by
  substituting \(\theta = X - m\) into both the linear and quadratic
  Taylor terms. Validated at scale \(10^{60}\) through
  \(n = 10^{12}\).
- **Proposition H (polynomial phase)** — **EXACT — HUMAN PROOF**: the
  OOO\* layer phase \(v^{3/2}\) equals a degree-\((2,1)\) polynomial
  in the integer pair \((m, v)\) with smooth coefficients, up to
  \(\tfrac34 n^{-9/8}\). The tier-2 analogue of Lemma A's linear
  structure. Branch algebra for OOO\* machine-checked.
- **Obstructions recorded**: (i) composed Lemma-B cells fail — the
  second-level gap changes at essentially every point of a cell
  (distinct ratio \(1.0000\)); (ii) the fiber transform to
  \(m\)-space strips one nesting level but loses to the sparsity
  exponent \(1/3 \gg 1/24\); the \(r = 1\) fiber mode is fatal. Both
  routes parked permanently.
- **Proposition J (conditional density-one)** — **EXACT — HUMAN
  PROOF** (`J-equidistribution-implies-density-one`): all-depth
  parity equidistribution with power savings implies density-one
  finite descent (Hoeffding, \(c > 0.0342\)) — the Juggler analogue
  of the Terras program. Implication unconditional; hypothesis open
  beyond depth 3 (closed by Proposition L in Phase 5) and the OOE\*
  splits at depth 4.
- **Census gate (depth 6)** — **COMPUTATIONALLY VERIFIED**: all 32
  words realized at \(N = 2\cdot10^6\); deviations obey the
  two-regime minimal-scale envelope
  \(|D_w| \le 1.1\max((N/2)N^{-\gamma_{\min}}, N^{2/3})\) across
  \(N = 10^5, 5\cdot10^5, 2\cdot10^6\). E-heavy words are
  boundary-dominated (deep values reach single digits), not biased.
- **Conjecture K**: all-depth equidistribution. The concrete next
  case is tier 2 (OOO\* split) via the double-differencing route:
  A-process on the polynomial phase, shifted-window Vaaler for the
  growing sawtooth amplitudes (\(\asymp khn^{7/8}\)),
  third-derivative tests, one more differencing. Expected saving
  \(\delta_2 \sim 10^{-2}\).

## Phase 5: depth-3 completion, tier-2 bricks, and the kernel

Working document, Part IV. Scope: close a discovered gap at depth 3,
prove the level-2 structural lemmas, and drive the tier-2 reduction
until it closes or the obstruction is exact. It did not close; the
obstruction is now a single named object.

- **Correction note**: Phase-4 wording said depth 3 was "proved" —
  but the OE-branch third letter (OEO/OEE split, \(\psi(m^{1/2})\) on
  even \(m\)) had never been stated. Recorded honestly; closed the
  same phase.
- **Proposition L (OE-branch third letter)** — **EXACT — HUMAN
  PROOF** (`J-even-branch-third-letter`): \(\#\mathrm{OEO}(N),
  \#\mathrm{OEE}(N) = N/8 + O(N^{7/8+\varepsilon})\) via the decaying
  smoothing \(m^{1/2} = n^{3/4} + D_1\) and van der Corput II. Depth
  3 is now genuinely complete.
- **Lemma M (plain and shifted second-order forms)** and **Lemma N
  (level-2 gap identity)** — **EXACT — HUMAN PROOF**
  (`J-tier2-gap-and-shifted-forms`): \(m^{3/2}\) and
  \((m{+}G)^{3/2}\) as quadratics in \(m\) with positive
  \(O(X^{-3/2})\) Taylor remainders; \(g_2 = \lfloor\Delta Y\rfloor +
  \kappa_2\), Lemma B one level up. Validated to \(n = 10^{12}\).
- **Kernel isolation** (negative knowledge with an exact core): after
  the A-process, the \(v\)-block term \(g_2 W_+\) leaves a
  unit sawtooth \(\theta_2\) carrying the smooth coefficient
  \(W \asymp k n^{9/8}\) whose derivative \(\asymp k n^{1/8} \gg 1\)
  crosses integers within single steps. Four reorganizations (Lemma-N
  split, the exact swap \(e(c\theta_2) = e(cY)e(-\{c\}v)\), a second
  A-process, raw differencing without Proposition H) all funnel into
  the same object. Only the \(\kappa_2\)-content is harmless (0/1
  indicator weight). **Kernel**: \(K_c(P) = \sum_{n \sim P}
  e(c(n)\{\lfloor n^{3/2}\rfloor^{3/2}\})\), \(c \asymp k P^{9/8}\),
  \(c' \asymp k P^{1/8}\).
- **Conjecture O (kernel cancellation)**: \(K_c \ll P^{1-\delta}\).
  Float probe with exact scaled phases: \(|K| = 51.9, 124.4, 1017.5\)
  on \(5\cdot10^3, 5\cdot10^4, 5\cdot10^5\) terms — square-root
  cancellation. A bilinear correlation between the fractional parts
  of one Piatetski–Shapiro layer and a smooth weight at the next
  layer's scale; no treatment found in the nested-floor literature.
- **OEO\* observation**: at depth 4 after OE, the growing layer rides
  the slow variable \(w = \lfloor m^{1/2}\rfloor\) (increments every
  \(\asymp n^{1/4}\) steps, long constancy cells) — the Theorem-C
  pattern shifted one level down. Likely closable by the existing
  engine *without* meeting the kernel; would settle depth 4 except
  OOO\*.

## Phase 6: the OE\*\* splits — depth 4 complete except OOO\*

Working document, Part V. Scope: the promoted question — does the
engine iterate one level down the scale hierarchy? It does, and the
reduction is *shorter* than Theorem C.

- **Lemma A′ (w-level linearization)** — **EXACT — HUMAN PROOF**:
  since \(U m^{1/4} = m^{3/4}\) exactly (\(U = m^{1/2}\), \(w =
  \lfloor U\rfloor\)), Lemma A collapses to \(w^{3/2} = m^{3/4} -
  \tfrac32 m^{1/4}\theta_w + E\) with \(0 \le E \le \tfrac38
  (U-1)^{-1/2}\). Two exact Taylor steps smooth the whole fourth
  letter to \(n^{9/8}\) minus one growing sawtooth \(B\theta_w\),
  \(B = \tfrac{3k}4 n^{3/8}\). Validated to \(n = 10^{12}\)
  (`lemma_a_prime_scan`, `oeo_smoothing_scan`).
- **Theorem Q (OE\*\* splits)** — **EXACT — HUMAN PROOF**
  (`J-depth4-slow-branch`): \(\#\mathrm{OEOE}, \#\mathrm{OEOO} =
  N/16 + O(N^{7/8+\varepsilon})\); \(\#\mathrm{OEEE}, \#\mathrm{OEEO}
  = N/16 + O(N^{13/16+\varepsilon})\). No differencing: \(B\) drifts
  by \(\le 1\) on intervals of length \(P^{5/8}/k\); shifted-window
  Fourier expansion, sign-collision check (\(T = P^{5/16} \ll
  kP^{3/8}\) for every \(k \ge 1\)), van der Corput II, balance
  \(J = P^{1/8}\). Branch consistency of all four indicators
  machine-checked (`oeo_indicator_identity_check`).
- **Depth 4 is complete except OOO\***: six of eight odd-rooted
  words proved (Theorems E and Q); OOO\* is exactly the kernel
  (Conjecture O). The regime boundary is now sharp: the engine
  reaches letters whose phase coefficients grow slower than \(n\)
  (integer crossings slower than one per step); OOO\* sits above.
- **Proposition J audit**: E-rooted words have a contracting prefix
  at length 1, so the hypothesis only consumes O-rooted class bounds
  — no further hidden gap.
- Float sanity: the OEO mode sum tracks the coherent-cell
  random-walk scale \(P^{5/8}\) (\(1361\) vs \(1333\) predicted at
  \(P = 10^5\); \(6142\) vs \(5623\) at \(10^6\)), far below the
  proven \(P^{7/8}\); the census fitted depth-4 exponent \(0.66\)
  matches.

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

One mathematical: does the Phase-8 double-differencing draft proof of
Conjecture O (Theorem R, working doc Part VI, \(\delta = 1/72\)
uniformly for \(k \le P^{1/24}\)) survive an adversarial review pass
at the Theorem-C standard, and does its passenger-robust variant
close the OOO\* corollary? The editorial import into the
finite-dynamics note is done (Phase 7, consolidation); the kernel
tag stays `CONJECTURE` until review.

## Decision

**PROMOTE** (Phase 0, census gate): every depth \(\le 4\) class
converges to the product density with envelope exponents
\(0.28\)–\(0.66\); the falsifier did not fire.

**PROMOTE** (Phase 1, analytic lemma): the growing-amplitude
obstruction dissolved under the exact linearization (Lemma A), the
supporting cell structure is exact (Lemma B), and a complete draft
proof of the depth-2 power saving \(N^{23/24+\varepsilon}\)
(Theorem C) was written with explicit exponent bookkeeping.

**PROMOTE** (Phase 2, review pass): every step of Theorem C
re-derived adversarially; the one delicate cancellation confirmed to
its exact constant \(81/256\); three presentational repairs applied;
ledger rows added and the module flag flipped. The theorem is
settled at project standard.

**PROMOTE** (Phase 3, depth-4 extension): Lemma D closed the fourth
letter with decaying amplitudes, Theorem E extended the discrepancy
bound to all eight triple-parity classes at the same exponent
\(23/24\), and Corollary F lifted the certified \(\le 4\)-step
descent class to density \(13/16\). Three ledger rows added;
`depth4_even_branch_proved` flipped to `True`.

**PROMOTE** (Phase 4, beyond depth 4): the generalization question
was answered structurally. Proposition I fixes \(13/16\) as the exact
ceiling of the one-growing-layer method; Lemma G and Proposition H
provide the proved algebraic bricks for the second growing layer;
two tempting shortcut routes were refuted and recorded; Proposition J
turns all-depth equidistribution into density-one finite descent
(the Juggler Terras program), unconditionally as an implication. Two
ledger rows added. The tier-2 analytic bound is the promoted open
frontier, not a claim.

**PROMOTE** (Phase 5, kernel isolation): a real gap at depth 3 was
found and closed the same phase (Proposition L); the tier-2 bricks
(Lemmas M/N) are proved and validated to \(10^{12}\); and the tier-2
reduction was driven to a single irreducible obstruction, the kernel
\(K_c\), with four dead reorganizations recorded as negative
knowledge and a float probe showing square-root cancellation
(Conjecture O). Two ledger rows added; the Proposition-J row
corrected. The kernel bound is the promoted frontier, not a claim.

**PROMOTE** (Phase 6, OE\*\* splits): the engine iterates down the
scale hierarchy exactly as conjectured — Lemma A′ collapsed the
reduction to two Taylor steps, Theorem Q closed all four OE\*\*
classes at \(N^{7/8+\varepsilon}\)/\(N^{13/16+\varepsilon}\) with no
differencing, and depth 4 is complete except OOO\*. The
engine/kernel regime boundary is now sharp (coefficient growth
\(n^{1}\)). One ledger row added; Proposition-J row and Conjecture-K
texts updated.

**PROMOTE** (Phase 7, consolidation): the branch is imported into the
finite-dynamics note at publication quality. Lemmas A/B/D/A′ and
Theorems C/E/L/Q enter as note Lemma 5.3, Theorem 5.4,
Proposition 5.5, Lemma 5.6, Theorems 5.7–5.8; Corollary F and the
Proposition-I ceiling as Corollary 5.9; Proposition J as
Proposition 6.1; Conjecture O as Conjecture 6.2, with the two
analytic route obstructions recorded in the note's Section 6
negative-knowledge paragraph. The exact floor reductions (parity
bridge, Lemma B/N gap identity) are now Lean-verified in
`formal/Problems/Juggler/GapCells.lean`
(`floor_odd_iff_half_le_fract_half`, `floor_add_eq_add_carry`,
`floor_gap_eq_carry`, `seq_floor_gap`), imported by both barrels.
Reviewer packet, formalization map, frontier figure, ledger
(`J-kernel-cancellation` added; lean fields on the gap rows), and the
review bundle are synchronized; PDFs rebuilt.

**PROMOTE** (Phase 8, kernel attack): a complete double-differencing
draft proof of Conjecture O was written (Theorem R, working doc Part
VI): two Weyl differencings exploit the level-2 numerology \(Y''
\asymp P^{1/4} \gg 1 > P^{-3/4} \asymp Y'''\), the exact double-gap
identity (Lemma R2, Lean `seq_floor_gap_second`) reduces the integer
content to bounded/frozen values, and the branch decomposition
(Lemma R3) carries the level-1 flicker in indicator weights — no
full-size sawtooth coefficient survives, evading both recorded
Phase-5 walls, which differenced sub-organizations rather than the
full phase. Draft exponent: \(\delta = 1/64\) for bounded \(k\),
\(1/72\) uniformly for \(k \le P^{1/24}\). The falsifier fired once
(raw \(\lfloor\Delta\Delta Y\rfloor\) is *not* frozen — mean run
1.5, jumps \(\tfrac32 P^{3/4}\)) and was met by the exact branch
reorganization, recorded as negative knowledge. New validators:
`kernel_reformulation_scan` (Lemma R1, kernel = level-2 local floor
defect sum, exact to \(10^{12}\)), `double_gap_identity_check`,
`branch_freeze_scan`, `differenced_kernel_probe` (\(|T_1|, |T_2|\)
at square-root scale). No ledger retag, no note import, no density
claim: `kernel_bound_proved` stays `False`;
`kernel_double_differencing_draft` flipped to `True`.

Best next question: does Theorem R's bookkeeping survive an
adversarial re-derivation of every piece (the Theorem-C treatment),
including the sign-dominance checks and the passenger-robust OOO\*
corollary?

## Publication assessment

Status: `THEOREM`, imported. Exact linearization lemmas, power-saving
joint-parity discrepancy bounds for nested floor-power sequences at
all depths \(\le 3\) and every depth-4 word except OOO\*, outside the
existing Piatetski-Shapiro literature, and a certified-descent
density of \(13/16\) — now the note's Section 5 headline, replacing
\(3/4\). The isolated kernel \(K_c\) (Conjecture O) is stated in the
note as Conjecture 6.2, with a sharp engine/kernel regime boundary.
No pending editorial debt.
