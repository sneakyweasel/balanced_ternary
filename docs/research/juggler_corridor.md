# Juggler two-sided minimal-counterexample corridor

Status: **CORRIDOR_REPACKAGING**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. Not the REFUTED two-sided
exponent-only law. A corridor is the pair of exact inequalities
x^{2^r} <= n^{3^o} and n^{2^s} <= x^{3^q} at a pivot x = T^j(n).

## Branch budget

```text
Mathematical target     On stay-above prefixes, does a pivot corridor
                        constrain x beyond 2^{r+s} <= 3^{o+q}?
Novelty hypothesis      prefix defect or closure forces extremality
                        or a contraction the full word misses
Falsifier               every exact predicate is power_bound_word + image>=n
Existing machinery      power_bound_*, first-defect, cmp_pow,
                        minimal_nonterm_image_ge, excursion corpus
Maximum Phase-0 scope   one probe; stay-above + first-return census; no Lean
```

## Metadata

- search_id: `juggler-corridor-phase0-n2-2000`
- algorithm_version: `corridor-v1`
- window: `n=2..2000`
- horizon: `10000` (not L)
- bit_cap: `4096`
- pivot_policy: `every j in 0..tau-1`
- suffix_policy: `every s>=1 with j+s<=tau; stay-above iff j+s<tau`
- engine control layer modified: `False`
- classification: **CORRIDOR_REPACKAGING**
- secondary: `[]`
- sorry-free: `True`

on stay-above segments, forward, reverse, and compat are the concatenated envelope plus image>=n; reverse never fires unless the concatenated word is formally contracting; equality hits are only known extremal towers.

## Census

- returned: `1999`
- unfinished: `0`
- corridors: `45948`
- stay-above: `39137`
- return suffixes: `6811`
- even stay-above: `0`
- identity failures: `0`
- forward unavailable: `17849`
- reverse unavailable: `213`
- mixed equality: `0`
- extremal equality count: `150`
- both sides equal: `0`
- novel reverse stay-above: `0`
- novel reverse at return: `0`
- defect over gap: `0`
- max τ_<: `70`
- max peak bits: `900`

## Closest stay-above slack

- n=`3` j=`0` s=`1` slack=`1` G=`-1` prefix=`` suffix=`O` extremal_eq=`False`
- n=`5` j=`0` s=`1` slack=`1` G=`-1` prefix=`` suffix=`O` extremal_eq=`False`
- n=`5` j=`0` s=`3` slack=`1` G=`-1` prefix=`` suffix=`OOE` extremal_eq=`False`
- n=`5` j=`1` s=`2` slack=`1` G=`-1` prefix=`O` suffix=`OE` extremal_eq=`False`
- n=`5` j=`2` s=`1` slack=`1` G=`-1` prefix=`OO` suffix=`E` extremal_eq=`False`
- n=`7` j=`0` s=`1` slack=`1` G=`-1` prefix=`` suffix=`O` extremal_eq=`False`
- n=`9` j=`0` s=`1` slack=`1` G=`-1` prefix=`` suffix=`O` extremal_eq=`False`
- n=`9` j=`0` s=`3` slack=`1` G=`-1` prefix=`` suffix=`OOE` extremal_eq=`False`
- n=`9` j=`1` s=`2` slack=`1` G=`-1` prefix=`O` suffix=`OE` extremal_eq=`True`
- n=`9` j=`2` s=`1` slack=`1` G=`-1` prefix=`OO` suffix=`E` extremal_eq=`False`
- n=`11` j=`0` s=`1` slack=`1` G=`-1` prefix=`` suffix=`O` extremal_eq=`False`
- n=`13` j=`0` s=`1` slack=`1` G=`-1` prefix=`` suffix=`O` extremal_eq=`False`

## Hard starts

- n=`9` τ=`5` stay=`10` return=`5` ident=`0` extremal_eq=`4` min_slack=`1` word=`OOEOE`
- n=`37` τ=`15` stay=`105` return=`15` ident=`0` extremal_eq=`0` min_slack=`1` word=`OOOOEOOOEEOOEEE`
- n=`49` τ=`5` stay=`10` return=`5` ident=`0` extremal_eq=`4` min_slack=`1` word=`OOEOE`
- n=`69` τ=`7` stay=`21` return=`7` ident=`0` extremal_eq=`0` min_slack=`1` word=`OOEOOEE`
- n=`77` τ=`10` stay=`45` return=`10` ident=`0` extremal_eq=`0` min_slack=`1` word=`OOOEOEOOEE`
- n=`173` τ=`26` stay=`325` return=`26` ident=`0` extremal_eq=`0` min_slack=`1` word=`OOEOOOOOOOOEOOEOOEEOEEOEEE`

## Tall starts

- n=`193` τ=`70` peak_bits=`900` stay=`2415` min_slack=`1`
- n=`557` τ=`27` peak_bits=`888` stay=`351` min_slack=`1`
- n=`761` τ=`62` peak_bits=`851` stay=`1891` min_slack=`1`

## Lean

- `power_bound_word`: `True`
- `power_bound_contracts`: `True`
- `power_bound_eq_iff_extremal`: `True`
- `power_bound_compensated_contracts`: `True`
- `minimal_nonterm_image_ge`: `True`
- new Corridor file absent: `True`
- ResidualStep not extended: `True`
- CycleDiophantine not rewritten: `True`
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
- finite_progress_for_all: `False`
- minimal_nonterm_rebuilt: `False`
- two_sided_exponent_law: `False`
- corridor_is_new_progress: `False`

## Decision

**CORRIDOR_REPACKAGING**

on stay-above segments, forward, reverse, and compat are the concatenated envelope plus image>=n; reverse never fires unless the concatenated word is formally contracting; equality hits are only known extremal towers.

A finite stay-above prefix is not a minimal counterexample.
A search-horizon miss is not a bound L. Do not claim termination.

