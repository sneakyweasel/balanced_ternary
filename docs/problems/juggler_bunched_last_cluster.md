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

`O^a`EEE, `O^a`EOEE, and `O^a`EOOEE are now Lean-excluded. A
uniform coarse \((n+1)^K\) cell for all remaining bunched
families is **REFUTED**. The other four bunched families remain
computational. This is not a halt theorem. There is no
`no_cycle_word_length_eight` and no `no_cycle_word_length_nine`.

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
- Uniform bunched `O^a`EOEE —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_three_even_eoee`).
- Uniform bunched `O^a`EOOEE —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_three_even_eooee`).
  The \(K=4\) cell is the shared two-even tail at \(n\ge 256\).
- Uniform coarse \((n+1)^K\) cell for all remaining
  bunched families —
  **REFUTED**. At the first expanding \(a\), \(K\cdot 2^a\ge 3^a\)
  for `EOOOEE`, `EEOE`, `EOEOE`, and `EOOEOE`.
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

Phase 1: Lean-exclude \(O^a\texttt{EEE}\) for every \(a\ge 6\).

Phase 1c (this branch): Lean-exclude \(O^a\texttt{EOOEE}\) for
every \(a\ge 4\) by \(z<(n+1)^4\) plus the shared two-even
tail. No other bunched family, no length-8/9 census, no halt.

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
- `EOEE` coarse cell \(n^{3^a}>2^{e_a}(n+1)^{6\cdot 2^a}\) cubes
  from \(a=5\) at \(n\ge 314\); \(z<(n+1)^6\) for \(n\ge 4\) —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_three_even_eoee`)
- `EOOEE` coarse cell \(n^{3^a}>2^{e_a}(n+1)^{4\cdot 2^a}\) is
  the shared two-even tail; \(z<(n+1)^4\) for \(n\ge 32\) —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_three_even_eooee`)
- a uniform coarse \((n+1)^K\) cell for all six remaining
  families — **REFUTED**
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
- `EEE` Lean is in `BunchedEEE.lean`. `EOEE` Lean is in
  `BunchedEOEE.lean`. `EOOEE` Lean is in
  `BunchedEOOEE.lean`. No Lean for the other four bunched
  families. Paper A records Theorems 3.14--3.16.

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
- “a uniform coarse \((n+1)^K\) cell excludes all six remaining
  bunched families” — **REFUTED**. The first-expanding exponent
  \(K\cdot 2^a\) meets or beats \(3^a\) on `EOOOEE`, `EEOE`,
  `EOEOE`, and `EOOEOE`.
- “every bunched leftover is Lean-excluded” — not claimed.
  Only `O^a`EEE, `O^a`EOEE, and `O^a`EOOEE are Lean; the other
  four families remain computational.
- “every three-even leftover is Lean-excluded” — not claimed.
- no cycle of length eight or nine — not claimed.

## Formalization

`formal/Problems/Juggler/BunchedEEE.lean` excludes the `EEE`
family: `no_cycle_word_three_even_eee`.
`formal/Problems/Juggler/BunchedEOEE.lean` excludes the `EOEE`
family: `no_cycle_word_three_even_eoee`. Large \(n\) at \(a=5\)
is the mixed cell \(z<(n+1)^6\) against \(C_{O^a}\) at
\(n\ge 314\); \(a=6\) already fires at \(n\ge 16\). Below those
cutoffs the argument is two tables and seven-odd.
`formal/Problems/Juggler/BunchedEOOEE.lean` excludes the `EOOEE`
family: `no_cycle_word_three_even_eooee`. The mixed cell
\(z<(n+1)^4\) for \(n\ge 32\) reduces to the shared two-even
tail at \(n\ge 256\). There is no
`no_cycle_word_bunched` and no `no_cycleMin_bunched`.
`SmallCycleCensus.lean` still assembles only through length
seven. No `no_cycle_word_length_eight`. No
`no_cycle_word_length_nine`. No `sorry`. No halt theorem.
Paper A records Theorems 3.14--3.16.

## Results

Classification **BUNCHED_LAST_CLUSTER_GREEN**.

The seven bunched last-cluster leftovers are one type: a fixed
short tail against \(C_{O^a}\). All seven fire at the first
expanding \(a\), with largest cutoff \(N_0=188\) on
`OOOEOOOEE`. Lean now excludes `O^a`EEE for every \(a\ge 6\),
`O^a`EOEE for every \(a\ge 5\), and `O^a`EOOEE for every
\(a\ge 4\). A uniform coarse \((n+1)^K\) cell for the remaining
families is **REFUTED**. The other four families remain
computational on the tight prefix-cell \(Z\). Tables below each
cutoff are empty through \(a=20\).

This is a three-family Lean exclusion, not a length-9 census and
not a no-cycles theorem.

## Open questions

Lean-exclude the next bunched family whose coarse exponent is
possible, or Lean the tight \(Z\) bound for a family whose coarse
exponent is impossible. Do not assemble
`no_cycle_word_length_eight` or `no_cycle_word_length_nine`. Do
not open first-E at \(e\ge 4\). Do not claim halt.

## Decision

**PROMOTE**. `O^a`EOOEE is now one Lean type: the cell
\(z<(n+1)^4\) reduces to the two-even tail. A uniform coarse
\(K\) for all remaining bunched families stays **REFUTED**. Four
families stay computational.

Best next question: Lean-exclude `O^a`EOOOEE, or a tight-\(Z\)
argument for a family whose coarse exponent is impossible.

## Publication assessment

Status: `EXPLORATORY`.

A three-family Lean exclusion inside the bunched remainder,
recorded in Paper A as Theorems 3.14--3.16, not a length-9
census and not a Juggler totality result.
