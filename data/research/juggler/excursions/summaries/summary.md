# Juggler first-return-below excursions

Status: **EXCURSION_ENVELOPE_GREEN**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The unit is a complete first
return strictly below the starting value. Full-word Δ >
formal_gap on a completed return is T<n rewritten.

## Branch budget

```text
Mathematical target     Can first-return-below words be certified by envelope/defect?
Novelty hypothesis      the complete excursion is the right FiniteProgress unit
Falsifier               COMPUTED_ONLY grazers with no structure, or T<n rewritten
Existing machinery      power_bound_*, first-defect, cmp_pow, FiniteProgress
Maximum Phase-0 scope   n=2..2000 + HARD_STARTS; persist; classify; no Lean
```

## Metadata

- search_id: `juggler-excursions-phase0-n2-2000`
- algorithm_version: `excursion-v1`
- window: `n=2..2000`
- horizon: `10000` (not L)
- bit_cap: `4096`
- engine control layer modified: `False`
- classification: **EXCURSION_ENVELOPE_GREEN**
- secondary: `[]`
- sorry-free: `True`

every first-return-below word in the window is formally contracting (2^k > 3^o); first-defect and peak-suffix never certify a return that the exponent gap misses.

## Census

- rows: `1999`
- returned: `1999`
- unfinished: `0`
- odd-odd returned: `505`
- start classes: `{'EVEN_AUTO': 1000, 'ODD_ODD_START': 505, 'OE_AUTO': 494}`
- certificate tags: `{'EXPONENT': 1999, 'FIRST_DEFECT': 1495, 'PEAK_SUFFIX': 1994}`
- certificate combos: `{'EXPONENT+FIRST_DEFECT+PEAK_SUFFIX': 1495, 'EXPONENT+PEAK_SUFFIX': 499, 'EXPONENT': 5}`
- certified fraction: `1.0`
- COMPUTED_ONLY: `0`
- COMPUTED_ONLY odd-odd: `0`
- COMPUTED_ONLY shapes: `[]`
- max τ_<: `70`
- max peak bits: `900`

## Lemmas

- A odd starts not an odd tower: `True`
- A universal (false if even E appears): `False`
- A universal counterexample sample: `[2, 4, 6, 8, 10]`
- B no all-odd return word: `True`
- B exact odd ascent does not return: `True`
- D no-first-defect count: `482`
- D shapes: `[[2, 2, 2, 0], [2, 2, 3, 1], [3, 3, 2, 0], [3, 3, 4, 1], [3, 3, 5, 2], [3, 3, 7, 3], [4, 4, 3, 0], [4, 4, 4, 1], [4, 4, 6, 2], [4, 4, 8, 3], [4, 4, 9, 4], [4, 4, 11, 5], [5, 4, 2, 0], [5, 4, 3, 1], [5, 5, 3, 0], [5, 5, 5, 1], [5, 5, 7, 2], [5, 5, 8, 3], [5, 5, 10, 4], [5, 5, 11, 5], [5, 5, 16, 8], [6, 5, 2, 0], [6, 5, 4, 1], [6, 5, 6, 2], [6, 5, 7, 3], [6, 6, 4, 0], [6, 6, 6, 1], [6, 6, 7, 2], [6, 6, 9, 3], [6, 6, 12, 5], [6, 6, 18, 9], [7, 6, 3, 0], [7, 6, 5, 1], [7, 6, 6, 2], [7, 6, 9, 4], [7, 6, 11, 5], [7, 6, 19, 10], [7, 7, 5, 0], [7, 7, 8, 2], [7, 7, 11, 4], [8, 6, 4, 1], [8, 7, 4, 0], [8, 7, 5, 1], [8, 7, 7, 2], [8, 7, 8, 3], [8, 7, 10, 4], [8, 7, 12, 5], [8, 7, 16, 8], [8, 8, 5, 0], [8, 8, 8, 2], [8, 8, 16, 7], [9, 7, 3, 0], [9, 7, 4, 1], [9, 7, 6, 2], [9, 7, 7, 3], [9, 7, 14, 7], [9, 8, 4, 0], [9, 8, 9, 3], [9, 8, 12, 5], [9, 8, 15, 7], [9, 8, 17, 8], [9, 9, 12, 4], [10, 8, 3, 0], [10, 8, 5, 1], [10, 8, 6, 2], [10, 8, 10, 4], [10, 9, 8, 2], [10, 9, 22, 11], [10, 10, 14, 5], [11, 8, 4, 1], [11, 9, 4, 0], [11, 9, 5, 1], [11, 9, 18, 9], [11, 10, 16, 7], [11, 10, 40, 22], [11, 11, 12, 3], [12, 9, 3, 0], [12, 9, 4, 1], [12, 9, 6, 2], [12, 10, 9, 3], [12, 10, 11, 4], [12, 10, 17, 8], [12, 11, 9, 2], [12, 11, 12, 4], [12, 11, 15, 6], [13, 10, 3, 0], [13, 10, 5, 1], [13, 10, 10, 4], [13, 11, 5, 0], [13, 11, 11, 4], [13, 12, 11, 3], [14, 10, 2, 0], [14, 11, 6, 1], [14, 11, 10, 4], [14, 12, 9, 2], [14, 13, 13, 4], [15, 13, 9, 2], [16, 12, 7, 2], [16, 13, 10, 3], [16, 14, 24, 11], [17, 13, 4, 0], [17, 13, 10, 4], [17, 14, 9, 2], [17, 14, 14, 5], [19, 15, 13, 5], [19, 15, 16, 7], [24, 19, 19, 8], [25, 18, 12, 5], [25, 19, 10, 3], [28, 21, 22, 10], [31, 22, 19, 9], [38, 27, 8, 2], [47, 34, 23, 10], [49, 35, 13, 4]]`
- prefix envelope false: `[]`
- tautological Δ used as certificate: `False`

## Hard starts

- n=`9` τ=`5` class=`ODD_ODD_START` k=`5` o=`3` G=`5` peak=`140` return=`6` deficit=`3` split=`(2,2,3,1)` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOEOE`
- n=`37` τ=`15` class=`ODD_ODD_START` k=`15` o=`9` G=`13085` peak=`24906114455136` return=`8` deficit=`29` split=`(8,7,7,2)` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOOOEOOOEEOOEEE`
- n=`49` τ=`5` class=`ODD_ODD_START` k=`5` o=`3` G=`5` peak=`6352` return=`26` deficit=`23` split=`(2,2,3,1)` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOEOE`
- n=`69` τ=`7` class=`ODD_ODD_START` k=`7` o=`4` G=`47` peak=`44992` return=`14` deficit=`55` split=`(5,4,2,0)` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOEOOEE`
- n=`77` τ=`10` class=`ODD_ODD_START` k=`10` o=`6` G=`295` peak=`2322378` return=`21` deficit=`56` split=`(3,3,7,3)` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOOEOEOOEE`
- n=`173` τ=`26` class=`ODD_ODD_START` k=`26` o=`16` G=`24062143` peak=`4450608860210678234719664930918817118564659064289879586228390154864378511410864886` return=`27` deficit=`146` split=`(17,14,9,2)` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOEOOOOOOOOEOOEOOEEOEEOEEE`

## Grazers (smallest n − C(n) among odd k>1)

- n=`3` deficit=`1` return=`2` k=`5` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OOOEE`
- n=`5` deficit=`3` return=`2` k=`4` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OOEE`
- n=`7` deficit=`3` return=`4` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`9` deficit=`3` return=`6` k=`5` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOEOE`
- n=`11` deficit=`5` return=`6` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`13` deficit=`7` return=`6` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`15` deficit=`8` return=`7` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`17` deficit=`9` return=`8` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`19` deficit=`10` return=`9` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`25` deficit=`10` return=`15` k=`5` certs=`['EXPONENT', 'PEAK_SUFFIX']` word=`OOOEE`
- n=`21` deficit=`12` return=`9` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`
- n=`23` deficit=`13` return=`10` k=`2` certs=`['EXPONENT', 'FIRST_DEFECT', 'PEAK_SUFFIX']` word=`OE`

## Tallest odd peaks

- n=`193` peak=`6743569603489758391265376070807357156339920158784377929096419715849060516985205368792190354996630779167466266586213526771780967700267133711091446786931423291036091166608223302792047793105565012490585915410391500762927066039966992101729450252321626382793545523711387059090` overshoot=`6743569603489758391265376070807357156339920158784377929096419715849060516985205368792190354996630779167466266586213526771780967700267133711091446786931423291036091166608223302792047793105565012490585915410391500762927066039966992101729450252321626382793545523711387058897` k=`70` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`557` peak=`1574129748074641238266477947016366564737788647737964712725226015704424966204805187535229840916967987155824008376401359208726835599504498723543801156199562476574693946628795032862408336683968515032287018752176270949381935119781771704619038962043542680073518307807995396` overshoot=`1574129748074641238266477947016366564737788647737964712725226015704424966204805187535229840916967987155824008376401359208726835599504498723543801156199562476574693946628795032862408336683968515032287018752176270949381935119781771704619038962043542680073518307807994839` k=`27` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`761` peak=`11986307718463031741056827050977981267870246529113307039126033359119925741719205025763602922516019092075566521972510765939208897103291873953039957492676896621570138635311245731202318151807665682479840140824238104215892354513024844489482216531801853394084822` overshoot=`11986307718463031741056827050977981267870246529113307039126033359119925741719205025763602922516019092075566521972510765939208897103291873953039957492676896621570138635311245731202318151807665682479840140824238104215892354513024844489482216531801853394084061` k=`62` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`663` peak=`11307766533079965984258844223359010907828494119652873324896780021733166159542096097177379727797856873718731056545100741084109625941065866738774869304120991337004025480315579808620479972369688625760748850793673889668580129932035025942104899396452` overshoot=`11307766533079965984258844223359010907828494119652873324896780021733166159542096097177379727797856873718731056545100741084109625941065866738774869304120991337004025480315579808620479972369688625760748850793673889668580129932035025942104899395789` k=`23` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`807` peak=`141340036301289163586349223234922872960283359416582422850138301747736704386604635485856183499769834567609974510494570545990194717454548429453833402500387444350830285090310850018976378688966165861920845173813929288` overshoot=`141340036301289163586349223234922872960283359416582422850138301747736704386604635485856183499769834567609974510494570545990194717454548429453833402500387444350830285090310850018976378688966165861920845173813928481` k=`40` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`1629` peak=`23292139916051353110852765829175511900830611448756758316847629067097093323384798569377582664784085690018868943566837712710317191290688069501988519497205164373033794724826480570657023982083857132171967850954926` overshoot=`23292139916051353110852765829175511900830611448756758316847629067097093323384798569377582664784085690018868943566837712710317191290688069501988519497205164373033794724826480570657023982083857132171967850953297` k=`24` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`293` peak=`782960644528031182478778269971671893857290991978652977413980144809602271665761768285250254182147217823074414682446735642976716076853608380272794108384550040642846923889122` overshoot=`782960644528031182478778269971671893857290991978652977413980144809602271665761768285250254182147217823074414682446735642976716076853608380272794108384550040642846923888829` k=`43` certs=`['EXPONENT', 'PEAK_SUFFIX']`
- n=`357` peak=`1580989446943204349269987976520466875945390265676357712616164899103502088741825409579379605266580890680620379312986028251134159031439455696176206088` overshoot=`1580989446943204349269987976520466875945390265676357712616164899103502088741825409579379605266580890680620379312986028251134159031439455696176205731` k=`24` certs=`['EXPONENT', 'PEAK_SUFFIX']`

## Lean

- `power_bound_word`: `True`
- `power_bound_contracts`: `True`
- `power_bound_eq_iff_extremal`: `True`
- `power_bound_compensated_contracts`: `True`
- new Excursions file absent: `True`
- ResidualStep not extended: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- search_horizon_is_L: `False`
- full_delta_is_certificate: `False`
- finite_progress_for_all: `False`
- minimal_nonterm_rebuilt: `False`
- first_return_means_orbit_period: `False`

## Decision

**EXCURSION_ENVELOPE_GREEN**

every first-return-below word in the window is formally contracting (2^k > 3^o); first-defect and peak-suffix never certify a return that the exponent gap misses.

A search-horizon miss is not a bound L. Do not claim termination.

