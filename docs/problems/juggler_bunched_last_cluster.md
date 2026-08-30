# Juggler bunched last-cluster leftover tails

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1. It is not a length-8 or length-9
census, not first-E transport at \(e\ge 4\), and not induction on
\(n\) or on the period.

## Problem

After the two-even families and gapped first-E transport, do the
seven bunched last-cluster leftovers \(O^a\) plus a fixed short
tail fire as prefix-cell tails for every expanding \(a\), with
\(N_0\) bounded independently of \(a\)?

## Exact statement

A leftover three-even `CycleMin` is even-terminating
\(O^aEO^bEO^cE\) with \(a\ge 2\) and \(c\in\{0,1\}\). First-E
transport already excludes the gapped cases \(b\ge 4\) (EE) and
\(b\ge 3\) (EOE). The bunched remainder is seven families

\[
O^a\texttt{EEE},\ 
O^a\texttt{EOEE},\ 
O^a\texttt{EOOEE},\ 
O^a\texttt{EOOOEE},\ 
O^a\texttt{EEOE},\ 
O^a\texttt{EOEOE},\ 
O^a\texttt{EOOEOE}.
\]

The prefix-cell tail is

\[
n^{3^a}>2^{e_a}Z(n,b,c)^{2^a},
\]

where \(e_a=\log_2(\mathrm{lowerDenom}(O^a))\) and \(Z\) is the
last-even / last-odd bound on \(T_{O^a}(n)\) through the fixed
tail. Phase 0 asks whether each family first fires at some
\(N_0(a)\), whether \(N_0(a)\) stays bounded, and whether there is
no `CycleWord` on \(2\le n<N_0(a)\). The `EEE` family is also
checked against the coarse cell \(z<(n+1)^8\) and cubing in \(a\).

`O^a`EEE is now Lean-excluded for every expanding \(a\ge 6\).
The other six bunched families remain computational. This is not
a halt theorem. There is no `no_cycle_word_length_eight` and no
`no_cycle_word_length_nine`.

## Current literature

- Uniform two-even leftover families —
  **EXACT — LEAN VERIFIED**.
- Gapped three-even `CycleMin`s —
  **EXACT — LEAN VERIFIED** (`no_cycleMin_gapped_three_even_ee`,
  `no_cycleMin_gapped_three_even_eoe`).
- Leftover `OOOOOOEEE` —
  **EXACT — LEAN VERIFIED**. Computational \(N_0=73\); Lean
  algebraic cutoff \(n\ge 128\). This is the \(a=6\) instance
  of the `EEE` family.
- Uniform bunched `O^a`EEE —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_three_even_eee`).
- Length-9 three-even leftovers —
  **COMPUTATIONALLY VERIFIED** as prefix-cell tails. Those nine
  words are the first expanding instance of each bunched family
  plus the two gapped \(a=2\) words.
- Prefix-OOO extra scale from \(n=3\) —
  **REFUTED**. That `CLOSE` is not reopened.

Project relationship: **extended**. This is the bunched remainder
after even-count steps (i) and (ii).

## Branch budget

```text
Mathematical target     Do the seven bunched last-cluster tails
                        fire for every large a, with N0 bounded in a?
Novelty hypothesis      Fixed mixed tail plus C_{O^a}; cutoffs drop
                        as a grows, as they did for two evens
Falsifier               A tail whose N0 grows with a, or never fires
Existing machinery      trailing-even / last-odd cells; denomBits;
                        OOOOOOEEE; first-E for the gapped complement
Maximum Phase-0 scope   N0(a) for the seven families; empty tables
                        below N0. No Lean, no length-8/9 census,
                        no e≥4 transport, no halt
Promotion criterion     All seven fire with N0 bounded and an
                        algebraic reason (n≤4 never; plateau at 5)
Stop criterion          A family that never fires; unbounded N0;
                        a census; e≥4 machinery
```

Phase 1 (this branch): Lean-exclude \(O^a\texttt{EEE}\) for every
\(a\ge 6\) by cubing the three-even cell. No other bunched
family, no length-8/9 census, no halt.

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- seven bunched tails, independent of length —
  **EXACT — HUMAN PROOF**
- first expanding \(a\) is \(6,5,4,3,5,4,3\) —
  **EXACT — HUMAN PROOF**
- prefix-cell tails fire at first-expanding
  \(N_0\in\{73,89,120,188,60,81,126\}\) —
  **COMPUTATIONALLY VERIFIED**
- \(N_0\) drops to 5 and stays there through \(a=20\) —
  **COMPUTATIONALLY VERIFIED**
- the shared comparison never holds for \(n\le 4\) —
  **COMPUTATIONALLY VERIFIED**
- `EEE` coarse cell \(n^{3^a}>2^{e_a}(n+1)^{2^{a+3}}\) cubes
  from \(a=6\) at \(n\ge 73\) —
  **COMPUTATIONALLY VERIFIED**; Lean uses the same cell at the
  algebraic cutoff \(n\ge 128\)
- `O^a`EEE is not a `CycleWord` for \(a\ge 6\), \(n\ge 2\) —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_three_even_eee`)
- no bunched family is a `CycleWord` on \(2\le n<N_0(a)\)
  for expanding \(a\le 20\) —
  **COMPUTATIONALLY VERIFIED**
- every three-even cycle word is impossible — not claimed
- no cycle of length eight or nine — not claimed
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.bunched_last_cluster`
- Records: [juggler_bunched_last_cluster.md](../research/juggler_bunched_last_cluster.md),
  [juggler_bunched_last_cluster.json](../research/juggler_bunched_last_cluster.json)
- Tests: `tests/research/juggler_sequence/test_bunched_last_cluster.py`
- The Research Engine control layer is not modified.
- No cycle-state search. No length-8 or length-9 census.
- `EEE` Lean is in `BunchedEEE.lean`. No Lean for the other
  six bunched families. No Paper A edit.

## Conjectures

None opened.

## Counterexamples

None to the seven tails or to the empty tables. The stronger
claims that remain false or unproved:

- “\(N_0\) tends to 2” — still **REFUTED**. The leading \(3^a\)
  coefficients force \(n>4\).
- “prefix-OOO extra scale from \(n=3\)” — still **REFUTED**.
- “first-E transport at \(e\ge 4\) reduces bunched last clusters”
  — not claimed. A bunched last cluster is exactly the remainder
  that last-cluster two-even transport does not take.
- “every bunched leftover is Lean-excluded” — not claimed.
  Only `O^a`EEE is Lean; the other six families remain
  computational.
- “every three-even leftover is Lean-excluded” — not claimed.
- no cycle of length eight or nine — not claimed.

## Formalization

`formal/Problems/Juggler/BunchedEEE.lean` excludes the `EEE`
family: `no_cycle_word_three_even_eee`. Large \(n\) cubes the
three-even cell from `OOOOOOEEE` at \(n\ge 128\). Below \(128\),
\(a=6\) is the existing table and \(a\ge 7\) is seven-odd. There
is no `no_cycle_word_bunched` and no `no_cycleMin_bunched`.
`SmallCycleCensus.lean` still assembles only through length
seven. No `no_cycle_word_length_eight`. No
`no_cycle_word_length_nine`. No `sorry`. No halt theorem. Paper A
is not edited.

## Results

Classification **BUNCHED_LAST_CLUSTER_GREEN**.

The seven bunched last-cluster leftovers are one type: a fixed
short tail against \(C_{O^a}\). All seven fire at the first
expanding \(a\), with largest cutoff \(N_0=188\) on
`OOOEOOOEE`. Cutoffs then drop to the same \(n=5\) plateau as the
two-even families. Lean now excludes `O^a`EEE for every
\(a\ge 6\) and \(n\ge 2\): the three-even cell cubes from
`OOOOOOEEE` at \(n\ge 128\); below \(128\) the argument is the
\(a=6\) table or seven-odd. The other six families remain
computational. Tables below each cutoff are empty through
\(a=20\).

This is a one-family Lean exclusion, not a length-9 census and
not a no-cycles theorem.

## Open questions

Lean-exclude the next bunched family (`O^a`EOEE), or a uniform
mixed-tail cell for the remaining six. Do not assemble
`no_cycle_word_length_eight` or `no_cycle_word_length_nine`.
Do not open first-E at \(e\ge 4\) as part of that phase. Do not
claim halt.

## Decision

**PROMOTE**. `O^a`EEE is now one Lean type, cubed from the
existing `OOOOOOEEE` comparison. The other six bunched families
are still computational.

Best next question: Lean-exclude `O^a`EOEE, or find a uniform
mixed-tail cell for the remaining six families.

## Publication assessment

Status: `EXPLORATORY`.

A one-family Lean exclusion inside the bunched remainder, not a
paper candidate and not a Juggler totality result. Paper A is not
edited.
