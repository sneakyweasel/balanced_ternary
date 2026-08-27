# Nearest-cube reduction of persisted fourth-power hits

Exact integer analysis of the persisted `a < 10^8` hit list.
This is not a theorem and not a new search.

- hits: `465`
- exact cubes `a = k^3`: `464`
- `a = 97`: `1`
- other non-cubes: `0`
- odd non-squares: `0`
- odd-a inexact hits: `1`
- odd `a` forces `m` odd: `True`
- odd non-cube candidate even: `True`
- exact hits sit at the left endpoint: `True`

## Invariant

odd non-cube a forces m odd, so the unique inexact candidate n = m+1 is even.

even non-cube a would have m even and candidate m+1 odd; no such hit is in the persisted corpus.

## a = 97

- `m = 198635`
- `r = 118202679086`
- gap `(m+1)^3 - a^8 = 165506495`
- width `2a^4 = 177058562`
- `n = m+1`: `True`
- `n` even: `True`
- `a` not a cube: `True`

## Residues

Exact-family `n` follows `k^8` and is therefore even exactly
when `k` is even. The unique inexact hit is `a = 97 ≡ 1 (mod 32)`,
`n = 198636 ≡ 12 (mod 16)`. No other residue pattern is needed.

