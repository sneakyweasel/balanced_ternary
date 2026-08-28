# Juggler minimal-bad survival signatures

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1. It does not reopen the closed
well-ordering census
([juggler_minimal_counterexample.md](juggler_minimal_counterexample.md))
or the closed stopping-prefix branch
([juggler_stopping_prefix.md](juggler_stopping_prefix.md)).

## Problem

Does “minimality plus exact inverse arithmetic” produce a new
constraint on a hypothetical least bad state, or only the already
proved leftover that one-step and two-step certificates miss exactly
the odd-to-odd class?

## Exact statement

Let \(T\) be `floorPower`. Write `Good = ReachesOne`,
`Bad = ¬ReachesOne`, and `MinimalNonTerm n` for a least bad state.
A one-step predecessor certificate from a smaller target covers \(n\)
exactly when \(T(n)<n\). A two-step certificate covers \(n\) when
\(T^2(n)<n\). Let `SurvivalSignature(n)` be the pair of those
failures together with the first two letters of the orbit. Decide
whether the surviving class is anything other than

\[
n\text{ odd and }T(n)\text{ odd},
\]

already isolated by `unresolved_is_odd_odd`, or whether inverse
closure of \([1,n-1]\) is anything other than “some iterate is
\(<n\)”.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**.
- `MinimalNonTerm` normal form — **EXACT — LEAN VERIFIED**.
- `PredClosure ↔ ReachesOne` — **EXACT — LEAN VERIFIED**.
  **REPARAMETERIZATION**. Branch **CLOSE**
  (`juggler_minimal_counterexample`).
- `finiteProgress_of_not_odd_odd` / `unresolved_is_odd_odd` —
  **EXACT — LEAN VERIFIED**. Branch **PROMOTE**
  (`juggler_progress_coverage`).
- Unbounded \(F_\tau\) — **REPARAMETERIZATION**. Branch **CLOSE**
  (`juggler_stopping_prefix`).

Project relationship: **independent** only if a new \(\Phi(n)\)
appears. The even rule \(T(2k)=k^2\) is a forward/inverse swap and
is not used. Totality remains unclaimed.

## Branch budget

```text
Mathematical target     Does SurvivalSignature add a constraint on
                        MinimalNonTerm beyond odd-to-odd leftover
                        and “the orbit never drops below n”?
Novelty hypothesis      Minimality plus exact inverse cells yields a
                        finite covering family or an impossible Φ(n)
Falsifier               Leftover = OO; inverse generation = first
                        descent; all statements KNOWN or
                        REPARAMETERIZATION
Existing machinery      MinimalNonTerm, UncoveredOneStep,
                        predClosure_iff_reachesOne,
                        finiteProgress_of_not_odd_odd,
                        even_good_of_sqrt_le, odd_not_pred_of_le,
                        floor_power, two_step, barrier_walk
Maximum Phase-0 scope   N=4000; one-step/two-step signatures;
                        leftover vs OO; residue diagnostic; decide
Promotion criterion     A new Φ(n) not already in Minimal.lean or
                        Progress.lean
Stop criterion          Leftover is OO; covering is descent;
                        tautology only
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

A leftover cylinder in least significant trits would have been a BT
observation. Phase-0 does not hunt a BT law.

## Candidate operations / invariants

- `MinimalNonTerm` — **EXACT — LEAN VERIFIED**. **KNOWN**
- `T^k(n)=m` and `Good m` implies `Good n` —
  **EXACT — LEAN VERIFIED**. **KNOWN**
- one-step cover \(T(n)<n\) — **EXACT — LEAN VERIFIED** for evens
- odd \(n\ge 3\) never one-step covered — **EXACT — LEAN VERIFIED**
  (`odd_not_pred_of_le`)
- leftover of one-step and two-step = odd-to-odd — **KNOWN**
- `PredClosure ↔ ReachesOne` — **REPARAMETERIZATION**
- inverse closure of \([1,n-1]\) equals first descent —
  **REPARAMETERIZATION**
- new \(\Phi(n)\) — **REFUTED** on the Phase-0 window
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.minimal_survival`
- Records: [juggler_minimal_survival.md](../research/juggler_minimal_survival.md),
  [juggler_minimal_survival.json](../research/juggler_minimal_survival.json)
- Data: `data/research/juggler/minimal_survival/`
- Tests: `tests/research/juggler_sequence/test_minimal_survival.py`
- The Research Engine control layer is not modified.

## Conjectures

None opened.

## Counterexamples

- “Minimality plus inverse arithmetic is a new mechanism.” **REFUTED**:
  leftover is odd-to-odd; inverse generation is first descent.
- “Every even predecessor exists only on squares / `T(2k)=k^2`.”
  **REFUTED**: `T` on evens is `⌊√n⌋`; every `m` has an even cell.
- “Leftover occupies one residue class.” **REFUTED**: residues
  `{'1': 278, '3': 229, '5': 280, '7': 222}`.

## Formalization

None added. Existing lemmas in `Minimal.lean`, `MinimalClosure.lean`,
and `Progress.lean` are cited, not restated. No
`research.juggler.minimal_bad` / `predecessor_cover` modules.

## Results

See [juggler_minimal_survival.md](../research/juggler_minimal_survival.md).
Classification **MINIMAL_SURVIVAL_COMPLEX**.

## Open questions

Whether every positive integer reaches 1. Well-ordering plus
one-step/two-step inverse arithmetic does not answer it.

## Decision

**CLOSE**. SurvivalSignature leftover is exactly the odd-to-odd class (1009 starts on n≤4000). Every even is one-step covered; no odd n≥3 is. Inverse generation from a smaller state is first descent: every leftover start in the window drops below itself. Leftover residues mod 8 are [1, 3, 5, 7]. All of this is KNOWN (MinimalNonTerm, UncoveredOneStep, unresolved_is_odd_odd) or a REPARAMETERIZATION of descent. Minimality plus inverse arithmetic does not create a new Φ(n). A branch whose surviving statements
are `KNOWN` or `REPARAMETERIZATION` is a `CLOSE`.

Best next question: none from this branch. Do not launch Phase 1.

## Publication assessment

Status: `ARCHIVED`.

The survival census repackages `unresolved_is_odd_odd` and first
descent. There is no new theorem and no paper distinction.
