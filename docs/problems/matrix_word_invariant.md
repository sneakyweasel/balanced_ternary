# Matrix-word recursive invariants

Status: **EXPLORATORY**

Final planned engine-capability experiment before freezing the attack
architecture. It does **not** reopen Collatz, add `EuclideanControl`,
or treat Euclidean identities as new mathematics. Hidden synthetics
live in `research_engine.benchmarks.hidden_matrix_invariants`.

## Problem

Can Research Engine v2 discover a recursive arithmetic invariant of
composed matrix words that proves

\[
(M(\mathbf u)-I)\mathbf x=-\mathbf c(\mathbf u)
\]

has no integer solution for an infinite control class, even when
entrywise magnitude \(|M-I|\le|\mathbf c|\) is `INAPPLICABLE`?

## Exact statement

Given a certified `vector_affine` family or finite alphabet, does
`matrix_word_invariant`

1. expose prefix state \((M_i,\mathbf c_i)\);
2. discover a predicate \(P\) with \(P_i\Rightarrow P_{i+1}\) on a
   control class;
3. imply \(\mathbf c\notin\operatorname{im}_{\mathbb Z}(M-I)\);
4. distinguish `CLASS IMPOSSIBLE EXCEPT E` from all-words claims;
5. refute false invariants;
6. return `UNKNOWN / NO OBSTRUCTION` on a realizable family;
7. consume Euclidean, parity-shear, and an unrelated lattice walk
   without target-specific code?

Magnitude domination is not a success criterion.

## Current literature

- Integer solvability of \(Ax=b\): Smith/invariant factors, gcd of
  minors. **KNOWN**.
- Scalar recursive remainder invariants:
  [control_obstruction.md](control_obstruction.md). **PROJECT-SPECIFIC**
  engine capability; mathematics **KNOWN**.
- Vector affine census: [vector_affine.md](vector_affine.md).
- Euclidean algorithm / continuants: Knuth; Vallée 2006. **KNOWN**.

## Branch budget

```text
Mathematical target     Recursive matrix-word invariant that eliminates
                        an infinite non-magnitude vector control class.
Novelty hypothesis      Smallest image-lattice / gcd / kernel predicate
                        on (M_i, c_i) transfers scalar remainder
                        recursion to matrix words.
Falsifier               Magnitude-only success; Euclidean-specific code;
                        hallucinated impossibility; ALL WORDS when
                        exceptions exist; scalar regression.
Existing machinery      vector_affine composition/cycle; scalar
                        RemainderInvariant; AffineSystem arithmetic.
Maximum Phase-0 scope   One attack + synthetics A–G + Euclid / parity
                        shear / lattice walk + Lean; then freeze.
Promotion criterion     Infinite non-magnitude class, discovered,
                        recursive, Lean-certified, reused.
Stop criterion          Theorem-prover search; Euclid solver;
                        another attack “in case”.
```

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Image kernel: a row of \(M-I\) vanishes while the matching
  coordinate of \(\mathbf c\) does not. **EXACT — LEAN VERIFIED**
  (`kernel_row_cycle_impossible`). **KNOWN**.
- Entry-gcd / first invariant factor: \(d=\gcd(M-I)\) must divide
  \(\mathbf c\). **EXACT — LEAN VERIFIED**
  (`entry_gcd_divides_translation`). **KNOWN**.
- Recursive shear offset: \(c_y\leftarrow c_y+1\). **EXACT — LEAN
  VERIFIED** (`shear_offset_y_succ`, `shear_word_class_impossible`).
- Magnitude \(|M-I|>|\mathbf c|\): recorded `USED` or
  `INAPPLICABLE`. Success requires `INAPPLICABLE`.

## Experiments

- `tests/research_engine/core/test_matrix_word_invariant.py`
- Synthetics A–G in `hidden_matrix_invariants`
- Consumers: `euclidean_spec`, `HiddenParityShearSpec`,
  `HiddenLatticeWalkSpec`

## Conjectures

None opened.

## Counterexamples

- All-parameter residue candidate on the false-invariant trap:
  **REFUTED** by a realizable odd-\(k\) probe.
- “All words impossible” on the exception family: **REFUTED**; finite
  realizable words exist (\(k=\pm 1\) length one).
- Realizable zero-offset shear family: no class obstruction
  (**UNKNOWN / NO OBSTRUCTION**).

## Formalization

`formal/Problems/Engine/MatrixWord.lean`:

- GENERIC: `recursive_matrix_word_step`,
  `kernel_row_cycle_impossible`, `entry_gcd_divides_translation`,
  `entry_gcd_cycle_impossible`, `shear_offset_y_succ`,
  `shear_word_class_impossible`
- No Euclidean specialization. No `sorry`. No ledger row.

## Results

### A. Capability

Attack `matrix_word_invariant` consumes `vector_affine`. Object
`MatrixWordInvariant` stores predicate, recursive update
\(M'=A_u M\), \(\mathbf c'=A_u\mathbf c+\mathbf b\), evidence status,
magnitude label, and class. Obstruction scopes reuse
`WORD|CLASS|SYMBOLIC_CLASS|RECURSIVE_INVARIANT`. Fingerprint field
`latent_control_obstruction` is reused (no
`vector_control_obstruction`). Capability
`matrix_word_recursive_invariant`. `ComplexityProfile` unchanged.

### B. Synthetic results

| Id | Hidden structure | Discovered | Status | Magnitude |
|----|------------------|------------|--------|-----------|
| A modular lattice | shear \(A_k\) + \((0,1)\) | image kernel, \(c_y\neq 0\) | `RECURSIVE_INVARIANT` `LEAN_CERTIFIED` | `INAPPLICABLE` |
| B gcd family | even-\(k\) shear + \((1,0)\) | entry-gcd on odd-length class | `PROVED` class | `INAPPLICABLE` |
| C smith-style | diagonal \((2,2+k)\) | det/preimage factor | `PROVED` class | `INAPPLICABLE` |
| D recursive shear | shear + \((0,1)\) | kernel recurrence across lengths | `RECURSIVE_INVARIANT` | `INAPPLICABLE` |
| E exceptions | shear + \((1,0)\), \(k=v_2\) | class except finite realizable words | `PROVED` except E | `INAPPLICABLE` |
| F false trap | even \(k\) in-window, odd outside | all-\(k\) candidate | `REFUTED` | `INAPPLICABLE` |
| G realizable | shear, \(\mathbf b=0\) | none | `UNKNOWN` / `NO OBSTRUCTION` | `INAPPLICABLE` |

### C. Class obstruction

Infinite non-magnitude class: every nonempty shear word with vertical
offset \((0,1)\) (synthetics A, D). Lean
`shear_word_class_impossible`. Magnitude `INAPPLICABLE` (e.g. \(k=0\)
gives \(M-I=0\)).

### D. Euclidean consumer

Same generic attack. Recovered family has \(\mathbf b=\mathbf 0\), so
\(\mathbf c=\mathbf 0\) and \(\mathbf x=\mathbf 0\) solves the cycle
equation. Result: `UNKNOWN` / no class obstruction. Transfer
measurement, not a Euclidean theorem. Mathematics **KNOWN**.

### E. Parity-shear consumer

Finite alphabet, zero offsets. Probed words yield `NO OBSTRUCTION`.
Attack source contains no remainder arithmetic.

### F. Unrelated vector target

`HiddenLatticeWalkSpec`: \((x,y)\mapsto(x+2y+1,2x+y)\). Finite
certified affine branch; same invariant attack emits a gcd/image
certificate. Not Euclidean in disguise.

### G. Lean

See Formalization. GENERIC only.

### H. ResearchLoop

`latent_control_obstruction` may be `RECURSIVE_INVARIANT` from
`matrix_word_invariant`. Coverage
`matrix_word_recursive_invariant`. Decision wording: “recursive
control invariant”. No new fingerprint dimension.

### I. ComplexityProfile

Unchanged schema. Word lengths, kinds, and magnitude live on
certificate evidence.

### J. Prior art

| Class | Item |
|-------|------|
| KNOWN MATHEMATICS | \(Ax=b\) over \(\mathbb Z\); shear composition; Euclidean algorithm |
| ENGINE REDISCOVERY | kernel/gcd predicates on recovered words |
| NEW GENERIC ENGINE CAPABILITY | `matrix_word_invariant` |
| NEW FORMALIZATION | `Problems.Engine.MatrixWord` |
| POTENTIALLY NEW MATHEMATICS | none claimed |

### K. Architecture freeze decision

```text
ATTACK ARCHITECTURE FROZEN
```

No further attack is added because a future target might benefit.
The next extension, if any, must be forced by a real mathematical
failure of the existing engine.

### L. Final research decision

Engine: `CONTINUE` on non-magnitude recursive synthetics.

Dossier:

```text
PARK
```

Capability succeeds; mathematics is **KNOWN**. Freeze the attack
stack. Do not open an Euclidean or Collatz matrix program.

## Open questions

None at the engine layer. The laboratory’s next question is a real
mathematical target consumed by the frozen engine.

## Decision

`PARK`. Matrix-word recursive invariants exist, are counterexample-first,
and eliminate infinite non-magnitude classes. Identities are **KNOWN**
integer-linear algebra. Attack architecture frozen.

Best next question: which real mathematical target should the frozen
Research Engine v2 consume next?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as number theory.
Value is the last generic obstruction layer before a real campaign.
