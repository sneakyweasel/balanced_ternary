# Juggler exact modular cycle closure

Status: **EXPLORATORY**

Refinement of
[juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md) and
[juggler_cycle_closure.md](juggler_cycle_closure.md), not a new
paper. It asks whether the modular shadow of the exact square/cube
floor cells refuses to close on a surviving \((L,o)\) in
\(\mathcal E_{\mathrm{run}}(10^6)\) without enumerating words.
Not a halt theorem, not a leftover-word census, not a new finance
budget, not Fourier, not a \(Q\)-return, not a 2-adic cylinder
reopen, and not a generic residue automaton.

## Problem

Pair-level interval closure is the exponent envelope. Formal
\(O/E\) feasibility is not integer realizability. Do the exact
cells

\[
y^2\le x^3<(y+1)^2\qquad\text{(odd)},\qquad
y^2\le x<(y+1)^2\qquad\text{(even)}
\]

impose a modular compatibility condition around a hypothetical
near-convergent cycle that finance and interval hulls cannot see?

## Exact statement

For a modulus \(m\) and a structural block \(W\), the relation
\(R_W(m)\subseteq(\mathbb Z/m\mathbb Z)^2\) contains \((x,y)\)
when the exact integer floor equations admit a realization
beginning at some integer \(\equiv x\) and ending at one
\(\equiv y\). Cycle-scale necessary form \(R_{\mathrm{nec}}\)
treats the defects \(\delta,\eta\) as free residues whenever
\(2Y+1>m\). Witness form \(R_{\mathrm{wit}}\) records exact
`floor_power` landings at \(n\ge N_0+1\).

A class is modularly impossible when

\[
R_{\mathrm{cycle}}(m)\cap\Delta_m=\varnothing,
\]

with \(\Delta_m=\{(r,r)\}\), for every word in the class. Phase 0
tests Level A (pair \((L,o)\)) and Level B (run-type `OOE`/`OE`
counts). It does not test Level C (a complete word).

No cycle of any length — not claimed.

## Current literature

- Inverse-floor cells, `odd_cell_unique`, `even_cell_iff` —
  **EXACT — LEAN VERIFIED** (`Cells.lean`)
- Odd-odd remainder \(\rho\equiv y-1\pmod 8\) —
  **EXACT — LEAN VERIFIED** (`LandingValuation.lean`)
- Defect lower bounds mod \(4\) and \(8\) —
  **EXACT — LEAN VERIFIED** (`DefectLowerBound.lean`)
- `OOE` cylinder does not decide the next letter —
  **EXACT — LEAN VERIFIED** (`ooe_cylinder_both_next_parities`)
- Pair-level interval closure —
  **CLOSE**
  ([juggler_cycle_closure.md](juggler_cycle_closure.md));
  leftover-killer **REFUTED**
- 2-adic itinerary cylinders —
  **CLOSE**
  ([juggler_2adic_integer_bridge.md](juggler_2adic_integer_bridge.md))
- Peak \((\delta,\varepsilon)\) residue census —
  **CLOSE**
  ([juggler_cycle_diophantine.md](juggler_cycle_diophantine.md));
  residues collapse to odd/odd
- Run-type finance, \(99\) leftovers —
  **EXACT — HUMAN PROOF** /
  **COMPUTATIONALLY VERIFIED**
  ([juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md))
- Prefix expansion of leftovers —
  **CLOSE**
  ([juggler_cycle_prefix_feasibility.md](juggler_cycle_prefix_feasibility.md))
- Collatz-style financing —
  **known** (`simons-de-weger-2005-collatz-m-cycles`)
- Every start reaches 1 — not claimed

Project relationship: **independent** of the closed interval-closure
and 2-adic-bridge branches; the object is \(R_W(m)\cap\Delta_m\).

## Branch budget

```text
Mathematical target     Modular closure of the exact square/cube floor
                        equations for the 99 finance-surviving (L,o) pairs
Novelty hypothesis      Exact floor cells impose modular compatibility
                        around a closed cycle that finance and interval
                        hulls cannot see
Falsifier               Every tested modulus admits a diagonal residue
                        realization; or the relation is only parity /
                        odd_cell_unique / existing cells; or only a
                        complete word dies; or the useful modulus is a
                        large automaton / p-adic system
Existing machinery      CycleMin; Cells; odd_cell_unique; even_cell_iff;
                        LandingValuation mod-8; run-type finance;
                        prefix_feasibility; cycle_closure (CLOSED)
Maximum Phase-0 scope   Exact modular shadows of composed floor cells;
                        2^a, 3^b, then 2^a 3^b; L=25781 and 55293 first;
                        word-independent / structural-class only
Promotion criterion     Reusable modular closure: exact cells + run
                        structure ⇒ R_cycle(m) ∩ Δ_m = ∅
Stop criterion          Nonempty diagonal on all structural classes;
                        bookkeeping only; Level C only; huge automaton
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required. Powers of \(3\) enter only as the odd-step
cube, not as a trit encoding.

## Candidate operations / invariants

- Cycle-scale \(R_{\mathrm{nec}}\) is first-letter parity
  (defects free once \(2Y+1>m\)) —
  **EXACT — HUMAN PROOF** (this dossier)
- Even-cell existence at scale \(2Y+1\ge m\) is the full
  even-source relation —
  **EXACT — HUMAN PROOF** (this dossier)
- Block identities `OE`, `OOE`, `OOOE`, `OEE`, `OOEE` as
  relations, not functions —
  **REPARAMETERIZATION** of the exact cells
- CycleMin first-odd versus last-even residues —
  **REPARAMETERIZATION** of the existing overshoot
  (different indices)
- Additive increment of `OOE`/`OE` at the run-type counts —
  tested; not a leftover-killer
- Pair-level modular leftover-killer —
  tested in Phase 0
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_mod_closure`
- Dataset: `data/research/juggler/cycle_finance/mod_closure/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_mod_closure.py`
- Window: \(L=25781\) and \(L=55293\); moduli \(8,16,32,64\),
  \(3,9,27,81\), and products \(2^a3^b\) through \(16\cdot 81\).
  Fast suite only. No CLI. No Lean.

## Conjectures

`juggler_cycle_mod_closure_leftover_killer` — recorded after
the scan.

## Counterexamples

Recorded after the scan.

## Formalization

None. No `CycleModClosure.lean`. Paper A is unchanged. Existing
mod-\(8\) lemmas in `LandingValuation` and `DefectLowerBound`
are not re-proved.

## Results

Recorded after the scan. Artifact
`mod_closure/summary.json`.

## Open questions

Pending the scan.

## Decision

Phase 0 is in progress. The branch will end in exactly one of
PROMOTE, PARK, or CLOSE after the modular scan.

Best next question: pending the scan.

## Publication assessment

Status: `EXPLORATORY`. Laboratory probe of a finance refinement;
not a second manuscript and not a Paper A edit.
