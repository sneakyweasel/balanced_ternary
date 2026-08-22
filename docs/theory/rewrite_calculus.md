# Rewrite calculus

**Status of this page:** a sound, classified rewrite system. Global
confluence of the full expression language is **not** claimed.

## Historical inspiration

Setun-70 evaluated postfix mathematical expressions. That motivates a
term language; it does not supply rewrite theorems.

## Existing mathematics

Operator-word identities already lived in
`research.operator_dynamics.algebra.REWRITE_RULES`
([operator_algebra.md](../operator_algebra.md)). The canonical table is
now `bt.calculus.rewrite.WORD_REWRITE_RULES`; the research module
re-exports it.

## Our formalization

Expression ADT (`bt.calculus.expressions`):

```text
Expr ::= Int | Trit | Add | Mul | Neg | D | I- | I0 | I+ | S | Nrm | Cmp3 | Select3
```

`evaluate : Expr → ℤ` is exact. `I0` rewrites to `S`.

**Tree rules** (each **PROVED / LEAN VERIFIED** as an integer identity):

| Rule | Lean |
|------|------|
| `D(I_a(x)) → x` | `rewrite_D_I` |
| `D(S(x)) → x` | `rewrite_D_S` |
| `N(N(x)) → x` | `rewrite_N_N` |
| `N(S(x)) → S(N(x))` | `rewrite_N_S` |
| `I0(x) → S(x)` | `rewrite_I0_S` |
| `N(I-(x)) → I+(N(x))` | `rewrite_N_Im` |
| `N(I+(x)) → I-(N(x))` | `rewrite_N_Ip` |

**Termination (operator fragment `{D, I_a, S, N}`).**
Innermost contraction of the rules above terminates: each `D(I_a)` /
`D(S)` / `N(N)` strictly decreases size; `I0 → S` does not increase
size and is applied once; `N` moving inward past a constructor
decreases the number of constructors above an `N`. This is a
**strategy**, not a proof that every rewrite order terminates once
commutation rules for the larger operator monoid are included.

**Confluence.**
On the operator fragment, the critical pairs we checked
(`D(I0(x))` vs `D(S(x))`; `N(N(S(x)))` vs `N(S(N(x)))`) join.
This is **VERIFIED COMPUTATIONALLY** on closed integer seeds and by
the Lean identities, not a Knuth–Bendix certificate for a larger
signature including `Add`/`Mul`/`W`.

**Word rules** remain sound on the intersection of domains. Two-way
commutation rules (`N∘S = S∘N` and converse) are marked
`simplifying=False` and `reversible=True`. The full word table is
**not** claimed confluent.

## Computational observations

`D(I+(D(I-(x))))` innermost-normalizes to `x` (not `D(x)`), because
`D ∘ I_a = id` twice. Identity discovery clusters closed unary terms; labels
are only `COMPUTATIONALLY VERIFIED`, `CONJECTURE`, or `REFUTED`.

## Conjectures

Whether the operator fragment has a unique normal form for every
open term (not just closed integers) is a small term-rewriting
question worth a dedicated proof. Not assumed.
