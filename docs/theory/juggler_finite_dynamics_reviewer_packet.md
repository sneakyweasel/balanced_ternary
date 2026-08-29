# Juggler finite-dynamics reviewer packet

Author: Philippe Cochin. Date: 29 August 2026.
Status: publication draft, not submitted.

Send this page with the
[math note](juggler_finite_dynamics_note.md).
The note is written to be self-contained. This page is a claim map, not
required reading for the proofs.

**Primary review question.** Are the power-envelope, global-defect, and
cycle arguments correct at their stated quantifiers; are the Section-5
discrepancy proofs sound — the depth-1–4 estimates (exponents \(5/6\)
to \(23/24\)), the kernel theorem (Theorem 5.11, double Weyl
differencing over the carry-branch decomposition, \(\delta=1/72\)),
the depth-4 completion (Theorem 5.13), and the contracting splits at
lengths five, seven, and eight (Theorems 5.14–5.16); and are the
secondary densities (\(3/4\) at two steps, \(13/16\) at four, \(7/8\)
at five, \(57/64\) at seven, \(29/32\) at eight) kept distinct from
existential descent and \(\operatorname{ReachesOne}\)?

No termination theorem is claimed. The level-3 kernel bound
(Conjecture 6.3) and the pure amplitude-product model (Conjecture
6.5) are open, and the note says so; the shift-average theorem
(Theorem 6.4) is proved.

Large language models were used extensively in drafting. They are not
authors. Lean theorems and named computations certify the exact-arithmetic
claims. The analytic estimates of Sections 5 and 6 and Proposition 6.1
are human proofs; only their exact floor reductions are in Lean
(`GapCells.lean`, including the double-gap identity
`seq_floor_gap_second`).

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
census: no nontrivial cycle has length at most six. As secondary
corollaries, an exact-linearization discrepancy calculus with a kernel
theorem for the level-2 floor defect proves **every** itinerary word
class of depth at most four equidistributed with power savings, plus
the contracting words of lengths five, seven, and eight, so the uniform
certificate classes have densities \(3/4\) (two steps), \(13/16\)
(four), \(7/8\) (five), \(57/64\) (seven), and \(29/32\) (eight); all-depth
equidistribution would imply density-one finite descent
(Proposition 6.1), with the base cases \(d\le4\) now unconditional,
and the precise remaining obstacle is the level-3 kernel of
Conjecture 6.3, whose shifted model provably cancels (Theorem 6.4)
and whose deterministic crystal is Conjecture 6.5.

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
| Parity bridge, gap-cell, and double-gap floor identities (Lemmas 5.3(ii), 5.10(ii)) | **EXACT — LEAN VERIFIED** | `GapCells.lean`; exact reductions only, no analytic content |
| Nested parity discrepancy \(N^{23/24+\varepsilon}\) (Theorem 5.4) | **EXACT — HUMAN PROOF** | depth 2; exponent deliberately unoptimized |
| OE-branch third letter \(N^{7/8+\varepsilon}\) (Proposition 5.5) | **EXACT — HUMAN PROOF** | completes depth 3 |
| Triple parity discrepancy \(N^{23/24+\varepsilon}\) (Theorem 5.7) | **EXACT — HUMAN PROOF** | OOE\(*\) depth-4 words |
| OE\(**\) splits \(N^{7/8+\varepsilon}\), \(N^{13/16+\varepsilon}\) (Theorem 5.8) | **EXACT — HUMAN PROOF** | depth 4 except OOO\(*\) |
| Certified-descent density \(13/16\) (Corollary 5.9) | **EXACT — HUMAN PROOF** | uniform four-step class; ceiling of the one-growing-layer method |
| Kernel cancellation \(K_c(P)\ll P^{1-1/72+\varepsilon}\) (Theorem 5.11, Corollary 5.12) | **EXACT — HUMAN PROOF** | \(W\)-shaped families \(\alpha\le9/8\), \(k\le P^{1/24}\); adversarially reviewed |
| OOO\(*\) splits; depth 4 complete (Theorem 5.13) | **EXACT — HUMAN PROOF** | all sixteen depth-4 classes with power savings |
| Length-5 and length-7 contracting splits (Theorems 5.14–5.15) | **EXACT — HUMAN PROOF** | exponents \(1-1/72\) and \(43/48\) |
| Length-8 engine quartet (Theorem 5.16) | **EXACT — HUMAN PROOF** | all-subcritical chains; exponent \(1-1/48\), unoptimized |
| Certified-descent densities \(7/8\), \(57/64\), \(29/32\) (Corollary 5.17) | **EXACT — HUMAN PROOF** | uniform five-, seven-, and eight-step classes |
| Equidistribution \(\Rightarrow\) density-one descent (Proposition 6.1) | **EXACT — HUMAN PROOF** | unconditional implication; hypothesis now a theorem for \(d\le4\), open beyond |
| Level-3 kernel reformulation (Lemma 6.2) | **EXACT — HUMAN PROOF** | exact Taylor identity; validated in scaled integers |
| Level-3 kernel cancellation \(K_3(P)\ll P^{1-\delta}\) (Conjecture 6.3) | **CONJECTURE** | not claimed; square-root cancellation observed in exact probes |
| Shift-averaged square-root cancellation (Theorem 6.4) | **EXACT — HUMAN PROOF** | almost-every-shift statement; no claim at \(\lambda=0\) |
| Pure amplitude-product model (Conjecture 6.5) | **CONJECTURE** | not claimed; Exp(1) censuses at \(P=10^6\)–\(10^{10}\) |

## Quantifier checks

1. `FiniteProgress` is `DescentCertificate`: four constructors, one
   predicate (image \(<n\) or image \(1\)). Theorems 4.1–4.2 isolate a
   uniform short subclass. They do not say that odd-to-odd starts lack
   descent.
2. Corollaries 5.2, 5.9, and 5.17 are densities of uniform
   subclasses (\(3/4\) at two steps, \(13/16\) at four, \(7/8\) at
   five, \(57/64\) at seven, \(29/32\) at eight). None is a density
   of `FiniteProgress` nor of `ReachesOne`.
3. Terras–Everett prove almost-all Collatz stopping times. The note does
   not prove the Juggler analogue; Proposition 6.1 is an unconditional
   *implication* from all-depth equidistribution, whose hypothesis is
   a theorem for \(d\le4\) and open beyond (first open case: the
   depth-5 \(OOOO*\) split, Conjecture 6.3).
4. `power_bound_contracts` requires a realized contracting word.
5. Cycle restrictions do not exclude all cycles. Theorem 3.3 is a
   census for lengths at most six only; cycles of length seven or more
   remain possible as far as the note proves.
6. The `native_decide` boundary checks cover both `Fin 256` itinerary
   tables and the finite inequality \(257^{64}<2\cdot256^{64}\).

## What the paper does not claim

- Every positive integer reaches \(1\).
- Three-quarters (or \(13/16\), \(7/8\), \(57/64\), \(29/32\)) of
  starts reach \(1\).
- Those densities as *complete* certificate inventories: they count
  uniform classes.
- A Collatz theorem, or a transfer of Terras's theorem to \(J\).
- Density-one finite descent (Proposition 6.1 is conditional on
  all-depth equidistribution; only \(d\le4\) is proved).
- The level-3 kernel bound \(K_3(P)\ll P^{1-\delta}\)
  (Conjecture 6.3 is open), or any bound on the pure
  amplitude-product model at the deterministic shift
  (Conjecture 6.5 is open; Theorem 6.4 is almost-every-shift only).
- Every trajectory meets a contracting word.
- Every nontrivial cycle is impossible.
- The Juggler map is irreducible or has no finite-state model.
- The \(N^{5/6}\) bound controls orbits or arbitrary image sets.

## Suggested falsifiers

Reject or revise if:

1. a Lean theorem is quoted with stronger quantifiers than its statement;
2. the \(3/4\) or \(13/16\) figure is called a Terras theorem or a
   `ReachesOne` density;
3. Theorem 4.2 is read as “odd-to-odd starts have no descent”;
4. any analytic estimate of Sections 5–6 (or Proposition 6.1) is
   described as Lean-certified;
5. the census of Theorem 3.3 is read beyond length six, or an
   exclusion of cycles of length seven or more is attributed to the
   note;
6. the discrepancy proofs replace a floor by a single exponential, or
   an exact linearization (Lemma 5.3(i), Lemma 5.6, Lemma 5.10,
   Lemma 6.2) is quoted without its one-signed remainder bounds;
7. an interval bound is applied to a sparse image set without transfer;
8. Proposition 4.4 is promoted from exact finite census to an infinite
   theorem;
9. Proposition 6.1 is quoted without its equidistribution hypothesis,
   or Conjecture 6.3 or 6.5 is cited as a theorem;
10. Theorem 6.4 is quoted as a bound at the deterministic shift
    \(\lambda=0\), or the \(OOOO*\) split is claimed as proved at
    depth 5.

## Verification

Repository: [https://github.com/sneakyweasel/balanced_ternary/](https://github.com/sneakyweasel/balanced_ternary/).

```text
pip install -e ".[dev]"
python tools/render_theorem_ledger.py --check
python -m pytest tests/unit/test_theorem_ledger.py
python -m pytest tests/research/juggler_sequence/test_oo_descent_density.py
python -m pytest tests/research/juggler_sequence/test_progress_coverage.py
python -m pytest tests/research/juggler_sequence/test_odd_image_discrepancy.py
python -m pytest tests/research/juggler_sequence/test_two_step_parity.py
python -m pytest tests/research/juggler_sequence/test_cycle_leftover_words.py
python -m pytest tests/research/juggler_sequence/test_layer_architecture.py
```

From `formal/`: `lake build Problems.JugglerPaper`.
The laboratory barrel `Problems.Juggler` is not the review object.
