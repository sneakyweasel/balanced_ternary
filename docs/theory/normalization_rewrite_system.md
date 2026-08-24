# Normalization rewrite system

Claim layers: **EXACT — HUMAN PROOF**, **COMPUTATIONALLY VERIFIED**, **CONJECTURE**,
**OBSERVATION**, **REFUTED**.

## Rule

A site `i` is legal iff `c_i ∉ {-1,0,+1}`. The unique balanced residue is

```text
r = ((c + 1) mod 3) - 1 ∈ {-1,0,+1}
q = (c - r) / 3
```

The step writes `r` at `i` and adds `q` to `c_{i+1}` (extending the word
if needed). There is no rewrite when `c_i` is already a trit.

The abstract relation `P → P'` is **one** legal step at **some** index.
Sweep order is a strategy, not part of the rule.

## Termination

**EXACT — HUMAN PROOF.** The finite-support sequence `(|c_0|, |c_1|, …)` strictly
decreases in lexicographic order: a step at `i` leaves positions `< i`
unchanged and replaces `|c_i| ≥ 2` by `|r| ≤ 1`. Lexicographic order on
finite-support `ℕ`-sequences is well-founded, so every finite word has
no infinite `→` path.

**REFUTED** as a rank: the weighted measure `Σ |c_i| α^i` with `α = 3/2`
*increases* on `[2] → [-1, 1]`. Keep that witness; do not use the
weighted L1 as a termination argument.

Lean records the lex decrease at the LSD and the inductive tail step,
plus `3 |DZ n| ≤ |n| + 1`.

## Confluence

The only overlapping redexes are sites `i` and `i+1`: a step at `i`
writes `c_{i+1}`. Disjoint sites `|i-j| ≥ 2` commute.

**COMPUTATIONALLY VERIFIED.** Every critical pair with
`a,b ∈ [-8,8]` joins, and every word in the box `width ≤ 3`, `|c| ≤ 2`
is locally confluent (bounded descendant search).

**EXACT — HUMAN PROOF** (Lean, modulo high-zero stripping, matching Python
`CoeffWord`). Unique stripped trit form is `encodeZ(value(P))`.
Strategy A is a rewrite path to that form, so every fork joins there.
Raw lists may differ by trailing zeros (`[-5,2]` → `[1,0]` vs
`[1,0,0]`); after `stripHigh` they are the same word.

Expected unique irreducible form: the canonical balanced word of
`value(P)`. Python Strategy A/B/C/D agree on that word on the
enumerated boxes.

## Normal form

**EXACT — HUMAN PROOF.**

- `irreducible(P)` iff every stored coefficient is a trit.
- `normalize_A(P)` equals `encode(value(P))` as LSD digits
  (`from_digits_lsd`).
- `value(normalize(P)) = value(P)`.

This is unique balanced expansion restated as a rewrite NF. The
rewrite-theoretic packaging is the extra structure.

## Strategies

| Name | Rule | Termination |
|------|------|-------------|
| A | lowest legal site | **EXACT — HUMAN PROOF**; equals `encode` |
| B | highest legal site | **EXACT — HUMAN PROOF** by the same lex rank |
| C | maximal LSD-greedy non-adjacent independent set per round | **EXACT — HUMAN PROOF** (each round is ≥1 abstract step) |
| D | `encode(value)` | 0 rewrite steps |

A and B need not have the same rewrite count
(**COMPUTATIONALLY VERIFIED** / typically **REFUTED** equality).
C’s *pass* count is parallel depth. It is **not** always ≤ A’s
sequential depth: `(-2,-2,2)` has parallel depth 3 and sequential
depth 2. Not a log-depth theorem.
