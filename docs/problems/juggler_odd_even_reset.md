# Juggler odd-to-even reset interface

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment, not a source-descent
reopen, not a cube-crossing reopen, not an `OddChain` primitive, not
\(Z_5\), not a length-11 assembly, not Paper A, and not a claim that
every positive integer reaches 1.

The local odd-branch program closed. The residual is no longer attached
to an individual odd step. This phase asks whether the first even reset
after a maximal odd run creates arithmetic that is invisible to
`EnvelopeState` and not already the generic `OE` two-step.

## Problem

What exact information is created at an odd-to-even reset that is not
already determined by the odd chain or the generic envelope?

## Exact statement

Let \(x\) start a maximal AboveAnchor odd run
\(x=x_0,\ldots,x_r=T^r(x)\), write \(e=T(x_r)\) for the first even
state, and \(s=T(e)\) for the post-even state. Phase 0 studies the
quadruple \((x,x_r,e,s)\) through the two floor defects

\[
x_r^3=e^2+\delta,\qquad 0\le\delta<2e+1,
\]

\[
e=s^2+\varepsilon,\qquad 0\le\varepsilon\le 2s,
\]

and the substitution identity

\[
x_r^3-s^4=2\varepsilon s^2+\varepsilon^2+\delta=\Psi(\delta,\varepsilon,s).
\]

The question is whether \((\delta,\varepsilon)\) or \(\Psi\) is
constrained beyond a generic odd-to-even step, whether
\(s^4\lessgtr x_r^3\) or \(s^A\le x^B\) is sharper than
`oe_block_scale` / `power_bound_word`, and whether two consecutive
resets give a well-founded source relation.

Do not assume \(s<x\). Do not introduce a scalar reset potential.
Do not prove totality.

## Current literature

- Realized `OE` scale \(T^2(x)^4\le x^3\) —
  **EXACT — LEAN VERIFIED** (`oe_block_scale`)
- Odd-to-even two-step descent \(T^2(x)<x\) —
  **EXACT — LEAN VERIFIED** (`floorPower_odd_even_two_step_lt`)
- Word envelope after \(O^r E\) —
  **EXACT — LEAN VERIFIED** (`EnvelopeState`, `power_bound_word`)
- Cube-odd even reset —
  **EXACT — LEAN VERIFIED** (`cube_lift_even_reset`)
- Source-relative first even below \(x^2\) —
  **REFUTED** (`J-source-relative-odd-reset`)
- Episode-source descent \(s<x\) —
  **REFUTED** (`J-episode-source-descent`)
- Two-episode source descent \(x_{i+2}<x_i\) —
  **REFUTED** (`J-two-episode-source-descent`)
- Whole-odd-chain compression —
  **CLOSE** (`juggler_odd_chain_minimality.md`)
- Cube-boundary crossing —
  **CLOSE** (`juggler_cube_crossing.md`)
- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**.
  Totality is not claimed

Project relationship: **extended**, then **reparameterized**. The
designated interface question after the odd-chain CLOSE.

## Branch budget

```text
Mathematical target     non-generic relation at odd-to-even reset
Novelty hypothesis      (delta, eps) or Psi couples beyond
                        EnvelopeState / generic OE
Falsifier A             reset is generic envelope propagation
Falsifier B             (delta, eps) as free as independent
                        floor steps
Falsifier C             every relation is oe_block_scale,
                        floorPower_odd_even_two_step_lt,
                        EnvelopeState, cube_lift_even_reset,
                        or ReturnBelow
Falsifier D             two consecutive resets unconstrained
Falsifier E             induced x -> x' contains a recurrent
                        family
Existing machinery      oe_block_scale; floorPower_odd_even_two_step_lt;
                        EnvelopeState; cube_lift_even_reset;
                        even_below_anchor_pow; ReturnBelow;
                        37 / leftover / long-run laboratories
Maximum Phase-0 scope   named reset quadruples; generic OE;
                        long starts 37/241/329; L-lab 33391;
                        no Lean; no reset automaton
Promotion criterion     a new reset identity with a semantic
                        consequence, a source inequality not
                        implied by the envelope, or a two-episode
                        well-founded / exact recurrence
Stop criterion          generic OE rewrite; source-descent
                        reopen; OddEvenReset Lean without a
                        new relation; local-invariant manufacture
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(\Psi(\delta,\varepsilon,s)=x_r^3-s^4\) —
  **REPARAMETERIZATION** of the two floor identities
- \(s^4<x_r^3\) —
  **EXACT — LEAN VERIFIED** (`oe_block_scale`) plus OE parity
  (an odd cube cannot be an even square)
- \(s<x_r\) —
  **EXACT — LEAN VERIFIED** (`floorPower_odd_even_two_step_lt`)
- \(s<x\) for a long odd run —
  **REFUTED** (\(37\to 9317\))
- leftover first reset \(s<x\) —
  **REFUTED** (those first runs have \(r=2\): \(365\to763\),
  \(501\to1089\), \(1517\to3789\), \(6187\to18425\))
- \(s^4\le x^3\) —
  **REFUTED** on long runs
- even \(s\) forces a second-even `FiniteProgress` —
  **REFUTED** (37 second reset \(s=4990602\), \(T(s)=2233\ge 37\))
- two-episode \(x_{i+2}<x_i\) —
  **REFUTED** (`J-two-episode-source-descent`, \(37\to9317\to2233\))
- `OddEvenReset` Lean primitive — not introduced
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.odd_even_reset`
- Records: [juggler_odd_even_reset.md](../research/juggler_odd_even_reset.md),
  [juggler_odd_even_reset.json](../research/juggler_odd_even_reset.json)
- Tests: `tests/research/juggler_sequence/test_odd_even_reset.py`

No CLI. No Lean. No reset automaton. No defect-potential search.

## Conjectures

None opened.

## Counterexamples

“The pair \((\delta,\varepsilon)\) is constrained beyond a generic
odd-to-even step” is false. Independent odd \(m<201\) with even
\(T(m)\) satisfy the same identity \(\Psi\) and the same strict
\(s^4<x_r^3\).

“\(s<x\) at the end of an odd episode” is false. The first 37 run
is \(x=37\), \(r=4\), \(x_r=196069\), \(e=86818724\), \(s=9317>37\).
Leftover first runs are the same obstruction at length \(2\):
\(365\to763\), \(501\to1089\), \(1517\to3789\), \(6187\to18425\).

“\(s^4\le x^3\) sharpens the episode envelope” is false on that
same run.

“A second even step after an even reset is `FiniteProgress`” is
false. The second 37 run resets to even \(s=4990602\) with
\(T(s)=2233\ge 37\).

“Two consecutive reset sources descend” is false:
\(37\to 9317\to 2233\) and \(2233>37\).

## Formalization

None added. Existing `Dynamics` and `Scale` already contain the
two-step descent and the `OE` fourth-power bound. No
`OddEvenReset.lean`. No `OddEvenResetRelation.lean`. Paper A is
unchanged. No `sorry`.

## Results

Classification **ODD_EVEN_RESET_CLOSED**.

Every named reset satisfies the exact substitution
\(x_r^3-s^4=\Psi(\delta,\varepsilon,s)\ge 0\), and the inequality
is strict on a genuine `OE` step. The same identity holds for
generic odd-to-even integers that are not episode endpoints. The
comparison \(s<x_r\) is `floorPower_odd_even_two_step_lt` on
\((x_r,e,s)\). The comparison \(s^4\le x_r^3\) is `oe_block_scale`.
The episode envelope \(s^{2^{r+1}}\le x^{3^r}\) is ordinary
`EnvelopeState` on \(O^r E\) and is too weak to force \(s<x\) when
\(r\ge 2\).

Leftover first runs have length \(2\), so their reset is an
`OOE` envelope \(s^8\le x^9\), which permits \(s>x\). The last
letter pair is still generic `OE` on \((x_r,e,s)\). That is not
new episode information.

This is Falsifier A, B, C, and D. Falsifier E is the already
recorded two-episode motion \(37\to9317\to2233\), not a new
recurrent family from the defects.

## Open questions

None from the odd-to-even reset interface. Do not introduce
`OddEvenReset`. Do not reopen source descent, two-episode descent,
cube-crossing, or odd-chain compression. The leftover hole is
still an odd cube escape whose even lift is known and whose odd
lift is a generic high odd step.

## Decision

**CLOSE**. The reset interface creates exactly the generic `OE`
floor composition already in Lean. The episode source \(x\) does
not impose an extra bound on \(s\). A branch whose statements are
all `KNOWN` or `REPARAMETERIZATION` is a close.

Best next question: none from the odd-to-even reset interface.
The residual is not a local reset-identity problem.

## Publication assessment

Status: `EXPLORATORY`.

A negative interface fragment. Not a paper candidate and not a
Juggler totality result.
