# Residual-state complexity

Master record for Milestone 16. The section algebra of Milestone 15 is a
**REPARAMETERIZATION** of 3-section / Cartier-style calculus. This
document is about **finite-horizon residual automata**, Myhill–Nerode
counts, composition, and the bounded normalizer.

Claim labels: **EXACT — LEAN VERIFIED**, **EXACT — HUMAN PROOF**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **REFUTED**,
**REPARAMETERIZATION**.

## Residual machine

For `f ∈ Z[x]` and input trit `a ∈ {-1,0,+1}`:

```text
ρ_a(f) = [f(a)]_3
δ(f,a) = 𝔇_a f
f  --[a / ρ_a(f)]-->  𝔇_a f
```

On a word `w`, the machine emits the first `|w|` balanced output trits
of `f` along that section path. Prefix locality says those trits do not
depend on a residual argument after `w`. End-of-horizon: compare only
those `|w|` trits, not residual polynomials.

## Finite-horizon equivalence

`f ≡_k g` iff every trit word `w` of length `k` produces the same output
word. Horizon `0` is trivial. Recursive characterization:

```text
f ≡_0 g
f ≡_{r+1} g  iff  ∀ a,  ρ_a(f)=ρ_a(g)  and  𝔇_a f ≡_r 𝔇_a g
```

**EXACT — LEAN VERIFIED** (`equivK`, `equivK_iff_outputs`, `equivK_refl`,
`equivK_symm`, `equivK_trans`, `equivK_of_succ`).

## Three counts

For horizon `k`, with universe `U_k(f) = { f_w : |w| < k }`:

| symbol | meaning |
|--------|---------|
| `R_k(f)` | distinct residual polynomials in `U_k` |
| `S_k(f)` | extensional `Z→Z` residuals; equals `R_k` for ordinary `Z[x]` |
| `M_k(f)` | `\|U_k / ≡_k\|` exact Myhill–Nerode |
| sample | LSD signatures on a finite `x`-sample (**not** `M_k`) |
| levelled | remaining-depth unfolding size (clocked implementation) |

**REFUTED:** sample minimization = Myhill–Nerode. Witness `x^2`, `k=3`:
sample `7`, `M_3=13`.

## Exact minimization

The recursive characterization is the minimizer. Signatures are memoized
`(polynomial, remaining)` DAGs, not hashed sample outputs.

## State counts

**EXACT — HUMAN PROOF.** Residuals of `x^2` along distinct words are
distinct polynomials: `R_k(x^2) = (3^k − 1)/2` for `k ≥ 1` (`A=3^{|w|}`,
linear coefficient encodes the packed prefix). Lean:
`residualAlong_Xsq`, `residualAlong_Xsq_injective`.

**EXACT — HUMAN PROOF.** Finite-horizon classes of degree `≤ 2` are
coefficient triples modulo `3^k`. Distinct residuals of `x^2` in `U_k`
are therefore `≡_k`-separated, and

```text
M_k(x^2) = R_k(x^2) = (3^k − 1)/2    (k ≥ 1).
```

Lean supplies the separation theorem (`equivK_quad`, `xsq_equivK_iff_eq`);
the cardinal identity combines that with the prefix-tree count and the
existing upper bound. Details:
[quadratic_residual_complexity.md](quadratic_residual_complexity.md).

**COMPUTATIONALLY VERIFIED** through `k=7`:

```text
k     0  1  2   3   4    5    6     7
R=M   1  1  4  13  40  121  364  1093
```

Polynomial structure does **not** collapse the residual tree of `x^2`
at finite horizon `k`. Do **not** extend this to `x^d` for `d ≥ 3`.

**COMPUTATIONALLY VERIFIED** (through `k=6`):

```text
M_k(x)     = 1
M_k(x+1)   = 2   (k ≥ 2)
M_k(2x+1)  = 3   (k ≥ 3)
M_k(3x+1)  = 3   (k ≥ 2)
M_k(x^3)   = 1,1,3,12,36,115,349
M_k(x^4)   = 1,1,4,11,37,110,338
```

`x^3` and `x^4` do collapse: `M_k < R_k` for `k ≥ 2` (`x^3`) and
`k ≥ 3` (`x^4`).

Affine maps have finite unbounded-horizon residual sets.
**EXACT — HUMAN PROOF** for `x` (`𝔇_a x = x`). Degree `≥ 2` cannot:
`LC(𝔇_w f) = 3^{|w|(d−1)} LC(f)` produces infinitely many polynomials.

## Bounds

Upper: `M_k(f) ≤ R_k(f) ≤ (3^k − 1)/2 ≤ 3^k`.
**EXACT — HUMAN PROOF** (one residual per prefix; Lean
`residualAlong_word_bound` plus `equivK` quotient).

Lower, `x^2`: `M_k(x^2) ≥ k` from distinct leading coefficients along
`0^m`, and `M_1` separates `x^2` from `3x^2`.
**EXACT — LEAN VERIFIED** (`x_sq_not_equiv_one_three`).
The matching lower bound `M_k(x^2) ≥ (3^k − 1)/2` is the coefficient
invariant of
[quadratic_residual_complexity.md](quadratic_residual_complexity.md).

Last-layer `ρ`-vectors of `x^2` are **not** unique (`k=7`: 729 polys,
9 triples), so `≡_1` does not separate the last layer. Full `≡_k` still
did, through `k=7`.

Compression `3^k / M_k(x^2) → 2`. Prefix locality does **not** imply a
small automaton. **REFUTED:** locality ⇒ small state complexity.

## Composition

```text
outputAlong(w, f ∘ g) = outputAlong(outputAlong(w, g), f)
```

**EXACT — LEAN VERIFIED** (`outputAlong_comp`, `residualAlong_comp`).

Hence `M_k(f ∘ g) ≤ M_k(f) M_k(g)`.
**EXACT — HUMAN PROOF** (cascade of classes). Strict inequality:
`M_5(x^2 ∘ x^2) = M_5(x^4) = 110 < 121 · 121`.
**COMPUTATIONALLY VERIFIED.** The quadratic machine does not remain
uncompressed after composition: `x^4` is degree 4.

Negation: `ρ_a(f ∘ N) = ρ_{-a}(f)` and
`𝔇_a(f ∘ N) = (𝔇_{-a} f) ∘ N`.
**EXACT — HUMAN PROOF** / **COMPUTATIONALLY VERIFIED**.

## Normalization composition

Residual outputs are already trits, so output-side `N_B` is the identity.

Coefficient-side: residual `|coeff|` of degree `d ≥ 2` grows as
`3^{k(d-1)}`. For any fixed `B`, the bounded normalizer cannot represent
residuals once `max |coeff| > B`.
**EXACT — HUMAN PROOF** (leading-coefficient formula). Witness:
`x^2`, `k=4`, `B=5` is not representable.

Affine `x` remains representable at `B=1` for all tested `k`.

## `hat D`

On unbounded `Z` coefficients: **not** one FST (Milestone 14).

For fixed `B`: `hat D = N_B` then drop the first output trit. State
upper bound `2(2B+1)`. **EXACT — HUMAN PROOF**. The `[2]` witness remains:
`hat D([2]) = 1 ≠ D_coeff([2])`.

## Local confluence

**PROVED** modulo high-zero stripping (`BTCalculus/Confluence.lean`).
Unique stripped trit NF is `encodeZ(value)`; Strategy A reaches it;
the overlapping `(i, i+1)` pair joins. Raw `[1,0]` vs `[1,0,0]` from
`[-5,2]` is the stripping witness, not a confluence failure.

## Open problems

1. Closed form for `M_k(x^d)`, `d ≥ 3`. For `d=3` the count is the
   image of an explicit map `F_k`; see
   [cubic_residual_image.md](cubic_residual_image.md).
2. Myhill–Nerode join of the overlapping normalization pair.
3. Tight cascade bound (when equality holds).
4. Lean cardinality of trit words, to make `M_k(x^2)=(3^k−1)/2` a
   single Lean theorem rather than a human combination.

`M_k(x^2)=(3^k−1)/2` is no longer open: see
[quadratic_residual_complexity.md](quadratic_residual_complexity.md).

## Framing

The paper-level object is **polynomial residual automata** with a
**normalization-aware coefficient layer**, not a new derivative.
