# Juggler nil-PET re-entry (the first difference re-expands \(A\{\Delta B\}\))

Status: **PROMOTE** (exact obstruction recorded; PET / characteristic
factors as a method for the floor-Hardy nil-orbit are **CLOSE**; the
rate-free conjecture stays **ACTIVE**)

Successor of [juggler_v94_rate_free](juggler_v94_rate_free.md)
(**CLOSE**), taking up the question that record left external: does
the first characteristic-factor / van der Corput step on the
Heisenberg lift keep the floor-removal correction as a Mal'cev
coordinate, or does Mal'cev reduction re-expand it into an
amplitude-product? Answer: **it re-expands.** Not an
equidistribution theorem, not a \(K_3\) bound, not a Paper B edit,
and not a reopen of BB/GG/JJ as rated methods.

## Problem

Whether Host–Kra / PET induction on the floor-Hardy Heisenberg
orbit \(n\mapsto\bigl(\tfrac32 v^{3/4},v^{3/2},0\bigr)\Gamma\)
absorbs \(\tfrac32 v^{3/4}\{v^{3/2}\}\) as a coordinate through the
first difference, or pays per oscillation of \(v^{3/4}\) at that
step.

## Exact statement

**Identity (EXACT — HUMAN PROOF, `J-nil-pet-reentry`).** Let
\(v=\lfloor n^{3/2}\rfloor\), \(A=\tfrac32 v^{3/4}\),
\(B=v^{3/2}\), and write \(g(n)=(A(n),B(n),0)\) in Heisenberg
Mal'cev coordinates with
\((x,y,z)*(x',y',z')=(x+x',\,y+y',\,z+z'+xy')\). Then
\(g(n)^{-1}=(-A,-B,AB)\) and

\[
g(n)^{-1}g(n+h)=(\Delta A,\,\Delta B,\,-A\,\Delta B).
\]

Right-reducing by \(\Gamma=H_3(\mathbb Z)\) to the fundamental
domain \([0,1)^3\) gives the vertical

\[
\chi_\Delta=\bigl\{-A\,\Delta B-\Delta A\,\lfloor\Delta B\rfloor\bigr\}
=\bigl\{-A(n+h)\,\lfloor\Delta B\rfloor-A(n)\{\Delta B\}\bigr\}.
\]

The first summand is integer dilation of \(\{A(n+h)\}\) (the cheap
decaying/tame \(A\)-axis of `J-horizontal-axis-species`). The second
is the amplitude-product \(A\{\Delta B\}\) with
\(A\asymp n^{9/8}\) and, for odd steps \(h=2\),

\[
A(n+2)-A(n)\sim\tfrac{27}{8}\,n^{1/8}\gg 1
\]

(GG species: `J-intra-block-harmonic-obstruction`). Equivalently,
\(A\{\Delta B\}\) is the vertical Mal'cev coordinate of a *second*
Heisenberg lift of \(\bigl(A(n),\Delta B(n,h),0\bigr)\) — the same
group law as `J-tower-heisenberg-coordinate`, valid for arbitrary
reals, not a degree drop. The entries of that second lift are not
\(o(1)\)-close to a Hardy-in-\(n\) pair: the leftover of \(\Delta B\)
against \((n+h)^{9/4}-n^{9/4}\) has size \(\asymp n^{3/4}\) (the
\(B\)-leftover exponent of `J-horizontal-leftover-exponents`).

This is a different identity from the v94 abelian difference
\(\{v(n+h)^{9/4}-v(n)^{9/4}\}=\{\Delta v\cdot\{\tfrac94\xi^{5/4}\}\}\).
Qualitative van der Corput on the circle axis stays that
integer-dilation statement. PET on the nilmanifold produces, after
reduction, an amplitude-product in the original family
\(A=\tfrac32 v^{3/4}\).

**Consequence.** Characteristic-factor / PET induction re-enters the
amplitude-product class at the first step. The algebraic lift still
applies (the second lift is the same algebra); it does not reach a
published Hardy-nil orbit (Richter / Frantzikinakis / Boshernitzan
still miss floor-Hardy composition). The optimistic claim
`juggler_nil_pet_stays_coordinate` is **REFUTED**. The rate-free
conjecture `juggler_tower_rate_free_equidistribution` is unharmed.

## Current literature

Project relationship: **extended** (opens the characteristic-factor
falsifier the v94 placement left external; the group law is KNOWN).

- Host–Kra 2005 (`host-kra-2005-nilmanifolds`): PET / cubespace
  induction on nilsequences. Supplies the schema, not a theorem
  about floor-Hardy entries.
- Bergelson–Leibman: the Heisenberg representation of
  \(A\lfloor B\rfloor\bmod 1\) is the depth-1 case; their
  equidistribution theorem needs polynomial entries.
- Richter 2023 / Frantzikinakis 2009 / Boshernitzan 1994: miss
  \(\{v^{9/4}\}\) ([juggler_v94_rate_free](juggler_v94_rate_free.md)).
  Not re-tested.
- `J-tower-heisenberg-coordinate`: the unshifted lift is algebra.
- `J-nil-lift-does-not-derandomize`: the lift is a dictionary for
  the \(\lambda\)-shift, not a method outside BB/GG/JJ. Sibling on
  the *rated* line; not reopened.
- `J-horizontal-axis-species` / `J-horizontal-theorem-r-shortcut`
  (**REFUTED**): abelian first difference and Theorem-R shortcut.
  Different identity; not re-tested.

## Branch budget

```text
Mathematical target     does the first PET difference of the
                        Heisenberg lift keep the floor-removal
                        correction as a Mal'cev coordinate, or does
                        Mal'cev reduction re-expand it into an
                        amplitude-product of GG species?
Novelty hypothesis      χ_Δ = {-A(n+h)⌊ΔB⌋ - A(n){ΔB}}; the second
                        term is A{ΔB} with A ≍ n^{9/8} and
                        A(n+2)-A(n) ≍ (27/8) n^{1/8} >> 1
Falsifier               the identity fails; or A{ΔB} is o(1); or
                        A' → 0; or ΔB is o(1)-close to a
                        Hardy-in-n increment
Existing machinery      J-tower-heisenberg-coordinate, leftover / GG
                        table, J-nil-lift-does-not-derandomize,
                        v94 abelian vdC (different identity),
                        bracket_nil_lift scaled roots
Maximum Phase-0 scope   Fraction identity + tower species witnesses;
                        dossier, journal, one ledger row, one
                        REFUTED method record; no Weyl census, no
                        Lean, no Paper B, no PET²
Promotion criterion     exact identity plus species that the
                        predicted fourth layer fires
Stop criterion          the identity is a reparameterization of the
                        v94 abelian difference, or there is no
                        re-entry
```

## Balanced-ternary formulation

None required. The objects live on \(H_3(\mathbb R)/H_3(\mathbb Z)\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Unreduced PET product
  \(g(n)^{-1}g(n+h)=(\Delta A,\Delta B,-A\Delta B)\) —
  **EXACT — HUMAN PROOF** (Heisenberg group law).
- Reduced vertical split
  \(\chi_\Delta=\{-A(n+h)\lfloor\Delta B\rfloor-A(n)\{\Delta B\}\}\) —
  **EXACT — HUMAN PROOF** (Mal'cev reduction).
  **COMPUTATIONALLY VERIFIED** on Fraction witnesses and one
  scaled tower pair.
- Discrete increment \(A(n+2)-A(n)\sim\tfrac{27}{8}n^{1/8}\) —
  **EXACT** (chain rule on \(A=\tfrac32 v^{3/4}\), \(v\sim n^{3/2}\));
  **COMPUTATIONALLY VERIFIED** leading ratio on the sample.
- Leftover of \(\Delta B\) versus \((n+h)^{9/4}-n^{9/4}\) of size
  \(\asymp n^{3/4}\) — **EXACT** (corollary of
  `J-horizontal-leftover-exponents`); **COMPUTATIONALLY VERIFIED**.
- Equidistribution of the difference orbit — not claimed.
- A second PET step — not taken.

## Experiments

- Probe: `research.juggler_sequence.nil_pet_reentry`
- Artifact: `data/research/juggler/nil_pet_reentry/summary.json`
- Tests: `tests/research/juggler_sequence/test_nil_pet_reentry.py`

Science sample: odd pairs with \(h=2\) on
\((10^4,10^4+200]\) and \((10^6,10^6+200]\). Tests use the short
\(10^4\) block. No Weyl grid: the nil-lift already has \(124\)
harmonics at \(\sqrt N\).

## Conjectures

`juggler_tower_rate_free_equidistribution` stays **ACTIVE**. The
method claim `juggler_nil_pet_stays_coordinate` is **REFUTED**.
Conjectures V/HH stay PARKED.

## Counterexamples

The novelty hypothesis did **not** die. The optimistic claim died
by the identity and the GG increment, not by a counterexample
orbit. No orbit is claimed to fail equidistribution.

## Formalization

None. Lean-ifying the Heisenberg group law for one difference is
machinery gravity ahead of an equidistribution theorem that would
consume it.

## Results

Classification **NIL_PET_REENTRY_GREEN**.

- **Identity (EXACT — HUMAN PROOF):**
  \(g(n)^{-1}g(n+h)=(\Delta A,\Delta B,-A\Delta B)\) and
  \(\chi_\Delta=\{-A(n+h)\lfloor\Delta B\rfloor-A(n)\{\Delta B\}\}\).
  Fraction witnesses exact; scaled tower pair exact.
- **Species:** \(A(n+2)-A(n)\asymp n^{1/8}\gg 1\) (GG);
  \(\{\Delta B\}\) is not concentrated at \(0\);
  leftover of \(\Delta B\) versus the smooth increment is
  \(\asymp n^{3/4}\), not \(o(1)\).
- **Method:** PET / characteristic-factor induction re-enters the
  amplitude-product class at step one. The second lift is the
  original algebra, not a published door.
- **Not claimed:** equidistribution; density-one; a \(K_3\) bound;
  that the rate-free conjecture is false; that Leibman-on-the-
  horizontal is dead (that remains the unbuilt composition).

## Open questions

- Rate-free equidistribution of the floor-Hardy nil-orbit —
  still the active conjecture; the missing lemma is still
  Hardy-of-floor composition (Leibman criterion on the
  horizontal triple), not a PET reduction. External; not opened.
- The node-wise E-share \(\beta>0.369\) non-concentration
  fallback of `J-rate-free-density-one` is a weaker ergodic ask
  and is not opened from here.
- A second PET step is machinery gravity: it cannot erase an
  amplitude-product that already appeared at step one.

## Decision

**PROMOTE.** The identity is exact, it is not the v94 abelian
difference, and the predicted fourth layer fires: the first
characteristic-factor step re-expands
\(\tfrac32 v^{3/4}\{v^{3/2}\}\) into \(A\{\Delta B\}\) of GG
species. PET as a method for the floor-Hardy nil-orbit is closed.
The rate-free conjecture stays ACTIVE as an external composition
problem (Leibman / Richter on floor-Hardy entries, not PET). Best
next question: none from this door; the live target remains the
rate-free conjecture as Hardy-of-floor composition, and the bias
fallback is not opened from here.

## Publication assessment

Status: `ARCHIVED`. An obstruction identity that names the
fourth-layer wall. Not a paper claim. No Paper B edit.
