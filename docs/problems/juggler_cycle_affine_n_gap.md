# Juggler affine \(n\)-gap diagnostic

Status: **ARCHIVED** (Phase 0 decided)

Diagnostic of the Paper A \(\times\) Paper B merge’s surviving
sentence: an \(n\)-dependent lower bound on \(\lvert 3^o-2^L\rvert\)
along the three affine families of Paper A Proposition 4.9. Not a
leftover-killer, not a Baker-constant reimport, not a floor raise,
not a Paper A edit, and not a fan-minimum successor.

## Problem

The merge close left one formulation standing. Does any reading of
that sentence escape Baker dominance and the existing CycleMin
identities, or is every reading already discharged?

## Exact statement

Write \(G=3^{o_{\min}}-2^L\) and
\(\theta=G/3^{o_{\min}}\). For a known pair \((L,o_{\min})\), \(G\)
is determined by those two integers alone.

**Baker dominance (EXACT — HUMAN PROOF; instance
COMPUTATIONALLY VERIFIED).** Any correct lower bound
\(\delta\le G\) produces a finance \(n_{\max}\) at least as large
as the exact-gap \(n_{\max}\). Locked at \(L=19\): \(G=7153\),
exact \(n_{\max}=297\); the adjacent gap \(7152\) cannot improve
that ceiling, and the half-gap \(3576\) raises it. The same
comparison with a relative weakening
\(\theta\mapsto 0.999\,\theta\) holds on the affine seeds and on
the live blocker \(L=478245\). An “\(n\)-dependent” lower bound
on \(G\) cannot exceed the exact value.

**Identity table (REPARAMETERIZATION / REFUTED).** The CycleMin
identities that involve \(n\) or \(G\) are:

- `cycleMin_finance`: \(n\log n\cdot G\le L\cdot 3^o\) — an
  *upper* bound on \(G\), the \(n\)-dependent bound in
  contrapositive
- `global_defect_identity` /
  `image_eq_start_defectRatio`: \(\log R=G\log n\) on a return
- exponent-budget sum \(=\Lambda=o\log 3-L\log 2\) — no \(n\)
- inhomogeneous \(p+\Lambda\) — already REFUTED
- height / position finance — stronger *upper* bounds on
  \(\theta\), already explored

No unused cycle-forced form uses \(\log n\) except \(G\log n\).

**Readings.**

- R1 universal linear forms — REFUTED
  (`juggler_cycle_gap_baker`)
- R2 finance contrapositive — KNOWN (`cycleMin_finance`; further
  floors PARK)
- R3 new \(\log n\) form — REPARAMETERIZATION (identity table)
- R4 defect-sum \(n\)-power — REPARAMETERIZATION (walk program
  terminal)
- R5 lattice binary recurrence — REFUTED as a leftover-killer
  (cannot beat exact \(\theta\) at a known point)

**Slogan.** An \(n\)-dependent lower bound on
\(\lvert 3^o-2^L\rvert\) along \(F_1,F_2,F_3\) escapes Baker
dominance — **REFUTED**.

No cycle of any length — not claimed.

## Current literature

- Cycle finance inequality —
  **EXACT — LEAN VERIFIED** (`cycleMin_finance`)
- Run-survivor lattice —
  **EXACT — LEAN VERIFIED**
  (`RunSurvivorLattice.lean`; Paper A Proposition 4.9)
- Baker / Rhin leftover-killer — **REFUTED**
  ([juggler_cycle_gap_baker.md](juggler_cycle_gap_baker.md))
- Inhomogeneous Wu–Wang — **REFUTED**
  ([juggler_cycle_inhomogeneous_log.md](juggler_cycle_inhomogeneous_log.md))
- Fan multipoint — **REFUTED**
  ([juggler_cycle_fan_multipoint.md](juggler_cycle_fan_multipoint.md))
- \(p\)-adic coupling — **REFUTED**
  ([juggler_cycle_padic_coupling.md](juggler_cycle_padic_coupling.md))
- Fan-minimum CF reduction — **CONJECTURE** / classical **OPEN**
  ([juggler_cycle_walk_fan_minimum.md](juggler_cycle_walk_fan_minimum.md));
  no successor is opened here
- Merge leftover-killer — **REFUTED**
  (`juggler_cycle_paper_merge`)
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a live laboratory target;
the published 2–3 measures remain **known**.

## Branch budget

```text
Mathematical target     Is every reading of the merge’s n-dependent
                        lower bound on |3^o-2^L| along F1/F2/F3 already
                        discharged, or does a cycle-forced form involve
                        log n without being G log n?
Novelty hypothesis      A live reading exists: some exact CycleMin
                        identity uses the floor n as a Diophantine
                        parameter and is not finance, not
                        image_eq_start_defectRatio, and not p+Λ
Falsifier               Every n-involving identity is one of those
                        three, and Baker dominance applies to any
                        lower bound on |3^o-2^L| (n-dependent or not)
Existing machinery      cycleMin_finance, global_defect_identity,
                        image_eq_start_defectRatio, exponent-budget
                        CLOSE, gap-Baker CLOSE, inhomogeneous WW
                        CLOSE, fan-multipoint CLOSE, p-adic CLOSE,
                        fan-minimum PROMOTE (no successor),
                        RunSurvivorLattice.lean, o_min_and_theta
Maximum Phase-0 scope   One probe: classify identities on a handful
                        of lattice seeds; lock dominance on L=19
                        and the live blocker 478245. No Rhin numbers,
                        no new CF, no floor, no Lean, no Paper A
Promotion criterion     A form F(n,L,o) that is cycle-forced, uses n
                        nontrivially, and is not G log n / finance /
                        p+Λ — then name it and stop (do not attack it)
Stop criterion          All readings are REPARAMETERIZATION, KNOWN,
                        or already REFUTED. Then CLOSE; do not open
                        a fan-minimum successor
```

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Exact gap \(G=3^{o_{\min}}-2^L\) determined by \((L,o)\) —
  **EXACT — HUMAN PROOF**
- Baker dominance: \(\delta\le G\) implies
  \(n_{\max}(\delta)\ge n_{\max}(G)\) —
  **EXACT — HUMAN PROOF**; instance
  **COMPUTATIONALLY VERIFIED** at \(L=19\) and the affine seeds
- `cycleMin_finance` as the \(n\)-dependent bound in
  contrapositive — **REPARAMETERIZATION**
- \(\log R=G\log n\) — **REPARAMETERIZATION** of
  `image_eq_start_defectRatio`
- Slogan “\(n\)-dependent lower bound escapes dominance” —
  **REFUTED**
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_affine_n_gap`
- Artifacts: `data/research/juggler/cycle_affine_n_gap/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_affine_n_gap.py`

Seeds: dominance lock \(L=19\); affine samples
\(F_1=(25781,16266)\), \(F_2=(50508,31867)\),
\(F_3=(76289,48133)\); live blocker \(L=478245\) from the
competition artifact. No CLI, no Lean, no floor work, no Rhin
recompute.

## Conjectures

`juggler_affine_n_gap_escapes_dominance` — **REFUTED**.

## Counterexamples

- \(L=19\): exact \(G=7153\) gives \(n_{\max}=297\); any
  \(\delta\le 7153\) cannot improve that ceiling (adjacent gap
  \(7152\) stays at \(297\); half-gap \(3576\) raises it)
- Affine seeds and \(L=478245\): \(\theta\) is a function of
  \((L,o)\) only; weakening \(\theta\) raises \(n_{\max}\)
- Identity table: every \(n\)-involving form is finance
  (upper bound) or \(G\log n\); \(p+\Lambda\) is already closed

## Formalization

None. Finance and the return identity are already Lean. No new
Lean, no `sorry`. Paper A is unchanged.

## Results

Classification **AFFINE_N_GAP_CLOSED**.

- Unimodular identity \(25781\cdot 665-1054\cdot 16266=1\);
  family samples match `RunSurvivorLattice.lean`
- Dominance lock \(L=19\): \(n_{\max}(7153)=297\),
  \(n_{\max}(7152)=297\), half-gap \(n_{\max}(3576)=538\)
- Relative weakening \(\theta\mapsto 0.999\,\theta\) raises
  \(n_{\max}\) on every listed seed
- Live blocker \(L=478245\) uses the stored competition
  \(\theta\) and \(n^*\approx 3.48\cdot 10^8\); no new floor
- Six identities, five readings, all discharged

## Open questions

None from this formulation. Do not reopen Baker / Rhin as a
leftover-killer, and do not open a fan-minimum successor. The
classical unboundedness of the dangerous-position partial
quotients of \(\log 2/\log 3\) remains OPEN and is not a
laboratory Phase-0.

## Decision

**CLOSE.** Every reading of the merge’s \(n\)-dependent gap is
KNOWN, REPARAMETERIZATION, or already REFUTED. Baker dominance
applies whether or not the bound is written in terms of \(n\);
the only exact \(n\)-log identity is \(G\log n\); finance is the
contrapositive already used to price \(n_{\max}\). The walk
program’s CF reduction is a different sentence and is not
reopened.

Best next question: none from this formulation.

## Publication assessment

Status: `ARCHIVED`.

A one-page discharge of the merge leftover sentence. The
dominance inequality is exact; the census is five seeds. Not a
paper candidate and not a halt theorem.
