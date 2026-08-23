# Balanced-ternary jets

Claim labels: **PROVED**, **VERIFIED COMPUTATIONALLY**, **CONJECTURE**,
**REFUTED**, **REPARAMETERIZATION**.

This is not a classical Taylor jet. A function jet is a finite path of
*residual section polynomials* indexed by an input trit word.

## Integer jets

**PROVED.** For `k ≥ 0`,

```text
J_k(n) = (lsd(n), lsd(D(n)), …, lsd(D^{k-1}(n)))
```

and `n = pack(J_k(n)) + 3^k D^k(n)`. This is iterated digit
decomposition (`BTC-decomp`).

## Function jets

For a polynomial `f ∈ Z[x]` and a section word `w = a0…a_{k-1}` with
each `a_i ∈ {-1,0,+1}`:

```text
f_ε = f
f_{wa} = 𝔇_a(f_w)
b_i = ρ_{a_i}(f_{a0…a_{i-1}})
```

**PROVED** (Python exhaustive on stated boxes; Lean
`function_jet_reconstruction`):

```text
f(n) = b0 + 3 b1 + … + 3^{k-1} b_{k-1} + 3^k f_w(D^k(n))
```

when `w = J_k(n)`. The output trits `b_i` depend on the residual
polynomial state, not only on the matching input trit `a_i`.

## Residual functions

The residual `f_w` is again in `Z[x]`. For `deg f = d ≥ 1`,
`deg(f_w) = d` and leading coefficients grow by `3^{d-1}` at each
section step. Constants eventually become the zero polynomial when the
value is a trit.

## Terminology

“Balanced-ternary jet calculus” is justified only as a *name for this
path of residuals plus the integer jet*. It is **not** a jet space in
the sense of differential geometry. Literature overlap: 3-kernels of
polynomial sequences / section operators. See
[polynomial_jet_calculus.md](polynomial_jet_calculus.md) and
[residual_state_complexity.md](residual_state_complexity.md).
