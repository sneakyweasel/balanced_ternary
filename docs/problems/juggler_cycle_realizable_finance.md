# Juggler realizable-prefix finance

Status: **ARCHIVED**

Refinement of
[juggler_cycle_conditioned_closure.md](juggler_cycle_conditioned_closure.md),
[juggler_cycle_extremizer_discrepancy.md](juggler_cycle_extremizer_discrepancy.md),
and [juggler_cycle_inverse_width.md](juggler_cycle_inverse_width.md),
not a new paper. After inverse-width closed as a cell
reparameterization, this phase asks whether *finite realizability
of a finance-extremal prefix* produces an extra defect large
enough to spend the packed-to-\(\theta\) slack at \(L=25781\).

Not a \(K\le 20\) proof, not a follow recensus, not an
inverse-width reopen, not a branch-and-bound engine, not a floor
raise, and not a halt theorem.

## Problem

A two-type word at \((L,o)=(25781,16266)\) maximises the
length-only finance bound, but an integer orbit may follow only
a short prefix. Does that gap

\[
\text{finance extremality}+\text{finite realizability}
\Longrightarrow\text{extra defect}
\]

exceed the slack in which one may already lose \(6532\) of
\(6751\) cheap `OOE` starts, or deepen every `OE`?

## Exact statement

**Packed-to-\(\theta\) slack is unchanged (KNOWN /
COMPUTATIONALLY VERIFIED).**
At \(n=10^6+1\), \(P/\theta\approx 23.12\), margin
\(5.63\cdot 10^{-4}\). One may lose \(6532\) cheap `OOE`
starts. Deepening every `OE` still leaves packed \(>\theta\).
This is the conditioned-closure table, not a new slack.

**Realized-prefix finance tax is \(0\) at the floor
(COMPUTATIONALLY VERIFIED).**
On the Beatty packed, bunched, \(OE\)-front, interleaved, and
extra-odd prefixes, every witness \(n\in\{10^6+1,1000057\}\)
has \(|S_{\mathrm{env}}-S_{\mathrm{real}}|<10^{-12}\) along
the realized head. \(1000057\) completes two prescribed
`OOE` with tax \(-2\cdot 10^{-15}\). There is nothing to
charge in the length-only sum.

**Local \(K\) is not a global cheap-`OOE` cap
(EXACT — HUMAN PROOF as a reading, not a theorem).**
If completed `OOE` blocks from one start capped the cycle
count, \(365\) (four blocks) and \(1000057\) (two) would imply
a loss of \(6747\)--\(6749>6532\) and would kill \(25781\).
That implication is false: later valleys can restart `OOE`.
Local follow forbids a *particular necklace from \(n\)*, not
the global run-type packing.

**Forced first-block deviations sit inside slack
(COMPUTATIONALLY VERIFIED).**
CycleMin two-type words start `OOE`. The realized head then
dies after one or two blocks — the archived cheap-`OOE` /
\(243<256\) events. At most two first-block deviations, not
\(6532\).

**Banning every two-type word would not kill \(25781\)
(COMPUTATIONALLY VERIFIED).**
Even the ideal theorem “no two-type word is fully realizable”
drops into the deepen-all class, which remains above
\(\theta\). Finite realizability of the extremizer is not a
stronger leftover-killer than conditioned closure.

No cycle of any length — not claimed. \(K\le 20\) is not proved.

## Current literature

- Packed-to-\(\theta\) slack, \(6532\) lost cheap `OOE`,
  deepen-all still legal —
  **CLOSE**
  ([juggler_cycle_conditioned_closure.md](juggler_cycle_conditioned_closure.md))
- Realized `OOE` hits the integer envelope; \(\Delta_{\mathrm{fin}}\)
  uncorrelated with follow depth —
  **CLOSE** / **REFUTED**
  ([juggler_cycle_extremizer_discrepancy.md](juggler_cycle_extremizer_discrepancy.md))
- Inverse-tube width —
  **CLOSE** / **REFUTED**
  ([juggler_cycle_inverse_width.md](juggler_cycle_inverse_width.md))
- Cheap-`OOE` adjacency; two-block \(243<256\) —
  **EXACT — HUMAN PROOF** /
  leftover-killer **REFUTED**
  ([juggler_cycle_ordered_excursion.md](juggler_cycle_ordered_excursion.md))
- Prescribed-word follow \(\le 11\) at the floor —
  **CLOSE**
  ([juggler_cycle_almost_search.md](juggler_cycle_almost_search.md))
- Collatz-style financing —
  **known** (`simons-de-weger-2005-collatz-m-cycles`)
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a leftover-killer; the
bridge is a reparameterization of slack plus archived first
blocks.

## Branch budget

```text
Mathematical target     Does finite realizability of near-extremal
                        prefixes force a finance tax larger than
                        the P-θ slack (6532 lost cheap OOE /
                        deepen-all) already computed?
Novelty hypothesis      finance extremality + finite realizability
                        ⇒ extra defect that is not 1/(x log x)
Falsifier               prefix tax is 0; implied loss ≤ 6532;
                        or the only killing reading is the false
                        implication “local K caps global OOE”
Existing machinery      budget_sum_terms, Δ_fin, lose_cheap_cost,
                        deficit_row, follow_word, envelope tax 0
Maximum Phase-0 scope   slack vs realized-prefix tax vs false
                        implication; no B&B, no Pareto CLI, no Lean
Promotion criterion     a per-block tax that exceeds slack and
                        is not an archived first-block cell
Stop criterion          tax 0 or inside slack; tautology k<L;
                        or K≤20 recensus
```

## Closed-bridge gates

- **CLOSE** if the prefix tax is \(0\) at the published floor.
- **CLOSE** if the only killing arithmetic is “local \(K\) caps
  global cheap `OOE`.”
- **CLOSE** if even a ban on every two-type word stays inside
  deepen-all.
- **PROMOTE** only if a realizability tax exceeds \(P-\theta\)
  and is not an archived first-block cell.

Do **not** prove \(K\le 20\). Do **not** build a branch-and-bound
search. Do **not** raise \(N_0\). Do **not** open \(L=55293\).
Do **not** edit Paper A.

## Explicitly out of Phase-0

A Pareto engine, inverse-fibre census, \(K=11\) proof, the
\(1054k\) family, Fourier / residues / \(Q\)-sections, ledger
row, Lean, CLI, visualization.

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Realized-prefix \(S_{\mathrm{env}}-S_{\mathrm{real}}\) —
  **COMPUTATIONALLY VERIFIED**; \(0\) at \(n\ge 10^6\)
- Local completed `OOE` as a global cap —
  **REFUTED** as a leftover-killer reading
- Forced first-block deviations —
  **COMPUTATIONALLY VERIFIED**; at most \(2\ll 6532\)
- “No two-type cycle” as a leftover-killer —
  **REFUTED**; deepen-all remains above \(\theta\)
- Inverse-width contraction —
  archived; not reopened
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_realizable_finance`
- Dataset: `data/research/juggler/cycle_finance/realizable_finance/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_realizable_finance.py`
- Window: witnesses \(\{365,10^6+1,1000057\}\); five near-extremal
  words; slack from `deficit_row`. Fast suite only. No CLI.
  No Lean. No \(N_0\) raise.

## Conjectures

`juggler_cycle_realizable_finance` — **REFUTED**.

## Counterexamples

- \(1000057\) completes two packed / bunched `OOE` with prefix
  tax \(-2\cdot 10^{-15}\).
- Treating those two blocks as a global cap would lose \(6749\)
  cheap starts and kill \(25781\); later valleys may restart
  `OOE`, so the reading is false.
- Deepen-all still has packed \(>\theta\)
  (`deepen_all_still_above_theta=true`).

## Formalization

None. No `RealizableFinance.lean`. Paper A is unchanged.
Do not formalize the sample table.

## Results

- **Slack** — **KNOWN** (`conditioned_closure`):
  \(P/\theta\approx 23.12\), \(k_{\mathrm{lose}}=6532\).
- **Prefix tax** — **COMPUTATIONALLY VERIFIED**:
  `prefix_tax_zero=true` on floor witnesses.
- **False implication** — recorded, not charged.
- **Charge** — does not kill \(25781\) at the published floor.
- **No leftover-killer.**

## Open questions

None from realizable-prefix finance. Do not open a
branch-and-bound Pareto search, a \(K=11\) proof, or
\(L=55293\).

## Decision

**CLOSE**. The missing bridge was supposed to be extra defect
from “the finance extremizer cannot persist.” Along every
realized near-extremal head at the floor the envelope tax is
\(0\). The only arithmetic that exceeds slack is the false
identification of local follow depth with the global cheap-`OOE`
count. Even a theorem that no two-type word is fully realizable
stays inside the deepen-all margin already computed. No Paper A
edit, no ledger row, no Lean, no \(N_0\) raise, no search engine.

Best next question: none from realizable-prefix finance.

## Publication assessment

Status: `ARCHIVED`. Laboratory negative knowledge on a finance
refinement; not a second manuscript and not a Paper A edit.
