# Generic vector-affine latent control

Status: **EXPLORATORY**

This module is an engine-capability experiment. It does **not** reopen
[engine_campaign.md](engine_campaign.md) as a Collatz or Euclidean
theorem program. There is no `EuclideanControl` and no
`EuclideanMatrix` type. Hidden synthetics live in
`research_engine.benchmarks.hidden_vector_affine`.

## Problem

Can Research Engine v2 discover, certify, compose, and obstruct hidden
control-dependent affine maps

\[
\mathbf{y}=A_u\mathbf{x}+\mathbf{b}_u
\]

on \(\mathbb{Z}^d\) (\(d\ge 2\)) from exact I/O alone, and does that
language transfer to Euclidean remainder dynamics and at least one
unrelated 2-D lattice map?

## Exact statement

Given a dimension-\(d\ge 2\) integer `ProblemSpec` with singleton
control and no supplied `AffineSystem`, does `vector_affine`

1. recover finite or parameterized matrix branches from samples;
2. certify an arithmetic predicate for the latent control \(u\);
3. compose matrix words to \(M\mathbf{x}+\mathbf{c}\);
4. derive cycle constraints \((M-I)\mathbf{x}=-\mathbf{c}\) and prove
   at least word- or class-level integer impossibilities when they
   hold;
5. consume Euclidean \((a,b)\mapsto(b,a\bmod b)\) and an unrelated
   parity-shear map with the same attack?

Window agreement is not a \(\mathbb{Z}^d\)-theorem for the map.

## Current literature

- Integer affine systems \(x'=Ax+b_u\) with shared \(A\): existing
  `AffineSystem`. **KNOWN**. Control-dependent \(A_u\) is the gap.
- Euclidean algorithm / quotient sequences: Knuth
  (`knuth-taocp-vol2`); Vallée (`vallee-2006-euclidean-algorithm`).
  Matrix form of one Euclidean step is **KNOWN**.
- Scalar latent control: [piecewise_affine_census.md](piecewise_affine_census.md),
  [control_word_composition.md](control_word_composition.md),
  [control_obstruction.md](control_obstruction.md). **PROJECT-SPECIFIC**
  engine capability; mathematics **KNOWN**.
- Prior campaign: [engine_campaign.md](engine_campaign.md) recorded that
  Euclidean failed the 1-D census gate. **PROJECT-SPECIFIC**.

Project relationship: **new generic engine capability**. Euclidean
identities rediscovered by v2 are not new number theory.

## Branch budget

```text
Mathematical target     Can latent control generalize from scalar
                        a_k x+b_k to vector A_u x+b_u, including
                        Euclidean as a consumer?
Novelty hypothesis      Same observe→infer→certify→compose→obstruct
                        loop works in dimension ≥ 2 without
                        Euclidean-specific attacks.
Falsifier               Euclid-only hardcoding; AffineSystem injection;
                        fitted matrices billed as Z-theorems; scalar
                        regression.
Existing machinery      AffineSystem arithmetic; scalar census chain;
                        diagnosis loop; EuclideanSpec (hint-free).
Maximum Phase-0 scope   vector_affine attack + synthetics A–D + Euclid
                        + unrelated parity shear + Lean composition /
                        cycle / obstruction; one dossier.
Promotion criterion     Euclid and an unrelated 2-D system both consume
                        the same attack with certified domains.
Stop criterion          Euclid-only solver; machinery gravity; only
                        KNOWN rediscovery with no reusable layer.
```

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required. Digit-fold cores remain a comparison cluster.

## Candidate operations / invariants

- Finite branches \(\mathbf{y}=A\mathbf{x}+\mathbf{b}\) on congruence
  regions. **OBSERVATION** / **EXACTLY_CERTIFIED** on a falsify window.
- Parameterized family \(A_k=A_0+kD\). **OBSERVATION**.
- Quotient / valuation predicates for \(k\). **OBSERVATION** on the
  window; direction `EXACT` after counterexample survival.
- Composition \(z=C(Ax+b)+d=(CA)x+(Cb+d)\). **EXACT — LEAN VERIFIED**
  (`compose_two_vector_affine`). **KNOWN** algebra.
- Cycle \((M-I)x=-c\). **EXACT — LEAN VERIFIED**
  (`cycle_of_vector_affine`). **KNOWN**.
- Determinant / Cramer obstruction. **EXACT — LEAN VERIFIED**
  (`vector_cycle_impossible`). **KNOWN**.
- Euclidean matrix \(\begin{pmatrix}0&1\\1&-q\end{pmatrix}\).
  **KNOWN** specialization (`euclidean_step_matrix`).

## Experiments

- `tests/research_engine/core/test_vector_affine.py`
- Synthetics: `HiddenFiniteAlphabetSpec`,
  `HiddenParameterizedMatrixSpec`, `HiddenDomainCoupledSpec`,
  `HiddenFalseAffineTrapSpec`, `HiddenParityShearSpec`
- Consumer: `research.euclidean_quotient.spec.euclidean_spec`

## Conjectures

None opened.

## Counterexamples

- Global identity on the trap map inside the sample box: **REFUTED** by
  points outside the box (\(x\mapsto 2x\)).
- Spurious tiny-support matrices defining a family direction:
  **REFUTED** by restricting family discovery to large-support
  branches.
- Billing Python `%` recovery as a new Euclidean theorem: explicitly
  rejected; mathematics is **KNOWN**.

## Formalization

`formal/Problems/Engine/VectorAffine.lean`:

- GENERIC: `compose_two_vector_affine`, `cycle_of_vector_affine`,
  `vector_cycle_dvd`, `vector_cycle_impossible`, `shear_compose`
- EUCLIDEAN SPECIALIZATION / KNOWN: `euclideanMatrix`,
  `euclidean_step_matrix`

No `sorry`. No ledger row (KNOWN algebra).

## Results

### A. Generic vector-affine architecture

New attack `vector_affine` after the scalar chain. Types:
`VectorAffineBranch`, `VectorAffineFamily`, `VectorAffineCensus`.
Composition and cycle helpers reuse `AffineSystem` matrix arithmetic.
Scalar `PiecewiseAffineCensus` / `ParameterDomain` / `ControlWord` /
`control_obstruction` are unchanged. Fingerprint gains
`affine_control_type` (`SCALAR|VECTOR|MATRIX_PARAMETERIZED`).
Capability `latent_vector_affine_control`.

### B. Synthetic discovery

| Target | Census | Domain | Notes |
|--------|--------|--------|-------|
| Finite alphabet | `FINITE_CENSUS` | congruence mod 2 on \(x_0\) `EXACT` | matrices \(((1,0),(0,1))\), \(((0,-1),(1,0))\) |
| Parameterized shear | `PARAMETERIZED_CENSUS` | valuation \(v_2(\lvert x_0\rvert+1)\) `EXACT` | \(A_k=((1,k),(0,1))\), offset \((1,1)\) |
| Domain-coupled | `PARAMETERIZED_CENSUS` | valuation of \(x_0-x_1\) `EXACT` | same shear family, offset \(0\) |
| False trap | identity `SUPPORTED_BY_SAMPLES` with cex | — | not `EXACTLY_CERTIFIED` |

### C. Matrix control words

Parameterized family composes words; length-one and length-two
relations are algebraically composed. Shear class obstruction fires
when offsets force inconsistent cycles (`CLASS`).

### D. Vector obstruction

Word-level determinant / inconsistent linear systems; class-level when
all observed length-one parameters obstruct. Lean
`vector_cycle_impossible` packages the Cramer obstruction.

### E. Euclidean consumer

Hint-free `EuclideanSpec`. Recovered

\[
A_k=\begin{pmatrix}0&1\\1&0\end{pmatrix}
+k\begin{pmatrix}0&0\\0&1\end{pmatrix},
\quad
\mathbf{b}=\mathbf{0},
\]

with quotient domain \(k=-\lfloor a/b\rfloor\) (`k_scale=-1`) certified
`EXACT` after falsify-window survival. Scalar `piecewise_affine`
remains inapplicable. Relations compose; seed gcd closure remains
**FINITE-HORIZON EXACT** and **KNOWN**.

### F. Unrelated vector consumer

`HiddenParityShearSpec`: finite census with matrices
\(((1,1),(0,1))\) and \(((1,0),(1,1))\) on congruence of \(x_0+x_1\)
mod 2. Same attack. No remainder arithmetic in the benchmark source.

### G. Comparative fingerprints

| Target | `affine_control_type` | Latent | Domain |
|--------|----------------------|--------|--------|
| digit-fold (seeded) | UNOBSERVED / SCALAR secondary | — | — |
| scalar \(mx+r\) / Syracuse | SCALAR | PARAMETERIZED | EXACT |
| Euclidean | MATRIX_PARAMETERIZED | PARAMETERIZED | EXACT |
| parity shear | VECTOR | FINITE | EXACT |
| parameterized shear | MATRIX_PARAMETERIZED | PARAMETERIZED | EXACT |

Digit-fold cores do not absorb Euclidean once vector language is
present; decision uses MEDIUM delta + vector recovery as
`CONTINUE`-eligible.

### H. Lean

See Formalization. GENERIC vs EUCLIDEAN SPECIALIZATION separated.

### I. Prior art

| Class | Item |
|-------|------|
| KNOWN MATHEMATICS | matrix affine composition; Euclidean step matrix; quotient sequences |
| ENGINE REDISCOVERY | \(A_q\) family and quotient domain from I/O; synthetic shears |
| NEW GENERIC ENGINE CAPABILITY | vector_affine census → domain → matrix words → obstruction |
| POTENTIALLY NEW MATHEMATICS | none claimed |

### J. ComplexityProfile

Unchanged schema. Matrix counts live on `AttackResult.evidence`
(`branch_count`, `relations`, `certificates`, `domains`).

### K. Research decision

Engine decisions on consumers: Euclidean and parameterized synthetics
`CONTINUE` when domain is certified and the vector language is novel
relative to the corpus; trap stays observational. Dossier mapping:

```text
CONTINUE
```

→ branch `PARK`. Capability succeeds; mathematics is **KNOWN**. Do not
auto-open an Euclidean research program.

## Open questions

Answered by [matrix_word_invariant.md](matrix_word_invariant.md): yes —
non-magnitude recursive class obstructions exist; that branch is
`PARK` and the attack architecture is frozen.

## Decision

`PARK`. v2 transfers latent control from scalar affine arithmetic to
genuinely multi-dimensional controlled affine dynamics. Euclidean and
an unrelated lattice map both consume the same attack. The identities
are **KNOWN**. Do not escalate to an Euclidean solver.

Best next question (answered): see
[matrix_word_invariant.md](matrix_word_invariant.md).

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as number theory. Value is
the generic vector-affine latent-control layer.
