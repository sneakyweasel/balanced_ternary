# Rewrite calculus

**Status of this page:** a sound, classified rewrite system. The
operator fragment `{D, I_a, S, N}` under the tree rules below has a
unique syntactic normal form, and those irreducibles inject into
integer functions (**PROVED**). Global confluence of the full
expression language (`Add` / `Mul` / `W` / the large word table) is
**not** claimed. Coefficient-word confluence
([BTN-confluence](theorem_ledger.md), `BTCalculus/Confluence.lean`) is
a different object.

## Historical inspiration

Setun-70 evaluated postfix mathematical expressions. That motivates a
term language; it does not supply rewrite theorems.

## Existing mathematics

Operator-word identities already lived in
`research.operator_dynamics.algebra.REWRITE_RULES`
([operator_algebra.md](../operator_algebra.md)). The canonical table is
now `bt.calculus.rewrite.WORD_REWRITE_RULES`; the research module
re-exports it. The word table already records `N∘D = D∘N` as a
reversible non-simplifying commutation. The tree rule below is the
terminating orientation of that identity.

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
| `N(D(x)) → D(N(x))` | `rewrite_N_D` |

`Nrm(x) → x` is in `TREE_RULES` as a destructor. The engine also
contracts `N(I0(x)) → S(N(x))`; that step is `I0 → S` followed by
`N(S) → S(N)`, not an extra primitive.

Without `N(D) → D(N)`, the trees `N(D(x))` and `D(N(x))` are distinct
irreducibles that agree under `evaluate`. That is the recorded
refutation of semantic canonicity for the smaller rule set
([BTC-op-fragment-semantic-nf](theorem_ledger.md)). The oriented
commute closes the gap.

## Termination (operator fragment `{D, I_a, S, N}`)

Every one-step tree contraction, at any redex, strictly decreases the
lexicographic rank

```text
(I0-count, N-inversion, size)
```

where `N-inversion` is the number of pairs `(N-node, pushable
descendant)` and a constructor is pushable when it is `S`, `I-`, `I+`,
`I0`, or `D`.

- `D(I_a)` / `D(S)` / `N(N)` / `Nrm → id` delete constructors, so they
  drop `size` (and never raise the first two coordinates).
- `I0 → S` drops `I0-count` by one; `S` is also pushable, so
  `N-inversion` is unchanged.
- `N(S)`, `N(I-)`, `N(I+)`, `N(D)` (and the engine shortcut `N(I0)`)
  move `N` inward past one pushable constructor and drop
  `N-inversion` by one.

The rank is well-founded on `ℕ³`. This is termination of **every**
rewrite order on the fragment, not only innermost contraction.

## Local confluence and unique syntactic NF

The system is left-linear. The only non-variable overlaps of two
left-hand sides are:

| Peak | Contractions | Join |
|------|----------------|------|
| `D(I0(x))` | `→ x` and `→ D(S(x))` | `x` |
| `N(N(N(x)))` | both `→ N(x)` | `N(x)` |
| `N(N(S(x)))` | `→ S(x)` and `→ N(S(N(x)))` | `S(x)` |
| `N(N(I-(x)))` | `→ I-(x)` and `→ N(I+(N(x)))` | `I-(x)` |
| `N(N(I+(x)))` | `→ I+(x)` and `→ N(I-(N(x)))` | `I+(x)` |
| `N(I0(x))` | `→ S(N(x))` and `→ N(S(x))` | `S(N(x))` |
| `N(N(I0(x)))` | `→ I0(x)` and `→ N(S(N(x)))` | `S(x)` |
| `N(N(D(x)))` | `→ D(x)` and `→ N(D(N(x)))` | `D(x)` |
| `N(D(I_a(x)))` | `→ N(x)` and `→ D(N(I_a(x)))` | `N(x)` |
| `N(D(S(x)))` | `→ N(x)` and `→ D(N(S(x)))` | `N(x)` |

No other left-hand side has a non-variable proper subterm that unifies
with a left-hand side: `I-`, `I+`, and `S` are never themselves a
left-hand side, and `Nrm` does not occur in any other left-hand side.
Disjoint redexes commute because every rule is left-linear.

Local confluence plus termination gives confluence (Newman). Every
term of the fragment therefore has a unique syntactic normal form
([BTC-op-fragment-nf](theorem_ledger.md)). It is not Lean-verified:
`formal/BTCalculus/Rewrite.lean` contains the integer soundness
identities, not a rewrite-relation Newman proof, and
`BTCalculus/Confluence.lean` is the coefficient-word system.

## Normal-form grammar

A term is irreducible iff it has no `I0` or `Nrm`, no `D` immediately
above `I_a` or `S`, and no `N` immediately above `N`, `S`, `I-`, `I+`,
`I0`, or `D`. Equivalently `N` is pushed all the way to the hole, then
only `D`s may wrap the core, then only `I±`/`S` may wrap that:

```text
NF    ::= Prefs Depth
Prefs ::= ε | I-(Prefs) | I+(Prefs) | S(Prefs)
Depth ::= x | N(x) | D(Depth)
```

So every irreducible is `Pref_{a_1,…,a_m} ∘ D^k ∘ N^ε` with
`a_i ∈ {-,0,+}`, `I_0` written `S`, `k ≥ 0`, and `ε ∈ {0,1}`.

## Semantic completeness

These irreducibles inject into maps `ℤ → ℤ`
([BTC-op-fragment-complete](theorem_ledger.md)). As functions,

```text
t(x) = A + 3^m · (−1)^ε · D^k(x)
```

where `A = Σ_i a_i 3^{m-i}` is the unique length-`m` balanced word
`(a_1,…,a_m)`. If two such presentations agree on `ℤ`, evaluate at `0`
to get `A = B`, then `3^m σ D^k = 3^n τ D^l` with `σ,τ ∈ {±1}`. The
cases `k ≠ l` fail at a length-`min(k,l)` all-`+` integer (one side
vanishes, the other does not). The case `k = l` forces `m = n` and
`σ = τ` by evaluating at `3^k`. Distinct length-`m` balanced words
give distinct `A`.

Without `N(D) → D(N)`, the same argument fails: `N∘D^k` and `D^k∘N`
are distinct irreducibles and equal as functions.

## Computational observations

`D(I+(D(I-(x))))` innermost-normalizes to `x` (not `D(x)`), because
`D ∘ I_a = id` twice. Identity discovery clusters closed unary terms;
labels are only `COMPUTATIONALLY VERIFIED`, `CONJECTURE`, or `REFUTED`.

On the fragment, every open term of size `≤ 6` (9331 unary trees with
one hole) has a unique irreducible descendant under all redex orders,
`rewrite_expr` (innermost-left) matches that descendant, the
irreducibles are exactly the grammar above, and no two distinct
irreducibles share an evaluation fingerprint on
`{−20,…,20} ∪ {3^k} ∪ {(3^k−1)/2}`
(`tests/unit/test_operator_fragment_nf.py`).

**Word rules** remain sound on the intersection of domains. Two-way
commutation rules (`N∘S = S∘N` and converse, and the same for `N∘D`)
are marked `simplifying=False` and `reversible=True`. The full word
table is **not** claimed confluent.

## Conjectures

Unique syntactic NF and semantic completeness for this fragment are
closed (**PROVED**). Lean packaging of the Newman argument is deferred;
do not write `sorry`. The full language (`Add`/`Mul`/`W`) remains
unclaimed.
