# Rewrite-calculus formalization gate

This note states the Lean-target theorems of the rewrite-calculus
paper candidate. It is **not** a new enlargement programme. Word-table
fragments stay closed. There is no AC-matching library.

Canonical informal record:
[rewrite_calculus.md](rewrite_calculus.md). Dossier:
[rewrite_calculus.md](../problems/rewrite_calculus.md).

## 1. Claim A — unary canonical calculus

**Term language.** The inductive type `OpFrag` in
`formal/BTCalculus/OpFrag.lean`:

```text
OpFrag ::= var | D(t) | Im(t) | I0(t) | Ip(t) | S(t) | N(t)
```

No `Add`, `Mul`, or word letters. One hole `var`.

**Tree semantics.** `OpFrag.eval : OpFrag → ℤ → ℤ` in
`OpFragSemantic.lean`, using the same integer maps as
`BTCalculus/Rewrite.lean`:

```text
I_a(x) = a + 3x,   S(x) = 3x,   D(x) = (x − lsd(x))/3,   N(x) = −x
```

**Rewrite.** `OpFrag.Step` is the documented unary tree rules plus
congruence, including `N(D(x)) → D(N(x))`.

**Canonicality.** `t ⇓ u` means `ReflTransGen Step t u` and
`¬∃ v, Step u v` (`IsNF`).

**Completeness (do not conflate).** On this grammar, all four hold:

| Sense | Lean |
|-------|------|
| existence of a normal form | `OpFrag.exists_normal` |
| termination of every rewrite order | `OpFrag.Step_terminating` |
| local confluence, hence confluence | `OpFrag.locally_confluent`, `OpFrag.confluent` |
| unique syntactic NF | `OpFrag.unique_normal_form` |
| semantic injectivity of irreducibles | `OpFrag.irreducible_eval_injective` |
| rewrite preserves `eval` | `OpFrag.eval_step` |

**Theorem candidate A** (already Lean, packaged in `RewriteCore.lean`):

> The unary tree TRS on `{D, I_a, S, N}` including `N(D)→D(N)` is
> terminating and locally confluent. Every term has a unique syntactic
> normal form, and distinct irreducibles denote distinct maps `ℤ → ℤ`.

**Assumptions.** Exact integer semantics; one-hole unary terms; the
oriented commute `N(D)→D(N)`. Without that commute, semantic
canonicity fails (`N(D(x))` vs `D(N(x))`).

**Difficulty.** Lean-trivial as packaging: the proofs already live in
`OpFragNewman.lean` and `OpFragSemantic.lean`. Method (Newman) is
`KNOWN`. The fragment + oriented commute is `PROJECT-SPECIFIC`.

## 2. Definitions for Claim B

**Unary constructors (affine).** `AffineCtor ∈ {S, I+, I−, N}` with

```text
apply S  t = 3t
apply I+ t = 1 + 3t
apply I− t = −1 + 3t
apply N  t = −t
```

`I0` is identified with `S`. `D` is **not** an affine constructor.

**Carry.** `addDigit` / `D_add` already in `Algebra.lean`:

```text
D(x+y) = D(x) + D(y) + carry(lsd(x), lsd(y))
```

where `carry = (addDigit (lsd x) (lsd y)).2 ∈ {−1,0,+1}`.

**D-local binary map.** A map `F : ℤ×ℤ → ℤ` is *D-local* if there
exists `G : ℤ×ℤ → ℤ` such that `D(F(x,y)) = G(D(x), D(y))` for all
`x,y`. Equivalently: `D ∘ F` depends only on the `D`-images of the
arguments, not on their least-significant trits.

**Carry-free Add extension.** A rewrite system on a signature
containing `Add` is *carry-free* if it treats `Add` as D-local: it
may use rules whose integer soundness would require
`D(x+y) = H(D(x), D(y))` for some `H` independent of `lsd`.

**Finite exact constructor-sum identity.** An identity
`U(x)+V(y)=W(x+y)` with `U,V,W ∈ AffineCtor` that holds for all
`x,y ∈ ℤ`.

**Named push-in system.** Terms `AddTree` over `{X, Y, D, S, Add}`.
Rules: unary `D(S(t))→t`, push-in `S(Add(t,u))→Add(S(t),S(u))`, and
congruence. No `D`-through-`Add` rule.

**Coefficient-word representation.** The existing Milestone 14 object:
evaluate the integer, then the unique balanced-ternary coefficient
word (`BTN-confluence`). This note does **not** treat “CAS” as a
formal category.

**What is not claimed.** “No finite rewrite system can represent
addition.” That is false (coefficient words do). The claim is only
about *carry-free tree extensions of the unary core*.

## 3. Claim B — restricted Add/carry exclusion

**Theorem candidate B1 (carry identity).** Already `D_add` /
`BTC-D-add`. Add requires a trit of extra state:

```text
D(x+y) − D(x) − D(y) = carry(lsd x, lsd y)
```

**Theorem candidate B2 (Add is not D-local).**

```text
¬ ∃ G, ∀ x y, D(x+y) = G(D(x), D(y))
```

Witness: `D(0+0)=0` and `D(1+1)=1` while `D(0)=D(1)=0`.

**Theorem candidate B3 (constructor-sum classification).**

```text
U(x)+V(y)=W(x+y)  for all x,y
  ↔  slope U = slope W ∧ slope V = slope W ∧ const U + const V = const W
```

The solutions in `{S, I+, I−, N}` are exactly the six parameterized
rows: `(S,S,S)`, `(N,N,N)`, `(I_a,S,I_a)`, `(S,I_a,I_a)`,
`(I+,I−,S)`, `(I−,I+,S)`.

**Theorem candidate B4 (same-sign residue).** There is no
`W ∈ AffineCtor` with `I+(x)+I+(y)=W(x+y)` (resp. `I−`). The sum is
`S(x+y)+2` (resp. `S(x+y)−2`), and `±2` is not a trit.

**Theorem candidate B5 (named push-in peak).** On the named push-in
system, `D(S(Add(X,Y)))` has two distinct irreducibles
`Add(X,Y)` and `D(Add(S(X),S(Y)))`. So that system is not locally
confluent. Both descendants evaluate to `X+Y` as integers.

**Restricted exclusion (the paper theorem).**

> Exact integer addition is not D-local. Every exact constructor-sum
> identity on `{S, I_a, N}` is one of the six rows. The named carry-free
> push-in extension of the unary core by `S`-through-`Add` fails local
> confluence at `D∘S`. Same-sign `I_a` is not a constructor identity.
> Therefore a complete exact treatment of `Add` requires carry state
> (or a coefficient-word / constant), which is a strict extension of
> the unary tree calculus.

This is **not** “no rewrite system can add.” It is “no *carry-free
D-local tree* extension of `{D,I_a,S,N}` is complete for Add.”

**Assumptions.** Affine constructors as above; D-locality as above;
the named push-in rule set. No quantification over arbitrary TRS
engines, AC-matching, or infinite signatures.

**Difficulty.** B1–B4 are elementary integer algebra (Lean-short).
B5 is a finite inversion argument on a five-constructor inductive
(short, no Newman library). The English “any push-in rule…” and
“already a CAS” remain human, not Lean.

## 4. Examples and non-examples

| Object | Status |
|--------|--------|
| `D(I_a(x))=x`, `D(S(x))=x`, `N(N(x))=x`, `N(D(x))=D(N(x))` | exact unary identities |
| `D(x+y)=D(x)+D(y)+carry` | exact, needs carry trit |
| `D(x+y)=D(x)+D(y)` | false; witness `(1,1)` |
| `S(x)+S(y)=S(x+y)` | exact constructor-sum |
| `I+(x)+I+(y)=I_b(x+y)` | false for every trit `b` |
| `N(x)+S(y)=W(x+y)` | false; slopes `−1` vs `3` |
| `D(S(x+y))→x+y` vs `D(S(x)+S(y))` | syntactic peak; semantic twins |
| Coefficient-word NF of `x+y` | complete, *outside* the unary tree TRS |
| Full `WORD_REWRITE_RULES` confluence | closed non-claim |

## 5. Literature

| Piece | Novelty |
|-------|---------|
| Newman / Knuth–Bendix | `KNOWN` |
| Unique BT expansion | `KNOWN` / `REPARAMETERIZATION` |
| Avizienis signed-digit addition | `KNOWN` |
| AC completion | `KNOWN` (not used) |
| Unary OpFrag package | `PROJECT-SPECIFIC` (method KNOWN) |
| D-locality failure of Add + six-row classification + named peak | `PROJECT-SPECIFIC` |

## 6. Lean map

| File | Role |
|------|------|
| `formal/BTCalculus/Rewrite.lean` | integer soundness of unary rules |
| `formal/BTCalculus/OpFrag*.lean` | Claim A |
| `formal/BTCalculus/Algebra.lean` | `D_add`, `addDigit` |
| `formal/BTCalculus/RewriteCore.lean` | packaging of Claim A |
| `formal/BTCalculus/RewriteAddBoundary.lean` | B1–B5 |

Do not edit `Confluence.lean`. No new CLI, word rules, or census.
