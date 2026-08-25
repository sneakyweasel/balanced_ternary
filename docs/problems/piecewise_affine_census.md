# Generic piecewise-affine census

Status: **EXPLORATORY**

This module is an engine-capability experiment. It is not a Collatz
solver and does not reopen [collatz.md](collatz.md). Hidden maps live in
`research_engine.benchmarks`; there is no `research.piecewise_affine`
application package.

## Problem

Can Research Engine v2 recover latent affine branches and a hidden
arithmetic control from exact input/output behavior, without being told
the partition, modulus, or valuation?

## Exact statement

Given a 1-D integer `ProblemSpec` with singleton control and no supplied
`AffineSystem`, does `PiecewiseAffineCensus` infer a sample-supported
decomposition \(q y = p x + r\) on discovered regions, distinguish a
finite table from a parameterized \(b^k\) family, and can
`parameter_domain` then synthesize and certify the arithmetic predicate
for each parameter without map-specific hints? Window agreement is not a
\(\mathbb{Z}\)-theorem for the map.

## Current literature

- Integer affine systems \(x' = Ax + b_u\): existing engine
  `AffineSystem`. **KNOWN**.
- Accelerated odd-only map: ledger `C-T-welldefined`, Lean
  `acceleratedT_mul`. **KNOWN**. Engine rediscovery of
  \(2^k S(n)=3n+1\) from I/O is not a new identity. The arithmetic
  relation \((b^k y=q \land b\nmid y)\leftrightarrow v_b(q)=k\) is
  **KNOWN** integer arithmetic (`mul_pow_eq_iff_padicValInt`).
- Piecewise-affine control of Collatz-type maps: classical; not claimed
  here as original mathematics.
- Previous Syracuse benchmark: [syracuse.md](syracuse.md) recorded
  `ENGINE_LIMITATION` before the census existed.

## Branch budget

```text
Mathematical target     Can v2 recover a piecewise-affine law with
                        latent control from exact I/O, without being
                        told the partition, modulus, or valuation?
Novelty hypothesis      A reusable census (finite vs parameterized),
                        not a new Collatz theorem.
Falsifier               Branch rules or 3x+1/v2 are seeded; digit-fold
                        core fingerprints change; a sample is billed
                        as a global branch theorem.
Existing machinery      AttackPlanner, AffineSystem, diagnosis loop,
                        integer probes, Syracuse adapter (hint-free).
Maximum Phase-0 scope   Census algorithm + four hidden synthetics;
                        Lean only for an exact synthetic identity.
Promotion criterion     Synthetics recover hidden structure with
                        counterexample-first status; then Syracuse
                        is re-diagnosed.
Stop criterion          Syracuse-specific predicates; planner
                        injection of invariants; machinery gravity.
```

## Balanced-ternary formulation

None required. The census uses ordinary integer I/O.

## Why BT may be relevant

SignedP0 admits a secondary residue-mod-3 affine census. That is a
local description of an existing BT operator iterate, not a reason to
reopen the saturated digit-fold family.

## Candidate operations / invariants

- Finite branches \(y=px+r\) on congruence, sign, interval, or
  valuation regions. **OBSERVATION** on a stated window.
- Parameterized family \(b^k y = p x + r\) from a coefficient box
  \(|p|,|r|\le 9\), bases \(\{2,3,5,7\}\), \(k\le 12\). **OBSERVATION**.
- Maximal-divisibility conjunction \(b^k\mid q \land b^{k+1}\nmid q\)
  as the exact parameter predicate. **OBSERVATION** on the window; the
  integer iff with \(v_b(q)\) is **EXACT — LEAN VERIFIED** and **KNOWN**.
  Presentation \(k=v_b(q)\) only after that conjunction is certified.
  Mere \(b^k\mid q\) is **NECESSARY_ONLY** when higher \(k\) exist.
- Synthetic A identities in Lean. **EXACT — LEAN VERIFIED**, **KNOWN**.
- \(2^k S(n)=3n+1\). **KNOWN** (`acceleratedT_mul`); engine rediscovery
  from samples is **OBSERVATION**, not a new theorem.

## Experiments

- `tests/research_engine/core/test_piecewise_affine.py`
- `tests/research_engine/core/test_parameter_domain.py`
- Hidden specs: `research_engine.benchmarks.hidden_piecewise`
- Corpus: SignedP0, DigitSumDynamics, WeightDynamics, WeightDrift,
  Syracuse via existing planners
- CLI: `btlab research analyze|attack … piecewise_affine|parameter_domain`

## Conjectures

None opened.

## Counterexamples

- Two-point lines are not promoted (`MIN_SUPPORT = 3`).
- Intersection points of distinct affine maps do not block a complete
  residue or sign region.
- Naive global affine on Syracuse: mixed samples refute a single
  \((p,q,r)\) with \(q=1\).
- Finite branch table on synthetic D / Syracuse: refused in favor of
  `PARAMETERIZED_CENSUS`.
- Mere divisibility \(b^k\mid q\) on an unbounded family: **NECESSARY_ONLY**
  when higher parameters exist (synthetic B trap).

## Formalization

`formal/Problems/Engine/PiecewiseCensus.lean`: `hiddenCongruenceA` and
the three residue identities. `formal/Problems/Engine/ParameterDomain.lean`:
generic iff \((b^k y=q \land b\nmid y)\leftrightarrow v_b(q)=k\). No
`sorry`. No ledger row (KNOWN elementary arithmetic). Syracuse Lean remains
`formal/Problems/Collatz/Syracuse.lean` / `Accelerated.lean`.

## Results

### A. Engine upgrade

Attacks `piecewise_affine` then `parameter_domain` in
[`src/research_engine/attacks/piecewise_affine.py`](../../src/research_engine/attacks/piecewise_affine.py)
and
[`src/research_engine/attacks/parameter_domain.py`](../../src/research_engine/attacks/parameter_domain.py).
Planner chains `AttackContext.prior_results` after each recorded result;
`AttackContext.affine` is not injected. Types: `AffineBranch`,
`BranchRegion`, `LatentControl`, `PiecewiseAffineCensus`, `AffineFamily`,
`ParameterDomain`, `DomainCertificate`, `AffineFamilyCertificate`.
Non-core fingerprint fields `piecewise_affine_structure`,
`latent_control`, `parameter_domain`. Capabilities
`latent_piecewise_affine_control` and `parameter_domain_certification`.
`valuation_dynamics` is exercised only given a parameterized family
plus an exact maximal-divisibility conjunction. `ComplexityProfile`
unchanged.

### B. PiecewiseAffineCensus and domain synthesis

Samples a stated window plus the seed orbit. Candidate lines from pairs
with support \(\ge 3\), then region inference by completeness. A
coefficient box searches \(b^k y = px+r\) for bases \(\{2,3,5,7\}\).
`parameter_domain` relabels samples by inferred \(k\), tries congruence,
divisibility, maximal conjunction, and mixed residue AND maximal, then
falsifies both directions. Predicate direction: `NECESSARY_ONLY` /
`SUFFICIENT_ONLY` / `EXACT` / `REFUTED` / `UNDERDETERMINED`. Map
globality on \(\mathbb{Z}\) is not claimed from samples.

### C. Synthetic benchmark results

Ground truth is in tests, not on the specs.

| Target | Ground truth | Discovered | Kind | Domain |
|--------|--------------|------------|------|--------|
| A (census) | \(2x+1,x-4,3x\) on \(x\bmod 3\) | three congruence branches | `FINITE_CENSUS` | window-exact residues |
| B (census) | \(2x+3\) (\(x\ge 0\)), \(x-5\) (\(x<0\)) | sign regions | `FINITE_CENSUS` | |
| C (census) | even \(2x\); odds split \(\bmod 6\) | four congruence branches | `FINITE_CENSUS` | |
| D (census) | \((x+1)/2^{v_2(x+1)}\) | family \(p=1,r=1\), several \(k\) | `PARAMETERIZED_CENSUS` | |
| A (domain) | maximal \(v_2(x+1)\) | conjunction \(2^k\mid q\land 2^{k+1}\nmid q\) | `EXACT` | Lean iff; not mere divisibility |
| B (domain) | non-maximal trap | \(2^k\mid q\) | `NECESSARY_ONLY` | higher \(k\) refute sufficiency |
| C (domain) | odd-prime \(v_3(x+1)\) | base 3 maximal | `EXACT` | not secretly base 2 |
| D (domain) | residue \(\bmod 6\) AND maximal | mixed conjunction | `EXACT` | |
| E (domain) | finite table (census A) | three congruences | window-exact | not a \(\mathbb{Z}\)-theorem |
| F (domain) | unbounded family (census D) | parameterized, not a table | `PARAMETERIZED` | |

### D. Corpus comparison

Core fingerprints (family clustering) are unchanged.

| Target | Core class | piecewise / latent / domain | Census |
|--------|------------|-----------------------------|--------|
| SignedP0 | `INTEGER_1D\|SINGLETON\|FINITE_CONTRACTING\|FINITE_SEED_CLOSURE` | `FINITE` / window domains | secondary: \(y=-x,-x\pm 1\) on \(x\bmod 3\) |
| DigitSumDynamics | same core | `UNCERTAIN` | `UNRESOLVED` |
| WeightDynamics | same core | `UNCERTAIN` | `UNRESOLVED` |
| WeightDrift | `MIXED_MAGNITUDE\|UNBOUNDED_SAMPLE` | `UNCERTAIN` | `UNRESOLVED`; still not in the digit family |
| Syracuse | `MIXED_MAGNITUDE\|UNBOUNDED_SAMPLE` | `PARAMETERIZED` / domain `EXACT` | family \(p=3,r=1\), \(q=2^k\); maximal conjunction |

Digit-fold family remains `SATURATED`. SignedP0's residue census is
secondary and does not reopen that family.

### E. Syracuse diagnosis

Census: sample-supported family \(2^k y = 3x+1\). Domain attack:
conjunction \(2^k\mid(3x+1)\land 2^{k+1}\nmid(3x+1)\) is `EXACT` for the
relation; presentation \(k=v_2(3x+1)\) only after that. Mere
divisibility is `NECESSARY_ONLY`. Engine decision `CONTINUE` (arithmetic
relation certified; map globality on \(\mathbb{Z}\) empirical). Adapter
still hint-free. **KNOWN** as `acceleratedT_mul`. Not a Collatz theorem.

### F. New mathematical structure

Reusable: finite vs parameterized census, then generic domain
certificates (maximal divisibility vs mere divisibility). Syracuse:
engine rediscovery of a **KNOWN** clearing identity. Modular/spectral
remain inapplicable in the same planner pass (no `AffineSystem`
injection). Algebraic `EXACT` on the relation is not silently a Collatz
theorem.

### G. Counterexamples

See Counterexamples above. Trap B is the domain-internal failure mode:
divisibility holds for several labels.

### H. Lean

`hiddenCongruenceA_mod0/1/2`. Generic
`mul_pow_eq_iff_padicValInt`. Syracuse `syracuseS_one` /
`acceleratedT_mul` unchanged. The census is not retagged
`EXACT — LEAN VERIFIED`. The relation certificate may cite the generic
lemma; that is KNOWN arithmetic, not a map theorem on \(\mathbb{Z}\).

### I. Prior art

| Kind | Item |
|------|------|
| known theorem | residue-wise affine maps; `acceleratedT_mul`; padic valuation iff |
| computationally verified range | census windows; Syracuse odd samples in \([-48,48]\) plus orbit |
| heuristic | none claimed |
| engine rediscovery | \(2^k S(n)=3n+1\) and its maximal domain from I/O; synthetics A–F |
| new formalization | Lean packaging of synthetic A and the generic valuation iff |
| potentially new result | none claimed |

### J. ComplexityProfile

Unchanged. Census and domain metrics on evidence: `branch_count`,
`coverage`, `coefficient_box`, `k_max`, `census_kind`, `predicate_count`,
`queries`, `overlap`.

### K. Final research decision

```text
CONTINUE
```

Engine decision on Syracuse after census plus domain certification.
Branch mapping: `PARK`. The arithmetic domain of the reconstructed
relation is certified generically; globality of the map on \(\mathbb{Z}\)
is not. Same-run modular/cycle attacks stay inapplicable.

## Open questions

Does a certified arithmetic domain plus a reconstructed family yield any
further generic certificate that is not already KNOWN clearing, still
without map-specific hints and without claiming convergence?

## Decision

`PARK`. The generic census and domain layer recover hidden finite
branches, parameterized \(b^k\) families, and exact-vs-necessary
predicates from I/O, including a Syracuse family already **KNOWN** as
`acceleratedT_mul`. That moved the old engine boundary. It does not
prove Collatz, does not certify the map on all of \(\mathbb{Z}\), and
does not justify reopening `research.collatz`. Do not auto-continue.

Best next question: is there a generic certificate beyond KNOWN
clearing that still does not require map-specific hints?

The Syracuse end-to-end rerun (2026-08-25) answered that for the
arithmetic relation: yes, via maximal divisibility. Control-word
composition (same day) consumes that certificate generically; see
[control_word_composition.md](control_word_composition.md). Remaining
work is map-agnostic obstruction, not a Collatz solver.

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE`. The value is a reusable
attack and a narrower engine boundary, not a new number-theoretic
theorem.
