# Digit derivative and integral

**Status of this page:** existing operator identities, restated as a
calculus of `D` and `I_a`, plus two exact correction laws.

## Historical inspiration

None required. The maps are the integer forms of “drop LSD” and
“prepend LSD” on a balanced-ternary word.

## Existing mathematics

Unique canonical expansion `n = Σ a_i 3^i` with `a_i ∈ {-1,0,+1}` already
implies

```text
n = lsd(n) + 3 D(n),    D(n) = (n - lsd(n))/3.
```

`D` is **not** floor division: `D(2)=1`, `D(-1)=0`. These facts were
already **PROVED** in [balanced_ternary_operators.md](../balanced_ternary_operators.md)
and Lean `evalMSD_dropLSD`, `D_after_S`.

## Our formalization

Wrappers in `bt.calculus.derivative` / `bt.calculus.integral` call
`bt.operators.digit_derivative`, `lsd_digit`, and `I_a(n)=3n+a`.
Word maps remain `drop_lsd_word` and `prepend_lsd_word`.

**PROVED / LEAN VERIFIED** (`formal/BTCalculus/`):

1. `n = lsdZ n + 3 * DZ n`
2. `DZ (IZ a x) = x`
3. `IZ a (DZ n) = n` iff `lsdZ n = a.toInt`
4. `DZ (SZ n) = n` and `SZ (DZ n) = n - lsdZ n`
5. Projections `PZ a n = IZ a (DZ n)` form a **left-zero band**:
   `PZ a (PZ b n) = PZ a n`
6. `DZ (PZ a n) = DZ n`
7. Word/integer: `evalMSD (dropLSD w) = DZ (evalMSD w)` on nonempty words;
   `evalMSD (integralWord a w) = IZ a (evalMSD w)`

`digit_at(n,k) = lsd(D^k(n))` recovers the canonical LSD-first digits
(existing `recovered_digits`).

## Sum and product rules

**Sum (elegant reformulation of the carry table).**
Using existing `rewrite_sum` on `lsd(x)+lsd(y)`:

```text
D(x+y) = D(x)+D(y)+carry(lsd(x),lsd(y))
```

**PROVED (LEAN VERIFIED)** as `D_add`. This **is** the standard
balanced-ternary addition carry, written as a D-law.

**Product (twisted Leibniz rule).**
Because `lsd(x) lsd(y) ∈ {-1,0,+1}`:

```text
lsd(xy) = lsd(x) lsd(y)
D(xy)   = lsd(x) D(y) + lsd(y) D(x) + 3 D(x) D(y)
```

**PROVED (LEAN VERIFIED)** as `lsdZ_mul`, `D_mul`. This is not
`x D(y)+y D(x)`. The extra term is `3 D(x) D(y)`, not `6 D(x) D(y)`.
It follows from the unique decomposition; it is a calculus identity,
not an independent arithmetic theorem.

## Computational observations

Python checks the decomposition on `|n| ≤ 10^6` and the product/sum
rules on `[-200,200]²` plus random pairs in `[-10^6,10^6]`.

## Conjectures

None. Do not promote the twisted product rule into a “new derivation
on all functions `ℤ→ℤ`”.
