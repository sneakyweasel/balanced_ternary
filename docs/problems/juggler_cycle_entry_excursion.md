# Juggler CycleMin entry excursion

Status: **ARCHIVED**

Refinement of
[juggler_cycle_finance_cell_bridge.md](juggler_cycle_finance_cell_bridge.md)
and [juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md),
not a new paper. After realizable-prefix finance closed, this
phase asks whether the distinguished CycleMin cut — entry into
the minimum \(n\), then the excursion, then the return —
imposes a finance tax that the valley-only model throws away.

Not a halt theorem, not a last-even reopen, not an inverse-width
reopen, not a floor raise, and not a claim that every valley
must itself land at \(n\).

## Problem

A cycle has no canonical start, but a `CycleMin` representation
does: the minimum state \(n\) is distinguished, so the last
even step into \(n\) is a real boundary. Does enumerating those
entry excursions force a predecessor valley whose finance cost
sits a definite \(\delta\) above the relaxed OE / OOE classes,
or conflict with the closing edge of the \(L=25781\) packed
necklace?

## Exact statement

**Entry cell is the last-even cell with \(n^2\) removed
(KNOWN / COMPUTATIONALLY VERIFIED).**
The predecessor of odd \(n\) is even and lies in
\([n^2,(n+1)^2)\). Parity forbids \(x=n^2\), so
\(n^2+1\le x<(n+1)^2\) and \(x\) even. At \(n=10^6+1\) that
is \(10^6+1\) evens, first even \(n^2+1\), relative width
\(2\cdot10^{-6}\). This is
`cycle_last_even_ne_odd_sq`, not a new cell.

**The only CycleMin-legal entry run is `OE`
(COMPUTATIONALLY VERIFIED).**
At \(n=10^6+1\) there are \(33\) exact \(O^aE\) landings
with every state \(\ge n\), all of them \(a=1\). For
\(a\in\{2,3,4\}\) the real envelope
\(v\sim n^{2^{a+1}/3^a}\) sits below \(n\)
(\(n^{8/9}\approx 2.15\cdot 10^5\), \(n^{16/27}\approx 3.6\cdot 10^3\))
and the exact fibre is empty. The first \(a=2\) start
\(1000057\) has peak \(3.16\cdot 10^{13}>(n+1)^2\) and
lands at \(5623773\neq n\). This is \(F_2(v)>v\) plus the
\(\ge n\) tube, not a new emptiness.

**Cheapest entry valley is exactly `oe_start_min`
(COMPUTATIONALLY VERIFIED).**
The \(33\) entry valleys occupy
\([100000135,100000265]\). The left endpoint equals
`oe_start_min`\((n)\), and that valley itself realizes
\(100000135\xrightarrow{\mathrm{OE}}n\) with peak
\(1000002025000\in(n^2,(n+1)^2)\). The \(\ge n\) tube is
automatic (\(v\sim n^{4/3}\)). Relative span of the whole
entry set is \(1.3\cdot 10^{-6}\). Valley finance tax
versus the relaxed OE class is \(0\) at the cheap end and
at most \(7.4\cdot 10^{-16}\) at the dear end.

**Finance-optimal cheap valleys are not entry-compatible
(COMPUTATIONALLY VERIFIED).**
Neither \(n\) nor \(n+2\) lands at \(n\) under \(O^aE\)
for \(a\le 4\). The slogan “every valley of the extremizer
must be entry-compatible with \(n\)” is false: only the
unique last valley before the CycleMin cut has to enter
\(n\). Rotational invariance of the unlabeled cycle does
not reproduce the CycleMin boundary at every local minimum.

**Packed closing edge already ends `OE`
(COMPUTATIONALLY VERIFIED / KNOWN Sturmian).**
The Beatty packed word at \((L,o)=(25781,16266)\) ends
`(2,1),(1,1)` and has \(2764\) `OE` blocks. The forced
last circuit `OE` is the suffix it already has. There is
no closing-edge conflict. Terminal \((2,1)\) realized is
the closed cell-bridge fact.

**No leftover-killing \(\delta\) (COMPUTATIONALLY
VERIFIED).**
One entry tax \(7.4\cdot 10^{-16}\) sits inside slack
\(5.63\cdot 10^{-4}\). Even the false reading that charges
that tax to every one of the \(2764\) OE valleys is
\(2.1\cdot 10^{-12}\) and still inside slack.
`parity_excludes` / `budget_excludes` remain false.

The narrow return cell of relative width \(O(1/n)\) pulls
back under \(x\mapsto x^{3/2}\) to a relative \(O(1/n)\)
window around the already-budgeted scale \(n^{4/3}\). It
does not create a new valley scale.

No cycle of any length — not claimed.

## Current literature

- Last-even cell, \(x\neq n^2\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_last_even_interval`, `cycle_last_even_ne_odd_sq`)
- OE-start scale \(v\ge n^{4/3}\) —
  **EXACT — HUMAN PROOF**
  ([juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md))
- Cyclic valley necklace: wrap-around is an `OE` landing,
  \(N_{\mathrm{cheap}}\le N_{\mathrm{OE}}\) —
  **CLOSE** / cheap-cap **EXACT — HUMAN PROOF**, leftover-killer
  **REFUTED**
  ([juggler_cycle_cyclic_valley.md](juggler_cycle_cyclic_valley.md))
- Last circuit cannot be `OOE`; terminal \((2,1)\) realized —
  **CLOSE** / **REFUTED** as leftover-killer
  ([juggler_cycle_finance_cell_bridge.md](juggler_cycle_finance_cell_bridge.md))
- \(F_2(v)>v\); cheap-`OOE`; \(243<256\) —
  **EXACT — HUMAN PROOF** /
  leftover-killer **REFUTED**
  ([juggler_cycle_ordered_excursion.md](juggler_cycle_ordered_excursion.md))
- Realizable-prefix finance tax \(0\) —
  **CLOSE** / **REFUTED**
  ([juggler_cycle_realizable_finance.md](juggler_cycle_realizable_finance.md))
- Collatz-style financing —
  **known** (`simons-de-weger-2005-collatz-m-cycles`)
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a leftover-killing entry
tax; the entry excursion is a **REPARAMETERIZATION** of the
last-even cell plus `oe_start_min` plus \(F_2(v)>v\).

## Branch budget

```text
Mathematical target     Does the CycleMin entry excursion into n
                        force a finance tax δ above the relaxed
                        OE / OOE minimum, or a closing-edge
                        conflict the L=25781 packed necklace
                        cannot satisfy?
Novelty hypothesis      the distinguished cut (entry / excursion /
                        return) plus the ≥n tube is a boundary
                        condition the valley-only model drops
Falsifier               cheapest entry valley equals oe_start_min;
                        a≥2 with v≥n is empty by F2(v)>v; packed
                        word already ends OE; “all valleys enter n”
                        is false; tax inside slack
Existing machinery      last-even cell; compatible_oe_preimages;
                        run_preimages; excursion_map; oe_start_min;
                        packed_block_word; cell-bridge terminal
                        (2,1); F2(v)>v
Maximum Phase-0 scope   exact O^a E census at n=10^6+1 for a≤4;
                        finance cost vs oe_start_min; packed
                        suffix; valley-class compatibility. No
                        Lean, no Paper A, no N0 raise
Promotion criterion     a reusable δ that, charged at the unique
                        entry, kills 25781 at N0=10^6, and is not
                        an archived cell
Stop criterion          tax 0 or O(1/n) at the OE scale; a≥2 empty
                        by archived F2; no closing conflict
```

## Closed-bridge gates

Classify the entry tax before any follow-up. Do not reopen
last-even-not-square, empty terminal `OOE`, or inverse-width.

- **CLOSE** if the cheapest CycleMin-legal entry valley is
  `oe_start_min` (tax \(0\) at the finance OE class).
- **CLOSE** if every \(a\ge 2\) entry with \(v\ge n\) is empty
  by \(F_2(v)>v\) / envelope \(v<n\).
- **CLOSE** if the packed word already ends `OE` and the
  “all valleys enter \(n\)” reading is false.
- **PROMOTE** only if a uniform entry \(\delta\) exceeds
  packed-to-\(\theta\) slack and is not an archived cell.

Do **not** raise \(N_0\). Do **not** open \(L=55293\). Do
**not** edit Paper A.

## Explicitly out of Phase-0

A \(K=11\) proof, the \(1054k\) family, Fourier / residues /
\(Q\)-sections, a branch-and-bound engine, ledger row, Lean,
CLI, visualization.

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Last-even entry cell \(n^2+1\le x<(n+1)^2\), \(x\) even —
  **KNOWN** (`cycle_last_even_ne_odd_sq`)
- Exact \(O^aE\) fibre of \(n\) with tube \(\ge n\) —
  **COMPUTATIONALLY VERIFIED**; only \(a=1\), \(33\) valleys
  at \(n=10^6+1\)
- Envelope \(v\sim n^{2^{a+1}/3^a}\) versus \(v\ge n\) —
  **COMPUTATIONALLY VERIFIED**; \(a\ge 2\) lies below \(n\)
- Entry finance tax versus `oe_start_min` —
  **COMPUTATIONALLY VERIFIED**; \(0\) at the cheap end
- “Every finance valley enters \(n\)” —
  **REFUTED**; \(n\) and \(n+2\) do not enter
- Packed closing edge versus forced last circuit `OE` —
  **COMPUTATIONALLY VERIFIED**; no conflict
- Entry leftover-killer at \(L=25781\) —
  **REFUTED** (`juggler_cycle_entry_excursion`)
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_entry_excursion`
- Dataset: `data/research/juggler/cycle_finance/entry_excursion/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_entry_excursion.py`
- Window: \(n=10^6+1\); runs \(a\le 4\); six odds in
  \([10^6+1,10^6+2001]\) stride \(400\); packed suffix at
  \(L=25781\). Fast suite only. No CLI. No Lean. No \(N_0\)
  raise.

## Conjectures

`juggler_cycle_entry_excursion` — **REFUTED**.

## Counterexamples

- \(100000135=\mathrm{oe\_start\_min}(10^6+1)\) enters \(n\)
  by `OE` with peak \(1000002025000\). Falsifier of a
  strictly dearer entry scale.
- \(n\) and \(n+2\) do not enter \(n\). Falsifier of
  “every finance valley is entry-compatible.”
- First \(a=2\) start \(1000057\) peaks at
  \(3.16\cdot 10^{13}>(n+1)^2\) and lands at \(5623773\).
  Falsifier of CycleMin-legal `OOE` entry.
- Even \(2764\times 7.4\cdot 10^{-16}\) stays inside slack
  \(5.63\cdot 10^{-4}\). Falsifier of a leftover-killing
  \(\delta\).

## Formalization

None. No `EntryExcursion.lean`. Paper A is unchanged.
Do not formalize the sample table.

## Results

- **Entry cell** — **KNOWN**
  (`entry_excursion/summary.json`): `first_even=n^2+1`,
  `count=n`, `contains_n2=false`.
- **Only `OE`** — **COMPUTATIONALLY VERIFIED**.
  `only_oe_entry=true`; `deep_ge_n=0`.
- **Tax** — **COMPUTATIONALLY VERIFIED**.
  `tax_zero=true`; `min_v_over_oe=1`; `at_oe_scale=true`.
- **Closing** — packed `ends_oe=true`; `closing_conflict=false`.
- **Charge** — does not kill \(25781\) at the published floor.
- **No new leftover-killer.**

## Open questions

None from the entry excursion. Do not open a \(K=11\) proof
or \(L=55293\). The CycleMin cut is a real distinguished
boundary; it does not add a charge the valley-only model
missed.

## Decision

**CLOSE**. The entry excursion into a CycleMin \(n\) is the
already-budgeted `OE` cell at scale \(n^{4/3}\). The
narrowness of the return interval is real and pulls back to
a relative \(O(1/n)\) window around `oe_start_min`; the
cheapest occupant *is* `oe_start_min`. Deeper odd runs cannot
enter while staying \(\ge n\), which is \(F_2(v)>v\). The
packed necklace already ends `OE`. Requiring every finance
valley to enter \(n\) confuses rotational invariance of the
unlabeled cycle with the unique CycleMin cut. No Paper A
edit, no ledger row, no Lean, no \(N_0\) raise.

Best next question: none from the CycleMin entry excursion.

## Publication assessment

Status: `ARCHIVED`. Laboratory negative knowledge on a
CycleMin-boundary refinement; not a second manuscript and
not a Paper A edit.
