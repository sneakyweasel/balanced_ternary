# Juggler adversarial parity paths

Status: **EXTREMAL_COMPLEX**

Standalone Phase-0 search for the hardest realizable finite O/E
paths. Not a Research Engine experiment, not a Lyapunov scalar,
and not a termination theorem. A horizon miss is not a bound on tau.

## Branch budget

```text
Mathematical target     Do the hardest realized paths share a structure?
Novelty hypothesis      recurring shape, peak law, survival law, or hardening swap
Falsifier               known first-return records; (k,o) splits; swaps do not harden
Existing machinery      _walk_returns, exponent_gap, first_defect_sufficient
Maximum Phase-0 scope   n=2..4000; no GPU; no Lean; no new scalar
```

## 1. Objective

- A: maximize endpoint ratio `T^k(n)/n` at each prefix horizon (exact cross-multiply)
- B: maximize peak ratio `P/n` (bit-length when the peak exceeds the storage cap)
- C: minimize return margin `M` and `M/n` among observed returns
- D/E: maximize duration `tau` / longest noncontracting prefix (`tau-1` on a return)
- F: Pareto front on min `M/n`, max peak bits, max `tau`

These are optimization coordinates, not proposed invariants.

## 2. Coverage

- window: `n=2..4000` starts `3999` returned `3999` miss `0`
- bit-cap promoted: `[2183, 3431]`
- tau: `1` … `77` distinct words `272`

Record paths are the known first-return extremals. Fixed-(k,o) arrangement splits, but no reproducible shape, peak-location, certificate-survival, or hardening-swap law survives. Extremality remains state-determined.

## 3. Record chains

- min M: `{'n': 2, 'tau': 1, 'word': 'E', 'o': 0, 'M': 1, 'ratio': '1/2', 'peak_bits': 2, 'peak_pos': 0, 'first_defect': 0, 'first_exp': 1, 'runs': (1, 0, 1), 'final': 'E'}`
- min M/n: `{'n': 425, 'tau': 46, 'word': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'o': 29, 'M': 60, 'ratio': '12/85', 'peak_bits': 243, 'peak_pos': 38, 'first_defect': 0, 'first_exp': 46, 'runs': (18, 7, 4), 'final': 'E'}`
- max tau: `{'n': 3889, 'tau': 77, 'word': 'OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOOOEEOEOEEOEOEEOOOEEOEOOEEOOEEOOOOOEEEE', 'o': 48, 'M': 3811, 'ratio': '3811/3889', 'peak_bits': 3350, 'peak_pos': 41, 'first_defect': 0, 'first_exp': 77, 'runs': (40, 6, 4), 'final': 'E'}`
- max peak bits: `{'n': 2183, 'tau': 54, 'word': 'OOEOOOOEOOOOOOOOEOOOEOOOOOOOEOOOEEEOOOEEEEEEOEEOEEOOEE', 'o': 34, 'M': 950, 'ratio': '950/2183', 'peak_bits': 19694, 'peak_pos': 32, 'first_defect': 0, 'first_exp': 54, 'runs': (20, 8, 6), 'final': 'E'}`
- M=1 witnesses: `[{'n': 2, 'tau': 1, 'word': 'E', 'o': 0, 'M': 1, 'ratio': '1/2', 'peak_bits': 2, 'peak_pos': 0, 'first_defect': 0, 'first_exp': 1, 'runs': (1, 0, 1), 'final': 'E'}, {'n': 3, 'tau': 5, 'word': 'OOOEE', 'o': 3, 'M': 1, 'ratio': '1/3', 'peak_bits': 6, 'peak_pos': 3, 'first_defect': 0, 'first_exp': 5, 'runs': (2, 3, 2), 'final': 'E'}]`

Prefix endpoint / peak records (`k<=20`):

| k | endpoint n | endpoint word | endpoint bits | peak n | peak bits |
| --- | --- | --- | --- | --- | --- |
| 1 | 3999 | O | 18 | 3999 | 18 |
| 2 | 3999 | OO | 27 | 3999 | 27 |
| 3 | 3999 | OOO | 41 | 3999 | 41 |
| 4 | 3987 | OOOO | 61 | 3987 | 61 |
| 5 | 3987 | OOOOO | 91 | 3987 | 91 |
| 6 | 3987 | OOOOOO | 137 | 3987 | 137 |
| 7 | 3973 | OOOOOOO | 205 | 3973 | 205 |
| 8 | 3439 | OOOOOOOO | 302 | 3439 | 302 |
| 9 | 3439 | OOOOOOOOO | 452 | 3439 | 452 |
| 10 | 3439 | OOOOOOOOOO | 678 | 3439 | 678 |
| 11 | 663 | OOOOOOOOOOO | 811 | 663 | 811 |
| 12 | 3973 | OOOOOOOEOOOO | 518 | 663 | 811 |
| 13 | 3151 | OOOOOOEOOOOOO | 754 | 663 | 811 |
| 14 | 3151 | OOOOOOEOOOOOOO | 1131 | 3151 | 1131 |
| 15 | 3151 | OOOOOOEOOOOOOOO | 1697 | 3151 | 1697 |
| 16 | 3151 | OOOOOOEOOOOOOOOO | 2545 | 3151 | 2545 |
| 17 | 3151 | OOOOOOEOOOOOOOOOE | 1273 | 3151 | 2545 |
| 18 | 3151 | OOOOOOEOOOOOOOOOEO | 1909 | 3151 | 2545 |
| 19 | 3973 | OOOOOOOEOOOOEEOOOOO | 982 | 3151 | 2545 |
| 20 | 3973 | OOOOOOOEOOOOEEOOOOOO | 1473 | 3151 | 2545 |

## 4. Pareto frontier

Count: `10`

| n | tau | M | M/n | peak bits | word |
| --- | --- | --- | --- | --- | --- |
| 425 | 46 | 60 | 12/85 | 243 | OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE |
| 557 | 27 | 119 | 119/557 | 888 | OOOOOEOOOOOOOOEOEOEEEOEEOEE |
| 2183 | 54 | 950 | 950/2183 | 19694 | OOEOOOOEOOOOOOOOEOOOEOOOOOOOEOOOEEEOOOEEEEEEOEEOEEOOEE |
| 761 | 62 | 421 | 421/761 | 851 | OOOOOOOOOEEOEOEEOOEEOOOEOOOOEOOOEOEOOOEEOOOOEOOOOEEEOOOEEEEOEE |
| 193 | 70 | 113 | 113/193 | 900 | OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOOOEOOOOEEOOEOOEOEEOOEOOEEOEEEE |
| 3439 | 62 | 2158 | 2158/3439 | 1045 | OOOOOOOOOOEOEOOEOOOEEOOEEOOOEEOOEOEOOOOEOOEEOOOOOEEEOEOEOEOEEE |
| 3547 | 70 | 2633 | 2633/3547 | 1049 | OOOEOOOEOOOOOOOOEEEEOOOOOEOEEOEOOOOOOOEOEOOEEOOOOEEOEOEOOOEEEOOOEOEEEE |
| 3973 | 59 | 3326 | 3326/3973 | 1890 | OOOOOOOEOOOOEEOOOOOOEOEOOEEOEOOOOOEOEOEOEOOOOEEEEEEOOOOEEEE |
| 3271 | 69 | 3181 | 3181/3271 | 2460 | OOEOOOOOOOEOEOOOOOOEEEEOEOOOOOOEEOOOEOOOOOOEEOEOOOOEEEEOEEOEEOOOEEOEE |
| 3889 | 77 | 3811 | 3811/3889 | 3350 | OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOOOEEOEOEEOEOEEOOOEEOEOOEEOOEEOOOOOEEEE |

## 5. Fixed-(k,o) extremals

- groups with several words (`k<=12`): `5`
- groups that split: `5` identical `0`
- clustered worst / distributed worst: `5` / `4`
- examples: `[{'k': 5, 'o': 3, 'n_words': 2, 'best_margin_word': 'OOOEE', 'worst_margin_word': 'OOEOE', 'best_peak_word': 'OOOEE', 'min_M_range': [1, 3], 'peak_bits_range': [27, 41]}, {'k': 7, 'o': 4, 'n_words': 3, 'best_margin_word': 'OOEOOEE', 'worst_margin_word': 'OOOOEEE', 'best_peak_word': 'OOOOEEE', 'min_M_range': [55, 237], 'peak_bits_range': [31, 61]}, {'k': 10, 'o': 6, 'n_words': 12, 'best_margin_word': 'OOOEOEOOEE', 'worst_margin_word': 'OOEOOOOEEE', 'best_peak_word': 'OOOOOOEEEE', 'min_M_range': [56, 2652], 'peak_bits_range': [34, 125]}, {'k': 8, 'o': 5, 'n_words': 7, 'best_margin_word': 'OOEOOEOE', 'worst_margin_word': 'OOOOEEOE', 'best_peak_word': 'OOOOOEEE', 'min_M_range': [19, 287], 'peak_bits_range': [31, 91]}, {'k': 12, 'o': 7, 'n_words': 18, 'best_margin_word': 'OOOOOOOEEEEE', 'worst_margin_word': 'OOOEOEOOEOEE', 'best_peak_word': 'OOOOOOOEEEEE', 'min_M_range': [269, 3649], 'peak_bits_range': [28, 201]}]`
- same-word spread: `{'multi_start_words': 49, 'strongest': {'word': 'OOEE', 'n_starts': 255, 'min_M': 3, 'max_M': 3878, 'min_n': 5, 'max_n': 3983}}`

## 6. First-defect structure

- first defect at index 0: `3937` of `3999`
- nonzero first defect: `[{'n': 4, 'first_defect': None, 'word': 'E'}, {'n': 9, 'first_defect': 1, 'word': 'OOEOE'}, {'n': 16, 'first_defect': None, 'word': 'E'}, {'n': 25, 'first_defect': 1, 'word': 'OOOEE'}, {'n': 36, 'first_defect': None, 'word': 'E'}, {'n': 49, 'first_defect': 1, 'word': 'OOEOE'}, {'n': 64, 'first_defect': None, 'word': 'E'}, {'n': 81, 'first_defect': 2, 'word': 'OOOEOEE'}]`

## 7. Certificate survival

- first `G_j>0` equals tau: `3999` of `3999`
- first `G_j>0` before tau: `[]`
- defect-certificate scan on extremals: `[{'n': 2, 'tau': 1, 'first_exp': 1, 'first_defect_cert': 1, 'first_return': 1, 'word': 'E'}, {'n': 3, 'tau': 5, 'first_exp': 5, 'first_defect_cert': 5, 'first_return': 5, 'word': 'OOOEE'}, {'n': 7, 'tau': 2, 'first_exp': 2, 'first_defect_cert': 2, 'first_return': 2, 'word': 'OE'}, {'n': 193, 'tau': 70, 'first_exp': 70, 'first_defect_cert': None, 'first_return': 70, 'word': 'OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOOOEOOOOEEOOEOOEOEEOOEOOEEOEEEE'}, {'n': 425, 'tau': 46, 'first_exp': 46, 'first_defect_cert': None, 'first_return': 46, 'word': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE'}, {'n': 2183, 'tau': 54, 'first_exp': 54, 'first_defect_cert': None, 'first_return': 54, 'word': 'OOEOOOOEOOOOOOOOEOOOEOOOOOOOEOOOEEEOOOEEEEEEOEEOEEOOEE'}, {'n': 3889, 'tau': 77, 'first_exp': 77, 'first_defect_cert': None, 'first_return': 77, 'word': 'OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOOOEEOEOEEOEOEEOOOEEOEOOEEOOEEOOOOOEEEE'}]`

H_k is therefore the set of proper prefixes of observed first-return
words: they survive the exponent certificate until the last letter.
That is the parked envelope census, not a new survival law.

## 8. Structural patterns

- Q1 holds `False` — lex record words: ['E', 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'OOEOOOOEOOOOOOOOEOOOEOOOOOOOEOOOEEEOOOEEEEEEOEEOEEOOEE', 'OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOOOEEOEOEEOEOEEOOOEEOEOOEEOOEEOOOOOEEEE']
- Q2 holds `False` — 5 fixed-(k,o) groups split extrema; clustered_worst=5 distributed_worst=4
- Q3 holds `False` — peak-at-OE is 1999 of 1999 long odd returns (early/mid/late 44/1822/133); universal odd-growth plus even contraction, not an extremal-only law
- Q4 holds `False` — first defect is 0 on 3937 of 3999; nonzero starts: [{'n': 4, 'first_defect': None, 'word': 'E'}, {'n': 9, 'first_defect': 1, 'word': 'OOEOE'}, {'n': 16, 'first_defect': None, 'word': 'E'}, {'n': 25, 'first_defect': 1, 'word': 'OOOEE'}, {'n': 36, 'first_defect': None, 'word': 'E'}, {'n': 49, 'first_defect': 1, 'word': 'OOEOE'}, {'n': 64, 'first_defect': None, 'word': 'E'}, {'n': 81, 'first_defect': 2, 'word': 'OOOEOEE'}]
- Q5 holds `False` — first G_j>0 equals tau on 3999 of 3999
- Q6 holds `False` — extremal peaks are not one growth/finance cut; positions [2, 3, 7, 193, 425, 2183, 3889] at [0, 3, 1, 47, 38, 32, 41]
- Q7 holds `False` — adjacent O/E swaps hardened 1 of 38 window trials

- peak location counts: early/mid/late `44`/`1822`/`133` OE `1999`
- G-profile tails: `[{'n': 2, 'tau': 1, 'G_head': [1], 'G_tail': [1], 'word': 'E'}, {'n': 3, 'tau': 5, 'G_head': [-1, -5, -19, -11, 5], 'G_tail': [-1, -5, -19, -11, 5], 'word': 'OOOEE'}, {'n': 7, 'tau': 2, 'G_head': [-1, 1], 'G_tail': [-1, 1], 'word': 'OE'}, {'n': 193, 'tau': 70, 'G_head': [-1, -5, -19, -11, -49, -179], 'G_tail': [-291363479247117974395, -910983925888773026417, -837196949593934819953, -689622997004258407025, -394475091824905581169, 195820718533800070543], 'word': 'OOOEOOOOOOOEOOOEEOEEOOOOOOEEEOOOEOOEEOOOOOEOOOOEEOOEOOEOEEOOEOOEEOEEEE'}, {'n': 425, 'tau': 46, 'G_head': [-1, -5, -19, -65, -211, -665], 'G_tail': [-5426574229435, -18478745943857, -14080699432753, -51038191320467, -33446005276051, 1738366812781], 'word': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE'}, {'n': 2183, 'tau': 54, 'G_head': [-1, -5, -1, -11, -49, -179], 'G_tail': [-1290070235430529, -727120282009217, -3307260752870275, -12173582072296073, -7669982444925577, 1337216809815415], 'word': 'OOEOOOOEOOOOOOOOEOOOEOOOOOOOEOOOEEEOOOEEEEEEOEEOEEOOEE'}, {'n': 3889, 'tau': 77, 'G_head': [-1, -5, -19, -65, -211, -179], 'G_tail': [-21866447876087858074091, -70321710111133219435969, -60876977145393929008577, -41987511213915348153793, -4208579350958186444225, 71349284374956136974911], 'word': 'OOOOOEOEOOOEOOEOEOEOOOOOOEOOOEOEOOOEOOOOOEEOEOEEOEOEEOOOEEOEOOEEOOEEOOOOOEEEE'}]`
- adjacent swaps: `{'n_trials': 38, 'n_hardened': 1, 'examples': [{'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOEOOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOOEOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOEOEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEOEOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOEOOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOOEEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOEEOEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOEOEOEOEOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOEOEEOEOOOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOEOEEOOOEOOOOEEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOEOEEOOEOOOOEOEEEOOOOOOOEEEOEOEE', 'realized': False}, {'from': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEEOOOOOOOEEEOEOEE', 'to': 'OOOOOOOEOOEEOOOEOEEOOEOOOOOEEEOEOOOOOOEEEOEOEE', 'realized': False}]}`

## 9. Counterexamples

- Recurring record shape: the five lex records are five words.
- Arrangement law at fixed (k,o): split groups in §5.
- Peak always at an O-to-E cut: §8 Q3 counts.
- First defect postponed on hard paths: defect 0 is generic.
- Hardening swap: §8 Q7.
- Return-margin law stronger than `M>=1`: `OOOEE` at 3.

## 10. Decision

**CLOSE** — `EXTREMAL_COMPLEX`

Record paths are the known first-return extremals. Fixed-(k,o) arrangement splits, but no reproducible shape, peak-location, certificate-survival, or hardening-swap law survives. Extremality remains state-determined.

This is not a halt result and not a proof that tau is finite.

## Lean

- sorry-free: `True`
- `power_bound_contracts`: `True`
- `floorPower_odd_ge`: `True`
- no forbidden engines: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- tau_always_finite: `False`
- new_lyapunov_scalar: `False`
- reopen_pe_factors: `False`
- reopen_residual_quotient: `False`
- reopen_sum_rho: `False`
- reopen_realization_geometry: `False`
- reopen_landing_image: `False`
- reopen_nc_boundary: `False`
- reopen_first_return: `False`
- reopen_information_complexity: `False`
- automaton: `False`

