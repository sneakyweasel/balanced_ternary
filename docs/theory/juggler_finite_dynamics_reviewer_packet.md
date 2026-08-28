# Juggler finite-dynamics reviewer packet

Send this page with the
[publication draft](juggler_finite_dynamics_note.md).
The draft and the explicitly linked certificates are the review object; the
full research journal is not required reading.

**Primary review question.** Does the paper correctly separate exact finite
structure from bounded computation, and does its synthesis support the claim
that the named symbolic, state, geometric, inverse, extremal, and statistical
reductions fail to provide a pointwise termination mechanism?

No termination theorem is claimed.

## What to read

| File | Role |
|---|---|
| [juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md) | publication draft |
| this page | claim, scope, and falsifier map |
| [juggler_finite_dynamics_formalization.md](juggler_finite_dynamics_formalization.md) | exact Lean targets |
| [../juggler_branch_ledger.md](../juggler_branch_ledger.md) | curated branch decisions and evidence |
| [../problems/juggler_word_atlas.md](../problems/juggler_word_atlas.md) | Atlas contract and bounded census |

Lean façade:

- `formal/Problems/Juggler.lean`;
- modules under `formal/Problems/Juggler/`.

Computational façade:

- `atlas/`;
- `src/research/juggler_sequence/atlas/`;
- `data/research/juggler/word_atlas/`.

## Paper thesis

The paper develops an exact finite-language semantics for the Juggler map,
certifies its central envelope, defect, cell, residual, and cycle results in
Lean, and pairs that layer with a reproducible CPU/GPU Word Atlas. The combined
apparatus identifies structure that survives exact scrutiny and supplies
certified counterexamples to several natural finite compressions.

The conclusion is qualified:

> No useful pointwise termination mechanism was found among the tested
> symbolic, residual, geometric, inverse, extremal, and statistical families.

This is neither an irreducibility theorem nor a statement about every possible
finite-state or analytic model.

## Evidence classes

The paper uses the repository's seven claim tags:

- `EXACT — HUMAN PROOF`;
- `EXACT — LEAN VERIFIED`;
- `COMPUTATIONALLY VERIFIED`;
- `CONJECTURE`;
- `OBSERVATION`;
- `REFUTED`;
- `REPARAMETERIZATION`.

Atlas phrases such as `GPU VERIFIED`, `CPU VERIFIED`, and
`NOT OBSERVED WITHIN SEARCH BOUND` describe validation or search status. They
do not replace the theorem-ledger tags and never turn absence into
non-realizability.

## Claim map

| Claim | Evidence | Novelty/scope | Certificate |
|---|---|---|---|
| `follows n w` is equivalent to the actual length-\(|w|\) itinerary | **EXACT — LEAN VERIFIED** | formal semantic foundation | `follows_iff_word`, `Itinerary.lean` |
| `image n w` is the \(|w|\)-fold iterate and composes under concatenation | **EXACT — LEAN VERIFIED** | formal semantic foundation | `image_eq_iterate`, `image_append` |
| A fixed-word image is monotone on its realizing set | **EXACT — LEAN VERIFIED** | exact surviving structure; no interval claim | `image_monotone_of_follows` |
| Every realized word obeys \(J^{|w|}(n)^{2^{|w|}}\le n^{3^{\#O(w)}}\) | **EXACT — LEAN VERIFIED** | finite-word envelope | `power_bound_word`, `Envelope.lean` |
| \(3^{\#O(w)}<2^{|w|}\) forces \(J^{|w|}(n)<n\), for \(n\ge2\) | **EXACT — LEAN VERIFIED** | conditional contraction, not eventual occurrence | `power_bound_contracts` |
| The global defect gives an exact additive slack identity | **EXACT — LEAN VERIFIED** | exact refinement of the envelope | `global_defect_identity` |
| Even and odd-to-even starts have `FiniteProgress`; any automatically unresolved start is odd-to-odd | **EXACT — LEAN VERIFIED** | exact induction boundary, not universal progress | `even_finiteProgress`, `odd_even_finiteProgress`, `unresolved_is_odd_odd` |
| Odd inverse cells have at most one integer, while even cells are interval fibers | **EXACT — LEAN VERIFIED** | exact inverse-cell asymmetry | `even_cell_iff`, `odd_cell_iff`, `odd_cell_unique` |
| Two `OOE` cylinders can have opposite next parity | **EXACT — LEAN VERIFIED** | counterexample to a tested cylinder quotient | `ooe_cylinder_both_next_parities` |
| Persistent expanding residual blocks can repeat | **REFUTED** | refutes a natural one-block stopping law | `two_block_ooe_365` |
| Every nontrivial cycle word is formally expanding | **EXACT — LEAN VERIFIED** | necessary cycle condition only | `cycle_word_formally_expanding` |
| Cycle extrema obey nested parity, order, and cell constraints | **EXACT — LEAN VERIFIED** | exact partial cycle structure | `cycle_distinguished_order` and supporting lemmas |
| `CycleMin` cannot end in `O`; one prefix-`OOO` equality slice is excluded | **EXACT — LEAN VERIFIED** | reuses exact cells; does not eliminate the two remaining words | `cycleMin_not_end_odd`, `cycleMin_prefix_ooo_even_sqrt_ne` |
| Atlas census through \(k\le20,n\le10^8\) is reproducible and CPU/GPU cross-checked | **COMPUTATIONALLY VERIFIED** | bounded apparatus, not a language theorem | experiment `wa-20260827T200310Z-cuda-k20-n100000000` |
| No extra PE-run grammar was found through factor length \(8\) | **OBSERVATION** | bounded confirmation of the known block grammar | Atlas summary |
| Tested residual and future quotients lose predictive information unless the current integer is retained | **REFUTED** within stated tests | finite-family elimination, not universal irreducibility | residual/future dossiers and witnesses |
| \(S_O(N)=\sum_{n\le N,\ n\ {\rm odd}}(-1)^{\lfloor n^{3/2}\rfloor}\) satisfies \(|S_O(N)|\ll N^{5/6}\) | **EXACT — HUMAN PROOF** | classical discrepancy method on the exact sequence | odd-image discrepancy dossier |
| The ambient discrepancy estimate automatically transfers to Juggler-generated image sets | **REFUTED** | fragmented images and certified finite concentration obstruct the tested transfer | parity-transfer dossier and data |
| Mixed ensembles have negative empirical log-log drift near \(-\tfrac12\log(4/3)\) | **OBSERVATION** | descriptive statistical agreement only | probabilistic records |

## Quantifier checks

The following distinctions are mandatory in review.

1. `follows n w` is an exact predicate; Atlas realization is existential only
   within a configured finite scan.
2. `power_bound_contracts` is conditional on a realized contracting word; no
   theorem says every trajectory reaches one.
3. `reachesOne_of_all_finiteProgress` is conditional on universal finite
   progress; the repository proves automatic coverage only for even and
   odd-to-even starts.
4. `odd_cell_unique` is a one-step inverse statement; it does not make an
   iterated inverse tree finite.
5. Cycle restrictions assume a `CycleWord`; they do not establish the
   existence or nonexistence of all nontrivial cycles.
6. The \(N^{5/6}\) result is an anchored ambient odd-input bound. It is not an
   orbit-frequency theorem.
7. Computational counterexamples refute their stated universal candidate
   laws, while positive censuses remain bounded observations.

## What the paper does not claim

- Every positive integer reaches \(1\).
- Every trajectory encounters a contracting finite word.
- Every nontrivial cycle is impossible.
- `OOOEOE` or `OOOOEE` has been excluded as a cycle word.
- The Juggler map is irreducible, unprovable, random, or computationally
  intractable.
- No finite-state model exists.
- The exact integer is necessary for every possible compression.
- Atlas prefix gaps are forbidden words.
- The \(N^{5/6}\) estimate controls parity along individual orbits or arbitrary
  Juggler-generated sets.
- The probabilistic model proves a tail inequality or termination.

## Suggested falsifiers

A review should reject or revise the package if:

1. a Lean theorem is quoted with stronger quantifiers than its declaration;
2. a computational absence is described as global non-realizability;
3. the Atlas GPU path is said to certify PE directly rather than through the
   exact host post-pass;
4. the global defect identity is presented as a state-independent contraction
   budget;
5. the tested quotient failures are generalized beyond the listed families;
6. either remaining length-six cycle orientation is described as excluded;
7. the discrepancy proof replaces the floor sign by a single exponential
   without the fractional-part identity;
8. an interval discrepancy estimate is applied to a sparse image set without a
   transfer theorem;
9. empirical drift, fitted tails, or model constants are presented as exact
   dynamics;
10. the integrated formal/computational novelty is already present in prior
    work in the same theorem-and-certificate form.

## Verification

From the repository root:

```powershell
python tools/render_theorem_ledger.py --check
python -m pytest tests/unit/test_theorem_ledger.py
python -m pytest tests/research/juggler_sequence/test_word_atlas.py tests/research/juggler_sequence/test_word_atlas_validate.py
python -m pytest tests/research/juggler_sequence/test_global_defect.py tests/research/juggler_sequence/test_preimage_cylinders.py
python -m pytest tests/research/juggler_sequence/test_odd_image_discrepancy.py tests/research/juggler_sequence/test_parity_discrepancy_transfer.py
```

From `formal/`:

```powershell
lake build
```

Native Atlas validation, when the binary is available:

```powershell
juggler-atlas validate
atlas\build\juggler-atlas-tests.exe
```
