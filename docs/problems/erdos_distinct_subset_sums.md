# Erdős distinct subset sums

Status: **EXPLORATORY**

Erdős Problem #1: the least possible maximum of an \(n\)-element
sum-distinct set. Phase 0 asks whether canonical balanced-ternary
normalization or \(v_3\) of signed sums adds a constraint beyond the
elementary kernel \(R(A)=\{0\}\).

## Problem

If
\(A=\{a_1,\ldots,a_n\}\subseteq\{1,\ldots,N\}\)
has all \(2^n\) subset sums distinct, Erdős conjectured
\(N\gg 2^n\).
The problem is open. This branch does not claim a solution.

## Exact statement

Write
\[
R(A)
=
\bigl\{\varepsilon\in\{-1,0,+1\}^n:
\textstyle\sum_i\varepsilon_i a_i=0\bigr\}.
\]
Then \(A\) is sum-distinct if and only if \(R(A)=\{0^n\}\). This
equivalence is elementary and is already the language of
Dubroff–Fox–Xu. The Phase-0 question is whether the canonical word
\(\operatorname{encode}(\sum\varepsilon_i a_i)\), its carry trace, or
\(v_3\) of that integer imposes a further structural constraint on a
sum-distinct set.

## Current literature

Status references, not exhaustive catalogues:
`erdos-problems-1`, `open-problem-garden-distinct-subset-sums`.

- Trivial pigeonhole \(N\gg 2^n/n\). `KNOWN`
- `erdos-moser-1956`: \(N\ge(1/4-o(1))\,2^n/\sqrt{n}\). Variance /
  second-moment. `KNOWN`
- `elkies-1986-sum-distinct`, Bae, Aliev: constant improvements.
  `KNOWN`
- `dubroff-fox-xu-2021`:
  \(N\ge(\sqrt{2/\pi}-o(1))\,2^n/\sqrt{n}\)
  and the exact bound
  \(N\ge\binom{n}{\lfloor n/2\rfloor}\).
  Berry–Esseen, and Harper isoperimetry on the cube using
  \(\varepsilon\in\{-1,0,+1\}^n\). `KNOWN`. This is the signed-alphabet
  baseline, not a balanced-ternary novelty.
- `steinerberger-2023-distinct-subset-sums`: near-Gaussian subset sums;
  another proof of the same \(\sqrt{2/\pi}\) bound. `KNOWN`
- Powers of 2: \(N\le 2^{n-1}\). `KNOWN`
- `conway-guy-1968`, `guy-1982-distinct-sums`, `oeis-A005318`:
  Conway–Guy construction. `KNOWN`
- `bohman-1996-conway-guy`: Conway–Guy sets are sum-distinct. `KNOWN`
- `lunnon-1988-distinct-subset-sums`: exact \(f(n)\) for \(n\le 8\);
  four families beating Conway–Guy at large \(n\). `KNOWN`
- `bohman-1998-construction`: record upper bound
  \(f(n)\le 0.22002\cdot 2^n\). `KNOWN`
- `oeis-A276661`: the sequence \(f(n)\). Lunnon \(n\le 8\), Grossman
  \(n=9\). `KNOWN`
- Dissociated-set restatement \(F(x)<\log_2 x+O(1)\). `KNOWN` /
  `REPARAMETERIZATION`
- `bae-1996-subset-sum-distinct`: \(q\)-fold dissociated sets. The
  \(q=2\) case is all signed sums distinct, strictly stronger than
  sum-distinctness. `KNOWN`
- `cambie-gao-kim-liu-2025-modular`: modular variant modulo
  \(2^n+t\), characterised by \(2\)-adic valuations. Different
  problem. `KNOWN`
- `gu-2025-generalisation`, `costa-dalai-della-fiore-2023`:
  \(\mathbb Z^k\) / restricted-size variants via statistical bridges
  on signed sums. Same signed-sum viewpoint, no \(v_3\). `KNOWN`
- `avizienis-1961-signed-digit`, `knuth-taocp-vol2`,
  `hayes-2001-third-base`: signed-digit encoding. `KNOWN`

The identity \(3^k\mid s\) and \(|s|<3^k\) implies \(s=0\) is
elementary. `KNOWN`

No source in the gate uses canonical balanced-ternary normalization
of signed sums to bound \(f(n)\). After the census that slot is
`REPARAMETERIZATION`: \(\operatorname{encode}(s)\) is a complete
invariant of the integer \(s\).

The parked module
[additive_combinatorics.md](additive_combinatorics.md) is
digit-restricted sumsets \(A_k,B_k,C_k\). Same digit alphabet,
different question. It stays `PARK`.

## Branch budget

```text
Mathematical target     Does canonical BT normalization, carry, or v_3 of
                        signed sums constrain sum-distinct sets beyond
                        the elementary kernel R(A)={0}?
Novelty hypothesis      Digit length, leading trit, carry, or a
                        magnitude+v_3 collision yields a structural
                        obstruction or a genuinely different proof of a
                        known lower bound.
Falsifier               Every useful consequence reduces to "nonzero
                        signed combinations are nonzero" plus ordinary
                        size/concentration (H1). DFX already uses
                        ε ∈ {-1,0,+1}^n.
Existing machinery      bt.representation.encode, bt.metrics.v3 /
                        lsd_nonzero_index, bt.normalization.rewrite_sum.
                        Parked research.additive_combinatorics is a
                        different problem and is not reopened.
Maximum Phase-0 scope   Literature gate + signed-relation model + exact
                        experiments on known constructions for n≤12 +
                        one candidate lemma or a documented H1 close.
Promotion criterion     One theorem that uses BT / 3-adic structure
                        nontrivially (new obstruction, new construction,
                        or a new mechanism for a known bound).
Stop criterion          All surviving claims are KNOWN or
                        REPARAMETERIZATION, or only computational tables
                        remain.
```

## Balanced-ternary formulation

A signed combination is the integer
\(s=\sum_i\varepsilon_i a_i\)
with \(\varepsilon_i\in\{-1,0,+1\}\). Its canonical word is
\(\operatorname{encode}(s)\). The relation tree walks coefficients in
order and merges nodes with the same partial integer sum. At depth
\(j\),
\[
R_j(A)=\#\{\text{distinct partial sums after }j\text{ coefficients}\}.
\]
A modular image
\(\phi_k(\varepsilon)=\sum\varepsilon_i a_i\bmod 3^k\)
is labelled `MODULAR ONLY` until magnitude forces \(s=0\).

## Why BT may be relevant

The coefficient alphabet is the balanced-ternary digit alphabet. That
fact alone is not novelty: DFX already uses it. Relevance of
*canonical normalization* would require the word of \(s\), its carry,
or \(v_3(s)\) to constrain \(A\) more tightly than the integer \(s\).
Phase 0 tests that and refutes it.

## Candidate operations / invariants

- Kernel equivalence
  \(A\) sum-distinct \(\iff R(A)=\{0^n\}\) — **PROVED**, elementary;
  `KNOWN`.
- All signed sums distinct is strictly stronger —
  **PROVED** by \(\{1,2,4\}\). `KNOWN` (Bae \(q=2\)).
- Magnitude–valuation bridge
  \(v_3(s)\ge k\) and \(|s|<3^k\) \(\Rightarrow s=0\) — **PROVED**,
  elementary. Hits equal \(R(A)\). `REPARAMETERIZATION`.
- Canonical length equals the magnitude bound
  \(|s|\le(3^L-1)/2\) — **PROVED** from uniqueness of balanced
  expansion. `REPARAMETERIZATION`.
- \(v_3(s)\) equals the least-significant nonzero digit index —
  **PROVED** (`bt.metrics.check_v3_identity`). `KNOWN`.
- High \(v_3\) density forces an exact relation — **REFUTED**.
  Powers of 2 and Conway–Guy are sum-distinct and have many nonzero
  signed sums with \(v_3\ge 1\).
- A BT digit pattern forbidden on every sum-distinct set —
  **REFUTED**. Both families admit leading trits \(\{-1,0,+1\}\) and
  overlapping length histograms.
- A 3-adic proof of DFX — **REFUTED** as a Phase-0 mechanism. The
  DFX gap is isoperimetric / Gaussian, not a statement about
  \(\operatorname{encode}(s)\).
- Powers of 3 as a construction — **REFUTED** as an improvement.
  They are even *signed*-sum-distinct (uniqueness of balanced
  expansions) but give \(N=3^{n-1}\), worse than \(2^{n-1}\).

## Experiments

`research.erdos_distinct_subset_sums.triage` on powers of 2,
Conway–Guy / A276661 extremals (identical for \(n\le 9\)), powers of
3, and the controls \(\{1,2,3\}\) and \(\{1,2,4\}\). Exact signed
enumeration through \(n=12\) (\(3^{12}=531441\)). Tests:
`tests/research/erdos_distinct_subset_sums/test_triage.py`. No
experiment runner is registered. No \(\binom{N}{n}\) search.

## Conjectures

None registered.

## Counterexamples

1. **All signed sums distinct is stronger than sum-distinct.**
   \(\{1,2,4\}\) is sum-distinct and
   \(1+4=5=(-1)+2+4\).
2. **High \(v_3\) does not force a relation.**
   For \(\{1,2,4\}\), eight nonzero signed sums have \(v_3=1\), and
   \(C_A(0)=1\).
3. **The magnitude–valuation bridge is the kernel.**
   On every tested set, including \(\{1,2,3\}\) and \(n\le 12\)
   constructions, the vectors with \(v_3(s)\ge k\) and \(|s|<3^k\)
   are exactly \(R(A)\).
4. **Powers of 3 lose to powers of 2.**
   At \(n=12\), \(\max=177147\) versus \(2048\).
5. **Canonical words do not separate the two extremal families.**
   Both admit leading trits \(\{-1,0,+1\}\). Digit length is the
   magnitude bound on both.

## Formalization

None. No `sorry`. Lean is not opened on this gate.

## Results

### What was learned

1. The signed-kernel equivalence is the DFX coefficient language, not
   a laboratory reformulation.
2. \(\operatorname{encode}(s)\) is a complete invariant of the integer
   signed sum. Length, leading trit, and \(v_3\) are functions of
   \(s\).
3. The three predicates must stay distinct: sum-distinct, all signed
   sums distinct, and modular relations.
4. The magnitude–valuation bridge reproduces \(R(A)\) and nothing
   else.
5. Modular collisions exist as soon as \(3^n>3^k\) and are labelled
   `MODULAR ONLY`. They do not force exact zeros.
6. Powers of 3 realise unique signed sums and are a worse
   construction than powers of 2.
7. Conway–Guy is sum-distinct through \(n=12\) with a strictly
   smaller maximum than powers of 2; its signed-sum tree is denser
   (\(R_{12}=16995\) versus \(8191\)) and is not \(3^n\).

### Known baseline

Erdős–Moser / Elkies / DFX / Steinerberger lower bounds; Conway–Guy /
Lunnon / Bohman constructions; Bae’s stricter signed-sum-distinct
property; the elementary \(3\)-adic magnitude lemma.

### Balanced-specific phenomenon

None that survives the integer identification
\(\operatorname{encode}(s)\leftrightarrow s\). Carry counts along
coefficient paths are ordinary word addition of the same integers.

### Strongest candidate theorem

For every integer \(s\) and every \(k\ge 1\),
\(v_3(s)\ge k\) and \(|s|<3^k\) if and only if \(s=0\).
Consequently the magnitude–valuation hit list of \(A\) equals
\(R(A)\). **EXACT — HUMAN PROOF**; tagged `REPARAMETERIZATION`.

### Strongest refutation

Hypothesis H2: canonical balanced normalization imposes an extra
constraint on sum-distinct sets. Every measured statistic of the
normalized word is a function of the integer signed sum, already
constrained by \(C_A(0)=1\).

### Relation to known bounds

Nothing is improved and nothing is reproduced by a new mechanism.
The DFX binomial bound is isoperimetric on the cube. Digit length of
\(s\) is \(\log_3|s|+O(1)\) and cannot replace Harper’s boundary
estimate.

### Computational evidence

Exact signed enumeration, \(n\le 12\). Selected rows, \(k=2\):

| set | \(n\) | \(\max\) | sum-distinct | all signed distinct | \(C_A(0)\) | \(R_n\) | \(3^n\) | modular-only kernel |
|-----|------:|---------:|:------------:|:-------------------:|-----------:|--------:|------:|--------------------:|
| \(\{1,2,3\}\) | 3 | 3 | no | no | 3 | 13 | 27 | 0 |
| \(\{1,2,4\}\) | 3 | 4 | yes | no | 1 | 15 | 27 | 0 |
| powers of 2 | 7 | 64 | yes | no | 1 | 255 | 2187 | 248 |
| Conway–Guy | 7 | 44 | yes | no | 1 | 385 | 2187 | 242 |
| powers of 3 | 7 | 729 | yes | yes | 1 | 2187 | 2187 | 242 |
| powers of 2 | 12 | 2048 | yes | no | 1 | 8191 | 531441 | 59102 |
| Conway–Guy | 12 | 1164 | yes | no | 1 | 16995 | 531441 | 59048 |
| powers of 3 | 12 | 177147 | yes | yes | 1 | 531441 | 531441 | 59048 |

Conway–Guy \(a_n\) through \(12\):
\(0,1,2,4,7,13,24,44,84,161,309,594,1164\).
A276661 extremals for \(n\le 9\) equal these Conway–Guy sets.
Carry census at \(n=7\): powers of 2 have \(7258\) nonzero carry
steps, Conway–Guy \(12180\); both have path-maxima \(11\) and \(14\).
That is denser addition, not an obstruction.

### Literature verdict

`KNOWN` / `REPARAMETERIZATION`. The census is `PROJECT-SPECIFIC`
measurement and is not promoted.

## Open questions

None retained. In particular, a construction hunt, a generic
additive-combinatorics package, Lean, and a 3-adic recast of DFX are
not opened.

## Decision

`CLOSE`. The signed-kernel equivalence is the classical definition of
a dissociated set, already used by Dubroff–Fox–Xu. Canonical
balanced-ternary data of a signed sum are a reparameterization of the
integer. The magnitude–valuation bridge is the elementary lemma
\(|s|<3^k\) and \(3^k\mid s\) imply \(s=0\), hence equals \(R(A)\).
High valuation, digit patterns, and modular collisions all reduce to
ordinary size or pigeonhole. Powers of 3 are the unique-expansion
set and lose to powers of 2. A branch whose exact statements are
`KNOWN` or `REPARAMETERIZATION` is a close.

Best next question: none on this branch; the gate is closed.

## Publication assessment

Status: `EXPLORATORY`.

Not a `PAPER_CANDIDATE`. No theorem uses balanced-digit structure
beyond the integer signed sum. Do not start Phase 1.
