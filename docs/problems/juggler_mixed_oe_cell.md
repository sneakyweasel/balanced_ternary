# Juggler mixed OE cell

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment, not a W_5
reopen, not a first-return \(Q\)-map, not Paper A, and not a claim
that every positive integer reaches 1.

After the cube-odd lift, the leftover question was whether
\(x^{3}\approx y^{2}\) followed by an even square step is a new
cell or only the product of existing envelopes.

## Problem

Does an odd cube step followed by an even square step occupy a
mixed cell strictly narrower than composing the two one-step
envelopes?

## Exact statement

Let \(x\) be odd and \(T(x)\) even. Then

\[
T^{2}(x)<n^{2}\qquad\Longleftrightarrow\qquad x^{3}<n^{8}.
\]

This is strictly sharper than the composed cube-band envelope
\(x<n^{3}\Rightarrow T^{2}(x)^{4}<n^{9}\). The floor defect
\(\delta=x^{3}-T(x)^{2}\) remains maximally broad:
\(\theta=\delta/(2T(x)+1)\) attains values near \(0\) and near
\(1\) on the cube-band.

On `MinimalNonTerm` an eighth-cell even lift cannot return even.
This is not a halt theorem.

## Current literature

- `even_below_fourth` / `cube_lift_even_reset_fourth` —
  **EXACT — LEAN VERIFIED** (`J-cube-odd-even-reset`)
- even return always below \(n^{2}\) —
  **REFUTED** (`J-cube-odd-even-below-square`)
- history-sensitive defect tighter than \(0\le\delta<2y+1\) —
  **REFUTED** (`J-mixed-oe-defect-gap`)
- postponed source-relative reset —
  **REFUTED** (`J-source-relative-odd-reset`)
- Every start reaches 1 — not claimed

Project relationship: **extended**. The designated mixed-cell
question after the cube-odd return.

## Branch budget

```text
Mathematical target     After an odd lift, is OE a new mixed
                        cell or only composed envelopes?
Novelty hypothesis      z < n^2 iff x^3 < n^8, sharper than
                        z < n^{9/4} from x < n^3
Falsifier               the iff is only even_below_fourth
                        restated; or leftovers sit above n^8
Existing machinery      even_below_fourth;
                        cube_lift_even_reset_fourth;
                        CubeOddLanding; 1517 / 501 laboratories
Maximum Phase-0 scope   Lean iff + leftover/501 split +
                        n=13 sharpness; no Q-return; no
                        letter chain
Promotion criterion     reusable mixed OE cell consumed by
                        CycleMin and MinimalNonTerm
Stop criterion          intersection of old cells only;
                        defect census; first-return Q; W_5
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- odd-then-even is \(z<n^{2}\) iff \(x^{3}<n^{8}\) —
  **EXACT — LEAN VERIFIED**
- leftover first lifts of \(365,501,1517,6187\) sit below \(n^{8}\) —
  **COMPUTATIONALLY VERIFIED**
- \(501\) later landing sits above \(n^{8}\) and not below \(n^{2}\) —
  **COMPUTATIONALLY VERIFIED**
- defect excludes an interval at cube scale —
  false
- first-return section — not asked
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.mixed_oe_cell`
- Records: [juggler_mixed_oe_cell.md](../research/juggler_mixed_oe_cell.md),
  [juggler_mixed_oe_cell.json](../research/juggler_mixed_oe_cell.json)
- Tests: `tests/research/juggler_sequence/test_mixed_oe_cell.py`
- Lean: `formal/Problems/Juggler/MinimumRelative.lean` and a CE
  consumer in `Minimal.lean`, laboratory barrel only. Not imported
  by `Problems.JugglerPaper`. No `sorry`.

## Conjectures

None opened.

## Counterexamples

“The floor defect becomes informative at cube scale” is false.
On the \(n=13\) cube-band, \(\theta\) ranges from near \(0\) to
near \(1\).

“Every even high lift returns below \(n^{2}\)” remains false:
\(n=501\), \(x=48693935\) has \(x^{3}\ge n^{8}\) and
\(z=582916\ge 501^{2}\). The mixed iff still holds.

## Formalization

`MinimumRelative.lean` adds `odd_even_eighth_lt_sq` and
`finiteProgress_of_odd_even_eighth`. `Minimal.lean` adds
`minimal_odd_even_eighth_forces_odd_return`. No new Lean file.
Paper A is unchanged. No `sorry`. No halt theorem.

## Results

Classification **MIXED_OE_CELL_GREEN**.

The first genuinely new mixed cell is the eighth-power
comparison. Leftover first cube-odd lifts occupy the square
side; the \(501\) later landing occupies the complementary
side and explains why \(z<n^{2}\) is not the cube-band
theorem. Defect adds no exact cut. Two-step composition of
\(x<n^{3}\) only gives \(z<n^{9/4}\).

This is not a halt theorem and not a first-return section.

## Open questions

The leftover first-lift question is answered in
[juggler_first_lift_eighth.md](juggler_first_lift_eighth.md):
the preferred first-lift theorem is **REFUTED**. Do not resume
a first-return \(Q\)-map. Do not reopen W_5.

## Decision

**PROMOTE** the mixed OE iff and the CE consumer. CycleMin and
MinimalNonTerm consume the same geometry. Do not claim that
every leftover orbit stays in the eighth cell. Do not claim
termination.

Best next question: taken up and parked in
[juggler_first_lift_eighth.md](juggler_first_lift_eighth.md).

## Publication assessment

Status: `EXPLORATORY`.

A small exact mixed cell that names the leftover / \(501\)
split. Not a paper candidate and not a Juggler totality result.
