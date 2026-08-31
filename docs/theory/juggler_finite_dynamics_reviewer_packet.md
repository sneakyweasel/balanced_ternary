# Juggler reviewer packet (two manuscripts)

Author: Philippe Cochin. Date: 31 August 2026.
Status: Paper A is a submission candidate; Paper B is a working draft.

The former single note has been split into two manuscripts:

- **Paper A** —
  [juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md):
  *Cycle financing and a period lower bound for the Juggler map.*
  The contribution is
  known verification through \(10^6\) plus the new
  Juggler-specific finance inequality, hence \(L\ge 25781\).
  Theorem 3.22 (\(e\ge 4\)) is the Section 3 headline.
  Theorem 4.7 is the supporting run-packing refinement.
  Finance-survivor arithmetic is secondary. Lemma 4.4b is the
  odd-count monotonicity used to evaluate the table at
  \(o_{\min}\). The core lemmas are mechanized in Lean 4;
  selected finite classifications and the descent floor
  (Proposition 1.3) are independently certified computations.
  Leftover \(84\) is a laboratory companion, not a paper
  theorem. Peak/run bounds and the closed return-cost branch
  are not paper claims.
- **Paper B** —
  [juggler_parity_discrepancy_note.md](juggler_parity_discrepancy_note.md):
  *Parity equidistribution of nested floor powers, with descent
  applications to the Juggler map.* The exact-linearization
  discrepancy calculus, the kernel theorem, depth-4 completeness over
  odd starts, the certified-descent density \(13/16\), and the
  level-3 frontier. Human proofs; only the exact floor identities
  beneath them are in Lean. (The former length-5/7/8 contracting
  splits and their densities \(7/8\), \(57/64\), \(29/32\) were
  withdrawn in the Phase-26 referee response and are laboratory
  conjectures, not paper claims.)

Each paper is written to be self-contained. This page is a claim map,
not required reading for the proofs.

**Primary review questions.** For Paper A: are the power-envelope,
census, and finance arguments correct at their stated
quantifiers? (The global-defect identity is Appendix C and is not
an input to Theorem 4.4.) Is Theorem 4.6 scoped as a verified computation,
not a Lean theorem? For Paper B: are the depth-1–4 estimates (exponents
\(5/6\) to \(23/24\)) sound; is the kernel theorem (Theorem 5.3,
double Weyl differencing over the carry-branch decomposition and
master identity of Lemma 5.1, with the level-2 wave Lemma 5.2,
\(\delta=1/96\), and the Step-5b sublevel splitting of Lemma 3.9) a
complete proof a stranger can check; is Theorem 6.1's passenger
inventory (explicit mode ranges, recomputed composites \(405/512\)
and \(8.27\,kh_1h_2\nu^{-5/8}\)) correctly reduced to it; and are the
densities (Corollaries 4.2, 4.9) kept distinct from existential
descent and \(\operatorname{ReachesOne}\)?

No termination theorem is claimed anywhere. The level-3 kernel bound
(Paper B, Conjecture 7.3) and the pure amplitude-product model
(Conjecture 7.5) are open, and the paper says so; the shift-averaged
\(L^2\) bound (Proposition 7.4) is proved, and is an average-only
statement carrying a \(\sqrt{\log L}\) factor in general.

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
envelope. An exact compositional global defect is recorded in
Appendix C; Theorem 4.4 uses only the envelope's nonnegativity.
Inverse-cell geometry classifies minimum-based words with at
most three evens; the family calculations (Appendix D) assemble
to \(e\ge 4\), hence period at least eleven (Theorem 3.22). The
financing inequality at a cycle minimum (Theorem 4.4,
constant \(1\)), with the convenient statewise bound of
Corollary 4.5 and the certified descent floor of
Proposition 1.3, yields \(L\ge 25781\). Theorem 4.6 certifies
that bound with a conservative \(6/5\) majorant; the cutoff is
not an artifact of that majorant.
Finance-survivor lengths through \(10^5\) and their lattice
are supporting material. Short certificates are a remark in
Section 5. Peak count \(p\) is named there as the next
direction; no peak-count theorem is claimed. The same
defect-financing pattern is noted for other piecewise
floor-power maps and is not taken up.

**Paper B.** An exact-linearization discrepancy calculus with a
kernel theorem for the level-2 floor defect proves every *O-rooted*
itinerary word class of depth at most four (the eight length-4 words
over odd starts) equidistributed with power savings, so the uniform
certificate classes have densities \(3/4\) (two steps) and \(13/16\)
(four); all-depth equidistribution would imply density-one finite
descent (Proposition 7.1), with the base cases \(d\le4\) now
unconditional, and the precise remaining obstacle is the level-3
kernel of Conjecture 7.3, whose deterministic model instance is
Conjecture 7.5 (the shift-averaged \(L^2\) bound of Proposition 7.4
says nothing about the deterministic shift).

## Claim map — Paper A

| Claim | Evidence | Scope |
|---|---|---|
| Power envelope and exponent-gap contraction | **EXACT — LEAN VERIFIED** | conditional on a realized word |
| Global defect identity, vanishing, and composition (Appendix C) | **EXACT — LEAN VERIFIED** | weighted lift, not an additive sum; not a uniform tax; not an input to Theorem 4.4 |
| Odd inverse cells have at most one integer (Lemma 3.1) | **EXACT — LEAN VERIFIED** | one-step fibers |
| Nontrivial cycle words are formally expanding; min-to-even prefixes are superquadratic (Theorem 3.2) | **EXACT — LEAN VERIFIED** | necessary condition; not an exclusion of all cycles |
| Coarse lower envelope \(C_v\) (Lemma 3.3) | **EXACT — LEAN VERIFIED** | one-step \(n<4\lfloor\sqrt n\rfloor^2\) and composition; used by Lemma 3.5; Lean `lower_growth_word` |
| Next-square thresholds (Lemma 3.4) | **EXACT — LEAN VERIFIED** | \(OO\) at \(q\ge5\), \(OOO\) at \(q\ge3\), odd inheritance, last-even cell, and \(O^aE\) for \(a\ge3\) |
| Length-six orientations \(OOOEOE\) and \(OOOOEE\) (Lemma 3.5) | **EXACT — LEAN VERIFIED** | the only two leftover even-terminating length-six words; \(n<256\) is a \(254\)-start table, not a census of all words; tail \(n\ge256\) by \(n^{81}>2^{130}(n+1)^{64}\) |
| Small-cycle census: no cycle word of length \(\le6\) (Theorem 3.6) | **EXACT — LEAN VERIFIED** | lengths \(\le6\) only; strengthened by Theorem 3.8 |
| Leftover length-seven orientations \(OOOOEOE\) and \(OOOOOEE\) (Lemma 3.7) | **EXACT — LEAN VERIFIED** | the only two leftover even-terminating length-seven words; \(n<14\) is a \(12\)-start table; tail \(n\ge14\) by \(n^{243}>2^{422}(n+1)^{128}\) |
| Small-cycle census: no cycle word of length \(\le7\) (Theorem 3.8) | **EXACT — LEAN VERIFIED** | lengths \(\le7\) only; strengthened by Theorem 3.22 |
| Trailing even run (Lemma 3.9) | **EXACT — LEAN VERIFIED** | cell identity; \(r=1\) is Lemma 3.4(iv) |
| Two-even leftover families (Theorem 3.12) | **EXACT — LEAN VERIFIED** | \(O^{k-2}EE\) and \(O^{k-3}EOE\) for every \(k\ge6\); not a length-8 census |
| First-even transport (Theorem 3.13) | **EXACT — LEAN VERIFIED** | minimum-based starts only; not a `CycleWord` theorem at a non-minimum start |
| Bunched families \(O^aEEE\), \(O^aEOEE\), \(O^aEOOEE\), \(O^aEOOOEE\), \(O^aEEOE\), \(O^aEOEOE\), and \(O^aEOOEOE\) (Theorems 3.14--3.20) | **EXACT — LEAN VERIFIED** | seven families only; not a length-8 or length-9 census |
| Gapped leftovers as cycle words (Theorem 3.21) | **EXACT — LEAN VERIFIED** | both gapped families; rotation of already-excluded CycleMins; not first-E at a non-minimum start; not a length-8 or length-9 census |
| Canonical run form (Lemma 3.21b); classification (Lemma 3.21a); even-count assembly (Theorem 3.22); period at least eleven (Corollary 3.23) | **EXACT — LEAN VERIFIED** | minimum-based words are \(O^aEO^bEO^cE\); no cycle word with fewer than four evens; expansion corollary, not a length-9 or length-10 word census |
| Cycle surplus \(\Delta_w(n)=n^{3^{\#O}}-n^{2^{\lvert w\rvert}}\) (Corollary 2.7, Appendix C); per-step slack bound \(x^e<(J(x)+1)^2\) | **EXACT — LEAN VERIFIED** | no uniform per-step tax exists; recorded for future work |
| Finance inequality (Theorem 4.4) | **EXACT — LEAN VERIFIED** | `cycleMin_finance`; constant \(1\); conceptual sharp form; not a halt theorem |
| Inv-sum form (Corollary 4.4c) | **EXACT — LEAN VERIFIED** | `cycleMin_finance_inv_sum`; same defects, remainders kept as \(1/x_{i+1}\) |
| Per-length exclusion given a floor (Corollary 4.5) | **EXACT — HUMAN PROOF** | convenient length-only statewise bound; \(n_{\max}\) from the parity charge |
| Verified computation (Theorem 4.6) | **COMPUTATIONALLY VERIFIED** | conservative \(6/5\) certification of Corollary 4.5 at floor \(10^6\); no period \(\le 25780\); \(141\) exceptions through \(10^5\); first length not excluded is \(25781\); the cutoff is not an artifact of \(6/5\) |
| Run-type packing (Theorem 4.7) | **EXACT — HUMAN PROOF** | \(\mathtt{OE}\)-starts lift to \(n^{4/3}\); not Lean |
| Run-type table (Theorem 4.8) | **COMPUTATIONALLY VERIFIED** | \(42\) of the \(141\) die; \(99\) remain; first survivor still \(25781\) |
| Survivor lattice (Proposition 4.9) | **EXACT — LEAN VERIFIED** | unimodular basis and family arithmetic; identification with \(\mathcal E_{\mathrm{run}}\) is Theorem 4.8 |
| Lean leftover \(84\) or \(\ge 85\) | **EXACT — LEAN VERIFIED** | Appendix A companion; formalization lag relative to Theorem 4.6 |
| Four-block expanding chain \(1999\to\cdots\to887471\) (Section 5) | **EXACT — LEAN VERIFIED** | one certified hard path; not a growth theorem |
| Even and odd-to-even starts have uniform short certificates (Section 5) | **EXACT — LEAN VERIFIED** | not all descent certificates |
| No descent certificate \(\Rightarrow\) odd-to-odd | **EXACT — LEAN VERIFIED** | one direction only; complement of the short-certificate remark |

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
| Certified-descent density \(13/16\) (Corollary 4.9) | **EXACT — HUMAN PROOF** | only the three classes \(E\), \(OE\), \(OOEE\); not an \(E\)-rooted census |
| Level-2 wave bound \(q^{-1/6}P^{23/24+\varepsilon}\) (Lemma 5.2) | **EXACT — HUMAN PROOF** | targeted third differencing; standalone statement; corrects the earlier frozen-coefficient model |
| Kernel cancellation \(K_c(P)\ll P^{1-1/96+\varepsilon}\) (Theorem 5.3) | **EXACT — HUMAN PROOF** | \(W\)-shaped family at \(\alpha=9/8\), \(k\le P^{1/24}\); Step 5b interpolant expanded (\(\Phi=a\nu^{5/4}+b\nu^{11/8}+w\nu^{3/2}\)); \(P_0\) ineffective |
| OOO\(*\) splits; depth 4 complete over odd starts (Theorem 6.1) | **EXACT — HUMAN PROOF** | eight O-rooted length-4 classes; Step E estimates the decorated phase at \(\lambda_a'\) and \(\lambda_0'\), not by slogan |
| Length-5/7/8 contracting splits and densities \(7/8\), \(57/64\), \(29/32\) (withdrawn) | **CONJECTURE** | withdrawn from the paper in Phase 26; holes recorded in the ledger (growing remainder, \(E'\) control, passenger budgets) |
| Equidistribution \(\Rightarrow\) density-one descent (Proposition 7.1) | **EXACT — HUMAN PROOF** | \(O\)-rooted hypothesis; conclusion unconditional for \(d\le4\); open beyond |
| Level-3 kernel reformulation (Lemma 7.2) | **EXACT — HUMAN PROOF** | exact Taylor identity; validated in scaled integers |
| Level-3 kernel cancellation \(K_3(P)\ll P^{1-\delta}\) (Conjecture 7.3) | **CONJECTURE** | not claimed; square-root cancellation observed in exact probes |
| Shift-averaged \(L^2\) bound (Proposition 7.4) | **EXACT — HUMAN PROOF** | almost-every-shift, square-root times \(\sqrt{\log L}\) in general; no claim at \(\lambda=0\) |
| Pure amplitude-product model (Conjecture 7.5) | **CONJECTURE** | not claimed; Exp(1) censuses at \(P=10^6\)–\(10^{10}\) |

## Quantifier checks

1. A descent certificate is a realized word with image strictly
   below the start. Paper A's short-certificate remark isolates a
   uniform short subclass. It does not say that odd-to-odd starts
   lack descent.
2. Paper B Corollaries 4.2 and 4.9 are densities of uniform
   subclasses (\(3/4\) at two steps, \(13/16\) at four). Neither is a
   density of `FiniteProgress` nor of `ReachesOne`. The former
   \(7/8\), \(57/64\), \(29/32\) figures are withdrawn conjectures,
   not paper claims.
3. Terras–Everett prove almost-all Collatz stopping times. Neither
   paper proves the Juggler analogue; Proposition 7.1 is an
   unconditional *implication* from all-depth equidistribution, whose
   hypothesis is a theorem for \(d\le4\) and open beyond (first open
   case: the depth-5 \(OOOO*\) split, Conjecture 7.3).
4. `power_bound_contracts` requires a realized contracting word.
5. Cycle restrictions do not exclude all cycles. Paper A Theorem 3.6
   is a census for lengths at most six; Theorem 3.8 extends it to
   lengths at most seven. Theorems 3.12--3.21 exclude leftover
   families; Theorem 3.22 assembles them as an even-count
   exclusion (period at least eleven). Section 4 excludes later
   *periods* by financing. A leftover-length cycle remains
   possible as far as the papers prove.
6. The `native_decide` boundary checks cover the `Fin 256` length-six
   leftover tables and \(257^{64}<2\cdot256^{64}\), and the `Fin 14`
   length-seven leftover tables together with
   \(2^{422}15^{128}<14^{243}\).

## What the papers do not claim

- Every positive integer reaches \(1\).
- Three-quarters (or \(13/16\)) of starts reach \(1\).
- Those densities as *complete* certificate inventories: they count
  uniform classes.
- The withdrawn length-5/7/8 splits or their densities \(7/8\),
  \(57/64\), \(29/32\) (laboratory conjectures since Phase 26).
- E-rooted (even-start) word classes at any depth.
- A Collatz theorem, or a transfer of Terras's theorem to \(J\).
- Density-one finite descent (Proposition 7.1 is conditional on
  all-depth equidistribution; only \(d\le4\) is proved).
- The level-3 kernel bound \(K_3(P)\ll P^{1-\delta}\)
  (Conjecture 7.3 is open), or any bound on the pure
  amplitude-product model at the deterministic shift
  (Conjecture 7.5 is open; Theorem 7.4 is almost-every-shift only).
- Every trajectory meets a contracting word.
- Every nontrivial cycle is impossible.
- A state-distribution finance inequality (the maximum of
  \(\sum 1/(x_i\log x_i)\) over realizable cycle geometry).
  Paper A records that program in Section 5; Theorems 4.4--4.7
  are length-only upper bounds on the same sum.
- The Juggler map is irreducible or has no finite-state model.
- The \(N^{5/6}\) bound controls orbits or arbitrary image sets.

## Suggested falsifiers

Reject or revise if:

1. a Lean theorem is quoted with stronger quantifiers than its statement;
2. the \(3/4\) or \(13/16\) figure is called a Terras theorem or a
   `ReachesOne` density;
3. Paper A's short-certificate remark is read as “odd-to-odd starts have no descent”;
4. any analytic estimate of Paper B is described as Lean-certified;
5. the census of Paper A Theorem 3.6 is read beyond length six, or
   Theorem 3.8 beyond length seven, or Theorem 3.22 is read as a
   length-9 or length-10 word census rather than an even-count
   assembly, or Theorem 3.13 is read
   as a cycle-word exclusion at a non-minimum start, or Theorem
   4.6 is quoted as a Lean theorem, or leftover \(84\) is quoted
   as the printed leftover, or an exclusion of every leftover
   length is attributed to either paper;
6. a discrepancy proof replaces a floor by a single exponential, or
   an exact linearization (Paper B Lemmas 4.3(i), 4.6, 5.1, 7.2) is
   quoted without its one-signed remainder bounds;
7. an interval bound is applied to a sparse image set without transfer;
8. a finite first-return count is promoted to an infinite theorem;
9. Proposition 7.1 is quoted without its equidistribution hypothesis,
   or Conjecture 7.3 or 7.5 is cited as a theorem;
10. Proposition 7.4 is quoted as a bound at the deterministic shift
    \(\lambda=0\), as pure square-root cancellation without the
    \(\sqrt{\log L}\) caveat, or any numerical probe or repository
    validation is treated as a proof step;
11. a withdrawn claim (Theorems 6.2–6.4, Corollaries 5.4 or 6.5 of
    the pre-Phase-26 drafts) is cited as a theorem of Paper B.

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
