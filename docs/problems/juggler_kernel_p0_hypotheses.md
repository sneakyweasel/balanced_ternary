# Juggler kernel \(P_0\) hypotheses

Status: **PROMOTE** (laboratory \(P_0\) table). Paper B stays
frozen; \(P_0\) remains ineffective in print. Not a \(K_3\)
attack and not a decoration-budget census.

Phase-0 check of the five printed Lemma 3.7 / Lemma 5.2
hypotheses in Paper B §5. Child of
[juggler_two_step_parity.md](juggler_two_step_parity.md).

## Problem

Paper B claims every numerical margin in Section 5 only for
\(P\ge P_0\) with \(P_0\) absolute and ineffective, and never
computes that threshold. Do the five printed Lemma 3.7 /
Lemma 5.2 conditions hold, and what is the first working
\(P_0\)?

## Exact statement

On the standing range (C1)–(C3) of Paper B §5, at which
first integer \(P\) do all five printed comparisons hold,
and does any fail for every feasible \(P\)?

- (3a) \(T=P^{1/2}/(2h_1)\ge 8(1+|B|)\) with
  \(B\sim kh_2P^{1/8}\) in the (E4) box
- Lemma 5.2 Stage 3 (s2)
  \(T=P^{1/2}\ge 8(1+2.25P^{1/4})\)
- Lemma 5.2(ii) \(th_3\le P^{1/2}\) at
  \(H_3=\lceil t^{1/3}P^{1/12}\rceil\)
- freeze-window count of \(B=\Delta_2c(n+d_1)\) versus
  \(2kh_2P^{1/4}+1\)
- frozen-floor runs of \(\lfloor F_{\boldsymbol\kappa}(X)\rfloor\)
  versus \(22(|j|+1)P^{3/4}\), and \(|G'|<1\)

Exponential sums are not evaluated.

## Current literature

- Paper B Lemma 3.7, Lemma 5.1(iii), Lemma 5.2, Theorem 5.3
  (`J-kernel-cancellation`) — **EXACT — HUMAN PROOF**.
  **reproduced** (the printed hypotheses only).
- The note states \(P_0\) is ineffective and does not compute
  it. **extended** by a laboratory number.
- Step 5b \(54P^{-25/24}\le 0.1P^{-5/6}\) is the known large
  source of ineffectivity. **independent** (out of scope).
- Decoration-and-mode budget census — **independent** (item 1
  of the same punch list; not this branch).
- Scale-invariant copy of Theorem R — **REFUTED**. Not
  re-tested.

## Branch budget

```text
Mathematical target     What is the first P at which the five printed
                        Lemma 3.7 / Lemma 5.2 hypotheses hold on the
                        standing range, and does any fail for every
                        feasible P?
Novelty hypothesis      The paper never computes P_0. A failure at
                        every feasible P is a hole of the Phase-26
                        species (cited lemma hypotheses not met). A
                        first working P_0 is new laboratory knowledge.
Falsifier               One printed comparison false for all P up to
                        the search ceiling, or a realized window/run
                        count above the printed inventory.
Existing machinery      Paper B Lemmas 3.7, 5.1(iii), 5.2; standing
                        (C1)–(C3) and (E4); branch_freeze_scan;
                        _eighth_scaled in two_step_parity.py.
Maximum Phase-0 scope   One thin probe + fast tests + child dossier.
                        Algebraic P_0 search; windowed inventories;
                        one optional full-block count at P=10^8.
                        No sums, no Paper B edit, no Lean, no CLI,
                        no items 1/2/4, no Step 5b.
Promotion criterion     A concrete first P_0 table, or a named hole.
Stop criterion          After the table (or hole). Machinery gravity.
```

## Balanced-ternary formulation

None required. The objects are the printed real inequalities
and integer run counts on odd \(n\sim P\).

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Printed-slack first \(P_0\) at the continuous majorants
  \(h_1\le P^{1/48}\), \(k,h_2\le P^{1/24}\),
  \(t\le 4P^{1/16}\) — **COMPUTATIONALLY VERIFIED**
- Integer-corner first \(P_0\) on (C1)–(C3) —
  **COMPUTATIONALLY VERIFIED**
- Freeze-window and frozen-branch-run inventories —
  **COMPUTATIONALLY VERIFIED**
- Step 5b large \(P_0\) — **OBSERVATION** (out of scope;
  not recomputed as a claim)
- Kernel bound, Paper B text — untouched

## Experiments

- Probe: `research.juggler_sequence.kernel_p0_hypotheses`
- Record: [summary.json](../../data/research/juggler/kernel_p0_hypotheses/summary.json)
- Tests: `tests/research/juggler_sequence/test_kernel_p0_hypotheses.py`

Algebraic search is exact in floats at the printed exponents.
Inventories walk odd \(n\in(P,2P]\) (or a prefix). The
\(P=10^8\) census is a probe, not a fast-suite test.

## Conjectures

None new.

## Counterexamples

None. The five printed comparisons hold past a finite
\(P_0\); no comparison failed at every feasible \(P\).

## Formalization

None added. Packaging an ineffective \(P_0\) in Lean is
machinery gravity.

## Results

Filled after the Phase-0 census. See the Decision.

## Open questions

The five Lemma 3.7 / Lemma 5.2 lines are not the source of
the writeup’s large ineffective \(P_0\). That remains
Step 5b (\(54P^{-25/24}\le 0.1P^{-5/6}\)), which this
branch does not compute.

## Decision

**PROMOTE** the laboratory \(P_0\) table. Justification
and the best next question are filled after the census
in the same section below.

Best next question: none from this branch until the
census is recorded.

## Publication assessment

Status: `EXPLORATORY`. Laboratory number only. Not a
Paper B edit.
