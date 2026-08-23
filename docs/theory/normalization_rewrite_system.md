# Normalization rewrite system

Claim layers: **PROVED**, **VERIFIED COMPUTATIONALLY**, **CONJECTURE**,
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

**PROVED.** The finite-support sequence `(|c_0|, |c_1|, …)` strictly
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

**VERIFIED COMPUTATIONALLY.** Every critical pair with
`a,b ∈ [-8,8]` joins, and every word in the box `width ≤ 3`, `|c| ≤ 2`
is locally confluent (bounded descendant search).

If the system is terminating and locally confluent, Newman’s lemma
gives global confluence. Lean does **not** claim that conjunction.
Expected unique irreducible form: the canonical balanced word of
`value(P)`. Python Strategy A/B/C/D agree on that word on the
enumerated boxes.

## Normal form

**PROVED.**

- `irreducible(P)` iff every stored coefficient is a trit.
- `normalize_A(P)` equals `encode(value(P))` as LSD digits
  (`from_digits_lsd`).
- `value(normalize(P)) = value(P)`.

This is unique balanced expansion restated as a rewrite NF. The
rewrite-theoretic packaging is the extra structure.

## Strategies

| Name | Rule | Termination |
|------|------|-------------|
| A | lowest legal site | **PROVED**; equals `encode` |
| B | highest legal site | **PROVED** by the same lex rank |
| C | maximal LSD-greedy non-adjacent independent set per round | **PROVED** (each round is ≥1 abstract step) |
| D | `encode(value)` | 0 rewrite steps |

A and B need not have the same rewrite count
(**VERIFIED COMPUTATIONALLY** / typically **REFUTED** equality).
C’s *pass* count is parallel depth. It is **not** always ≤ A’s
sequential depth: `(-2,-2,2)` has parallel depth 3 and sequential
depth 2. Not a log-depth theorem.
