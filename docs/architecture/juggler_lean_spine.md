# Juggler Lean spine

Live-tree pointer for `formal/Problems/Juggler`. The canonical
architecture dossier is
[juggler_lean_architecture.md](../problems/juggler_lean_architecture.md).
This note is not a research attack.

`EnvelopeState` implements one-sided cell comparison via
`map_word`. `PowerCorridor` is the two-sided collision.
`AboveAnchor` is the shared prefix geometry. `CycleMin` and
`MinimalNonTerm` consume it downward. Paper A
(`Problems.JugglerPaper`) is unchanged.

## Live import graph

```text
Dynamics → Iteration → Termination → Itinerary → WordStats
                                              ↓
                                           Envelope
                                              ↓
                                           Corridor
                                    ↓                 ↓
                              Progress          MinimumRelative
                                    ↓                 ↓
                                 Minimal          CycleCore
                                    ↓                 ↓
                                 Scale            CycleObstructions
                                    ↓                 ↓
                              Residuals          CycleExtrema / leftover
```

`CycleCore` imports `Envelope` + `Cells` + `MinimumRelative`, not
`Residuals`. `Cycles.lean` re-exports Core + Obstructions + Extrema.

## Concept classification

| Kind | Objects | Home |
|------|---------|------|
| Primitive | `floorPower` / `follows` / words | `Dynamics.lean`, `Itinerary.lean`, `WordStats.lean` |
| Primitive | `EnvelopeState` / `map_word` / `envelope_lt_pow` | `Envelope.lean` |
| Primitive | `PowerCorridor` / Corollaries A–C | `Corridor.lean` |
| Primitive | `AboveAnchor` / Corollaries D–F | `MinimumRelative.lean` |
| Primitive | `HasFiniteStop` | `FirstPassage.lean` |
| Primitive | `DescentCertificate` / `FiniteProgress` | `Certificates.lean`, `Progress.lean` |
| Derived | `PowerBound` as `A=2^{\|w\|}`, `B=3^{\#O}` | `Envelope.lean` |
| Derived | `power_bound_word` / `power_bound_lt_pow` | `Envelope.lean` |
| Consumer | `CycleMin` + `aboveAnchor_of_cycleMin` | `CycleCore.lean` |
| Consumer | `MinimalNonTerm` + `aboveAnchor_of_minimalNonTerm` | `Minimal.lean` |
| Consumer | named `no_cycle_word_*` | `CycleObstructions.lean` |
| Consumer | `ReturnBelow` | `Residuals.lean` |

`EscapeEpisode` is Python-only. Do not merge `HasFiniteStop` with
`FiniteProgress`.

## Accepted debt

- `PowerBound` append lemmas stay for Defect. Comparison is
  `EnvelopeState.map_word`; `of_follows` is `(refl n).map_word`.
- Short CycleWord exclusions through length 5 stay in `CycleCore`.
- Named Escape words, leftover census, Defect / Equality,
  CycleExtrema stay as research wrappers. No rename campaign.
- `JugglerPaper.lean` already imports `Envelope`. Do not mention
  `EnvelopeState` in Paper A comments.
- Python `has_named` / `lean_api_present` are string checks.
  `lake build` is the formal regression.
- `CycleCore` sees `Progress` only transitively through
  `MinimumRelative`. It does not import `Residuals` or `Minimal`.

## What this note is not

Not a next odd-lift attack on `1517`. Not a CycleExtrema rewrite.
Not a generic “Juggler framework”. Not a Paper A edit.
