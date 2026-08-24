# Trit control algebra

**Status of this page:** `cmp3` and `select3` as a formal ordered-control
language. Nested `select3` represents every function `Trit → ℤ`.
Compilation to sequential transducers is **not** automatic.

## Historical inspiration

Setun used the sign trit in control and addressing. That is engineering
motivation. The primitive below is ours.

## Existing mathematics

Integer trichotomy and piecewise definitions of `abs`, `min`, `max`
are standard. Trit-valued comparison is the sign of a difference.

## Our formalization

```text
cmp3(x,y) = sign(x-y) ∈ {-1,0,+1}
select3(c, x_minus, x_zero, x_plus)
```

**EXACT — LEAN VERIFIED:**

- `cmp3(x+z, y+z) = cmp3(x,y)`
- `cmp3(-x,-y) = -cmp3(x,y)`
- `cmp3(x,y) = -cmp3(y,x)`
- `cmp3(c x, c y) = cmp3(x,y)` for `c>0`
- `cmp3(c x, c y) = -cmp3(x,y)` for `c<0`
- `select3` on the three values of `f : Trit → ℤ` recovers `f`
- `abs`, `min`, `max` via `select3`/`cmp3` agree with the usual functions

Other `trit_if` sketches (sign-weighted averages, two-way tests) are
not primitives.

Piecewise library (`bt.calculus.select`): `abs_z`, `max_z`, `min_z`,
`sign_z`, `clamp_z`, `median_z`. These are exact definitions. They are
not claimed to be “especially small circuits”.

The postfix VM (`bt.calculus.vm`) evaluates

```text
x y CMP3 a b c SELECT3
```

as `select3(cmp3(x,y), a, b, c)`. It is a mathematical stack evaluator,
not a Setun cycle emulator.

## Computational observations

Piecewise functions match Python `abs`/`min`/`max`/`median` on
`[-40,40]`. Expression-size comparisons for `n+1` are observations
only.

## Conjectures

Which piecewise arithmetic functions are sequential as balanced-ternary
word maps remains the existing transducer classification. `select3` does
not by itself produce a finite-state implementation of `W` or odd-part.
