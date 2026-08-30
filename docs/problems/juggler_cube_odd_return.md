# Juggler cube-odd return

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment, not a W_5
reopen, not a power-cell census, not Paper A, and not a claim that
every positive integer reaches 1.

The cube-not-square cell left an odd residual
\(n^{2}\le x<n^{3}\). This phase names the return after the lift
\(y=T(x)\ge n^{3}\).

## Problem

What exact information is preserved by an odd cube-band lift, and
what forces its first meaningful return?

## Exact statement

Let \(n\ge 2\) and \(n^{2}\le x<n^{3}\) with \(x\) odd. Then
\(n^{3}\le T(x)<n^{5}\) and \(T(x)^{2}<n^{9}\). Write
\(y=T(x)\) and \(z=T(y)\).

- if \(y\) is even, then \(n\le z<x<n^{3}\) and \(z^{4}<n^{9}\);
- if \(y\) is odd, then \(x<z\) and \(n^{4}\le z\).

If that even reset is itself even and already below \(n^{2}\), the
three-letter word from \(x\) is `FiniteProgress`. On
`MinimalNonTerm` an even lift therefore cannot return even below
\(n^{2}\).

The stronger claim \(z<n^{2}\) is false.

## Current literature

- `odd_ge_sq_floor_ge_cube` / even cube reset —
  **EXACT — LEAN VERIFIED** (`J-cube-not-square-split`)
- `floorPower_odd_even_two_step_lt` —
  **EXACT — LEAN VERIFIED**
- `floorPower_odd_odd_two_step_gt` —
  **EXACT — LEAN VERIFIED**
- \(1517\to 43916043\) is an odd cube landing —
  **COMPUTATIONALLY VERIFIED** (`J-second-o-below-square`)
- even return always below \(n^{2}\) —
  **REFUTED** (`J-cube-odd-even-below-square`)
- Every start reaches 1 — not claimed

Project relationship: **extended**. The designated next question
of the cube-not-square certificate.

## Branch budget

```text
Mathematical target     After an odd cube lift, what constrains
                        the first return?
Novelty hypothesis      even y returns below the source (hence
                        below n^3); odd y continues above x
Falsifier               even y indistinguishable from generic
                        y >= n^3; or only a new power census
Existing machinery      odd_ge_sq_floor_ge_cube;
                        floorPower_odd_even_two_step_lt;
                        even_below_square_iff; EnvelopeState;
                        1517 laboratory
Maximum Phase-0 scope   Lean even-reset + odd continuation +
                        1517 / 501 laboratories; no n^6 chain
Promotion criterion     reusable return theorem: even reset to
                        a known corridor or controlled higher
                        excursion
Stop criterion          only generic 3/2 growth; residue
                        automaton; W_5 / Z_5 / length-11
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- odd \(x<n^{3}\) gives \(T(x)^{2}<n^{9}\) and \(T(x)<n^{5}\) —
  **EXACT — LEAN VERIFIED**
- even \(y=T(x)\) gives \(n\le T^{2}(x)<x<n^{3}\) —
  **EXACT — LEAN VERIFIED**
- even return satisfies \(T^{2}(x)^{4}<n^{9}\) —
  **EXACT — LEAN VERIFIED**
- odd \(y\) gives \(T^{2}(x)>x\) and \(T^{2}(x)\ge n^{4}\) —
  **EXACT — LEAN VERIFIED**
- even return below \(n^{2}\) —
  false (`501`, later landing \(48693935\))
- first leftover lifts even-reset below \(n^{2}\) —
  **COMPUTATIONALLY VERIFIED** on \(365,501,1517,6187\)
- history-sensitive defect tighter than \(0<\delta<2y+1\) —
  not obtained
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.cube_odd_return`
- Records: [juggler_cube_odd_return.md](../research/juggler_cube_odd_return.md),
  [juggler_cube_odd_return.json](../research/juggler_cube_odd_return.json)
- Tests: `tests/research/juggler_sequence/test_cube_odd_return.py`
- Lean: `formal/Problems/Juggler/MinimumRelative.lean` and a CE
  consumer in `Minimal.lean`, laboratory barrel only. Not imported
  by `Problems.JugglerPaper`. No `sorry`.

## Conjectures

None opened.

## Counterexamples

“Even high lift after an odd cube landing returns below \(n^{2}\)”
is false. For \(n=501\) the later cube-odd state \(x=48693935\)
has even
\(y=339791341082\ge 501^{4}\) and
\(z=582916\in[501^{2},501^{3})\). The source return
\(z<x\) still holds.

Generic odd \(x\in[n^{2},n^{3})\) (not produced by an
`AboveAnchor` orbit) also returns to \([n^{2},n^{9/4})\) often;
that is not the leftover corridor.

## Formalization

`CubeCorridor.lean` adds `CubeOddLanding`,
`odd_lt_cube_floor_sq_lt_nine`, `odd_lt_cube_floor_lt_five`,
`cube_odd_lift`, `cube_lift_even_reset`,
`cube_lift_even_reset_lt_cube`, `cube_lift_even_reset_fourth`,
`cube_lift_odd_continues`, and `cube_lift_odd_ge_fourth`.
`Progress.lean` adds
`finiteProgress_of_cube_odd_even_below_square`.
`Minimal.lean` adds
`minimal_cube_odd_even_not_even_below_square`. Paper A is
unchanged. No `sorry`. No halt theorem.

## Results

Classification **CUBE_ODD_RETURN_GREEN**.

An odd cube lift is a two-sided transition. The even branch
returns below the source, hence into the already-analysed region
below \(n^{3}\), and into the fractional corridor \(z^{4}<n^{9}\).
The odd branch continues above the source and at least to
\(n^{4}\). The first leftover lifts of \(365,501,1517,6187\) all
take the even branch and land below \(n^{2}\); \(1517\) then drops.
A later landing on \(501\) shows that square-cell return is not
the theorem.

This is not a halt theorem and not another integer-power census.

## Open questions

The leftover is now an odd lift \(y=T(x)\) that stays odd. Do not
resume an \(n^{6},n^{7},\ldots\) envelope. Do not reopen W_5.

## Decision

**PROMOTE** the even-reset return theorem and the odd-continuation
lower bound. CycleMin and MinimalNonTerm consume the same geometry.
Do not claim that every even reset is `FiniteProgress`. Do not
claim termination.

Best next question: after an odd cube lift whose first image is
odd, does the first later even letter still return below the
original cube-band source, or only below a later high state?

## Publication assessment

Status: `EXPLORATORY`.

A small exact return dichotomy that makes the odd cube residual a
named two-sided transition. Not a paper candidate and not a
Juggler totality result.
