# Juggler cumulative floor loss

Status: **CUMULATIVE_FLOOR_LOSS_CLOSED**

Exact floor remainders versus the existing global-defect spine.
Not a halt theorem. Not a new `FloorLoss` layer.

## Branch budget

```text
Mathematical target     does discarded floor loss accumulate
                        past the survival margin?
Novelty hypothesis      amplified Delta exceeds slack
                        independently of T<n
Maximum Phase-0 scope   named first runs; 9; 329/33391;
                        no Lean; no p-adic
```

## Metadata

- classification: **CUMULATIVE_FLOOR_LOSS_CLOSED**
- dictionary ok: `True`
- leftover first OOE: `True`
- proposed product false: `True`
- global identity: `True`
- mechanism A: `False`
- zero first defect: `True`
- window zero: `[9, 25, 49, 81, 121, 169]`

the proposed rho-product omits the cubic slack lift; Delta_r is globalDefect; R>1 is T<n; delta_0 vanishes on odd squares; leftovers are OOE; long runs survive.

## Named first odd runs

- `37`: odds=`4` word=`OOOO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`37` y=`225` delta=`28` eps=`28/451`
  - x=`225` y=`3375` delta=`0` eps=`0`
  - x=`3375` y=`196069` delta=`306614` eps=`27874/35649`
  - x=`196069` y=`86818724` delta=`74808333` eps=`74808333/173637449`
- `69`: odds=`2` word=`OO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`69` y=`573` delta=`180` eps=`180/1147`
  - x=`573` y=`13716` delta=`3861` eps=`3861/27433`
- `89`: odds=`2` word=`OO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`89` y=`839` delta=`1048` eps=`1048/1679`
  - x=`839` y=`24302` delta=`2515` eps=`503/9721`
- `365`: odds=`2` word=`OO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`365` y=`6973` delta=`4396` eps=`4396/13947`
  - x=`6973` y=`582276` delta=`949141` eps=`32729/40157`
- `501`: odds=`2` word=`OO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`501` y=`11213` delta=`20132` eps=`20132/22427`
  - x=`11213` y=`1187360` delta=`2070997` eps=`2070997/2374721`
- `1517`: odds=`2` word=`OO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`1517` y=`59085` delta=`18188` eps=`18188/118171`
  - x=`59085` y=`14362030` delta=`28718225` eps=`28718225/28724061`
- `6187`: odds=`2` word=`OO` image_ge_n=`True` measurable=`True` R_gt_1=`False`
  - x=`6187` y=`486653` delta=`838794` eps=`838794/973307`
  - x=`486653` y=`339491658` delta=`95178113` eps=`95178113/678983317`

## Amplification D2 vs d0+d1

- `37`: d0=`28` d1=`0` D2=`215401904452` naive=`28` amplified=`True`
- `69`: d0=`180` d1=`3861` D2=`59696627209893` naive=`4041` amplified=`True`
- `89`: d0=`1048` d1=`2515` D2=`1563158178947593` naive=`3563` amplified=`True`
- `365`: d0=`4396` d1=`949141` D2=`31825094526207867149` naive=`953537` amplified=`True`
- `501`: d0=`20132` d1=`2070997` D2=`960755116231624844501` naive=`2091129` amplified=`True`
- `1517`: d0=`18188` d1=`28718225` D2=`676840830837961629519997` naive=`28736413` amplified=`True`
- `6187`: d0=`838794` d1=`95178113` D2=`141163764185571974400565859131` naive=`96016907` amplified=`True`

## Long runs (local only)

- `37` source=`37` odds=`4` min_eps=`0.0` max_eps=`0.7819013156049258` survive=`True` measurable=`True`
- `241` source=`241` odds=`5` min_eps=`0.12940345811593285` max_eps=`0.8967344521840641` survive=`True` measurable=`True`
- `329` source=`329` odds=`8` min_eps=`0.024973450386664337` max_eps=`0.928115571761933` survive=`True` measurable=`False`
- `33391` source=`67709` odds=`5` min_eps=`0.0820000378923647` max_eps=`0.708466137035831` survive=`True` measurable=`False`

## Existing Lean (unchanged)

- `localDefectOdd`: `True`
- `localDefectEven`: `True`
- `globalDefect`: `True`
- `global_defect_identity`: `True`
- `globalDefect_eq_powerDeficit`: `True`
- `onePlusSlack_concat`: `True`
- `defectRatio_le_one_iff_image_ge`: `True`
- `amplifyDefect`: `True`
- `sequentialDefect`: `True`
- `oddMordellStep`: `True`
- `EnvelopeState`: `True`
- `AboveAnchor`: `True`
- new Lean file: `False`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- new_cumulative_obstruction: `False`
- floor_loss_lean: `False`
- padic: `False`
- analytic_nt: `False`

## Decision

**CUMULATIVE_FLOOR_LOSS_CLOSED**

the proposed rho-product omits the cubic slack lift; Delta_r is globalDefect; R>1 is T<n; delta_0 vanishes on odd squares; leftovers are OOE; long runs survive.

