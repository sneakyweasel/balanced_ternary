# Balanced-ternary normalization

Master record for Milestone 14. Claim labels have the usual meaning.
This is **core mathematics**, not a Setun emulator and not Collatz.
Collatz remains a client of the library.

The object is an arbitrary integer coefficient vector

```text
P = Σ_i c_i 3^i,    c_i ∈ ℤ,   LSD-first
```

and the unique irreducible form of `P` under the local carry rewrite
`c = 3q + r` with `r ∈ {-1,0,+1}`.

## Honesty

**Standard signed-digit fact.** Every integer has a unique canonical
balanced-ternary expansion. Strategy A agreeing with `encode(value(P))`
is that uniqueness, packaged as a rewrite normal form.

**What might be paper-shaped.** The abstract one-step relation `P → P'`
(independent of sweep order), the lexicographic termination rank on
`(|c_0|, |c_1|, …)`, overlapping critical pairs, parallel depth,
finite-state classification *by alphabet bound*, and the FMA cost gap
between `normalize(PQ+R)` and `normalize(normalize(PQ)+R)`.

Do not advertise a log-depth theorem. Do not lift a finite-`B`
transducer to unbounded integer coefficients.

## Objects

| Object | Meaning |
|--------|---------|
| `CoeffWord` | LSD-first `List[ℤ]`, high zeros stripped except `[0]` |
| `value(P)` | `Σ c_i 3^i` |
| `balanced_divmod(c)` | unique `(r,q)` with `c = 3q + r`, `r` a trit |
| `P → P'` | one legal step at some index `i` with `c_i ∉ {-1,0,+1}` |
| Strategy A | LSD→MSD; **PROVED** equal to `encode(value(P))` |
| Strategies B, C | MSD-down and parallel non-adjacent rounds |
| Strategy D | `encode(value)` with zero rewrite steps |

`rewrite_sum` in `bt.normalization` is **not** this function. It remains
the addition helper on `[-3,3]`. On that interval the two maps agree.
`rewrite_sum(5)` is still `(2,1)`, which is not a trit.

`BTPolynomial` still requires trit coefficients. Expression-tree
normalization stays in `bt.calculus.normalization`.

## Normal-form theorem

**PROVED** (Python + Lean value/step/NF):

```text
value(P → P') = value(P)
irreducible(P)  iff  every stored coefficient is a trit
normalize_A(P)  =  digits of encode(value(P))
value(normalize(P)) = value(P)
```

Lean proves global confluence **modulo high-zero stripping**
(`BTCalculus/Confluence.lean`): unique stripped trit NF, Strategy A
reaches it, overlapping sites `i` / `i+1` join. Raw `[1,0]` vs
`[1,0,0]` is the `[-5,2]` witness that stripping is required.

## Pointers

- [Rewrite system](normalization_rewrite_system.md)
- [Complexity](normalization_complexity.md)
- [Setun subset](setun_normalization.md)
- [Calculus](balanced_ternary_calculus.md)
- Package: `src/bt/normtheory/`
- Lean: `formal/BTCalculus/Normalization.lean`, `formal/BTCalculus/Confluence.lean`
- CLI: `btprime normalize …`
