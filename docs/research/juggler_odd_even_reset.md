# Juggler odd-to-even reset interface

Status: **ODD_EVEN_RESET_CLOSED**

Reset quadruple (x, x_r, e, s) versus generic OE floor identities.
Not a halt theorem. Not a source-descent reopen.

## Branch budget

```text
Mathematical target     non-generic relation at odd-to-even reset
Novelty hypothesis      (delta, eps) couples beyond EnvelopeState
Maximum Phase-0 scope   named resets; generic OE; no Lean
```

## Metadata

- classification: **ODD_EVEN_RESET_CLOSED**
- resets: `29`
- psi ok: `True`
- s^4 < x_r^3: `True`
- s < x fails on long runs: `True`
- two-episode descent false: `True`
- leftover first runs have r>=2: `True`
- leftover first s>x: `True`
- s^4 <= x^3 on all named resets: `False`
- even-s second even always FiniteProgress: `False`
- 37 sources: `[37, 9317, 2233]`
- 37 first reset: x=`37` r=`4` x_r=`196069` e=`86818724` s=`9317`

x_r^3 - s^4 = 2 e_eps s^2 + e_eps^2 + delta is generic OE; s^4 < x_r^3 is oe_block_scale plus odd/even parity; s < x_r is floorPower_odd_even_two_step_lt; s < x fails for r>=2; two-episode descent is already false.

## Named orbits

- `37`: count=`3`
  - x=`37` r=`4` x_r=`196069` e=`86818724` s=`9317` s_odd=`True` s_lt_x=`False`
  - x=`9317` r=`3` x_r=`852846071` e=`24906114455136` s=`4990602` s_odd=`False` s_lt_x=`False`
  - x=`2233` r=`2` x_r=`105519` e=`34276462` s=`5854` s_odd=`False` s_lt_x=`False`
- `69`: count=`2`
  - x=`69` r=`2` x_r=`573` e=`13716` s=`117` s_odd=`True` s_lt_x=`False`
  - x=`117` r=`2` x_r=`1265` e=`44992` s=`212` s_odd=`False` s_lt_x=`False`
- `89`: count=`3`
  - x=`89` r=`2` x_r=`839` e=`24302` s=`155` s_odd=`True` s_lt_x=`False`
  - x=`155` r=`2` x_r=`1929` e=`84722` s=`291` s_odd=`True` s_lt_x=`False`
  - x=`291` r=`1` x_r=`291` e=`4964` s=`70` s_odd=`False` s_lt_x=`True`
- `365`: count=`5`
  - x=`365` r=`2` x_r=`6973` e=`582276` s=`763` s_odd=`True` s_lt_x=`False`
  - x=`763` r=`2` x_r=`21075` e=`3059506` s=`1749` s_odd=`True` s_lt_x=`False`
  - x=`1749` r=`2` x_r=`73145` e=`19782308` s=`4447` s_odd=`True` s_lt_x=`False`
  - x=`4447` r=`2` x_r=`296551` e=`161491284` s=`12707` s_odd=`True` s_lt_x=`False`
  - x=`12707` r=`1` x_r=`12707` e=`1432400` s=`1196` s_odd=`False` s_lt_x=`True`
- `501`: count=`7`
  - x=`501` r=`2` x_r=`11213` e=`1187360` s=`1089` s_odd=`True` s_lt_x=`False`
  - x=`1089` r=`3` x_r=`6812597` e=`17781526790` s=`133347` s_odd=`True` s_lt_x=`False`
  - x=`133347` r=`2` x_r=`48693935` e=`339791341082` s=`582916` s_odd=`False` s_lt_x=`False`
  - x=`763` r=`2` x_r=`21075` e=`3059506` s=`1749` s_odd=`True` s_lt_x=`False`
  - x=`1749` r=`2` x_r=`73145` e=`19782308` s=`4447` s_odd=`True` s_lt_x=`False`
  - x=`4447` r=`2` x_r=`296551` e=`161491284` s=`12707` s_odd=`True` s_lt_x=`False`
  - x=`12707` r=`1` x_r=`12707` e=`1432400` s=`1196` s_odd=`False` s_lt_x=`True`
- `1517`: count=`5`
  - x=`1517` r=`2` x_r=`59085` e=`14362030` s=`3789` s_odd=`True` s_lt_x=`False`
  - x=`3789` r=`2` x_r=`233231` e=`112636568` s=`10613` s_odd=`True` s_lt_x=`False`
  - x=`10613` r=`2` x_r=`1093345` e=`1143235850` s=`33811` s_odd=`True` s_lt_x=`False`
  - x=`33811` r=`1` x_r=`33811` e=`6217088` s=`2493` s_odd=`True` s_lt_x=`True`
  - x=`2493` r=`3` x_r=`43916043` e=`291028018566` s=`539470` s_odd=`False` s_lt_x=`False`
- `6187`: count=`4`
  - x=`6187` r=`2` x_r=`486653` e=`339491658` s=`18425` s_odd=`True` s_lt_x=`False`
  - x=`18425` r=`3` x_r=`3955183437` e=`248742471750750` s=`15771571` s_odd=`True` s_lt_x=`False`
  - x=`15771571` r=`2` x_r=`62634329559` e=`15675400641582836` s=`125201440` s_odd=`False` s_lt_x=`False`
  - x=`11189` r=`1` x_r=`11189` e=`1183550` s=`1087` s_odd=`True` s_lt_x=`True`

## Long / L resets

- `37`: x=`37` r=`4` x_r=`196069` e=`86818724` s=`9317` s_odd=`True` s_lt_x=`False`
- `241`: x=`241` r=`5` x_r=`1145068740593` e=`1225313838630510914` s=`1106938949` s_odd=`True` s_lt_x=`False`
- `329`: x=`329` r=`8` x_r=`10191096955185724142110473921312275306979975` e=`32533545863179570755492129120411963721630316057459884067704058780` s=`180370579261640036336071806107777` s_odd=`True` s_lt_x=`False`
- `33391`: x=`67709` r=`5` x_r=`2851985988922126936589955` e=`4816383738386359112539037957095874424` s=`2194626104462069664` s_odd=`False` s_lt_x=`False`

## Existing Lean (unchanged)

- `oe_block_scale`: `True`
- `oe_block_contracts`: `True`
- `floorPower_odd_even_two_step_lt`: `True`
- `floorPower_odd_sq_le_cube`: `True`
- `floorPower_even_sq_le`: `True`
- `EnvelopeState`: `True`
- `cube_lift_even_reset`: `True`
- `even_below_anchor_pow`: `True`
- `ReturnBelow`: `True`
- new Lean file: `False`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- independent_reset_identity: `False`
- source_reset_bound: `False`
- two_episode_descent: `False`
- odd_even_reset_lean: `False`
- source_descent_reopen: `False`
- z5_reopen: `False`

## Decision

**ODD_EVEN_RESET_CLOSED**

x_r^3 - s^4 = 2 e_eps s^2 + e_eps^2 + delta is generic OE; s^4 < x_r^3 is oe_block_scale plus odd/even parity; s < x_r is floorPower_odd_even_two_step_lt; s < x fails for r>=2; two-episode descent is already false.

