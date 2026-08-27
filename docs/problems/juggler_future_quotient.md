# Juggler residual future-quotient

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1.

## Problem

After the Word Atlas PE-factor scale-up, the leftover question is
arithmetic, not linguistic: does bounded residual-future behaviour
admit a nontrivial finite-information quotient, or does
distinguishability force progressively finer arithmetic precision?

This is a state-minimization measurement. It is not an invariant hunt
and not a finite-state automaton.

## Exact statement

Keep the existing successor. Do not replace it with a state machine.

\[
\mathrm{ResidualStep}(x,y)
\iff
\exists\,a,b\ (b\ge 1\ \wedge\ x\ \text{follows}\ O^aE^b\ \wedge\ T_{O^aE^b}(x)=y).
\]

From a residual landing \(x\), write \(\mathrm{Future}_H(x)\) for the
length-\(H\) observation word whose letters are the existing
independent labels

\[
(\text{exists},\;\mathrm{residual\_class},\;\text{odd-odd},\;\text{persistent},\;\text{expanding}).
\]

This is **bounded future equivalence at horizon \(H\)**, not
Myhill–Nerode equivalence and not a language theorem.

A projection \(S\) is sufficient at \(H\) on a sample \(Y\) when

\[
S(x)=S(y)\implies \mathrm{Future}_H(x)=\mathrm{Future}_H(y).
\]

The 2-adic precision demand on that sample is

\[
k^*(H)=1+\max\bigl\{v_2(x-y):x,y\in Y,\;\mathrm{Future}_H(x)\ne\mathrm{Future}_H(y)\bigr\},
\]

or \(>k_{\max}\) if a class modulo \(2^{k_{\max}}\) still splits.

This says nothing about totality. Do not add `ResidualState`. Do not
extend `ResidualStep`. Do not reopen the PE-factor branch.

## Current literature

- Residual-state sufficiency — **CLOSE** as `RESIDUAL_STATE_NEEDS_X`.
  Incoming \((A,G,\mathrm{cell})\) is inert history. Intrinsic \(V\)
  is a function of \(y\).
- ResidualStep \(\sim_H\) census — **CLOSE** as `RESIDUAL_MN_REPACK`.
  \(Q_H\) plateaus below \(\lvert Y\rvert\) only because some landings
  share a complete observation word to HALT.
- Landing valuation — **CLOSE** as `LANDING_VALUATION_IS_Y_MOD_8`.
  Residue modulo \(8\) does not decide PE continuation.
- Word-language / PE-factor grammar —
  **CLOSE** as `JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`. The atlas
  scale-up found no extra PE-run factor law. Do not reopen it.
- Word atlas — **PARK** as machinery.

Project relationship: **extended**. The leftover after those CLOSEs is
whether listed arithmetic projections predict \(\mathrm{Future}_H\),
and whether \(k^*(H)\) grows.

## Branch budget

```text
Mathematical target     On residual landings, which listed arithmetic
                        projections determine Future_H for H<=6, and
                        does k*(H) grow with H?
Novelty hypothesis      A compact S (not exact y) predicts next-step
                        residual labels on a substantial sample, or
                        k*(H) is a genuine precision hierarchy.
Falsifier               Every listed projection except exact y has a
                        small H=1 separator, leftover multi-y fibers
                        are shared HALT words, and k*(H) is a window
                        rewrite of RESIDUAL_STATE_NEEDS_X /
                        RESIDUAL_MN_REPACK.
Existing machinery      residual_excursion, classify_step,
                        residual_class, intrinsic_V, residual_minimize
                        traces, landing_valuation.v2
Maximum Phase-0 scope   H<=6; odd-odd residual landings n<=4000;
                        optional atlas PE starts n<=1e5 (cap);
                        listed projections only. No GPU, no new
                        atlas tables, no BT features, no Lean, no
                        automaton, no realization-boundary grammar.
Promotion criterion     STATE_QUOTIENT_GREEN or a surviving
                        k*(H) hierarchy that is not a halt-word
                        certificate.
Stop criterion          All no-y projections separate at H=1;
                        only exact y is sufficient; ResidualState.lean;
                        PE-factor reopen; GPU census; halt.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. Level-C BT features are out of Phase-0 scope.

## Candidate operations / invariants

- `Future_H` from existing labels —
  **OBSERVATION** (experimental object; 6 classes at \(H=1\))
- exact \(y\) —
  sufficient by construction; leftover same-future pairs are
  overdescription
- \(y\bmod 8\), \(v_2(3y+1)\) predict \(\mathrm{Future}_1\) —
  **REFUTED**; smallest pair \(1,9\)
- \(y\bmod 2^{16}\) predicts \(\mathrm{Future}_1\) on the
  atlas-enriched sample —
  **REFUTED**; pair \(33\) and a PE landing congruent modulo \(2^{16}\)
- intrinsic \(V\) is a compact quotient of \(y\) —
  **REPARAMETERIZATION** of the next ResidualStep at \(H=1\);
  **REFUTED** as a multi-step state at \(H=6\) by \(9,49\)
- \(k^*(H)\) grows with \(H\) on \(n\le 80\) —
  **REFUTED**; \(k^*=9\) for every \(H\le 6\)
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.future_quotient`
- Records: [juggler_future_quotient.md](../research/juggler_future_quotient.md),
  [juggler_future_quotient.json](../research/juggler_future_quotient.json)
- Dataset: `data/research/juggler/future_quotient/`
- Tests: `tests/research/juggler_sequence/test_future_quotient.py`

Do not launch a GPU pair-search or new atlas tables in Phase-0.
Do not inspect `EEEEEE` / `EEEEOE` / `EEEOEO` as a grammar.

## Conjectures

None opened.

## Counterexamples

- “\(y\bmod 8\) determines \(\mathrm{Future}_1\)”: \(1\) and \(9\).
- “\(v_2(3y+1)\) determines \(\mathrm{Future}_1\)”: \(1\) and \(9\).
- “\(y\bmod 2^{16}\) determines \(\mathrm{Future}_1\) on the
  atlas-enriched sample”: \(33\) versus
  \(573141612728625270488952931933108109345\).
- “intrinsic \(V\) is a multi-step quotient”: \(9\) and \(49\) share
  \(\mathrm{Future}_1\) and split at \(H=2\).
- “incoming history / a new scalar energy”: not tested; closed
  branches stay closed.

## Formalization

None added. `ResidualStep` stays unchanged. No `ResidualState.lean`.
No `sorry`.

## Results

Classification **FUTURE_QUOTIENT_REPACK**, with secondary
**STATE_QUOTIENT_COUNTEREXAMPLE** and **STATE_COMPLEXITY_PARK**.

On odd-odd residual landings from \(n\le 80\) there are \(30\)
distinct \(y\). Label \(Q_H\) is

\[
1,6,11,12,12,12,12
\]

and plateaus from \(H=3\) on HALT fibers. \(k^*(H)=9\) for every
\(H\le 6\), witnessed by \(243\) and \(1523\).

On the Phase-0 sample — those landings plus \(4000\) atlas
`PE_CERTIFIED` starts, \(|Y|=6004\) — label \(Q_H\) is

\[
1,6,18,54,158,393,769
\]

with \(2154\) capped traces. This is computationally observed class
growth up to \(H=6\), not a finite-state theorem. Every listed
arithmetic projection of \(y\) has an \(H=1\) separator.
`residual_V` predicts \(\mathrm{Future}_1\) because it *is* the next
ResidualStep vector, and it splits by \(H=6\).

No `ResidualState.lean`. `ResidualStep` is unchanged. No GPU
pair-search and no new atlas tables were added.

## Open questions

Object C — a global \(\sum\rho\) bound in \((n,\text{word
statistics})\) — stays recorded, not opened. Do not invent another
scalar projection. Do not reopen the PE-factor branch.

## Decision

**CLOSE** the future-quotient Phase-0 as `FUTURE_QUOTIENT_REPACK`.
The listed arithmetic signatures do not predict bounded residual
futures. The only apparent compression is a rewrite of the next
ResidualStep or a shared HALT word. Do not add Lean. Do not build
an automaton. Do not claim termination.

Best next question: a global \(\sum\rho\) bound in
\((n,\text{word statistics})\) — object C — not another residual
relation and not another modulus.

## Publication assessment

Status: `EXPLORATORY`. A negative precision/quotient census, not a
paper candidate and not a Juggler totality result.
