# Frozen Engine campaign: aliquot dynamics

Status: **EXPLORATORY**

This is an engine-capability campaign on \(A(n)=\sigma(n)-n\). It does
**not** claim a Catalan–Dickson theorem, a proof that 276 terminates or
diverges, or a new aliquot-cycle classification. Adapters live in
`research.aliquot_dynamics`. There is no `AliquotAttack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

What can frozen Research Engine v2 discover about divisor-sum iteration
when its affine-control machinery is given a genuinely arithmetic,
non-affine transition, including the open seed 276?

## Exact statement

On hint-free `ProblemSpec` adapters for \(A(n)=\sigma(n)-n\), does
unmodified `ResearchLoop`

1. diagnose a regime distinct from digit-fold / residue-affine /
   valuation control;
2. recover known recurrent seeds (fixed point, period 2, termination)
   as exact finite closures;
3. refuse to certify a piecewise-affine cover;
4. refrain from claiming a fate for 276?

Computational budget (adapter, not an attack):

- maximum term \(n\le 10^{12}\);
- trial factorization to \(10^{6}\);
- at most 16 planner steps / 32 residual states / 40 post-run steps;
- if \(n>10^{12}\), report `TRANSITION_UNRESOLVED`, not dynamical
  UNKNOWN.

## Current literature

- Guy–Selfridge, *What drives an aliquot sequence?*, Math. Comp. 1975
  (`guy-selfridge-1975-aliquot-drivers`). Drivers; counter-conjecture.
  **CONJECTURE** / **HEURISTIC**.
- Erdős, *On asymptotic properties of aliquot sequences*, Math. Comp.
  1976 (`erdos-1976-aliquot`). **THEOREM** (analytic).
- te Riele, *Advances in aliquot sequences*, Math. Comp. 1999
  (`te-riele-1999-advances-aliquot`). **COMPUTATIONAL**.
- OEIS A008892 (`oeis-A008892`): sequence from 276; 2145 terms; term
  2145 has 214 digits; whether it reaches 0 is open. **COMPUTATIONAL**.
- Catalan (1888) / Dickson (1913): every sequence terminates or becomes
  periodic. **CONJECTURE**.
- Pythagoras / Euclid: perfect numbers, amicable pair 220–284.
  **THEOREM**.

Project relationship: **engine diagnosis**. No new number-theory theorem
is claimed.

## Branch budget

```text
Mathematical target     What can frozen v2 discover about A(n)=sigma(n)-n,
                        including seed 276, without affine-control
                        representations?
Novelty hypothesis      A genuinely new regime fingerprint, or an exact
                        invariant/obstruction outside known aliquot lore.
Falsifier               Adapter leaks Catalan–Dickson / 276-open / cycle
                        names; new attacks; claiming a fate for 276;
                        treating incomplete factorization as dynamics.
Existing machinery      Unmodified ResearchLoop; 1-D dummy-control spec;
                        post-run quantifier probes.
Maximum Phase-0 scope   Control seeds 12, 6, 220 + flagship 276 + Lean
                        for KNOWN identities + ResearchLoop next + dossier.
Promotion criterion     A new exact invariant or a precise ENGINE_LIMITATION.
Stop criterion          New divisor-sum attack; claiming Catalan–Dickson;
                        unrestricted factorization.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required. Digit-fold cores remain a comparison cluster.

## Candidate operations / invariants

- \(A(1)=0\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- \(A(p)=1\) for prime \(p\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- \(A(6)=6\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- \(A(12)=16>12\). **EXACT — LEAN VERIFIED**. **KNOWN** counterexample
  to global descent.
- \(A(220)=284\), \(A(284)=220\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- No piecewise-affine cover of \(A\) on the sample window.
  **OBSERVATION** / **ENGINE_LIMITATION**.

## Experiments

- `tests/research/aliquot_dynamics/test_aliquot_dynamics.py`
- Runner: `research.aliquot_dynamics.runner.run_campaign`
- Scout (never imported by the adapter): `research.aliquot_dynamics.scout`

## Conjectures

None opened. Catalan–Dickson and Guy–Selfridge remain literature
conjectures and are not restated as project conjectures.

## Counterexamples

- “Every defined step satisfies \(A(n)<n\).” **REFUTED** at 12.
- “No fixed point.” **REFUTED** at 6 (and 28 in the window).
- “No short cycle.” **REFUTED** as a window claim by those fixed
  points; period 2 at 220–284 by exact seed closure.
- “Finite seed closure means the map is contracting.” **REFUTED** as a
  diagnosis: 6 is stationary, 220 is a 2-cycle, both billed
  `FINITE_CONTRACTING`.

## Formalization

`formal/Problems/Engine/AliquotDynamics.lean`: `properDivisorSum_*`.
KNOWN identities. No `sorry`. No ledger row.

## Results

### A. Scout dossier

See `scout.py` and Current literature. Classified claims:

| Claim | Tag |
|-------|-----|
| \(A(n)=\sigma(n)-n\) | THEOREM |
| Perfect / amicable / sociable cycles | THEOREM |
| Every start \(<138\) is settled | THEOREM / COMPUTATIONAL (classical) |
| Catalan–Dickson | CONJECTURE |
| Guy–Selfridge divergence | CONJECTURE / HEURISTIC |
| 276 / Lehmer five unresolved | COMPUTATIONAL |
| A008892: 2145 terms, 214-digit term | COMPUTATIONAL |
| Erdős analytic mean-abundance | THEOREM |

Factorization of large terms is the practical barrier, not a theorem.

### B. Blind adapter

`SigmaMinusNSpec`: positive integer state; dummy control; identity
observation; `affine_system()=None`; successor \(\sigma(n)-n\) via
trial factorization inside budget. Empty menu at \(n\le 0\) (terminal)
and at \(n>10^{12}\) (`TRANSITION_UNRESOLVED`, distinguished by
`transition_status`).

No Catalan–Dickson, no “276 is open”, no perfect/amicable/abundant
labels, no OEIS trajectory. Scout is not imported by
`spec.py` / `adapter.py` / `planner.py`.

### C. Control targets

| Role | Seed | Engine |
|------|------|--------|
| known termination | 12 | exact closure size 8: \(12\mapsto 16\mapsto 15\mapsto 9\mapsto 4\mapsto 3\mapsto 1\mapsto 0\). Halt. **FINITE EXACT REACHABILITY** |
| known fixed point | 6 | exact closure size 1. Cycle. Quotient 1 class |
| known period 2 | 220 | exact closure size 2: \(\{220,284\}\). Identity observation **separates** them (different outputs). Not billed as an amicable pair |
| open flagship | 276 | see D |

All four have piecewise census `UNRESOLVED`. Control-word stack skipped.

### D. 276 analysis

Blind prefix (post-run, 40 steps, all `DEFINED`, none
`TRANSITION_UNRESOLVED`):

\[
276,396,696,1104,1872,3770,\ldots
\]

matches the published opening of A008892 **after** the run. Last
computed term in the 40-step probe is still below the \(10^{12}\)
budget. Planner closure hits cap 32 (`INCONCLUSIVE`): **not**
infinitude.

| Claim | Engine |
|-------|--------|
| Termination of 276 | **not claimed** |
| Divergence | **not claimed** |
| Eventual periodicity | **not claimed** |
| Unboundedness | **not claimed** |
| Strongest statement | `ENGINE_LIMITATION`: singleton control, mixed magnitude, truncated reachable set, no affine language |
| Reachability class | `COMPUTATIONALLY EXPLORED` / truncated exact BFS |

Literature status remains: ultimate fate unknown (A008892, 2145 terms).
The engine did not improve that status.

### E. Diagnosis

Flagship 276:

| Field | Engine |
|-------|--------|
| Decision | `ENGINE_LIMITATION` |
| Semantic class | `INTEGER_1D\|SINGLETON\|MIXED_MAGNITUDE\|UNBOUNDED_SAMPLE` |
| Piecewise | `UNCERTAIN` / census `UNRESOLVED` |
| Contraction | `MIXED_MAGNITUDE` |
| Eventual region | `UNBOUNDED_SAMPLE` (cap, not a theorem) |
| Control words | skipped |
| Nearest (isolated) | none |

Seeds 6/12/220: `INTEGER_1D|SINGLETON|FINITE_CONTRACTING|FINITE_SEED_CLOSURE`
and isolated `CONTINUE` (“new structural regime with an exact
certificate” = finite closure / quotient). Seed-orbit coarseness again.

Versus corpus (digit-fold / Syracuse / BB-5 affine): 276 does **not**
core-match `FINITE_CONTRACTING`. That is a genuinely different
fingerprint from the affine/valuation family, obtained because the
census failed and the orbit did not close.

Capability coverage exercised: finite closure, numerical contraction,
growth, (for 276) infinite_reachable_trajectories, behavioral quotient,
separation, latent piecewise-affine control (as an **inconclusive**
attempt). Control-word obstruction **not** exercised.

### F. Existing attack results (276)

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | INCONCLUSIVE (`UNRESOLVED`) |
| parameter_domain | INAPPLICABLE |
| control_word | INAPPLICABLE |
| control_obstruction | INAPPLICABLE |
| closure | INCONCLUSIVE (cap 32) |
| functional | REFUTED |
| separation | SUPPORTED (identity observation) |
| quotient | INCONCLUSIVE (no finite reachable set) |
| vector_affine, matrix_word_invariant, modular, affine, reverse, block, spectral, factorization, symmetry, symbolic | INAPPLICABLE |

The engine `factorization` attack is **control-contribution**
factorization, not integer factorization of \(n\). Integer factoring is
only the adapter's budgeted evaluator.

### G. Mathematical yield

```text
Known rediscoveries:     A(6)=6; A(220)=284=A^{-1}; A(12) terminates;
                         A(276) prefix; A(p)=1
New exact identities:    none beyond the definition
New invariants:          none
New obstructions:        none (control stack never ran)
New counterexamples:     global descent at 12; contraction diagnosis
New trajectory classifications: exact closures for 6, 12, 220;
                         276 truncated / ENGINE_LIMITATION
New conjectures:         none
Lean-certified results:  properDivisorSum_* (KNOWN; no ledger)
Potentially new mathematics: none
Unresolved questions:    fate of 276; Catalan–Dickson
Engineering changes:     0
```

| Result | Class |
|--------|-------|
| \(A(6)=6\), \(220\leftrightarrow 284\), descent of 12 | `KNOWN_REDISCOVERY` |
| Census `UNRESOLVED` | `NEW_COMPUTATIONAL_OBSERVATION` about the **engine**, not about \(A\) |
| 276 prefix | `KNOWN_REDISCOVERY` (A008892) |
| ENGINE_LIMITATION on 276 | engine diagnosis, not a number-theory theorem |

No `POTENTIALLY_NEW_THEOREM`.

### H. Falsification

Window \(\{1,\ldots,60\}\): descent **REFUTED** at 12; fixed points 6
and 28; mixed magnitude (46 drops, 12 growths, 2 equals). Scope
`CERTIFIED ON WINDOW`. Not a \(\mathbb{N}\)-theorem.

### I. Prior-art reconciliation

| Literature | Engine |
|------------|--------|
| Perfect 6 | exact 1-state closure. Not named “perfect” |
| Amicable 220–284 | exact 2-state closure. Separated by identity observation |
| Terminating 12 | exact path to 0 |
| A008892 opening | independently recomputed prefix |
| Drivers / abundance heuristics | **not recovered**. No abundance attack |
| Catalan–Dickson | **not addressed** |
| 276 open after 2145 terms | engine: 40 exact terms, then budgeted truncation; fate still unknown |

### J. Lean

`properDivisorSum_one`, `_prime`, `_six`, `_twelve`, `_220_284`. KNOWN.
No ledger.

### K. Engineering limitations

Not implemented.

```text
Problem              Affine/valuation census cannot represent
                     factorization-dependent A(n)=sigma(n)-n
Affected component   PiecewiseAffineCensus; dependent control-word
                     stack; decide_research ENGINE_LIMITATION branch
Semantic mismatch    Growth/contraction and exact small cycles are
                     visible, but there is no latent affine language
Minimal example      sigma_minus_n_276; also the unresolved census on
                     6, 12, 220
Mathematical importance  High: this is a natural arithmetic dynamical
                         system outside the frozen attack language
Potential generic fix    Not an affine census. Would require a new
                         arithmetic-structure attack. Forbidden here.
```

```text
Problem              Seed-orbit finiteness billed as contraction
Affected component   RegimeFingerprint core
Minimal example      sigma_minus_n_6 (stationary), _220 (2-cycle)
```

```text
Problem              Engine factorization attack ≠ integer factorization
Affected component   attacks.factorization (raw_contribution)
Semantic mismatch    Aliquot evaluation needs primes of n; the attack
                     needs control-to-contribution factorization
```

### L. ResearchLoop

After the portfolio is recorded, `score_candidate` runs on the same
mixed pool as the SLC campaign (increment, \(mx+r\), hidden congruence,
vector shear, integer polynomial) with **no taste override**.

The flagship 276 is `ENGINE_LIMITATION`, not a saturated digit-fold
core. The loop's next-target choice is recorded by the campaign test
(`researchloop_next`). Do not override.

### M. Final decision

Engine (276): `ENGINE_LIMITATION`.

Campaign (methodology): `PARK`.

## Open questions

The fate of 276 remains open in the literature. Do not assign Catalan–
Dickson to the engine. The named affine-language limitation waits for
an engineering thaw.

## Decision

`PARK`. The frozen stack correctly refused a piecewise-affine language
for \(A(n)=\sigma(n)-n\), recovered known small recurrent/terminating
seeds as exact closures, recomputed the opening of the 276 trajectory,
and did not invent a fate for 276. That is a precise boundary of the
frozen attack language, not new aliquot mathematics. Do not add a
divisor-sum attack. Do not auto-continue into Catalan–Dickson.

Best next question: which frozen-engine target still lies *inside* the
existing attack language, now that this arithmetic boundary is
recorded?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE`. Value is a frozen-engine
stress test whose primary metric is whether v2 can distinguish known
aliquot structure from what its affine machinery can actually certify.
