# Juggler realization-set geometry

Status: **EXPLORATORY**

Standalone arithmetic layer on the parked word atlas. It is **not** a
Research Engine control-layer experiment, not a reopening of the
closed PE-factor or residual-future branches, and not a claim that
every positive integer reaches 1.

## Problem

What arithmetic geometry of the realizing set \(R_w\) causes a
prefix in the Juggler \(O/E\) trie to become unary?

## Exact statement

For a finite word \(w\) and a bound \(N\),

\[
R_w(N)=\{n\le N:\operatorname{follows}(n,w)\}.
\]

The child sets satisfy \(R_{wb}(N)\subseteq R_w(N)\). The observed
degree \(d(w)\) is the number of nonempty children among \(wO\) and
\(wE\). Keep the quantifiers existential. A missing child under a
scan bound is

\[
\texttt{NOT\_FOUND\_WITHIN\_BOUND},
\]

never a forbidden factor, unless a separate arithmetic certificate
exists. The first rooted holes `EEEEEE`, `EEEEOE`, `EEEOEO` are
classified at least as `SCALE_LIMITED` when they appear as interior
factors.

This says nothing about totality.

## Current literature

- `follows` / `image` / `floorPower` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.Itinerary` and
  `Dynamics`.
- `even_tower_to_one` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.Collapse`.
- Inverse-floor cells `even_cell_iff` / `odd_cell_iff` /
  `odd_cell_unique` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.Cells`.
- Word atlas prefix trie —
  **PARK** as machinery; graph reading in
  [juggler_atlas_graph.md](../research/juggler_atlas_graph.md).
- Word-language arrangement attack —
  **CLOSE** as `JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`.
- Residual-future quotient —
  **CLOSE**. Do not reopen.

Project relationship: **extended**.

## Branch budget

```text
Mathematical target     What geometry of R_w makes a prefix unary?
Novelty hypothesis      inverse-floor cells or scale of R_w force
                        d(w)=1 by an explicit arithmetic rule
Falsifier               unary without monochrome landings; a square
                        amplification law that survives mixed words;
                        only tautological restatements of landing parity
Existing machinery      follows_word, image_after, even_cell,
                        odd_cell_integers, parked atlas continuations
Maximum Phase-0 scope   reproduce atlas facts; exact R_w on n<=4000
                        then n<=1e5; child split; min-realizer laws;
                        root vs interior for the three first holes
Promotion criterion     an explicit A(w),B(w) or cell rule for d(w)=1
                        that is not landing-parity restated
Stop criterion          only scan-bound tautologies; PE-factor or
                        residual-quotient reopen; automaton; halt claim
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Nested realizing sets \(R_{wb}\subseteq R_w\) —
  **EXACT — HUMAN PROOF** from `follows`
- Child split by parity of \(T_w(n)\) —
  **EXACT — HUMAN PROOF**
- \(m(E^r)=2^{2^{r-1}}\) —
  **EXACT — HUMAN PROOF**, Lean `even_tower_to_one`
- \(m(wE)\ge m(w)^2\) for mixed words —
  **REFUTED** on `OOE` / `OO`
- First rooted holes as forbidden factors —
  **REFUTED**; they are `SCALE_LIMITED` and interior-realized
- Unary iff landing parity of \(T_w(R_w)\) is monochrome —
  **EXACT — HUMAN PROOF** (definitional on the exact split)

## Experiments

- Probe: `research.juggler_sequence.realization_geometry`
- Diagnostic window: \(n\le 4000\), \(k\le 12\)
- Confirm window: \(n\le 10^5\), \(k\le 12\)
- Atlas: `wa-20260827T200310Z-cuda-k20-n100000000`
- Records: [juggler_realization_geometry.md](../research/juggler_realization_geometry.md)
- Tests: `tests/research/juggler_sequence/test_realization_geometry.py`

## Conjectures

None opened in `conjectures/`.

## Counterexamples

- “`m(wE)\ge m(w)^2` after an odd letter.” False: `OOOE` has
  \(m(\texttt{OOOE})=m(\texttt{OOOOE})=3\); `OEEE` has
  \(m=7\) and \(m(\texttt{OEEEE})=41<49\).
- “A length-6 even-ish word absent as a rooted prefix is forbidden.”
  False: `EEEEEE` occurs inside \(2906\) length-20 realized prefixes.
- “Unary corridors never regain two children.” False: \(52\) returns
  in the confirm window, and \(5\) atlas `EE…` parents thaw.

## Formalization

None added. Certification uses `Collapse.lean` and `Cells.lean`.
No `sorry`. No automaton.

## Results

Phase 0 is recorded in
[juggler_realization_geometry.md](../research/juggler_realization_geometry.md).
The exact child rule is landing parity of \(T_w(R_w)\). Naive
square amplification is special to the even tower. The first holes
are `SCALE_LIMITED`. No extra low-complexity interval predicate
beyond landing parity survived the diagnostic and confirm windows.

## Open questions

The leftover atlas question is unchanged: is there any arithmetic,
other than the integer \(y\) itself, that decides whether a
persistent residual landing stays odd-to-odd? This branch does not
answer it. A tighter cell description of \(R_w\) itself — not of
\(d(w)\) — remains open and is not automatically the next phase.

## Decision

**PARK**. Landing parity explains \(d(w)\) exactly and the root /
interior split is real, but both are already implied by `follows` /
`image` plus even-scale. The square law does not lift past odd
letters. Do not promote a restatement. Do not reopen PE factors or
residual quotients. Do not pursue termination.

Best next question: is there any arithmetic, other than the integer
\(y\) itself, that decides whether a persistent residual landing
stays odd-to-odd?

## Publication assessment

Status: `EXPLORATORY`. A realizing-set reading of the parked atlas,
not a paper candidate and not a Juggler totality result.
