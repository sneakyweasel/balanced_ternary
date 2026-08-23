# Jet transducers

Residual polynomials are the state of a section jet. This is not a new
Mealy theory in Lean.

## Raw states

For fixed `f ∈ Z[x]` and depth `k`,

```text
S_k(f) = { 𝔇_w f : |w| < k }
```

has size at most `(3^k − 1)/2`. That bound is combinatorial (ternary
words), not a minimization theorem.

**VERIFIED COMPUTATIONALLY** (`bt.calculus.jet_locality.profile_jet`), depth `k=3`:

| polynomial | raw | minimized | max \|coeff\| | LC abs |
|---|---:|---:|---:|---:|
| `x` | 1 | 1 | 1 | 1 |
| `x+1` | 2 | 2 | 1 | 1 |
| `2x+1` | 3 | 3 | 2 | 2 |
| `3x+1` | 3 | 3 | 3 | 3 |
| `x^2` | 13 | 7 | 9 | 9 |
| `x^3` | 13 | 4 | 108 | 81 |
| `x^4` | 13 | 8 | 1296 | 729 |
| `2-3x` | 4 | 3 | 3 | 3 |

Raw `13` is the combinatorial ceiling `(3^3−1)/2` of distinct section words of length `< 3`. For `deg ≥ 2` at this depth, every word yields a distinct residual polynomial; minimization (sample LSD signature) can still collapse some. Affine maps stay a small family.

Do **not** claim `state_count(f,k)=O(1)` for general polynomials.

## Minimization

Two residuals are identified when they produce the same LSD stream on a
finite sample of residual arguments. Minimized counts are
computational proxies, not Myhill–Nerode proofs.

**REFUTED** as a substitute for `M_k`. Witness `x^2`, depth `3`: sample
`7`, exact `M_3=13=R_3`. The equality `M_k(x^2)=R_k(x^2)=(3^k−1)/2` is
now a theorem:
[quadratic_residual_complexity.md](quadratic_residual_complexity.md).
See also [residual_state_complexity.md](residual_state_complexity.md).

## Locality

**PROVED** for `f ∈ Z[x]`: `f(n) ≡ f(m) (mod 3^k)` whenever
`n ≡ m (mod 3^k)`, so the low `k` canonical trits of `f(n)` depend only
on the low `k` input trits (prefix locality).

**REFUTED:** output trit `i` is a function of input trit `i` alone
(`x^2`).

## Normalization vs unbounded coefficients

Milestone 14: fixed alphabet `[-B,B]` admits an LSD Mealy normalizer;
unbounded `Z` coefficients do not. Jet states of a *fixed* polynomial
at *fixed* `k` are finite, but coefficient magnitude of residuals
grows with `k` for `deg ≥ 2`. Do not lift finite-`B` normalization to
the residual algebra of `x^d`.

## Information

Input lookahead for the first `k` output trits of a polynomial map is
the first `k` input trits (prefix locality). Output delay is 0 in that
window. Normalization rewrite counts for displaying residual
coefficients are a separate cost, measured by Strategy A on those
coefficient words when needed.
