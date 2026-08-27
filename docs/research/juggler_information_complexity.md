# Juggler information complexity

Status: **INFO_COMPLEXITY_COUNTEREXAMPLE**

Standalone Phase-0 measurement of finite dynamical information
complexity. Not a Research Engine experiment, not a halt theorem,
and not an independence claim. `~_H` is experimental future-equality,
not Myhill–Nerode equivalence.

## Branch budget

```text
Mathematical target     Do D_H and k*(H) grow with H<=6 on fixed Y?
Novelty hypothesis      longer word futures need more arithmetic bits
Falsifier               Q_H is 2^H counting; k* plateaus at H=2
Existing machinery      floor_power, itinerary, word_of, collect_landings
Maximum Phase-0 scope   H<=6; samples A/B/C/D; no GPU; no Lean pilot
```

## 1. Motivation

The tested compression hierarchy (word statistics, PE grammar,
realization-set and landing-image geometry, low-dimensional
projections of y, summed defects, noncontracting thresholds) failed
because the exact integer retained information those summaries
dropped. This phase asks whether that failure has a quantitative
horizon law. It does not reopen those branches.

## 2. Definitions

- `F_H(x)` = `O/E itinerary of the next H steps (parities of x, T(x), ..., T^{H-1}(x))`
- x ~_H y iff F_H(x)=F_H(y); experimental, not Myhill-Nerode
- `Q_H` = number of observed `F_H` classes on a fixed sample Y
- `I_H` = `ceil(log2 Q_H)` (class-index bits; not Kolmogorov complexity)
- `C_H` = `Q_H / |Y|` (finer futures give C_H closer to 1)
- `k*_2(H;Y)` = least k such that `x mod 2^k` separates the observed
  `F_H` classes, or `INSUFFICIENT_PRECISION_WITHIN_K_MAX`
- `D_H` is reported separately as `I_H`, `k*_2`, `k*_3`, BT-MSD length,
  and greedy query count — not as a single invented energy

## 3. Fixed-sample results

Q_H <= 2^H and I_H <= H on every fixed sample (word-alphabet counting). k*_2 jumps at H=2 and then plateaus; the H=2 value grows with |Y| on nested consecutive intervals. Apparent horizon complexity is the itinerary bound plus a sample-diameter 2-adic pair.

### A_residual_80

- |Y| kept: `30` meta `{'source': 'collect_landings(n_max=80)', 'n_requested': 30, 'n_kept': 30, 'n_dropped_bitcap': 0}`
| H | Q_H | I_H | C_H | max_size | n_multi | k*_2 | k*_3 | k_bt_msd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.0333 | 30 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 0.0667 | 23 | 2 | 9 | 4 | None |
| 3 | 4 | 2 | 0.1333 | 14 | 4 | 9 | 4 | None |
| 4 | 8 | 3 | 0.2667 | 11 | 7 | 9 | 4 | None |
| 5 | 12 | 4 | 0.4000 | 6 | 7 | 9 | 4 | None |
| 6 | 16 | 4 | 0.5333 | 4 | 9 | 9 | 4 | None |

### B_n_4000

- |Y| kept: `3999` meta `{'source': 'integers 2..4000', 'n_requested': 3999, 'n_kept': 3999, 'n_dropped_bitcap': 0}`
| H | Q_H | I_H | C_H | max_size | n_multi | k*_2 | k*_3 | k_bt_msd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0.0005 | 2000 | 2 | 1 | 8 | 9 |
| 2 | 4 | 2 | 0.0010 | 1023 | 4 | 12 | 8 | None |
| 3 | 8 | 3 | 0.0020 | 596 | 8 | 12 | 8 | None |
| 4 | 16 | 4 | 0.0040 | 406 | 16 | 12 | 8 | None |
| 5 | 29 | 5 | 0.0073 | 406 | 29 | 12 | 8 | None |
| 6 | 49 | 6 | 0.0123 | 406 | 48 | 12 | 8 | None |

### C_atlas_enriched

- |Y| kept: `5999` meta `{'source': 'landings n<=4000 with bit_length<=1024 plus atlas PE starts', 'n_landings_kept': 2329, 'n_landings_excluded_bits': 3, 'excluded_bit_lengths': [1273, 2462, 5836], 'n_pe': 4000, 'n_requested': 6001, 'atlas_present': True, 'n_kept': 5999, 'n_dropped_bitcap': 2}`
| H | Q_H | I_H | C_H | max_size | n_multi | k*_2 | k*_3 | k_bt_msd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.0002 | 5999 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 0.0003 | 5244 | 2 | 22 | None | None |
| 3 | 4 | 2 | 0.0007 | 2882 | 4 | 26 | None | None |
| 4 | 8 | 3 | 0.0013 | 1962 | 8 | 26 | None | None |
| 5 | 16 | 4 | 0.0027 | 1783 | 16 | 26 | None | None |
| 6 | 32 | 5 | 0.0053 | 919 | 32 | 26 | None | None |

### D_hard

- |Y| kept: `21` meta `{'source': 'documented hard / PE / first-return extremals', 'n_requested': 21, 'n_kept': 21, 'n_dropped_bitcap': 0}`
| H | Q_H | I_H | C_H | max_size | n_multi | k*_2 | k*_3 | k_bt_msd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0.0952 | 16 | 2 | 1 | 4 | 6 |
| 2 | 4 | 2 | 0.1905 | 13 | 3 | 17 | 4 | None |
| 3 | 7 | 3 | 0.3333 | 8 | 4 | 17 | 4 | None |
| 4 | 10 | 4 | 0.4762 | 6 | 6 | 17 | 4 | None |
| 5 | 14 | 4 | 0.6667 | 4 | 5 | 17 | 4 | None |
| 6 | 16 | 4 | 0.7619 | 2 | 5 | 17 | 4 | None |

Word vs coarse vs exact on the primary samples. Exact `F_H^state` is
the next-H-state tuple, so it is determined by `T(x)` and cannot
refine with H. Coarse atoms are `(parity, x mod 8, v2(3x+1), 4 LSD trits)`
along the length-H window.

### Refinement A_residual_80

| H | Q_word | Q_coarse | Q_state |
| --- | --- | --- | --- |
| 1 | 1 | 30 | 30 |
| 2 | 2 | 30 | 30 |
| 3 | 4 | 30 | 30 |
| 4 | 8 | 30 | 30 |
| 5 | 12 | 30 | 30 |
| 6 | 16 | 30 | 30 |

### Refinement B_n_4000

| H | Q_word | Q_coarse | Q_state |
| --- | --- | --- | --- |
| 1 | 2 | 866 | 2055 |
| 2 | 4 | 3989 | 2055 |
| 3 | 8 | 3999 | 2055 |
| 4 | 16 | 3999 | 2055 |
| 5 | 29 | 3999 | 2055 |
| 6 | 49 | 3999 | 2055 |

## 4. Precision hierarchy

Nested consecutive samples (growth with |Y| at fixed H):

| |Y| | k*_2(H=1) | k*_2(H=2) | k*_2(H=3) | k*_2(H=4) | k*_2(H=5) | k*_2(H=6) | I(H=1) | I(H=2) | I(H=3) | I(H=4) | I(H=5) | I(H=6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30 | 1 | 5 | 5 | 5 | 5 | 5 | 1 | 2 | 3 | 4 | 4 | 4 |
| 100 | 1 | 7 | 7 | 7 | 7 | 7 | 1 | 2 | 3 | 4 | 5 | 5 |
| 500 | 1 | 9 | 9 | 9 | 9 | 9 | 1 | 2 | 3 | 4 | 5 | 6 |
| 1000 | 1 | 10 | 10 | 10 | 10 | 10 | 1 | 2 | 3 | 4 | 5 | 6 |

## 5. Separating witnesses

- A_residual_80: `[None, {'y': 243, 'z': 1523, 'H_first_difference': 2, 'Fy': 'OO', 'Fz': 'OE'}, {'y': 243, 'z': 1523, 'H_first_difference': 2, 'Fy': 'OOE', 'Fz': 'OEO'}, {'y': 243, 'z': 1523, 'H_first_difference': 2, 'Fy': 'OOEE', 'Fz': 'OEOO'}, {'y': 243, 'z': 1523, 'H_first_difference': 2, 'Fy': 'OOEEO', 'Fz': 'OEOOE'}, {'y': 243, 'z': 1523, 'H_first_difference': 2, 'Fy': 'OOEEOE', 'Fz': 'OEOOEE'}]`
- B_n_4000: `[{'y': 2, 'z': 3, 'H_first_difference': 1, 'Fy': 'E', 'Fz': 'O'}, {'y': 4, 'z': 2052, 'H_first_difference': 2, 'Fy': 'EE', 'Fz': 'EO'}, {'y': 4, 'z': 2052, 'H_first_difference': 2, 'Fy': 'EEO', 'Fz': 'EOO'}, {'y': 2, 'z': 2050, 'H_first_difference': 4, 'Fy': 'EOOO', 'Fz': 'EOOE'}, {'y': 2, 'z': 2050, 'H_first_difference': 4, 'Fy': 'EOOOO', 'Fz': 'EOOEE'}, {'y': 2, 'z': 2050, 'H_first_difference': 4, 'Fy': 'EOOOOO', 'Fz': 'EOOEEE'}]`
- C_atlas_enriched: `[None, {'y': 2529, 'z': 3195097057761, 'H_first_difference': 2, 'Fy': 'OO', 'Fz': 'OE'}, {'y': 26261, 'z': 397989144213, 'H_first_difference': 3, 'Fy': 'OOO', 'Fz': 'OOE'}, {'y': 26261, 'z': 397989144213, 'H_first_difference': 3, 'Fy': 'OOOO', 'Fz': 'OOEE'}, {'y': 26261, 'z': 397989144213, 'H_first_difference': 3, 'Fy': 'OOOOO', 'Fz': 'OOEEO'}, {'y': 26261, 'z': 397989144213, 'H_first_difference': 3, 'Fy': 'OOOOOE', 'Fz': 'OOEEOE'}]`
- D_hard: `[{'y': 2, 'z': 3, 'H_first_difference': 1, 'Fy': 'E', 'Fz': 'O'}, {'y': 33, 'z': '573141612728625270488952931933108109345', 'H_first_difference': 2, 'Fy': 'OO', 'Fz': 'OE'}, {'y': 33, 'z': '573141612728625270488952931933108109345', 'H_first_difference': 2, 'Fy': 'OOE', 'Fz': 'OEO'}, {'y': 33, 'z': '573141612728625270488952931933108109345', 'H_first_difference': 2, 'Fy': 'OOEE', 'Fz': 'OEOO'}, {'y': 33, 'z': '573141612728625270488952931933108109345', 'H_first_difference': 2, 'Fy': 'OOEEO', 'Fz': 'OEOOO'}, {'y': 33, 'z': '573141612728625270488952931933108109345', 'H_first_difference': 2, 'Fy': 'OOEEOE', 'Fz': 'OEOOOO'}]`

## 6. Information loss

Word futures collapse many starts into one class. `forgotten = 1 - C_H`
is the fraction of starts that are not unique as H-step words.

- A_residual_80 forgotten: `[0.9667, 0.9333, 0.8667, 0.7333, 0.6, 0.4667]` max class `[30, 23, 14, 11, 6, 4]` intra-k2 `[{'min': 9, 'median': 9, 'max': 9, 'n_classes': 1}, {'min': 7, 'median': 7, 'max': 7, 'n_classes': 2}, {'min': 4, 'median': 6, 'max': 7, 'n_classes': 4}, {'min': 0, 'median': 3, 'max': 7, 'n_classes': 8}, {'min': 0, 'median': 2, 'max': 5, 'n_classes': 12}, {'min': 0, 'median': 2, 'max': 5, 'n_classes': 16}]`
- B_n_4000 forgotten: `[0.9995, 0.999, 0.998, 0.996, 0.9927, 0.9877]` max class `[2000, 1023, 596, 406, 406, 406]` intra-k2 `[{'min': 12, 'median': 12, 'max': 12, 'n_classes': 2}, {'min': 12, 'median': 12, 'max': 12, 'n_classes': 4}, {'min': 12, 'median': 12, 'max': 12, 'n_classes': 8}, {'min': 7, 'median': 12, 'max': 12, 'n_classes': 16}, {'min': 7, 'median': 12, 'max': 12, 'n_classes': 29}, {'min': 0, 'median': 12, 'max': 12, 'n_classes': 49}]`

## 7. Complexity growth

D_H versus H on the two primary fixed samples:

- A_residual_80 I_H `[0, 1, 2, 3, 4, 4]` k*_2 `[0, 9, 9, 9, 9, 9]` greedy `[{'n_tests': 0, 'bits': 0, 'predicates': [], 'unresolved': 0}, {'n_tests': 1, 'bits': 4, 'predicates': ['mod3_4'], 'unresolved': 0}, {'n_tests': 1, 'bits': 4, 'predicates': ['mod3_4'], 'unresolved': 0}, {'n_tests': 1, 'bits': 4, 'predicates': ['mod3_4'], 'unresolved': 0}, {'n_tests': 1, 'bits': 4, 'predicates': ['mod3_4'], 'unresolved': 0}, {'n_tests': 1, 'bits': 4, 'predicates': ['mod3_4'], 'unresolved': 0}]`
- B_n_4000 I_H `[1, 2, 3, 4, 5, 6]` k*_2 `[1, 12, 12, 12, 12, 12]` greedy `[{'n_tests': 1, 'bits': 1, 'predicates': ['parity'], 'unresolved': 0}, {'n_tests': 1, 'bits': 12, 'predicates': ['mod2_12'], 'unresolved': 0}, {'n_tests': 1, 'bits': 12, 'predicates': ['mod2_12'], 'unresolved': 0}, {'n_tests': 1, 'bits': 12, 'predicates': ['mod2_12'], 'unresolved': 0}, {'n_tests': 1, 'bits': 12, 'predicates': ['mod2_12'], 'unresolved': 0}, {'n_tests': 1, 'bits': 12, 'predicates': ['mod2_12'], 'unresolved': 0}]`

## 8. Family comparison

- fam_even |Y|=`2000` Q=`[1, 2, 4, 8, 13, 18]` k*_2=`[0, 12, 12, 12, 12, 12]`
- fam_odd |Y|=`1999` Q=`[1, 2, 4, 8, 16, 31]` k*_2=`[0, 12, 12, 12, 12, 12]`
- fam_OOO |Y|=`509` Q=`[1, 1, 1, 2, 4, 8]` k*_2=`[0, 0, 0, 12, 12, 12]`
- fam_EEE |Y|=`427` Q=`[1, 1, 1, 2, 2, 2]` k*_2=`[0, 0, 0, 12, 12, 12]`
- fam_mixed |Y|=`3933` Q=`[2, 4, 8, 16, 29, 48]` k*_2=`[1, 12, 12, 12, 12, 12]`
- fam_PE |Y|=`4000` Q=`[1, 1, 2, 3, 4, 7]` k*_2=`[0, 0, 16, 16, 16, 16]`

## 9. Proof-complexity pilot

Not performed. Phase 0 did not produce a surviving precision hierarchy.

## 10. Interpretation

- `Q_H <= 2^H` on word futures: **COMPUTATIONALLY VERIFIED** (and the
  tautological alphabet bound)
- `I_H <= H`: **COMPUTATIONALLY VERIFIED** from the same bound
- `k*_2(1)` is 0 on an all-odd sample and 1 when both parities appear:
  **COMPUTATIONALLY VERIFIED** (definition of `F_1`)
- `k*_2(H)` plateaus for `H>=2` on samples A, B, and D;
  sample C is `0,22,26,26,26,26` (one extra split at H=3, then flat):
  **COMPUTATIONALLY VERIFIED**
- nested `|Y|` increases `k*_2(2)`: **COMPUTATIONALLY VERIFIED**
- word vs coarse vs exact refinement: **OBSERVATION** (see §3)
- BT low digits vs `y mod 3^k`: expected **REPARAMETERIZATION**
- exact theorem stronger than the alphabet bound: none
- candidate conjecture: none
- formal independence: not studied

Decision reason: Q_H <= 2^H and I_H <= H on every fixed sample (word-alphabet counting). k*_2 jumps at H=2 and then plateaus; the H=2 value grows with |Y| on nested consecutive intervals. Apparent horizon complexity is the itinerary bound plus a sample-diameter 2-adic pair.

## 11. What this experiment cannot show

WHAT THIS EXPERIMENT CANNOT SHOW

* finite-state complexity does not imply formal independence;
* failure of tested projections does not imply no compact representation exists;
* finite horizons do not establish asymptotic unboundedness;
* generalized Collatz undecidability does not transfer automatically to the
  ordinary Juggler / 3n+1 system.

## Lean

- sorry-free: `True`
- no forbidden engines: `True`
- no global halt theorem: `True`
- no independence claim in Lean text: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- tau_always_finite: `False`
- formal_independence: `False`
- unbounded_complexity_implies_unprovability: `False`
- myhill_nerode: `False`
- automaton: `False`
- kolmogorov_complexity: `False`
- reopen_pe_factors: `False`
- reopen_residual_quotient: `False`
- reopen_sum_rho: `False`
- reopen_realization_geometry: `False`
- reopen_landing_image: `False`
- reopen_nc_boundary: `False`
- reopen_first_return: `False`

## Decision

**CLOSE** — `INFO_COMPLEXITY_COUNTEREXAMPLE`

Q_H <= 2^H and I_H <= H on every fixed sample (word-alphabet counting). k*_2 jumps at H=2 and then plateaus; the H=2 value grows with |Y| on nested consecutive intervals. Apparent horizon complexity is the itinerary bound plus a sample-diameter 2-adic pair.

This is not a halt result and not an independence result.

