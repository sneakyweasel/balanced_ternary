# Even cube-root surplus of fourth-power windows

Discovery scan of non-cube `a` with even `m = ⌊∛(a^8)⌋`.
This is not a `10^8` rerun and not a theorem.

- discovery `a_max`: `20000`
- even-`m` non-cubes: `9971`
- even-`m` window hits: `0`
- trivial `m >= a^{8/3}-1` cannot threshold: `True`

## a = 97 must survive

- `m = 198635` odd: `True`
- in window: `True`
- surplus `gap - 2a^4 = -11552067`

## a = 3 even-`m` miss

- `m = 18` even: `True`
- in window: `False`
- surplus: `136`

## Closest even-`m` near-misses

Ranked by `gap / (2a^4)`. All listed ratios are `> 1`.

Minimum surplus is `a = 2`, surplus `55`.

- a `3`: m `18`, gap `298`, width `162`, surplus `136`
- a `6`: m `118`, gap `5543`, width `2592`, surplus `2951`
- a `79`: m `114904`, gap `177861064`, width `77900162`, surplus `99960902`
- a `2`: m `6`, gap `87`, width `32`, surplus `55`
- a `37`: m `15200`, gap `21711680`, width `3748322`, surplus `17963358`
- a `4`: m `40`, gap `3385`, width `512`, surplus `2873`
- a `73`: m `93080`, gap `446156360`, width `56796482`, surplus `389359878`
- a `12`: m `754`, gap `387179`, width `41472`, surplus `345707`

## High interval position

Example `a = 37840` has even `m = 1613874181766`,
`r = 7813705284528762532036904`, cube gap `7813769623717469643181567`,
remaining gap `64339188707111144663`, width `4100478192926720000`.
The eighth power can sit at the top of a cube cell. A uniform
positive remaining-fraction lemma is false. The candidate is
still outside the window (in_window `False`).

## Invariant

a non-cube with even m never placed m+1 in the window on the discovery range; a=97 remains an odd-m hit; interval position can sit at the top of a cube cell, so a uniform remaining-fraction bound is false.

the trivial bound m >= a^{8/3}-1 is sharp and cannot produce an A0. Proving gap > 2a^4 for even m needs more than cube-root bracketing.

