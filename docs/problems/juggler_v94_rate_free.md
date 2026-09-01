# Juggler \(v^{9/4}\) rate-free door (published Hardy-nil vs qualitative van der Corput)

Status: **CLOSE** (the named question is answered: no published Hardy-nil
theorem identifies \(\{v^{9/4}\}\) without a \(\theta\)-unwind, and
qualitative van der Corput lands on integer dilation of
\(\{v^{5/4}\}\), the same unbuilt composition; rate-free conjecture
stays ACTIVE)

Successor of
[juggler_horizontal_weyl](juggler_horizontal_weyl.md) and
[juggler_heisenberg_cut](juggler_heisenberg_cut.md), taking up the
recorded next question: does a rate-free argument identify
\(\{v^{9/4}\}\), \(v=\lfloor n^{3/2}\rfloor\), without unwinding
through \(\theta=\{n^{3/2}\}\), or is that still the unbuilt
Hardy-field door? Answer: the door is the missing composition
\(a^{f(\lfloor h(n)\rfloor)}\) with \(f\) a nonlinear Hardy
monomial. Not an equidistribution theorem, not a \(K_3\) bound, not
a Paper B edit, and not a reopen of the Theorem-R shortcut,
\(\lambda=0\), or the Lemma G confirmation.

## Problem

Whether the remaining abelian axis of the nil-lift horizontal torus
is already a published Hardy-field unique-ergodicity theorem, or a
qualitative van der Corput reduction to a recorded row.

## Exact statement

Let \(v=\lfloor n^{3/2}\rfloor\). The rate-free tower target
(`juggler_tower_rate_free_equidistribution`) reduces, after
`J-tower-heisenberg-coordinate` and `J-horizontal-axis-species`, to
equidistribution of the floor-Hardy orbit, and the only axis that
is not a reduction lemma is \(\{v^{9/4}\}\).

**Placement (EXACT — HUMAN PROOF; no new ledger row).** None of
the three named published doors applies to
\(n\mapsto\{\lfloor n^{3/2}\rfloor^{9/4}\}\).

| Source | Hypothesis | Instance |
|---|---|---|
| Boshernitzan 1994 (`boshernitzan-1994-hardy-fields`) | \(f\) Hardy, polynomial growth, log-away from \(\mathbb Q[t]\); then \(\{f(n)\}\) equidistributes | \(\{n^{27/8}\}\) matches; \(\lfloor n^{3/2}\rfloor^{9/4}\) is not Hardy in \(n\) |
| Frantzikinakis 2009 (`frantzikinakis-2009-sparse-nilmanifolds`) | floor sits in the *time slot* of a *fixed* nilrotation, \(b^{\lfloor a(n)\rfloor}x\) | not a Hardy monomial of a floor; not \(g(v)=\exp\bigl(\tfrac32 v^{3/4}e_{12}+v^{3/2}e_{23}\bigr)\) at \(v=\lfloor n^{3/2}\rfloor\) |
| Richter 2023 (`richter-2023-hardy-nilmanifolds`) | \(a_1^{f_1(n)}\cdots a_k^{f_k(n)}\Gamma\) with each \(f_i\) Hardy of polynomial growth | smooth model \((n^{3/4},n^{3/2},n^{9/4})\) matches; \(\lfloor n^{3/2}\rfloor^{9/4}\) does not |

The missing lemma is the composition \(a^{f(\lfloor h(n)\rfloor)}\)
with \(f\) a nonlinear Hardy monomial. Unwinding
\(\lfloor h\rfloor\to h\) is the leftover
\(\tfrac94 n^{15/8}\theta\) of `J-horizontal-axis-species`, already
HH/GG and forbidden by `J-nested-floor-without-W-family`. Rate-free
does not help: the leftover is not \(o(1)\), so Richter on the
smooth model does not transfer.

**Difference species (EXACT — HUMAN PROOF; corollary of
`J-horizontal-axis-species`).** For \(h\ge 1\) and
\(\Delta v=v(n+h)-v(n)\in\mathbb Z\), the mean-value identity
already recorded gives
\[
v(n+h)^{9/4}-v(n)^{9/4}
=\tfrac94\xi^{5/4}\,\Delta v,
\qquad
\xi\in\bigl(v(n),v(n+h)\bigr).
\]
Because \(\Delta v\) is an integer,
\[
\bigl\{v(n+h)^{9/4}-v(n)^{9/4}\bigr\}
=\bigl\{\Delta v\cdot\bigl\{\tfrac94\xi^{5/4}\bigr\}\bigr\}.
\]
This is integer dilation of \(\{v^{5/4}\}\) (up to the
\(O(n^{7/8})\) mean-value slack between \(\xi\) and \(v\)), not
the classical Hardy monomial \(\{n^{19/8}\}\). Qualitative van der
Corput therefore asks for equidistribution of a dilated floor-Hardy
coordinate — the same unbuilt composition, or harder
(\(\Delta v\asymp n^{1/2}\)). The recorded \(C'\gg 1\) kills rated
character windows (`J-horizontal-theorem-r-shortcut`); it does
**not** kill qualitative equidistribution of the difference.

## Current literature

Project relationship: **known** (the three theorems) /
**reproduced** (the leftover and first-difference already in
`J-horizontal-axis-species`).

- Boshernitzan 1994 — circle unique ergodicity for Hardy \(f\).
- Frantzikinakis 2009 — floor-removal in the time slot of a fixed
  nilrotation; cites Boshernitzan for the circle.
- Richter 2023 — Leibman criterion for Hardy-field nil-orbits.
- The lab's species statement
  ([juggler_k3_rate_free.md](juggler_k3_rate_free.md)): Hardy
  entries and single floors are handled; nested floor-power
  brackets are not. This branch names the composition gap that
  sentence only sketched.
- `J-horizontal-theorem-r-shortcut` (**REFUTED**): rated unwind /
  one Weyl step re-enters GG/HH. Not re-tested.
- `J-nil-lift-does-not-derandomize` (**CLOSE**): not reopened.
- Characteristic-factor self-similarity of floor-removal remains
  the named *external* route-falsifier; not opened.

## Branch budget

```text
Mathematical target     does a rate-free argument identify {v^{9/4}},
                        v = floor(n^{3/2}), without unwinding through
                        theta = {n^{3/2}} — published Hardy-nil theorem,
                        or qualitative van der Corput to a recorded row?
Novelty hypothesis      either Richter/Frantzikinakis/Boshernitzan apply
                        verbatim to n |-> {floor(n^{3/2})^{9/4}}, or the
                        keep-v difference {v(n+h)^{9/4}-v(n)^{9/4}}
                        reduces to a classical Hardy monomial
Falsifier               every cited theorem requires f in a Hardy field
                        or floor-removal in the time slot of a fixed
                        nilrotation (not a monomial of a floor); and the
                        difference is integer-dilation of {v^{5/4}},
                        same unbuilt composition (or worse)
Existing machinery      J-rate-free-density-one, J-tower-heisenberg-coordinate,
                        J-heisenberg-vertical-riemann, J-horizontal-axis-species,
                        J-horizontal-theorem-r-shortcut (REFUTED),
                        horizontal_weyl first-difference identity
Maximum Phase-0 scope   literature mismatch table + one keep-v difference
                        identity (reuse horizontal_weyl scaled roots);
                        dossier, journal, literature JSON; no Weyl census,
                        no Lean, no Paper B, no K3/HH reopen
Promotion criterion     a verbatim citation, or qualitative vDC reducing
                        to a recorded/classical equidistributed sequence
Stop criterion          mismatches are KNOWN packaging of "door unbuilt"
                        and the difference is the same composition species
```

## Balanced-ternary formulation

None required. The objects live on \(\mathbb T\) and on
\(H_3(\mathbb R)/H_3(\mathbb Z)\).

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Richter / Frantzikinakis / Boshernitzan hypothesis match —
  **KNOWN** (hypotheses fail; recorded above)
- Keep-\(v\) mean-value identity —
  **EXACT — HUMAN PROOF** (already `J-horizontal-axis-species`)
- Integer-dilation form of the qualitative difference —
  **EXACT — HUMAN PROOF** (elementary \(\{k\alpha\}=\{k\{\alpha\}\}\)
  for \(k\in\mathbb Z\); **COMPUTATIONALLY VERIFIED** on the
  existing first-difference sample)
- Reduction of the difference to \(\{n^{19/8}\}\) — fails; the
  torus distance to the smooth monomial is not \(o(1)\)
- Rated \(C'\gg 1\) as a qualitative kill — not claimed; that
  only kills character windows
- Equidistribution of \(\{v^{9/4}\}\) — not claimed

## Experiments

None new as a research module. The identity witness reuses
`first_difference_check` from
`research.juggler_sequence.horizontal_weyl` (odd pairs near
\(10^6\) and \(10^8\)) inside
`tests/research/juggler_sequence/test_v94_rate_free.py`. No Weyl
grid: the nil-lift already has \(124\) harmonics at \(\sqrt N\).

## Conjectures

None new. `juggler_tower_rate_free_equidistribution` stays
**ACTIVE**. The composition mismatch is recorded in its notes.
Conjectures V/HH stay PARKED.

## Counterexamples

None. The novelty hypothesis died by obstruction (hypothesis
mismatch and difference species), not by a counterexample orbit.

## Formalization

None. Lean-ifying Hardy-field membership or Mal'cev coordinates
ahead of an equidistribution theorem that would consume them is
machinery gravity.

## Results

Classification **V94_RATE_FREE_DOOR_UNBUILT**.

- **Published doors miss.** Richter needs Hardy times; Frantzikinakis
  needs floor in the time slot of a fixed nilrotation; Boshernitzan
  needs a Hardy function of \(n\). The instance is
  \(a^{f(\lfloor h(n)\rfloor)}\) with \(f\) nonlinear Hardy.
- **Unwind does not transfer**, even rate-free: the leftover
  \(\tfrac94 n^{15/8}\theta\) is not \(o(1)\).
- **Qualitative van der Corput does not cheapen the axis:** the
  difference is integer dilation of \(\{v^{5/4}\}\), not
  \(\{n^{19/8}\}\).
- No new ledger row: every surviving statement is `KNOWN` or a
  one-line corollary of `J-horizontal-axis-species`.

## Open questions

- Equidistribution of the floor-Hardy nil-orbit — still the
  active conjecture; the missing lemma is Hardy-of-floor
  composition for nil-orbits. External; not opened as a
  laboratory branch. The sibling three-term reading
  [juggler_v94_hardy_lift.md](juggler_v94_hardy_lift.md)
  is **CLOSE**: it recovers Lemma G and does not open a
  published door.
- Characteristic-factor self-similarity of floor-removal remains
  the named route-falsifier and stays external.

## Decision

**CLOSE.** The standing question is answered: the published
Hardy-nil theorems do not identify \(\{v^{9/4}\}\) without the
forbidden \(\theta\)-unwind, and qualitative van der Corput asks
for the same unbuilt composition. The rate-free conjecture stays
ACTIVE; this branch produced a placement record, not a method.
Best next question: none from this door; the live target remains
the rate-free conjecture as an external composition problem, and
characteristic factors are not opened from here.

## Publication assessment

Status: `ARCHIVED`. A placement record that names the missing
composition lemma. Not a paper claim. No Paper B edit.
