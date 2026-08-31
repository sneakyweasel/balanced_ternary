# Juggler coupled exponent-walk charge

Status: **ACTIVE** (Phase 0 GREEN; certification pending)

Refinement of the Paper A Section 5 state-distribution program
([juggler_cycle_finance.md](juggler_cycle_finance.md)), answering
the coupling question left open by the necklace phase
([juggler_cycle_cyclic_valley.md](juggler_cycle_cyclic_valley.md)):
a coupling that forbids \(o-e\) independent \(n\)-valleys. Not a
halt theorem, not a no-cycle-of-any-length claim, not a floor
raise, and not a Paper A edit.

## Problem

The length-only parity and run-pack tables price valleys
independently. On a real CycleMin cycle every state is coupled
through one closed exponent walk: with
\(u_k = \log_2(3/2)\cdot\#O_k - \#E_k\), the defect-free upper
envelope (\(\lfloor x^{3/2}\rfloor\le x^{3/2}\),
\(\lfloor\sqrt x\rfloor\le\sqrt x\)) gives \(x_k\le n^{2^{u_k}}\),
and CycleMin forces \(u_k\ge 0\) exactly. Does the exact optimum of
\(\sum_k 1/(x_k\ln x_k)\) over all nonnegative closed walks with
\(o\) up-steps and \(e\) down-steps fall below \(\theta(L)\) at the
certified floor — killing \(L=50508\) without a
\(1.63\cdot 10^8\) campaign?

## Exact statement

**Walk pricing (EXACT — HUMAN PROOF, modulo the transport lemma).**
At step \(k\) with \(a\) odd letters used, \(u=(1+\mu)a-k\) with
\(\mu=\log_2(3/2)\); the DP over \((k,a)\) is exact on the lattice
(no grid rounding). Charging \(x_k\ge n^{\max(2^{u_k}-\eta,\,1)}\)
requires the lower-envelope defect transport \(\eta\): the
log-deficit obeys \(E'\le\tfrac32E+2x^{-3/2}\) (odd),
\(E'\le\tfrac12E+2x^{-1/2}\) (even), amplification from injection
\(j\) to state \(k\) is exactly \(w_k/w_j\), even states have
\(w\ge2\), so \(\eta\le 1.01\,(e/n+2o/n^{3/2})/\ln n\). This bound
is numerical (OBSERVATION), not yet a certified lemma.

**Kill at the target (COMPUTATIONALLY VERIFIED numbers; theorem
pending the transport lemma).** At \(L=50508\), \(o=31867\),
floor \(N_0=26254995\) (`J-residual-floor-twenty-six-million`):
\(\theta=7.2649\cdot 10^{-6}\), parity RHS
\(4.9878\cdot 10^{-5}\), walk RHS \(6.4790\cdot 10^{-6}\) at
\(\eta=0\) — improvement \(7.70\) over parity against the required
\(6.87\). Kill margin \(1.121\) at \(\eta=0\), \(1.120\) at the
transport bound \(\eta^*=4.2\cdot 10^{-5}\), \(1.113\) at
\(10\eta^*\), \(1.042\) at \(100\eta^*\). Classification
**WALK_CHARGE_GREEN**.

**Calibration (COMPUTATIONALLY VERIFIED).** At \(L=25781\), floor
\(10^6\): walk RHS \(1.2984\cdot 10^{-4}\), matching the archived
necklace height-walk value \(1.30\cdot 10^{-4}\) to three digits;
margin \(0.196\) — correctly no kill (required \(32.5\), walk gives
\(6.37\)). The 2026 merge-assessment conclusion (constants cannot
kill the seeds at \(10^6\)) is reproduced, not contradicted.

**Structure.** Cheap valleys need excursion exponents
\((3/2)^a/2^r\) near \(1\), forcing \((a,r)\) onto near-convergents
of \(\log_2(3/2)\): the cheapest return is \(O^{12}E^7\)
(19 letters, valley at \(n^{2^{0.0195}}\)); \(O^{29}E^{17}\),
\(O^{41}E^{24}\), \(O^{53}E^{31}\) are the drift-compensating
types. The walk optimum realizes roughly one cheap valley per 19
letters instead of the parity table's one per \(L/e\approx 2.7\).

No cycle of any length — not claimed.

## Current literature

- Length-only parity \(6/5\) table — **COMPUTATIONALLY VERIFIED**
  (`J-cycle-parity-finance-instance`); run-pack Theorems 4.7--4.8
- Certified floor \(26254995\) and period bound \(50507\) —
  **COMPUTATIONALLY VERIFIED** (`J-residual-floor-twenty-six-million`,
  `J-cycle-period-fifty-thousand`)
- Two-type cheap cap \(N_{\mathrm{cheap}}\le 2e-o\) —
  **EXACT — HUMAN PROOF**
  ([juggler_cycle_cyclic_valley.md](juggler_cycle_cyclic_valley.md));
  its open question (full coupling) is what this branch computes
- Valley-coupling excursion table (\(O^{12}E^7\) below \(9/8\),
  \(O^{53}E^{31}\) at \(n^{1.002}\)) — **CLOSE**
  ([juggler_cycle_valley_coupling.md](juggler_cycle_valley_coupling.md));
  leftover-killer refuted at \(25781\)/\(10^6\), consistent with the
  calibration here
- Paper A × Paper B merge — CLOSE (`juggler_cycle_paper_merge`):
  constant-factor refinements cannot kill seeds at \(10^6\); this
  branch targets \(50508\) at \(26254995\) where the requirement is
  \(6.87\), not \(223\)
- Every start reaches 1 — not claimed

Project relationship: **extended** (the Section 5 program's first
quantitative success at a live target).

## Branch budget

```text
Mathematical target     Does the exact optimum of the cyclic
                        exponent-walk charge fall below θ(50508) at
                        the certified floor 26254995?
Novelty hypothesis      The walk DP over (step, odd-count) is exact
                        on the lattice and is the valley coupling
                        named open by the Section-5 PARK; the
                        required factor is now 6.87, not 32.5
Falsifier               DP optimum ≥ θ, or the defect-transport
                        band erases a sub-1.5 kill margin
Existing machinery      o_min_and_theta / EPS_CONST; Lean power
                        envelope; valley-coupling excursion table;
                        necklace cheap cap as calibration
Maximum Phase-0 scope   One probe: exact DP at (50508,31867)
                        n=26254995, calibration (25781,16266) at
                        10^6, kill table for the 19 leftovers,
                        eta-sensitivity band. No Lean, no Paper A
                        edit, no floor raise, no CLI
Promotion criterion     Budget < θ at 50508 with margin surviving
                        the eta band
Stop criterion          Budget ≥ θ, or margin inside the eta band
```

## Balanced-ternary formulation

None required. The walk lives on the exponent lattice
\(\mu a - b\); the map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Exponent walk \(u_k=(1+\mu)a-k\), exact lattice DP —
  **COMPUTATIONALLY VERIFIED** (matches brute force through
  \(L=14\))
- Upper envelope \(x_k\le n^{2^{u_k}}\), hence \(u_k\ge 0\) —
  **EXACT — HUMAN PROOF** (defect-free floors)
- Transport bound \(\eta^*\) — **OBSERVATION** (numerical, the
  certification target)
- Even-state constraint \(u\ge 1\) before a down-step — automatic
  (\(u\ge 0\) after the unit down-step), consistent with
  `cycleMin_even_ge_sq`
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_walk_charge`
- Artifacts: `data/research/juggler/cycle_walk_charge/summary.json`
  (target + calibration), `survey.json` (19-leftover kill table)
- Tests: `tests/research/juggler_sequence/test_cycle_walk_charge.py`

## Conjectures

`juggler_cycle_walk_charge` (active): the coupled exponent-walk
charge with a certified transport lemma excludes \(L=50508\) as a
CycleMin length at the certified floor \(26254995\).

## Counterexamples

None against the walk model. The calibration point
\((25781, 10^6)\) is a deliberate non-kill: margin \(0.196\),
reproducing the archived necklace value and the merge-assessment
conclusion.

## Formalization

None yet. The certification path: (i) upper envelope \(u\ge 0\)
(defect-free floors, trivial); (ii) lower-envelope transport lemma
(the \(E\)-recursion with amplification \(w_k/w_j\)); (iii) the DP
value as a maximum over the relaxation (any binary word with
\(o\) odds, \(e\) evens, \(u\ge 0\)); (iv) the existing \(6/5\)
unroll interface. No `sorry`. Not started.

## Results

Classification **WALK_CHARGE_GREEN**.

- Target \(L=50508\) at floor \(26254995\): walk RHS
  \(6.479\cdot 10^{-6}<\theta=7.265\cdot 10^{-6}\); margins
  \(1.121/1.120/1.113/1.042\) at
  \(\eta\in\{0,\eta^*,10\eta^*,100\eta^*\}\),
  \(\eta^*=4.2\cdot 10^{-5}\)
- Improvement over parity \(7.70\) (required \(6.87\)); the
  necklace phase's best at \(25781\) was \(6.37\) against a
  required \(32.5\) — the mechanism did not change, the target did
- Calibration \(1.2984\cdot 10^{-4}\) vs archived \(1.30\cdot 10^{-4}\)
- DP is exact on the lattice and matches brute force on all tested
  tiny lengths

## Open questions

- Certify the transport lemma (the only gap between GREEN and a
  laboratory theorem at \(L=50508\))
- The survey's hypothetical cutoff over the 19 leftovers
  (`survey.json`): which lengths beyond the \(50508\) cluster die
- Whether the walk charge plus run-pack composition tightens the
  thin \(1.12\) margin

## Decision

**PROMOTE.** The Phase-0 promotion criterion is met: the walk
optimum excludes the target across the full principled
\(\eta\)-band. The next phase is certification (transport lemma +
outward-rounded comparison), not another probe. Do not claim the
period bound \(>50507\) until certified.

## Publication assessment

If certified, this is the first length-only charge that kills a
survivor-lattice seed below its parity ceiling — a Paper A
Section 5 result (state-distribution finance), upgrading
Theorem 4.6's architecture. Until the transport lemma is exact,
the claim tag is **CONJECTURE** with strong numerics.
