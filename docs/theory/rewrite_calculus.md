# Rewrite calculus

**Status of this page:** a classified rewrite system and a
[paper-candidate artifact](../problems/rewrite_calculus.md). The
publication spine is the Lean-verified unary core
`{D, I_a, S, N}` plus the exact theorem that `D(x+y)` does not
factor through `(D(x),D(y))`
([formalization note](rewrite_calculus_formalization.md);
[publication draft](rewrite_calculus_note.md);
[reviewer packet](rewrite_calculus_reviewer_packet.md);
[explorer UI plan](rewrite_calculus_explorer_plan.md)).
Word-table fragments are a closed appendix. Cubic residuals remain
the laboratory frontier; this page is not a Collatz claim.

## Three canonicalizers

These are three different objects. Do not merge them.

| Object | What it canonicalizes | Home |
|--------|----------------------|------|
| OpFrag tree TRS | Open unary terms in `{D, I_a, S, N}` | `rewrite_expr`, `formal/BTCalculus/OpFrag*.lean` |
| Coefficient-word TRS | Integer sums / affine forms after evaluation | `bt.normtheory`, `BTCalculus/Confluence.lean` |
| Word-string fragments | Operator words; named opt-in tables only | `rewrite_word`, `WORD_SIMP_RULES` / `WORD_WN_RULES` / `WORD_WND_RULES` |

## Canonicalization decision guide

- Unary constructor term in `{D, I_a, S, N}` → `rewrite_expr` / OpFrag NF. Unique syntactic *and* semantic representative (**PROVED — LEAN**: [BTC-op-fragment-nd-nf](theorem_ledger.md), [BTC-op-fragment-nd-semantic](theorem_ledger.md)).
- Integer sum of constructor terms → evaluate, then coefficient-word NF. Never a tree rule on `Add` ([BTC-add-affine-only](theorem_ledger.md)).
- Operator word → `rewrite_word(..., simplifying_only=True)` for the production-safe fragment, or pass `rules=WORD_WN_RULES` / `WORD_WND_RULES` for the named opt-in enlargements. Do **not** treat the full `WORD_REWRITE_RULES` table as a confluent TRS ([BTC-word-full-lc](theorem_ledger.md), **REFUTED**).
- There is no unified `canonicalize(Expr)` that includes `Add`/`Mul` as tree constructors.

## Paper theorem package

The operator fragment `{D, I_a, S, N}` under the tree rules below —
including `N(D(x)) → D(N(x))` — is terminating, locally confluent, and
has a unique syntactic normal form that is also a unique representative
of the integer operator function. For the output
`H(x,y)=D(x+y)`, no function `G` satisfies
`H(x,y)=G(D(x),D(y))` for every `x,y`
([BTC-add-not-D-local](theorem_ledger.md)). The exact carry identity
explains the missing least-significant-trit state. The named push-in
system for `S` through `Add` exhibits the same boundary in a
non-joining peak at `D∘S`
([BTC-push-in-S-peak](theorem_ledger.md)).

Universal maximality among Add-tree systems is not a paper theorem.
The older push-in, factor-out, and affine-only records remain human
research claims and counterexamples. Global confluence of the full
expression language is not claimed.

The production word table is **not** locally confluent
([BTC-word-full-lc](theorem_ledger.md), **REFUTED**); its
simplifying-only fragment is terminating and locally confluent
([BTC-word-simp-nf](theorem_ledger.md)). The opt-in fragments
`WORD_WN_RULES` and `WORD_WND_RULES` are also terminating and
locally confluent ([BTC-word-wn-nf](theorem_ledger.md),
[BTC-word-wnd-nf](theorem_ledger.md)). Adding one-way `N∘D` without
word-level `I±` sign-flips fails at `N∘D∘I±`
([BTC-word-simp-nd-lc](theorem_ledger.md), **REFUTED**). Further
word-table enlargement is **closed**. Coefficient-word confluence
([BTN-confluence](theorem_ledger.md), `BTCalculus/Confluence.lean`) is
the complete finite canonicalizer for those sums after evaluation.

## Novelty after literature

Method is KNOWN. The classification of *this* operator algebra is
the candidate distinction. See the
[dossier](../problems/rewrite_calculus.md) for the full audit.

| Claim | Novelty | Why |
|-------|---------|-----|
| Newman / Knuth–Bendix on a finite left-linear TRS | `KNOWN` | `newman-1942-confluence`, `baader-nipkow-1998-term-rewriting` |
| Unique balanced-ternary expansion; `D`/`I_a` as drop/prepend | `KNOWN` / `REPARAMETERIZATION` | `knuth-taocp-vol2`, `hayes-2001-third-base` |
| Signed-digit carry-free addition as an *arithmetic* algorithm | `KNOWN` | `avizienis-1961-signed-digit` |
| Completion / rewriting modulo AC | `KNOWN` | `peterson-stickel-1981-unification-ac` |
| OpFrag confluence + semantic injectivity of the NF grammar | `PROJECT-SPECIFIC` (method KNOWN) | Oriented `N(D)→D(N)` is necessary; without it `N(D)`/`D(N)` are semantic twins |
| Maximality: exact `S`/`I_a` push-in through Add/Mul dies at `D∘S` | `PROJECT-SPECIFIC` | Avizienis does not state a TRS maximality theorem for `{D,I_a,S,N}` |
| Finite exact factor-out Add is already a CAS | `PROJECT-SPECIFIC` (AC engine KNOWN) | Same-sign `I_a` residue `±2` is the trit carry of `1+1` |
| Six exact identities `U(x)+V(y)=W(x+y)` on `{S,I_a,N}`; Add is affine-only | `PROJECT-SPECIFIC` | Exhaustive constructor classification, not just unique expansion |
| Named word fragments `SIMP` / `WN` / `WND` | `PROJECT-SPECIFIC` appendix | Same Newman method; not the publication spine |

The falsifier for the package — prior work already proving the same
maximal tree core and Add-exclusion for this operator algebra — did
not fire. Two central claims remain `PROJECT-SPECIFIC` and form one
coherent theorem: **maximal unary tree core + Add/carry exclusion**.

## Word-table enlargement is closed

PRs #8–#10 answered the word-table question: the production table is
a permanent non-claim; `WORD_SIMP_RULES`, `WORD_WN_RULES`, and
`WORD_WND_RULES` are named opt-in fragments with Newman certificates;
`N∘K3` and the `I±` sign-flips stay out of `WORD_REWRITE_RULES`.
Further one-way production commutes (`N∘M2`, `N∘Wz`, `N∘Wt`) would
be more named fragments of the same species, not a new mathematical
consequence. That programme is **CLOSE**. Do not install those
commutes. Do not open another word-fragment Phase-0.

## Note outline

A 5–8 page note, if written, should use this spine — not a rewrite
engine travelogue:

1. Definitions: `D`, `I_a`, `S=I_0`, `N`; tree terms versus words versus coefficient words.
2. OpFrag TRS including `N(D)→D(N)`: termination, local confluence, unique NF (**LEAN**).
3. Semantic injectivity of the NF grammar (**LEAN**); necessity of the oriented commute.
4. Push-in Add/Mul obstruction: the `D∘S` peak (human).
5. Exhaustive Add classification: six identities; same-sign `I_a` needs `±2` (human).
6. Architectural conclusion: sums are affine / coefficient-word; Add stays out of the tree TRS.
7. Optional appendix: production word table fails at `N∘W∘W`; named fragments.

Do not package census tooling, CLI, identity-discovery, or
`Confluence.lean` (Milestone 14, a different object).

## Historical inspiration

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
`reversible=True`. The full word table is **not** locally confluent
([BTC-word-full-lc](theorem_ledger.md)); see
[Word-table fragments](#word-table-fragments-excluding-add).

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
locally confluent ([BTC-word-full-lc](theorem_ledger.md)).

On the *one-way* subset that matches the tree orientation
(`N∘D → D∘N`, `N∘W → W∘N`, plus the existing simplifying `W`/`K3`
rules), the peak `N∘W∘W` does not join:

```text
N∘W∘W  →  W∘N∘W  →  W∘W∘N  →  K3∘N
N∘W∘W  →  N∘K3
```

`N∘K3` and `K3∘N` are distinct irreducibles
([BTC-w-nd-word-lc](theorem_ledger.md), **REFUTED**). The same peak
is present in the *production* table: two-way `N∘W` does not join it,
because `N∘K3` is not a production rule. The missing commute
`N∘K3 → K3∘N` is exact (`K3` strips factors of `3`). On that *bounded*
one-way list — which does **not** include the production cancellations
`D∘I±` — adding `N∘K3` makes every critical pair join. That check is
not a reason to install `N∘K3` in `WORD_REWRITE_RULES`, and it is not
a Newman certificate for SIMP plus `N∘D`: see
[Named fragment `WORD_WN_RULES`](#named-fragment-word_wn_rules).
Enlarging the unary signature by `W` immediately introduces `K3` and a
new `N`-commute — the same species of gap that `N(D)`/`D(N)` was
before the commute became a tree rule.

### Obstruction

[BTC-unary-s-distrib-obstruction](theorem_ledger.md) (**PROVED**):
any exact push-in rule that copies `S` (or `I_a`) through `Add` or
`Mul` overlaps `D∘S = id` (resp. `D∘I_a = id`) in a peak whose other
descendant is `D` of a sum or product of `S`/`I` terms. Without an
unsound `D`-through-binary rule, that peak does not join. So
`{D, I_a, S, N}` is the maximal complete *tree* core among those
extensions. `W` is a word-level question, decided in
[Word-table fragments](#word-table-fragments-excluding-add).

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

Proof of the classification: `W(x+y)` depends only on `x+y`, so the
coefficients of `x` and `y` in `U(x)+V(y)` must be equal. Those
coefficients are `3` for `S`/`I_a` and `-1` for `N`. Hence both
constructors are in `{S, I_a}` or both are `N`. The constant term
is then the sum of trits `a+b`, which is itself a trit precisely on
the six rows above. Same-sign `I_a(x)+I_a(y) = 3(x+y)±2` is a
function of `x+y`, but `±2` is not a trit, so any tree rule for it
introduces a constant. Mixed `N` with `S`/`I_a` has unequal
coefficients `-1` and `3`. `D(x)+D(y)=D(x+y)` is unsound
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
Independent of `Add`, the production word table is decided below.

## Word-table fragments (excluding Add)

`WORD_REWRITE_RULES` is a string-rewriting table, not the OpFrag tree
TRS and not coefficient-word `Confluence.lean`. `Add` is not a letter.

### Full table — permanent non-claim

[BTC-word-full-lc](theorem_ledger.md) (**REFUTED**). The production
peak is the same shape as the one-way `W` peak:

```text
N∘W∘W  →  W∘N∘W  →*  {N∘K3, K3∘N}
N∘W∘W  →  N∘K3
```

Both `N∘K3` and `K3∘N` are irreducible: the table has two-way `N∘W`
and `W∘W → K3`, but no `N∘K3` rule. The opposite overlap `W∘W∘N`
has the same two irreducibles. Two-way commutation does not repair
the peak.

The two-way rows `N∘D ↔ D∘N` (and the other reversible commutes) are
also non-terminating as a TRS — a KNOWN fact about inverse
length-preserving rules, not a ledger theorem. Newman therefore
cannot apply to the full table even if the `N∘W∘W` peak were joined.

Any production fragment that keeps both `W∘W → K3` and an `N∘W`
commute (one-way or two-way) fails at this peak, unless the missing
exact commute `N∘K3` is added, and that rule is **not** in
`WORD_REWRITE_RULES`. Full-table confluence is therefore a permanent
non-claim inside the production table.

### Named fragment `WORD_SIMP_RULES`

[BTC-word-simp-nf](theorem_ledger.md) (**PROVED**). The sixteen
`simplifying=True` rows — cancellations `N∘N`, `D∘S`, `D∘I±`,
`D∘I0`, `Wz∘Wz`, `Wt∘Wt`, `H2∘M2`, `H3∘S`; the `W`/`K3` stock
`W∘W → K3`, `W∘S → W`, `K3∘S → K3`, `K3∘W → W`, `W∘K3 → W`,
`K3∘K3 → K3`; and `I0 → S` — form a terminating, locally confluent
string TRS. Every word has a unique syntactic normal form.

**Termination.** Rank `(I0-count, length)` on `ℕ²`. `I0 → S` drops
the first coordinate. Every other simplifying rule has source length
2 and destination length at most 1, so drops length, and never
introduces `I0`.

**Local confluence.** The system is left-linear. The complete list of
prefix/suffix overlaps and inclusions joins:

| Peak | Contractions | Join |
|------|----------------|------|
| `N∘N∘N` | both `→ N` | `N` |
| `D∘I0` | `→ ε` and `→ D∘S` | `ε` |
| `Wz∘Wz∘Wz` | both `→ Wz` | `Wz` |
| `Wt∘Wt∘Wt` | both `→ Wt` | `Wt` |
| `K3∘K3∘K3` | both `→ K3∘K3` | `K3` |
| `K3∘K3∘S` | `→ K3∘S` and `→ K3∘K3` | `K3` |
| `K3∘K3∘W` | both `→ K3∘W` | `W` |
| `W∘W∘W` | `→ K3∘W` and `→ W∘K3` | `W` |
| `W∘W∘S` | `→ K3∘S` and `→ W∘W` | `K3` |
| `W∘W∘K3` | `→ K3∘K3` and `→ W∘W` | `K3` |
| `K3∘W∘W` | `→ W∘W` and `→ K3∘K3` | `K3` |
| `K3∘W∘S` | `→ W∘S` and `→ K3∘W` | `W` |
| `K3∘W∘K3` | `→ W∘K3` and `→ K3∘W` | `W` |
| `W∘K3∘K3` | both `→ W∘K3` | `W` |
| `W∘K3∘S` | `→ W∘S` and `→ W∘K3` | `W` |
| `W∘K3∘W` | both `→ W∘W` | `K3` |

The `W`/`K3` stock (six rules, twelve of the rows above) is the
interesting kernel. The remaining simplifying rules are disjoint
involutions and cancellations except for the inclusion `I0 ⊂ D∘I0`.
Newman gives unique syntactic NF. Semantic canonicity of those
irreducibles is **not** claimed.

`rewrite_word(..., simplifying_only=True)` is this fragment. The
production table is not widened: `N∘K3` stays out of
`WORD_REWRITE_RULES`, and the two-way commutes stay in the full table
as identities, not as a confluent TRS.

Adding a production commute to this fragment is not uniformly safe.
`N∘W` alone recreates `N∘W∘W` and, without `N∘S`, also `N∘W∘S →
W∘N∘S | W∘N`. `N∘D` without word-level `I±` sign-flips fails at
`N∘D∘I±`. The safe enlargement that contains both `W` and `N` is
the named fragment below; the further W+N+D enlargement is
[`WORD_WND_RULES`](#named-fragment-word_wnd_rules).

### Named fragment `WORD_WN_RULES`

[BTC-word-wn-nf](theorem_ledger.md) (**PROVED**). The nineteen-rule
opt-in fragment

```text
WORD_SIMP_RULES
N∘S  → S∘N
N∘W  → W∘N
N∘K3 → K3∘N
```

is a terminating, locally confluent string TRS. Every word has a
unique syntactic normal form. The orientation is the tree convention
(`N` moves inward). The reverse rows `S∘N`, `W∘N`, `K3∘N` are not
rules; two-way `N∘K3 ↔ K3∘N` is a length-preserving cycle.

`N∘K3` is exact (`K3(n) = n/3^{v_3(n)}` and `v_3(-n)=v_3(n)`). It is
**not** installed in `WORD_REWRITE_RULES`. Use
`rewrite_word(..., rules=WORD_WN_RULES)`.

**Termination.** Rank `(I0-count, N-inversion, length)` on `ℕ³`,
where `N-inversion` is the number of pairs `(N` at `i`, pushable
letter at `j>i)` and pushable means `{S, W, K3}`.

- `I0 → S` drops `I0-count`. This may raise `N-inversion` (an `I0`
  after `N` becomes pushable `S`); the first coordinate still drops.
- Every remaining SIMP rule has source length 2 and destination
  length at most 1, never introduces `I0`, and does not raise
  `N-inversion` (a cancelled or collapsed pushable after `N` can only
  lose inversions).
- `N∘S`, `N∘W`, `N∘K3` are length-preserving and each drop
  `N-inversion` by one.

The rank is well-founded. This is termination of every rewrite order
on the fragment.

**Local confluence.** The system is left-linear. Every SIMP overlap
still joins. The new left-hand sides are `N∘S`, `N∘W`, `N∘K3`. The
only rule that ends in `N` is `N∘N`, so the new prefix/suffix
overlaps are exactly

| Peak | Contractions | Join |
|------|----------------|------|
| `N∘N∘S` | `→ S` and `→ N∘S∘N` | `S` |
| `N∘N∘W` | `→ W` and `→ N∘W∘N` | `W` |
| `N∘N∘K3` | `→ K3` and `→ N∘K3∘N` | `K3` |
| `N∘W∘W` | `→ W∘N∘W` and `→ N∘K3` | `K3∘N` |
| `N∘W∘S` | `→ W∘N∘S` and `→ N∘W` | `W∘N` |
| `N∘W∘K3` | `→ W∘N∘K3` and `→ N∘W` | `W∘N` |
| `N∘K3∘K3` | `→ K3∘N∘K3` and `→ N∘K3` | `K3∘N` |
| `N∘K3∘S` | `→ K3∘N∘S` and `→ N∘K3` | `K3∘N` |
| `N∘K3∘W` | `→ K3∘N∘W` and `→ N∘W` | `W∘N` |

`N∘S` has no overlap with a SIMP left-hand side except through
`N∘N`: no SIMP source begins with `S`. There is no `I0` inside a new
source. Disjoint redexes commute by left-linearity. Newman gives
unique syntactic NF. Semantic canonicity of those irreducibles is
**not** claimed (`N∘D` and `D∘N` remain distinct irreducibles).

The opposite one-way orientation `K3∘N → N∘K3` (without `N∘K3`)
fails at `N∘W∘K3` / `W∘K3∘N`, leaving `W∘N∘K3` irreducible. So the
inward `N∘K3 → K3∘N` is the orientation that matches the tree
convention and joins the `W`/`K3` stock.

### Obstruction: `N∘K3` does not absorb `N∘D`

[BTC-word-simp-nd-lc](theorem_ledger.md) (**REFUTED**). Adding
one-way `N∘D → D∘N` to `WORD_WN_RULES` (or to SIMP plus `N∘S` and
`N∘K3`) produces two non-joining peaks:

```text
N∘D∘Ip  →  D∘N∘Ip  |  N
N∘D∘Im  →  D∘N∘Im  |  N
```

`D∘N∘I±` is irreducible on that fragment: `N∘Ip → Im∘N` is a *tree*
rule, not a production word rule and not a `WORD_WN_RULES` row. The
same peaks join for `I0` and `S` (`I0 → S` then `N∘S`, then
`D∘S → ε`). The earlier bounded one-way `{N,D,S,W,K3}` list hid this
obstruction by omitting `D∘I±`. The opt-in repair is
[`WORD_WND_RULES`](#named-fragment-word_wnd_rules).

`N∘K3` is therefore enough for a confluent W+N production fragment,
and not enough to include the D-commute while keeping SIMP's `I±`
cancellations *unless* those tree sign-flips are installed as word
rules. Two-way `N∘D ↔ D∘N` remains a KNOWN non-termination.

### Named fragment `WORD_WND_RULES`

[BTC-word-wnd-nf](theorem_ledger.md) (**PROVED**). The twenty-two-rule
opt-in fragment

```text
WORD_WN_RULES
N∘D  → D∘N
N∘Ip → Im∘N
N∘Im → Ip∘N
```

is a terminating, locally confluent string TRS. Every word has a
unique syntactic normal form. The orientation is the tree convention
(`N` moves inward; `I±` flip sign). The reverse rows `D∘N`,
`Im∘N → N∘Ip`, and `Ip∘N → N∘Im` are not rules; each pair is a
length-preserving cycle.

The sign-flips are exact on `ℤ`: `I_a(x) = a + 3x`, so
`N(I_+(n)) = -(3n+1) = 3(-n)-1 = I_-(-n)` and
`N(I_-(n)) = -(3n-1) = 3(-n)+1 = I_+(-n)`. They are the word
spellings of the existing tree rules `N(I+(x)) → I-(N(x))` and
`N(I-(x)) → I+(N(x))`. They are **not** installed in
`WORD_REWRITE_RULES`. Use `rewrite_word(..., rules=WORD_WND_RULES)`.

**Termination.** Rank `(I0-count, N-inversion, length)` on `ℕ³`,
where `N-inversion` is the number of pairs `(N` at `i`, pushable
letter at `j>i)` and pushable means `{S, W, K3, D, Ip, Im}`.

- `I0 → S` drops `I0-count`. This may raise `N-inversion` (an `I0`
  after `N` becomes pushable `S`); the first coordinate still drops.
- Every remaining SIMP rule has source length 2 and destination
  length at most 1, never introduces `I0`, and does not raise
  `N-inversion`.
- `N∘S`, `N∘W`, `N∘K3`, `N∘D`, `N∘Ip`, `N∘Im` are length-preserving
  and each drop `N-inversion` by one (`N∘Ip → Im∘N` replaces the
  inversion `(N, Ip)` by a trailing `N` with no later pushable).

The rank is well-founded. This is termination of every rewrite order
on the fragment.

**Local confluence.** The system is left-linear. Every SIMP and WN
overlap still joins. The new left-hand sides are `N∘D`, `N∘Ip`,
`N∘Im`. No SIMP or WN source begins with `Ip` or `Im`, so those two
rules have no prefix/suffix overlap except through `N∘N`. The only
rule that ends in `N` is `N∘N`. The new overlaps are exactly

| Peak | Contractions | Join |
|------|----------------|------|
| `N∘N∘D` | `→ D` and `→ N∘D∘N` | `D` |
| `N∘N∘Ip` | `→ Ip` and `→ N∘Im∘N` | `Ip` |
| `N∘N∘Im` | `→ Im` and `→ N∘Ip∘N` | `Im` |
| `N∘D∘S` | `→ D∘N∘S` and `→ N` | `N` |
| `N∘D∘Ip` | `→ D∘N∘Ip` and `→ N` | `N` |
| `N∘D∘Im` | `→ D∘N∘Im` and `→ N` | `N` |
| `N∘D∘I0` | `→ D∘N∘I0` and `→ N` | `N` |

The previously non-joining peaks join by the sign-flips:
`D∘N∘Ip → D∘Im∘N → N` and `D∘N∘Im → D∘Ip∘N → N`. The `I0` peak
still joins by `I0 → S` then `N∘S` then `D∘S → ε`. There is no
`I0` inside a new source. Disjoint redexes commute by left-linearity.
Newman gives unique syntactic NF. Semantic canonicity of those
irreducibles is **not** claimed.

The sign-flips are not ordinary commutes: they change the letter
(`Ip ↔ Im`) while pushing `N` inward. That is still an exact pure
word rule, so W+N+D is the same species of object as `WORD_WN_RULES`,
not a different encoding. Production `WORD_REWRITE_RULES` is not
widened.

Further one-way production commutes (`N∘M2`, `N∘Wz`, `N∘Wt`) are
**not** opened. They would be more named fragments of the same
species; see [Word-table enlargement is closed](#word-table-enlargement-is-closed).

Tests: `tests/unit/test_rewrite_word_fragments.py`.

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
tree extension of that kind is assumed. The
production word table is **not** locally confluent
([BTC-word-full-lc](theorem_ledger.md)); the named simplifying
fragment is ([BTC-word-simp-nf](theorem_ledger.md)); the opt-in
W+N fragment is ([BTC-word-wn-nf](theorem_ledger.md)); SIMP plus
one-way `N∘D` without word `I±` sign-flips is not
([BTC-word-simp-nd-lc](theorem_ledger.md)); the opt-in W+N+D
fragment is ([BTC-word-wnd-nf](theorem_ledger.md)). Word-table
enlargement beyond those named fragments is **closed**.

Lean Newman for the enlarged fragment is packaged in
`BTCalculus/OpFragNewman.lean` (termination, local confluence,
confluence, unique syntactic NF, and the NF grammar). Semantic
canonicity of distinct irreducibles is `OpFrag.irreducible_eval_injective`
in `BTCalculus/OpFragSemantic.lean`
([BTC-op-fragment-nd-semantic](theorem_ledger.md), **PROVED — LEAN**).
Do not edit `BTCalculus/Confluence.lean`.
