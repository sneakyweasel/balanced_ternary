# Juggler word atlas

Status: **EXPLORATORY**

Standalone computational microscope for the finite Juggler \(O/E\)
word language. It is **not** a Research Engine control-layer
experiment, not a reopening of the closed word-language attack, and
not a claim that every positive integer reaches 1.

## Problem

Build a reusable, exact, GPU-first census of finite \(O/E\) words:
which words are observed under a configured bound, with minimum
witnesses and separate language tags.

## Exact statement

Keep the quantifiers existential. A word is experimentally realized
when some scanned \(n\) follows it. Failure to find a realizer is

\[
\texttt{NOT\_FOUND\_WITHIN\_BOUND},
\]

never global non-realizability. Persistent-expanding rows use the
repository predicate `PersistentExpandingResidual` and are stored as
`PE_CERTIFIED`. The GPU does not classify PE in Milestone 1.

This says nothing about totality.

## Current literature

- `follows` / `image` / `floorPower` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.Itinerary` and
  `Dynamics`.
- `PersistentExpandingResidual` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.Residuals`.
- Existential languages `jugglerLanguage` /
  `expandingLanguage` / `persistentExpandingLanguage` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.WordLanguage`.
- Word-language arrangement attack —
  **CLOSE** as `JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`. This atlas does
  not reopen that claim.

Project relationship: **extended** (infrastructure on existing
predicates).

## Branch budget

```text
Mathematical target     Build a reusable, exact, GPU-first census of
                        finite O/E words: which words are observed
                        under a bound, with min witnesses and
                        separate language tags.
Novelty hypothesis      None in M1. This is infrastructure for later
                        questions, not a new forbidden-factor law.
Falsifier               GPU itinerary disagrees with the CPU/Lean
                        floorPower/follows fixtures, or PE_PROXY is
                        written as PE_CERTIFIED.
Existing machinery      floor_power, follows_word, classify_step,
                        walk_pe_run, WordLanguage.lean, closed
                        word_language.py prototype
Maximum Phase-0 scope   Milestone 1 only: k<=12, n<=10^6, Kernel A,
                        compact tables, validation, manifest
Promotion criterion     Not applicable in M1. Default is PARK as
                        machinery after the validation suite passes.
Stop criterion          Machinery gravity (Kernel B, Nsight campaign,
                        automata, new conjecture); any claim that
                        absence under a bound is global prohibition
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Packed \(O/E\) words, LSB = first symbol, `0=E`, `1=O` —
  **OBSERVATION** (encoding only)
- Observed `min_realizer` under a scan bound —
  **COMPUTATIONALLY VERIFIED**, not a global minimum theorem
- `PE_CERTIFIED` via `classify_step` / `walk_pe_run` —
  **COMPUTATIONALLY VERIFIED** against Lean fixtures
- `PE_PROXY` — unused in Milestone 1; must not be mixed with
  `PE_CERTIFIED`
- Factor complexity \(p(r)\) as a query over observed words —
  **OBSERVATION**; absence is `NOT OBSERVED WITHIN SEARCH BOUND`

## Experiments

- Engine: `atlas/` CUDA/C++ census (`juggler-atlas-census`)
- Python API: `research.juggler_sequence.atlas`
- CLI: `juggler-atlas build|validate|factors|continuations|benchmark`
- Data: [word_atlas](../../data/research/juggler/word_atlas/)
- Milestone 1 window: word length \(\le 12\), \(n\le 10^6\)
- Tests: `tests/research/juggler_sequence/test_word_atlas.py`

Do not default-test the later scientific window \(k\le 20\),
\(n\le 10^8\).

## Conjectures

None opened in `conjectures/`.

## Counterexamples

None. This branch is infrastructure. Closed-branch counterexamples
stay in `juggler_word_language.md`.

## Formalization

None added. Certification uses existing
`formal/Problems/Juggler/` lemmas and hard-coded fixtures. No Lean
FFI. No `sorry`.

## Results

Milestone 1 ships a deterministic trajectory census, compact
Parquet/SQLite tables, a `PE_CERTIFIED` host post-pass, and a
three-way validation gate. On this machine Kernel A matched the
Python exact reference on every filled slot for `k<=12`,
`n<=10^6` (`GPU VERIFIED`; wide intermediates overflow to the
CPU reference). Fixtures `floorPower`, `OOE` at 5, and the 365 /
1999 PE chains match Lean (`CPU VERIFIED` / `LEAN-CERTIFIED`).
Stored word metadata recomputes from packed bits. No new
language law is claimed.

## Open questions

The leftover scientific question is unchanged: is there any
arithmetic, other than the integer \(y\) itself, that decides
whether a persistent residual landing stays odd-to-odd? The atlas
does not answer it. A later phase may scale the census; that is a
separate decide step.

## Decision

**PARK** as reusable machinery. Milestone 1 is an experimental
microscope, not a theorem and not a reopening of
`JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`. Do not claim termination. Do
not treat `NOT_FOUND_WITHIN_BOUND` as a prohibition.

Best next question: after a validated scale-up, does the
`PE_CERTIFIED` language show any factor structure beyond the known
\(O^a E^b\) grammar *inside a stated search bound*, recorded only as
`COMPUTATIONALLY OBSERVED` / `NOT OBSERVED WITHIN SEARCH BOUND`?

## Publication assessment

Status: `EXPLORATORY`. A computational census pipeline, not a paper
candidate and not a Juggler totality result.
