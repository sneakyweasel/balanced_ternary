# Juggler cycle near-tight rigidity

Status: **ARCHIVED**

Standalone application phase on the Juggler floor-power map, on the
**cycle half** of the `cycles_or_escapes` split. It tests the remaining
Simons–de Weger-family slogan from the cycle-finance open questions:
that `NearTightScale.lean` covers leftover near-convergents by forcing
a hypothetical cycle into an almost-monochrome tower. It is not a halt
theorem, not a floor raise, and not a reopen of approximate equality
rigidity.

## Problem

Open-orbit near-tightness is automatic at large scale: a fixed mixed
word has \(q\to 0\). Exact equality rigidity (\(q=0\) implies a
monochrome tower) is already Lean; approximate stability of that
rigidity is **REFUTED**. Cycle finance leftover lengths
\(L=19,84,569,1054,\ldots\) have a tiny relative gap
\(\theta=1-2^L/3^o\). Is cycle near-tightness (return + tiny gap)
stricter than open-orbit near-tightness, and does that force those
cycles into an almost-monochrome tower?

## Exact statement

Write \(G=3^o-2^L\) and
\(q_w(n)=n^{3^o}/T_w(n)^{2^L}-1\).

**Cycle slack identity (REPARAMETERIZATION of
`image_eq_start_defectRatio`).**
If \(T_w(n)=n\), then \(1+q_w(n)=n^G\) and \(R_w(n)=1\). The
comparison \(q_{\mathrm{open}}<n^G-1\) is exactly \(T_w(n)>n\).

**Zero-defect path expands (EXACT — HUMAN PROOF).**
If \(q=0\), then \(T_w(n)=n^{3^o/2^L}=n\cdot n^{G/2^L}>n\) whenever
\(G>0\) and \(n\ge 2\). A near-tight open orbit stays near that
envelope and cannot return.

**Slogan (REFUTED).** A hypothetical cycle at a record convergent
is forced into an almost-monochrome tower because return + tiny
\(\theta\) is a stricter form of \(q\to 0\).

Counterexamples:

- Tiny \(\theta\) is not tiny \(q\). At \(L=19\), \(G=7153\), so a
  cycle has \(1+q=n^{7153}\). Open-orbit \(q\to 0\) is the opposite
  regime.
- Hamming distance to a monochrome word at \(o_{\min}\) is the even
  count: \(7,31,210,389\) along \(L=19,84,569,1054\). Even-count
  \(\ge 4\) is already Lean. The leftovers become *less* monochrome.
- Realized `OOE` (the first leftover length, \(G=1\)) expands and
  never returns on the scanned window; \(q_{\mathrm{open}}<n-1\)
  holds exactly by the image comparison.
- The mixed `OOE` at \(y=180370579261640036336071806107777\) has
  \(0<q<10^{-30}\) and \(T(y)>y\). A cycle at \(y\) would need
  \(q=y-1\).

NearTightScale therefore does not cover leftover convergents
simultaneously. \(R=1\) on a return is Corollary 2.7, already Lean.
No leftover length dies.

## Current literature

- Scale-induced near-tightness —
  **EXACT — LEAN VERIFIED** / **COMPUTATIONALLY VERIFIED**
  (`J-near-tight-scale-bounds`, `J-ooe-scale-decay`,
  [juggler_near_tight_scale.md](juggler_near_tight_scale.md)).
- Approximate equality rigidity —
  **REFUTED** (`J-approx-equality-rigidity`).
- Exact equality rigidity —
  **EXACT — LEAN VERIFIED** (`power_bound_eq_implies_monochrome`).
- A realized return burns the formal surplus —
  **EXACT — LEAN VERIFIED** (`image_eq_start_defectRatio`).
- Cycle finance inequality —
  **EXACT — LEAN VERIFIED** (`cycleMin_finance`,
  [juggler_cycle_finance.md](juggler_cycle_finance.md)).
- Baker / Rhin on \(\lvert 3^o-2^L\rvert\) as a leftover killer —
  **CLOSE** / **REFUTED**
  ([juggler_cycle_gap_baker.md](juggler_cycle_gap_baker.md)).
- Collatz \(m\)-cycle financing-versus-gap —
  **known** (`simons-de-weger-2005-collatz-m-cycles`).
- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**.
  Totality is not claimed.

Project relationship: **refuted** as a leftover killer; the
scale-decay bounds themselves remain **known**.

## Branch budget

```text
Mathematical target     Is cycle near-tightness (return + tiny θ)
                        stricter than open-orbit near-tightness
                        (q→0), and does that force leftover
                        convergents L=19,84,569,1054,… into an
                        almost-monochrome tower?
Novelty hypothesis      Return plus a record gap is a stronger
                        rigidity than scale-induced tiny q
Falsifier               cycle 1+q = n^{3^o-2^L} (huge); leftover
                        Hamming to monochrome grows; open near-tight
                        paths expand instead of returning
Existing machinery      image_eq_start_defectRatio, NearTightScale,
                        cycleMin_finance, equality monochrome,
                        J-approx-equality-rigidity REFUTED
Maximum Phase-0 scope   Exact cycle-q identity; record Hamming/θ
                        table; OOE open-vs-cycle check; 329
                        illustration. No Lean, no floor raise
Promotion criterion     a leftover-killing rigidity that is not
                        R=1 or cycleMin_finance
Stop criterion          slogan is a category error, or every exact
                        fact is a reparameterization
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Cycle \(1+q=n^G\) and \(R=1\) on a return —
  **REPARAMETERIZATION** of `image_eq_start_defectRatio`
- \(q_{\mathrm{open}}<n^G-1\) iff \(T_w(n)>n\) —
  **REPARAMETERIZATION** of the slack definition
- Zero-defect path expands by \(n^{G/2^L}\) —
  **EXACT — HUMAN PROOF**
- Record Hamming to monochrome grows along
  \(L=19,84,569,1054\) —
  **COMPUTATIONALLY VERIFIED**
- Realized `OOE` expands and does not return —
  **COMPUTATIONALLY VERIFIED** on the scanned window;
  length 3 is already census-excluded
- Mixed `OOE` at the 329 successor is near-tight and expanding —
  **COMPUTATIONALLY VERIFIED** (reuses `J-approx-equality-rigidity`)
- Cycle at a leftover convergent is almost-monochrome —
  **REFUTED** (`juggler_cycle_near_tight_monochrome`)
- NearTightScale excludes a leftover length —
  **REFUTED**
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_near_tight`
- Records: [juggler_cycle_near_tight.md](../research/juggler_cycle_near_tight.md),
  [juggler_cycle_near_tight.json](../research/juggler_cycle_near_tight.json)
- Dataset: `data/research/juggler/cycle_near_tight/`
- Tests: `tests/research/juggler_sequence/test_cycle_near_tight.py`

Science window: record lengths \(1,3,11,19,84,569,1054\); realized
`OOE` on odd-odd starts \(n\le 2000\); the existing 329 successor.
No CLI. No new Lean. Paper A is unchanged.

## Conjectures

`juggler_cycle_near_tight_monochrome` — **REFUTED**.

## Counterexamples

- \(L=19\), \(o=12\): cycle \(1+q=n^{7153}\); Hamming to monochrome
  is \(7\); a zero-defect path at \(n=53\) grows by more than
  \(5\%\).
- Hamming \(7,31,210,389\) along \(L=19,84,569,1054\).
- Realized `OOE` through \(n=2000\): \(0\) returns, every open
  \(q<n-1\), every \(R<1\).
- Mixed `OOE` at
  \(y=180370579261640036336071806107777\): \(0<q<10^{-30}\) and
  \(T(y)>y\); cycle-required \(q=y-1\).

## Formalization

None added. `image_eq_start_defectRatio`,
`power_bound_eq_implies_monochrome`, and `NearTightScale.lean`
already exist. No `CycleNearTight.lean`, no
`AlmostMonochrome.lean`, and no `sorry`. Paper A is unchanged.
Not a halt theorem.

## Results

Classification **CYCLE_NEAR_TIGHT_CLOSED**. Regenerate with
`python -m research.juggler_sequence.cycle_near_tight`.

- Cycle slack on a return is \(n^G-1\), not a vanishing \(q\).
- Open-orbit near-tightness is the expanding regime
  \(T_w(n)>n\). Return is the opposite comparison.
- Leftover convergents are farther from monochrome as \(L\)
  grows, not closer.
- No leftover length is excluded. The finance open question that
  named `NearTightScale.lean` as a wholesale leftover killer is
  closed.

## Open questions

Stop on NearTightScale as a leftover-convergent killer. Do not
reopen approximate equality rigidity. The leftover lengths remain
a floor question, not a slack-rigidity question.

## Decision

**CLOSE**. The slogan is a category error: tiny \(\theta\) is not
tiny \(q\), and cycle \(R=1\) is already Lean. Open-orbit
near-tight paths expand; a cycle needs more defect, not less.
Leftover Hamming to monochrome grows. This is not a halt theorem
and not a reason to raise the floor inside this branch.

Best next question: can the residual floor be raised past the
next live convergent \(n_{\max}\), so that finance kills that
length?

## Publication assessment

Status: `ARCHIVED`.

A negative transfer: the unused NearTightScale leftover-killer
does not become a Juggler theorem. The obstruction is exact
(cycle \(1+q=n^G\) versus open-orbit \(q\to 0\)) and the
Hamming comparison is finite. Not a paper candidate and not a
Juggler totality result.
