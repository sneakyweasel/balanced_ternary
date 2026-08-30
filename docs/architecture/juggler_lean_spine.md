# Juggler Lean spine

Live-tree audit of `formal/Problems/Juggler`. This is an architecture
note, not a problem dossier and not a research attack.

The spine is one-definition / one-generic / thin-corollary when a
failed proof names a missing cell rather than a missing wrapper.
`EnvelopeState` implements cell comparison. `AboveAnchor` is the
shared prefix geometry. `CycleMin` and `MinimalNonTerm` consume it
downward. Paper A (`Problems.JugglerPaper`) is unchanged.

## Concept classification

| Kind | Objects | Home |
|------|---------|------|
| Primitive | `floorPower` / `follows` / words | `Dynamics.lean`, `Itinerary.lean`, `WordStats.lean` |
| Primitive | `EnvelopeState` / `envelope_lt_pow` | `Envelope.lean` |
| Primitive | `AboveAnchor` | `MinimumRelative.lean` |
| Primitive | `DescentCertificate` / `FiniteProgress` | `Certificates.lean`, `Progress.lean` |
| Derived | `PowerBound` as `A=2^{\|w\|}`, `B=3^{\#O}` | `Envelope.lean` |
| Derived | `power_bound_word` / `power_bound_lt_pow` | `Envelope.lean` |
| Derived | `even_below_anchor_pow` / `even_below_cube_cell` / `odd_ge_sq_floor_ge_cube` | `MinimumRelative.lean` |
| Derived | `isolatedOddSurvival_bound` | `MinimumRelative.lean` |
| Consumer | `CycleMin` + `aboveAnchor_of_cycleMin` | `CycleCore.lean` |
| Consumer | `MinimalNonTerm` + `aboveAnchor_of_minimalNonTerm` | `Minimal.lean` |
| Consumer | `ReturnBelow` (shifted drop, not a second descent type) | `Residuals.lean` |
| Wrapper | `no_cycleMin_prefix_ooe_oe`, `minimal_isolated_two`, named Escape words, leftover census, `J-cyclemin-*` ledger ids | keep names |

`EscapeEpisode` is Python-only.

`HasFiniteStop` is `∃ k, T^k(n)<n` (`FirstPassage.lean`).
`FiniteProgress` is a certificate inductive. Do not merge.

## Import graph

Ideal:

```text
Dynamics → Envelope / Cells → AboveAnchor → CycleMin | MinimalNonTerm
```

Before this audit:

```text
Progress → Minimal → Scale → MinimumRelative(AboveAnchor)
                                  → Residuals → CycleCore(CycleMin)
```

`CycleMin → AboveAnchor` was already downward and thin
(`aboveAnchor_of_cycleMin` in `CycleCore.lean`). `MinimumRelative`
did not import `CycleCore`. The inversion was the other way:
`MinimumRelative` imported `Scale`, which imported `Minimal`, so
`AboveAnchor` sat above `MinimalNonTerm`. Two causes: CE consumers
lived in `MinimumRelative`, and `isolatedPrefix` needed `wordOE` /
`repeatedOE` / `oddEvenBlock` from `Scale`.

After this cleanup:

```text
WordStats / Envelope / Progress
            ↓
      MinimumRelative (AboveAnchor)
         /                    \
    Minimal.lean           CycleCore
    (CE wrappers)        (cycle wrappers)
```

`Scale` keeps CE scale barriers and imports `WordStats` + `Minimal`.
`Residuals` imports `Minimal` so `MinimalNonTerm` remains visible
without routing it through `AboveAnchor`. Word combinators
(`wordOE`, `repeatedOE`, `oddEvenBlock`, length / `oddCount` lemmas,
`four_pow_eq_two_pow_two_mul`) live in `WordStats`. `repeated_oe_scale`
lives in `Envelope` because it is `power_bound_word` on `repeatedOE`.

## Red flags (live tree, then disposition)

1. **Import inversion.** `AboveAnchor` imported `Minimal` through
   `Scale`. **Fixed:** `MinimumRelative` imports `Envelope` +
   `Progress` + `WordStats`. CE consumers
   `aboveAnchor_of_minimalNonTerm`,
   `minimal_nonterm_not_follow_odd_even`,
   `minimal_cube_even_forces_odd_image` moved to `Minimal.lean`.
2. **Dead `EnvelopeState`.** Defined in `Envelope.lean`; no other
   file mentioned it. Escape / Scale / Residuals / CycleExtrema
   called `power_bound_word` / `power_bound_lt_pow` with a parallel
   proof. **Fixed:** `power_bound_lt_pow` is
   `(EnvelopeState.of_follows hw).lt_pow`. `power_bound_contracts`
   is the `k = 1` case of that theorem.
3. **Handwritten Escape `*_pow` theorems.** The seven
   `follows_*_image_lt_sq|cube` proofs were already
   `power_bound_lt_pow` + `decide`. Unused `follows_*_pow` blocks
   still unfolded `x^{2^{|w|}} ≤ n^{3^{\#O}}` with `convert` /
   `norm_num` and `set_option exponentiation.threshold`.
   **Fixed:** those `*_pow` theorems deleted. Cell names kept.

## Accepted debt

- `PowerBound` remains the inductive word engine
  (`power_bound_from`, append). `EnvelopeState.of_follows` wraps
  `power_bound_word`. One comparison engine; not a second
  composition engine.
- Named Escape words, leftover census, Defect / Equality,
  CycleExtrema stay as research wrappers. No rename campaign.
- `JugglerPaper.lean` already imports `Envelope` for
  `power_bound_word`. It does not import `MinimumRelative` /
  `Escape`. `EnvelopeState` is visible to Paper A only because it
  lives in an already-imported file. Do not mention it in Paper A
  comments.
- Python `has_named` / `lean_api_present` are string checks on
  sources. `lake build` is the formal regression. Do not turn
  probes into a second proof checker.
- Residuals imports `Minimal` and `Scale` so `MinimalNonTerm` and
  Scale CE barriers (`contracting_odd_even_block_contracts`) stay
  visible to `CycleCore` / `CycleExtrema` without routing them
  through `AboveAnchor`. Word combinators live in `WordStats`.

## What this note is not

Not a next odd-lift attack on `1517`. Not a CycleExtrema rewrite.
Not a generic “Juggler framework”. Not a Paper A edit.
