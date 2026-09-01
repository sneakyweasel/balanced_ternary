# Juggler length-7 remainder engine

Status: **PROMOTE** (remainder estimate only). Theorem X and
density \(57/64\) stay **CONJECTURE**. Paper B stays frozen at
\(13/16\).

Phase-29 desk classification of the Lemma X1 remainder. Child of
[juggler_engine_harvest.md](juggler_engine_harvest.md). Not a
\(K_3\) attack and not a Paper B edit.

## Problem

The Phase-13 draft of Theorem X discarded the Taylor remainder
\(E_X\le\tfrac38 p^{-1/2}+\tfrac{45}{32}v^{1/8}\). The second
term grows like \(n^{9/32}\); discarding costs
\(kP^{1+9/32}\), worse than trivial. Can \(kE_X\) be kept as a
phase and estimated?

## Exact statement

For \(1\le\lvert k\rvert\le P^{1/24}\) and \(E_X\) as in
Lemma X1, is
\(\lvert\sum_{n\sim P,\,n\text{ odd}}e(kE_X(n))\rvert
\ll P^{27/32+\varepsilon}\), and is the extra phase an engine
of amplitude \(\asymp kn^{9/32}\) in the smooth argument
\(n^{9/8}\)?

## Current literature

- Lemma X1 (`sixth_ooeoo_scan`) — **EXACT — HUMAN PROOF**.
  **reproduced**.
- Paper B Lemma 3.3 / 3.7 / 3.10 — **EXACT — HUMAN PROOF**.
  **reproduced**.
- Theorem R at \(\alpha=33/32\)
  (`J-w-family-thirty-three-thirty-seconds`) — **EXACT —
  HUMAN PROOF**. **independent** (used by other length-7
  pieces, not by this remainder).
- Theorem X (`J-depth7-engine-contracting`) —
  **CONJECTURE**. The remainder was one named hole; the
  passenger inventory is the other. **extended**.
- Scale-invariant copy at \(\alpha>9/8\) — **REFUTED**. Not
  re-tested.

## Branch budget

```text
Mathematical target     Can kE, E ≍ v^{1/8}, be retained as a
                        phase and estimated (not discarded)?
Novelty hypothesis      The hole was discarding a growing
                        envelope; the actual E_w is A {n^{9/8}}^2
                        with A ≍ k n^{9/32} < n.
Falsifier               The Fourier / Lemma 3.3 cost of
                        e(A {n^{9/8}}^2) exceeds trivial, or
                        the argument is a nested floor above
                        the engine line.
Existing machinery      Lemma X1; Paper B Lemmas 3.3, 3.7, 3.10;
                        sixth_ooeoo_scan.
Maximum Phase-0 scope   Desk classification of kE. Seal the
                        {v^{1/2}} ~ {n^{9/8}} reduction. No
                        Theorem X retag, no length-8, no
                        Paper B, no new CLI.
Promotion criterion     A displayed estimate of the extra
                        phase inside P^{23/24}.
Stop criterion          A load-bearing margin dies (PARK).
                        Machinery gravity.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Split \(E_X=E_p+E_w\) with \(E_p\) decaying —
  **EXACT — HUMAN PROOF**
- Reduction \(\theta_w=\{n^{9/8}+O(n^{-3/8})\}\) —
  **EXACT — HUMAN PROOF** (`x1_remainder_reduction_scan`)
- Lemma X4, Fresnel engine
  (`J-length7-remainder-engine`) —
  **EXACT — HUMAN PROOF**
- Theorem X / density \(57/64\) — **CONJECTURE**
  (passenger inventory not rerun)
- Length-8 \(E'\) — **CONJECTURE** (untouched)
- \(K_3\) bound — **PARK** (BB/GG/JJ)

## Experiments

No new runner. Seals in
`research.juggler_sequence.two_step_parity`:
`sixth_ooeoo_scan` (identity) and
`x1_remainder_reduction_scan` (argument reduction through
\(n=10^6\)). Tests:
`tests/research/juggler_sequence/test_two_step_parity.py`.

## Conjectures

None new. `J-depth7-engine-contracting` and
`J-seven-step-descent-density` stay conjectures.

## Counterexamples

None. Discarding \(E_w\) is the hole, not a refutation of
the count.

## Formalization

None added. Packaging a Fresnel engine at one extra
exponent would be machinery gravity.

## Results

- **Lemma X4 (EXACT — HUMAN PROOF,
  `J-length7-remainder-engine`).**
  \(\lvert\sum e(kE_X)\rvert\ll P^{27/32+\varepsilon}\)
  for \(\lvert k\rvert\le P^{1/24}\). The extra phase is
  \(A\{n^{9/8}\}^2\) with \(A\asymp kn^{9/32}\). Proof:
  lemma Part XIV.

## Open questions

The passenger slogan is the child
[juggler_length7_passenger.md](juggler_length7_passenger.md)
(Phase 30, **REFUTED** as a method). Length 8 stays behind
\(E'\).

## Decision

**PROMOTE** the remainder estimate. \(kE_w\) is an engine,
not a discardable remainder and not a (D3) decoration.
Do not retag Theorem X. Do not auto-continue to the
passenger rerun or length 8. Best next question: the
length-7 passenger inventory.

## Publication assessment

Status: `THEOREM` (laboratory). Not a Paper B edit: Paper B
already names the growing remainder as future work and
prints \(13/16\) only.
