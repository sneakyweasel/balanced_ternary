# Juggler \(W\)-family at \(\alpha=33/32\)

Status: **PROMOTE** (instance only). The Corollary R′ family
(`J-w-family-below-nine-eighths`) stays **CONJECTURE**. Length 7/8
stay **PARK**. Paper B stays frozen at \(13/16\).

Phase-28 desk rerun of Paper B Theorem 5.3 at one concrete
exponent. Child of
[juggler_engine_harvest.md](juggler_engine_harvest.md). Not a
\(K_3\) attack and not a Paper B edit.

## Problem

Corollary R′ was withdrawn in Phase 26 as proof-by-monotonicity:
the bound was never rerun at any \(\alpha\neq 9/8\). The intended
consumer is the length-7 engine, which uses a \(W\)-family at
\(\alpha=33/32<9/8\). Does Theorem R’s bound hold at that single
exponent?

## Exact statement

Let \(c\) be smooth on \((P,2P]\) with
\(c^{(r)}\asymp kP^{33/32-r}\) for \(r=0,\ldots,4\), derivative
signs following the monomial pattern, and \(1\le k\le P^{1/24}\).
Is \(K_c(P)\ll P^{1-1/96+\varepsilon}\), uniformly in \(k\)?

## Current literature

- Paper B Theorem 5.3 (`J-kernel-cancellation`): the same bound
  at \(\alpha=9/8\) — **EXACT — HUMAN PROOF**. **reproduced**.
- Corollary R′ (`J-w-family-below-nine-eighths`): family on a
  finite subset of \((0,9/8]\setminus\{1/4,3/4\}\) —
  **CONJECTURE**. **extended** at one point.
- Scale-invariant copy at \(\alpha=27/16\) or \(45/16\)
  (`J-scale-invariant-R-extension`) — **REFUTED**. Not re-tested.
- Length-7 contractors (`J-depth7-engine-contracting`) still have
  the growing remainder \(n^{9/32}\). **independent**.
- Parent
  [juggler_engine_harvest.md](juggler_engine_harvest.md)
  remains `THEOREM` for the length-5 repair.

## Branch budget

```text
Mathematical target     Does Theorem R's bound hold at the single
                        monomial family α = 33/32?
Novelty hypothesis      The Phase-24 hole was a missing rerun, not
                        a refutation; 33/32 < 9/8 so most windows
                        ease, but a curvature composite can flip.
Falsifier               A displayed Step-5 / Lemma 5.2 margin that
                        dies or changes sign at α = 33/32.
Existing machinery      Paper B Theorem 5.3 + Lemmas 3.8–3.10,
                        5.1–5.2; ledger row
                        J-w-family-below-nine-eighths.
Maximum Phase-0 scope   Desk rerun at α = 33/32 only. No length-7
                        remainder, no Paper B edit, no new CLI,
                        no family-for-all-α claim.
Promotion criterion     Every displayed constraint survives with
                        a named margin; instance row EXACT.
Stop criterion          A load-bearing margin dies (PARK the
                        instance; leave the family CONJECTURE).
                        Machinery gravity.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Standing estimates (E3)\(^\dagger\)–(E4)\(^\dagger\) at
  \(\alpha=33/32\) — **EXACT — HUMAN PROOF**
- Offset composite \(\lambda_a=\tfrac{9369}{8192}k|j|n^{-7/32}\)
  single-signed at ratio \(3.711\) — **EXACT — HUMAN PROOF**
- Zero-offset interpolant coefficient \(1701/1024\) and
  exponent set \(E^\dagger=E\cup\{41/32,57/32\}\), with
  \(c_6\bigl(\tfrac54,\tfrac{41}{32}\bigr)=1/55\) —
  **EXACT — HUMAN PROOF**
- Instance bound `J-w-family-thirty-three-thirty-seconds` —
  **EXACT — HUMAN PROOF**
- Corollary R′ family — **CONJECTURE**
- Length-7 remainder \(n^{9/32}\), length-8 \(E'\) —
  **CONJECTURE** (untouched)
- \(K_3\) bound — **PARK** (BB/GG/JJ)

## Experiments

No new runner. Algebraic seals (exact fractions, sign product,
distinctness of \(E^\dagger\), \(c_6=1/55\)) live in
`tests/research/juggler_sequence/test_two_step_parity.py`.

## Conjectures

None new. `J-w-family-below-nine-eighths` stays a conjecture.
Length-7/8 harvest rows stay as they are.

## Counterexamples

None. The Phase-26 hole was a missing rerun. The close pair
\(\bigl(\tfrac54,\tfrac{41}{32}\bigr)\) does not vanish
\(c_6\) and is not a refutation.

## Formalization

None added. Packaging the discrepancy kernel at a second
exponent would be machinery gravity.

## Results

- **Theorem R at \(\alpha=33/32\) (EXACT — HUMAN PROOF,
  `J-w-family-thirty-three-thirty-seconds`).**
  \(K_c(P)\ll P^{1-1/96+\varepsilon}\) for
  \(c^{(r)}\asymp kP^{33/32-r}\), uniformly in
  \(k\le P^{1/24}\). Proof: lemma Part XIII.

## Open questions

The length-7 remainder: can \(kE\) with \(E\asymp v^{1/8}\) be
kept as a subcritical extra phase and estimated? The
Corollary R′ family at any other concrete
\(\alpha\in(0,9/8]\setminus\{1/4,3/4,33/32\}\) is a separate
rerun.

## Decision

**PROMOTE** the instance. Every displayed constraint of
Theorem 5.3 survives at \(\alpha=33/32\): \(M_1\) deletion,
Lemma 3.7 windows, Lemma 5.2 a fortiori, offset ratio
\(3.711\), zero-offset sub-unit \(B\), and the middle-band
triple \(\bigl(\tfrac54,\tfrac{41}{32},\tfrac32\bigr)\) with
\(c_6=1/55\). Do not promote the family. Do not auto-continue
to length 7. Best next question: the length-7 remainder
\(n^{9/32}\).

## Publication assessment

Status: `THEOREM` (laboratory). Not a Paper B edit: the
referee froze the printed claim set at \(\alpha=9/8\). Import
is a later editorial decide.
