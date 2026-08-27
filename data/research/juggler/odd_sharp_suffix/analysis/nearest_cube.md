# Nearest-cube reduction of persisted fourth-power hits

Exact integer analysis of the persisted `a < 10^8` hit list.
This is not a theorem and not a new search.

- hits: `465`
- exact cubes `a = k^3`: `464`
- `a = 97`: `1`
- other non-cubes: `0`
- odd non-squares: `0`
- odd-a inexact hits: `1`
- inexact hits are `n = m+1`: `True`
- odd-`m` inexact hits have even `n`: `True`
- odd `a` need not force odd `m` (`a=3`): `True`
- exact hits sit at the left endpoint: `True`

## Invariant

a non-cube leaves at most the candidate n = m+1; that candidate is even exactly when m is odd. The only persisted inexact hit is a = 97, where m is odd and n is even.

an even m makes n = m+1 odd. Odd a does not force m odd (a = 3 has m = 18). No persisted hit has even m except the exact even family a = k^3. The leftover is: a non-cube with even m never places m+1 in the window.

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

