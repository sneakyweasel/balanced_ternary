# Juggler Step 5b interpolant \(P_0\)

Status: **PROMOTE** (printed-chain hole + laboratory
\(P_0\) table). Paper B stays frozen.
`J-kernel-cancellation` is not retagged.

Child of
[juggler_kernel_p0_hypotheses.md](juggler_kernel_p0_hypotheses.md).
The remaining omitted threshold named by that branch.
Sibling of the Step 5b sublevel geometry gate. Not a
\(K_3\) attack and not a Paper B edit.

## Problem

Paper B says several comparisons force a large ineffective
\(P_0\), and quotes \(54P^{-25/24}\le 0.1P^{-5/6}\) in
Step 5b as the example. The displayed interpolant-error
chain is
\(203P^{-25/24}+0.11P^{-5/6}+16P^{-25/24}\le 0.1P^{-5/6}\).
Does that chain hold for any \(P\), and what is the first
working \(P_0\) for every displayed Step 5b numerical
margin?

## Exact statement

On the printed majorants of Theorem 5.3 Step 5b, at which
first integer \(P\) (if any) do the following hold?

- the displayed interpolant-error chain
  \(219P^{-25/24}+0.11P^{-5/6}\le 0.1P^{-5/6}\)
- the introductory example
  \(54P^{-25/24}\le 0.1P^{-5/6}\)
- \(V\ge 10\lvert f''-\Lambda\rvert\) at the printed
  \(V\ge 1.35P^{-37/48}\) against the three-term error
- \(V/S\le 6.7P^{-7/48}\le c_7S/2\) (printed majorant)

Exponential sums and the Lemma 3.9 geometry census are
not re-run.

## Current literature

- Paper B Theorem 5.3 Step 5b / Lemma 3.9
  (`J-kernel-cancellation`) — **EXACT — HUMAN PROOF**.
  **reproduced** (the printed numerical chain only).
- Kernel \(P_0\) hypotheses — **extended** (this is the
  named leftover).
- Step 5b sublevel geometry — **independent** (interval
  counts, not this chain).
- Decoration-budget \(P\ge 3^{48}\) — **independent**
  (a different overflow).
- Scale-invariant copy of Theorem R — **REFUTED**. Not
  re-tested.

## Branch budget

```text
Mathematical target     Does the printed Step 5b interpolant-error
                        chain hold for any P, and what is the first
                        P0 for every displayed Step 5b numerical
                        margin?
Novelty hypothesis      The 0.11 > 0.1 coefficient may be a hole;
                        otherwise the first P0 is the omitted large
                        threshold.
Falsifier               The chain fails for all P, or a displayed
                        margin never holds.
Existing machinery      kernel_p0 first_true search; step5b_sublevel
                        c7; Paper B Step 5b displayed constants.
Maximum Phase-0 scope   Closed-form checker of the printed Step 5b
                        numerical lines only. No sums, no sublevel
                        re-grid, no Paper B edit, no Lean, no
                        kernel retag.
Promotion criterion     A named hole or a concrete first P0.
Stop criterion          After the table. Machinery gravity.
```

## Balanced-ternary formulation

None required. The objects are real power comparisons.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- As-printed interpolant chain —
  **REFUTED** (never holds)
- Introductory example \(54P^{-25/24}\le 0.1P^{-5/6}\) —
  **COMPUTATIONALLY VERIFIED** first \(P_0\)
- \(V\ge 10\lvert f''-\Lambda\rvert\) and \(V/S\le c_7/2\) —
  **COMPUTATIONALLY VERIFIED** first \(P_0\)
- Kernel bound — untouched **EXACT — HUMAN PROOF**

## Experiments

- Probe: `research.juggler_sequence.step5b_p0`
- Record: [summary.json](../../data/research/juggler/step5b_p0/summary.json)
- Tests: `tests/research/juggler_sequence/test_step5b_p0.py`

Closed-form only. No odd-\(n\) walk.

## Conjectures

None new. `J-kernel-cancellation` stays
**EXACT — HUMAN PROOF**.

## Counterexamples

The displayed chain
\(219P^{-25/24}+0.11P^{-5/6}\le 0.1P^{-5/6}\)
fails for every \(P>1\), because the \(0.11P^{-5/6}\)
term already exceeds the right-hand side. See Results.

## Formalization

None added. Packaging a false displayed constant is
machinery gravity.

## Results

- **Displayed interpolant chain (REFUTED as a printed
  comparison).**
  \(203P^{-25/24}+0.11P^{-5/6}+16P^{-25/24}\le 0.1P^{-5/6}\)
  never holds for \(P>1\): the \(0.11P^{-5/6}\) term
  already exceeds the right-hand side, and the
  \(219P^{-25/24}\) leftover is positive. This is a
  coefficient slip, not a disproof of
  \(K_c\ll P^{1-1/96+\varepsilon}\).
  `J-kernel-cancellation` stays **EXACT — HUMAN PROOF**.
- **Introductory example \(P_0=1.3046380695369\cdot 10^{13}\)
  (COMPUTATIONALLY VERIFIED).**
  First integer with \(54P^{-25/24}\le 0.1P^{-5/6}\).
- **Leftover \(219P^{-25/24}\le 0.1P^{-5/6}\):** first
  \(P_0=1.0817620739800119\cdot 10^{16}\). This is the
  threshold after discarding the illegal \(0.11\) term.
- **\(V\ge 10\lvert f''-\Lambda\rvert\) against the
  three-term error:** first \(P_0=1.258495661293\cdot 10^{12}\).
  If the \(0.1P^{-5/6}\) claim had held, this line would
  be immediate.
- **\(V/S\le 6.7P^{-7/48}\le c_7/2\):** first
  \(P_0=3.918539669348145\cdot 10^{24}\) at the explicit
  \(c_7=1/288\) of the printed triple
  \(\bigl(\tfrac54,\tfrac{11}{8},\tfrac32\bigr)\). This
  is the large ineffective threshold among the lines
  that can hold.
- No exponential sum was evaluated. Paper B is not
  edited.

## Open questions

A writeup repair of the interpolant RHS (any constant
\(>0.11\)) is a Paper B edit, out of this laboratory
branch. The independent human check of Section 5
remains.

## Decision

**PROMOTE** the hole and the \(P_0\) table. The displayed
Step 5b interpolant-error chain is impossible as written;
the introductory example first holds at \(1.30\cdot 10^{13}\);
the \(V/S\le c_7/2\) line first holds at \(3.92\cdot 10^{24}\).
This is not an effectiveness campaign and not a retag of
the kernel. Do not auto-continue.

Best next question: one independent human check of
Paper B Section 5 (the remaining external debt), not
another \(P_0\) census.

## Publication assessment

Status: `EXPLORATORY`. Laboratory number / coefficient
hole only. Not a Paper B edit.
