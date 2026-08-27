# Near-square / near-cube gap of even-m fourth-power windows

Discovery scan of the displacement `(u, v)` around the exact family
`a = k^3`, `m = k^8`. This is not a `10^8` rerun, not a modular
search, and not a theorem.

- discovery `a_max`: `20000`
- neighborhood `k_max`: `30`
- `u` radius: `6`
- even-`m` non-cubes: `9971`
- even-`m` window hits: `0`
- same sign `(u, v)`: `9971`
- leave nearest exact-family cell: `9971`
- classification: **DIOPHANTINE_ESCALATION_REQUIRED**

## a = 97 must survive

- `a = 97`, nearest cube `k = 5`, `u = -28`
- `m = 198635` odd: `True`
- `v = -191990` (same sign as `u`: `True`)
- left exact-family cell: `True`
- in window: `True`
- surplus `D - 2a^4 = -11552067`

Route A (`a` non-cube `⇒ D > 2a^4`) is false at this example.
Leaving the exact-family cell does not force a miss.

## Closest even-`m` failures

Ranked by `D / (2a^4)`. These are the sharp local near-misses.
They are not the integers closest to a cube.

Minimum surplus is `a = 2`, `u = 1`, surplus `55`.

`a = 3` has `k = 1`, `u = 2`, `m = 18`, `v = 17`, surplus `136`.

- a `3`: k `1`, u `2`, m `18`, v `17`, surplus `136`
- a `6`: k `2`, u `-2`, m `118`, v `-138`, surplus `2951`
- a `79`: k `4`, u `15`, m `114904`, v `49368`, surplus `99960902`
- a `2`: k `1`, u `1`, m `6`, v `5`, surplus `55`
- a `37`: k `3`, u `10`, m `15200`, v `8639`, surplus `17963358`
- a `4`: k `1`, u `3`, m `40`, v `39`, surplus `2873`
- a `73`: k `4`, u `9`, m `93080`, v `27544`, surplus `389359878`
- a `12`: k `2`, u `4`, m `754`, v `498`, surplus `345707`

## Closest to the next cube

Even-`m` non-cubes with largest `r / (3m^2+3m+1)`. A hit needs
`r` in the top slice of width `2a^4`. Sitting high in the cell
is not enough by itself (`a = 37840`).

- a `19970`: u `287`, r `258463783458915667498432`, cube gap `258506182366956060298669`, surplus `42080823724711180237`
- a `4952`: u `39`, r `152238900049301918056`, cube gap `152271273549880899631`, surplus `31170813792044743`
- a `11784`: u `-383`, r `15507062329980313616896`, cube gap `15512525264841734468521`, surplus `5424369186958102953`
- a `7720`: u `-280`, r `1625012558163129071496`, cube gap `1625848931117065896871`, surplus `829269015371705375`
- a `11473`: u `-694`, r `13443153440895480274617`, cube gap `13450297400620130003011`, surplus `7109306953536501512`
- a `15341`: u `-284`, r `63301203033799535773657`, cube gap `63339431495304440879011`, surplus `38117685760944043432`
- a `9642`: u `381`, r `5317483921556298513400`, cube gap `5321236966991802566227`, surplus `3735759276468991035`
- a `2691`: u `-53`, r `5883809808120640993`, cube gap `5888359393955730469`, surplus `4444707740942754`

## Exact-family neighborhood `a = k^3 + u`

Checked `1 <= k <= 30` and `1 <= |u| <= 6`.

- neighborhood rows: `354`
- any window hit: `0`
- even-`m` window hit: `0`
- `|u| = 1` window hits: `0`
- `|u| = 1` still in the `k^8` cell: `0`
- non-cube occupants of an exact-family cell: `0`

The linear increment `8k^{21}u` already exceeds the cell width
`3k^{16}+3k^8+1` for every checked `k >= 1` and `|u| >= 1`.
Sign of `v` matched sign of `u` on the discovery even-`m` set,
but that is only an observation. Nonzero `u` jumps to a
different cube cell; it does not identify the gap `D`.

## Sample `|u| = 1` rows

- k `1`, u `1`, a `2`: m `6`, v `5`, even m `True`, leaves ref cell `True`, in window `False`, surplus `55`
- k `2`, u `-1`, a `7`: m `179`, v `-77`, even m `False`, leaves ref cell `True`, in window `False`, surplus `62397`
- k `2`, u `1`, a `9`: m `350`, v `94`, even m `True`, leaves ref cell `True`, in window `False`, surplus `183708`
- k `3`, u `-1`, a `26`: m `5932`, v `-629`, even m `True`, leaves ref cell `True`, in window `False`, surplus `16522709`
- k `3`, u `1`, a `28`: m `7229`, v `668`, even m `False`, leaves ref cell `True`, in window `False`, surplus `129839352`
- k `4`, u `-1`, a `63`: m `62840`, v `-2696`, even m `True`, leaves ref cell `True`, in window `False`, surplus `2749315878`
- k `4`, u `1`, a `65`: m `68302`, v `2766`, even m `True`, leaves ref cell `True`, in window `False`, surplus `9124262252`
- k `5`, u `-1`, a `124`: m `382347`, v `-8278`, even m `False`, leaves ref cell `True`, in window `False`, surplus `383980752064`
- k `5`, u `1`, a `126`: m `399013`, v `8388`, even m `False`, leaves ref cell `True`, in window `False`, surplus `5424034616`

## Adversarial regressions

- a `1`: cube `True`, u `0`, m even `False`, in window `False`, surplus `5`
- a `2`: cube `False`, u `1`, m even `True`, in window `False`, surplus `55`
- a `3`: cube `False`, u `2`, m even `True`, in window `False`, surplus `136`
- a `5`: cube `False`, u `-3`, m even `False`, in window `False`, surplus `13349`
- a `6`: cube `False`, u `-2`, m even `True`, in window `False`, surplus `2951`
- a `8`: cube `True`, u `0`, m even `True`, in window `False`, surplus `189185`
- a `27`: cube `True`, u `0`, m even `False`, in window `False`, surplus `128096965`
- a `79`: cube `False`, u `15`, m even `True`, in window `False`, surplus `99960902`
- a `97`: cube `False`, u `-28`, m even `False`, in window `True`, surplus `-11552067`
- a `125`: cube `True`, u `0`, m even `False`, in window `False`, surplus `457276562501`
- a `37840`: cube `False`, u `-1464`, m even `True`, in window `False`, surplus `60238710514184424663`

## Routes

- A unrestricted non-cube gap: `False`
- B exact-family cell exclusive: `True`
- B leaving the cell implies a miss: `False`
- B `|u|=1` closes the window: `True`
- C elementary fourth-power rigidity: `False`
- D trivial `D >= 1` threshold: `False`
- target empty on discovery: `True`
- observation `surplus >= a^4` on discovery: `True`

Route B's exclusive-cell fact is elementary and true, but it is
not a lower bound on `D` in the *new* cell. Route C would need
a quantitative gap for `X^2 - Y^3` with `X = a^4`; that is not
an integer-polynomial comparison. Route D cannot start because
`m >= a^{8/3}-1` is sharp.

## Unresolved Diophantine statement

a non-cube and m = floor_cbrt(a^8) even imply (m+1)^3 - a^8 > 2a^4.

No Baker, Thue, or Mordell machinery is introduced.

## Invariant

the exact-family cube cell of k^8 holds a^8 only for a = k^3; nonzero u immediately leaves that cell. This does not force D > 2a^4: a=97 left the cell of its nearest cube and still hit. Closest even-m failures are small a, not near-cubes. Route A is false. No elementary lower bound stronger than D >= 1 produces a threshold.

`a = 97` survives: `True`.

