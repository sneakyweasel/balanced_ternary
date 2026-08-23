# Rewrite calculus

**Status of this page:** a sound, classified rewrite system. The
operator fragment `{D, I_a, S, N}` under the tree rules below —
including `N(D(x)) → D(N(x))` — is terminating, locally confluent, and
has a unique syntactic normal form (**PROVED — LEAN**) that is also a
unique representative of the integer operator function
(**PROVED — LEAN**). That fragment is **maximal** as a complete
tree-level canonical core among exact push-in *or* factor-out
extensions by `Add` or `Mul`: push-in `S`-distributivity overlaps
`D∘S = id` in a non-joining peak
([BTC-add-s-push-lc](theorem_ledger.md),
[BTC-mul-s-push-lc](theorem_ledger.md), **REFUTED**); finite
factor-out Add is already AC-engine / CAS territory
([BTC-add-factor-cas-obstruction](theorem_ledger.md)). Integer sums of
unary constructor terms are canonicalized only as affine maps /
coefficient words, never by a tree TRS on `Add`
([BTC-add-affine-only](theorem_ledger.md)). Global confluence
of the full expression language and of the large word table is **not**
claimed. Coefficient-word confluence
([BTN-confluence](theorem_ledger.md), `BTCalculus/Confluence.lean`) is
a different object — and is the complete finite canonicalizer for
those sums after evaluation.

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

## Signature enlargement (`Add` / `Mul` / `W`)

Phase-0 asked whether the same one-way tree orientation remains a
rewrite core after adding `Add`, `Mul`, or `W`. Candidate rules were
kept out of `rewrite._step`; they are exact on ℤ only when stated
below. Tests: `tests/unit/test_rewrite_signature_enlargement.py`.

### Rejected as unsound

These fail on ℤ by balanced-trit carry. They are **not** tree rules.

| Candidate | Witness |
|-----------|---------|
| `D(x+y) → D(x)+D(y)` | `x = y = 1`: `D(2) = 1`, `D(1)+D(1) = 0` |
| `D(x*y) → D(x)*D(y)` | `x = 2`, `y = 4`: `D(8) = 3`, `D(2)*D(4) = 1` |
| `I_a(x*y) → I_a(x)*y` | `a = +1`, `x = 1`, `y = 2`: `7` versus `8` |
| `I_a(x)+I_b(y) → I_{a+b}(x+y)` | `a = b = +1`: `I+(1)+I+(1) = 8`, `I+(2) = 7` |

`D` through a binary constructor is therefore not an exact closed
tree rule. Repairing it needs the carry trit, which is the start of a
computer-algebra engine and is out of Phase-0 scope.

### `Add`, push-in (matches unary “`N` moves inward”)

Exact candidates:

```text
N(x+y) → N(x)+N(y)
S(x+y) → S(x)+S(y)
I_a(x+y) → I_a(x)+S(y)    (left orientation)
```

`N(N(x+y))` and `N(S(x+y))` join. The overlap of `D(S(z)) → z` with
`S`-distributivity does **not**:

```text
D(S(x+y))  →  x+y
D(S(x+y))  →  D(S(x)+S(y))
```

Both descendants are irreducible and `evaluate` agrees
([BTC-add-s-push-lc](theorem_ledger.md), **REFUTED**). The same shape
appears for `D(I+(x+y))`. Choosing both left and right `I_a`
orientations is a second non-join (`I_a(x)+S(y)` versus
`S(x)+I_a(y)`).

`N(x+y) → N(x)+N(y)` alone is locally confluent on the named overlaps
and on every size-`≤ 5` unary-plus-one-`Add` open term, but
`S(x+y)` and `S(x)+S(y)` are distinct irreducibles with equal
`evaluate` ([BTC-add-n-push-semantic](theorem_ledger.md), **REFUTED**).

### `Mul`, push-in

Exact candidates `N(x*y) → N(x)*y` and `S(x*y) → S(x)*y`. Again
`N`-overlaps join and `D∘S` does not:

```text
D(S(x*y))  →  x*y
D(S(x*y))  →  D(S(x)*y)
```

([BTC-mul-s-push-lc](theorem_ledger.md), **REFUTED**). Left-only
`N`-through-`Mul` leaves the semantic twins `N(x)*y` and `x*N(y)`.

`Add+Mul` together still contains the `Add` peak; it was not a
separate system.

### Factor-out (opposite orientation)

The finite exact-on-ℤ pair table is size-decreasing:

```text
S(x)+S(y) → S(x+y)          (I0 counts as S)
N(x)+N(y) → N(x+y)
I_a(x)+S(y) → I_a(x+y)
S(x)+I_a(y) → I_a(x+y)
I+(x)+I-(y) → S(x+y)
I-(x)+I+(y) → S(x+y)
```

Same-sign `I_a(x)+I_a(y)` is **not** a rule: `I+(x)+I+(y) = 3(x+y)+2`
and `I-(x)+I-(y) = 3(x+y)-2`, and `±2` is not a trit, so the sum is
not `I_b(x+y)` for any trit `b`.

**Binary matching** (redexes only at a node `u+v`). The `D∘S` peak
is repaired: `D(S(x)+S(y)) → D(S(x+y)) → x+y`. Named unary overlaps
(`N(S(x))+N(S(y))`, `D(I+(x)+S(y))`) join. Every Add of two small
unary atoms has a unique syntactic NF
(`tests/unit/test_rewrite_factor_out_add.py`). Semantic canonicity
fails even after identifying AC twins
([BTC-add-factor-binary-semantic](theorem_ledger.md), **REFUTED**):

```text
S(x)+(S(y)+z)     irreducible, atoms {S(x), S(y), z}
S(x+y)+z          irreducible, atoms {S(x+y), z}
```

These are not AC-equivalent and agree under `evaluate`. The same
shape is `I+(x+y)+I+(z)` versus `I+(x)+I+(y+z)` (both
`3(x+y+z)+2`). If integer constants are allowed as summands,
`I+(x)+I+(y)` twins `S(x+y)+2`.

**AC-matching** of the same finite table (flatten the Add spine;
contract any pair). Non-adjacent `S` summands collect, and three
`S` join to `S(x+y+z)` modulo AC. Opposite-sign
`I+(x)+S(y)+I-(z)` joins to `S(x+y+z)`. Same-sign does **not**
([BTC-add-factor-ac-semantic](theorem_ledger.md), **REFUTED**):

```text
I+(x)+S(y)+I+(z)  →  I+(x+y)+I+(z)
I+(x)+S(y)+I+(z)  →  I+(x)+I+(y+z)
```

Both descendants are irreducible and not AC-equivalent. The
`I-` residue `-2` is the same peak. Collecting non-adjacent
summands is already AC-matching; joining the same-sign peak needs
constants, an explicit carry, or a polynomial normal form.

[BTC-add-factor-cas-obstruction](theorem_ledger.md) (**PROVED**):
any finite exact-on-ℤ factor-out Add extension of the unary tree
core either matches only adjacent binary summands, leaving
`S(x)+(S(y)+z)` versus `S(x+y)+z` (not AC-equivalent), or, once
AC-matching is granted, cannot join `I+(x+y)+I+(z)` versus
`I+(x)+I+(y+z)` because `I_a(x)+I_a(y)` is not `I_b(x+y)` for any
trit `b`. A complete form is therefore an AC engine with constants
or carry — already a computer-algebra engine. The rules stay out of
`rewrite._step`. This is the same balanced-trit carry of `1+1` that
made `D`-through-Add unsound and that blocked push-in at `D∘S`.

### `W` (bounded word fragment only)

`W` is not a tree constructor and is not one-way sequential. The
production word table keeps two-way `N∘D` and `N∘W` and is **not**
claimed confluent.

On the *one-way* subset that matches the tree orientation
(`N∘D → D∘N`, `N∘W → W∘N`, plus the existing simplifying `W`/`K3`
rules), the peak `N∘W∘W` does not join:

```text
N∘W∘W  →  W∘N∘W  →  W∘W∘N  →  K3∘N
N∘W∘W  →  N∘K3
```

`N∘K3` and `K3∘N` are distinct irreducibles
([BTC-w-nd-word-lc](theorem_ledger.md), **REFUTED**). The missing
commute `N∘K3 → K3∘N` is exact (`K3` strips factors of `3`). Adding
it makes every critical pair of that bounded one-way list join
(**COMPUTATIONALLY VERIFIED** on that list, not a Newman certificate
and not a claim about `WORD_REWRITE_RULES`). Enlarging the unary
signature by `W` immediately introduces `K3` and a new `N`-commute —
the same species of gap that `N(D)`/`D(N)` was before the commute
became a tree rule.

### Obstruction

[BTC-unary-s-distrib-obstruction](theorem_ledger.md) (**PROVED**):
any exact push-in rule that copies `S` (or `I_a`) through `Add` or
`Mul` overlaps `D∘S = id` (resp. `D∘I_a = id`) in a peak whose other
descendant is `D` of a sum or product of `S`/`I` terms. Without an
unsound `D`-through-binary rule, that peak does not join. So
`{D, I_a, S, N}` is the maximal complete *tree* core among those
extensions. `W` is a word-level question and was only bounded-checked.

Factor-out does not escape that maximality: see
[BTC-add-factor-cas-obstruction](theorem_ledger.md). The two
orientations fail for the same carry.

### Architectural theorem (Add is affine-only)

[BTC-add-affine-only](theorem_ledger.md) (**PROVED**). Let
`U, V, W ∈ {S, I+, I-, N}` (and `I0 = S`). The identity
`U(x)+V(y) = W(x+y)` holds on `ℤ` if and only if `(U,V,W)` is one of

```text
(S, S, S)     (N, N, N)
(I_a, S, I_a) (S, I_a, I_a)
(I+, I-, S)   (I-, I+, S)
```

Proof of the classification: `S` and `I_a` have slope `3`, `N` has
slope `-1`, and `W(x+y)` has slope `3` or `-1` in the sum `x+y`.
Matching slopes forces `{U,V} ⊂ {S, I_a}` with `W ∈ {S, I_a}`, or
`U = V = W = N`. The constant term is then the sum of trits
`a+b`, which is itself a trit precisely on the six rows above.
Same-sign `I_a(x)+I_a(y) = 3(x+y)±2` is exact, but `±2` is not a
trit, so any tree rule for it introduces a constant. Mixed `N` with
`S`/`I_a` has slope `2` or `-4`. `D(x)+D(y)=D(x+y)` is unsound
(`x=y=1`: `D(2)=1` and `D(1)+D(1)=0` — the carry of `1+1`,
[BTC-D-add](theorem_ledger.md)).

Those identities *are* the push-in and factor-out tables, plus
`N`-distrib. Each orientation is already incomplete without
AC-matching and constants or carry:

- push-in `S` / `I_a` — [BTC-unary-s-distrib-obstruction](theorem_ledger.md);
- `N`-through-Add alone — [BTC-add-n-push-semantic](theorem_ledger.md);
- finite factor-out — [BTC-add-factor-cas-obstruction](theorem_ledger.md).

There is no third exact-on-`ℤ` tree orientation. Therefore every
finite exact tree TRS on `Add` either fails semantic canonicity or is
already a CAS. The unique complete finite representatives of such
sums are their affine maps: a sum of constructor terms is a
multi-linear form with integer coefficients (a single unary
*composition* remains `±3^{|w|} D^d(n)+c(w)`,
[BTC-op-fragment-nd-semantic](theorem_ledger.md)). Closed instances
are integers; their unique representative is the balanced-ternary
word ([BT-encode-unique](theorem_ledger.md)), obtained by
`evaluate` then the coefficient-word NF
(`bt.normtheory.arithmetic.add_coeff` /
`bt.normtheory.strategies.normal_form`;
[BTN-nf](theorem_ledger.md), [BTN-confluence](theorem_ledger.md)).

`Add` is therefore evaluation / affine / coefficient-word only.
The rules stay out of `rewrite._step`. Tests:
`tests/unit/test_rewrite_add_affine_only.py`.

## Conjectures

The unary-fragment questions — termination, local confluence, unique
syntactic NF, and semantic canonicity on `{D, I_a, S, N}` — are
closed (**PROVED**). The Phase-0 enlargement questions for push-in
`Add` / `Mul`, for one-way `W` without `N∘K3`, and for finite
factor-out Add (binary or AC-matching) are closed (**REFUTED**). The
architectural question — whether a tree TRS on `Add` can still be a
complete finite canonicalizer — is closed (**PROVED**): it cannot,
and the complete forms are affine / coefficient-word
([BTC-add-affine-only](theorem_ledger.md)). No finite exact Add/Mul
tree extension of that kind is assumed, and the full word table is
still not assumed confluent.

Lean Newman for the enlarged fragment is packaged in
`BTCalculus/OpFragNewman.lean` (termination, local confluence,
confluence, unique syntactic NF, and the NF grammar). Semantic
canonicity of distinct irreducibles is `OpFrag.irreducible_eval_injective`
in `BTCalculus/OpFragSemantic.lean`
([BTC-op-fragment-nd-semantic](theorem_ledger.md), **PROVED — LEAN**).
Do not edit `BTCalculus/Confluence.lean`.
