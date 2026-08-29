# Juggler reviewer packet (two manuscripts)

Author: Philippe Cochin. Date: 29 August 2026.
Status: Paper A is a submission candidate; Paper B is a working draft.

The former single note has been split into two manuscripts:

- **Paper A** —
  [juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md):
  *Power envelopes, exact defects, and cycle restrictions for the
  Juggler map.* Exact word calculus, defect identity, inverse cells,
  the small-cycle census (no nontrivial cycle of length at most six),
  and the uniform one- and two-step certificates. Everything is
  Lean-backed except the horizon-20 census (exact Python integers).
  No density result is stated.
- **Paper B** —
  [juggler_parity_discrepancy_note.md](juggler_parity_discrepancy_note.md):
  *Parity equidistribution of nested floor powers, with descent
  applications to the Juggler map.* The exact-linearization
  discrepancy calculus, the kernel theorem, depth-4 completeness, the
  contracting words of lengths five, seven, and eight, the
  certified-descent densities, and the level-3 frontier. Human
  proofs; only the exact floor identities beneath them are in Lean.

Each paper is written to be self-contained. This page is a claim map,
not required reading for the proofs.

**Primary review questions.** For Paper A: are the power-envelope,
global-defect, and cycle arguments correct at their stated
quantifiers? For Paper B: are the depth-1–4 estimates (exponents
\(5/6\) to \(23/24\)) sound; is the kernel theorem (Theorem 5.3,
double Weyl differencing over the carry-branch decomposition of
Lemma 5.1, with the mixed-piece Lemma 5.2, \(\delta=1/72\)) a
complete proof a stranger can check; are the applications (Theorems
6.1–6.4) correctly reduced to it; and are the densities (Corollaries
4.2, 4.9, 6.5) kept distinct from existential descent and
\(\operatorname{ReachesOne}\)?

No termination theorem is claimed anywhere. The level-3 kernel bound
(Paper B, Conjecture 7.3) and the pure amplitude-product model
(Conjecture 7.5) are open, and the paper says so; the shift-average
theorem (Theorem 7.4) is proved.

Large language models were used extensively in drafting. They are not
authors. Lean theorems and named computations certify the
exact-arithmetic claims of Paper A and the floor identities cited by
Paper B; every analytic estimate of Paper B is a human proof.

## What to read

| File | Role |
|---|---|
| [juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md) | Paper A (review object 1) |
| [juggler_parity_discrepancy_note.md](juggler_parity_discrepancy_note.md) | Paper B (review object 2) |
| this page | claim and falsifier map |
| [juggler_finite_dynamics_formalization.md](juggler_finite_dynamics_formalization.md) | Lean names, optional |
| `formal/Problems/JugglerPaper.lean` | paper Lean barrel (`lake build Problems.JugglerPaper`) |

## Theses

**Paper A.** Every realized finite Juggler word obeys a power
envelope, and its local floor losses assemble into an exact
compositional global defect with rigid zero cases. Inverse cells give
cycle restrictions and a small-cycle census: no nontrivial cycle has
length at most six. Even and odd-to-even starts carry uniform short
certificates; the unresolved starts are exactly the odd-to-odd class.

**Paper B.** An exact-linearization discrepancy calculus with a
kernel theorem for the level-2 floor defect proves **every**
itinerary word class of depth at most four equidistributed with power
savings, plus the contracting words of lengths five, seven, and
eight, so the uniform certificate classes have densities \(3/4\)
(two steps), \(13/16\) (four), \(7/8\) (five), \(57/64\) (seven), and
\(29/32\) (eight); all-depth equidistribution would imply density-one
finite descent (Proposition 7.1), with the base cases \(d\le4\) now
unconditional, and the precise remaining obstacle is the level-3
kernel of Conjecture 7.3, whose shifted model provably cancels
(Theorem 7.4) and whose deterministic crystal is Conjecture 7.5.

## Claim map — Paper A

| Claim | Evidence | Scope |
|---|---|---|
| Power envelope and exponent-gap contraction | **EXACT — LEAN VERIFIED** | conditional on a realized word |
| Global defect identity, vanishing, and composition | **EXACT — LEAN VERIFIED** | weighted lift, not an additive sum; not a uniform tax |
| Odd inverse cells have at most one integer | **EXACT — LEAN VERIFIED** | one-step fibers |
| Nontrivial cycle words are formally expanding; min-to-even prefixes are superquadratic | **EXACT — LEAN VERIFIED** | necessary condition; not an exclusion of all cycles |
| Length-six orientations \(OOOEOE\) and \(OOOOEE\) (Lemma 3.2) | **EXACT — LEAN VERIFIED** | the key lemma of the census |
| Small-cycle census: no cycle word of length \(\le6\) (Theorem 3.3) | **EXACT — LEAN VERIFIED** | lengths \(\le6\) only; length \(\ge7\) open |
| Cycle surplus \(\Delta_w(n)=n^{3^{\#O}}-n^{2^{\lvert w\rvert}}\) (Corollary 2.7); per-step slack bound \(x^e<(J(x)+1)^2\) | **EXACT — LEAN VERIFIED** | no uniform per-step tax exists |
| Four-block expanding chain \(1999\to\cdots\to887471\) (Section 5) | **EXACT — LEAN VERIFIED** | one certified hard path; not a growth theorem |
| Even and odd-to-even starts have uniform short certificates | **EXACT — LEAN VERIFIED** | not all `FiniteProgress` |
| \(\neg\mathrm{FP}\Rightarrow\) odd-to-odd | **EXACT — LEAN VERIFIED** | one direction only |
| \(\{1,\ldots,11\}\) and even residuals \(<144\) reach \(1\) | **EXACT — LEAN VERIFIED** | finite landing class |
| Proposition 4.4 horizon-\(20\) first-return census | **COMPUTATIONALLY VERIFIED** | exact Python integers, zero unresolved cases; not Lean or almost-all |

## Claim map — Paper B

| Claim | Evidence | Scope |
|---|---|---|
| Parity bridge, gap-cell, and double-gap floor identities (Lemmas 3.2, 4.3(ii), 5.1(ii)) | **EXACT — LEAN VERIFIED** | `GapCells.lean`; exact reductions only, no analytic content |
| Branch-consistency identity (Lemma 3.6) | **EXACT — HUMAN PROOF** | exact indicator algebra; replaces any sampled verification |
| \(\lvert S_O(N)\rvert\ll N^{5/6}\) (Theorem 4.1) | **EXACT — HUMAN PROOF** | classical van der Corput; included for completeness |
| \(\lvert\mathrm{OO}(N)-N/4\rvert\ll N^{5/6}\) (Corollary 4.2) | **EXACT — HUMAN PROOF** | short-certificate class density \(3/4\) |
| Nested parity discrepancy \(N^{23/24+\varepsilon}\) (Theorem 4.4) | **EXACT — HUMAN PROOF** | depth 2; exponent deliberately unoptimized |
| OE-branch third letter \(N^{7/8+\varepsilon}\) (Proposition 4.5) | **EXACT — HUMAN PROOF** | completes depth 3 |
| Triple parity discrepancy \(N^{23/24+\varepsilon}\) (Theorem 4.7) | **EXACT — HUMAN PROOF** | OOE\(*\) depth-4 words |
| OE\(**\) splits \(N^{7/8+\varepsilon}\), \(N^{13/16+\varepsilon}\) (Theorem 4.8) | **EXACT — HUMAN PROOF** | depth 4 except OOO\(*\) |
| Certified-descent density \(13/16\) (Corollary 4.9) | **EXACT — HUMAN PROOF** | uniform four-step class; ceiling of the one-growing-layer method |
| Mixed-piece bound (Lemma 5.2) | **EXACT — HUMAN PROOF** | targeted third differencing; standalone statement |
| Kernel cancellation \(K_c(P)\ll P^{1-1/72+\varepsilon}\) (Theorem 5.3, Corollary 5.4) | **EXACT — HUMAN PROOF** | \(W\)-shaped families \(\alpha\le9/8\), \(k\le P^{1/24}\) |
| OOO\(*\) splits; depth 4 complete (Theorem 6.1) | **EXACT — HUMAN PROOF** | all sixteen depth-4 classes with power savings |
| Length-5 and length-7 contracting splits (Theorems 6.2–6.3) | **EXACT — HUMAN PROOF** | exponents \(1-1/72\) and \(43/48\) |
| Length-8 engine quartet (Theorem 6.4) | **EXACT — HUMAN PROOF** | all-subcritical chains; exponent \(1-1/48\), unoptimized |
| Certified-descent densities \(7/8\), \(57/64\), \(29/32\) (Corollary 6.5) | **EXACT — HUMAN PROOF** | uniform five-, seven-, and eight-step classes |
| Equidistribution \(\Rightarrow\) density-one descent (Proposition 7.1) | **EXACT — HUMAN PROOF** | unconditional implication; hypothesis a theorem for \(d\le4\), open beyond |
| Level-3 kernel reformulation (Lemma 7.2) | **EXACT — HUMAN PROOF** | exact Taylor identity; validated in scaled integers |
| Level-3 kernel cancellation \(K_3(P)\ll P^{1-\delta}\) (Conjecture 7.3) | **CONJECTURE** | not claimed; square-root cancellation observed in exact probes |
| Shift-averaged square-root cancellation (Theorem 7.4) | **EXACT — HUMAN PROOF** | almost-every-shift statement; no claim at \(\lambda=0\) |
| Pure amplitude-product model (Conjecture 7.5) | **CONJECTURE** | not claimed; Exp(1) censuses at \(P=10^6\)–\(10^{10}\) |

## Quantifier checks

1. `FiniteProgress` is `DescentCertificate`: four constructors, one
   predicate (image \(<n\) or image \(1\)). Paper A Theorems 4.1–4.2
   isolate a uniform short subclass. They do not say that odd-to-odd
   starts lack descent.
2. Paper B Corollaries 4.2, 4.9, and 6.5 are densities of uniform
   subclasses (\(3/4\) at two steps, \(13/16\) at four, \(7/8\) at
   five, \(57/64\) at seven, \(29/32\) at eight). None is a density
   of `FiniteProgress` nor of `ReachesOne`.
3. Terras–Everett prove almost-all Collatz stopping times. Neither
   paper proves the Juggler analogue; Proposition 7.1 is an
   unconditional *implication* from all-depth equidistribution, whose
   hypothesis is a theorem for \(d\le4\) and open beyond (first open
   case: the depth-5 \(OOOO*\) split, Conjecture 7.3).
4. `power_bound_contracts` requires a realized contracting word.
5. Cycle restrictions do not exclude all cycles. Paper A Theorem 3.3
   is a census for lengths at most six only; cycles of length seven
   or more remain possible as far as the papers prove.
6. The `native_decide` boundary checks cover both `Fin 256` itinerary
   tables and the finite inequality \(257^{64}<2\cdot256^{64}\).

## What the papers do not claim

- Every positive integer reaches \(1\).
- Three-quarters (or \(13/16\), \(7/8\), \(57/64\), \(29/32\)) of
  starts reach \(1\).
- Those densities as *complete* certificate inventories: they count
  uniform classes.
- A Collatz theorem, or a transfer of Terras's theorem to \(J\).
- Density-one finite descent (Proposition 7.1 is conditional on
  all-depth equidistribution; only \(d\le4\) is proved).
- The level-3 kernel bound \(K_3(P)\ll P^{1-\delta}\)
  (Conjecture 7.3 is open), or any bound on the pure
  amplitude-product model at the deterministic shift
  (Conjecture 7.5 is open; Theorem 7.4 is almost-every-shift only).
- Every trajectory meets a contracting word.
- Every nontrivial cycle is impossible.
- The Juggler map is irreducible or has no finite-state model.
- The \(N^{5/6}\) bound controls orbits or arbitrary image sets.

## Suggested falsifiers

Reject or revise if:

1. a Lean theorem is quoted with stronger quantifiers than its statement;
2. the \(3/4\) or \(13/16\) figure is called a Terras theorem or a
   `ReachesOne` density;
3. Paper A Theorem 4.2 is read as “odd-to-odd starts have no descent”;
4. any analytic estimate of Paper B is described as Lean-certified;
5. the census of Paper A Theorem 3.3 is read beyond length six, or an
   exclusion of cycles of length seven or more is attributed to either
   paper;
6. a discrepancy proof replaces a floor by a single exponential, or
   an exact linearization (Paper B Lemmas 4.3(i), 4.6, 5.1, 7.2) is
   quoted without its one-signed remainder bounds;
7. an interval bound is applied to a sparse image set without transfer;
8. Proposition 4.4 is promoted from exact finite census to an infinite
   theorem;
9. Proposition 7.1 is quoted without its equidistribution hypothesis,
   or Conjecture 7.3 or 7.5 is cited as a theorem;
10. Theorem 7.4 is quoted as a bound at the deterministic shift
    \(\lambda=0\), or any numerical probe or repository validation is
    treated as a proof step.

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
