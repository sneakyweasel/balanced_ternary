# Frozen Engine campaign: open order-10 LRS Positivity instance

Status: **EXPLORATORY**

This is an engine-capability campaign on companion-window iteration
and first-coordinate nonnegativity. It does **not** claim a Positivity
decision procedure, a negative term of the survey's order-10 sequence,
or a universal nonnegativity theorem for that sequence. Adapters live in
`research.positivity_lrs`. There is no `PositivityAttack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Can frozen Research Engine v2, augmented only by v2.2 research memory,
make useful mathematical progress on a genuinely unresolved order-10
Positivity instance using only its existing vector/matrix, reachability,
invariant, quotient, modular, and obstruction machinery?

## Exact statement

On hint-free `ProblemSpec` adapters whose state is an integer window
and whose transition is the exact linear shift that appends one
declared combination of the window, with accepting states those whose
first coordinate is negative, does unmodified `ResearchLoop`

1. recover the companion matrix in dimension 2;
2. certify small negative observations by exact finite reachability;
3. distinguish a finite negative prefix from nonnegativity from \(n=0\);
4. refrain from equating a nonnegative finite window with universal
   nonnegativity on the order-10 flagship?

Computational budget (adapter, not an attack):

- maximum search index \(64\);
- maximum coordinate bit length \(512\);
- at most 16 planner steps / 32 residual states;
- vector-census cube of side \(25\) skipped when \(25^d>50000\)
  (`COMPUTATION_EXHAUSTED`, not a theorem).

## Current literature

- Bacik–Karimov–Luca–Nieuwveld–Ouaknine–Purser–Worrell, *A survey of
  the Skolem and Positivity Problems*, 2026
  (`bacik-et-al-2026-skolem-positivity-survey`). Section 8.4 sequence
  (16) is a simple order-10 integer LRS whose Positivity status is
  unresolved. **OPEN** / **COMPUTATIONAL**.
- Ouaknine–Worrell, *Positivity Problems for Low-Order Linear
  Recurrence Sequences*, 2014
  (`ouaknine-worrell-2014-positivity-low-order`). Positivity decidable
  for integer LRS of order \(\le 5\). **THEOREM**.
- Ouaknine–Worrell, *On the Positivity Problem for Simple Linear
  Recurrence Sequences*, 2014
  (`ouaknine-worrell-2014-simple-positivity`). Positivity decidable for
  simple integer LRS of order \(\le 9\). **THEOREM**.

Project relationship: **engine diagnosis**. No new Positivity theorem
is claimed.

## Branch budget

```text
Mathematical target     Can frozen v2 exploit companion-matrix dynamics
                        to make progress on the 2026 order-10 Positivity
                        instance, and is GLOBAL_REASONING the same
                        cluster as Skolem?
Novelty hypothesis      A new exact invariant, infinite-index sign
                        restriction, or a diagnostic that half-space
                        safety fails for the same finite-to-infinite gap.
Falsifier               Adapter leaks roots / Positivity name / survey
                        status; new attacks; equating CERTIFIED_ON_WINDOW
                        with universal nonnegativity.
Existing machinery      Unmodified ResearchLoop; vector_affine;
                        matrix-word; closure; modular; v2.2 memory ingest;
                        post-run residue/sign probes.
Maximum Phase-0 scope   Calibrations A–E + flagship F + Lean KNOWN
                        identities + memory ingest + dossier.
Promotion criterion     A new exact invariant or infinite exclusion.
Stop criterion          New Positivity/spectral/p-adic attack; claiming
                        the instance is decided; machinery gravity.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required. Digit-fold cores remain a comparison cluster.

## Candidate operations / invariants

- Calibration A: nonnegative last-row coefficients preserve the
  nonnegative orthant. **EXACT — LEAN VERIFIED**. **KNOWN**.
- Calibration B: first coordinate negative at index \(1\).
  **EXACT — LEAN VERIFIED**. **KNOWN**.
- Calibration C: first coordinate negative at index \(2\).
  **EXACT — LEAN VERIFIED**. **KNOWN**.
- Calibration D: first coordinate negative at index \(1\); later
  nonnegative tail on the window. **EXACT — LEAN VERIFIED**. **KNOWN**.
  Eventual nonnegativity is not nonnegativity from \(n=0\).
- Flagship: initial window nonnegative; no negative on \(\{0,\ldots,64\}\).
  **COMPUTATIONALLY VERIFIED** on that index set. Not a universal theorem.
- No universal nonnegativity theorem. **OBSERVATION**.

## Experiments

- `tests/research/positivity_lrs/test_positivity_lrs.py`
- Runner: `research.positivity_lrs.runner.run_campaign`
- Scout (never imported by the adapter): `research.positivity_lrs.scout`

## Conjectures

None opened. The survey instance remains literature-open.

## Counterexamples

- “All terms are nonnegative.” **REFUTED** on calibrations B, C, and D.
- “A finite negative prefix is compatible with nonnegativity from \(n=0\).”
  **REFUTED** on D.
- “The nonnegative orthant is invariant under the flagship last row.”
  **REFUTED** (mixed signs in the last row).
- “A modulus in \(2,\ldots,32\) is a sign theorem.” **REFUTED** as an
  integer claim: residues are not signs.
- “Finite seed closure means the map is contracting.” **REFUTED** as a
  diagnosis on expanding companion windows.

## Formalization

`formal/Problems/Engine/CompanionObservation.lean`. KNOWN identities. No
`sorry`. No ledger row.

## Results

Dimension 2 recovers the companion matrices and certifies easy negative
witnesses. Dimension 3 already yields census `UNRESOLVED`. The order-10
flagship is `CERTIFIED_ON_WINDOW` on \(\{0,\ldots,64\}\),
`COMPUTATION_EXHAUSTED` for the census, and `UNKNOWN` as a Positivity
answer. Memory ingest places the flagship in the existing
`GLOBAL_REASONING` cluster. See sections A–N.

## Open questions

Does survey sequence (16) satisfy \(u_n\ge 0\) for every \(n\in\mathbb N\)?
Frozen v2 does not answer this.

## Decision

**PARK**. Frozen v2 reconstructs the companion matrix in dimension 2
and certifies easy negative witnesses, then meets the known order-10
Positivity barrier: the vector census cannot even be run in dimension
10, and already fails to fit a matrix in dimension 3. No new invariant
or infinite-horizon sign restriction. The flagship answer remains
`UNKNOWN`. The reusable deficiency is the same `GLOBAL_REASONING`
cluster as Skolem hyperplane reachability. Campaign label:
`ENGINE_LIMITATION`. Do not implement a Positivity solver.

Best next question: which frozen-engine target still lies inside the
existing low-dimensional affine language, now that both existential
hyperplane reachability and universal half-space safety have been
recorded as the same finite-to-infinite gap?

## Publication assessment

Status: `EXPLORATORY`.

No paper candidate. The mathematical yield is an engine-boundary
measurement against a genuine open instance.

---

### A. Scout dossier

See `scout.py` and Current literature. Classified claims:

| Claim | Tag |
|-------|-----|
| Positivity decidable for integer LRS of order \(\le 5\) | THEOREM |
| Positivity decidable for simple integer LRS of order \(\le 9\) | THEOREM |
| Sequence (16) is simple of order 10 and ultimately positive | THEOREM |
| \(u_n\ge 0\) for \(n\le 10^6\) | COMPUTATIONAL |
| Sequence (16) has no zeros | COMPUTATIONAL |
| No semialgebraic invariant certifies \(u_n\ge 0\) | THEOREM |
| Whether \(u_n\ge 0\) for every \(n\) | UNKNOWN |
| Modular methods do not yield Positivity certificates | THEOREM |

Closed form, roots, and the growth-theorem onset stay in the scout.

### B. Blind adapter

`CompanionObsSpec`: integer window; dummy control; first-coordinate
observation; accepting iff that coordinate is \(<0\);
`affine_system()=None`; successor the declared linear shift. Empty
menu at a negative observation, at phase \(0\), or past the bit-length
cap.

No Positivity name, no roots, no closed form, no “this instance is
open”. Scout is not imported by `spec.py` / `adapter.py` / `planner.py`.

Vector-census attacks are skipped only when \(25^d>50000\), via the
existing `skip_attacks` hook. That is a declared computational budget,
not a new attack.

### C. Calibration results

| Role | Spec | Engine |
|------|------|--------|
| A trivially nonnegative | `companion_obs_nonneg_small` | `CERTIFIED_ON_WINDOW`; recovered \(M=((0,1),(1,1))\); orthant step exact; closure truncated 33; `CONTINUE`; live ingest also flags `GLOBAL_REASONING` because the infinite tail is not certified |
| B early negative | `companion_obs_early_negative` | `NEGATIVE_WITNESS` at index 1; recovered \(M=((0,1),(1,1))\); closure size 2 complete; `CONTINUE` |
| C periodic sign | `companion_obs_periodic_sign` | `NEGATIVE_WITNESS` at index 2; recovered \(M=((0,1),(-1,0))\); closure size 3; `CLOSE` (low delta from B) |
| D finite negative prefix | `companion_obs_finite_negative` | `NEGATIVE_WITNESS` at index 1; last negative at 3; later nonnegative tail on the window; `CLOSE`. Eventual nonnegativity is not nonnegativity from \(n=0\) |
| E order-3 classified | `companion_obs_order3` | no negative in bound; vector census `UNRESOLVED`; `CONTINUE` |
| F open order-10 | `companion_obs_order10` | see below |

### D. Open order-10 results

Blind prefix:

\[
35,574,34592,8999992,115734548,5682747424,1837938758372,\ldots
\]

Independently matching the closed form \(w_n^2-2^n\). No negative on
\(\{0,\ldots,64\}\): `CERTIFIED_ON_WINDOW` on that index set,
`COMPUTATION_EXHAUSTED` for the unbounded question, `UNKNOWN` as a
Positivity answer. Vector census skipped (\(25^{10}\)). Functional bound
of the first coordinate is refuted by growth.

### E. Regime diagnosis

Flagship (after A–E are in the same corpus):

| Field | Engine |
|-------|--------|
| `ResearchDecision` | `CLOSE` (“no new structural regime”) |
| Vector census | `COMPUTATION_EXHAUSTED` (cube \(25^{10}\)) |
| Semantic class | `INTEGER_VECTOR\|SINGLETON\|UNIVERSAL_DESCENT_REFUTED\|UNBOUNDED_SAMPLE` |
| Affine control | `UNOBSERVED` |
| Nearest | `companion_obs_order3` (delta `LOW`) |
| Closure | size 33, incomplete |

Dimension-2 calibrations recover `VECTOR` affine control and the exact
companion matrices. Dimension 3 already yields census `UNRESOLVED`.
Stopping at a negative observation on B/C/D is billed
`FINITE_CONTRACTING`; that is seed-orbit coarseness, not numerical
contraction of the linear map.

### F. Existing attack results

On the flagship: reconnaissance `OBSERVATION`; `vector_affine` and
`matrix_word_invariant` `COMPUTATION_EXHAUSTED`; closure
`INCONCLUSIVE`; functional `REFUTED`; separation `SUPPORTED`; quotient
`INCONCLUSIVE`. Control-stack, modular, affine, reverse, block,
spectral, factorization, and symmetry attacks are `INAPPLICABLE`
without a supplied `AffineSystem`. Modular post-run residues on
\(m=2,\ldots,32\) are not a sign theorem.

### G. Invariants and obstructions

No new invariant. The nonnegative orthant is invariant on calibration A
and is **not** invariant for the flagship last row. No class obstruction
that excludes a later negative term of F.

### H. Counterexamples

See Counterexamples above. Flagship all-terms-nonneg remains
**INCONCLUSIVE** on the search bound.

### I. Mathematical yield

```text
Known rediscoveries:     companion shift; easy negatives; Fibonacci-like
                         orthant preservation; prefix of survey (16)
New exact identities:    none beyond the definition
New invariants:          none
New modular exclusions:  none
New negative witnesses:  none on the flagship
New counterexamples:     orthant invariance on the flagship last row
New conjectures:         none
New reductions:          none
Lean-certified results:  companion_obs_* (KNOWN; no ledger)
Potentially new mathematics: none
Unresolved bottlenecks:  3-point vector census vs dim>=3; 25^d grid;
                         unbounded Positivity for sequence (16)
Engineering changes:     0
```

No `POTENTIALLY_NEW_THEOREM`.

### J. Failure-memory update

Flagship ingested into `ResearchMemory` with

- `GLOBAL_REASONING` / `finite_to_infinite_certificate` /
  `LANGUAGE_ADEQUATE` / `global_reachability`
- `COMPUTATIONAL` / `finite_budget_exhausted`

This is the same cluster key as Skolem order 6, Carelli \(R^+\), and
BB-5. Grey loot records that changing

\[
\exists n:\; e_1^\top x_n=0
\]

into

\[
\forall n:\; e_1^\top x_n\ge 0
\]

does not create a new frozen-engine capability.

### K. Lean

`Problems.Engine.CompanionObservation`: companion step, calibration
witnesses, orthant preservation, flagship tenth term and nonnegative
initial window. KNOWN. No `sorry`.

### L. Prior-art reconciliation

| Literature | Engine |
|------------|--------|
| Survey sequence (16) initials | independently used as a blind window; prefix recomputed from the recurrence |
| \(u_n\ge 0\) for \(n\le 10^6\) | engine only saw \(\{0,\ldots,64\}\); weaker |
| Ultimate positivity via Subspace Theorem | **not recovered** |
| No semialgebraic invariant | **not recovered** |
| Baker / order \(\le 9\) simple Positivity | calibration A is an order-2 nonnegative sequence; engine did not produce a universal certificate beyond the orthant step |
| Theorem 52 reduction to Skolem order 5 | **not recovered** (and not injected) |

All exact identities: `KNOWN_REDISCOVERY`. Finite window: `NEW_COMPUTATIONAL_OBSERVATION` about the **engine**, weaker than the literature \(10^6\) bound.

### M. ResearchLoop

Next target is selected from the mixed pool (increment, \(mx+r\),
hidden congruence, parity shear, integer polynomial) without override,
with `FailureLearningValue` supplied by v2.2 memory.

### N. Final decision

```text
ENGINE_LIMITATION
```

Laboratory branch: `PARK`. Flagship `ResearchDecision` recorded after
the live run. Engineering backlog: recurring `GLOBAL_REASONING` of
finite-to-infinite certificates on companion-matrix dynamics, now
covering both hyperplane reachability (Skolem) and half-space safety
(Positivity). Positivity answer for sequence (16): `UNKNOWN`.
Not `ESCALATE`. Do not implement a Positivity solver.
