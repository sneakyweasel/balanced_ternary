# Polynomial section calculus

Master record for Milestone 15. Unique balanced expansion is **standard**.
The 3-section operator on `Z[x]` is a **REPARAMETERIZATION** of known
p-section / Cartier / p-kernel constructions. What this repository
adds is the **normalization boundary** from Milestone 14 and trit-valued
control.

## Architecture (do not flatten)

```text
integer semantic layer          D, I_a, lsd          bt.calculus.derivative
polynomial semantic layer       𝔇_a, ρ_a             bt.calculus.section (Z[x])
raw coefficient layer           CoeffWord, D_coeff    bt.normtheory
canonical coefficient layer     encode / Strategy A   bt.representation, strategies
normalization boundary          P → NF(P)             bt.normtheory.rewrite
normalized derivative           hat D                 bt.normtheory.hatd
```

Never identify `D_coeff` with `D` unless the LSD is already a trit.
Never treat balanced trit coefficients of a polynomial as the same
object as `Z[x]`. `BTPolynomial` (trit word with `P(3)=n`) is a third
object and is not loosened.

The exact laws of `𝔇_a` live in ordinary `Z[x]`. Canonical digit words
are how integers (and integer values of polynomials) are displayed and
how `hat D` operates.

## Section derivative

For `a ∈ Z` (digit sections: `a ∈ {-1,0,+1}`):

```text
ρ_a(f) = [f(a)]_3 ∈ {-1,0,+1}
𝔇_a f(x) = (f(a+3x) - ρ_a(f)) / 3   ∈ Z[x]
```

**EXACT — LEAN VERIFIED** (`section_reconstruction`):

```text
f(a+3x) = ρ_a(f) + 3 𝔇_a f(x)     as polynomials in x
```

Closure `Z[x] → Z[x]` is definitional: the operator is constructed by
the binomial recurrence `(a+3X)^{n} = a^n + 3 powShift_n`, no
pointwise integer division.

## Product

**EXACT — LEAN VERIFIED** (`section_product`, `section_product_eval`):

```text
𝔇_a(fg) = ρ_a(f) 𝔇_a g + ρ_a(g) 𝔇_a f + 3 (𝔇_a f)(𝔇_a g)
```

This is the lift of the integer twisted Leibniz rule, not classical
Leibniz. **REFUTED:** `𝔇_a(fg) = (𝔇_a f)g + f(𝔇_a g)`.

## Composition

**EXACT — LEAN VERIFIED** (`section_comp`, `section_comp_eval`):

```text
𝔇_a(f ∘ g) = 𝔇_{ρ_a(g)} f ∘ 𝔇_a g
```

Branch-selecting chain rule. **REFUTED:** ordinary
`(𝔇 f)(g) · 𝔇_a g` with a section-independent `𝔇 f`.

## Degree

**EXACT — HUMAN PROOF** / **VERIFIED COMPUTATIONALLY**. For
`deg f = d ≥ 1`,

```text
deg(𝔇_a f) = d
LC(𝔇_a f) = 3^{d-1} LC(f)
```

**REFUTED:** degree-lowering `deg(𝔇_a f) = deg f - 1`. Witness `x^2`.

## Normalization interaction

```text
D(value(P)) = value(hatD_raw(P))
hatD(P) = encode(D(value(P))) = normalize(D_coeff(normalize(P)))
```

`hatD_raw` is one LSD `balanced_divmod` then drop (carry correction).
**EXACT — LEAN VERIFIED** (`hatDRaw_value`, `m14_witness_naive_ne`).

If `c_0` is a trit, naive drop equals semantic `D`
(`canonical_drop`).

**REFUTED** without that side condition. Witness `[2]`:
`[2] → [-1,1]`, `D(2)=1`, `D_coeff([2])=0`.

Canonical `hat D(I_a(P)) = normalize(P)`. Raw `hatD_raw(I_a(P)) = P`.

## Classification

**Outcome B**, with an operational **C-layer**: the section algebra is
known 3-section calculus; the project-specific theorem is the
normalization boundary and `hat D` as the coefficient-level semantic
derivative.

“Balanced-ternary jet calculus” names the residual-path object plus
trit residues. It is not a claim of a new differential-geometric jet
bundle.

Normalization theory and jet calculus are **two interacting layers**,
not one theory.

Milestone 16: residual Myhill–Nerode complexity lives in
[residual_state_complexity.md](residual_state_complexity.md). Sample
minimization is **not** `M_k`. `x^2` does not collapse at finite
horizon (`M_k=R_k` through `k=7`).
