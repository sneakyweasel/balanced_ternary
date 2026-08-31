# Juggler reviewer packet (two manuscripts)

Author: Philippe Cochin. Date: 31 August 2026.
Status: Paper A is a submission candidate; Paper B is a working draft.

The former single note has been split into two manuscripts:

- **Paper A** —
  [juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md):
  *Cycles of the Juggler map.* Exact word calculus, defect
  identity, inverse cells, the small-cycle census (no nontrivial
  cycle of length at most seven), the uniform leftover families
  (Theorems 3.12--3.21), the even-count assembly (Theorem 3.22:
  no cycle word has fewer than four even letters, so the period
  is at least eleven), the financing inequality (Theorem 4.4),
  and the floor-\(10^6\) leftover (Theorem 4.6: no period
  \(\le 1053\); remaining periods \(\le 10^5\) lie in \(397\)
  near-convergents of \(\ln 2/\ln 3\)). The arguments of
  Sections 2, 3, and 4 are written in the note. Lean is an
  independent check of the exact claims except Theorem 4.6, which
  is a named computation. Lemma 3.3 is an elementary envelope
  used by Lemma 3.5. Lemma 3.4 writes the next-square
  thresholds, including the odd-run exclusion \(O^aE\) for
  \(a\ge 3\), that assemble Theorem 3.6. Theorems 3.12--3.21
  exclude leftover families by even-count and assemble as
  Theorem 3.22. Section 4 excludes later periods by financing.
  Lean leftover \(84\) is an Appendix A companion, not a paper
  theorem. No density result is stated. After the short-certificate
  remark, the complement of the uniform short certificates is the
  odd-to-odd class.
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
global-defect, census, and finance arguments correct at their stated
quantifiers? Is Theorem 4.6 scoped as a computation, not a Lean
theorem? For Paper B: are the depth-1–4 estimates (exponents
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
envelope, and its local floor losses assemble into an exact
compositional global defect with rigid zero cases. Inverse cells give
cycle restrictions and a small-cycle census: no nontrivial cycle has
length at most seven. After the census, two leftover two-even
families are excluded at every expanding length, gapped three-even
leftovers are excluded on a cycle minimum, the seven bunched
three-even families are excluded, and both gapped leftovers are
excluded as cycle words. Those families assemble: no cycle word has
fewer than four even letters, so a nontrivial cycle has period at
least eleven. A financing inequality at a cycle minimum
restricts every remaining period to a near-convergent of
\(\ln 2/\ln 3\), or to a huge length; with a verified floor through
\(10^6\) there is no period \(\le 1053\). Even and odd-to-even starts
carry uniform short certificates; the starts not covered by those
certificates are exactly the odd-to-odd class, not the starts with
no descent of any length. The small-cycle census is Theorems 3.6
and 3.8; the family theorems are 3.12--3.21; the even-count
assembly is Theorem 3.22; finance is Theorems
4.4--4.6; short certificates are a remark in Section 5.

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
| Global defect identity, vanishing, and composition | **EXACT — LEAN VERIFIED** | weighted lift, not an additive sum; not a uniform tax |
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
| Even-count assembly (Theorem 3.22); period at least eleven (Corollary 3.23) | **EXACT — LEAN VERIFIED** | no cycle word with fewer than four evens; expansion corollary, not a length-9 or length-10 word census |
| Cycle surplus \(\Delta_w(n)=n^{3^{\#O}}-n^{2^{\lvert w\rvert}}\) (Corollary 2.7); per-step slack bound \(x^e<(J(x)+1)^2\) | **EXACT — LEAN VERIFIED** | no uniform per-step tax exists |
| Finance inequality (Theorem 4.4) | **EXACT — LEAN VERIFIED** | `cycleMin_finance`; constant \(1\); not a halt theorem |
| Per-length exclusion given a floor (Corollary 4.5) | **EXACT — HUMAN PROOF** | \(6/5\) table; conservative relative to Theorem 4.4 |
| Computational leftover (Theorem 4.6) | **COMPUTATIONALLY VERIFIED** | floor \(10^6\); no period \(\le 1053\); \(397\) exceptions through \(10^5\); first record survivor \(1054\) |
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
