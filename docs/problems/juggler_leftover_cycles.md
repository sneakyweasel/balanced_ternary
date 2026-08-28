# Juggler leftover length-six cycle orientations

Status: **THEOREM**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1. It does not reopen the closed
uniform-from-\(3\) extra-scale branch.

## Problem

Are the leftover legal `CycleMin` orientations `OOOEOE` and `OOOOEE`
impossible as `CycleWord` for every \(n\ge 2\)?

## Exact statement

For every \(n\ge 2\),
\[
\neg\mathrm{CycleWord}(n,OOOEOE)
\qquad\text{and}\qquad
\neg\mathrm{CycleWord}(n,OOOOEE).
\]
The argument is an exhaustive evaluation for \(n<256\) together with
the last-even cell against the coarse lower envelope
\(n^{81}>2^{130}(n+1)^{64}\) for \(n\ge256\).

This is not an exclusion of every length-six word, not an exclusion of
odd-terminating cycle words, and not a halt theorem.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Cycle exponent and extrema —
  **EXACT — LEAN VERIFIED**.
- Internal-E bootstrap —
  **EXACT — LEAN VERIFIED**. `OOOEOE` and `OOOOEE` were the leftovers.
- Prefix-OOO extra scale from \(n=3\) —
  **REFUTED**; first forced `OOO` overshoot at \(n=109\). That `CLOSE`
  is not reopened.

Project relationship: **extended**. The parked leftover of
`juggler_cycle_internal_e` and `juggler_cycle_ooo_scale`. Totality
remains unclaimed.

## Branch budget

```text
Mathematical target     Are CycleWord n OOOEOE and CycleWord n OOOOEE
                        impossible for all n≥2?
Novelty hypothesis      Finite eval below 256 plus n≥256 LowerPowerBound
                        / last-even comparison
Falsifier               A realizing n exists, or the tail is only a
                        rewrite of closed OOO identities
Existing machinery      LowerPowerBound, last-even cells, CycleWord,
                        ooo_suffix_threshold
Maximum Phase-0 scope   These two words only; no length-7; no halt
Promotion criterion     Lean exclusion of both CycleWords
Stop criterion          Tail fails to formalize or is reparameterization
                        without exclusion
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- `CycleWord` on `OOOEOE` is impossible —
  **EXACT — LEAN VERIFIED**
- `CycleWord` on `OOOOEE` is impossible —
  **EXACT — LEAN VERIFIED**
- every length-six cycle word is impossible — not claimed
- cycles ending in `O` as `CycleWord` are impossible — not claimed
- global halt — not claimed

## Experiments

- Lean: `formal/Problems/Juggler/LeftoverEval.lean`,
  `formal/Problems/Juggler/LeftoverCycles.lean`
- Tests: `tests/research/juggler_sequence/test_cycle_leftover_words.py`
- The Research Engine control layer is not modified.
- No cycle-state search. No length 7. No O-terminating programme.

## Conjectures

None opened.

## Counterexamples

None to the two exclusions. The stronger claims that remain false:

- “`LowerPowerBound` on `OOO` forces last-even overshoot from \(n=3\)”
  — still fails at \(n=3\) and \(n=5\); this branch uses cutoff \(256\).
- “every length-six word is excluded” — not claimed.

## Formalization

`formal/Problems/Juggler/LeftoverEval.lean` isolates `native_decide`
facts. `formal/Problems/Juggler/LeftoverCycles.lean` proves

- `no_cycle_word_oooeoe`
- `no_cycle_word_ooooee`

`FloorPower`, `Progress`, and `Minimal` are not rewritten. No `sorry`.
No halt theorem. No `no_juggler_cycle`. No `CycleSearch`. No
`no_cycle_word_length_six`. No `no_cycle_word_ooooeoe`. No
`PowerBoundEq` attack. No `PowerHeight`.

## Results

Both leftover orientations are impossible as cycle words
(**EXACT — LEAN VERIFIED**). The math note records this as Theorem 3.2.

## Open questions

Whether almost every odd-to-odd start has a finite descent certificate.
Do not open length 7. Do not start an O-terminating `CycleWord`
programme.

## Decision

**PROMOTE**. Finite evaluation below \(256\) plus the last-even cell
against `LowerPowerBound` excludes both leftover `CycleWord`s. This is
not the closed uniform-from-\(3\) extra-scale attack, not a length-six
census, and not a halt theorem.

Best next question: do almost all odd-to-odd starts have a finite
descent certificate?

## Publication assessment

Status: `THEOREM`.

Named exclusion of two leftover orientations; recorded in the math
note as Theorem 3.2. Not a Juggler totality result.
