# Juggler stopping-time prefix

Status: **STOPPING_PREFIX_COMPLEX**

Standalone Phase-0 on the unbounded stopping-time prefix of the exact
Juggler floor-power map. This is not a termination theorem. The closed
windowed inverse-basin census stays closed.

Every statement below is labelled
`LOGICAL CONSEQUENCE` | `LEAN-CERTIFIED` | `EXACT COMPUTATION` |
`COMPUTATIONALLY OBSERVED` | `COUNTEREXAMPLE`.
These are report labels. Ledger tags, when used, remain the seven
standard tags from [docs/README.md](../README.md).

## 1. Object

`T` is `floorPower`: even `⌊√n⌋`, odd `⌊n^{3/2}⌋`. `τ(1)=0` and
`τ(n)` is the first `k` with `T^k(n)=1`. Label:
**LEAN-CERTIFIED** for the map; **EXACT COMPUTATION** for `τ` on
`n ≤ 4000`.

```text
M(N)   := max_{n ≤ N} τ(n)
F_τ(r) := max { N : M(N) ≤ r }
b_r    := F_τ(r) + 1
```

This identity is the definition of the inverse of a nondecreasing
running maximum. Label: **LOGICAL CONSEQUENCE**. **REPARAMETERIZATION**
of `τ`, not a new induction.

## 2. Window census

Every `n ≤ 4000` reaches `1` inside horizon
`10000`: `True`. Max `τ` is
`80`. Therefore `F_τ(80) =
4000`. Label: **EXACT COMPUTATION**. That is the
already-recorded window totality from the closed minimal-counterexample
branch, not a proof that `F_τ(r)→∞`.

Finite-depth even cell: if `[1, F] ⊆ {τ ≤ r}` then every even
`n < (F+1)^2` in the window has `τ(n) ≤ r+1`:
`True`. Label: **EXACT COMPUTATION**. The
unbounded `Good` form is `even_good_of_sqrt_le`
(**LEAN-CERTIFIED**). One-step closure still adds no odd `n > F`
(`odd_not_pred_of_le`, **LEAN-CERTIFIED**).

First gaps with `F_τ(r) ≥ 2` and `b_r ≤ N` are odd:
`True` (`79` rows, exceptions
`[]`). Label: **EXACT COMPUTATION**.

## 3. Prefix table

Sampled `F_τ(r)` (full table in `data/research/juggler/stopping_prefix/prefix.csv`):

| r | F_τ | b_r | ratio | plateau |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 2.0000 | False |
| 5 | 2 | 3 | 4.0000 | False |
| 10 | 24 | 25 | 1.5000 | False |
| 15 | 36 | 37 | 1.0000 | True |
| 20 | 162 | 163 | 1.0000 | True |
| 25 | 162 | 163 | 1.0000 | True |
| 30 | 162 | 163 | 1.0000 | True |
| 35 | 162 | 163 | 1.0000 | True |
| 40 | 162 | 163 | 1.0000 | True |
| 45 | 192 | 193 | 1.0000 | True |
| 50 | 192 | 193 | 1.0000 | True |
| 55 | 192 | 193 | 1.0000 | True |
| 60 | 192 | 193 | 1.0000 | True |
| 65 | 192 | 193 | 1.0000 | True |
| 70 | 192 | 193 | 1.0000 | True |
| 75 | 1154 | 1155 | 1.0000 | True |
| 80 | 4000 | 4001 | 1.0000 | True |

Plateau fraction `0.8625`
(`69` of `80` steps). Max one-step
ratio `5.8229`. Label: **EXACT COMPUTATION**.

Side-by-side with the closed windowed inverse-basin prefix
`maximum_certified_interval`:

| r | F_τ | F_window | F_τ − F_window |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 2 | 2 | 0 |
| 3 | 2 | 2 | 0 |
| 4 | 2 | 2 | 0 |
| 5 | 2 | 2 | 0 |
| 6 | 8 | 8 | 0 |
| 7 | 18 | 18 | 0 |
| 8 | 18 | 18 | 0 |
| 9 | 24 | 24 | 0 |
| 10 | 24 | 24 | 0 |
| 11 | 36 | 24 | 12 |
| 12 | 36 | 24 | 12 |

`F_τ` and the windowed `F` agree only at the smallest depths. The
windowed prefix freezes at `24` because `25` leaves `[1, 4000]`. The
unbounded prefix continues because `τ(25)` is finite. Label:
**EXACT COMPUTATION**. **COUNTEREXAMPLE** to “the two prefixes are the
same sequence”.

## 4. First gaps

Each newly appearing `b_r ≤ N`:

| b | r | F_prev | τ | parity | word | T | T≤F | entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 1 | even | EO | 1 | True | 1 |
| 3 | 1 | 2 | 6 | odd | OO | 5 | False | 5 |
| 9 | 6 | 8 | 7 | odd | OO | 27 | False | 5 |
| 19 | 7 | 18 | 9 | odd | OE | 82 | False | 2 |
| 25 | 9 | 24 | 11 | odd | OO | 125 | False | 5 |
| 37 | 11 | 36 | 17 | odd | OO | 225 | False | > |
| 77 | 17 | 76 | 19 | odd | OO | 675 | False | > |
| 163 | 19 | 162 | 43 | odd | OO | 2081 | False | > |
| 193 | 43 | 192 | 73 | odd | OO | 2681 | False | > |
| 1119 | 73 | 1118 | 75 | odd | OE | 37432 | False | 2 |
| 1155 | 75 | 1154 | 80 | odd | OO | 39253 | False | 8 |

`entry` is the first `j ≤ 8` with `T^j(b) ≤ F_prev`, or
`>` if none. Odd first gaps have `T(b) > F_prev`: their one-step image
leaves the certified interval. Label: **EXACT COMPUTATION**.

No candidate congruence or two-letter motif predicts the next `b`
without computing `τ(b)`. Label: **COMPUTATIONALLY OBSERVED**.

## 5. Growth tests

Diagnostic only. Superlinear test `F(r+k) ≥ F(r)^α`:

| k | α | hits | eligible | density |
| --- | --- | --- | --- | --- |
| 1 | 1.5 | 1 | 79 | 0.0127 |
| 1 | 2.0 | 1 | 79 | 0.0127 |
| 2 | 1.5 | 2 | 78 | 0.0256 |
| 2 | 2.0 | 2 | 78 | 0.0256 |
| 3 | 1.5 | 4 | 77 | 0.0519 |
| 3 | 2.0 | 3 | 77 | 0.0390 |
| 4 | 1.5 | 5 | 76 | 0.0658 |
| 4 | 2.0 | 4 | 76 | 0.0526 |

A high density here would still not be a lemma: a jump after a late
odd is certified is “`τ(b)` is finite”, the window fact. Label:
**COMPUTATIONALLY OBSERVED**.

## 6. Lean

Cited, not added, from `Problems.Juggler.MinimalClosure`:

- `even_good_of_sqrt_le`
- `odd_not_pred_of_le`

Sorry-free: `True`. Not formalized, and not
claimed: `goodAt_interval_amplification`, `prefix_growth_theorem`.

## 7. Decision

Classification: **STOPPING_PREFIX_COMPLEX**.

F_τ is the definitional inverse of the running-max of τ. First gaps are odd expanders whose images leave the previous prefix; no uniform k≤4 entry exists. Plateaus cover 0.863 of depth steps. Window totality F_τ(max τ)=N is the already-recorded fact that every n≤4000 reaches 1, not a coverage theorem.

`PREFIX_AMPLIFICATION_GREEN` is not awarded. `RECORD_LADDER_UNEXPLAINED`
is not awarded. Branch status: **CLOSE**.

Phase 1 (`N = 10^5`) is not launched. A larger window lengthens the
record ladder of `τ` and does not isolate an amplification lemma.
