# Even cube-root modular obstruction

Targeted residue tables for even `m = ⌊∛(a^8)⌋`.
This is not a generic modular framework, not a `10^8` rerun,
and not a theorem.

- discovery `a_max`: `2000`
- even-`m` non-cubes: `1021`
- even-`m` window hits: `0`
- classification: **OBSTRUCTION_NOT_MODULAR**

## Parity (Candidate A)

- even `m`, even `a` ⇒ `D` odd: `True`
- even `m`, odd `a` ⇒ `D` even: `True`
- `a=97` has odd `D`: `True`
- `a=3` has even `D`: `True`

Parity splits the cases but does not contradict `0 < D ≤ 2a^4`.
Candidate A: `False`.

## a = 97 regression

- `m = 198635` even: `False`
- in window: `True`
- `D = 165506495`, `v2(D) = 0`

## a = 3 even-`m` miss

- `m = 18` even: `True`
- in window: `False`
- `D = 298`

Because `a=3` is a live even-`m` pair, no modulus can claim that
even `m` is impossible. An obstruction must use `D ≤ 2a^4`.

## Odd `a` modulo 32

- odd eighth powers: `[1]`
- `2a^4` for odd `a`: `[2]`
- even-`m` `r` counts: `{'25': 140, '9': 128, '1': 235}`
- even-`m` `D` counts: `{'10': 28, '30': 32, '6': 41, '22': 32, '8': 31, '18': 43, '4': 35, '26': 31, '0': 32, '2': 38, '28': 25, '12': 31, '14': 23, '24': 30, '16': 21, '20': 30}`

## Modulus tables

Each row is observed even-`m` non-cubes on the discovery range.
Empty even-`m` classes would be Candidate B/C. None are empty.

- q `2`: even-`m` classes `2`, empty `False`, `D` residues `[0, 1]`
- q `4`: even-`m` classes `8`, empty `False`, `D` residues `[0, 1, 2, 3]`
- q `8`: even-`m` classes `32`, empty `False`, `D` residues `[0, 1, 2, 3, 4, 5, 6, 7]`
- q `16`: even-`m` classes `128`, empty `False`, `D` residues `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
- q `32`: even-`m` classes `448`, empty `False`, `D` residues `32 values`
- q `64`: even-`m` classes `801`, empty `False`, `D` residues `64 values`
- q `128`: even-`m` classes `965`, empty `False`, `D` residues `128 values`
- q `3`: even-`m` classes `9`, empty `False`, `D` residues `[0, 1, 2]`
- q `5`: even-`m` classes `25`, empty `False`, `D` residues `[0, 1, 2, 3, 4]`
- q `7`: even-`m` classes `49`, empty `False`, `D` residues `[0, 1, 2, 3, 4, 5, 6]`
- q `9`: even-`m` classes `81`, empty `False`, `D` residues `[0, 1, 2, 3, 4, 5, 6, 7, 8]`
- q `13`: even-`m` classes `169`, empty `False`, `D` residues `[0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]`
- q `15`: even-`m` classes `223`, empty `False`, `D` residues `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]`
- q `24`: even-`m` classes `278`, empty `False`, `D` residues `24 values`

## Candidates

- A pure parity: `False`
- B some `2^k` empties even `m`: `False`
- C mixed small modulus empties even `m`: `False`
- D modular + size: `False`
- E not modular: `True`

## Invariant

even m occurs (a=3); D is odd when a is even and even when a is odd. For odd a, a^8 ≡ 1 (mod 32) and 2a^4 ≡ 2 (mod 32), and r ≡ 1,9,25 (mod 32) on the discovery range. None of these forces D > 2a^4. a=97 remains an odd-m window hit.

a non-cube with even m and D <= 2a^4 is not ruled out by parity, 2^k, or the small odd/mixed moduli. The leftover is still that size inequality.

