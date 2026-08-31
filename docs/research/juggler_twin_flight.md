# Juggler twin-flight of nearby same-parity starts

Status: **TWIN_FLIGHT_CLOSED**

Same-parity pair object $(n,n+2)$: synchronized relative gap,
merge time, common tail / phase shift, and high-water isolation.
First-step closeness is the setup, not a shadow. The sink
`{1, 2}` is excluded from common-tail detection.
Not a halt theorem. A pair census is not a theorem.
Absence is NOT_OBSERVED_WITHIN_BOUND.

## Branch budget

```text
Mathematical target     nearby same-parity merge / shadow / isolate
Novelty hypothesis      hard flights are local families
Maximum Phase-0 scope   HARD_LABS ±10; n<=2000 control; no Lean
```

## Metadata

- classification: **TWIN_FLIGHT_CLOSED**
- labs: `[37, 69, 89, 365, 501, 1517, 6187, 329, 33391, 193, 425, 557, 761, 1181, 1721, 1773, 2183, 3889]`
- control n_max: `2000` pairs: `999`
- hard adjacent pairs: `90`
- hard contact/shadow/separate: `0.5222` / `0.0000` / `0.4556`
- control contact/shadow/separate: `0.5495` / `0.0000` / `0.4505`
- contact elevated: `False` shadow elevated: `False`
- isolated labs: `[37]` count: `1`
- 365/501 at 763: `True`
- first-step 37 delta_1: `0.0741` approx 3/n: `0.0811`

hard-window adjacent pairs match the control (generic coalescence: contact 0.522 vs 0.550; shadow 0.000 vs 0.000).

## Hard-window adjacent pairs

- counts: `{'exact_merge': 26, 'shifted_flight': 21, 'long_shadow': 0, 'separate': 41, 'capped_shadow': 0, 'capped_separate': 2}`
- even-reset merges: `24`

- lab `37`: adjacent `{'exact_merge': 3, 'shifted_flight': 2, 'long_shadow': 0, 'separate': 5, 'capped_shadow': 0, 'capped_separate': 0}` R-=`1.195690321492879e-10` R+=`9.356979404386482e-09` isolated=`True` neighbors=`separate`/`separate`
  - `35`/`37`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
  - `37`/`39`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
- lab `69`: adjacent `{'exact_merge': 3, 'shifted_flight': 3, 'long_shadow': 0, 'separate': 4, 'capped_shadow': 0, 'capped_separate': 0}` R-=`0.012179943100995733` R+=`0.013291251778093883` isolated=`False` neighbors=`shifted_flight`/`separate`
  - `67`/`69`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`0.9999` common=state=`3` i=`5` j=`8` r=`3`
  - `69`/`71`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
- lab `89`: adjacent `{'exact_merge': 2, 'shifted_flight': 2, 'long_shadow': 0, 'separate': 6, 'capped_shadow': 0, 'capped_separate': 0}` R-=`41.42673685701471` R+=`0.010245272774485966` isolated=`False` neighbors=`separate`/`separate`
  - `87`/`89`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
  - `89`/`91`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
- lab `365`: adjacent `{'exact_merge': 2, 'shifted_flight': 5, 'long_shadow': 0, 'separate': 3, 'capped_shadow': 0, 'capped_separate': 0}` R-=`4.282584068128407e-05` R+=`4.353176113207447e-05` isolated=`False` neighbors=`shifted_flight`/`shifted_flight`
  - `363`/`365`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`6` j=`17` r=`11`
  - `365`/`367`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`17` j=`6` r=`-11`
- lab `501`: adjacent `{'exact_merge': 0, 'shifted_flight': 3, 'long_shadow': 0, 'separate': 7, 'capped_shadow': 0, 'capped_separate': 0}` R-=`0.00013682971982732181` R+=`3.526216990064059e-06` isolated=`False` neighbors=`shifted_flight`/`separate`
  - `499`/`501`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`14` j=`25` r=`11`
  - `501`/`503`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
- lab `1517`: adjacent `{'exact_merge': 4, 'shifted_flight': 1, 'long_shadow': 0, 'separate': 5, 'capped_shadow': 0, 'capped_separate': 0}` R-=`2.0261966628009426e-07` R+=`8.00768259868248e-07` isolated=`False` neighbors=`separate`/`shifted_flight`
  - `1515`/`1517`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
  - `1517`/`1519`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`27` i=`17` j=`9` r=`-8`
- lab `6187`: adjacent `{'exact_merge': 3, 'shifted_flight': 1, 'long_shadow': 0, 'separate': 4, 'capped_shadow': 0, 'capped_separate': 2}` R-=`3937885803426.588` R+=`2.1673362472073608e-08` isolated=`False` neighbors=`shifted_flight`/`separate`
  - `6185`/`6187`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`4` i=`12` j=`20` r=`8`
  - `6187`/`6189`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
- lab `329`: adjacent `{'exact_merge': 2, 'shifted_flight': 3, 'long_shadow': 0, 'separate': 5, 'capped_shadow': 0, 'capped_separate': 0}` R-=`1.021626510621912e-76` R+=`5.2181130109242306e-76` isolated=`False` neighbors=`separate`/`shifted_flight`
  - `327`/`329`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
  - `329`/`331`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`27` i=`23` j=`15` r=`-8`
- lab `33391`: adjacent `{'exact_merge': 7, 'shifted_flight': 1, 'long_shadow': 0, 'separate': 2, 'capped_shadow': 0, 'capped_separate': 0}` R-=`7.374696002388749e-189` R+=`9.05677246914381e-184` isolated=`False` neighbors=`separate`/`shifted_flight`
  - `33389`/`33391`: class=`separate` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=none
  - `33391`/`33393`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`43` j=`10` r=`-33`

## Record-extra adjacent counts

- `193`: adjacent `{'exact_merge': 2, 'shifted_flight': 0, 'long_shadow': 0, 'separate': 8, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`True` R-=`2.010329958333111e-266` R+=`2.1070739735001505e-266`
- `425`: adjacent `{'exact_merge': 5, 'shifted_flight': 2, 'long_shadow': 0, 'separate': 3, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`False` R-=`9.857331906268177e-68` R+=`1.1461372874654395e-53`
- `557`: adjacent `{'exact_merge': 2, 'shifted_flight': 4, 'long_shadow': 0, 'separate': 4, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`True` R-=`8.305541532387116e-264` R+=`8.39575010647301e-264`
- `761`: adjacent `{'exact_merge': 3, 'shifted_flight': 2, 'long_shadow': 0, 'separate': 5, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`True` R-=`1.7444905045939557e-252` R+=`1.3472979986259483e-248`
- `1181`: adjacent `{'exact_merge': 2, 'shifted_flight': 3, 'long_shadow': 0, 'separate': 5, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`True` R-=`4.4827992323103297e-39` R+=`4.6052925867340455e-30`
- `1721`: adjacent `{'exact_merge': 6, 'shifted_flight': 1, 'long_shadow': 0, 'separate': 3, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`True` R-=`1.8221020593089e-87` R+=`5.795460098918822e-122`
- `1773`: adjacent `{'exact_merge': 1, 'shifted_flight': 4, 'long_shadow': 0, 'separate': 5, 'capped_shadow': 0, 'capped_separate': 0}` isolated=`False` R-=`1.9694948981314336e-83` R+=`1.604796706464202e-89`
- `2183`: adjacent `{'exact_merge': 1, 'shifted_flight': 0, 'long_shadow': 0, 'separate': 7, 'capped_shadow': 0, 'capped_separate': 2}` isolated=`True` R-=`0.0` R+=`0.0`
- `3889`: adjacent `{'exact_merge': 0, 'shifted_flight': 6, 'long_shadow': 0, 'separate': 2, 'capped_shadow': 0, 'capped_separate': 2}` isolated=`True` R-=`0.0` R+=`0.0`

## Control

- counts: `{'exact_merge': 333, 'shifted_flight': 216, 'long_shadow': 0, 'separate': 450, 'capped_shadow': 0, 'capped_separate': 0}`
- even-reset merges: `306`
- capped pairs: `0`

## Cross-lab tails among HARD_LABS

- hits: `16` of `36`

- `37`/`89`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`8` i=`15` j=`9` r=`-6`
- `69`/`365`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`5` i=`9` j=`16` r=`7`
- `69`/`501`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`5` i=`9` j=`24` r=`15`
- `69`/`1517`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`10` j=`19` r=`9`
- `69`/`329`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`10` j=`25` r=`15`
- `69`/`33391`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`14` i=`7` j=`40` r=`33`
- `365`/`501`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`763` i=`3` j=`11` r=`8`
- `365`/`1517`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`17` j=`19` r=`2`
- `365`/`329`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`17` j=`25` r=`8`
- `365`/`33391`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`5` i=`16` j=`42` r=`26`
- `501`/`1517`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`25` j=`19` r=`-6`
- `501`/`329`: class=`exact_merge` tau_merge=`25` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`25` j=`25` r=`0`
- `501`/`33391`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`5` i=`24` j=`42` r=`18`
- `1517`/`329`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`27` i=`17` j=`23` r=`6`
- `1517`/`33391`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`19` j=`43` r=`24`
- `329`/`33391`: class=`shifted_flight` tau_merge=`None` even_reset=`False` max_delta=`1.0000` common=state=`11` i=`25` j=`43` r=`18`

## Existing Lean (unchanged)

- `floorPower`: `True`
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
- coalescence_is_not_termination: `False`
- pair_census_is_theorem: `False`
- high_merge_reopen: `False`
- ten_to_nine_census: `False`
- twin_flight_lean: `False`

## Decision

**TWIN_FLIGHT_CLOSED**

hard-window adjacent pairs match the control (generic coalescence: contact 0.522 vs 0.550; shadow 0.000 vs 0.000).

