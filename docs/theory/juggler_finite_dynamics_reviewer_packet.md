# Juggler finite-dynamics reviewer packet

Author: Philippe Cochin. Date: 28 August 2026.
Status: publication draft, not submitted.

Send this page with the
[math note](juggler_finite_dynamics_note.md).
The note is written to be self-contained. This page is a claim map, not
required reading for the proofs.

**Primary review question.** Does the note correctly separate the uniform
one- and two-step descent certificates from existential descent, and does
it avoid presenting the density-\(3/4\) short-certificate class as a
Terras theorem or a \(\operatorname{ReachesOne}\) density?

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

## Paper thesis

Every realized finite Juggler word obeys a power envelope; a negative
exponent gap forces contraction. Every even start and every odd-to-even
start has a uniform short descent certificate. The complementary
odd-to-odd class has density \(1/4\) by a classical discrepancy bound on
the ambient odd-input sign sum. That density is not Terras's almost-all
stopping-time theorem, and it is not a density of arrival at \(1\).

## Claim map

| Claim | Evidence | Scope |
|---|---|---|
| Power envelope and exponent-gap contraction | **EXACT — LEAN VERIFIED** | conditional on a realized word |
| Global defect identity | **EXACT — LEAN VERIFIED** | slack, not a uniform tax |
| Odd inverse cells have at most one integer | **EXACT — LEAN VERIFIED** | one-step fibers |
| Nontrivial cycle words are formally expanding | **EXACT — LEAN VERIFIED** | necessary condition; not an exclusion of all cycles |
| Length-six orientations \(OOOEOE\) and \(OOOOEE\) | **EXACT — LEAN VERIFIED** | these two words only; not a length-six census |
| Even and odd-to-even starts have uniform short certificates | **EXACT — LEAN VERIFIED** | not all `FiniteProgress` |
| \(\neg\mathrm{FP}\Rightarrow\) odd-to-odd | **EXACT — LEAN VERIFIED** | one direction only |
| \(\{1,\ldots,11\}\) and even residuals \(<144\) reach \(1\) | **EXACT — LEAN VERIFIED** | finite landing class |
| Every \(n\le4000\) reaches \(1\) | **COMPUTATIONALLY VERIFIED** | window only |
| Horizon-\(20\) first-return rates | **OBSERVATION** | not Lean, not almost-all |
| \(\lvert S_O(N)\rvert\ll N^{5/6}\) | **EXACT — HUMAN PROOF** | ambient; not Lean |
| \(\lvert\mathrm{OO}(N)-N/4\rvert\ll N^{5/6}\) | **EXACT — HUMAN PROOF** | short-certificate class density \(3/4\) |
| Ambient bound transfers to Juggler images | **REFUTED** | tested form |

## Quantifier checks

1. `FiniteProgress` is existential over all finite words. Theorems 4.1–4.2
   isolate a uniform short subclass. They do not say that odd-to-odd
   starts lack descent.
2. Corollary 5.2 is a density of that uniform subclass. It is not
   density of `FiniteProgress` and not density of `ReachesOne`.
3. Terras–Everett prove almost-all Collatz stopping times. The note does
   not prove the Juggler analogue on odd-to-odd starts.
4. `power_bound_contracts` requires a realized contracting word.
5. Cycle restrictions do not exclude all cycles. The two leftover
   length-six orientations are excluded; that is not a length-six census.
6. Atlas absence, if mentioned, is `NOT OBSERVED WITHIN SEARCH BOUND`.

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
5. either leftover orientation is described as still open, or all
   length-six cycle words are claimed excluded;
6. the discrepancy proof replaces the floor by a single exponential;
7. an interval bound is applied to a sparse image set without transfer;
8. Proposition 4.5 is promoted from observation to theorem.

## Verification

Repository: [https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).

```text
pip install -e ".[dev]"
python tools/render_theorem_ledger.py --check
python -m pytest tests/unit/test_theorem_ledger.py
python -m pytest tests/research/juggler_sequence/test_progress_coverage.py
python -m pytest tests/research/juggler_sequence/test_odd_image_discrepancy.py
python -m pytest tests/research/juggler_sequence/test_cycle_leftover_words.py
```

From `formal/`: `lake build`.
