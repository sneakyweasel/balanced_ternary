# Juggler finite-dynamics reviewer packet

Author: Philippe Cochin. Date: 28 August 2026.
Status: publication draft, not submitted.

Send this page with the
[math note](juggler_finite_dynamics_note.md).
The note is written to be self-contained. This page is a claim map, not
required reading for the proofs.

**Primary review question.** Are the power-envelope, global-defect, and
cycle arguments correct at their stated quantifiers, and is the secondary
density-\(3/4\) corollary kept distinct from existential descent and
\(\operatorname{ReachesOne}\)?

No termination theorem is claimed.

Large language models were used extensively in drafting. They are not
authors. Lean theorems and named computations certify the exact-arithmetic
claims. Theorem 5.1 is a human proof.

## What to read

| File | Role |
|---|---|
| [juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md) | math note (the review object) |
| this page | claim and falsifier map |
| [juggler_finite_dynamics_formalization.md](juggler_finite_dynamics_formalization.md) | Lean names, optional |
| `formal/Problems/JugglerPaper.lean` | paper Lean barrel (`lake build Problems.JugglerPaper`) |

## Paper thesis

Every realized finite Juggler word obeys a power envelope, and its local
floor losses assemble into an exact compositional global defect with rigid
zero cases. Inverse cells give cycle restrictions and a small-cycle
census: no nontrivial cycle has length at most six. As a secondary
corollary, the uniform one- and two-step certificate class has density
\(3/4\).

## Claim map

| Claim | Evidence | Scope |
|---|---|---|
| Power envelope and exponent-gap contraction | **EXACT — LEAN VERIFIED** | conditional on a realized word |
| Global defect identity, vanishing, and composition | **EXACT — LEAN VERIFIED** | weighted lift, not an additive sum; not a uniform tax |
| Odd inverse cells have at most one integer | **EXACT — LEAN VERIFIED** | one-step fibers |
| Nontrivial cycle words are formally expanding; min-to-even prefixes are superquadratic | **EXACT — LEAN VERIFIED** | necessary condition; not an exclusion of all cycles |
| Length-six orientations \(OOOEOE\) and \(OOOOEE\) (Lemma 3.2) | **EXACT — LEAN VERIFIED** | the key lemma of the census |
| Small-cycle census: no cycle word of length \(\le6\) (Theorem 3.3) | **EXACT — LEAN VERIFIED** | lengths \(\le6\) only; length \(\ge7\) open |
| Cycle surplus \(\Delta_w(n)=n^{3^{\#O}}-n^{2^{\lvert w\rvert}}\) (Corollary 2.7); per-step slack bound \(x^e<(J(x)+1)^2\) | **EXACT — LEAN VERIFIED** | no uniform per-step tax exists |
| Four-block expanding chain \(1999\to\cdots\to887471\) (Section 6) | **EXACT — LEAN VERIFIED** | one certified hard path; not a growth theorem |
| Even and odd-to-even starts have uniform short certificates | **EXACT — LEAN VERIFIED** | not all `FiniteProgress` |
| \(\neg\mathrm{FP}\Rightarrow\) odd-to-odd | **EXACT — LEAN VERIFIED** | one direction only |
| \(\{1,\ldots,11\}\) and even residuals \(<144\) reach \(1\) | **EXACT — LEAN VERIFIED** | finite landing class |
| Proposition 4.4 horizon-\(20\) first-return census | **COMPUTATIONALLY VERIFIED** | exact Python integers, zero unresolved cases; not Lean or almost-all |
| \(\lvert S_O(N)\rvert\ll N^{5/6}\) | **EXACT — HUMAN PROOF** | ambient; not Lean |
| \(\lvert\mathrm{OO}(N)-N/4\rvert\ll N^{5/6}\) | **EXACT — HUMAN PROOF** | short-certificate class density \(3/4\) |

## Quantifier checks

1. `FiniteProgress` is `DescentCertificate`: four constructors, one
   predicate (image \(<n\) or image \(1\)). Theorems 4.1–4.2 isolate a
   uniform short subclass. They do not say that odd-to-odd starts lack
   descent.
2. Corollary 5.2 is a density of that uniform subclass. It is not
   density of `FiniteProgress` and not density of `ReachesOne`.
3. Terras–Everett prove almost-all Collatz stopping times. The note does
   not prove the Juggler analogue on odd-to-odd starts.
4. `power_bound_contracts` requires a realized contracting word.
5. Cycle restrictions do not exclude all cycles. Theorem 3.3 is a
   census for lengths at most six only; cycles of length seven or more
   remain possible as far as the note proves.
6. The `native_decide` boundary checks cover both `Fin 256` itinerary
   tables and the finite inequality \(257^{64}<2\cdot256^{64}\).

## What the paper does not claim

- Every positive integer reaches \(1\).
- Three-quarters of starts reach \(1\).
- Three-quarters of starts have some descent certificate.
- A Collatz theorem, or a transfer of Terras's theorem to \(J\).
- Every trajectory meets a contracting word.
- Every nontrivial cycle is impossible.
- The Juggler map is irreducible or has no finite-state model.
- The \(N^{5/6}\) bound controls orbits or arbitrary image sets.

## Suggested falsifiers

Reject or revise if:

1. a Lean theorem is quoted with stronger quantifiers than its statement;
2. the \(3/4\) figure is called a Terras theorem or a `ReachesOne` density;
3. Theorem 4.2 is read as “odd-to-odd starts have no descent”;
4. Theorem 5.1 is described as Lean-certified;
5. the census of Theorem 3.3 is read beyond length six, or an
   exclusion of cycles of length seven or more is attributed to the
   note;
6. the discrepancy proof replaces the floor by a single exponential;
7. an interval bound is applied to a sparse image set without transfer;
8. Proposition 4.4 is promoted from exact finite census to an infinite theorem.

## Verification

Repository: [https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).

```text
pip install -e ".[dev]"
python tools/render_theorem_ledger.py --check
python -m pytest tests/unit/test_theorem_ledger.py
python -m pytest tests/research/juggler_sequence/test_oo_descent_density.py
python -m pytest tests/research/juggler_sequence/test_progress_coverage.py
python -m pytest tests/research/juggler_sequence/test_odd_image_discrepancy.py
python -m pytest tests/research/juggler_sequence/test_cycle_leftover_words.py
python -m pytest tests/research/juggler_sequence/test_layer_architecture.py
```

From `formal/`: `lake build Problems.JugglerPaper`.
The laboratory barrel `Problems.Juggler` is not the review object.
