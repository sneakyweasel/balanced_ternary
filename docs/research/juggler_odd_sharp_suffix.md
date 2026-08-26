# Juggler odd-start sharp even-tower suffixes

Status: **ODD_SHARP_SUFFIX_INCOMPLETE**

Standalone application phase. Not a Research Engine experiment and
not a termination theorem. This page records the inverse-floor form
of an odd Juggler step and the search for sharp suffixes `OE^s`.

## Branch budget

```text
Mathematical target     Can odd n have T(n)=a^{2^s} for unbounded s
                        (sharp OE^s)?
Novelty hypothesis      s≥2 is impossible, or a finite exceptional
                        family, or an infinite odd family
Falsifier               An odd n with square_depth(T(n))≥2, or a failed
                        obstruction
Existing machinery      localDefectOdd, power_deficit_eq_local_odd_iff,
                        HasPowTwoDepth, isqrt
Maximum Phase-0 scope   Inverse-floor lemma; integer-root search past
                        2000; smallest s≥2 obstruction or witness
```

## Metadata

- odd scan: `n <= 50000`
- fourth-power scan: `b <= 2500`
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

the inverse-floor reduction is Lean-verified and no odd s ≥ 2 hit was found, but a finite-search empty set is not an impossibility theorem.

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

the inverse-floor reduction is Lean-verified and no odd s ≥ 2 hit was found, but a finite-search empty set is not an impossibility theorem.

This is a local inverse-floor statement, not a global halt result.

