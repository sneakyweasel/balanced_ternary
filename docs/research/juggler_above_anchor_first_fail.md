# Juggler first shared AboveAnchor failure

Status: **FIRST_ANCHOR_FAIL_CLOSED**

First named shared `AboveAnchor` kill on leftover odd-landing
corridors. The last even-below-square step is excluded.
Not a halt theorem.

## Branch budget

```text
Mathematical target     which leftover corridor first fails
                        a named shared AboveAnchor cell
Novelty hypothesis      a missed shared kill, or a new cell
Maximum Phase-0 scope   named starts; odd window < 201;
                        no Lean; no Sigma
```

## Metadata

- classification: **FIRST_ANCHOR_FAIL_CLOSED**
- pins ok: `True`
- leftover strong: `{'365': 'eighth_oee', '501': 'eighth_oee', '1517': 'cube_odd_even_below_square', '6187': None}`
- contrast strong: `{'69': 'eighth_oee', '89': None}`
- lab strong: `cube_even_even`
- window tautological: `[89, 111, 163]`
- window hist: `{'cube_odd_even_below_square': 8, 'eighth_oee': 26, 'isolated_scale_gap': 11, 'cube_even_even': 4, 'none': 3, 'two_even_below_fourth_not_cube': 4}`

non-tautological first kills are eighth_oee, cube_even_even, or cube_odd_even_below_square; 6187 and 89 fail only the last even-below-square step after a square-odd OE.

## Named starts

- `37`: word=`OOOOEOOOEEOOEEE` drop=`15` tag=`cube_even_even` i=`13` band=`cube` x=`5854` tags=`['cube_even_even']`
  - i=`13` cube E x=`5854` tags=`['cube_even_even']`
  - i=`14` square E x=`76` tags=`['k2_envelope_even', 'even_below_square']`
- `69`: word=`OOEOOEE` drop=`7` tag=`eighth_oee` i=`4` band=`square` x=`1265` tags=`['eighth_oee']`
  - i=`4` square O x=`1265` tags=`['eighth_oee']`
  - i=`5` cube E x=`44992` tags=`['cube_even_even']`
  - i=`6` square E x=`212` tags=`['k2_envelope_even', 'even_below_square']`
- `89`: word=`OOEOOEOE` drop=`8` tautological_only
  - i=`6` square O x=`291` tags=`['square_odd_even_drop']`
  - i=`7` square E x=`4964` tags=`['k2_envelope_even', 'even_below_square']`
- `365`: word=`OOEOOEOOEOOEOEE` drop=`15` tag=`eighth_oee` i=`12` band=`square` x=`12707` tags=`['eighth_oee']`
  - i=`12` square O x=`12707` tags=`['eighth_oee']`
  - i=`13` cube E x=`1432400` tags=`['cube_even_even']`
  - i=`14` square E x=`1196` tags=`['k2_envelope_even', 'even_below_square']`
- `501`: word=`OOEOOOEOOEEOOEOOEOOEOEE` drop=`23` tag=`eighth_oee` i=`20` band=`square` x=`12707` tags=`['eighth_oee']`
  - i=`20` square O x=`12707` tags=`['eighth_oee']`
  - i=`21` cube E x=`1432400` tags=`['cube_even_even']`
  - i=`22` square E x=`1196` tags=`['k2_envelope_even', 'even_below_square']`
- `1517`: word=`OOEOOEOOEOEOOOEE` drop=`16` tag=`cube_odd_even_below_square` i=`13` band=`cube` x=`43916043` tags=`['cube_odd_even_below_square', 'eighth_oee']`
  - i=`13` cube O x=`43916043` tags=`['cube_odd_even_below_square', 'eighth_oee']`
  - i=`14` fourth E x=`291028018566` tags=`['two_even_below_fourth_not_cube']`
  - i=`15` square E x=`539470` tags=`['k2_envelope_even', 'even_below_square']`
- `6187`: word=`OOEOOOEOOEEOE` drop=`13` tautological_only
  - i=`11` square O x=`11189` tags=`['square_odd_even_drop']`
  - i=`12` square E x=`1183550` tags=`['k2_envelope_even', 'even_below_square']`

## Existing Lean (unchanged)

- `AboveAnchor`: `True`
- `aboveAnchor_not_envelope_drop`: `True`
- `aboveAnchor_not_odd_even`: `True`
- `aboveAnchor_isolated_two`: `True`
- `even_below_square_drop`: `True`
- `two_even_below_fourth`: `True`
- `finiteProgress_of_cube_even_even`: `True`
- `finiteProgress_of_cube_odd_even_below_square`: `True`
- `finiteProgress_of_odd_even_eighth`: `True`
- `finiteProgress_of_even_power_bound_square`: `True`
- `finiteProgress_of_ooe_oe`: `True`
- `odd_even_eighth_lt_sq`: `True`
- `CubeOddLanding`: `True`
- new Lean file: `False`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- new_shared_obstruction: `False`
- tautological_square_is_new_cell: `False`
- first_fail_lean: `False`
- eighth_reopen: `False`
- sigma_automaton: `False`

## Decision

**FIRST_ANCHOR_FAIL_CLOSED**

non-tautological first kills are eighth_oee, cube_even_even, or cube_odd_even_below_square; 6187 and 89 fail only the last even-below-square step after a square-odd OE.

