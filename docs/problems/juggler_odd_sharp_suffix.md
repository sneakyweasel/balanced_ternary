# Juggler odd-start sharp even-tower suffixes

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1.

## Problem

Can an odd first defect feed an arbitrarily deep exact even tower, or
is the sharp family \(OE^s\) bounded?

## Exact statement

For odd \(n\) that is not a square, does

\[
T(n)=a^{2^s}
\]

occur for unbounded \(s\ge 2\)? Equivalently, can an odd cube lie in

\[
a^{2^{s+1}}\le n^3<(a^{2^s}+1)^2?
\]

This is a local Diophantine question. It is not a termination theorem.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Phase-20 (`juggler_defect_sharpness`): sharpness iff exact even
  suffix **EXACT — LEAN VERIFIED**. **extended** here by asking how
  deep that suffix can be after an odd first defect.

## Branch budget

```text
Mathematical target     Can odd n have T(n)=a^{2^s} for unbounded s
                        (sharp OE^s)?
Novelty hypothesis      s≥2 is impossible, or a finite exceptional
                        family, or an infinite odd family
Falsifier               An odd n with square_depth(T(n))≥2, or a failed
                        obstruction
Existing machinery      localDefectOdd, power_deficit_eq_local_odd_iff,
                        HasPowTwoDepth, isqrt
Maximum Phase-0 scope   Inverse-floor lemma; integer-root search past
                        2000; smallest s≥2 obstruction or witness
Promotion criterion     Classification of odd-start sharp depths, or a
                        minimized s≥2 witness
Stop criterion          Recursive defect object; PowerHeight; equality
                        census; engine edits; termination
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(T(n)=M\) iff \(M^2\le n^3<(M+1)^2\) for odd \(n\) —
  **EXACT — LEAN VERIFIED**
- \(T(n)=a^{2^s}\) iff the exact interval
  \(a^{2^{s+1}}\le n^3<(a^{2^s}+1)^2\) —
  **EXACT — LEAN VERIFIED**
- Even first defect, unbounded \(E^s\) — already
  **EXACT — LEAN VERIFIED**
- Odd first defect, \(s\ge 2\) — search recorded; not a theorem
- Recursive suffix-defect object — not added
- `PowerHeight` — not added

## Experiments

- Probe: `research.juggler_sequence.odd_sharp_suffix`
- Heavy exact search: `tools/odd_fourth_power_search.py`, dataset
  [odd_sharp_suffix](../../data/research/juggler/odd_sharp_suffix/)
- Integer cube-root / fourth-power interval search on the output
  parameter \(a\); no huge \(n^{3/2}\) construction; no floats
- Records: [juggler_odd_sharp_suffix.md](../research/juggler_odd_sharp_suffix.md),
  [juggler_odd_sharp_suffix.json](../research/juggler_odd_sharp_suffix.json)
- Tests: `tests/research/juggler_sequence/test_odd_sharp_suffix.py`,
  `tests/tools/test_odd_fourth_power_search.py`
- The Research Engine control layer is not modified.

## Conjectures

None opened.

## Counterexamples

- Universal \(s\ge 2\) impossibility is not claimed. One even cube lies
  in a fourth-power square interval (\(b=97\), \(n=198636\)); that is
  not an odd Juggler step.
- Mixed-word local strictness remains refuted at word `O`, \(n=9\).

## Formalization

`formal/Problems/Engine/FloorPower.lean`. Added:

- `floor_sqrt_eq_iff_sq_interval`
- `floorPower_odd_eq_iff_cube_interval`
- `floorPower_odd_eq_pow_two_depth_iff`

No `PowerHeight`. No `sorry`. No `mixed_word_power_lt`. No
`PowerBoundStrict`. No ledger row. Existing sharpness theorems are
unchanged. There is no `s ≥ 2` impossibility theorem.

## Results

Classification **ODD_SHARP_SUFFIX_INCOMPLETE**. Decision **PARK**.

For odd \(n\),

\[
T(n)=M \iff M^2\le n^3<(M+1)^2
\]

is **EXACT — LEAN VERIFIED**. Specializing \(M=a^{2^s}\) gives

\[
T(n)=a^{2^s} \iff a^{2^{s+1}}\le n^3<(a^{2^s}+1)^2,
\]

also **EXACT — LEAN VERIFIED**. This is the integer form of the
inverse-floor equation. It is not a termination theorem.

Odd first-defect scan \(n\le 50000\): thirteen hits with
\(\mathrm{square\_depth}(T(n))\ge 1\), all of depth \(1\). The
smallest is \(11\to 36=6^2\). None of the \(s=1\) bases is a square,
so none of them lifts to \(s\ge 2\).

Persisted \(a\)-parameter search on \(1\le a<10^8\)
(**COMPUTATIONALLY VERIFIED**): \(99\,999\,999\) values, \(465\)
interval cubes, \(0\) odd non-squares. Every cube is either the exact
family \(a=k^3\), \(n=k^8\) for \(1\le k\le 464\), or the one inexact
even hit \(a=97\), \(n=198636\). Occupancy is at most one cube. Even
\(a\) forces even \(n\). This is
`ODD_FOURTH_POWER_NO_WITNESS` plus
`ODD_FOURTH_POWER_STRUCTURE_DISCOVERED`. It is not a theorem.

Even first defects remain unbounded: \(n=q^2+2\) with
\(q=4,16,256\) gives sharp suffixes of depths \(1,2,3\).

A finite empty search is not `ODD_SHARP_SUFFIX_IMPOSSIBLE`. No
elementary modular or factorization obstruction was proved.

## Open questions

If \(T(n)=a^4\) and \(n\) is odd, must \(n\) be a square? Equivalently:
must every inexact cube in \([a^8,(a^4+1)^2)\) be even? A yes would
make odd-start sharp suffixes exactly the family \(OE\).

## Decision

**PARK** the depth classification. Record
`ODD_SHARP_SUFFIX_INCOMPLETE`. The heavy search through \(a<10^8\)
found structure and no odd non-square witness; that is evidence, not
an impossibility theorem. Keep the inverse-floor lemmas. Do not
register an attack. Do not claim termination. Do not add
`PowerHeight` or a recursive defect object. Do not start Lean in
this phase.

Best next question: prove \(T(n)=a^4\) and \(n\) odd implies \(n\) is
a square, or exhibit an odd non-square witness.

## Publication assessment

Status: `EXPLORATORY`. A local inverse-floor lemma plus an unfinished
Diophantine question, not a paper candidate and not a Juggler
totality result.
