# Juggler hug-cylinder construction (backward freedom flow)

Status: **EXPLORATORY**

Follow-up to the hug-cylinder realization branch's recorded question.
It is **not** a \(K_3\) attack, not a reopen of the closed
mechanical-lift branch (that was exact single-cell inverse lifts for
cycles; `empty_ooe` was death of cell-following, not of counting),
not a halt theorem, and not a claim that hug cylinders are proved
nonempty at every depth.

## Problem

Is hug-cylinder nonemptiness provable at **every** depth by an
explicit preimage-cylinder construction (existence, not density) —
turning the fixed-depth close of the realization branch from a scan
into a theorem?

## Exact statement

The hug word factors into `OE`/`OOE` blocks: O-runs are \(\le 2\)
because \(2\log_2(3/2)>1\), E-runs are exactly \(1\). The
E-preimage of a single valid state \(y\) is the full interval
\([y^2,(y+1)^2)\), so backward freedom regenerates every block.
Counting harvestable suffix-realizers \(V\) at level scale
\(X=2^\lambda\):

- an E-regeneration multiplies \(V\) by \(\sim X^{1/2}\)
  (\(+\lambda/2\) bits);
- an O-pullback multiplies \(V\) by \(\sim\frac13 X^{-1/3}\)
  (\(-\lambda/3-\log_2 3\) bits).

Per block the flow is **strictly positive**: `OE` nets
\(+5\lambda/12\) bits, `OOE` nets \(+7\lambda/24\) bits. The only
unproved induction steps are hit-count lower bounds for depth-\(\le
2\) nested floor parities on odd-\(x\) windows of length
\(\sim\frac23 X^{1/3}\) — above the van der Corput threshold
\(X^{1/4}\) (for \(f=x^{3/2}/2\),
\(|\sum_H e(f)|\ll HX^{-1/4}+X^{1/4}\) is nontrivial at
\(H=X^{1/3}\)), i.e. short-interval depth-\(\le 2\) statements, not
the \(K_3\) wall (depth \(5\), deterministic shift).

## Current literature

- Hug word block grammar `OE`/`OOE` — **EXACT — LEAN VERIFIED**
  (`WalkChargeWords.lean` hug rule; the grammar is the
  \(2\log_2(3/2)>1\) window arithmetic).
- Hug cylinder filled to depth \(28\) at the \(2^{-L}\) rate on
  \([3,2\cdot 10^8]\) — **COMPUTATIONALLY VERIFIED**
  (realization branch, CLOSE).
- Long-interval parity equidistribution of nested floor powers to
  depth \(\le 4\) with power savings — **EXACT — HUMAN PROOF**
  (Paper B). The lemma needed here is its *short-interval*
  depth-\(\le 2\) analogue.
- Exact single-cell inverse hug lifts die at empty `OOE` cells —
  mechanical-lift branch, CLOSE (`empty_ooe`); consistent with the
  \(w^{-1/9}\) per-anchor hazard measured here, and superseded by
  counting over regenerated intervals.

Project relationship: **PROJECT-SPECIFIC** exponent ledger on top of
KNOWN machinery; the needed analytic lemma is OPEN.

## Branch budget

```text
Mathematical target     is C_L != empty provable for every L by
                        backward induction - concretely: is the
                        freedom flow positive per block, and do the
                        parity hits the induction needs live inside
                        provable windows?
Novelty hypothesis      the block grammar bounds the induction's
                        analytic needs at depth <= 2 on windows
                        X^{1/3} - above the vdC threshold, below the
                        K3 wall; nobody priced the backward flow
Falsifier               generator-chain / pullback death at generic
                        positions, or parity runs exceeding the
                        X^{1/3} working window
Existing machinery      hug letters (Lean rule), gmpy2 exact roots,
                        Paper B depth<=4 (long-interval), the
                        realization scan to depth 28
Maximum Phase-0 scope   one probe: parity-run census 2^20..2^40,
                        OE-pullback survivor census, OOE two-stage
                        hazard census (generic + resonant offsets);
                        no Lean, no Paper edits, no deep search
Promotion criterion     flow confirmed at all scales and a provable
                        route for the window lemma
Stop criterion          flow anomaly at generic positions, or the
                        route reducing to K3-strength statements
```

## Balanced-ternary formulation

Not BT-specific; the flow exponents are the shared \(2\)–\(3\)
multiplicative data (the block mix that makes the scale exponent
neutral is the hug rotation itself).

## Why BT may be relevant

Only through the shared \(2\)–\(3\) structure; no representation
claim.

## Candidate operations / invariants

- **Freedom-flow ledger** (per backward block, at level scale
  \(2^\lambda\)): E-regeneration \(+\lambda/2\) bits, O-pullback
  \(-\lambda/3-\log_2 3\) bits; `OE` \(+5\lambda/12\), `OOE`
  \(+7\lambda/24\) (**OBSERVATION**, exponent arithmetic confirmed
  by census).
- **Working window**: parity hits needed on odd-\(x\) windows of
  length \(\frac23 X^{1/3}\); measured constant-parity runs must
  stay below it (**OBSERVATION**).
- **Resonance hazard**: where \(\sqrt x\) is near-integral, the
  increment \(\lfloor 3\sqrt x\rfloor\) parity locks and runs grow;
  `OOE` pullbacks can die locally (**OBSERVATION**).

## Experiments

Runner: `python -m research.juggler_sequence.hug_cylinder_construction`
(probe `src/research/juggler_sequence/hug_cylinder_construction.py`).
Artifact:
`data/research/juggler/hug_cylinder_construction/summary.json`.
Fast suite:
`tests/research/juggler_sequence/test_hug_cylinder_construction.py`.

Three censuses, all exact integer arithmetic: constant-parity runs
of \(\lfloor x^{3/2}\rfloor\) over odd \(x\) at scales
\(2^{20}\)–\(2^{40}\); `OE`-block pullback survivors on full
regenerated windows at \(2^{16}\)–\(2^{40}\); `OOE`-block two-stage
pullback hazard over \(3000\)-anchor runs at generic and
sqrt-resonant offsets.

## Conjectures

- `juggler_hug_flow_window` (ACTIVE): the short-interval
  depth-\(\le 2\) window lemma; with the positive flow it gives
  \(C_L\ne\emptyset\) for every \(L\).

## Counterexamples

None. The falsifier did not fire at generic positions; the resonant
`OOE` death at \(2^{36}\) (below) is the hazard the lemma's
exclusion clause must carry, not a flow refutation.

## Formalization

None new. The block grammar is already Lean
(`WalkChargeWords.lean`); the flow ledger and window lemma are
unformalized prose/data.

## Results

- **Flow confirmed (COMPUTATIONALLY VERIFIED, classification
  `HUG_FLOW_CONFIRMED`):**
  - parity runs: max constant-parity runs of
    \(\lfloor x^{3/2}\rfloor\) over odd \(x\) are \(58\) at
    \(2^{20}\) up to \(836\) at \(2^{40}\) — always below the
    \(\frac23 X^{1/3}\) working window, with the ratio falling
    \(0.86\to 0.12\); but **above** the naive quadratic-crossing
    budget \(\frac23 X^{1/4}\) at \(2^{36}\) and \(2^{40}\)
    (\(754>341\), \(836>683\)) — the induction genuinely needs the
    \(X^{1/3}\) window, i.e. the vdC-nontrivial regime;
  - `OE` pullbacks: survival rate \(0.4996\)–\(0.50\) on full
    windows, **zero** empty anchors across \(7\) scales;
  - `OOE` pullbacks: generic-offset hits track the
    \(\frac{8/27}{2}w^{-1/9}\) law at \(0.71\)–\(0.82\) of
    prediction at every scale \(2^{16}\)–\(2^{40}\).
- **Resonance hazard isolated:** at the \(2^{36}\) resonant offset
  the swept \(x\approx 2^{32}\) is a perfect square;
  \(\lfloor x^{3/2}\rfloor\) parity locks and `OOE` pullbacks die
  completely (\(0/3000\) against \(\approx 28\) predicted). Any
  all-depth statement must excise or route around sqrt-resonances;
  anchor freedom at generic positions is ample.
- **Negative knowledge — construction cost:** a backward
  *constructor* pays \(\sim X^{1/9}\) anchor pulls per `OOE` block,
  cascading multiplicatively across blocks; no backward search is
  cheaper than the \(2^L\) forward scan. The deepest certified
  witness stays the realization branch's depth \(28\). (The naive
  generator-chain implementation was discarded for this reason.)
- **Route classified:** all-depth nonemptiness reduces to
  `juggler_hug_flow_window` — short-interval depth-\(\le 2\)
  equidistribution with resonance exclusion. This is *not* the
  \(K_3\) wall, but it is a genuine analytic project (Paper B's
  machinery is long-interval), and its payoff is an
  obstruction-existence theorem (extremal descent-free prefixes
  realized at every depth), not descent progress.

## Open questions

- Prove `juggler_hug_flow_window` depth \(1\) (single-`O` hits at
  window \(X^{1/3}\)) by van der Corput / exponent pairs, with an
  explicit resonance exclusion.
- Does the depth-\(2\) statement follow from Paper B's elementary
  long-interval technique localized to windows above \(X^{1/4}\)?

## Decision

**PARK.** The flow ledger is positive per block, the census confirms
every exponent at every measured scale, and the missing lemmas are
precisely identified and recorded (`juggler_hug_flow_window`) —
short-interval depth-\(\le 2\), above the vdC threshold, with a
necessary resonance exclusion the census discovered. The branch does
not close (the route is neither KNOWN nor refuted) and does not
promote now: the payoff is an obstruction-existence theorem while
the lab's frontier questions (cycles, termination) are terminal or
parked behind other walls, and the lemma is a paper-sized analytic
effort. Reopening key: prove the window lemma at depth \(1\); the
flow ledger then makes each further depth a bookkeeping induction.

Best next question: none from this branch — the asymptotic-descent
program's standing targets remain `juggler_asymptotic_descent` and
`juggler_descent_time_log`.

## Publication assessment

Status: **EXPLORATORY**. The freedom-flow ledger and the resonance
hazard are a tight, publishable-quality observation if the window
lemma is ever proved; as of now, a section-length note inside any
future descent-certificate paper.
