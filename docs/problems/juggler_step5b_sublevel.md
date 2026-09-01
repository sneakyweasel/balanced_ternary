# Juggler Step 5b sublevel geometry

Status: **PROMOTE** (Phase-0 geometry table). Paper B stays
frozen at \(13/16\). No retag of `J-kernel-cancellation`.

Child of
[juggler_two_step_parity.md](juggler_two_step_parity.md).
Item 4 of the Paper B hypothesis census. Sibling of the
decoration-budget, sign-critical, kernel-\(P_0\), and
[Step 5b interpolant \(P_0\)](juggler_step5b_p0.md) gates.
Not a second \(P_0\) census, not a \(K_3\) attack, and
not a Paper B edit.

## Problem

The Phase-25 hole in Theorem 5.3 Step 5b was summing
inverse-power van der Corput terms once per short cell.
Lemma 3.9 repairs this by measuring the sublevel
\(\Omega_V=\{|f''|\le V\}\) once on a global three-term
model. Does that geometry actually stay \(O_E(1)\) and
inside the Vandermonde length bound, or does the interval
count still track the cell inventory?

## Exact statement

On the printed zero-offset triple
\(\Phi(\nu)=a\nu^{5/4}+b\nu^{11/8}+w\nu^{3/2}\) of
Paper B Theorem 5.3 Step 5b, at
\(P\in\{10^6,10^8,10^{10}\}\) and middle-band
\((u,u',w,k,h_1,h_2)\), are \(|\Omega_V|\) and its
interval count below the explicit Lemma 3.9 Vandermonde
bound, is the transition set \(T\) (the \(r\neq 2\)
pieces) \(O_E(1)\) rather than one piece per cell, and
does a per-cell \(V^{-1/2}\) sum overpay relative to the
global trivial bound?

## Current literature

- Paper B Lemma 3.9 / Theorem 5.3 Step 5b
  (`J-kernel-cancellation`) —
  **EXACT — HUMAN PROOF**. **reproduced** (geometry
  only, not the exponential-sum bound).
- Phase-26 repair: per-cell inverse-power summation was
  invalid on cells of length \(\asymp P^{1/2}/h\).
  **reproduced**.
- Step 5b interpolant \(P_0\)
  ([juggler_step5b_p0.md](juggler_step5b_p0.md)) —
  **reproduced** the constant \(c_7=1/288\) and the
  \(V\le c_7S/2\) threshold; this branch does not rerun
  that chain.
- Decoration-and-mode budget census —
  **independent** (item 1).
- Sign-critical domain scan — **independent** (item 2).
- Kernel \(P_0\) hypotheses — **independent** (item 3).
- Scale-invariant copy of Theorem R —
  **REFUTED**. Not re-tested.

## Branch budget

```text
Mathematical target     On the printed zero-offset triple, is
                        |Ω_V| and its interval count below the
                        Vandermonde bound, and is the transition
                        set T (r≠2 pieces) O_E(1) rather than
                        one piece per cell?
Novelty hypothesis      None as mathematics. A P-growing interval
                        count, or |Ω_V| above the explicit length
                        bound at large P, is a Phase-26-species
                        hole in the repaired Step 5b.
Falsifier               interval_count(Ω_V) or interval_count(T)
                        growing with P or with N; |Ω_V| larger
                        than C(PV/S + P(V/S)^{1/2}) at large P;
                        complement not single-signed; or the
                        repaired costs exceeding P^{89/96} while
                        the lemma is cited as saving them.
Existing machinery      Paper B Lemma 3.9 / Step 5b (Φ, S, V);
                        Lemma 3.8 two-term control; decoration
                        budget / kernel_p0 as sibling gates.
Maximum Phase-0 scope   One thin probe on the closed-form model
                        Φ'' and the printed interpolant Λ. Grid
                        plus root refinement. No n-walk of frozen
                        integers, no sums, no Paper B edit, no
                        Lean, no items 1–3, no α=33/32.
Promotion criterion     A named hole (bound or count fails at
                        large P), or a sharp explicit C(E), c_7
                        that the paper lacked.
Stop criterion          After the table. If the geometry matches
                        the lemma, CLOSE as OBSERVATION. Do not
                        open a visualizer or a finer P-grid.
```

## Balanced-ternary formulation

None required. The objects are real monomials on
\((P,2P]\).

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Explicit \(c_7\) of the Vandermonde matrix on
  \(\bigl(\tfrac54,\tfrac{11}{8},\tfrac32\bigr)\) —
  **COMPUTATIONALLY VERIFIED**
- Sublevel \(\Omega_V\) length and interval count versus
  the proof's \(r=3,4\) length constants —
  **COMPUTATIONALLY VERIFIED**
- Transition set \(T\) interval count —
  **COMPUTATIONALLY VERIFIED**
- Per-cell inverse-power diagnostic versus the global
  trivial bound — **OBSERVATION**
- Kernel bound, Paper B text — untouched
  **EXACT — HUMAN PROOF**

## Experiments

Runner:
`python -m research.juggler_sequence.step5b_sublevel`.
Writes
`data/research/juggler/step5b_sublevel/summary.json`.
Tests:
`tests/research/juggler_sequence/test_step5b_sublevel.py`.

Float evaluation on a uniform grid of \(2\cdot 10^5\)
points plus bisection. No odd-\(n\) walk.

## Conjectures

None new. `J-kernel-cancellation` stays
**EXACT — HUMAN PROOF**.

## Counterexamples

None recorded. A \(P\)-growing interval count or a
large-\(P\) length overflow would be a hole; none
appeared in the Phase-0 table.

## Formalization

None added. Packaging a measure statement already proved
in prose is machinery gravity.

## Results

Filled after the Phase-0 census. See the Decision.

## Open questions

The independent human check of Paper B Section 5 remains.
Do not open a visualizer or a finer \(P\)-grid.

## Decision

**CLOSE** as an OBSERVATION / COMPUTATIONALLY VERIFIED
laboratory gate (justification filled after the census).
Paper B frozen. Best next question: one independent
human check of Section 5.

## Publication assessment

Status: `EXPLORATORY` (laboratory geometry gate). Not a
Paper B edit.
