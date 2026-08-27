# Juggler odd-start sharp even-tower suffixes

Status: **ODD_SHARP_SUFFIX_INCOMPLETE**

Standalone application phase. Not a Research Engine experiment and
not a termination theorem. This page records the inverse-floor form
of an odd Juggler step and the search for sharp suffixes `OE^s`.

## Branch budget

```text
Mathematical target     non-cube a and even m => (m+1)^3-a^8 > 2a^4
Novelty hypothesis      elementary gap bound or finite A0
Falsifier               even-m non-cube window hit
Existing machinery      nearest-cube Lean, persisted 465-hit corpus
Maximum Phase-0 scope   even-m surplus analysis; Lean only a bound
                        the analysis actually yields
```

## Metadata

- odd scan: `n <= 50000`
- fourth-power scan: `b <= 2500` (in-memory probe)
- persisted exact search: `1 <= a < 10^8` in
  `data/research/juggler/odd_sharp_suffix/`
- eighth-power scan: `a <= 150`
- engine control layer modified: `False`
- classification: **ODD_SHARP_SUFFIX_INCOMPLETE**
- odd first-defect depth ≥ 1: `13`
- odd first-defect depth ≥ 2: `0`
- s=1 bases that are squares: `0`
- fourth-power odd hits: `0`
- fourth-power even hits: `1`
- eighth-power odd hits: `0`
- sorry-free: `True`

nearest-cube Lean covers occupancy, the exact family, and odd m implying even n; even-m surplus analysis did not yield an elementary gap bound.

## Inverse-floor reduction

For odd `n`,

```text
T(n) = M  ↔  M^2 ≤ n^3 < (M+1)^2
```

is the definition of `Nat.sqrt` on `n^3`. Specializing `M = a^{2^s}`
gives the exact Diophantine interval

```text
a^{2^{s+1}} ≤ n^3 < (a^{2^s} + 1)^2
```

No real `n^{3/2}` is used. A large finite search is not a theorem.

Nearest-cube Lean: the window holds at most one cube; a cube `a`
places `n = k^8` at the left endpoint; a non-cube leaves only
`n = m+1`; that candidate is even exactly when `m` is odd. The
even-`m` leftover is open. `a = 3` shows that odd `a` need not
make `m` odd. Even-`m` discovery (`a <= 20000`) found no window
hit; `a = 37840` shows an eighth power can sit at the top of a
cube cell, so a uniform remaining-fraction bound is false. Notes:
`data/research/juggler/odd_sharp_suffix/analysis/even_cbrt.md`.

## Odd first-defect census

Odd `n` that are not locally exact, with `square_depth(T(n)) ≥ 1`.
All recorded depths are `1`. The `s = 1` family includes
`11 → 36 = 6^2` and `37 → 225 = 15^2`.

- n `11`: T `36` = `6`^2, depth `1`, sharp suffix `1`
- n `37`: T `225` = `15`^2, depth `1`, sharp suffix `1`
- n `339`: T `6241` = `79`^2, depth `1`, sharp suffix `1`
- n `797`: T `22500` = `150`^2, depth `1`, sharp suffix `1`
- n `905`: T `27225` = `165`^2, depth `1`, sharp suffix `1`
- n `927`: T `28224` = `168`^2, depth `1`, sharp suffix `1`
- n `1077`: T `35344` = `188`^2, depth `1`, sharp suffix `1`
- n `1771`: T `74529` = `273`^2, depth `1`, sharp suffix `1`
- n `1797`: T `76176` = `276`^2, depth `1`, sharp suffix `1`
- n `8115`: T `731025` = `855`^2, depth `1`, sharp suffix `1`
- n `14363`: T `1721344` = `1312`^2, depth `1`, sharp suffix `1`
- n `16231`: T `2067844` = `1438`^2, depth `1`, sharp suffix `1`
- n `23055`: T `3500641` = `1871`^2, depth `1`, sharp suffix `1`

## Fourth-power interval

For `s ≥ 2` one may take `M = b^4`. A cube in
`[M^2, (M+1)^2)` is possible: `b = 97` gives the even preimage
`n = 198636`. That is an even cube, so
it is not an odd Juggler step. No odd preimage was found.

The persisted exact search `1 <= a < 10^8` (dataset
`data/research/juggler/odd_sharp_suffix/`) found 465 interval cubes:
the exact family `a = k^3`, `n = k^8` for `k <= 464`, plus the one
inexact even hit `a = 97` (`m = 198635` odd). Zero odd non-squares.
Nearest-cube notes:
`data/research/juggler/odd_sharp_suffix/analysis/nearest_cube.md`.
That finite search is not a theorem. “Even `a` forces even `n`” is
only an observation on the hit set.

- even hits (truncated): `[{'b': 97, 'M': 88529281, 'n': 198636, 'parity': 'even', 'n3_minus_M2': 165506495, 'interval_len': 177058563, 'exact_cube': False}]`
- odd hits: `[]`
- eighth-power odd hits: `[]`
- eighth-power even hits: `[]`

## Even-start contrast

An even first defect `n = q^2 + r` has `T(n) = q`. If `q` is a
sufficiently deep 2-power, the exact even tower can be arbitrarily
long. Samples:

- n `18`: T `4`, depth `1`, word starts even
- n `258`: T `16`, depth `2`, word starts even
- n `65538`: T `256`, depth `3`, word starts even

The remaining asymmetry is therefore: even first defects admit
unbounded sharp suffixes `E^s`; odd first defects are only known
to support `OE` (`s = 1`).

## Lean

- `floor_sqrt_eq_iff_sq_interval`: `True`
- `floorPower_odd_eq_iff_cube_interval`: `True`
- `floorPower_odd_eq_pow_two_depth_iff`: `True`
- `fourth_window_occupancy`: `True`
- `exact_cube_left_endpoint`: `True`
- `fourth_window_cube_eq_succ_cbrt`: `True`
- `noncube_odd_cbrt_fourth_window_cube_even`: `True`
- `odd_cube_interval_of_odd_cbrt_implies_square`: `True`
- `floorPower_odd_eq_fourth_power_of_odd_cbrt_implies_square`: `True`
- `odd_nonsquare_not_fourth_power_of_odd_cbrt`: `True`
- `odd_first_defect_not_pow_two_depth_ge_two_of_odd_cbrt`: `True`
- impossibility theorem: `False`
- `PowerHeight` absent: `True`
- `PowerBoundStrict` absent: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`

## Decision

**ODD_SHARP_SUFFIX_INCOMPLETE**

nearest-cube Lean covers occupancy, the exact family, and odd m implying even n; even-m surplus analysis did not yield an elementary gap bound.

This is a local inverse-floor statement, not a global halt result.

