# Research Engine v2 first real-problem campaign

Status: **EXPLORATORY**

This is an engine-capability campaign. It does **not** claim a Collatz
solution, a Euclidean-algorithm theorem, or a new \(mx+r\) identity.
Adapters live in `research.mx_plus_r`, `research.euclidean_quotient`,
and `research.engine_campaign`. There is no `FiveXPlusOneAttack` and no
`EuclideanSpecificAttack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Can the same Research Engine v2 loop

```text
observe → infer → certify → compose → constrain → obstruct → decide
```

turn genuinely different exact dynamics into certified structure,
without adapting each target to a favourite attack?

## Exact statement

On hint-free `ProblemSpec` adapters, does unmodified `ResearchLoop`
(i) recover a parameterized family \(2^k y=mx+r\) across several odd
\((m,r)\); (ii) distinguish local control language from global seed
behaviour on \(T_5\); (iii) transfer that language to Euclidean
remainder dynamics \((a,b)\mapsto(b,a\bmod b)\); then (iv) let
`score_candidate` select Target D from a fixed pool? Window agreement
is not a map theorem on \(\mathbb{Z}\). Seed-orbit finiteness is not
numerical contraction of the map.

## Current literature

- Accelerated \(3x+1\): ledger `C-T-welldefined`, Lean `acceleratedT`.
  **KNOWN**. Engine consumer: [syracuse.md](syracuse.md).
- Generalized \(qx+1\) / \(mx+r\): Crandall
  (`crandall-1978-3x+1`), Chamberland
  (`chamberland-2003-3x+1-survey`), Lagarias
  (`lagarias-2010-3x+1-survey`). **KNOWN**.
- \(5x+1\) as a hard relative with extra cycles and apparently
  divergent orbits: **KNOWN** (Crandall). Finite seed cycles are not
  global convergence.
- Euclidean algorithm / quotient sequences: Knuth
  (`knuth-taocp-vol2`); dynamical statistics (Vallée,
  `vallee-2006-euclidean-algorithm`). **KNOWN**.
- Digit-fold family: SignedP0, \(s(n)\), \(W(n)\) independently
  `SATURATED`. WeightDrift excluded. **PROJECT-SPECIFIC** diagnosis,
  classical maps.

Project relationship: **engine diagnosis / rediscovery**. No new
number-theory theorem is claimed.

## Branch budget

```text
Mathematical target     Can the same v2 loop diagnose, attack, and
                        certify structure across mx+r, 5x+1, Euclidean
                        remainder dynamics, then select Target D?
Novelty hypothesis      Transfer of latent-control → domain → word →
                        obstruction outside Syracuse, and possibly
                        valuation-control → quotient-control.
Falsifier               Adapter seeds v2/quotients/cycles; Collatz
                        language; new attack modules before the first
                        unmodified run; D overridden by taste.
Existing machinery      ResearchLoop; census → domain → word →
                        obstruction; Syracuse adapter as 1-D template.
Maximum Phase-0 scope   Thin adapters + corpus-seeded runner +
                        unmodified loop + one dossier. Lean only for
                        a recovered generic identity.
Promotion criterion     Exact certificates in more than one domain, or
                        a precise ENGINE_LIMITATION naming a missing
                        reusable abstraction.
Stop criterion          New *Control / *Attack types; Collatz
                        escalation; infrastructure before the first
                        unmodified run.
```

## Balanced-ternary formulation

None. The adapters use ordinary integer arithmetic.

## Why BT may be relevant

It is not required. The saturated digit-fold family is a comparison
cluster so the campaign can ask whether new targets leave that regime.

## Candidate operations / invariants

- Parameterized family \(2^k y = m x + r\). **OBSERVATION** on a
  window; the integer iff with \(v_2(mx+r)=k\) is **EXACT — LEAN
  VERIFIED** (`mxPlusR_parameter_iff`) and **KNOWN**.
- Maximal-divisibility parameter domain. **OBSERVATION** on the window;
  relation exactness as in ParameterDomain.
- Control-word composition and class/symbolic/recursive obstructions.
  **KNOWN** arithmetic via Engine lemmas.
- Euclidean remainder orbit of one seed. **FINITE-HORIZON EXACT**
  closure; **KNOWN** termination of gcd.
- Seed 27 is a 3-cycle of \(T_5\). **FINITE-HORIZON EXACT** for that
  seed; not a classification of \(5x+1\) cycles.

## Experiments

- `tests/research/mx_plus_r/test_mx_plus_r.py`
- `tests/research/euclidean_quotient/test_euclidean_quotient.py`
- `tests/research/engine_campaign/test_engine_campaign.py`
- Runner: `research.engine_campaign.runner.run_campaign`

## Conjectures

None opened.

## Counterexamples

- “Default seed 27 is a long mixed-magnitude trajectory for every
  \(T_{m,r}\).” **REFUTED** for \((m,r)=(5,1)\): \(27\mapsto 17\mapsto 43\mapsto 27\).
- “Same local family \(2^k y=mx+r\) implies the same core fingerprint.”
  **REFUTED**: \((3,1)\), \((5,3)\), \((7,1)\) stay `MIXED_MAGNITUDE` /
  `UNBOUNDED_SAMPLE`; \((3,-1)\) and seed-27 \(T_5\) close finitely and
  are billed as `FINITE_CONTRACTING`.
- “C.0 Euclidean remainder is engine `ENGINE_LIMITATION`.” **REFUTED**
  as an enum outcome: exact seed closure yields `CLOSE`, while the
  census chain is simply inapplicable.

## Formalization

`formal/Problems/Engine/MxPlusR.lean`: `mxPlusR_parameter_iff`,
`mxPlusR_compose_two`, `mxPlusR_len_one_cycle_dvd`. Generic Engine
lemmas, not map theorems. No `sorry`. No ledger row (KNOWN). Target D
reuses existing `hiddenCongruenceA` identities. Euclidean termination
is not re-formalized.

## Results

### A. Engine baseline

Unmodified planner order: reconnaissance → piecewise_affine →
parameter_domain → control_word → control_obstruction → … Census is
1-D singleton integer only. `AffineSystem` is multi-D with **fixed**
\(A\) and \(b_u\). Digit-fold cores `SATURATED` from SignedP0, digit-sum,
and weight (CLOSE). Syracuse `CONTINUE` against that family. WeightDrift
is a non-member expanding control. `HiddenFiveClearSpec` is **not**
\(5x+1\).

### B. Target A — generalized accelerated \(T_{m,r}\)

Adapter `MxPlusRSpec`: dummy control, identity observation, no \(v_2\),
`affine_system()=None`. Pairs \((3,1)\), \((3,-1)\), \((5,1)\),
\((5,3)\), \((7,1)\).

Every pair recovered

\[
2^k y = m x + r
\]

as `PARAMETERIZED_CENSUS`, domain `EXACT`, algebra `EXPLOITABLE`,
obstruction scopes `WORD|CLASS|SYMBOLIC_CLASS|RECURSIVE_INVARIANT`.
Observed \(k\) vary; all bases are \(2\).

| Pair | Engine decision | Nearest | Delta | Core contraction / region |
|------|-----------------|---------|-------|---------------------------|
| \((3,1)\) | `CLOSE` | syracuse | LOW | `MIXED_MAGNITUDE` / `UNBOUNDED_SAMPLE` |
| \((3,-1)\) | `FAMILY_SATURATED` | digit-sum | MEDIUM | `FINITE_CONTRACTING` / `FINITE_SEED_CLOSURE` |
| \((5,1)\) | `FAMILY_SATURATED` | \(T_{3,-1}\) | LOW | `FINITE_CONTRACTING` / `FINITE_SEED_CLOSURE` |
| \((5,3)\) | `CLOSE` | syracuse | LOW | `MIXED_MAGNITUDE` / `UNBOUNDED_SAMPLE` |
| \((7,1)\) | `CLOSE` | syracuse | LOW | `MIXED_MAGNITUDE` / `UNBOUNDED_SAMPLE` |

Odd-window magnitude (n=1..79 odd, **EMPIRICAL**): \((3,1)\) 19 drops /
20 growths / 1 equal; \((3,-1)\) 20 / 19 / 1; \((5,1)\) 10 / 30 / 0;
\((5,3)\) 9 / 30 / 1; \((7,1)\) 9 / 30 / 1.

Answers to the A questions: (1–4) yes, the existing chain generalizes
across the family; (5) recursive remainder fires on the same path as
Syracuse (KNOWN growth identities); (6–7) fingerprints cluster
Syracuse-like mixed maps together and separate seed-closed maps, but
that split is a **seed-orbit artefact**, not a new dynamical invariant;
(8) no new behavioural quotient; (9) recurrent structure is seed-exact
when the default seed 27 hits a cycle; (10) all recovered identities
are **KNOWN**.

### C. Target B — accelerated \(5x+1\)

Same adapter, \((m,r)=(5,1)\). Local language equals the family:
\(2^k y=5x+1\), domain exact, full obstruction stack.

Global regime is **not** the Syracuse mixed-unbounded core **for seed
27**, because that seed is a 3-cycle

\[
27\mapsto 17\mapsto 43\mapsto 27
\]

(**FINITE-HORIZON EXACT**). The odd-window census still shows net
growth (30 vs 10). Orbit of 7 is recorded and is **not** used as a
divergence theorem. Same local control does not imply the same core
fingerprint; the core uses seed closure as if it were map contraction.

### D. Target C — Euclidean remainder dynamics

Adapter: dimension 2, \((a,b)\mapsto(b,a\bmod b)\), dummy control, no
quotient. Seed \((1071,462)\).

- `piecewise_affine` inapplicable (`dimension != 1`).
- Domain / control-word / obstruction skipped as dependents.
- Closure: exact residual size 4 (**FINITE-HORIZON EXACT**, **KNOWN**
  gcd termination).
- Fingerprint: `INTEGER_VECTOR`, `SINGLETON`, `FINITE_CONTRACTING`,
  `FINITE_SEED_CLOSURE`; latent-control fields `UNOBSERVED`.
- Engine decision: `CLOSE` (not `ENGINE_LIMITATION`). C.1 vector census
  is **not** built: the gate required the engine enum
  `ENGINE_LIMITATION`. The missing reusable structure remains
  \(y=A_u x+b_u\) with control-dependent \(A\).
- Behavioural quotient, if any, is state equivalence, not \(a//b\).

Valuation-control \(\to\) quotient-control transfer **did not occur**
with the current census.

### E. Target comparison

Digit-fold cores stay a separate cluster from Syracuse-like
`MIXED_MAGNITUDE`/`UNBOUNDED_SAMPLE` maps. Euclidean is
`INTEGER_VECTOR` and does not core-match digit-fold. \(T_{3,-1}\) and
seed-27 \(T_5\) **do** core-match digit-fold because finite seed
closure forces `FINITE_CONTRACTING`. That is a diagnosis coarseness,
not evidence that \(5x+1\) is a digit fold.

### F. Capability coverage

Exercised on A/B (evidence-gated): latent piecewise-affine control,
parameter-domain certification, valuation dynamics, control-word
composition, cycle obstruction, control-obstruction calculus, symbolic
multi-step obstruction, recursive remainder invariant, growth,
numerical contraction, infinite reachable trajectories (unbounded
members). Euclidean exercised finite closure on a 2-D seed, not latent
quotient control. `symbolic_control` remains `NOT_TESTED` (deferred
attack). Do not mark quotient control exercised.

### G. Prior art

| Class | Item |
|-------|------|
| KNOWN MATHEMATICS | \(2^k y=mx+r\); padic iff; Euclidean gcd; \(5x+1\) cycles; congruence piecewise maps |
| ENGINE REDISCOVERY | family, domain, words, obstructions on every \((m,r)\); 27-cycle of \(T_5\); Euclidean seed closure |
| NEW GENERIC ENGINE CAPABILITY | none added; the campaign **consumed** existing attacks |
| POTENTIALLY NEW MATHEMATICS | none claimed |

### H. Lean

`mxPlusR_parameter_iff`, `mxPlusR_compose_two`,
`mxPlusR_len_one_cycle_dvd`. No ledger.

### I. Infrastructure changes

Thin `ProblemSpec` adapters and an in-process corpus runner. No new
engine attack. No CLI. C.1 not implemented.

### J. ResearchLoop selection

After A–C, `score_candidate` on six sketches (default claimed
capabilities = full `CAPABILITIES` list). Restricted claimed-capability
lists had collapsed every value to 0 because A/B already exercised
those names; the default list restores a nonzero capability gap.
Lexicographic tie-break remains in `score_pool`. Winner is consumed as
Target D with **no taste override**.

### K. Target D

Selected spec is the highest `SelectionReport.value` in the fixed pool
(finite piecewise-affine congruence, Möbius pair, transducer parity
carry, \(x^2-2\), \(7x+1\), subtractive Euclidean). The winner is run
through the same unmodified `ResearchLoop`. The hidden-congruence
synthetic already has Lean identities in `PiecewiseCensus.lean`. Engine
decision `FAMILY_SATURATED` / dossier `CLOSE` is a capability reuse,
not new mathematics.

### L. ComplexityProfiles

Existing schema. mx+r: `control_count=1`, reachable count unset when
the seed is not a closed residual within the cap. Euclidean: reachable
count equals the gcd orbit length when the remainder hits 0.
Census/word/obstruction counts stay on `AttackResult.evidence`.

### M. Final research assessment

v2 **does** generalize latent affine-control across a parameterized
\(mx+r\) family and **does** distinguish some global seed behaviours,
but the distinction is polluted by using seed-closure as a core
contraction feature. It **does not** transfer valuation control to
Euclidean quotient control: the 1-D census gate and fixed-\(A\)
`AffineSystem` are the obstruction. `score_candidate` can rank a next
target once capability claims are not restricted to already-exercised
names. The engine is producing **attack surfaces** (certified families
and obstructions) rather than new theorems. Its effective range is
still concentrated in 1-D affine/valuation dynamics.

Evidence levels used above: **EMPIRICAL** (window growth counts),
**FINITE-HORIZON EXACT** (seed orbits, Euclidean closure),
**LEAN CERTIFIED** (generic \(2^k y=mx+r\) iff), never a universal
map theorem on all odd positives.

## Open questions

Answered by [vector_affine.md](vector_affine.md): yes — Euclidean and
an unrelated parity-shear map both consume `vector_affine`; that
branch is `PARK`. Remaining open: matrix-word recursive invariants
when entrywise magnitude domination fails.

## Decision

`PARK`. The campaign answered its engine questions. Recovered
identities are **KNOWN**. Quotient-control transfer failed for a named
generic reason and was not patched in Phase 0; the follow-up
vector-affine experiment closed that gap as a capability transfer, not
as new Euclidean mathematics. Do not auto-continue into Collatz. Do not
open a dedicated \(5x+1\) branch because of a 3-cycle at seed 27.

Best next question (answered): see [vector_affine.md](vector_affine.md).
Next from that dossier: can matrix-word recursive invariants obstruct
infinite control classes when entrywise magnitude domination fails?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as number theory. Value
is the first multi-domain consumption of Research Engine v2.
