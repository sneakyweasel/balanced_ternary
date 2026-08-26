# Juggler even-run scale barrier

Status: **MINIMAL_NORMAL_FORM_GREEN**

Standalone application phase. Not a Research Engine experiment and
not a termination theorem. A hypothetical minimal non-1 orbit is
not forced to be all-odd. Every even run `E^r` on it must start at
scale `n^{2^r}`.

## Branch budget

```text
Mathematical target     E^r on a minimal non-1 orbit implies entry >= n^{2^r}
Novelty hypothesis      Minimality plus even square-root gives a scale barrier
Falsifier               An even run with exit >= n but entry < n^{2^r}
Existing machinery      ReachesOne closure, even_word_contracts, even_run identities
Maximum Phase-0 scope   MinimalNonTerm; barrier; normal form; short pattern census
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **MINIMAL_NORMAL_FORM_GREEN**
- sorry-free: `True`

E^r on a minimal non-1 orbit forces entry >= n^{2^r}; normal form packages scale, no descent below n, no capture, and first image odd; even states above n remain allowed.

## Even-run census

- realized runs: `103`
- power-envelope failures: `0`
- scale failures with exit >= n: `0`
- runs that stay >= n: `25`
- runs that exit below n: `78`
- even entries above the start (allowed, not all-odd): `64`

## Short patterns

- n=`13` word=`OE` T=`6` kind=`DESCENT` even_ge_sq=`False`
- n=`13` word=`OOE` follows=`False`
- n=`13` word=`OEO` follows=`False`
- n=`13` word=`OEE` T=`2` kind=`DESCENT` even_ge_sq=`False`
- n=`13` word=`OOEE` follows=`False`
- n=`13` word=`OOOE` follows=`False`
- n=`25` word=`OE` follows=`False`
- n=`25` word=`OOE` follows=`False`
- n=`25` word=`OEO` follows=`False`
- n=`25` word=`OEE` follows=`False`
- n=`25` word=`OOEE` follows=`False`
- n=`25` word=`OOOE` T=`228` kind=`NO_CERTIFICATE` even_ge_sq=`True`
- n=`37` word=`OE` follows=`False`
- n=`37` word=`OOE` follows=`False`
- n=`37` word=`OEO` follows=`False`
- n=`37` word=`OEE` follows=`False`
- n=`37` word=`OOEE` follows=`False`
- n=`37` word=`OOOE` follows=`False`
- n=`41` word=`OE` T=`16` kind=`DESCENT` even_ge_sq=`False`
- n=`41` word=`OOE` follows=`False`
- n=`41` word=`OEO` follows=`False`
- n=`41` word=`OEE` T=`4` kind=`DESCENT` even_ge_sq=`False`
- n=`41` word=`OOEE` follows=`False`
- n=`41` word=`OOOE` follows=`False`

## Changing-family capture

- n=`2` word=`E` kind=`CAPTURE` T=`1`
- n=`16` word=`EEEOOOOOOOOO` kind=`CAPTURE` T=`1`
- n=`7` word=`OEEEOOOOOOOOO` kind=`CAPTURE` T=`1`
- n=`2500` word=`EEOEEEOOOOOOOOOOOO` kind=`CAPTURE` T=`1`

## First image after an odd start

- odd starts in `13..80` with even first image: `19`
- all of those `OE` prefixes are descent: `True`

A hypothetical minimal start cannot do this. Later even states
above `n^2` remain allowed.

## Lean

- `MinimalNonTerm`: `True`
- `minimal_nonterm_ge_of_not_reachesOne`: `True`
- `even_run_pow_le`: `True`
- `even_run_exit_ge`: `True`
- `even_run_scale_barrier`: `True`
- `minimal_nonterm_even_ge_sq`: `True`
- `minimal_nonterm_first_even_ge_sq`: `True`
- `minimal_nonterm_avoid_even_lt_sq_twelve`: `True`
- `even_tower_not_on_minimal`: `True`
- `minimal_nonterm_oe_descent`: `True`
- `minimal_nonterm_odd_image_odd`: `True`
- `minimal_counterexample_normal_form`: `True`
- `minimal_nonterm_odd`: `True`
- `minimal_nonterm_image_ge`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- no infinite-path type: `True`
- no all-odd orbit theorem: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- all_odd_orbit: `False`

## Decision

**MINIMAL_NORMAL_FORM_GREEN**

E^r on a minimal non-1 orbit forces entry >= n^{2^r}; normal form packages scale, no descent below n, no capture, and first image odd; even states above n remain allowed.

This is not a halt result and not an all-odd orbit theorem.

