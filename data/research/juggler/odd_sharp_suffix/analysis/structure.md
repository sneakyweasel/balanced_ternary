# Observed fourth-power interval structure

Outcome: **ODD_FOURTH_POWER_STRUCTURE_DISCOVERED**
Witness outcome: **ODD_FOURTH_POWER_NO_WITNESS**
Proof-ready: **no** (even-`m` leftover)

On the persisted range `1 <= a < 10^8` the integer interval

```text
[a^8, (a^4 + 1)^2)
```

contains a cube for exactly 465 values of `a`. Those cubes are:

1. The exact left-endpoint family `a = k^3`, `n = k^8`, for
   `1 <= k <= 464`.
2. One inexact even cube: `a = 97`, `n = 198636`.

There is no `ODD_NON_SQUARE` hit. Odd cubes occur only when `a` is an
odd cube, hence `n` is an eighth power.

This is computational evidence. It is not a theorem.

## Lean nearest-cube facts

**EXACT — LEAN VERIFIED** in `FloorPower.lean`:

- Occupancy is at most one cube.
- If `a = k^3`, the unique cube is `n = k^8`.
- If `a` is not a cube, the only possible cube is `n = m+1`,
  where `m = ⌊∛(a^8)⌋`.
- That candidate is even exactly when `m` is odd.

The restricted claim `T(n)=a^4`, `n` odd, and `m` odd implies `n` is
a square is therefore Lean. The unrestricted English target is not.

## Retracted observations

- “Even `a` forces even `n`” is only an observation on the hit set
  (every even hit is an exact `k^3`). It is not a theorem.
- “Odd `a` forces `m` odd” is false: `a = 3` has `3^8 = 6561` and
  `m = 18`. The candidate `19` misses the window.

## Leftover

The only remaining counterexample shape is a non-cube `a` with even
`m` such that `(m+1)^3 - a^8 ≤ 2a^4`. Discovery on `a <= 20000`
found none. A uniform remaining-fraction bound is false (`a = 37840`
sits at the top of its cube cell and still misses). The trivial
bound `m >= a^{8/3}-1` cannot produce a threshold. Finite emptiness
is not a theorem.

Interval emptiness is the wrong conjecture: `a = 97` is a cube in the
interval (`m` odd, `n` even).

## Decision

**PARK**. Keep the nearest-cube Lean. Do not treat `a < 10^8`
emptiness as impossibility. Do not claim `ODD_FOURTH_POWER_GREEN`
or `ODD_SHARP_SUFFIX_GREEN`.
