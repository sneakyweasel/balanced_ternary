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
Mathematical target     non-cube a and even m => (m+1)^3-a^8 > 2a^4
Novelty hypothesis      an elementary gap bound, possibly after a finite
                        threshold A0
Falsifier               NONCUBE_EVEN_CANDIDATE_SURVIVES
Existing machinery      occupancy, exact family, odd-cbrt parity,
                        integer_cbrt, persisted 465-hit corpus
Maximum Phase-0 scope   even-m surplus / near-miss analysis; integer
                        inequality or explicit A0; Lean only that bound
Promotion criterion     FOURTH_POWER_ODD_GREEN and ODD_SHARP_SUFFIX_GREEN
Stop criterion          no elementary or finite-reduction after the
                        focused analysis; Baker/Thue/Mordell; PowerHeight;
                        search expansion; engine edits
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
- Occupancy \(\le 1\), exact family \(a=k^3\Rightarrow n=k^8\),
  non-cube \(\Rightarrow n=m+1\), odd \(m\Rightarrow n\) even —
  **EXACT — LEAN VERIFIED**
- Even first defect, unbounded \(E^s\) — already
  **EXACT — LEAN VERIFIED**
- Odd first defect, unrestricted \(s\ge 2\) — leftover even-\(m\)
  case; not a theorem
- Recursive suffix-defect object — not added
- `PowerHeight` — not added

## Experiments

- Probe: `research.juggler_sequence.odd_sharp_suffix`
- Heavy exact search: `tools/odd_fourth_power_search.py`, dataset
  [odd_sharp_suffix](../../data/research/juggler/odd_sharp_suffix/)
- Nearest-cube analysis of the persisted hits (no \(10^8\) rerun):
  [nearest_cube.md](../../data/research/juggler/odd_sharp_suffix/analysis/nearest_cube.md)
- Even-\(m\) surplus / near-miss discovery (no \(10^8\) rerun):
  [even_cbrt.md](../../data/research/juggler/odd_sharp_suffix/analysis/even_cbrt.md)
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

- Universal interval emptiness is false: one even cube lies in a
  fourth-power square interval (\(a=97\), \(n=198636\)).
- “Odd \(a\) forces \(m=\lfloor\sqrt[3]{a^8}\rfloor\) odd” is false:
  \(a=3\) has \(m=18\). That window is empty (gap \(298>2\cdot 3^4\)).
- Mixed-word local strictness remains refuted at word `O`, \(n=9\).

## Formalization

`formal/Problems/Engine/FloorPower.lean`. Added:

- `floor_sqrt_eq_iff_sq_interval`
- `floorPower_odd_eq_iff_cube_interval`
- `floorPower_odd_eq_pow_two_depth_iff`
- `fourth_window_occupancy`
- `exact_cube_left_endpoint`
- `fourth_window_cube_eq_succ_cbrt`
- `noncube_odd_cbrt_fourth_window_cube_even`
- `odd_cube_interval_of_odd_cbrt_implies_square`
- `floorPower_odd_eq_fourth_power_of_odd_cbrt_implies_square`
- `odd_first_defect_not_pow_two_depth_ge_two_of_odd_cbrt`

No `PowerHeight`. No `sorry`. No `mixed_word_power_lt`. No
`PowerBoundStrict`. No ledger row: the Lean statement is the
restricted odd-\(m\) form, not the English claim
\(T(n)=a^4\) and \(n\) odd \(\Rightarrow n\) square. The reserved
name `floorPower_odd_pow_two_depth_ge_two_false` remains absent.

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

also **EXACT — LEAN VERIFIED**.

Nearest-cube reduction of that fourth-power window is
**EXACT — LEAN VERIFIED**:

- occupancy \(\le 1\);
- if \(a=k^3\), the unique cube is \(n=k^8\);
- if \(a\) is not a cube, the only possible cube is \(n=m+1\);
- that candidate is even exactly when \(m\) is odd.

The restricted Juggler form follows: if \(T(n)=a^4\), \(n\) is odd, and
\(m\) is odd, then \(n\) is a square. The restricted Phase-G corollary
is: an odd first defect cannot have a sharp exact-even suffix of
length \(\ge 2\) when that cube root is odd. Neither statement is
`ODD_FOURTH_POWER_GREEN` or `ODD_SHARP_SUFFIX_GREEN`.

Persisted \(a\)-parameter search on \(1\le a<10^8\)
(**COMPUTATIONALLY VERIFIED**, not rerun in this phase):
\(99\,999\,999\) values, \(465\) interval cubes, \(0\) odd non-squares.
Every cube is either the exact family \(a=k^3\), \(n=k^8\) for
\(1\le k\le 464\), or the one inexact even hit \(a=97\),
\(n=198636\) (\(m=198635\) odd). Occupancy is at most one cube. This
is `ODD_FOURTH_POWER_NO_WITNESS` plus
`ODD_FOURTH_POWER_STRUCTURE_DISCOVERED`. Finite emptiness is not a
theorem.

“Even \(a\) forces even \(n\)” is only an observation on the hit
set (every even hit is an exact \(k^3\)). It is not a theorem.

Even-\(m\) discovery on \(1\le a\le 20000\) found \(0\) window hits.
Closest near-misses are small: \(a=3,6,79,2\). The example \(a=37840\)
has even \(m\) with \(a^8\) at the top of its cube cell, so a uniform
remaining-fraction lemma is false. The trivial bound
\(m\ge a^{8/3}-1\) is sharp and cannot produce a threshold \(A_0\).
This is not `NONCUBE_EVEN_CANDIDATE_SURVIVES` and not
`FOURTH_POWER_ODD_GREEN`.

Even first defects remain unbounded: \(n=q^2+2\) with
\(q=4,16,256\) gives sharp suffixes of depths \(1,2,3\).

## Open questions

If \(a\) is not a cube and \(m=\lfloor\sqrt[3]{a^8}\rfloor\) is even,
can \(n=m+1\) lie in the window? Cube-root bracketing and a uniform
remaining-fraction bound do not decide this. The \(a=97\) even hit
and the exact family \(a=k^3\), \(n=k^8\) must remain legal.

## Decision

**PARK** the unrestricted fourth-power claim. Record
`ODD_SHARP_SUFFIX_INCOMPLETE`. The elementary nearest-cube lemmas
remain Lean. The even-\(m\) gap inequality is not elementary after
the focused surplus analysis: no uniform remaining-fraction bound,
no cube-root threshold \(A_0\), and no small-modulus obstruction on
the surviving candidate. Do not start Baker/Thue/Mordell. Do not
rerun \(10^8\). Do not register an attack. Do not claim termination.
Do not add `PowerHeight` or a recursive defect object.

Best next question: prove that a non-cube with even \(m\) never
satisfies \((m+1)^3-a^8\le 2a^4\), or exhibit such an \(a\).

## Publication assessment

Status: `EXPLORATORY`. A local inverse-floor lemma plus a restricted
nearest-cube obstruction and an unfinished even-\(m\) question, not a
paper candidate and not a Juggler totality result.
