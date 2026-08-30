# Juggler leftover-class certificate harvest

Status: **EXPLORATORY**

Standalone computational phase on the Juggler floor-power map. It
adapts the parked Word Atlas GPU engine into a first-descent sieve.
It is **not** a Word Atlas recensus, not a new atlas language tag,
not a Research Engine control-layer experiment, not Paper A or
Paper B, and not a claim that every positive integer reaches 1.

## Problem

Among \(n\le X\), what first contracting words fire on the complement
of \(\{E, OE, OOEE\}\), and does that leftover dictionary drift with
scale?

## Exact statement

A **certificate** is the first realized word \(w\) with
\(T_{|w|}(n)<n\). Coarse bins are

- \(E\) — even \(n\ge 2\) (Paper A Theorem 4.1)
- \(OE\) — odd-to-even (Theorem 4.1)
- \(OOEE\) — first descent is exactly `OOEE`
- leftover — first descent is none of the above

The leftover-class histogram is the count of leftover starts by
first contracting packed word. Absence under a bound is
`NOT OBSERVED WITHIN SEARCH BOUND`. This is not a halt theorem.

## Current literature

- Uniform short certificates \(E\) / \(OE\) —
  **EXACT — LEAN VERIFIED** (Paper A Theorem 4.1)
- `OOEE` as a uniform contracting class —
  Paper B / two-step parity harvest
- Word Atlas —
  **PARK** as machinery
  ([juggler_word_atlas.md](juggler_word_atlas.md))
- Published totality through \(7{,}110{,}200\) —
  `derneueschwan-2026-juggler`; through \(10^6\) — Weisstein
- Every start reaches 1 — not claimed

Project relationship: **extended**. A leftover-class census on
existing certificates. Do not reopen
`JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`.

## Branch budget

```text
Mathematical target     Among n ≤ X, what first contracting words fire
                        on the complement of {E, OE, OOEE}, and does
                        that leftover dictionary drift with scale?
Novelty hypothesis      A short stable leftover list (or a persistent
                        bias vs product density) that is invisible at
                        the published 7e6 totality bound.
Falsifier               Histogram is only OOOO* until an even letter,
                        with no new shape and no scale drift — then
                        the sieve is a verification bound.
Existing machinery      Atlas Kernel A + Wide8 floor_power; packed
                        O/E words; orbit_until_drop; Theorem 4.1
                        (E / OE); Paper B OOEE class
Maximum Phase-0 scope   Harvest kernel; leftover-word histogram;
                        coarse counts; overflow CPU merge; science
                        at 10^9; optional 10^10 slabs. No Lean, no
                        new atlas language, no per-n storage.
Promotion criterion     Stable leftover dictionary whose frequencies
                        match or stably bias Paper B product densities
Stop criterion          Only “still reaches 1”; machinery gravity
                        (Nsight, PE recensus, CLI/UI, automata)
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- first contracting word —
  **COMPUTATIONALLY VERIFIED** as a bounded observation
- coarse split \(E\) / \(OE\) / \(OOEE\) / leftover —
  **COMPUTATIONALLY VERIFIED** as a bounded observation
- leftover `run_signature` grouping —
  **OBSERVATION**
- scale-split total variation of leftover shares —
  **OBSERVATION**
- global halt — not claimed
- new atlas language — not added

## Experiments

- Probe: `research.juggler_sequence.certificate_harvest`
- Native: `juggler-atlas-census --mode harvest`
- Records: [juggler_certificate_harvest.md](../research/juggler_certificate_harvest.md),
  [juggler_certificate_harvest.json](../research/juggler_certificate_harvest.json)
- Dataset: `data/research/juggler/certificate_harvest/`
- Tests: `tests/research/juggler_sequence/test_certificate_harvest.py`

Science window: \(2\le n\le 10^9\), \(k\le 20\), scale split at
\(10^8\). Tests use \(n\le 400\). Optional \(10^{10}\) only if
overflow and uncapped stay rare. No Lean. No new `LANGUAGE_IDS`.

## Conjectures

None opened.

## Counterexamples

Recorded after the science window.

## Formalization

None added. Existing `FiniteProgress`, `even_finiteProgress`, and
`odd_even_finiteProgress` already contain the uniform certificates.
No `CertificateHarvest.lean`. No `sorry`. Paper A is unchanged.

## Results

Recorded after the science window. Classification is produced by
`certificate_harvest.classify`.

## Open questions

Whether the leftover first-contracting dictionary is a short unary
\(O^+E^+\) list or a scale-stable mixed family.

## Decision

Pending the Phase-0 science window. The branch will end in exactly
one of PROMOTE, PARK, or CLOSE after the leftover-class histogram.

## Publication assessment

Status: `EXPLORATORY`. A leftover-class histogram, not a paper
candidate and not a Juggler totality result.
