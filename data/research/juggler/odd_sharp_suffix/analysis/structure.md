# Observed fourth-power interval structure

Outcome: **ODD_FOURTH_POWER_STRUCTURE_DISCOVERED**
Witness outcome: **ODD_FOURTH_POWER_NO_WITNESS**
Proof-ready: **no**

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

This is computational evidence. It is not a theorem. The preferred
Lean target remains

```text
T(n) = a^4 and n odd  =>  n is a square.
```

## Cheap exact facts used by the search

- Occupancy is 0 or 1: the interval width `2a^4 + 1` is smaller than
  the next-cube gap once a cube sits at or above `a^8`.
- Even `a` forces even `n`.
- An odd square `n` with `T(n) = a^4` is exactly an eighth power.

## What the search adds

Interval emptiness is the wrong conjecture: `a = 97` is a cube in the
interval. The remaining restriction is oddness of `n`, and on this
range the only odd preimages are squares.

No congruence was found that forbids an inexact odd cube in general.
`a = 97` is odd and still produces an even `n`.

## Decision

Park the computational conjecture. Do not open Lean in this phase.
Do not treat `a < 10^8` emptiness as impossibility.
