# Frozen Engine campaign: open order-6 Skolem instance

Status: **EXPLORATORY**

This is an engine-capability campaign on companion-window iteration
and first-coordinate vanishing. It does **not** claim a Skolem
decision procedure, a zero of the survey's order-6 sequence, or a
universal zero-free theorem for that sequence. Adapters live in
`research.skolem_lrs`. There is no `SkolemAttack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Can frozen Research Engine v2 make useful mathematical progress on a
genuinely unresolved order-6 Skolem instance using only its existing
vector/matrix, reachability, invariant, and obstruction machinery?

## Exact statement

On hint-free `ProblemSpec` adapters whose state is an integer window
and whose transition is the exact linear shift that appends one
declared combination of the window, does unmodified `ResearchLoop`

1. recover the companion matrix in dimension 2;
2. certify small zeros by exact finite reachability;
3. fail to reconstruct the same matrix in dimension 3 by the frozen
   3-point census;
4. refrain from equating a finite zero-search with non-existence on
   the order-6 flagship?

Computational budget (adapter, not an attack):

- maximum search index \(64\);
- maximum coordinate bit length \(512\);
- at most 16 planner steps / 32 residual states;
- vector-census cube of side \(25\) skipped when \(25^d>50000\)
  (`COMPUTATION_EXHAUSTED`, not a theorem).

## Current literature

- Bacik–Karimov–Luca–Nieuwveld–Ouaknine–Purser–Worrell, *A survey of
  the Skolem and Positivity Problems*, 2026
  (`bacik-et-al-2026-skolem-positivity-survey`). Order-6 sequence
  (13) is unresolved. **OPEN** / **COMPUTATIONAL**.
- Lipton–Luca–Nieuwveld–Ouaknine–Purser–Worrell, LICS 2022
  (`lipton-et-al-2022-skolem-conjecture`). Conditional order-5;
  different order-6 example. **THEOREM** (conditional) / **KNOWN**.
- Luca–Ouaknine–Worrell, arXiv:2607.15510, 2026
  (`luca-ouaknine-worrell-2026-conjectural-decidability`). Large
  zeros sparse; Cramér-type conditional decidability. **CONJECTURE**
  / **THEOREM** (unconditional sparsity).
- Kenison–Nieuwveld–Ouaknine–Worrell, TheoretiCS 2025
  (`kenison-et-al-2025-order-4-skolem`). Order 4 complete. **THEOREM**.

Project relationship: **engine diagnosis**. No new Skolem theorem is
claimed.

## Branch budget

```text
Mathematical target     Can frozen v2 exploit companion-matrix reachability
                        to make progress on the 2026 order-6 Skolem instance?
Novelty hypothesis      A new exact invariant, infinite index exclusion, or
                        finite-dimensional obstruction surviving prior-art.
Falsifier               Adapter leaks roots / p-adic / Skolem name; new
                        attacks; equating NO ZERO FOUND with NO ZERO EXISTS.
Existing machinery      Unmodified ResearchLoop; vector_affine; matrix-word;
                        closure; functional; post-run residue probes.
Maximum Phase-0 scope   Calibrations A–D + flagship E + Lean KNOWN identities
                        + ResearchLoop next + dossier.
Promotion criterion     A new exact invariant or infinite exclusion.
Stop criterion          New Skolem/p-adic attack; claiming the instance is
                        decided; machinery gravity.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required. Digit-fold cores remain a comparison cluster.

## Candidate operations / invariants

- Calibration A: observation \(0\) at index \(3\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- Calibration B: positive windows stay positive. **EXACT — LEAN VERIFIED**. **KNOWN**.
- Calibration C: observation \(0\) at the first successor. **EXACT — LEAN VERIFIED**. **KNOWN**.
- Flagship: first negative observation at index \(11\). **EXACT — LEAN VERIFIED**. **KNOWN** (after the fact).
- No universal zero-free theorem. **OBSERVATION**.

## Experiments

- `tests/research/skolem_lrs/test_skolem_lrs.py`
- Runner: `research.skolem_lrs.runner.run_campaign`
- Scout (never imported by the adapter): `research.skolem_lrs.scout`

## Conjectures

None opened. The survey instance remains literature-open.

## Counterexamples

- “The first coordinate never vanishes.” **REFUTED** on calibrations A and C.
- “The flagship observation has fixed sign.” **REFUTED** at index \(11\).
- “A modulus in \(2,\ldots,32\) excludes integer zeros of the flagship.”
  **REFUTED** as an integer claim: every such modulus has a prefix residue \(0\).
- “Finite seed closure means the map is contracting.” **REFUTED** as a
  diagnosis on expanding companion windows.

## Formalization

`formal/Problems/Engine/CompanionShift.lean`. KNOWN identities. No
`sorry`. No ledger row.

## Results

Filled after the campaign run. See sections A–N below.

## Open questions

Does the survey sequence (13) vanish for some \(n\in\mathbb N\)? Frozen
v2 does not answer this.

## Decision

**PARK**. Frozen v2 reconstructs the companion matrix in dimension 2
and certifies the easy zeros, then meets the known order-6 barrier:
the vector census cannot even be run in dimension 6, and already
fails to fit a matrix in dimension 3. No new invariant or infinite
exclusion. The flagship `ResearchDecision` is `CLOSE` (low delta from
the order-3 census failure). The reusable deficiency of the frozen
census language is recorded as an engineering `ENGINE_LIMITATION`
backlog item, not as a Skolem theorem.

Best next question: which frozen-engine target still lies inside the
existing low-dimensional affine language, now that this
high-dimensional census barrier is recorded?

## Publication assessment

Status: `EXPLORATORY`.

No paper candidate. The mathematical yield is an engine-boundary
measurement against a genuine open instance.

---

### A. Scout dossier

See `scout.py` and Current literature. Classified claims:

| Claim | Tag |
|-------|-----|
| Skolem decidable for integer LRS of order \(\le 4\) | THEOREM |
| Skolem open for general order \(\ge 5\) | OPEN |
| Survey sequence (13) has no modular or semialgebraic certificate | THEOREM |
| \(u_n\neq 0\) for \(n\le 10^{1000}\) | COMPUTATIONAL |
| Whether any integer zero exists | OPEN |
| Zeros modulo every \(m\ge 2\) | THEOREM |

Closed form, roots, and \(p\)-adic interpolants stay in the scout.

### B. Blind adapter

`CompanionShiftSpec`: integer window; dummy control; first-coordinate
observation; accepting iff that coordinate is \(0\);
`affine_system()=None`; successor the declared linear shift. Empty
menu at a zero, at phase \(0\), or past the bit-length cap.

No Skolem name, no roots, no closed form, no “this instance is open”.
Scout is not imported by `spec.py` / `adapter.py` / `planner.py`.

Vector-census attacks are skipped only when \(25^d>50000\), via the
existing `skip_attacks` hook. That is a declared computational budget,
not a new attack.

### C. Calibration results

| Role | Spec | Engine |
|------|------|--------|
| A trivial zero | `companion_shift_zero_small` | `ZERO_WITNESS` at index 3; closure size 4 complete; recovered \(M=((0,1),(-2,3))\); `CONTINUE` |
| B obviously zero-free | `companion_shift_positive` | no zero in bound; recovered \(M=((0,1),(1,1))\); closure truncated 33; `CONTINUE` |
| C periodic zeros | `companion_shift_periodic` | `ZERO_WITNESS` at index 1; recovered \(M=((0,1),(-1,0))\); closure size 2; `CLOSE` (low delta from A) |
| D order-3 classified | `companion_shift_order3` | no zero in bound; vector census `UNRESOLVED`; `CLOSE` |
| E open order-6 | `companion_shift_order6` | see below |

### D. Open order-6 results

Blind prefix:

\[
12,49,374,6003,21520,150773,2711418,\ldots
\]

First negative term at index \(11\). No zero in \(\{0,\ldots,64\}\):
`FINITE_ZERO_FREE` on that index set, `COMPUTATION_EXHAUSTED` for the
unbounded question, `UNKNOWN` as a Skolem answer. Every modulus
\(2,\ldots,32\) has a residue-\(0\) observation in the same bound, so
there is **no** modular exclusion.

### E. Regime diagnosis

Flagship (after A–D are in the same corpus):

| Field | Engine |
|-------|--------|
| `ResearchDecision` | `CLOSE` (“no new structural regime”) |
| Vector census | `COMPUTATION_EXHAUSTED` (cube \(25^6\)) |
| Semantic class | `INTEGER_VECTOR\|SINGLETON\|UNIVERSAL_DESCENT_REFUTED\|UNBOUNDED_SAMPLE` |
| Affine control | `UNOBSERVED` |
| Nearest | `companion_shift_order3` (delta `LOW`) |
| Closure | size 33, incomplete |

Dimension-2 calibrations recover `VECTOR` affine control and the exact
companion matrices. Dimension 3 already yields census `UNRESOLVED`.
Stopping at a zero on A is billed `FINITE_CONTRACTING`; that is the
same seed-orbit coarseness as earlier campaigns, not numerical
contraction of the linear map.

### F. Exact reachability

A and C: exact finite paths to an accepting (first-coordinate \(0\))
state. B, D, E: truncated orbits, no accepting state in the closure
cap. Finite-range nonvanishing on \(\{0,\ldots,64\}\) for E is a
computer check, not the survey's \(10^{1000}\) certificate.

### G. Invariants and obstructions

No new invariant. No class obstruction that excludes zeros of E.
Matrix-word never ran on E. Functional bound of the first coordinate
is refuted by growth.

### H. Falsification

- Never vanishes: **REFUTED** on A and C; **INCONCLUSIVE** on E.
- Fixed sign / eventual positivity on E: **REFUTED** at \(11\).
- Modular exclusion on \(m=2,\ldots,32\): prefix zeros exist; not an
  integer theorem. (Literature Proposition 53 is stronger and was
  **not** given to the engine.)
- Finite reachable set on E: **REFUTED** on the search bound.

### I. Mathematical yield

```text
Known rediscoveries:     companion shift; easy zeros; Fibonacci-like
                         positivity; u_11 < 0; prefix of survey (13)
New exact identities:    none beyond the definition
New invariants:          none
New modular exclusions:  none
New zero witnesses:      none on the flagship
New counterexamples:     fixed-sign on the flagship at n=11
New conjectures:         none
New reductions:          none
Lean-certified results:  companion_shift_* (KNOWN; no ledger)
Potentially new mathematics: none
Unresolved bottlenecks:  3-point vector census vs dim>=3; 25^d grid;
                         unbounded Skolem for sequence (13)
Engineering changes:     0
```

| Result | Class |
|--------|-------|
| Easy zeros / positivity step | `KNOWN_REDISCOVERY` |
| Flagship prefix and \(u_{11}<0\) | `KNOWN_REDISCOVERY` |
| Census failure at \(d=3\) and skip at \(d=6\) | `NEW_COMPUTATIONAL_OBSERVATION` about the **engine** |
| No zero on \(\{0,\ldots,64\}\) | `NEW_COMPUTATIONAL_OBSERVATION` (weaker than the literature \(10^{1000}\) bound) |

No `POTENTIALLY_NEW_THEOREM`.

### J. Lean

`Problems.Engine.CompanionShift`: companion step, calibration
witnesses, positivity preservation, flagship eleventh term negative.
KNOWN. No `sorry`.

### K. Prior-art reconciliation

| Literature | Engine |
|------------|--------|
| Survey sequence (13) initials | independently used as a blind window; prefix recomputed |
| First negative \(u_{11}\) | recovered by iteration |
| Prop. 53: zeros mod every \(m\) | engine only saw prefix zeros for \(m=2,\ldots,32\); not the theorem |
| \(17\)-adic bound \(10^{1000}\) | **not recovered** |
| Congruence \(n\equiv 4\pmod{16}\) for any integer zero | **not recovered** |
| MSTV / Baker / interpolants | **not recovered** (and not injected) |
| Order \(\le 4\) decidability | calibration D is a known zero-free order-3 sequence; engine did not produce a universal certificate |

### L. Engineering backlog

Do **not** implement these:

1. Vector census `_fit_affine` is called on 3 points, so it cannot
   determine a matrix in dimension \(\ge 3\).
2. `collect_vector_samples` materializes a cube of side \(25^d\), which
   OOMs at \(d=6\).
3. No generic exact-power / modular-period attack on \(M^n x_0\).
4. No \(p\)-adic interpolant language in the frozen stack.

### M. ResearchLoop

Next target is selected from the mixed pool (increment, \(mx+r\),
hidden congruence, parity shear, integer polynomial) without override.

### N. Final decision

```text
PARK
```

Campaign: `PARK`. Flagship `ResearchDecision`: `CLOSE`. Engineering
backlog: `ENGINE_LIMITATION` of the frozen vector census at
dimension \(\ge 3\). Skolem answer for sequence (13): `UNKNOWN`.
Not `ESCALATE`.
