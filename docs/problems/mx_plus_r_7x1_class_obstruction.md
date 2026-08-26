# Frozen Engine campaign: 7x+1 class obstruction

Status: **EXPLORATORY**

This is the first mathematical campaign on frozen Research Engine v2.3.
It does **not** claim convergence or divergence of \(7x+1\). Adapters
reuse `research.mx_plus_r`. There is no new attack.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

Does the exact residue/valuation control of the normalized odd map
\(T(x)=(7x+1)/2^{v_2(7x+1)}\) induce a nontrivial class obstruction
relevant to reaching 1?

## Exact statement

On the hint-free existing adapter `MxPlusRSpec(m=7,r=1)` with seed
\(x=3\) and dummy control, does frozen v2.3 recover a class restriction
that prevents, constrains, or forces access to the class containing 1,
without rediscovering \(2^k y=7x+1\) as the yield?

Computational budget (stored packet): 16 planner steps / 32 residual
states.

## Current literature

- Crandall 1978 (`crandall-1978-3x+1`): \(qx+1\) relatives; \(5x+1\) /
  \(7x+1\) believed typically divergent. **KNOWN**.
- Chamberland 2003 (`chamberland-2003-3x+1-survey`): survey of \(3x+1\)
  and nearby generalized maps. **KNOWN**.
- Family \(2^k y=mx+r\): laboratory infrastructure, Lean
  `mxPlusR_parameter_iff`. **KNOWN**.
- Image of accelerated \(3x+1\) avoids \(0\pmod 3\). **KNOWN**. The
  \(7x+1\) analogue is elementary and stricter because \(2\) has order
  \(3\) in \((\mathbb Z/7\mathbb Z)^*\).

Project relationship: **engine diagnosis / elementary arithmetic**.
The image class is not a new number-theory theorem.

## Branch budget

```text
Mathematical target     Does T_{7,1} induce a nontrivial class
                        obstruction relevant to reaching 1?
Novelty hypothesis      A 7-specific class restriction, not the family
                        2^k y = 7x+1.
Falsifier               Every candidate class is escaped, a horizon
                        artefact, a family rediscovery, or does not
                        constrain access to 1.
Existing machinery      MxPlusRSpec; StrategyPlanner census_obstruction;
                        reverse/closure; Lean mxPlusR_*; ResearchMemory.
Maximum Phase-0 scope   Scout+blind at seed 3, horizon≤16, residual≤32;
                        falsify; smallest exact statement; Lean.
Promotion criterion     Exact class restriction that excludes an
                        infinite family from reaching 1.
Stop criterion          Candidates fail structurally, or yield is only
                        family rediscovery.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Family \(2^k y=7x+1\). **OBSERVATION** on a window; relation exactness
  **EXACT — LEAN VERIFIED** (`mxPlusR_parameter_iff`). **KNOWN**.
- Image \(T(n)\not\equiv 0\pmod 7\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- Image \(T(n)\equiv 1,2,\) or \(4\pmod 7\). **EXACT — LEAN VERIFIED**.
  **KNOWN** (order of \(2\) modulo \(7\)).
- Only positive length-one cycle is \(1\). **EXACT — LEAN VERIFIED**.
  **KNOWN**.
- \(73\equiv 3\pmod 7\) maps to \(1\). **EXACT — LEAN VERIFIED**.
- \(299593\equiv 0\pmod 7\) maps to \(1\). **EXACT — LEAN VERIFIED**.
- Seed \(3\) misses \(1\) on horizons \(16\) and \(32\). **OBSERVATION**;
  not divergence.

## Experiments

- `tests/research/mx_plus_r_7x1_class_obstruction/test_mx_plus_r_7x1_class_obstruction.py`
- Runner: `research.mx_plus_r_7x1_class_obstruction.runner.run_campaign`
- Scout (never imported by the adapter): `research.mx_plus_r_7x1_class_obstruction.scout`

## Conjectures

None opened.

## Counterexamples

- “Rediscovering \(2^k y=7x+1\) is the yield.” **REFUTED** as a campaign
  success criterion: that family is KNOWN infrastructure.
- “Seed \(3\) reaches \(1\) within \(16\) steps.” **REFUTED**.
- “Odd \(n\equiv 3,5,6\pmod 7\) cannot reach \(1\).” **REFUTED** at
  \(T(73)=1\).
- “Odd multiples of \(7\) cannot reach \(1\).” **REFUTED** at
  \(T(299593)=1\).
- “The \(7x+1\) image class fills all units, as for \(3x+1\) and
  \(5x+1\).” **REFUTED**: \(T_{3,1}\) hits \(\{1,2\}\pmod 3\) and
  \(T_{5,1}\) hits \(\{1,2,3,4\}\pmod 5\).
- “Widening the odd window inside the budget changes the image class.”
  **REFUTED**.

## Formalization

`formal/Problems/Engine/MxPlusR.lean`. Image-class and counterexample
identities, including `mxPlusR_seven_image_residue`. No `sorry`. No
ledger row (KNOWN).

## Results

See sections A–L below.

## Open questions

Which odd positive integers reach \(1\)? The image class does not
decide that. Finite non-visit of \(1\) from seed \(3\) is not
divergence.

## Decision

**CLOSE**. Frozen v2.3 recovered the known family and generic
control-word cycle words. The exact 7-specific statement is elementary:
after one step, every odd image lies in the subgroup \(\langle 2\rangle
=\{1,2,4\}\) of \((\mathbb Z/7\mathbb Z)^*\). Complementary classes are
not excluded from the basin of \(1\) (\(T(73)=1\), \(T(299593)=1\)).
All statements are `KNOWN`. Laboratory decision `CLOSE`.

Best next question: the unmodified leftover pick on the board after
this ingest. What exact obstruction, if any, can frozen v2.3 produce
there without new attacks?

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`MxPlusRSpec` / `mx_plus_r_7_1`):

- state space odd positive integers;
- dummy singleton control;
- identity observation;
- seed \(3\);
- successor \((7x+1)\) divided by the maximal power of \(2\);
- budget 16 planner steps / 32 residual states.

No named conjecture, open-problem status, or residue partition in
`spec.py` / `adapter.py` / `planner.py`. Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `CYCLE_EXCLUSION` selected
`census_obstruction` (score \(1.500\)). With historical memory, the
same goal selects `law_domain`; that track rediscovered the family and
sample residue domains for fixed \(k\), which is not injected into the
blind packet.

Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_1D`, `SINGLETON`, `PARAMETERIZED`
  piecewise-affine / latent control, `SCALAR` affine control,
  `MIXED_MAGNITUDE`, `UNBOUNDED_SAMPLE`, obstruction
  `RECURSIVE_INVARIANT`.
- `ResearchDecision`: **CONTINUE** — family recovered, domain certified,
  recursive invariant proved; map globality on \(\mathbb Z\) remains
  empirical.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | OBSERVATION; `PARAMETERIZED_CENSUS`; \(2^k y=7x+1\) |
| parameter_domain | SUPPORTED |
| control_word | SUPPORTED; 36 words |
| control_obstruction | SUPPORTED; class/symbolic/recursive cycle words |
| closure | INCONCLUSIVE |
| modular | INAPPLICABLE (`AffineSystem` absent) |
| reverse | INAPPLICABLE (no `reverse_preimage` in the packet) |
| functional | REFUTED |
| separation | SUPPORTED |
| quotient | INCONCLUSIVE |

The class-level engine obstructions are generic cycle constraints
(length-one possible \(k=(3,)\); recursive remainder). They classify
cycles, they do not exclude an infinite family from reaching \(1\).

### D. Class analysis

Let \(C_1=\{n\text{ odd}: n\equiv 1,2,4\pmod 7\}\) and
\(C_{\mathrm{out}}=\{n\text{ odd}: n\equiv 0,3,5,6\pmod 7\}\).

- \(T(\mathbb Z_{\mathrm{odd}}^+)\subseteq C_1\). **EXACT**.
- \(C_1\) is forward-invariant. **EXACT**.
- \(C_{\mathrm{out}}\) is transient: one step lands in \(C_1\).
- \(1\in C_1\), so the image class does **not** forbid reaching \(1\).
- Direct preimages of \(1\) are \((2^{3m}-1)/7\), and these occupy every
  residue modulo \(7\) as \(m\) varies (\(m\equiv n\pmod 7\)).

Seed \(3\equiv 3\pmod 7\) enters \(C_1\) immediately (\(T(3)=11\equiv 4\))
and does not hit \(1\) on horizons \(16\) or \(32\). That miss is not a
theorem.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| family \(2^k y=7x+1\) | yes | yes | common structural result; **KNOWN** |
| generic cycle-word obstructions | yes | yes | common; **KNOWN** |
| sample domains for fixed \(k\) | law_domain (memory) | not named in the packet | scout-only presentation |
| image residues \(\{1,2,4\}\pmod 7\) | yes (after family) | independently from I/O | independently rediscovered |
| \(C_{\mathrm{out}}\) cannot reach \(1\) | hypothesized | refuted by \(73\) | false lead |
| seed \(3\) reaches \(1\) on the bound | — | refuted | false lead |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| image in \(\langle 2\rangle\subseteq(\mathbb Z/7\mathbb Z)^*\) | **PROVED** / **LEAN_CERTIFIED** |
| \(7\nmid T(n)\) | **PROVED** / **LEAN_CERTIFIED** |
| \(v_2(7n+1)\bmod 3\) determines \(T(n)\bmod 7\) | **PROVED** (same congruence) |
| \(C_{\mathrm{out}}\) closed / basin-excluded | **REFUTED** |
| finite origin-reachability quotient | not obtained |

### G. Mathematical yield

```text
known_rediscoveries:     2^k y = 7x+1; generic cycle-word obstructions
new_exact_results:       mxPlusR_seven_image_residue and supporting identities
new_invariants:          image class {1,2,4} (mod 7)
new_obstructions:        image class, not a basin exclusion
new_counterexamples:     T(73)=1; T(299593)=1
new_conjectures:         none
new_formalizations:      Problems.Engine.MxPlusR image-class lemmas
potentially_new_mathematics: none
unresolved_questions:    which odd n reach 1
engineering_changes:     0
representation_novelty:  MEDIUM
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` of the local family, plus
`NEW_FORMALIZATION` of an elementary image class. Not
`POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

No `GLOBAL_REASONING` record. The basin question remains open as a map
theorem; the image class is a finite-modulus fact, not an infinite-time
certificate.

Grey loot stored: image class; \(C_{\mathrm{out}}\) counterexamples;
family rediscovery is not a basin obstruction.

### I. Prior-art reconciliation

Crandall/Chamberland discuss \(qx+1\) heuristics and extra cycles.
They do not list a \(7x+1\) basin obstruction. The identity
\(2^k y\equiv 1\pmod 7\) is immediate from \(7x+1\equiv 1\pmod 7\).
The proper subgroup \(\langle 2\rangle\subset(\mathbb Z/7\mathbb Z)^*\)
is the 7-specific comparison with \(3x+1\) and \(5x+1\), where \(2\)
generates the full unit group. That comparison is elementary, not new.

### J. Lean

`Problems.Engine.MxPlusR`. Strongest exact theorem:
`mxPlusR_seven_image_residue`. Counterexamples
`mxPlusR_seven_one_from_seventy_three` and
`mxPlusR_seven_one_from_multiple_of_seven`. No `sorry`.

### K. ResearchLoop / StrategyPlanner

Memory ingest did not change flood-planner output. Blind
`StrategyPlanner(CYCLE_EXCLUSION)` selected `census_obstruction`.
Next leftover target is selected automatically (no override).

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE` (family recovered on an
unbounded sample). Laboratory and campaign close because no class
excludes an infinite family from reaching \(1\), and the surviving
image statement is `KNOWN` elementary arithmetic. Do not add a \(7x+1\)
attack. Do not expand the census. Do not claim divergence.
