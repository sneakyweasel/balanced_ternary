# Juggler cycle near-tight rigidity

Status: **CYCLE_NEAR_TIGHT_CLOSED**

Cycle return + tiny finance gap versus open-orbit q -> 0.
Not a halt theorem. Not a no-cycle-of-any-length theorem.
No new Lean.

## Metadata

- classification: **CYCLE_NEAR_TIGHT_CLOSED**
- record lengths: `[1, 3, 11, 19, 84, 569, 1054]`
- OOE census n_max: `2000` checked `254`
- OOE returns: `0`
- slogan fails: `True`
- leftover killed by near-tight: `False`

cycle 1+q = n^{3^o-2^L} is the opposite of open-orbit q->0; leftover Hamming to monochrome grows (7,31,210,389); realized OOE expands and never returns; the 329 successor is mixed with 0<q<10^{-30} against cycle-required q=y-1. R=1 on a return is image_eq_start_defectRatio, already Lean. NearTightScale does not cover leftover convergents.

## Record convergents

- L=`1` o=`1` evens=`0` G=`1` theta=`0.333333` Hamming=`0` n_max=`3` ln(1+q) at 53=`3.97029` envelope growth at 53=`6.28011`
- L=`3` o=`2` evens=`1` G=`1` theta=`0.111111` Hamming=`1` n_max=`13` ln(1+q) at 53=`3.97029` envelope growth at 53=`0.64261`
- L=`11` o=`7` evens=`4` G=`139` theta=`0.0635574` Hamming=`4` n_max=`52` ln(1+q) at 53=`551.871` envelope growth at 53=`0.309268`
- L=`19` o=`12` evens=`7` G=`7153` theta=`0.0134596` Hamming=`7` n_max=`297` ln(1+q) at 53=`28399.5` envelope growth at 53=`0.0556617`
- L=`84` o=`53` evens=`31` G=`40432553845953101497907` theta=`0.00208595` Hamming=`31` n_max=`5599` ln(1+q) at 53=`1.605e+23` envelope growth at 53=`0.00833369`
- L=`569` o=`359` evens=`210` G=`None` theta=`0.00106533` Hamming=`210` n_max=`58398` ln(1+q) at 53=`8.182e+168` envelope growth at 53=`0.00424314`
- L=`1054` o=`665` evens=`389` G=`None` theta=`4.365e-05` Hamming=`389` n_max=`1997197` ln(1+q) at 53=`inf` envelope growth at 53=`0.000173338`

## Open-orbit OOE (first leftover length L=3, G=1)

- checked `254` odd-odd realized OOE through `2000`
- expands `254` returns `0`
- all open q < cycle q (`n-1`): `True`
- all R < 1: `True` max R `0.5025400424808198`
- max open q `0.8073451736296384`

## 329 successor (mixed near-tight OOE)

- y=`180370579261640036336071806107777` image=`1941719144218166368455510841464890645`
- expands `True` returns `False`
- open q `1.3586274926649128e-36` cycle q `y-1`
- 0 < open q < 10^-30: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- halt_theorem: `False`
- no_cycle_all_lengths: `False`
- floor_raise: `False`
- new_lean: `False`
- almost_monochrome_forced: `False`
- leftover_killed: `False`
- approx_rigidity_reopened: `False`

## Decision

**CYCLE_NEAR_TIGHT_CLOSED**

cycle 1+q = n^{3^o-2^L} is the opposite of open-orbit q->0; leftover Hamming to monochrome grows (7,31,210,389); realized OOE expands and never returns; the 329 successor is mixed with 0<q<10^{-30} against cycle-required q=y-1. R=1 on a return is image_eq_start_defectRatio, already Lean. NearTightScale does not cover leftover convergents.

