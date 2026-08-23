# Normalization complexity

Measures and families for the coefficient rewrite. No log-depth claim.

## Measures

| Measure | Meaning |
|---------|---------|
| rewrite count | number of abstract `→` steps used by a strategy |
| passes | Strategy A/B: one site per pass; Strategy C: one parallel round |
| sequential depth | Strategy A rewrite count |
| parallel depth | Strategy C pass count |
| peak `|c|` | max absolute coefficient seen |
| peak width | max length seen |
| max carry distance | sites touched in a run (here 1 per atomic step) |

Strategy D contributes 0 rewrites and is the integer-encoder baseline.

## Enumeration honesty

Full `width ≤ 12`, `|c| ≤ 5` is `11^12` and is **not** exact-enumerable.
Practical exhaustive boxes:

- `width ≤ 5` and `|c| ≤ 3`
- `width ≤ 8` and `|c| ≤ 2`

Targeted words: `width ≤ 30`, `|c| ≤ 20`. Balanced-word arithmetic uses
`|n| ≤ 10^6` where cheap. Large dumps belong under
`experiments/normalization/*.jsonl` (gitignored).

## Families

`3^k`, `3^k ± 1`, constant-`c` words, alternating signs, random words,
and sparse products (convolution before NF). Worst-case rewrite count
and carry chains are searched on the practical boxes only.

**OBSERVATION / REFUTED inequality.** Parallel depth is *not* always
at most sequential depth. Witness `(-2,-2,2)`: Strategy A uses 2
rewrites, Strategy C uses 3 rounds. No log-depth theorem.

## Finite-state class

Distinguish alphabets. Do not lift a finite bound to `ℤ`.

| Alphabet | Class | Status |
|----------|-------|--------|
| already trits | identity / strip high zeros | **PROVED** |
| fixed `[-B,B]` | LSD Mealy; carry stays in `[-B,B]` for `B ≥ 1`; single-coeff `|q| ≤ ⌊(B+1)/3⌋` | **PROVED** existence; Lean has the algebraic carry bound |
| unbounded `ℤ` | not one finite-state transduction | **PROVED** (carry scale follows `3^k`) |

The transducer zoo records these three rows. The bounded machine is
`BoundedNormalizeTransducer`.

## Add / mul / FMA

**PROVED** as value identities:

```text
normalize(P+Q) = encode(value(P)+value(Q))
normalize(P*Q) = encode(value(P)·value(Q))
value(normalize(PQ+R)) = value(normalize(normalize(PQ)+R))
```

Costs may differ. Fused FMA can save rewrites; staged NF of `PQ` can
also be cheaper on some inputs. There is **no** generic
sparsity-preservation theorem. Both savings and staged-cheaper
witnesses are searched by `bt.normtheory.discovery` and never
auto-promoted to **PROVED**.
