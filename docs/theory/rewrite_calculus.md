# Rewrite calculus

**Status of this page:** a sound, classified rewrite system. The
operator fragment `{D, I_a, S, N}` under the tree rules below —
including `N(D(x)) → D(N(x))` — is terminating, locally confluent, and
has a unique syntactic normal form (**PROVED — LEAN**) that is also a
unique representative of the integer operator function
(**PROVED — LEAN**).
Global confluence of the
full expression language (`Add` / `Mul` / `W` / the large word table)
is **not** claimed. Coefficient-word confluence
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
| `N(D(x)) → D(N(x))` | `rewrite_N_D` |

`Nrm(x) → x` is in `TREE_RULES` as a destructor. The engine also
contracts `N(I0(x)) → S(N(x))`; that step is `I0 → S` followed by
`N(S) → S(N)`, not an extra primitive.

Without `N(D) → D(N)`, the remaining rules already have a unique
syntactic NF ([BTC-op-fragment-nf](theorem_ledger.md)), but
`N(D(x))` and `D(N(x))` are distinct irreducibles that agree under
`evaluate` ([BTC-op-fragment-semantic-nf](theorem_ledger.md),
**REFUTED**). The commute is now a tree rule.

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
  `N-inversion` by one. `N(D(x)) → D(N(x))` leaves `size` unchanged.

The rank is well-founded on `ℕ³`. This is termination of **every**
rewrite order on the fragment, not only innermost contraction. Adding
`D` to the pushable class is the only change needed for the new rule.

## Local confluence and unique syntactic NF

The system is left-linear. The only non-variable overlaps of two
left-hand sides are the old peaks together with every overlap that
mentions the new left-hand side `N(D(x))`:

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
| `N(D(I-(x)))` | `→ D(N(I-(x)))` and `→ N(x)` | `N(x)` |
| `N(D(I+(x)))` | `→ D(N(I+(x)))` and `→ N(x)` | `N(x)` |
| `N(D(I0(x)))` | `→ D(N(I0(x)))` and `→ N(x)` | `N(x)` |
| `N(D(S(x)))` | `→ D(N(S(x)))` and `→ N(x)` | `N(x)` |

The new overlaps are exactly the unifications of `D(x)` (the only
non-variable proper subterm of `N(D(x))`) with `D(I_a(y))` or
`D(S(y))`, and the unification of `N(x)` (the non-variable proper
subterm of `N(N(x))`) with `N(D(y))`. `I-`, `I+`, and `S` are never
themselves a left-hand side, and `Nrm` does not occur in any other
left-hand side. Disjoint redexes commute because every rule is
left-linear.

Join of `N(D(I_a(x)))`: `D(N(I_a(x)))` pushes `N` past `I_a` and then
cancels `D(I_{-a})`, reaching `N(x)`. Join of `N(N(D(x)))`:
`N(D(N(x))) → D(N(N(x))) → D(x)`.

Local confluence plus termination gives confluence (Newman). Every
term of the fragment therefore has a unique syntactic normal form.
This is **PROVED — LEAN** as a rewrite-relation Newman argument
([BTC-op-fragment-nd-nf](theorem_ledger.md),
`BTCalculus/OpFragNewman.lean`). The smaller system without the
commute remains [BTC-op-fragment-nf](theorem_ledger.md) and is still
only a human proof. `formal/BTCalculus/Rewrite.lean` contains the
integer soundness identities. `BTCalculus/Confluence.lean` is the
coefficient-word system and is a different object.

## Normal-form grammar

A term is irreducible iff it has no `I0` or `Nrm`, no `D` immediately
above `I_a` or `S`, and no `N` immediately above `N`, `S`, `I-`, `I+`,
`I0`, or `D`. After `N` is pushed inward past every pushable
constructor, the only remaining `N` sits on the hole:

```text
NF   ::= I-(NF) | I+(NF) | S(NF) | Core
Core ::= x | N(x) | D(Core)
```

Every irreducible is therefore a word `w ∈ {I-, I+, S}*` applied to
`D^d(x)` or `D^d(N(x))`.

## Semantic canonicity

Each such irreducible denotes a unique integer function. Write
`val(w)(n) = 3^{|w|} n + c(w)`. Unique balanced-ternary expansion of
length `|w|` (including high zeros) identifies `w` with the pair
`(|w|, c(w))`. The two families are

```text
F_{w,d,+}(n) = 3^{|w|} D^d(n) + c(w)
F_{w,d,-}(n) = -3^{|w|} D^d(n) + c(w)
```

using `D(-n) = -D(n)` (`rewrite_N_D`). These agree as functions of
`n` only when the triples `(w, d, sign)` agree:

- at `n = 0` the constants `c` match;
- if the signs match and `d > d'`, evaluate at `n = 3^{d'}`:
  `D^{d'}(3^{d'}) = 1` and `D^d(3^{d'}) = 0`, which forces
  `3^{|w'| } = 0`;
- if the signs differ, evaluate at `n = 3^{\max(d,d')}`: a positive
  power of `3` cannot equal a negative power of `3`.

So distinct irreducibles are distinct integer operator functions
([BTC-op-fragment-nd-semantic](theorem_ledger.md), **PROVED — LEAN**).
Together with soundness of the rules, the enlarged TRS is a complete
canonical form for the integer operator algebra on this fragment:
semantically equal terms have the same NF.

The same statement for the system *without* `N(D) → D(N)` stays
**REFUTED** ([BTC-op-fragment-semantic-nf](theorem_ledger.md)):
`N(D(x))` and `D(N(x))` were the witnesses.

## Computational observations

`D(I+(D(I-(x))))` innermost-normalizes to `x` (not `D(x)`), because
`D ∘ I_a = id` twice. Identity discovery clusters closed unary terms;
labels are only `COMPUTATIONALLY VERIFIED`, `CONJECTURE`, or `REFUTED`.

On the enlarged fragment, every open term of size `≤ 6` (9331 unary
trees with one hole) has a unique irreducible descendant under all
redex orders, and `rewrite_expr` (innermost-left) matches that
descendant. Every one-step contraction on size `≤ 5` drops the
termination rank. The irreducibles of size `≤ 6` are exactly the
grammar above, `N(D(x))` joins to `D(N(x))`, and no two of those
irreducibles agree on a probe set that includes `±3^k` through
`k = 8` (`tests/unit/test_operator_fragment_nf.py`).

**Word rules** remain sound on the intersection of domains. Two-way
commutation rules (`N∘S = S∘N` and converse, and the word-level
`N∘D = D∘N` pair) are marked `simplifying=False` and
`reversible=True`. The full word table is **not** claimed confluent.

## Conjectures

The enlarged-fragment questions — termination, local confluence,
unique syntactic NF, and semantic canonicity on `{D, I_a, S, N}` —
are closed (**PROVED**). Extending the same one-way `N`–`D`
orientation to `Add` / `Mul` / `W` is a different signature and is
not assumed.

Lean Newman for the enlarged fragment is packaged in
`BTCalculus/OpFragNewman.lean` (termination, local confluence,
confluence, unique syntactic NF, and the NF grammar). Semantic
canonicity of distinct irreducibles is `OpFrag.irreducible_eval_injective`
in `BTCalculus/OpFragSemantic.lean`
([BTC-op-fragment-nd-semantic](theorem_ledger.md), **PROVED — LEAN**).
