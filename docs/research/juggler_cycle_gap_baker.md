# Juggler cycle-gap Baker transfer

Status: **CYCLE_GAP_BAKER_CLOSED**

Map the unused Simons-de Weger half (Rhin linear forms on
|3^o - 2^L|) into Juggler cycle finance. Not a halt theorem.
Not the parked x^3 - y^2 campaign.

## Metadata

- classification: **CYCLE_GAP_BAKER_CLOSED**
- dense table: L <= `2000`
- record lengths: `[1, 3, 11, 19, 84, 569, 1054, 25781, 50508]`
- dominance (Rhin weaker than exact): `True`
- squeeze fires on leftover records: `False`
- exact gap kills L=19 at Lean floor 53: `False`
- Rhin floor that would exclude L=19: `1000000000000000000`

Rhin/SdW Lemma 12 is strictly weaker than the exact gap on every tested length; the squeeze never fires on leftover record lengths at floors 53, 10^6, or 10^9; even the exact gap leaves L=19 alive at the Lean floor 53, so no correct transcendence lower bound can kill every near-convergent at a realistic floor.

## Record lengths: exact gap versus Rhin/SdW

- L=`1` o=`1` exact theta=`0.333333` n_max=`3` rhin theta=`0.00218383` rhin n_max=`115`
- L=`3` o=`2` exact theta=`0.111111` n_max=`13` rhin theta=`9.862e-10` rhin n_max=`191413154`
- L=`11` o=`7` exact theta=`0.0635574` n_max=`52` rhin theta=`3.084e-17` rhin n_max=`11570465652905257`
- L=`19` o=`12` exact theta=`0.0134596` n_max=`297` rhin theta=`2.149e-20` rhin n_max=`1000000000000000000`
- L=`84` o=`53` exact theta=`0.00208595` n_max=`5599` rhin theta=`5.582e-29` rhin n_max=`1000000000000000000`
- L=`569` o=`359` exact theta=`0.00106533` n_max=`58398` rhin theta=`4.974e-40` rhin n_max=`1000000000000000000`
- L=`1054` o=`665` exact theta=`4.36532e-05` n_max=`1997197` rhin theta=`1.367e-43` rhin n_max=`1000000000000000000`
- L=`25781` o=`16266` exact theta=`2.54592e-05` n_max=`67410774` rhin theta=`4.671e-62` rhin n_max=`1000000000000000000`
- L=`50508` o=`31867` exact theta=`7.26491e-06` n_max=`420161535` rhin theta=`6.095e-66` rhin n_max=`1000000000000000000`

## Leftover exclusions by floor

- dense L<=`2000`, floor `53`: leftover `1931`, Rhin killed `[]`
- dense L<=`2000`, floor `1000000`: leftover `1`, Rhin killed `[]`
- dense L<=`2000`, floor `1000000000`: leftover `0`, Rhin killed `[]`
- records, floor `53`: leftover `6`, Rhin killed `[]`
- records, floor `1000000`: leftover `3`, Rhin killed `[]`
- records, floor `1000000000`: leftover `0`, Rhin killed `[]`

## Squeeze on leftover records

- L=`19` floor `53`: finance cap `0.108352`, Rhin `2.149e-20`, fires `False`
- L=`84` floor `53`: finance cap `0.479029`, Rhin `5.582e-29`, fires `False`
- L=`569` floor `53`: finance cap `3.24485`, Rhin `4.974e-40`, fires `False`
- L=`1054` floor `53`: finance cap `6.01068`, Rhin `1.367e-43`, fires `False`
- L=`25781` floor `53`: finance cap `147.022`, Rhin `4.671e-62`, fires `False`
- L=`50508` floor `53`: finance cap `288.034`, Rhin `6.095e-66`, fires `False`
- L=`19` floor `1000000`: finance cap `1.65032e-06`, Rhin `2.149e-20`, fires `False`
- L=`84` floor `1000000`: finance cap `7.29615e-06`, Rhin `5.582e-29`, fires `False`
- L=`569` floor `1000000`: finance cap `4.94227e-05`, Rhin `4.974e-40`, fires `False`
- L=`1054` floor `1000000`: finance cap `9.15493e-05`, Rhin `1.367e-43`, fires `False`
- L=`25781` floor `1000000`: finance cap `0.00223931`, Rhin `4.671e-62`, fires `False`
- L=`50508` floor `1000000`: finance cap `0.00438707`, Rhin `6.095e-66`, fires `False`
- L=`19` floor `1000000000`: finance cap `1.100e-09`, Rhin `2.149e-20`, fires `False`
- L=`84` floor `1000000000`: finance cap `4.864e-09`, Rhin `5.582e-29`, fires `False`
- L=`569` floor `1000000000`: finance cap `3.295e-08`, Rhin `4.974e-40`, fires `False`
- L=`1054` floor `1000000000`: finance cap `6.103e-08`, Rhin `1.367e-43`, fires `False`
- L=`25781` floor `1000000000`: finance cap `1.49287e-06`, Rhin `4.671e-62`, fires `False`
- L=`50508` floor `1000000000`: finance cap `2.92471e-06`, Rhin `6.095e-66`, fires `False`

## Length 19

- exact gap `3^12 - 2^19 = 7153`
- exact n_max `297` (Lean floor is 53)
- Rhin n_max `1000000000000000000`

## Anti-overclaim

- halt_theorem: `False`
- no_cycle_all_lengths: `False`
- x3_y2_campaign: `False`
- baker_solver: `False`
- lean_rhin_imported: `False`
- new_lean_file: `False`

## Decision

**CYCLE_GAP_BAKER_CLOSED**

Rhin/SdW Lemma 12 is strictly weaker than the exact gap on every tested length; the squeeze never fires on leftover record lengths at floors 53, 10^6, or 10^9; even the exact gap leaves L=19 alive at the Lean floor 53, so no correct transcendence lower bound can kill every near-convergent at a realistic floor.

