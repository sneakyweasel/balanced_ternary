# Frozen Engine campaign: BB-5 generalized Collatz map

Status: **EXPLORATORY**

This is an engine-capability campaign against Michel's BB-5 map and the
Yolcu–Aaronson–Heule rewriting treatment. It does **not** claim a Busy
Beaver theorem, a Collatz theorem, or totality of the Marxen–Buntrock
machine on all inputs. Adapters live in `research.bb5_map`. There is no
`BB5Attack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Can frozen Research Engine v2, given only the exact partial transition
of the BB-5 generalized Collatz map, independently reconstruct its
residue-controlled affine language and derive any exact constraint
beyond rediscovery of the definition?

## Exact statement

On a hint-free `ProblemSpec` for the partial map

\[
n \mapsto y \quad\text{iff}\quad n\ge 0\text{ and }3y\in\{5n+18,\,5n+22\},
\]

does unmodified `ResearchLoop`

1. recover the two affine branches and a modulus-3 latent control;
2. certify domains and compose control words;
3. produce cycle obstructions, including interaction with the undefined
   residue;
4. distinguish seed-0 / window halt from universal convergence on
   \(\mathbb{N}\)?

Window agreement is not a map theorem on \(\mathbb{N}\). Finite seed
closure is not numerical contraction. BB(5) is a different statement
from convergence of \(B\) on all seeds.

## Current literature

- Michel, *Busy beaver competition and Collatz-like problems*, TCS
  1993 (`michel-1993-busy-beaver-collatz`). **KNOWN**.
- Michel, *Problems in number theory from busy beaver competition*,
  LMCS 2015 (`michel-2015-busy-beaver-number-theory`). **KNOWN**.
  Source of the correspondence: the BB-5 candidate simulates \(B\).
- Yolcu–Aaronson–Heule, *An Automated Approach to the Collatz
  Conjecture*, JAR 2023 / CADE 2021
  (`yolcu-aaronson-heule-2023-automated-collatz`). **KNOWN**. Gives
  \(B\) exactly and reports failure to prove termination of the mixed
  \(\{3,5\}\)-ary SRS.
- Aaronson, *The Busy Beaver Frontier*, SIGACT News 2020
  (`aaronson-2020-busy-beaver-frontier`). **KNOWN**.
- bbchallenge Collaboration, *Determination of the fifth Busy Beaver
  value*, arXiv:2509.12337 (`bbchallenge-2025-fifth-busy-beaver`).
  **KNOWN**. \(S(5)=47{,}176{,}870\) by Coq/Rocq enumeration of 5-state
  machines. Not a termination proof of \(B\) on all seeds.

Project relationship: **engine diagnosis / rediscovery**. No new
number-theory or Busy Beaver theorem is claimed.

## Branch budget

```text
Mathematical target     Can frozen v2 reconstruct and exploit the
                        arithmetic of the BB-5 map B from the exact
                        partial transition, beyond rediscovery of
                        3y=5x+18 and 3y=5x+22?
Novelty hypothesis      Certified control words and class-level cycle
                        obstructions that the 2021 rewriting paper did
                        not record in this form; possibly a new
                        terminal-class restriction.
Falsifier               Adapter seeds residue labels, affine formulas
                        as engine hints, BB-5 language, or a
                        termination claim; new attack modules;
                        identifying map convergence with BB(5).
Existing machinery      Unmodified ResearchLoop; census → domain →
                        word → obstruction; 1-D dummy-control spec.
Maximum Phase-0 scope   One blind adapter + scout off the adapter +
                        unmodified loop + Lean for the strongest exact
                        identities + one campaign dossier.
Promotion criterion     An exact constraint not already in the
                        definition or the cited literature.
Stop criterion          Pure rediscovery of the two lines; finite
                        seed-0 closure as the only dynamical result;
                        claiming BB-5 or Collatz.
```

## Balanced-ternary formulation

None. The adapter uses ordinary integer arithmetic.

## Why BT may be relevant

It is not required. Digit-fold cores remain a comparison cluster in the
seeded corpus.

## Candidate operations / invariants

- Unique successor when defined. **EXACT — LEAN VERIFIED**
  (`bRel_unique`). **KNOWN**.
- \(3y=5x+18\) or \(3y=5x+22\). **EXACT — LEAN VERIFIED**
  (`bRel_clear`). **KNOWN**.
- Undefined on \(x\equiv 2\pmod{3}\) for \(x\ge 0\). **EXACT — LEAN
  VERIFIED** (`bRel_undefined_two`). **KNOWN**.
- Length-1 cycle candidates \(x=-9\) and \(x=-11\), outside \(x\ge 0\).
  **EXACT — LEAN VERIFIED**. **KNOWN**.
- No nonnegative fixed point. **EXACT — LEAN VERIFIED**
  (`bRel_not_fixed`). **KNOWN**.
- Engine census \(3y=5x+18\) on \(x\equiv 0\pmod{3}\) and
  \(3y=5x+22\) on \(x\equiv 1\pmod{3}\). **OBSERVATION** on the sample
  window; **DISCOVERED** (not adapter-labelled). Domain `EXACT` after
  counterexample search.
- CLASS obstructions: mixed length-2 words blocked (\(16\nmid C\));
  mixed length-3 words blocked (\(98\nmid C\)). **EXACT** on the
  composed relation. **KNOWN** arithmetic via Engine lemmas.

## Experiments

- `tests/research/bb5_map/test_bb5_map.py`
- Runner: `research.bb5_map.runner.run_campaign`
- Scout (never imported by the adapter): `research.bb5_map.scout`

## Conjectures

None opened. Universal convergence of \(B\) on \(\mathbb{N}\) remains
literature-open and is not re-stated as a project conjecture.

## Counterexamples

- “Every defined step strictly decreases.” **REFUTED** at seed 0:
  \(0\mapsto 6\).
- “Every defined step is a one-step contraction
  \(\lvert y\rvert<\lvert x\rvert\).” **REFUTED** at seed 1:
  \(1\mapsto 9\).
- “No cycle exists on \(\mathbb{Z}\).” **REFUTED** as an unrestricted
  algebraic claim: \(x=-9\) and \(x=-11\) are fixed points of the two
  lines. They lie outside the adapter domain \(n\ge 0\).
- “Finite seed closure means the map is contracting.” **REFUTED** as a
  diagnosis: \(B\) expands on the defined nonnegative locus, yet seed 0
  closes at 15 states and is billed `FINITE_CONTRACTING`.

## Formalization

`formal/Problems/Engine/BB5Map.lean`: `bRel_unique`, `bRel_clear`,
`bRel_undefined_two`, `bRel_ediv_zero`, `bRel_ediv_one`,
`bRel_len_one_neg_nine`, `bRel_len_one_neg_eleven`, `bRel_not_fixed`.
KNOWN integer consequences of the problem definition. No `sorry`. No
ledger row.

## Results

### A. Scout dossier

Carelli-style prior art, classified and **not** passed to the adapter:

- Michel: the 5-state champion simulates \(B\). Blank-tape behaviour is
  the orbit of \(B\) from 0. Totality on all inputs is a different
  claim, historically open as of the 2021 rewriting paper.
- Yolcu–Aaronson–Heule: mixed \(\{3,5\}\)-ary SRS; termination not
  proved. They give \(B\) exactly as in this campaign.
- bbchallenge 2024/2025: \(S(5)=47{,}176{,}870\) by enumerating 5-state
  machines. This settles BB(5), not \(\forall n\ge 0\), \(B\) hits
  \(\bot\).
- Map convergence \(\neq\) BB-5 totality \(\neq\) a generalized-Collatz
  theorem. Keep them separate.

Open scout question: does every nonnegative orbit of \(B\) eventually
become undefined?

### B. Blind adapter

`PartialFiveThreeSpec` exposes only: nonnegative integer state; dummy
control; identity observation; `affine_system()=None`; successors
\(y\) with \(3y\in\{5n+18,5n+22\}\). Empty menu when \(n<0\) or neither
divisibility holds.

No residue table, no branch labels, no Michel/BB-5/Collatz language.
Scout lives in `scout.py`. `spec.py` / `adapter.py` / `planner.py` do
not import it.

### C. Diagnosis

Isolated `ResearchLoop` (no corpus):

| Field | Engine |
|-------|--------|
| Decision | `CONTINUE` — finite piecewise-affine census on a structurally distant regime; window agreement is not a \(\mathbb{Z}\)-theorem |
| Semantic class | `INTEGER_1D\|SINGLETON\|FINITE_CONTRACTING\|FINITE_SEED_CLOSURE` |
| Control | `SINGLETON` / `DETERMINISTIC` |
| Piecewise | `FINITE` |
| Latent control | `FINITE` (residue mod 3, values \(\{0,1\}\)) |
| Parameter domain (fingerprint) | `SAMPLE_SUPPORTED` |
| Algebra | `EXPLOITABLE` |
| Obstruction | `CLASS` |
| Affine type | `SCALAR` |
| StructuralDelta | none (empty corpus) |

Seeded digit-fold / Syracuse corpus:

| Field | Engine |
|-------|--------|
| Decision | `FAMILY_SATURATED` against `INTEGER_1D\|SINGLETON\|FINITE_CONTRACTING\|FINITE_SEED_CLOSURE` |
| Nearest | `operator_dynamics_benchmark` |

No taste override. The core is again a **seed-orbit artefact**: \(B\)
expands whenever defined, but seed 0 closes.

Capability coverage exercised: finite closure, numerical contraction,
growth, modular restrictions, cycle obstruction, behavioral quotient,
separation, latent piecewise-affine control, parameter-domain
certification, control-word composition, control-obstruction calculus.

### D. Branch discovery

`PiecewiseAffineCensus`: `FINITE_CENSUS`, two branches, coverage 1.0,
unresolved empty.

| Branch | Region | Status |
|--------|--------|--------|
| \(3y=5x+18\) | \(x\equiv 0\pmod{3}\) | `SUPPORTED_BY_SAMPLES` |
| \(3y=5x+22\) | \(x\equiv 1\pmod{3}\) | `SUPPORTED_BY_SAMPLES` |

Latent control: residue modulo 3, observed values \(\{0,1\}\). The
undefined class \(x\equiv 2\pmod{3}\) is the empty menu, not a third
affine branch.

Structure origin: **DISCOVERED**. The adapter did not label residues.

`ParameterDomain`: both congruence domains `EXACT` after
`COUNTEREXAMPLE_SURVIVED`. Not a \(\mathbb{Z}\)-wide map theorem.
Fingerprint still bills `SAMPLE_SUPPORTED`.

Terminal class: `bRel_undefined_two` packages \(x\equiv 2\Rightarrow\)
no successor on \(x\ge 0\). **KNOWN**.

### E. Control analysis

14 composed words. Length-1/2 relations `LEAN_CERTIFIED` against Engine
lemmas; length 3 `ALGEBRAICALLY_COMPOSED`.

Examples: \((0)\): \(3y=5x+18\); \((1)\): \(3y=5x+22\);
\((0,0)\): \(9y=25x+144\); \((0,1)\): \(9y=25x+156\).

Realizability: mixed words such as \((0,1)\) are
`REALIZABLE_FOR_SOME_SEED` as **paths** (seed 6: \(6\mapsto 16\mapsto 34\))
and `IMPOSSIBLE` as **cycles**. Constant words are realizable as paths;
their cycle candidates sit at \(-9\) and \(-11\).

Obstruction (frozen stack):

- WORD gcd: mixed length-2 \((0,1),(1,0)\) blocked (\(4\nmid 156\) in
  the reported form; modulus 16). Mixed length-3 six words blocked
  (modulus 98).
- CLASS: length 2 requires \(16\mid C\); allowed closing words
  \((0,0),(1,1)\). Length 3 requires \(98\mid C\); allowed
  \((0^3),(1^3)\).
- WORD sign: unique cycle candidates of the allowed constant words are
  \(-9\) and \(-11\), **outside the spec domain**.

A cycle obstruction is not a cycle. Mixed cyclic words of length 2 and
3 form an impossible class. That is the boxed pathway

\[
\text{residue-controlled affine map}
\rightarrow
\text{certified control words}
\rightarrow
\text{impossible class},
\]

and it is **KNOWN** divisibility, the same engine pattern as Carelli
\(R^+\).

### F. Terminal analysis

\(n\equiv 2\pmod{3}\) has empty `legal_controls`. Frozen semantics:
deadlock, not a named \(\bot\) attack.

Seed-0 closure hits \(12284\equiv 2\pmod{3}\) and stops. Exact finite
`Post^*` of that seed, not a proof that every legal infinite word must
hit the class. Control words that remain defined never use a letter at
residue 2 because there is no letter there. The engine does not state a
separate “avoiding language” theorem.

### G. Reachability

| Claim | Status |
|-------|--------|
| Exact residual closure from seed 0 | size 15, complete. Orbit \(0,6,16,\ldots,12284\). **FINITE WINDOW** / exact seed closure. **KNOWN** (published BB-5 trajectory) |
| Universal reachability of \(\bot\) on \(\mathbb{N}\) | **not claimed**. Window \(0..80\) is `CERTIFIED_ON_WINDOW` |
| `NO PATH FOUND` for cycles on the nonnegative window | search miss on length \(\le 6\), plus sign obstruction for length 1–3 constant words. Not `NO PATH EXISTS` on all of \(\mathbb{N}\) for every period |

Do not infer global termination from the seed-0 closure.

### H. Falsification

See Counterexamples. Surviving window facts that are **not** promoted:
no length-\(\le 6\) cycle in \(\{0,\ldots,80\}\); every seed in that
window eventually has an empty menu.

### I. Mathematical yield

```text
Known rediscoveries:     3y=5x+18 / 5x+22 on residues 0 and 1;
                         seed-0 orbit to 12284; length-1 algebra
                         x=-9,-11; CLASS gcd obstructions
New exact identities:    none beyond the problem definition
New branch/domain certificates: engine EXACT congruence domains
                         (KNOWN arithmetic; DISCOVERED labels)
New cycle obstructions:  mixed length-2/3 words; constant-word
                         candidates outside n>=0. KNOWN (A-B)|C
New terminal/reachability obstructions: empty menu at residue 2;
                         seed-0 exact closure. KNOWN
New counterexamples:     monotone descent; one-step contraction;
                         seed closure as map contraction
New conjectures:         none
New Lean theorems:       packaging of KNOWN identities; no ledger
Potentially new mathematics: none claimed
Engineering changes:     0
```

Prior-art classes:

| Result | Class |
|--------|-------|
| Two affine lines and mod-3 control | `KNOWN_REDISCOVERY` (Michel / Yolcu). **DISCOVERED** by the engine |
| \(x=-9,-11\) | `KNOWN_REDISCOVERY` / `NEW_FORMALIZATION` in Lean |
| Mixed-word CLASS obstruction | `KNOWN_REDISCOVERY` of Engine divisibility |
| Seed-0 finite orbit | `KNOWN_REDISCOVERY` (Aaronson / wiki trajectory) |
| Window halt \(0..80\) | `NEW_COMPUTATIONAL_OBSERVATION`, not a theorem |
| Universal convergence of \(B\) | not obtained |

No `POTENTIALLY_NEW_THEOREM`.

### J. Lean

Strongest exact results, all **KNOWN**: unique successor; two-line
clearing; undefined residue 2; Euclidean division on each line;
length-1 candidates; no nonnegative fixed point.

No ledger row.

### K. Prior-art reconciliation

| Literature | Engine |
|------------|--------|
| Michel: TM simulates \(B\) | **Not given** to the adapter. Not rediscovered as a TM fact |
| Yolcu–Aaronson–Heule: \(B\) and failed SRS termination | Engine reconstructed \(B\)'s affine language from the integer relation and did **not** prove termination |
| BB(5)=47,176,870 | Independent of this campaign. Seed-0 halt is necessary for the champion's blank-tape run and is **not** billed as BB(5) |
| Totality of the 5-state machine | **Not** addressed. Distinct from map convergence and from BB(5) |

The 2021 paper's failure to prove SRS termination is **not** repaired
here. The engine's yield is reconstruction of the research language
plus KNOWN cycle-class arithmetic.

### L. Engineering backlog

Not implemented. Recurring coarseness only:

```text
Problem              Distinguish finite seed closure from map contraction
Affected component   RegimeFingerprint core dimensions
Semantic mismatch    Expanding 5/3 steps billed FINITE_CONTRACTING
                     because seed 0 closes
Minimal example      partial_five_three seed 0; also slc_rplus
Mathematical importance  High: Collatz-like expanding maps cluster with
                         digit-fold cores and FAMILY_SATURATE
Potential generic fix    Core contraction from a window magnitude census
```

No singleton-census or nondeterminism issue on this target. No
involution-census issue.

### M. Research decision

Isolated engine: `CONTINUE`. Seeded engine: `FAMILY_SATURATED`. Campaign
decision: `PARK`.

## Open questions

Whether every nonnegative orbit of \(B\) eventually hits
\(n\equiv 2\pmod{3}\) remains a Collatz-like question. Do not assign it
to the engine. Do not identify it with BB(5).

## Decision

`PARK`. The frozen stack independently recovered the two residue-
selected affine branches, certified their domains, composed control
words, and proved class-level cycle obstructions, including that the
only length-1 solutions lie outside \(n\ge 0\). That is automatic
reconstruction of Michel's language, not a new theorem and not a
termination proof. The remaining dynamical question is the known
convergence problem. Do not auto-continue into proving totality of
\(B\) or of the 5-state machine.

Best next question: which other frozen-engine mathematical target
should be consumed next, leaving parked fingerprint coarseness and
the open convergence of \(B\) untouched?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as verification, Busy
Beaver, or number theory. Value is a frozen-engine campaign whose
primary metric is mathematical yield against a contemporary
Collatz-adjacent target.
