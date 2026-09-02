# Juggler length-8 remainder discard

Status: **PROMOTE** (remainder rate only). Theorem AA and
density \(29/32\) stay **CONJECTURE**. Paper B stays at
the imported length-5 harvest (\(7/8\)); length 8 is
not a paper claim.

Phase-40 desk classification of the Phase-26 \(E'\)
hole. Child of
[juggler_engine_harvest.md](juggler_engine_harvest.md).
Not a \(K_3\) attack and not a Paper B edit. Not another
rewriting of \(e(uw^{3/2})\).

## Problem

Lemma AA1 writes a seven-level Taylor chain
\(X_7=n^{243/128}-\sum_i B_i\theta_i+E\) with
\(\lvert E\rvert<1\) for \(n\ge 51\). Phase 26 discarded
\(E\) at that crude size (Vaaler cost \(J_8P\)) or asked
for \(E'\) if \(E\) is kept. Do the AA1 envelopes give a
rate that makes discard legal, or is \(E'\) too large to
discard and too wild to keep?

## Exact statement

On each quartet parent, is \(\lvert E\rvert\ll n^{-\alpha}\)
for some \(\alpha>13/384\), so that
\(k\lvert E\rvert\to 0\) on \(k\le P^{13/384}\) and the
Vaaler cost of \(e(kE)-1\) sits inside \(P^{23/24}\)? If
\(E\) is kept, is \(\lvert E'\rvert<1\), or does a new
decoration class appear?

## Current literature

- Lemma AA1 (`eighth_letter_chain_check`) —
  **EXACT — HUMAN PROOF**. Subcritical coefficients;
  envelopes written, rate not named. **reproduced**.
- Theorem AA (`J-depth8-engine-quartet`) —
  **CONJECTURE**. The \(E'\) hole was one named
  withdrawal; Theorem X is the other. **extended**.
- Length-7 remainder engine
  (`J-length7-remainder-engine`) — **EXACT — HUMAN
  PROOF**. The sibling growing remainder, kept as a
  phase. **independent**.
- Theorem X — **CONJECTURE**. Untouched. **independent**.
- Crude \(\lvert E\rvert<1\) discard — dead method
  (Phase 26). **reproduced**.

## Branch budget

```text
Mathematical target     Can E' be controlled so |E|<1
                        becomes a usable length-8 remainder,
                        or does the missing derivative kill
                        the quartet?
Novelty hypothesis      Contraction and subcritical
                        eighth-letter coefficient already
                        stand; E' may be an engine or a
                        decaying Taylor term, not a slogan.
Falsifier               |E'| too large to discard and too
                        wild to keep (grows, or E''>1, or
                        a new decoration class).
Existing machinery      Lemma AA1; eighth_letter_chain_check;
                        Phase 29 remainder-engine pattern;
                        depth8_chains_subcritical=True.
Maximum Phase-0 scope   Desk classification of E and E'
                        on the four length-8 words. No
                        Theorem X retag, no e(u w^{3/2})
                        rewrite, no Paper B edit, no new CLI.
Promotion criterion     E' sits in an existing class with
                        displayed room, or a named exact
                        remainder estimate.
Stop criterion          A load-bearing margin dies
                        (PARK AA); machinery gravity.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. The 2-adic / BT bridge stays closed.

## Candidate operations / invariants

- AA1 envelopes, leading term
  \(\tfrac{297}{512}x_4^{-5/16}\asymp n^{-45/128}\) —
  **EXACT — HUMAN PROOF** (Lemma AA2)
- Crude \(\lvert E\rvert<1\) discard (cost \(J_8P\)) —
  dead method (not a new `REFUTED` row)
- Theorem AA / density \(29/32\) — **CONJECTURE**
- Theorem X / density \(57/64\) — **CONJECTURE**
- \(K_3\) bound — **PARK** (BB/GG/JJ)

## Experiments

No new CLI. Seals in
`research.juggler_sequence.two_step_parity`:
`eighth_remainder_rate_scan` (envelope with no slack;
size ratio \(n^{45/128}\); drift ratio \(n^{29/128}\)).
Tests:
`tests/research/juggler_sequence/test_two_step_parity.py`
(`test_length8_remainder_discard`).

## Conjectures

None new. `J-depth8-engine-quartet` and
`J-eight-step-descent-density` stay conjectures.

## Counterexamples

None for the counts. The method counterexample is the
crude \(\lvert E\rvert<1\) discard, already named in
Phase 26: cost \(P^{1+13/384}\).

## Formalization

None added.

## Results

- **Lemma AA2 (EXACT — HUMAN PROOF,
  `J-length8-remainder-discard`).**
  On each quartet parent,
  \(\lvert E\rvert\ll n^{-45/128}\) and
  \(\lvert E'\rvert\ll n^{-29/128}<1\). Discarding
  \(e(kE)-1\) on \(k\le P^{13/384}\) costs
  \(\ll P^{131/192}\). Proof: lemma Part XXIII.

## Open questions

Answered in Phase 41
([juggler_harvest_counting.md](juggler_harvest_counting.md)):
the harvest counting program is laboratory-terminal.
Do not reopen \(E'\) and do not reopen the length-7
sixth-letter rewrites.

## Decision

**PROMOTE** the remainder rate. \(E\) decays; discard is
legal at \(P^{131/192}\). The crude \(\lvert E\rvert<1\)
discard stays dead. Do not retag Theorem AA. Best next
question: the harvest counting program is blocked only
by Theorem X — is there an outside-toolkit attack, or is
that door terminal?

## Publication assessment

Status: `THEOREM` (laboratory). Not a Paper B edit.
Paper B already refuses densities beyond \(7/8\).
