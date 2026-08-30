# Juggler source-relative odd reset

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment, not a W_5
reopen, not an \(n^{6}\) census, not Paper A, and not a claim that
every positive integer reaches 1.

The cube-odd even branch is already a source-relative descent
\(T^{2}(x)<x\). This phase asks whether a persistent-odd lift
postpones the same reset to the first later even state.

## Problem

If a cube-odd source stays odd, does the first subsequent even
return still fall below that source?

## Exact statement

Let \(n\ge 2\) and \(n^{2}\le x<n^{3}\) with \(x\) odd. Write
\(\tau(x)=\min\{j\ge 1:T^{j}(x)\text{ even}\}\) and
\(e=T^{\tau(x)}(x)\). The \(\tau=1\) case is the existing
source-relative theorem \(T^{2}(x)<x\). Phase 0 asks whether
\(\tau\ge 2\) still forces

\[
e<x^{2}\qquad\text{and}\qquad T(e)<x.
\]

It also asks whether the next expansion source is strictly
smaller than \(x\).

Do not resume an absolute power census. Do not prove totality.

## Current literature

- Cube-odd even reset \(n\le T^{2}(x)<x\) —
  **EXACT — LEAN VERIFIED** (`J-cube-odd-even-reset`)
- Cube-odd odd continuation \(T^{2}(x)>x\) and \(T^{2}(x)\ge n^{4}\) —
  **EXACT — LEAN VERIFIED**
- `floorPower_odd_even_two_step_lt` resets relative to the
  *current* odd state, not the episode source —
  **EXACT — LEAN VERIFIED**
- Two-odd source envelope \(e^{4}\le x^{9}\) —
  **REPARAMETERIZATION** of `EnvelopeState.odd`
- Persistent-odd first even below \(x^{2}\) —
  **REFUTED** (`J-source-relative-odd-reset`)
- Episode-source descent —
  **REFUTED** (`J-episode-source-descent`)
- Every start reaches 1 — not claimed

Project relationship: **extended**. The designated next question
of the cube-odd return certificate.

## Branch budget

```text
Mathematical target     If a cube-odd lift stays odd, is the
                        first even still below x^2?
Novelty hypothesis      persistent odd postpones the same
                        source-relative reset
Falsifier               first even e >= x^2 and T(e) >= x;
                        or next source >= x with no secondary
                        well-founded quantity
Existing machinery      cube_lift_even_reset;
                        cube_lift_odd_continues;
                        floorPower_odd_even_two_step_lt;
                        EnvelopeState; 37 laboratory
Maximum Phase-0 scope   37 witness; leftover tau; exact 9/4
                        envelope; no new Lean; no n^6 chain
Promotion criterion     first even < x^2, or well-founded
                        episode-source descent
Stop criterion          Falsifier A; leftover only tau=1;
                        envelope is EnvelopeState; W_5
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(\tau=1\) gives \(e^{2}\le x^{3}\), hence \(T(e)<x\) —
  **EXACT — LEAN VERIFIED** (existing)
- two odd steps give \(e^{4}\le x^{9}\), and \(9>8\) so not
  \(e<x^{2}\) —
  **REPARAMETERIZATION**
- three odd steps give \(e^{8}\le x^{27}\) —
  **REPARAMETERIZATION**
- first leftover lifts of \(365,501,1517,6187\) have \(\tau=1\) —
  **COMPUTATIONALLY VERIFIED**
- \(69\) and \(89\) have no cube-odd landing —
  **COMPUTATIONALLY VERIFIED**
- persistent-odd first even below \(x^{2}\) —
  false (\(n=37\), \(x=3375\), \(e=86818724\), \(T(e)=9317\))
- episode sources strictly decrease —
  false (\(3375,9317,2233\))
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.source_relative_odd`
- Records: [juggler_source_relative_odd.md](../research/juggler_source_relative_odd.md),
  [juggler_source_relative_odd.json](../research/juggler_source_relative_odd.json)
- Tests: `tests/research/juggler_sequence/test_source_relative_odd.py`
- Lean: none new. Existing `cube_lift_even_reset` and
  `cube_lift_odd_continues` stay in `MinimumRelative.lean`.
  Paper A is unchanged. No `sorry`.

## Conjectures

None opened.

## Counterexamples

“A persistent-odd cube lift has first even \(e<x^{2}\) and
\(T(e)<x\)” is false. For \(n=37\) the cube-odd source
\(x=3375\) follows `OO`: \(T(3375)\) is odd and
\(e=86818724\ge 3375^{2}\), with \(T(e)=9317\ge 3375\). The
two-odd envelope \(e^{4}\le x^{9}\) still holds.

“Each completed odd episode has a strictly smaller next source”
is false on the same orbit: the cube-odd sources are
\(3375,9317,2233\).

On odd starts \(n<400\), every scanned persistent-odd cube
episode likewise had \(e\ge x^{2}\) and \(T(e)\ge x\).

## Formalization

No new Lean file and no new source-relative primitive. The
obstruction \(9>8\) is the existing odd-odd composition of
`EnvelopeState`. Paper A is unchanged. No `sorry`. No halt
theorem.

## Results

Classification **SOURCE_RELATIVE_ODD_CLOSED**.

Persistent odd growth does not postpone the source-relative
reset. The \(\tau=1\) theorem is sharp: already at `OO` the
source-relative square comparison fails, because the exact
envelope is \(9/4\) rather than \(2\). The first even may sit
above \(x^{2}\), the post-even state may sit above \(x\), and
the next expansion source may grow. Leftover laboratories never
enter this branch on their first cube-odd landing.

This is not a halt theorem and not another integer-power
census.

## Open questions

None from source-relative reset. The residual is still an
odd-to-odd cube lift; do not iterate episode anchors. Do not
reopen W_5.

## Decision

**CLOSE**. The preferred, stronger, and best promotion targets
are all false. What remains is the already-named \(\tau=1\)
reset plus a generic EnvelopeState ratio. That is not a new
theorem.

Best next question: none from this reset. The leftover is still
an odd-to-odd cube lift with no source-relative descent.

## Publication assessment

Status: `EXPLORATORY`.

A one-witness refutation of a postponed reset. Not a paper
candidate and not a Juggler totality result.
