# Juggler cyclic valley necklace

Status: **ARCHIVED**

Refinement of
[juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md),
[juggler_cycle_valley_coupling.md](juggler_cycle_valley_coupling.md),
and [juggler_cycle_realizable_finance.md](juggler_cycle_realizable_finance.md),
not a new paper. After local realizability of the finance
extremizer closed, this phase asks whether treating valleys as a
**closed necklace**

\[
v_1\to p_1\to v_2\to\cdots\to v_m\to p_m\to v_1
\]

forces a finance deficit versus the independent run-type packing
that cannot be rotated away. Not a halt theorem, not a
branch-and-bound engine, not a floor raise, and not a \(K\le 20\)
proof.

## Problem

The length-only packing maximises \(\sum 1/(x_i\log x_i)\) over
valleys that may be chosen independently subject to lower bounds.
A real cycle must realise every adjacent pair, including the
wrap-around \(v_m\to p_m\to v_1\). There is no privileged first
valley. Does that cyclic transition constraint kill \(L=25781\)
at the published floor, or strictly lower the packed RHS below
\(\theta\)?

## Exact statement

**Two-type cheap cap (EXACT — HUMAN PROOF).**
On a CycleMin two-type necklace the only legal landings below
envelope height \(9/8\) are `OE` landings. An `OOE` run from
\(\alpha\ge 1\) lands at \(\ge 9/8\). An `OE` start requires
\(\alpha\ge 4/3\). The CycleMin start is the wrap-around landing,
not a free boundary. Hence

\[
N_{\mathrm{cheap}}(\alpha<9/8)\;\le\;N_{\mathrm{OE}}=2e-o.
\]

At \((L,o)=(25781,16266)\) this is \(2764<6751=o-e\).

**Cyclic charge does not kill \(25781\) (COMPUTATIONALLY VERIFIED).**
Charging \(2764\) valleys at \(n\), the remaining \(3987\) `OOE`
starts at the laboratory \(9/8\) height, and `OE` starts at
`oe_start_min`, gives RHS \(3.041\cdot 10^{-4}\) against
\(\theta=2.546\cdot 10^{-5}\) (factor \(11.94\)). Lost cheap
starts \(3987\le 6532\). `parity_excludes` and `budget_excludes`
remain false.

**Legal two-type necklaces attain the cap, not the packing
(COMPUTATIONALLY VERIFIED).**
The Beatty packed, letter-extremal, and Christoffel words are
two-type, prefix-admissible, and CycleMin-legal, each with
exactly \(2764\) cheap valleys. Their envelope height-walk RHS
is \(1.30\cdot 10^{-4}\), still above \(\theta\). Bunched
`OOE` then `OE` is legal with one cheap valley. Interleaving
`OOE`/`OE` is CycleMin-illegal: `OE` after one `OOE` sits at
\(9/8<4/3\).

**Wrap-around is not a privileged extra tax (COMPUTATIONALLY
VERIFIED).**
Every sampled CycleMin-legal cyclic cut of a legal two-type
necklace respects the cheap cap (span \(0\)). Exact wrap
\(F_a(v_{\mathrm{last}})=v_1\) fails on the realized chains
from \(365\), \(1517\), and \(1000057\). Rotating a path and
re-testing \(F_a\) only rediscovers existing edges.

**Small-\(m\) cyclic max is strictly below independent packing
(COMPUTATIONALLY VERIFIED).**
On \(m\le 5\) and run depth \(\le 3\), \(170\) CycleMin-legal
necklaces; none beats the independent packing. Champion
\((2,2,2,1,2)\).

No cycle of any length — not claimed.

## Current literature

- Run-type packing, \(N_{\mathrm{cheap}}=o-e\) —
  **EXACT — HUMAN PROOF**
  ([juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md));
  cyclic run-adjacency leftover-killer **REFUTED**
  (`juggler_cycle_run_extremum_leftover_killer`). That
  refutation treated non-adjacent cheap valleys as free; the
  two-type cap is the cyclic correction.
- Return-cost coupling, \((5,3)\) descent —
  **CLOSE** / leftover-killer **REFUTED**
  ([juggler_cycle_valley_coupling.md](juggler_cycle_valley_coupling.md))
- Prefix expansion of near-convergents —
  **CLOSE**
  ([juggler_cycle_prefix_feasibility.md](juggler_cycle_prefix_feasibility.md))
- Realizable-prefix finance tax \(0\) —
  **CLOSE**
  ([juggler_cycle_realizable_finance.md](juggler_cycle_realizable_finance.md))
- Cheap-`OOE` / \(243<256\) —
  **EXACT — HUMAN PROOF** /
  leftover-killer **REFUTED**
  ([juggler_cycle_ordered_excursion.md](juggler_cycle_ordered_excursion.md))
- Collatz-style financing —
  **known** (`simons-de-weger-2005-collatz-m-cycles`)
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a leftover-killer; the
two-type cheap cap is negative knowledge on the Section 5
independent-valley model.

## Branch budget

```text
Mathematical target     Does requiring every adjacent valley pair,
                        including the wrap-around v_m → p_m → v_1,
                        to be a realizable Juggler transition force
                        a finance deficit versus independent
                        run-type packing that cannot be rotated
                        away, large enough to kill L=25781?
Novelty hypothesis      The finance relaxation is a path of
                        independently cheap valleys. A cycle is a
                        closed necklace: there is no privileged
                        first valley.
Falsifier               Wrap-around is unique visit / 3^o≈2^L /
                        cheap-OOE adjacency; a closed type-necklace
                        attains the packed sum; the closure deficit
                        rotates inside the 6532-slack; or the graph
                        is exponent-balance rewritten
Existing machinery      excursion_map; run_type_counts / budget_rhs;
                        valley_coupling circuits; run_extremum
                        cyclic adjacency; prefix_admissible;
                        conditioned-closure slack
Maximum Phase-0 scope   Small cyclic valley graph: two-type height
                        walks, cheap cap, small-m exhaustive, exact
                        wrap/rotation. No B&B, no 2^L search, no
                        Lean, no floor raise
Promotion criterion     A reusable cyclic-necklace inequality
                        Σ c(v_i) ≤ packed − δ, not unique visit /
                        3^o≈2^L / cheap-OOE adjacency, that kills
                        25781 or shrinks E_run
Stop criterion          Closed type-walk attains packing; wrap
                        deficit is a rotation of known cells; δ
                        inside 6532-slack; or the graph is
                        exponent-balance rewritten
```

## Closed-bridge gates

- **CLOSE** if \(N_{\mathrm{cheap}}\le N_{\mathrm{OE}}\) on two-type
  necklaces but the charged RHS stays above \(\theta\).
- **CLOSE** if the wrap-around is unique visit or \(3^o\approx 2^L\),
  or if rotation moves the deficit inside the \(6532\) slack.
- **CLOSE** if every legal two-type necklace attains the packed
  independent sum.
- **PROMOTE** only if a cyclic-necklace bound excludes \(25781\)
  or shrinks \(\mathcal E_{\mathrm{run}}\) and is not an archived
  cell.

Do **not** build a branch-and-bound valley search. Do **not**
prove \(K\le 20\). Do **not** raise \(N_0\). Do **not** open
\(L=55293\). Do **not** edit Paper A.

## Explicitly out of Phase-0

A Pareto / B&B engine, \(K=11\) proof, the \(1054k\) family,
Fourier / residues / \(Q\)-sections, ledger row, Lean, CLI,
visualization, Paper A edit.

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Two-type cheap cap \(N_{\mathrm{cheap}}\le N_{\mathrm{OE}}\) —
  **EXACT — HUMAN PROOF**
- Envelope height walk of two-type necklaces —
  **COMPUTATIONALLY VERIFIED**; Beatty attains the cap
- Cyclic two-type charge versus \(\theta\) —
  **COMPUTATIONALLY VERIFIED**; factor \(11.94\), inside slack
- Wrap-around as a privileged extra tax —
  **REFUTED**; legal cuts respect the cap; exact wrap does not
  close
- Small-\(m\) cyclic versus independent packing —
  **COMPUTATIONALLY VERIFIED**; independent strictly larger
- Leftover-killer at \(L=25781\) —
  **REFUTED** (`juggler_cycle_cyclic_valley`)
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_cyclic_valley`
- Dataset: `data/research/juggler/cycle_finance/cyclic_valley/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_cyclic_valley.py`
- Window: two-type necklaces at \((25781,16266)\); motifs
  \((2,1)\), \((5,3)\), \((12,7)\), \((53,31)\),
  \((\mathtt{OOE})^3\mathtt{OE}\); small-\(m\le 5\); exact wrap
  on \(\{365,1517,1000057\}\). Fast suite only. No CLI. No Lean.

## Conjectures

`juggler_cycle_cyclic_valley` — **REFUTED**.

## Counterexamples

- Lost cheap starts \(3987\le 6532\); cyclic RHS
  \(3.041\cdot 10^{-4}>\theta\). Falsifier of a leftover-killer.
- Beatty packed / Christoffel / letter-extremal words are
  CycleMin-legal two-type necklaces with \(N_{\mathrm{cheap}}=2764\).
  Falsifier of “no closed two-type necklace exists.”
- Interleave `OOE`/`OE` has \(2764\) illegal `OE` starts at
  \(9/8\). Falsifier of “every two-type word is a legal necklace.”
- \(365\) ends \(12707\to 1196\); wrap attempts \(a\in\{1,2,3,5,12\}\)
  miss \(365\). Falsifier of an exact integer wrap on a realized
  cheap chain.

## Formalization

None. No `CyclicValley.lean`. Paper A is unchanged.
Do not formalize the sample table.

## Results

- **Cheap cap** — **EXACT — HUMAN PROOF**:
  \(N_{\mathrm{cheap}}\le 2764\) on two-type CycleMin necklaces.
- **Charge** — **COMPUTATIONALLY VERIFIED**
  (`cyclic_valley/summary.json`): RHS factor \(11.94\) over
  \(\theta\); Beatty height-walk \(1.30\cdot 10^{-4}\).
- **Wrap** — not a privileged extra tax; exact wrap does not close.
- **Small \(m\)** — independent packing strictly larger; \(0\)
  cyclic beats.
- **No leftover-killer.**

## Open questions

None from the cyclic valley necklace. Do not open a
branch-and-bound search, a \(K=11\) proof, or \(L=55293\).
The Section 5 state-distribution program stays **PARK**.

## Decision

**CLOSE**. The optimisation-model correction is real: on a
two-type CycleMin necklace the first valley is an `OE` landing
and \(N_{\mathrm{cheap}}\le N_{\mathrm{OE}}<o-e\). That is the
cyclic wrap-around, not a free path boundary. The charged RHS
and the Beatty height walk both stay above \(\theta\), inside
the slack in which one may already lose \(6532\) cheap starts.
Wrap-around is not an extra rotation-sensitive tax. No Paper A
edit, no ledger row, no Lean, no \(N_0\) raise, no search engine.

Best next question: none from the cyclic valley necklace.

## Publication assessment

Status: `ARCHIVED`. Laboratory negative knowledge on the
Section 5 independent-valley model; not a second manuscript
and not a Paper A edit.
