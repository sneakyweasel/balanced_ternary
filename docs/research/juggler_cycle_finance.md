# Juggler cycle finance inequality

Status: **CYCLE_FINANCE_GREEN**

Finance bound n ln n <= (6/5) L 3^o/(3^o - 2^L) on cycle minima.
Not a halt theorem. Not a no-cycle-of-any-length theorem.
The floor is COMPUTATIONALLY VERIFIED, not Lean.

## Metadata

- classification: **CYCLE_FINANCE_GREEN**
- gap table: L <= `100000` exact bignum
- floor: every 2 <= n <= `1000000` reaches 1: `True` (max first-passage steps `253` at seed `78901`, peak `6342922` bits)
- contiguous excluded prefix at this floor: L <= `1053`
- exceptional lengths at this floor: `397`
- Eliahou leftover: period `57`, or one of `397` listed near-convergents, or `>= 100000`

per-step finance bounds hold on every measured orbit step; descent induction verifies every n <= 1000000 reaches 1; finance excludes every cycle length L <= 1053 at once, far beyond the length-8 census; exceptional lengths are exactly the near-convergent ones.

## Census cross-check (L <= 8)

- n_max by length: `{1: 3, 2: 3, 3: 13, 4: 6, 5: 6, 6: 13, 7: 8, 8: 7}`
- killed by finance + Lean residual floor: `[1, 2, 4, 5, 7, 8]`
- census-only lengths: `[3, 6]`

## Record (near-convergent) lengths

- L=`1` o=`1` theta=`3.333e-01` n_max=`3`
- L=`3` o=`2` theta=`1.111e-01` n_max=`13`
- L=`11` o=`7` theta=`6.356e-02` n_max=`52`
- L=`19` o=`12` theta=`1.346e-02` n_max=`297`
- L=`84` o=`53` theta=`2.086e-03` n_max=`5599`
- L=`569` o=`359` theta=`1.065e-03` n_max=`58398`
- L=`1054` o=`665` theta=`4.365e-05` n_max=`1997197`
- L=`25781` o=`16266` theta=`2.546e-05` n_max=`67410774`
- L=`50508` o=`31867` theta=`7.265e-06` n_max=`420161535`

## Exceptional lengths by floor

- floor `11`: count `99992`, first `3`, contiguous prefix `2`
- floor `1000`: count `97734`, first `84`, contiguous prefix `83`
- floor `1000000`: count `397`, first `1054`, contiguous prefix `1053`
- floor `1000000000`: count `0`, first `None`, contiguous prefix `100000`

## Orbit slack

- seed `25`: steps `11` step bound ok `True` defect bound ok `True` identity err `1.84e-16` tightness `0.2166`
- seed `27`: steps `6` step bound ok `True` defect bound ok `True` identity err `1.11e-16` tightness `0.3756`
- seed `37`: steps `17` step bound ok `True` defect bound ok `True` identity err `2.14e-16` tightness `0.3505`
- seed `365`: steps `21` step bound ok `True` defect bound ok `True` identity err `2.11e-16` tightness `0.4383`
- seed `1999`: steps `31` step bound ok `True` defect bound ok `True` identity err `1.64e-16` tightness `0.4689`
- seed `30817`: steps `93` step bound ok `True` defect bound ok `True` identity err `2.09e-16` tightness `0.456`
- seed `1000003`: steps `8` step bound ok `True` defect bound ok `True` identity err `1.72e-16` tightness `0.4747`

## Anti-overclaim

- halt_theorem: `False`
- no_cycle_all_lengths: `False`
- escape_claim: `False`
- corridor_extension: `False`
- population_census_reopen: `False`
- lean_finance_added: `False`
- floor_is_lean_verified: `False`

## Decision

**CYCLE_FINANCE_GREEN**

per-step finance bounds hold on every measured orbit step; descent induction verifies every n <= 1000000 reaches 1; finance excludes every cycle length L <= 1053 at once, far beyond the length-8 census; exceptional lengths are exactly the near-convergent ones.

