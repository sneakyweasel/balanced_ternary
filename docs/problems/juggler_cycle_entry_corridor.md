# Juggler CycleMin backward entry corridor

Status: **STRUCTURAL**

Refinement of
[juggler_cycle_entry_excursion.md](juggler_cycle_entry_excursion.md)
and the excursion necklace in
[juggler_finite_dynamics_note.md](../theory/juggler_finite_dynamics_note.md)
§3, not a new paper. After the entry-excursion finance tax closed,
this phase asks whether the unique circular seam at a CycleMin
minimum — last run exactly `OE`, entry valley in the two-sided
\(n^{4/3}\) cell, pre-entry run \(\le 2\) — has an exact backward
1–2-block corridor that empties or collides with the forced
forward `OO` lift for a reason that is not an archived cell.

Not a halt theorem, not a leftover-killing finance tax, not an
inverse-width reopen, not a floor raise, and not a claim that
every positive integer reaches 1.

## Problem

Paper A writes the two ends of a CycleMin necklace separately:
forced prefix `OO` with \(J^2(n)\ge(n+1)^2\), last peak in the
last-even cell, last excursion written as unconstrained
\(O^{a_e}E\). The same sandwich already kills the whole-word
cases \(O^aE\) (\(a\ge 3\)) and `OOEOOE`. Does the sandwich
force \(a_e=1\) on every CycleMin necklace, pin the last valley
to \(n^4<v^3<(n+1)^4\), and does the exact backward tree from
that cell collide with the initial lift?

## Exact statement

**Lemma A — last run is `OE` (EXACT — HUMAN PROOF).**
On a CycleMin start \(n\ge 5\), the last excursion is
\(v\xrightarrow{O}p\xrightarrow{E}n\). If the last odd-run had
length \(a\ge 2\), then \(v\ge n\) realizes `OO`, so
monotonicity (`image_monotone_of_follows`) plus Lemma 3.4(i)
give \(p=T^a(v)\ge T^2(v)\ge T^2(n)\ge(n+1)^2\), contradicting
the last-even cell \(p<(n+1)^2\) (Lemma 3.4(iv)). This is the
`OOEOOE` argument of Theorem 3.6 with the last valley in place
of \(y=J^3(m)\). Paper A §3 does not name
`cycleMin_last_odd_run_eq_one`.

**Lemma B — two-sided corridor (EXACT — HUMAN PROOF).**
The last valley satisfies \(n^4<v^3<(n+1)^4\), i.e.
\(n^{4/3}<v<(n+1)^{4/3}\). The lower bound is the existing
`oe_start_min` / \(v^3\ge n^4\). The upper bound is the
odd-cell pullback of \(p<(n+1)^2\), already used for the last
`OE` of `OOOEOE` in Lemma 3.5. The intermediate claim
\(v^3<(n+1)^{8/3}\) is false; the boxed \((n+1)^{4/3}\) is the
correct dual.

**Lemma C — pre-entry \(b\le 2\) (EXACT — HUMAN PROOF for
\(n\ge 5\)).**
The run into \(v_{\mathrm{in}}\) has length \(\le 2\). The
lower bound is the odd-run envelope from an AboveAnchor `OOO`
start \(u\ge n\): \(T^2(u)\) is odd and at least \((n+1)^2+1\)
(because CycleMin \(n\) realizes `OO` and \((n+1)^2\) is even),
so \(T^3(u)\ge\lfloor\sqrt{((n+1)^2+1)^3}\rfloor\), which
already exceeds \((v_{\mathrm{hi}}+1)^2\) at \(n=5\). Do not
compare to \(T^3(n)\): \(a_0=2\) is legal and \(n\) need not
realize `OOO`.

**Entry set and first layer (COMPUTATIONALLY VERIFIED).**
At \(n=10^6+1\) the exact `OE` fibre with tube \(\ge n\) is
the known \(33\) valleys
\([100000135,100000265]\subset(n^{4/3},(n+1)^{4/3})\). The
left endpoint equals `oe_start_min`. Every valley has a
nonempty \(F_1\) fibre (\(5101\) AboveAnchor predecessors,
scale \(\sim n^{16/9}\)). Exactly one valley,
\(100000159\), also has a nonempty \(F_2\) fibre, the
singleton \(12915515\). The \(F_3\) fibre is empty on all
\(33\). No entry valley is a forward-seam state.

**Forward seam (COMPUTATIONALLY VERIFIED).**
The finance-floor representative \(n=10^6+1\) does **not**
realize `OO`: \(T(n)=1000001500\) is even and the first even
lands at \(31622<n\). The first `OO`-legal start at this
scale is \(1000057\), with
\(T^2=31626832356906\ge(n+1)^2\) and first-\(E\) landing
\(5623773\). Neither seam meets a backward valley.

**Second block (COMPUTATIONALLY VERIFIED).**
One further block \(a\in\{1,2\}\) from the \(5102\)
predecessors yields \(10204\) fibres: \(5133\) occupied,
\(5071\) `empty_ooe`, zero unarchived tags, zero collisions.
The coarse three-`OOE` exponent \(2048/2187<1\) is the suffix
dual of \(243<256\), not a leftover-killer.

The cycle-necessary set is the **union**
\(\mathcal E_n\cap\bigl(F_1(\mathrm{AA})\cup F_2(\mathrm{AA})\bigr)\),
which is nonempty. The triple intersection (an occupancy
diagnostic) is the singleton \(\{100000159\}\).

No cycle of any length — not claimed.

## Current literature

- Last-even cell, \(x\neq n^2\) —
  **EXACT — LEAN VERIFIED**
  (`cycle_last_even_interval`, `cycle_last_even_ne_odd_sq`)
- \(J^2(q)\ge(q+1)^2\) on a realized `OO` —
  **EXACT — HUMAN PROOF** (Lemma 3.4(i)); Lean
  `cycleMin_first_even_overshoots` / `oo_suffix_threshold`
- `OE`-start \(v^3\ge n^4\) —
  **EXACT — HUMAN PROOF**
  ([juggler_cycle_budget_opt.md](juggler_cycle_budget_opt.md))
- `OOEOOE` exclusion —
  **EXACT — LEAN VERIFIED** (Theorem 3.6)
- Entry run is `OE` at \(n=10^6+1\); finance tax \(0\) —
  **CLOSE** / leftover-killer **REFUTED**
  ([juggler_cycle_entry_excursion.md](juggler_cycle_entry_excursion.md))
- Wrap-around is an `OE` landing —
  **CLOSE** / cheap-cap **EXACT — HUMAN PROOF**
  ([juggler_cycle_cyclic_valley.md](juggler_cycle_cyclic_valley.md))
- \(F_2(v)>v\); \(243<256\) —
  **EXACT — HUMAN PROOF** /
  leftover-killer **REFUTED**
  ([juggler_cycle_ordered_excursion.md](juggler_cycle_ordered_excursion.md))
- Inverse tubes die on archived cells —
  **CLOSE**
  ([juggler_cycle_inverse_width.md](juggler_cycle_inverse_width.md),
  [juggler_cycle_almost_search.md](juggler_cycle_almost_search.md),
  [juggler_backward_geometry.md](juggler_backward_geometry.md))
- Collatz-style financing —
  **known** (`simons-de-weger-2005-collatz-m-cycles`)
- Every start reaches 1 — not claimed

Project relationship: **extended**. Lemma A names a CycleMin
word-shape that Paper A §3 uses only for whole-word / two-circuit
exclusions. The backward tree is a **REPARAMETERIZATION** of
archived `empty_ooe` / `empty_odd_cell` fibres and does not
kill a leftover.

## Branch budget

```text
Mathematical target     Is the CycleMin last excursion exactly OE, with
                        entry valley in the exact two-sided n^{4/3}
                        cell, and does the exact 1–2-block backward
                        corridor from that cell empty or collide with
                        the forced forward OO lift for a reason that
                        is not last-even / oe_start_min / F2(v)>v /
                        243<256 / empty_ooe?
Novelty hypothesis      the unique circular seam is a local CycleMin
                        theorem (a_final=1 + two-sided corridor +
                        pre-entry b≤2) whose backward tree is not the
                        archived prefix/inverse package
Falsifier               a_final=1 is only F2(v)>v restated; the 2-block
                        tree is occupied and dies only on archived
                        cells; the exponent ladder is 243<256 read
                        backward; no collision with {n, T(n), T^2(n)}
Existing machinery      cycleMin_starts_two_odds; Lemma 3.4(i)/(iv);
                        image_monotone_of_follows; cycle_last_even_*;
                        oe_start_min; compatible_oe_preimages;
                        run_preimages; excursion_map; entry_row /
                        run_layer (33 OE valleys at 10^6+1)
Maximum Phase-0 scope   human proofs of the three seam lemmas; exact
                        2-block backward census at n=10^6+1; forward
                        seam comparison; no finance, no Lean, no
                        Paper A, no automaton, no N0 raise
Promotion criterion     a Lean-ready CycleMin lemma that is not an
                        archived cell, or a predecessor emptiness that
                        is not empty_ooe / 243<256 / F2(v)>v
Stop criterion          all three lemmas reparameterize archived
                        facts AND the tree is occupied with only
                        archived deaths
```

## Closed-bridge gates

Classify the seam before any follow-up. Do not reopen the
entry-excursion tax, inverse-width tubes, or \(243<256\).

- **CLOSE** if Lemmas A–C are only last-even + `oe_start_min` +
  \(F_2(v)>v\) written in one box, **and** the 2-block tree is
  occupied and dies only on `empty_ooe` / `below_n` / \(243<256\).
- **CLOSE** if “collision” is the ordered-excursion prefix cell
  read backward.
- **PROMOTE** Lemma A (and only then Lean) if
  `cycleMin_last_odd_run_eq_one` is a reusable CycleMin statement
  that Paper A §3 does not already have — even if the tree does
  not empty. Do not auto-open a corridor engine after that.
- **PROMOTE** the tree only if some fibre empties for a reason
  that is not an archived cell.

Do **not** raise \(N_0\). Do **not** open \(L=25781\) or
\(L=55293\). Do **not** edit Paper A or the theorem ledger in
Phase-0.

## Explicitly out of Phase-0

A leftover-killer at \(L=25781\), a third interior block, a
generic run automaton, Fourier / residues / \(Q\)-sections,
ledger row, Lean, CLI, visualization.

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Last odd-run length on a CycleMin word —
  **EXACT — HUMAN PROOF** (Lemma A)
- Two-sided entry corridor \(n^4<v^3<(n+1)^4\) —
  **EXACT — HUMAN PROOF** (Lemma B)
- Pre-entry run \(b\le 2\) for \(n\ge 5\) —
  **EXACT — HUMAN PROOF** (Lemma C); \(n_0=5\)
- Exact \(\mathcal E_n\) at \(n=10^6+1\) —
  **COMPUTATIONALLY VERIFIED**; \(33\) valleys, all in-corridor
- \(F_1\) / \(F_2\) / \(F_3\) of \(\mathcal E_n\) —
  **COMPUTATIONALLY VERIFIED**; \(F_3=\emptyset\), one \(F_2\)
  witness \(12915515\xrightarrow{\mathrm{OOE}}100000159\)
- Forward `OO` lift versus backward valleys —
  **COMPUTATIONALLY VERIFIED**; no exact collision; the floor
  representative is not itself `OO`-legal
- Second-block tags —
  **COMPUTATIONALLY VERIFIED**; only `occupied` / `empty_ooe`
- Three-`OOE` exponent \(2048<2187\) —
  **REPARAMETERIZATION** of \(243<256\)
- Entry leftover-killer — not claimed
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_entry_corridor`
- Dataset: `data/research/juggler/entry_corridor/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_entry_corridor.py`
- Window: \(n=10^6+1\); first legal `OO` start \(1000057\);
  backward runs \(a\le 3\) on \(\mathcal E_n\), then one more
  block \(a\in\{1,2\}\). Fast suite only. No CLI. No Lean.
  No \(N_0\) raise.

## Conjectures

None. No leftover-killer conjecture.

## Counterexamples

- \(n=10^6+1\) does not realize `OO`
  (\(T(n)=1000001500\) even, first even lands at \(31622<n\)).
  Falsifier of reading the finance-floor representative as a
  CycleMin start.
- \(100000159\xrightarrow{\mathrm{OE}}n\) has an AboveAnchor
  `OOE` predecessor \(12915515\). Falsifier of “every pre-entry
  run is `OE`” at this \(n\).
- \(5101\) AboveAnchor `OE` predecessors of \(\mathcal E_n\).
  Falsifier of an empty first backward cell.
- Zero exact collisions with
  \(\{n,T(n),T^2(n)\}\) or the legal `OO` seam at \(1000057\).
  Falsifier of a 2-block seam collision.

## Formalization

None in Phase-0. No `EntryCorridor.lean`. Paper A is unchanged.
The Lean-ready target after this decision is
`cycleMin_last_odd_run_eq_one` in `EvenCountThree.lean` /
`CycleCore.lean`. Do not formalize the sample table.

## Results

- **Lemma A** — **EXACT — HUMAN PROOF**. Every CycleMin necklace
  ends `OE`. Classification `ENTRY_CORRIDOR_GREEN`.
- **Lemma B** — **EXACT — HUMAN PROOF**. Integer corridor
  \(n^4<v^3<(n+1)^4\). At \(n=10^6+1\),
  `v_lo=v_hi` window \([100000135,100000265]\) matches
  `oe_start_min` through the last occupant; all \(33\) exact
  entries lie in it (`all_in_corridor=true`).
- **Lemma C** — **EXACT — HUMAN PROOF**. Envelope \(n_0=5\);
  `f3_empty=true` at the published floor start.
- **Tree** — **COMPUTATIONALLY VERIFIED**. Union occupied
  (\(5101+1\)); second-block deaths archived; `exact_collision`
  false; `leftover_killer` false.
- **No new leftover-killer. No \(N_0\) raise.**

## Open questions

Formalize `cycleMin_last_odd_run_eq_one`. Do not open a third
backward block, a corridor engine, \(L=25781\), or \(L=55293\).

## Decision

**PROMOTE**. Lemma A is a reusable CycleMin word-shape that
Paper A §3 does not name: the last odd-run of every CycleMin
necklace has length exactly one. It is the `OOEOOE` sandwich of
Theorem 3.6 applied to an arbitrary last valley, not a new
cell. Lemmas B–C are the exact two-sided pullback and the
`OOO` envelope; they do not improve finance. The 2-block
backward tree is occupied, dies only on `empty_ooe` /
`empty_odd_cell`, and does not collide with the forward `OO`
lift. No Paper A edit, no ledger row, no Lean, no \(N_0\)
raise in this phase.

Best next question: Lean `cycleMin_last_odd_run_eq_one`.

## Publication assessment

Status: `STRUCTURAL`. Laboratory CycleMin local-structure
lemma, not a second manuscript and not a Phase-0 Paper A edit.
Lean packaging is the follow-up, not an automatic engine.
