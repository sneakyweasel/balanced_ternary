# Juggler verified-descent-floor sensitivity

Status: **COMPUTATIONALLY VERIFIED** for the sensitivity table (implemented finance functions). The period bound is a Theorem 4.6 instance, not a new inequality and not a halt theorem.

## Metadata

- architecture: `parity_6/5 Theorem 4.6`
- baseline prefix: `25780`
- published floor: `1000000`
- L table: `1..200000`
- bit cap: `512000000`
- classification: `DESCENT_FLOOR_PARK`

verified N0=26254995 bought L*=50507; next useful floor 162848325 is 6.2× larger, so the marginal theorem gain is a later convergent, not more of this run

## Spotlight n_max (implemented, padded)

- L=`1054` parity 6/5=`788014` parity 1=`665021` runpack 6/5=`574721` crude 6/5=`1997197`
- L=`25780` parity 6/5=`2890` parity 1=`2460` runpack 6/5=`2185` crude 6/5=`6989`
- L=`25781` parity 6/5=`26254995` parity 1=`22102111` runpack 6/5=`19010076` crude 6/5=`67410774`
- L=`50508` parity 6/5=`162848325` parity 1=`136961378` runpack 6/5=`117641110` crude 6/5=`420161535`
- L=`76289` parity 6/5=`57774895` parity 1=`48615552` runpack 6/5=`41787350` crude 6/5=`148669538`
- L=`99962` parity 6/5=`7485` parity 1=`6357` runpack 6/5=`5601` crude 6/5=`18330`

## Sensitivity table (parity 6/5 is the theorem layer)

| N0 | L_max parity 6/5 | gain | survivors | L_max runpack | L_max parity 1 | est. time |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1000000 | 25780 | 0 | 576 | 25780 | 25780 | 0:45 |
| 10000000 | 25780 | 0 | 48 | 25780 | 25780 | 7:30 |
| 26254995 | 50507 | 24727 | 19 | 50507 | 50507 | 19:42 |
| 68000000 | 50507 | 24727 | 6 | 50507 | 50507 | 51:01 |
| 100000000 | 50507 | 24727 | 4 | 50507 | 50507 | 1:15:02 |
| 1000000000 | 176250 | 150470 | 1 | 200000 | 200000 | 12:30:22 |

## Recomputed period bound

- floor: `26254995`
- statement: No nontrivial Juggler cycle has length at most 50507
- first survivor: `50508`
- parity leftovers through L=200000: `19`

## Verification certificate

- N0: `26254995`
- verified: `True`
- odds walked: `13127497`
- total first-passage steps: `78553787`
- max stopping time: `325` at `15909091`
- max bits: `298912128` at `7110201`
- bit cap: `512000000`
- git: `8b82f054b7eaf5b02bd7d7f4811700a901056300`
- sha256 chunks: `cbcbb540dd860b775d2a3b4351f7cf779609104d3aaf30c342aed6b87f36c9dc`

## Bottleneck

- kind: `computation`
- 25781 is dead; next record leftover L=50508 needs N0>=162848325

## Recommendation

STOP COMPUTING — IMPROVE THE MATHEMATICS

