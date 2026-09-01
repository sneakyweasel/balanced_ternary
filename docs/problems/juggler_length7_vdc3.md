# Juggler length-7 isolated chirps (vdC III)

Status: **PROMOTE** (isolated monomials only). Theorem X and
density \(57/64\) stay **CONJECTURE**. Paper B stays frozen at
\(13/16\).

Phase-35 desk estimate of the two Phase-34 chirps. Child of
[juggler_engine_harvest.md](juggler_engine_harvest.md). Not a
\(K_3\) attack and not a Paper B edit.

## Problem

Lemma 3.3 is worse than trivial on \(e(un^{27/16})\) and
\(e(Cn^{3/2})\). Does one further \(A\)-process, feeding
Lemma 3.3, close those isolated sums inside \(P^{23/24}\)
without a new decoration class?

## Exact statement

For odd \(n\sim P\) and \(1\le\lvert k\rvert\le P^{1/24}\),
are
\[
\Bigl\lvert\sum e(un^{27/16})\Bigr\rvert\ll P^{23/24},
\qquad
\lvert u\rvert\le P^{85/96},
\]
and
\[
\Bigl\lvert\sum e(Cn^{3/2})\Bigr\rvert\ll P^{23/24},
\qquad
\lvert C\rvert\le P^{103/96},
\]
and do the leftover phases sit in (D1) / (D3) or get
dominated by \(f'''\)?

## Current literature

- Paper B Lemma 3.3 and the displayed \(A\)-process —
  **EXACT — HUMAN PROOF**. **reproduced**.
- Phase-1 third-derivative test on \(\theta\)-frozen short
  cells — interval length at \(\lambda_3^{-1/3}\), useless.
  **independent** (different setting).
- Phase-9 per-run third-derivative on mixed pieces —
  summed to the trivial bound; repaired by targeted
  differencing. **independent** (mixed, not isolated).
- Theorem T passenger slogan
  (`J-length7-passenger-theorem-t`) — **REFUTED**.
  **reproduced**.
- Lemma X4 / \(\alpha=33/32\) \(W\)-family —
  **EXACT — HUMAN PROOF**. **independent**.
- Theorem X (`J-depth7-engine-contracting`) —
  **CONJECTURE**. **extended** by an isolated-sum theorem
  that does not close the inventory.

## Branch budget

```text
Mathematical target     Do vdC III close ∑ e(u n^{27/16}) and
                        ∑ e(C n^{3/2}) inside P^{23/24}
                        without a new decoration class?
Novelty hypothesis      Lemma 3.3 dies because |f''| is large;
                        one A-process may still give a 1/6-saving.
Falsifier               N |f'''|^{1/6} exceeds P^{23/24}, or
                        lower terms force a new third-derivative
                        decoration class.
Existing machinery      Paper B A-process + Lemma 3.3;
                        Phase 34 ranges; Lemmas X1, X4.
Maximum Phase-0 scope   Desk estimate of the two isolated
                        chirps plus a decoration check.
                        No Theorem X retag unless both close
                        with existing classes only.
                        No length-8, no Paper B, no new CLI.
Promotion criterion     Both isolated sums ≪ P^{23/24}, and
                        leftover phases sit in (D1)/(D3) or
                        are dominated by f'''.
Stop criterion          A chirp overshoots, or decorations
                        need a new class (PARK X).
                        Machinery gravity.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- Isolated \(\sum e(un^{27/16})\) and \(\sum e(Cn^{3/2})\)
  (`J-length7-vdc3-chirps`) — **EXACT — HUMAN PROOF**
- Reduction \(w^{3/2}=n^{27/16}+O(n^{3/16}\theta_2)\) as a
  (D1)/(D3) decoration — **REFUTED** as a method (spawned
  amplitude exceeds \(n\))
- “Theorem T applies as a passenger”
  (`J-length7-passenger-theorem-t`) — **REFUTED**
- Theorem X / density \(57/64\) — **CONJECTURE**
- Length-8 \(E'\) — **CONJECTURE** (untouched)
- \(K_3\) bound — **PARK** (BB/GG/JJ)

## Experiments

No new runner. Exponent seals in
`tests/research/juggler_sequence/test_two_step_parity.py`
(`test_length7_vdc3_chirps`).

## Conjectures

None new. `J-depth7-engine-contracting` and
`J-seven-step-descent-density` stay conjectures.

## Counterexamples

None for the isolated sums. The counterexample to closing
Theorem X by this door is the spawned sawtooth of amplitude
\(\lvert u\rvert n^{3/16}>n\).

## Formalization

None added.

## Results

- **Lemma X5 (EXACT — HUMAN PROOF,
  `J-length7-vdc3-chirps`).**
  Isolated monomials \(\ll P^{535/576}\) uniformly in the
  Phase-34 ranges, and \(\ll P^{177/192}\) at the natural
  sizes. Both inside \(P^{23/24}\). Proof: lemma Part XX,
  one \(A\)-process plus Lemma 3.3.
- The \(w^{3/2}\to n^{27/16}\) reduction is not a
  decoration. Isolated \(e(un^{27/16})\) is not the
  \(\theta_p\) inventory sum \(e(uw^{3/2})\).

## Open questions

Answered in Phase 37
([juggler_length7_x3_carry.md](juggler_length7_x3_carry.md)):
X3 plus Q/R3 does not close \(e(uw^{3/2})\). Remaining:
the integer-\(w\) block at \(\xi\asymp n^{45/32}\).
Length 8 stays behind \(E'\). Do not reopen
\(e(uw^{3/2})\).

## Decision

**PROMOTE** the isolated chirp bounds. Both named sums
close inside \(P^{23/24}\) by existing Paper B tools. The
promotion criterion’s second half fails: leftover phases
do not sit in (D1)/(D3) and are not dominated by
\(f'''\). Do not retag Theorem X. Do not write Lemma 3.11.
Best next question: the actual \(\theta_p\) sum
\(e(uw^{3/2})\) on X3-runs plus the Q/R3 carry.

## Publication assessment

Status: `EXPLORATORY` (laboratory exact bound; not a
density move). Not a Paper B edit. Paper B already
refuses densities beyond \(13/16\).
