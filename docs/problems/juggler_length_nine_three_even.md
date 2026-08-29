# Juggler length-9 three-even leftovers

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1. It does not reopen Paper B densities,
does not start induction on \(n\) or on the period, and is not a
length-9 census.

## Problem

What argument excludes the even-terminating expanding length-9 words
that have three even letters and survive the Paper A filters — the
words that the two leftover families \(O^{k-2}EE\) and \(O^{k-3}EOE\)
no longer cover?

## Exact statement

A length-9 word is formally expanding if and only if it has at least
six odd letters (\(2^9=512<729=3^6\)). Every mixed cycle word rotates
to an even-terminating orientation. Every even-terminating three-even
word is uniquely

\[
O^aEO^bEO^cE,\qquad a+b+c=6.
\]

The suffix after the last internal even letter is always \(O^c\). It
never contains \(E\). Last-internal bootstrap therefore still applies
exactly when \(c\ge 2\). The leftover orientations are the nine words
with \(a\ge 2\) and \(c\in\{0,1\}\):

\[
\begin{align*}
&OOOOOOEEE,\ OOOOOEOEE,\ OOOOOEEOE,\\
&OOOOEOOEE,\ OOOOEOEOE,\\
&OOOEOOOEE,\ OOOEOOEOE,\\
&OOEOOOOEE,\ OOEOOOEOE.
\end{align*}
\]

Phase 0 asks whether each of these satisfies an odd-prefix cell tail

\[
n^{3^a}>C_{O^a}\,Z^{2^a}
\]

for all \(n\ge N_0\), where \(Z\) is a last-even / last-odd upper bound
on \(T_{O^a}(n)\) through the mixed tail \(EO^bEO^cE\), and whether
there is no `CycleWord` realization on \(2\le n<N_0\).

This is not a Lean census and not a halt theorem.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Small-cycle census (Paper A Theorem 3.6) —
  **EXACT — LEAN VERIFIED**. No cycle word of length at most six.
- Internal-E bootstrap —
  **EXACT — LEAN VERIFIED**. Last-internal next-square suffix.
- Leftover length-six orientations (Lemma 3.5) —
  **EXACT — LEAN VERIFIED**. Finite table plus
  \(n^{81}>2^{130}(n+1)^{64}\).
- Length-7 leftover inventory and census —
  **EXACT — LEAN VERIFIED** (`no_cycle_word_oooooee`,
  `no_cycle_word_ooooeoe`, `no_cycle_word_length_le_seven`).
  Length eight is open. Not reopened.
- Prefix-OOO extra scale from \(n=3\) —
  **REFUTED**. That `CLOSE` is not reopened.

Project relationship: **extended**. The first length at which an
expanding even-terminating word can have three evens.

## Branch budget

```text
Mathematical target     What argument excludes the length-9 three-even
                        leftover CycleWords?
Novelty hypothesis      Last-internal suffix is always O^c; leftovers
                        are nine words O^a E O^b E O^c E; odd-prefix
                        plus mixed-tail cells replace the two-even
                        families
Falsifier               A leftover whose prefix-cell tail never fires,
                        or a CycleWord realization below N0
Existing machinery      expansion; rotation; odd-run; OO/OOO/odd-run
                        thresholds; CycleMin; internal-E bootstrap;
                        Lemma 3.5 last-even / last-odd cells;
                        lowerDenom
Maximum Phase-0 scope   inventory + prefix-cell N0 + finite table on
                        the nine leftovers. No Lean, no Paper A edit,
                        no length 10, no four-even, no halt, no cycle
                        search, no CLI
Promotion criterion     A named argument that computationally excludes
                        all nine leftovers, not a rewrite of induction
Stop criterion          A leftover whose tail never fires; a table hit;
                        machinery gravity (census engine, length 10,
                        Paper A, Lean)
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- even-terminating expanding length-9 family has 37 words (1 odd-run,
  8 two-even, 28 three-even) —
  **COMPUTATIONALLY VERIFIED**
- last-internal suffix of a three-even even-terminating word is always
  \(O^c\) —
  **COMPUTATIONALLY VERIFIED**
- six three-even words with \(c\ge 2\) and \(a\ge 2\) are last-internal
  bootstrap shapes; \(n=3,5\) fail by parity —
  **COMPUTATIONALLY VERIFIED**
- leftovers are exactly the nine words above —
  **COMPUTATIONALLY VERIFIED**
- for \(a=2\) the remainder after the first \(E\) is a Lemma 3.5 word
  (`OOOOEE` / `OOOEOE`) —
  **COMPUTATIONALLY VERIFIED**
- odd-prefix cell tails fire at
  \(N_0\in\{8,60,81,89,120,126,188,250,374\}\) —
  **COMPUTATIONALLY VERIFIED**
- no leftover is a `CycleWord` on \(2\le n<N_0\) —
  **COMPUTATIONALLY VERIFIED**
- `OOOEOOOEE` is realized at \(n=183\) but returns \(1664\), not \(183\) —
  **COMPUTATIONALLY VERIFIED**
- every length-9 cycle word is impossible — not claimed
- cycles of length ten or more are impossible — not claimed
- global halt — not claimed
- induction on \(n\) or on the period excludes cycles — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_length_nine`
- Records: [juggler_cycle_length_nine.md](../research/juggler_cycle_length_nine.md),
  [juggler_cycle_length_nine.json](../research/juggler_cycle_length_nine.json)
- Tests: `tests/research/juggler_sequence/test_cycle_length_nine.py`
- The Research Engine control layer is not modified.
- No cycle-state search. No length 10. No four-even programme.
- No Lean file.

## Conjectures

None opened.

## Counterexamples

None to the inventory or to the nine leftover tails. The stronger
claims that remain false or unproved:

- “the last two \(E\)s can be separated by a suffix containing \(E\)” —
  false for an even-terminating word; the last-internal suffix is
  \(O^c\).
- “induction on the period reduces length 9 to length 8” — still
  false. A period-9 cycle does not produce a period-\(\le 8\) cycle.
  The case \(T_{O^aE}(n)=n\) is divisor reduction (\(a+1\mid 9\)), not
  an inductive step on \(k\).
- “a general no-cycle induction on \(n\)” — still the census of
  odd-to-odd cycle minima.
- “every length-9 word is Lean-excluded” — not claimed.

## Formalization

None added. `SmallCycleCensus.lean` already assembles length seven
(`no_cycle_word_length_le_seven`) and records that length eight is
open. No `no_cycle_word_length_nine`. No `sorry`. No halt theorem.
No `CycleSearch`. FloorPower, Progress, and Minimal are not
rewritten.

A later Lean phase, if opened, would follow `LeftoverCycles.lean`
on the nine tails, starting with `OOOOOOEEE` at \(N_0=8\). That is
not this phase.

## Results

Classification **THREE_EVEN_PREFIX_CELL_GREEN**, with secondary
**FIRST_E_TRANSPORT_FOR_A2** and
**LAST_INTERNAL_SUFFIX_ALWAYS_O_RUN**.

The 28 three-even words split as: 7 start \(E\), 6 start \(OE\), 6
last-internal bootstrap, 9 leftovers. The last-internal suffix never
contains \(E\), so “bootstrap does not fire because the suffix is
`OE…`” is a first-\(E\) remark, not a last-internal one.

The argument that covers the nine leftovers is the Lemma 3.5 method
with the extra even kept in the cell chain, not in `lowerDenom`.
Naive `cycle_pow_le_lowerDenom` on the full word inflates the
constant through the internal \(E\)s (\(N_0\) in the thousands). The
refined comparison uses \(C_{O^a}\) only and bounds \(T_{O^a}(n)\)
by last-even / last-odd cells through \(EO^bEO^cE\). All nine tails
fire, with largest cutoff \(N_0=374\) on `OOEOOOOEE`, and the exact
tables below the cutoffs have zero returns.

For the two \(a=2\) leftovers the remainder after the first \(E\) is
exactly a length-6 leftover. On a cycle minimum that remainder starts
at \(y\ge n\), so Lemma 3.5 transports at \(256\). The prefix-cell
bound already excludes those two words as `CycleWord`, so the
transport is a CycleMin simplification, not a second method.

This is a computational exclusion of the nine leftover `CycleWord`s,
not a Lean census and not a no-cycles theorem.

## Open questions

Lean-exclude the nine three-even leftovers by the prefix-cell tails,
starting with `OOOOOOEEE` at \(N_0=8\). Do not open length 10 or
four-even words automatically. A uniform two-even theorem for
lengths 6–8 remains a later distill. Do not start an O-terminating
`CycleWord` programme. Do not claim halt.

## Decision

**PROMOTE**. The three-even gap is a finite leftover list with a
named exclusion path: odd-prefix LowerPowerBound against a mixed-tail
cell bound. All nine tails fire and the finite tables are empty.
That is the Lemma 3.5 method with one extra even, not induction on
\(n\) or on the period. A length-9 Lean census is not automatic.

Best next question: Lean-exclude `CycleWord` on `OOOOOOEEE` by the
prefix-cell tail at \(N_0=8\), then the remaining eight leftovers.

## Publication assessment

Status: `EXPLORATORY`.

A Phase-0 inventory and leftover-tail computation, not a paper
candidate and not a Juggler totality result. Paper A is not edited.
