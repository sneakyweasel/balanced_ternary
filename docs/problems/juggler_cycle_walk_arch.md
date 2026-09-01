# Juggler DK-arch free-kill of the blocker

Status: **ARCHIVED** (Phase 0 decided)

Successor of the walk-sharpness PARK
([juggler_cycle_walk_sharpness.md](juggler_cycle_walk_sharpness.md)),
answering its recorded reopening point as a *period-bound attack*.
Measurement and one dominance lemma only: the envelope currency
stays \(2s(L)\), no arch-height proof, no new kills, no floor
raise. Not a halt theorem, not a uniform \(B/\theta\) claim.

## Problem

Does a human arch bound \(e=O(\max_j a_{j+1})\) on the DK excess
tighten \(2s(L)/L\) enough to pull the break-even of the live
blocker \(L=478245\) below the certified floor \(162849448\),
killing it with zero new compute?

## Exact statement

Write \(e(L)=\sum_{k<L}F(\{k\alpha\})-LC_*\) for the hug/IET
Birkhoff excess, so \(C_L=C_*+e(L)/L\). The census-free kill
envelope uses \(C_L\le C_*+2s(L)/L\). An arch bound would replace
the cap \(2s(L)\) by \(O(\max_j a_{j+1})\).

**Dominance (EXACT — HUMAN PROOF).** Hug is the unique charge
maximizer
([juggler_cycle_walk_exchange.md](juggler_cycle_walk_exchange.md)).
The walk DP computes that maximum, so it *is* \(C_L\). The DK
envelope is an upper bound on the same quantity. Any valid
tightening of the constant \(2s(L)\) remains an upper bound
\(\ge C_L\). Therefore a length the DP fails to kill at a given
floor cannot be killed at that floor by any valid DK tightening,
arch bound included.

**Instance (COMPUTATIONALLY VERIFIED).** At \(L=478245\),
\(o=301739\), floor \(162849448\), the certified hug DP has
margin \(0.4334<1\)
(`new_floor_kills/L478245.json`). The DK margin is \(0.4333\)
(relative gap \(2.0\cdot 10^{-4}\)). Digit sum \(s=2\), so
\(2s/L=4/478245=8.36\cdot 10^{-6}\) against
\(C_*=0.04372\) (relative \(1.91\cdot 10^{-4}\)).

**Cap-zero still loses (COMPUTATIONALLY VERIFIED).** The most
optimistic (and, since the census excess is one-sided positive,
not even valid) replacement \(C_L\le C_*\) drops
\(n^*(478245)\) from \(3.483\cdot 10^8\) to \(3.482\cdot 10^8\),
relative drop \(1.81\cdot 10^{-4}\), still above
\(162849448\). The same pattern holds on every still-open focus
row (\(780239\), mid-fan \(8632083\), seed \(16785921\)):
cap-zero margins stay \(<1\) and \(n^*\) drops by at most
\(1.7\cdot 10^{-4}\) relatively.

**Required excess (EXACT — HUMAN PROOF; instance
COMPUTATIONALLY VERIFIED).** Kill at a fixed floor is monotone
in the cap \(\kappa/L\). Writing \(m_0\) for the cap-zero
margin, kill requires \(\kappa\le LC_*(m_0-1)\). At the blocker
this is \(\kappa\le -11848\). An arch bound supplies
\(\kappa=O(\max a_{j+1})=O(55)\) on fan A — wrong sign, and
more than two hundred times too small.

**Survivor sparsity (EXACT — HUMAN PROOF).** A negative-side
convergent has greedy Ostrowski digit sum \(s=1\). A
semiconvergent \(L=q+kQ\) with \(0<k\le a_{j+1}\) has
\(s\le k+1\). The lengths that survive are exactly the
digit-sparse ones, so \(2s/L=O(a/q)\) is negligible against
\(C_*\asymp 1/\ln n'\). The lengths where \(2s/L\) is large are
digit-rich, hence already killed with uniform window margin
\(\ge 5.48\). Even the digit-richest priced row (fan A,
\(k=28\), \(s=29\)) has \(2s/L=1.54\cdot 10^{-4}\,C_*\).

No cycle of any length — not claimed.

## Current literature

- DK/Ostrowski envelope \(|C_L-C_*|\le 2s(L)/L\) —
  **EXACT — HUMAN PROOF**
  ([juggler_cycle_walk_ostrowski.md](juggler_cycle_walk_ostrowski.md))
- Hug maximizer and \(C_*\) Laplace integral —
  **EXACT — HUMAN PROOF**
  ([juggler_cycle_walk_exchange.md](juggler_cycle_walk_exchange.md))
- Certified hug DP at the blocker, margin \(0.4334\) —
  **COMPUTATIONALLY VERIFIED**
  ([juggler_cycle_walk_charge.md](juggler_cycle_walk_charge.md))
- Break-even floors and \(n^*(478245)=3.48\cdot 10^8\) —
  **COMPUTATIONALLY VERIFIED**
  ([juggler_cycle_walk_competition.md](juggler_cycle_walk_competition.md))
- Window-bounded one-sided excess, DK never tight —
  **OBSERVATION**
  ([juggler_cycle_walk_sharpness.md](juggler_cycle_walk_sharpness.md))
- Sawtooth / Birkhoff arches (Hecke, Ostrowski, Schoissengeier)
  — **KNOWN**; not used, and not needed
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a period-bound method. The
\(O(\max_j a_{j+1})\) height statement itself stays the parked
sharpness observation, with no cycle consequence.

## Branch budget

```text
Mathematical target     Does a human arch bound e = O(max_j a_{j+1})
                        pull n*(478245) below the certified floor
                        162849448?
Novelty hypothesis      Tightening 2s(L)/L to O(max a)/L lowers every
                        break-even, possibly killing the blocker with
                        zero new compute — the only modest-proof
                        route to a free period-bound move
Falsifier               (i) the certified hug DP already loses at the
                        blocker, and any valid DK tightening sits
                        above that DP; (ii) even the invalid cap
                        C_L <= C_* leaves n* at 3.48e8; (iii)
                        kill requires a large negative excess
Existing machinery      dk_price, break_even_floor, competition
                        artifact, new_floor_kills/L478245.json
Maximum Phase-0 scope   recompute n* at cap 0 and the required
                        excess on the dangerous rows; write the
                        dominance lemma; no Lean, no Paper A, no N0,
                        no arch-height proof
Promotion criterion     n*(478245 | cap=0) < 162849448, or a valid
                        envelope below the hug DP
Stop criterion          the DP loses and cap-zero still sits above
                        the certified floor
```

## Balanced-ternary formulation

None required. The walk lives on the exponent lattice
\(\mu a-b\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Envelope dominance (DP \(\ge\) any valid DK tightening) —
  **EXACT — HUMAN PROOF**
- Survivor sparsity \(s=O(1)\) on near-convergents and
  \(s\le k+1\) on fan members —
  **EXACT — HUMAN PROOF**
- Required excess \(\kappa\le LC_*(m_0-1)\) —
  **EXACT — HUMAN PROOF**
- “Arch bound kills \(478245\) at the certified floor” —
  **REFUTED** (`juggler_walk_arch_kills_blocker`)
- Human proof of \(e=O(\max_j a_{j+1})\) — not attempted
- Improvement of the certified envelope constant — not claimed
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_walk_arch`
- Artifacts: `data/research/juggler/cycle_walk_arch/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_walk_arch.py`

No CLI. No new Lean. Paper A is unchanged. The certified
envelope, kill table, and period bound are not edited. The
arch-height question is not re-opened.

## Conjectures

`juggler_walk_arch_kills_blocker` — **REFUTED**.

`juggler_walk_excess_arch` stays
**COMPUTATIONALLY_SUPPORTED** as a window observation; its
period-bound reading is the refuted row above.

## Counterexamples

- \(L=478245\) at floor \(162849448\): hug DP margin
  \(0.4334<1\); cap-zero \(n^*=3.482\cdot 10^8>162849448\);
  required excess \(-11848\).
- Fan A \(k=2,28\) and seed \(16785921\): same sign, larger
  \(|\kappa|\).

## Formalization

None. No Lean, no `sorry`. Paper A is unchanged. Not a halt
theorem.

## Results

Classification **WALK_ARCH_PAYOFF_DEAD**.

- Dominance: no valid DK tightening can beat the hug DP
- At the blocker, DP and DK agree to relative \(2.0\cdot 10^{-4}\)
- Cap-zero drops \(n^*(478245)\) by \(1.81\cdot 10^{-4}\)
  relatively, leaving \(3.482\cdot 10^8\)
- Required excess \(-11848\) versus arch currency \(O(55)\)
- Digit-rich survivors do not exist: even \(s=29\) at
  \(L=8632083\) has \(2s/L=1.54\cdot 10^{-4}\,C_*\)
- Envelope, kill table, period bound unchanged

## Open questions

Stop on the arch bound as a period-bound method. Do not attempt
the Schoissengeier-type height proof as a cycle attack. The
\(O(\max_j a_{j+1})\) statement remains the parked sharpness
observation, with no cycle consequence. The cycle frontier stays
the fan-minimum reduction of \(\log 2/\log 3\).

## Decision

**CLOSE.** The free-kill slogan is false: the hug DP already
computes the quantity an arch bound would only estimate, and it
loses at the blocker with margin \(0.4334\). Even the illegal
bound \(C_L\le C_*\) leaves \(n^*\) at \(3.48\cdot 10^8\),
because the dangerous lengths are digit-sparse and \(2s/L\) is a
\(10^{-4}\) perturbation of \(C_*\). A kill at the certified
floor would need excess \(-11848\), not \(O(\max a)\). This is
not a halt theorem and not a reason to raise the floor.

Best next question: the cycle frontier remains the fan-minimum
CF reduction — do not reopen the arch height as a period-bound
method.

## Publication assessment

Status: `ARCHIVED`.

A negative payoff: the sharpness reopen does not move the
period bound. The obstruction is exact (DP dominance plus
survivor sparsity). Not a paper candidate and not a Juggler
totality result.
