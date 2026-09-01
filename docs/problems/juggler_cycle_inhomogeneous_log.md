# Juggler inhomogeneous Wu–Wang form

Status: **ARCHIVED** (Phase 0 decided)

The unused piece of Wu–Wang after Attacks A/B/C
([juggler_cycle_fan_multipoint.md](juggler_cycle_fan_multipoint.md),
[juggler_cycle_padic_coupling.md](juggler_cycle_padic_coupling.md),
[juggler_cycle_walk_fan_growth.md](juggler_cycle_walk_fan_growth.md)).
The published measure is for \(1,\log 2,\log 3\), not merely for
the ratio. Attack C used only the homogeneous case \(p=0\). Does
an exact CycleMin identity produce a genuinely independent
nonzero integer \(p\)? Not a Baker leftover-killer, not a floor
raise, not a Paper A edit, and not a halt theorem.

## Problem

Wu–Wang give
\(\lvert p+b\log 2+c\log 3\rvert\ge H^{-4.1163051-\varepsilon}\).
Two-log finance is the \(p=0\) specialisation
\(\Lambda=o\log 3-L\log 2\). The literature search asked whether
floor/cell geometry can generate a third coefficient that this
reduction cannot see. If yes, the inhomogeneous cases might
squeeze a leftover that the ratio bound leaves standing.

## Exact statement

**The exact identities are homogeneous
(EXACT — HUMAN PROOF / REPARAMETERIZATION).**
`global_defect_identity` is \(n^{3^o}=T_w(n)^{2^L}+\Delta_w(n)\).
On a return, `image_eq_start_defectRatio` gives
\(\Delta_w(n)=n^{2^L}(n^G-1)\) with \(G=3^o-2^L\), so the
multiplicative remainder satisfies \(\log R=G\log n\), not an
integer. The block exponent sum is
\(\sum_i(a_i\log 3-(a_i+r_i)\log 2)=\Lambda\) identically
([juggler_cycle_exponent_budget.md](juggler_cycle_exponent_budget.md)).
The integer \(1\) in Wu–Wang is the real number \(1\), not a
floor remainder and not \(\log n\).

**Integer gap (EXACT — HUMAN PROOF).**
For every integer \(p\neq 0\),
\(\lvert p+\Lambda\rvert\ge 1-\lvert\Lambda\rvert\). On every
leftover, \(\lvert\Lambda\rvert=\lvert\log(1-\theta)\rvert<1/2\),
so every unscaled inhomogeneous form is at least \(1/2\), while
\(\lvert\Lambda\rvert=\theta+O(\theta^2)\) is the finance gap.

**Clearing is the same approximation
(EXACT — HUMAN PROOF / REPARAMETERIZATION).**
Choosing \(k=\mathrm{round}(1/\Lambda)\) after the fact makes
\(\lvert -1+ko\log 3-kL\log 2\rvert=\lvert k\Lambda-1\rvert\)
smaller than \(\lvert\Lambda\rvert\). The cycle does not produce
the integer \(-1\); any small \(\Lambda\) has such a \(k\). This
is Baker-dominance again: at \(L=19\),
\(\lvert k\Lambda-1\rvert=2.78\cdot 10^{-3}\) against a
diagnostic Wu–Wang floor \(H^{-4.116}\approx 1.1\cdot 10^{-13}\)
(\(k=74\), \(H=1406\), ratio \(2.52\cdot 10^{10}\)). At
\(L=176251\) the ratio is \(1.20\cdot 10^{38}\).

**Slogan.** An exact CycleMin identity produces a Wu–Wang form
with \(p\neq 0\) that is forced smaller than two-log finance —
**REFUTED**.

No cycle of any length — not claimed.

## Current literature

- Wu–Wang measure for \(1,\log 2,\log 3\) — **KNOWN**
  (`wu-wang-2014-irrationality-measure-log3`). Attack C used the
  \(p=0\) corollary as a fan-width cap
- Global defect / return identity —
  **EXACT — LEAN VERIFIED**
  (`global_defect_identity`, `image_eq_start_defectRatio`)
- Exponent-budget sum \(=\Lambda\) — **REPARAMETERIZATION**
- Baker/Rhin leftover-killer — **REFUTED**
- Attacks A and B — **CLOSE**; Attack C — **PROMOTE**
- Every start reaches 1 — not claimed

Project relationship: **refuted** as a third-coefficient squeeze;
the published measure remains **known**.

## Branch budget

```text
Mathematical target     Does any exact CycleMin identity produce
                        |p + b log 2 + c log 3| with p ≠ 0 forced
                        smaller than homogeneous Lambda?
Novelty hypothesis      The integer 1 in Wu-Wang is a new
                        coefficient that two-log finance cannot see
Falsifier               Every identity is p = 0; |p+Lambda| >=
                        1-|Lambda| for p ≠ 0; clearing is the
                        same Lambda after the fact
Existing machinery      global_defect_identity,
                        image_eq_start_defectRatio, exponent
                        budget, Attack C, Baker REFUTED
Maximum Phase-0 scope   One probe: integer shifts and k-clearing
                        on seven leftover seeds. No Lean, no
                        floor, no Baker solver, no Paper A edit
Promotion criterion     A forced p ≠ 0 form smaller than Lambda
                        and below the Wu-Wang floor
Stop criterion          Homogeneous identities plus the integer
                        gap, or clearing is Baker-dominance
```

## Balanced-ternary formulation

None required.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(\Lambda=-\log(1-\theta)=o\log 3-L\log 2\) —
  **EXACT — HUMAN PROOF**
- \(\lvert p+\Lambda\rvert\ge 1-\lvert\Lambda\rvert\) for
  \(p\neq 0\) — **EXACT — HUMAN PROOF**
- Unscaled inhomogeneous form smaller than \(\lvert\Lambda\rvert\)
  — **REFUTED** on the seven seeds
- Forced third coefficient from \(\Delta_w\) / cells —
  **REPARAMETERIZATION** (\(\log R=G\log n\))
- No cycle of any length — not claimed

## Experiments

- Probe: `research.juggler_sequence.cycle_inhomogeneous_log`
- Artifacts: `data/research/juggler/cycle_inhomogeneous_log/summary.json`
- Tests: `tests/research/juggler_sequence/test_cycle_inhomogeneous_log.py`

No CLI, no Lean, no floor work.

## Conjectures

`juggler_inhomogeneous_ww_beats_finance` — **REFUTED**.

## Counterexamples

- On \(L=19,84,569,1054,25781,50508,176251\), the smallest
  unscaled form is \(\lvert\Lambda\rvert\); the next is
  \(\lvert-1+\Lambda\rvert=1-\Lambda\in[0.986,1)\).
- Clearing \(k=\mathrm{round}(1/\Lambda)\) is smaller than
  \(\lvert\Lambda\rvert\) (as any small \(\Lambda\) permits) and
  stays at least \(2.52\cdot 10^{10}\) above the diagnostic
  Wu–Wang floor.

## Formalization

None. The return identity is already in `NormalizedDefect.lean`.
No new Lean, no `sorry`. Paper A is unchanged.

## Results

Classification **INHOMOGENEOUS_LOG_CLOSED**.

- Integer gap holds with equality at \(p=-1\) on all seven seeds
- Homogeneous \(\Lambda\) is the unique smallest unscaled form
- Clearing ratios \(\mathrm{form}/H^{-4.116}\) from
  \(2.52\cdot 10^{10}\) (\(L=19\)) to \(1.20\cdot 10^{38}\)
  (\(L=176251\))
- \(\log R=G\log n\) is the global-defect return, already Lean

## Open questions

None from the third Wu–Wang coefficient. Do not import a sharper
measure of the same shape. The Diophantine programme from the
literature search is complete: A CLOSE, B CLOSE, C PROMOTE
(width only), inhomogeneous CLOSE. The fan obstruction remains
the open unboundedness of the partial quotients of
\(\log 2/\log 3\).

## Decision

**CLOSE.** The integer \(1\) in Wu–Wang is not a floor remainder.
Every exact cycle identity is the homogeneous form already priced
by finance; every nonzero integer shift is order \(1\); clearing
denominators is the same \(\Lambda\) and is Baker-dominance. The
literature’s “look at the third coefficient” does not produce a
new Juggler constraint.

Best next question: none from this literature programme. The
frontier is the classical OPEN unboundedness of the dangerous
partial quotients of \(\log 2/\log 3\).

## Publication assessment

Status: `ARCHIVED`.

A one-page elimination of the inhomogeneous reading of Wu–Wang.
The integer-gap inequality is exact and trivial; the census is
finite. Not a paper candidate and not a halt theorem.
