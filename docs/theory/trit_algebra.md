# Trit algebra

**Status of this page:** our exact formalization of the 3-element chain
`{-1, 0, +1}`. This is existing finite-lattice mathematics, now first-class
in the laboratory. It is **not** a Boolean algebra.

## Historical inspiration

Setun used a signed trit as a machine digit and as a control/sign value.
That is engineering motivation only. No Setun source is cited here as a
theorem about lattices.

## Existing mathematics

The three-element chain is the unique (up to isomorphism) bounded
distributive lattice with three elements. Equipping it with the
order-reversing involution `neg(-1)=+1`, `neg(0)=0`, `neg(+1)=-1` yields
the **3-element Kleene algebra** (a De Morgan algebra satisfying
`min(a, neg(a)) ≤ max(b, neg(b))`). This structure appears in Kleene’s
three-valued logic and in Łukasiewicz 3-valued logic as the truth-value
lattice. It is not Boolean: `max(0, neg(0)) = 0 ≠ +1`.

## Our formalization

Python: `bt.calculus.trit.Trit` (`IntEnum`). Lean: existing
`CollatzDual.Warp.Trit` plus `BTCalculus.TritAlgebra`.

Exact operations:

- `neg`, `min`, `max`, `sign`, `compare`
- order `-1 < 0 < +1`

Verified laws (exhaustive on 3 elements; Lean by cases):

- associativity, commutativity, idempotence of `min` and `max`
- absorption
- distributivity both ways
- De Morgan identities
- Kleene inequality
- `neg` is an involution and order-reversing

**PROVED (LEAN VERIFIED):** not Boolean, via `not_boolean_zero`.

## Computational observations

None beyond the finite check. The algebra is finite, so the Python
exhaustive check is a complete proof of the equational laws; Lean
re-checks them by cases.

## Conjectures

None.
