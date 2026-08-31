# Juggler cycle-finance budget optimization

Status: **EXPLORATORY**

Refinement of
[juggler_cycle_finance.md](juggler_cycle_finance.md), not a new
paper. It asks whether minimum uniqueness, odd-run type, and the
cycle maximum force a strictly smaller length-only error budget
than parity finance on \(\mathcal E_{\mathrm{par}}(10^6)\). Not a
halt theorem, not a leftover-word census, not a floor raise, and
not a Paper A edit.

## Problem

Parity finance charges every valley at the `CycleMin` start \(n\).
A cycle cannot put an `OE`-start at \(n\): the next state is even
and below \(n^2\). Does the exact transition geometry — unique
visit of \(n\), the `OE`/`OO` split forced at \(o_{\min}\), and a
bound on the maximum — cut the global floor-error sum enough to
shrink the leftover set?

## Exact statement

**\(n\)-circuit even cap (EXACT — HUMAN PROOF).**
A `CycleMin` circuit starting at \(n\) with \(k\) odds and
\(\ell\) evens lands at most \(n^{3^k/2^{k+\ell}}\) (floors only
make the landing smaller). The landing is \(\ge n\) only if
\(3^k\ge 2^{k+\ell}\). In particular \(k=1\) is impossible from
\(n\), and a \(k=2\) circuit can take only \(\ell=1\) (`OOE`).

**`OE`-start height (EXACT — HUMAN PROOF).**
A length-1 odd-run is followed by an even state, so
`cycleMin_even_ge_sq` gives \(T(v)\ge n^2\), hence
\(v^3\ge n^4\). The least such odd \(v\) is `oe_start_min(n)`.

**Run-type packing (EXACT — HUMAN PROOF).**
At \(o=o_{\min}(L)\) one has \(o-e<e\), so every internal odd can
sit at \(t=\lfloor n^{3/2}\rfloor\). The largest number of
\(n\)-valleys compatible with the even cap is \(o-e\) copies of
`OOE`. The remaining \(2e-o\) circuits are `OE` from
`oe_start_min(n)`. Unique visit of \(n\) (prefix return) puts the
other \(o-e-1\) low valleys at \(n+2\). Evens stay at \(n^2\).
Hence

\[
\sum_i\frac1{x_i\ln x_i}
\;\le\;
\frac{1}{n\ln n}
+\frac{o-e-1}{(n+2)\ln(n+2)}
+\frac{2e-o}{v\ln v}
+\frac{1}{t\ln t}
+\frac{o-e-1}{t_+\ln t_+}
+\frac{e}{2n^2\ln n},
\]

where \(v=\)`oe_start_min(n)` and \(t_+=T(n+2)\). This is
strictly smaller than the parity sum whenever \(2e-o>0\). Sending
the maximum \(M\to\infty\) removes one even term and does not
change the valley packing.

No cycle of any length — not claimed.

## Current literature

- Length-only parity finance — **EXACT — HUMAN PROOF**
  ([juggler_cycle_finance.md](juggler_cycle_finance.md));
  table at \(N_0=10^6\) is **COMPUTATIONALLY VERIFIED**
  (prefix \(25780\), \(141\) leftovers)
- Unique visit of \(n\) — **REPARAMETERIZATION** of prefix return
  ([juggler_cycle_equal_valleys.md](juggler_cycle_equal_valleys.md));
  \(n+2\) as a leftover-killer is **REFUTED**
- Odd-run height packing — **EXACT — HUMAN PROOF**
  ([juggler_cycle_position_finance.md](juggler_cycle_position_finance.md));
  at \(o_{\min}\) it coincides with parity
- Prefix-weight leftover-killer — **REFUTED**
  (`juggler_cycle_prefix_weight_leftover_killer`)
- `cycleMin_even_ge_sq`, `power_bound_word` — **EXACT — LEAN
  VERIFIED**
- Every start reaches 1 — not claimed

Project relationship: **extended**.

## Branch budget

```text
Mathematical target     Optimize the cycle-finance error budget using
                        minimum uniqueness + odd-run depth + maximum
                        excursion, rather than counting low states only
Novelty hypothesis      A cycle cannot simultaneously:
                        (i) concentrate many finance-expensive states
                        near n,
                        (ii) have deep odd runs, and
                        (iii) keep the maximum small.
                        The exact transition geometry forces a strictly
                        smaller global floor-error budget than parity finance.
Falsifier               The parity bound is already extremal: there exist
                        abstract/cyclic state geometries satisfying all
                        known transition constraints whose error sum matches
                        the parity RHS; or the max/run-position constraints
                        give no additional reduction for the 141 survivors.
Existing machinery      cycleMin, AboveAnchor,
                        cycle_min uniqueness/rotation,
                        power_bound_word,
                        log_step_even / log_step_odd,
                        cycleMin_log_envelope,
                        parity_rhs / parity_n_max,
                        floor cells,
                        odd-run structure,
                        known minima/maxima on cycle controls
Maximum Phase-0 scope   Symbolic optimization first; exact integer checks
                        only for the 141 survivors; derive run-depth lower
                        bounds and max-forced states; no new dynamical
                        invariant, no Q-section, no p-adic/residue system,
                        no terminal-cluster reopen
Promotion criterion     A reusable finance theorem of the form
                        Σ_i 1/(x_i log x_i)
                        ≤ F(L,o,n,M,{a_j})
                        with F strictly smaller than parity_rhs for every
                        admissible cycle configuration, yielding a new
                        period cutoff or shrinking E_par(10^6)
Stop criterion          The optimization collapses to parity finance;
                        maximum M can be sent arbitrarily large without
                        changing the extremum; run-depth information can be
                        rearranged to reproduce the same RHS; or only
                        numerical optimization with no exact theorem
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(n\)-circuit even cap \(3^k\ge 2^{k+\ell}\) —
  **EXACT — HUMAN PROOF** (ideal power; floors only help)
- `OE`-start \(v^3\ge n^4\) — **EXACT — HUMAN PROOF**
  (`cycleMin_even_ge_sq`)
- Run-type packing \(o-e\) copies of `OOE` and \(2e-o\) copies of
  `OE` — **EXACT — HUMAN PROOF**
- Unique visit of \(n\) — **REPARAMETERIZATION** (already known)
- Maximum \(M\to\infty\) — does not change the extremum
- Height packing at \(\tau_j\), \(j\ge 2\) — not forced at
  \(o_{\min}\)
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_budget_opt`
- Dataset: `data/research/juggler/cycle_finance/budget_opt.json`
- Tests: `tests/research/juggler_sequence/test_cycle_budget_opt.py`
- Window: the \(141\) parity leftovers at \(n=10^6+1\). Fast suite
  only. No CLI. No Lean.

## Conjectures

None opened.

## Counterexamples

The hypothesis that uniqueness or a bound on \(M\) is the leftover
killer is false: dropping the unique-min split or sending
\(M\to\infty\) does not change which leftovers die. The shrink
comes from the `OE`-start lift.

## Formalization

None. The packing is Python-checked against the parity leftover
list. No `CycleBudgetOpt.lean`. Paper A is unchanged.

## Results

- **Run-type finance** — **EXACT — HUMAN PROOF**. At
  \(n=10^6+1\), \(L=25781\): parity RHS \(\approx 8.27\cdot 10^{-4}\),
  packed RHS \(\approx 5.89\cdot 10^{-4}\) (factor \(23\) above
  \(\theta\approx 2.55\cdot 10^{-5}\)). Unique-min and
  \(M\to\infty\) change the seventh significant digit.
- **Leftover shrink** — **COMPUTATIONALLY VERIFIED**
  (`budget_opt.json`): \(42\) of the \(141\) leftovers die,
  namely \(56347+1054k\) for \(k=0,\ldots,41\). First survivor
  remains \(25781\). \(L=55293\) still lives
  (\(\theta\approx 1.247\cdot 10^{-3}\) versus
  RHS \(\approx 1.262\cdot 10^{-3}\)). \(99\) leftovers remain.
  Every leftover has packed RHS strictly below parity. Climb
  packing at \(\tau_1\) holds for all \(141\). Dropping the max
  even term does not change the kill list.

## Open questions

None from this packing. Necklace consistency of `OOE` landings
with `OE` starts is a composition question already closed as
extremal composition / Christoffel, and is out of Phase-0 scope.

## Decision

**PROMOTE**. The run-type bound is not a reparameterization of
parity finance: it replaces \(2e-o\) valleys at \(n\) by valleys
at \(n^{4/3}\), using only `cycleMin_even_ge_sq` and the ideal
power cap on \(n\)-circuits. It shrinks
\(\mathcal E_{\mathrm{par}}(10^6)\) from \(141\) to \(99\). The
period cutoff stays \(25780\). Uniqueness and the maximum do not
bind. Paper A still prints the parity table. Not a halt theorem.

Best next question: none from this packing. The frontier leftover
\(L=25781\) still has a factor-\(23\) valley gap at \(P=1\).

## Publication assessment

Status: `EXPLORATORY`. Laboratory refinement of the finance
dossier; not a second manuscript and not a Paper A edit.
