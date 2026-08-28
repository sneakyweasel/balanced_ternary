# Juggler minimal counterexample and predecessor closure

Status: **MINIMALITY_COMPLEX**

Standalone well-ordering phase on the exact Juggler floor-power map.
This is not a termination theorem. Closed local, symbolic, statistical,
and quotient branches stay closed. Finite-horizon evidence is not `Bad`.

Every statement below is labelled
`LOGICAL CONSEQUENCE` | `LEAN-CERTIFIED` | `EXACT COMPUTATION` |
`COMPUTATIONALLY OBSERVED` | `CANDIDATE CONJECTURE` | `COUNTEREXAMPLE`.
These are report labels. Ledger tags, when used, remain the seven
standard tags from [docs/README.md](../README.md).

## 1. Formal minimal-counterexample setup

`ReachesOne n` is the existing Lean predicate `∃ k, T^[k] n = 1`.

```text
Good(n)  := ReachesOne n
Bad(n)   := ¬ReachesOne n
```

Label: **LEAN-CERTIFIED** (`Good`, `Bad` in
`Problems.Juggler.MinimalClosure`). `Bad` is not proved decidable and
is not assumed decidable.

The computational proxy is strictly weaker:

```text
Bad_H(n) := T^[k] n ≠ 1 for all k ≤ H
```

`Bad_H(n)` does not imply `Bad(n)`. Label: **LOGICAL CONSEQUENCE**.

A hypothetical counterexample is a positive `n > 1` with `Bad(n)`.
Well-ordering supplies a least such value `n*`. Then every positive
`m < n*` is `Good`. Label: **LOGICAL CONSEQUENCE**. This is
`MinimalNonTerm` already in `Problems.Juggler.Minimal`. **LEAN-CERTIFIED**.

Minimality does *not* give a uniform finite bound on the stopping
times of the smaller good states. Label: **LOGICAL CONSEQUENCE**.

## 2. Exact logical consequences

If the orbit of `n*` ever visits `m < n*`, then `m` is `Good`, so `n*`
is `Good`. Therefore a minimal-bad orbit satisfies `T^[k] n* ≥ n*` for
every `k`. Label: **LEAN-CERTIFIED**
(`minimal_bad_barrier_constraint`, already `minimal_nonterm_iterate_ge`).

Local contraction `T(x) < x` is allowed as long as `T(x) ≥ n*`. The
forbidden event is a visit strictly below `n*`, not a descent relative
to the current state. Label: **LOGICAL CONSEQUENCE**.

`n*` is odd and at least `12`. The first image is odd. Every even
state on the orbit is at least `n*^2`. Start-`OE` is descent.
Label: **LEAN-CERTIFIED** (existing `Minimal.lean` normal form).

An immediate predecessor of a `Good` state is `Good`.
Label: **LEAN-CERTIFIED** (`good_of_good_successor`,
`good_of_predecessor_certificate`).

`n*` cannot lie in the even or odd inverse cell of any `m < n*`.
Label: **LEAN-CERTIFIED** (`minimal_bad_even_cell_exclusion`,
`minimal_bad_odd_cell_exclusion`). Both are corollaries of the
already-proved odd start plus odd expansion.

## 3. Barrier-surviving trajectories

For each start `n ≤ 4000`, `H_n` is the first time the
trajectory is strictly below `n`, or the horizon if no such time is
seen. This is a barrier against the *start*, not a first-return
census and not a new delay table.

Every `n` in `2..4000` drops below `n` inside the horizon.
`barrier_survival` is therefore false on the whole Phase-0 window.
Label: **EXACT COMPUTATION**. That is compatible with totality on
the window and is not a proof that `Bad` is empty.

Longest observed `H_n` in the window:

| 3889 | 77 | int[3350bits] | `OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOO` |
| 3547 | 70 | int[1049bits] | `OOOEOOOEOOOOOOOOEEEEOOOOOEOEEOEOOOOOOOEO` |
| 193 | 70 | int[900bits] | `OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOO` |
| 3271 | 69 | int[2460bits] | `OOEOOOOOOOEOEOOOOOOEEEEOEOOOOOOEEOOOEOOO` |
| 2681 | 69 | int[900bits] | `OOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOO` |
| 3439 | 62 | int[1045bits] | `OOOOOOOOOOEOEOOEOOOEEOOEEOOOEEOOEOEOOOOE` |
| 761 | 62 | int[851bits] | `OOOOOOOOOEEOEOEEOOEEOOOEOOOOEOOOEOEOOOEE` |
| 3085 | 62 | int[407bits] | `OOOOEOOOOOOEEEOEOOEOEEOOOOOEOOEEOEOOOOOO` |
| 3973 | 59 | int[1890bits] | `OOOOOOOEOOOOEEOOOOOOEOEOOEEOEOOOOOEOEOEO` |
| 3981 | 56 | int[840bits] | `OOOEOOOEOOOOOEEOEOEOOOOOEEEOEOEOOOOOOOEO` |
| 2247 | 56 | int[686bits] | `OOOOOOOOOEOOEOEOOOEOOEEOEEEOOEOOEOEOOOEO` |
| 3987 | 56 | int[443bits] | `OOOOOOEEEOOEOOOOOOOEOEEOOOOEEOOOEOOOEEEE` |

Label: **EXACT COMPUTATION**.

The barrier prefix of a terminating start is exactly the walk until
the first state `< n`. At the start itself, `Min_w(n) < n` coincides
with ordinary word contraction. The new inequality `Min_w(x) < n*`
for a later state `x > n*` is weaker than `T_w(x) < x`. Label:
**LOGICAL CONSEQUENCE**.

## 4. Two-step and block barrier analysis

On a realized two-step word the exact barrier tests against a lower
cut `b` are:

| word | `b ≤ T^2(x)` |
| --- | --- |
| `OE` | `b^4 ≤ x^3` |
| `EE` | `b^4 ≤ x` |
| `EO` | `b^2 ≤ ⌊√x⌋^3` |
| `OO` | automatic if `3 ≤ b ≤ x` |

Label: **LEAN-CERTIFIED** (`oe_barrier_pow`, `ee_barrier_pow`,
`eo_barrier_pow`, `oo_barrier_of_le`).

Finite check on `n = 2..4000`: counts `{'EO': 977, 'OO': 1009, 'EE': 1023, 'OE': 990}`;
failures `0`. Label: **EXACT COMPUTATION**.

At a minimal-bad start, `OE` is already impossible. A later `OE` from
`x ≥ n*` stays above `n*` if and only if `n*^4 ≤ x^3`. That is the
even-cell law `T(x) ≥ n*^2` rewritten through `T(x)^2 ≤ x^3`. It
excludes no new infinite family. Label: **LOGICAL CONSEQUENCE**.

For a block `O^a E^b` launched *at* `n*`, remaining above `n*` after
the even run is the same comparison `3^a ≥ 2^{a+b}` as the known
exponent envelope, up to floor error. That is not a new obstruction.
For a later state `x > n*` the same block may contract relative to
`x` and still stay above `n*`. Label: **LOGICAL CONSEQUENCE**.

`BARRIER_GREEN` is not awarded: no new block family is incompatible
with the permanent lower cut.

## 5. Minimality exclusions

If `[1, B] ⊆ Good`, then one-step predecessor closure adds exactly
the even integers `n` with `⌊√n⌋ ≤ B`, i.e. even `n < (B+1)^2`, and
adds no odd integer `> B`. Label: **LEAN-CERTIFIED**
(`even_good_of_sqrt_le`, `odd_not_pred_of_le`, `uncovered_odd`,
`uncovered_even_iff`).

Therefore

```text
U(B) ∩ (B, N]  =  {odd n : B < n ≤ N}
                 ∪ {even n : max(B, (B+1)^2) ≤ n ≤ N}
```

when `Good` contains `[1, B]`. Density tends to `1/2`, not to `0`.
Label: **LEAN-CERTIFIED** for the predicate; **EXACT COMPUTATION**
for the Phase-0 counts:

| B | scanned | formula | density |
| --- | --- | --- | --- |
| 11 | 3923 | 3923 | 0.9835 |
| 12 | 3910 | 3910 | 0.9804 |
| 36 | 3298 | 3298 | 0.8320 |
| 63 | 1968 | 1968 | 0.4999 |
| 100 | 1950 | 1950 | 0.5000 |
| 193 | 1903 | 1903 | 0.4999 |
| 255 | 1872 | 1872 | 0.4999 |
| 512 | 1744 | 1744 | 0.5000 |
| 1000 | 1500 | 1500 | 0.5000 |
| 2183 | 908 | 908 | 0.4997 |
| 3999 | 0 | 0 | 0.0000 |

A hypothetical `n*` lies in `U(n*-1)` because it is odd. One-step
closure of the smaller good interval does not catch it. Label:
**LEAN-CERTIFIED** (`minimal_bad_uncovered_one_step`).

## 6. Good-set predecessor closure

Define `PredClosure` inductively: `1` is closed, and any preimage of
a closed state is closed.

```text
PredClosure n  ↔  ReachesOne n
```

Label: **LEAN-CERTIFIED** (`predClosure_iff_reachesOne`).

This is the exact content of iterated `G ↦ G ∪ Pred(G)` starting at
`{1}`. It is a reparameterization of `Good`, not a new basin
geometry. `GOOD_CLOSURE_GREEN` as a *new inductive mechanism* is
false. Label: **COUNTEREXAMPLE** to “closure from 1 is a new
induction”.

Unbounded `PredClosure` is `ReachesOne`. The Phase-0 set is the
*window-restricted* inverse basin: `n ≤ N` whose path to `1` of
length `≤ r` stays inside `[1, N]`. That matches the computed
`G_r`: `True`. It is strictly
smaller than `{n : τ(n) ≤ r}`. Starts with `τ ≤ r` whose orbit
leaves the window include
`[25, 43, 45, 49, 53, 55, 59, 73]`.
Label: **EXACT COMPUTATION**. **COUNTEREXAMPLE** to “finite-N
closure is the stopping-time filtration”.

One extra even-cell layer above `N`, followed by odd re-entry,
would certify
`535` additional odd starts
`≤ N` whose image is an even `> N` in a certified cell. Examples:
`[253, 255, 257, 259, 261, 267, 273, 275, 277, 279, 281, 283, 291, 295, 297, 299]`. This is upward
propagation, not interval closure. Label: **EXACT COMPUTATION**.

## 7. Closure growth

| round | certified | prefix interval | components | largest gap |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 3999 |
| 1 | 2 | 2 | 1 | 3998 |
| 2 | 5 | 2 | 4 | 3992 |
| 3 | 26 | 2 | 25 | 3920 |
| 4 | 436 | 2 | 431 | 1600 |
| 5 | 500 | 2 | 473 | 1600 |
| 6 | 1023 | 8 | 987 | 671 |
| 7 | 1316 | 18 | 1258 | 123 |
| 8 | 1369 | 18 | 1278 | 123 |
| 9 | 1441 | 24 | 1342 | 123 |
| 10 | 1534 | 24 | 1433 | 123 |
| 11 | 1539 | 24 | 1428 | 123 |
| 12 | 1651 | 24 | 1540 | 119 |

At depth `12`: certified `1651` of
`4000`, uncovered `2349`, prefix
`24`, components
`1540`. Every `n ≤ 4000` reached `1`
inside the walk horizon: `True`; max
`τ` in the window is `80`. Label:
**EXACT COMPUTATION**.

The prefix `[1, F(r)]` is not a power of 3:
`True`. No closed form for `F(r)`
is proposed. `COVERAGE_GREEN` is not awarded. Label:
**COMPUTATIONALLY OBSERVED**.

`G_r ∩ [1, N]` is not a single interval. Label: **COUNTEREXAMPLE**
to interval closure.

## 8. Uncovered-set geometry

First uncovered value after each round (least `n` outside the
window-restricted inverse basin, not `τ(n) > r`):

| round | first gap | successor status | first two letters |
| --- | --- | --- | --- |
| 1 | 3 | successor_inside_window_uncertified | OO |
| 2 | 3 | successor_inside_window_uncertified | OO |
| 3 | 3 | successor_inside_window_uncertified | OO |
| 4 | 3 | successor_inside_window_uncertified | OO |
| 5 | 3 | successor_certified | OO |
| 6 | 9 | successor_certified | OO |
| 7 | 19 | successor_inside_window_uncertified | OE |
| 8 | 19 | successor_certified | OE |
| 9 | 25 | successor_inside_window_uncertified | OO |
| 10 | 25 | successor_inside_window_uncertified | OO |
| 11 | 25 | successor_inside_window_uncertified | OO |
| 12 | 25 | successor_inside_window_uncertified | OO |

Label: **EXACT COMPUTATION**. From round 9 the first gap freezes at
`25`, whose orbit leaves `[1, N]` (`25 → 125 → 1397 → 52214`). That
state is never certified at any depth inside the window. The leftover
set at infinite depth, for this `N`, is the starts whose path to `1`
exits `[1, N]`. That is neither `Bad` nor `Bad_H`. Odd cells remain
singletons; even cells fill square intervals.

## 9. Balanced-ternary observations, if any

First-gap least digits: `{0: 6, 1: 6}`. More than one trit
occurs, so the uncovered minima are not an lsd cylinder. Lengths
`[2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4]`. No closure boundary of the form
`(3^k ± 1)/2` appears. Balanced ternary is not used as a solving
coordinate. Label: **COMPUTATIONALLY OBSERVED**.

## 10. Candidate induction laws

No `CANDIDATE CONJECTURE` is opened.

The attractive schema “after `r` closure rounds, `[1, F(r)]` is
covered” fails already at small `r`: the certified set gains distant
even square-cells while leaving small odd gaps. The only exact unbounded recurrence is
`G_{r+1} = {n : T(n) ∈ G_r} ∪ G_r`, i.e. `τ(n) ≤ r+1`. Inside a
finite window it is the same rule restricted to targets already in
`[1, N]`. Label: **LOGICAL CONSEQUENCE**.

`MINIMAL_BAD_CONTRADICTION_GREEN` is false: `n*` is excluded from
`PredClosure` if and only if it is `Bad`, which is the assumption.
Label: **LEAN-CERTIFIED** (`minimal_bad_not_predClosure`).

## 11. Smallest counterexamples

Canonical hard starts in the window, with stopping time and barrier
time (not a new score):

| n | τ | H_n | peak | barrier word |
| --- | --- | --- | --- | --- |
| 3 | 6 | 5 | 36 | `OOOEE` |
| 9 | 7 | 5 | 140 | `OOEOE` |
| 37 | 17 | 15 | 24906114455136 | `OOOOEOOOEEOOEEE` |
| 193 | 73 | 70 | int[900bits] | `OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOOOEOOOOEEOOEOOEOEEOOEOOE...` |
| 425 | 67 | 46 | 8230847938518493917482830769503142723891695891144676325086026635806232664 | `OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE` |
| 761 | 66 | 62 | int[851bits] | `OOOOOOOOOEEOEOEEOOEEOOOEOOOOEOOOEOEOOOEEOOOOEOOOOEEEOOOEEEEOEE` |
| 2183 | 72 | 54 | int[19694bits] | `OOEOOOOEOOOOOOOOEOOOEOOOOOOOEOOOEEEOOOEEEEEEOEEOEEOOEE` |
| 3431 | 61 | 54 | int[4634bits] | `OOEOOOOEOOOOOEOEOOOOOEOOEOOOOOOEEEEOEEEOOOOEEEEOOOEOEE` |
| 3889 | 80 | 77 | int[3350bits] | `OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOOOEEOEOEEOEOEEOOOEEOEOOEE...` |

Pareto front of `(H_n, peak)` on `n ≤ 4000`:

| n | H_n | peak |
| --- | --- | --- |
| 3889 | 77 | int[3350bits] |
| 2183 | 54 | int[19694bits] |

Label: **EXACT COMPUTATION**. These are terminating starts. They
resemble a minimal-bad candidate only in having a long sojourn above
the start. Each of them does drop below the start, so none is
minimal-bad.

## 12. Lean targets

Formalized, sorry-free, in `formal/Problems/Juggler/MinimalClosure.lean`:

- `good_of_good_successor`
- `good_of_predecessor_certificate`
- `minimal_bad_even_cell_exclusion`
- `minimal_bad_odd_cell_exclusion`
- `minimal_bad_barrier_constraint`
- `oe_barrier_pow` / `ee_barrier_pow` / `eo_barrier_pow`
- `PredClosure` / `predClosure_iff_reachesOne`
- `minimal_bad_not_predClosure`

Not formalized, and not claimed: `good_interval_closure`,
`closure_growth_theorem`, `minimal_bad_impossible`.

## 13. Decision

Classification: **MINIMALITY_COMPLEX**.

Unbounded predecessor closure from {1} is ReachesOne. The finite-N experiment is the inverse basin of 1 inside [1, N], which is strictly smaller than {n : τ(n) ≤ r} because high-peak orbits leave the window. U(B) is all odds > B together with evens >= (B+1)^2, so it is not sparse. Two-step barriers are floor-sqrt identities. No interval-growth recurrence and no contradiction to a minimal bad state appear.

`MINIMALITY_GREEN` is not awarded: the new Lean lemmas package
existing minimality facts or reparameterize `ReachesOne`.
`BARRIER_GREEN` is not awarded. `GOOD_CLOSURE_GREEN` is not awarded.
`COVERAGE_GREEN` is not awarded. `MINIMAL_BAD_CONTRADICTION_GREEN`
is not awarded.

Branch status in the dossier: **CLOSE**.

Phase 1 (`N = 10^5`) is not launched. A larger window only moves the
escape threshold; it does not create an interval-growth law.
