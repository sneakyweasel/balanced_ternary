# Exact left-endpoint cubes

If `a = k^3`, then `a^8 = k^{24} = (k^8)^3`, so `n = k^8` sits at the
left endpoint of `[a^8, (a^4+1)^2)`. Classification:

- `k` odd → `n` odd and an eighth power → `ODD_SQUARE`
- `k` even → `n` even → `EVEN_CUBE`

This is the entire odd-square family. An odd square `n = b^2` satisfies
`T(n) = b^3`, so `b^3 = a^4` forces `a = k^3` and `n = k^8`.

The leftover question is not “odd `a` that is not a cube”. Odd `a`
need not make `m = ⌊∛(a^8)⌋` odd (`a = 3` has `m = 18`). The only
remaining counterexample shape is a non-cube with even `m` that places
`n = m+1` in the window.
