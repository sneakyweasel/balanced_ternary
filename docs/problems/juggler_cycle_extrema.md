# Juggler cycle extrema

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1.

## Problem

Can the existing power, parity, and cell machinery impose incompatible
constraints on the excursion from a cycle minimum \(m\) to a cycle
maximum \(M\) and back, without enumerating cycle words?

## Exact statement

For a nontrivial `CycleWord` with \(n\ge 2\), write \(m\) for a
minimum state and \(M\) for a maximum state. Then:

- \(m\) is odd,
- \(M\) is even,
- \(M>m^2\).

The last inequality is strict because \(m^2\) is odd. Equivalently,
\(T(M)=\lfloor\sqrt M\rfloor\ge m\), so \(M\ge m^2\), and parity
forbids equality.

Any realized finite word from a start \(n\ge 2\) to a state at least
\(n^2\) is superquadratic:

\[
3^{\#O(w)}\ge 2^{|w|+1}.
\]

In particular, on a cycle minimum the path to any later even state —
including the maximum — is superquadratic. This is stronger than the
full-cycle envelope \(3^{\#O}>2^{|w|}\): the prefix `OOE` is expanding
(\(9>8\)) but not superquadratic (\(9<16\)), so it cannot carry \(m\)
to square scale.

The maximum return cell is the ordinary even branch:

\[
T(M)=q=\lfloor\sqrt M\rfloor,\qquad
M\in[q^2,(q+1)^2),\qquad q\ge m.
\]

This does not force \(q=m\). The first-cell family
\(M\in(m^2,(m+1)^2)\) is not excluded.

This says nothing about cycles ending in a particular letter. Do not
prove that every cycle word is impossible. Do not prove totality.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Cycle minimum is odd —
  **EXACT — LEAN VERIFIED**.
- Finite-word power envelope —
  **EXACT — LEAN VERIFIED**.
- Internal-E bootstrap —
  **EXACT — LEAN VERIFIED**.

Project relationship: **extended**. Extrema are packaged independently
of word length. Totality remains unclaimed.

## Branch budget

```text
Mathematical target     extrema force M > m^2 and a superquadratic min-to-even path
Novelty hypothesis      max even + PowerBound give a prefix law stronger than 2^r < 3^o
Falsifier               a path to ≥ m^2 with 3^o < 2^{k+1}; or max odd on a cycle
Existing machinery      CycleMin, power_bound_word, floorPower_odd_gt / even_lt
Maximum Phase-0 scope   CycleMax; M > m^2; square-scale superquadratic; transient calibration
Promotion criterion     reusable extrema package, or a genuine prefix law
Stop criterion          cycle engine; word census; FloorPower rewrite; first-cell census
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- cycle maximum is even —
  **EXACT — LEAN VERIFIED**
- \(M>m^2\) on a cycle minimum —
  **EXACT — LEAN VERIFIED**
- square-scale image implies superquadratic word —
  **EXACT — LEAN VERIFIED**
- min-to-even (hence min-to-max) prefixes are superquadratic —
  **EXACT — LEAN VERIFIED**
- growth and collapse cannot coexist — not claimed
- first-cell maxima are impossible — not claimed
- every cycle word is impossible — not claimed
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_extrema`
- Records: [juggler_cycle_extrema.md](../research/juggler_cycle_extrema.md),
  [juggler_cycle_extrema.json](../research/juggler_cycle_extrema.json)
- Tests: `tests/research/juggler_sequence/test_cycle_extrema.py`
- The Research Engine control layer is not modified.
- Stay-above-min transient calibration only. No cycle-state search.
- No evaluation of huge eventual \(Q_0\).

## Conjectures

None opened.

## Counterexamples

None to the extrema package. The stronger claims that fail:

- “every odd start hits \(m^2\) before dropping” — `7` walks
  `O` then `E` and falls to `4`.
- “the cycle envelope already forces the prefix law” — `OOE` is
  expanding and not superquadratic.
- “\(M=m^2\) is possible” — \(m\) odd makes \(m^2\) odd.
- “the maximum must collapse to the minimum” — the return cell
  permits \(q>m\).

## Formalization

`formal/Problems/Engine/CycleWord.lean`, a small extension. Added:

- `CycleMax` / `exists_cycle_max_even` / `cycleMax_start_even`
- `cycleMin_max_gt_sq` / `cycleMin_max_sqrt_ge` / `cycleMax_return_cell`
- `square_scale_superquadratic`
- `cycleMin_to_even_superquadratic` / `cycleMin_to_max_superquadratic`

`FloorPower` and `Progress` are not rewritten. No `sorry`. No halt
theorem. No `no_juggler_cycle`. No `CycleSearch`. No length
classification. No first-cell census. No `PowerBoundEq` attack. No
`PowerHeight`.

## Results

Classification **CYCLE_EXTREMES_GREEN**, with secondary
**ASCENDING_SUPERQUADRATIC_GREEN**.

The package is reusable and word-independent. It is not a
growth-versus-collapse obstruction. Ordinary transients often drop
before square scale, so the cycle demand \(M>m^2\) is not vacuous.

## Open questions

Does the superquadratic min-to-max prefix plus the exact maximum
return cell force a forbidden transition for some scalable family,
without enumerating words? Do not start a first-cell census. Do not
reopen length 7.

## Decision

**PROMOTE** the extrema package and the square-scale prefix law. Do
not claim that growth and collapse cannot coexist. Do not claim that
first-cell maxima are impossible. Do not claim termination.

Best next question: does the superquadratic min-to-max prefix plus
the exact maximum return cell force a forbidden transition without a
word census?

## Publication assessment

Status: `EXPLORATORY`. An extrema-and-prefix lemma, not a paper
candidate and not a Juggler totality result.
