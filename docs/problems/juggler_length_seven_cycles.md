# Juggler length-7 cycle-word inventory

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1. It does not reopen Paper B densities
and does not start a general no-cycle theorem.

## Problem

Do the Paper A cycle filters, together with the leftover-tail method of
Lemma 3.5, exclude every even-terminating expanding length-7 word as a
`CycleWord` for \(n\ge 2\)?

## Exact statement

A length-7 word is formally expanding if and only if it has at least
five odd letters (\(2^7=128<243=3^5\)). Every mixed cycle word rotates
to an even-terminating orientation. The even-terminating expanding
candidates are exactly

\[
OOOOOOE,\ 
EOOOOOE,\ 
OEOOOOE,\ 
OOEOOOE,\ 
OOOEOOE,\ 
OOOOEOE,\ 
OOOOOEE.
\]

Phase 0 asks which of these survive the existing filters, and whether
the two leftover orientations \(OOOOOEE\) and \(OOOOEOE\) satisfy a
Lemma 3.5 tail

\[
n^{243}>2^{422}(n+1)^{128}
\]

for all \(n\ge N_0\), with no `CycleWord` realization on
\(2\le n<N_0\).

This is not a Lean census and not a halt theorem.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Small-cycle census (Paper A Theorem 3.6) —
  **EXACT — LEAN VERIFIED**. No cycle word of length at most six.
  Length seven was the stated boundary.
- Internal-E bootstrap —
  **EXACT — LEAN VERIFIED**. Length-6 leftovers were `OOOEOE` and
  `OOOOEE`.
- Leftover length-six orientations —
  **EXACT — LEAN VERIFIED**. Finite table below 256 plus
  \(n^{81}>2^{130}(n+1)^{64}\).
- Prefix-OOO extra scale from \(n=3\) —
  **REFUTED**. That `CLOSE` is not reopened.
- Paper B length-7 contracting splits `OOEOOEE` / `OOOEOEE` —
  withdrawn density claims. Not this branch.

Project relationship: **extended**. The first open length after the
small-cycle census.

## Branch budget

```text
Mathematical target     Which even-terminating expanding length-7 words
                        survive the Paper A filters, and do the two
                        leftover tails exclude CycleWord for all n≥2?
Novelty hypothesis      Length 7 is the same two-even type as length 6;
                        bootstrap kills the OO/OOO-suffix pair; the
                        leftover-tail method of Lemma 3.5 kills
                        OOOOOEE and OOOOEOE.
Falsifier               A leftover whose tail comparison never fires,
                        or a third leftover shape the filters miss.
Existing machinery      formal expansion; rotation to even-terminating;
                        odd-run; OO/OOO thresholds; CycleMin barriers;
                        no_cycleMin_internal_even_threshold;
                        lowerDenom / last-even cell; leftover finite
                        table + tail (LeftoverCycles.lean).
Maximum Phase-0 scope   One probe: inventory + leftover-tail cutoffs
                        + exact CycleWord check on 2≤n<N0 for the two
                        leftovers only. No Lean, no Paper A edit, no
                        length 8/9, no halt, no cycle search, no CLI.
Promotion criterion     Both leftovers excluded by tail+finite check,
                        or a named leftover that is not a rewrite of
                        a closed length-6 identity.
Stop criterion          Inventory is only reparameterization with no
                        exclusion path; tail fails; machinery gravity
                        (census engine, length-9, Paper B).
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- even-terminating expanding length-7 family is the seven words above —
  **COMPUTATIONALLY VERIFIED**
- `OOOOOOE` is the odd-run case of Lemma 3.4(v) —
  **OBSERVATION** (existing Lean theorem applies; not re-proved)
- `OOEOOOE` / `OOOEOOE` are internal-E bootstrap shapes; \(n=3\) fails
  by parity —
  **COMPUTATIONALLY VERIFIED**
- `EOOOOOE` rotates onto `OOOOOEE`; `OEOOOOE` is not a `CycleMin` —
  **OBSERVATION**
- leftovers are exactly `OOOOOEE` and `OOOOEOE` —
  **COMPUTATIONALLY VERIFIED**
- `lowerDenom(OOOOO)=2^{422}` and the tail
  \(n^{243}>2^{422}(n+1)^{128}\) for \(n\ge 14\) —
  **COMPUTATIONALLY VERIFIED**
- neither leftover is a `CycleWord` on \(2\le n<14\) (neither is even
  realized) —
  **COMPUTATIONALLY VERIFIED**
- length-8 is the same two-even type; length 9 is the first
  three-even length —
  **OBSERVATION** (not implemented)
- every length-7 cycle word is impossible —
  not claimed in Lean
- cycles of length eight or more are impossible — not claimed
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_length_seven`
- Records: [juggler_cycle_length_seven.md](../research/juggler_cycle_length_seven.md),
  [juggler_cycle_length_seven.json](../research/juggler_cycle_length_seven.json)
- Tests: `tests/research/juggler_sequence/test_cycle_length_seven.py`
- The Research Engine control layer is not modified.
- No cycle-state search. No length 8. No O-terminating programme.
- No Lean file.

## Conjectures

None opened.

## Counterexamples

None to the inventory or to the two leftover tails. The stronger
claims that remain false or unproved:

- “`LowerPowerBound` extra scale from \(n=3\) excludes the leftovers”
  — still the closed prefix-OOO branch.
- “every length-7 word is Lean-excluded” — not claimed.
- “a uniform defect tax excludes length 7” — still false; slack
  tends to 0.

## Formalization

None added. `SmallCycleCensus.lean` still records that length seven
is open. No `no_cycle_word_length_seven`. No `sorry`. No halt
theorem. No `CycleSearch`. No `PowerBoundEq` attack. No
`PowerHeight`. FloorPower, Progress, and Minimal are not rewritten.

A later Lean phase, if opened, would follow
`LeftoverCycles.lean`: isolate a `native_decide` table for
\(2\le n<14\) and prove the tail \(n^{243}>2^{422}(n+1)^{128}\) for
\(n\ge 14\), then assemble `no_cycle_word_length_seven`. That is not
this phase.

## Results

Classification **LENGTH_SEVEN_LEFTOVER_TAIL_GREEN**, with secondary
**TWO_EVEN_TYPE_THROUGH_EIGHT**.

The seven even-terminating expanding words are exactly the predicted
family. Odd-run and internal-E bootstrap cover five of them, up to
rotation. The two leftovers are the length-7 members of the same
families as `OOOOEE` and `OOOEOE`. Both die by the refined tail at
cutoff \(N_0=14\), and the exact tables on \(2\le n<14\) have zero
realizations and zero returns. The naive `OOOOEOE` comparison
\(n^{243}>2^{550}(n+1)^{128}\) also fires, at \(N_0=29\).

This is a computational exclusion of the two leftover `CycleWord`s,
not a Lean census.

## Open questions

Lean-exclude `OOOOOEE` and `OOOOEOE` by the \(N_0=14\) tail, then
assemble a length-7 census. Do not open length 8 automatically.
Length 8 is the same two-even type; length 9 is the first three-even
length. Do not start an O-terminating `CycleWord` programme. Do not
claim halt.

## Decision

**PROMOTE**. The inventory is the length-6 geometry with one extra
odd letter, not a rewrite without an exclusion path: both leftover
tails fire at \(N_0=14\) and the finite tables are empty. That is
the Lemma 3.5 method reaching the first open length. A later Lean
assembly is justified and is not automatic. This is not a halt
theorem and not a length-8 programme.

Best next question: Lean-exclude `CycleWord` on `OOOOOEE` and
`OOOOEOE` by the tail \(n^{243}>2^{422}(n+1)^{128}\) for \(n\ge 14\),
then assemble `no_cycle_word_length_seven`.

## Publication assessment

Status: `EXPLORATORY`.

A Phase-0 inventory and leftover-tail computation, not a paper
candidate and not a Juggler totality result. Paper A is not edited.
