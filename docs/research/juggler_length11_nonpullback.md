# Juggler length-11 non-pullback leftover attacks

Status: **LENGTH11_NONPULLBACK_REFUTED**

Standalone application phase. Not a Research Engine experiment
and not a termination theorem. The thirty length-11 short-gap
words only; not a length-8/9/11 census and not last-cluster
pullback.

## Branch budget

```text
Mathematical target     Do rotation or internal-E next-square
                        exclude any of the 30 length-11 leftovers?
Novelty hypothesis      A mixed word dies by orientation or by
                        a next-square suffix after an internal E
Falsifier               Every word is already a surviving
                        CycleMin spelling; every internal-E
                        suffix has exponent < 2
Existing machinery      exists_cycleMin; internal-E threshold;
                        the 30-word list
Maximum Phase-0 scope   Classify rotations and exponents;
                        no Lean, no census, no Paper A
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **LENGTH11_NONPULLBACK_REFUTED**
- shapes: `30`
- necklaces: `30`
- next-square suffixes: `0`
- closest margin: `243/256` on `OOOOOEE`
- spot undershoot: `True` at m=`1000215`

rotation cannot exclude an open CycleMin leftover; every internal-E suffix on the 30 words has 3^{#O} < 2^{len+1}, closest 243/256 on v=OOOOOEE; not a length-11 census.

## Lean

- `exists_cycleMin`: `True`
- `cycleMin_not_end_odd`: `True`
- `cycleMin_not_start_even`: `True`
- `cycleMin_not_odd_even`: `True`
- `no_cycleMin_internal_even_threshold`: `True`
- `oo_suffix_threshold`: `True`
- no length-11 theorem: `True`
- length eight open in census: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- cycles_impossible: `False`
- four_even_cycles_impossible: `False`
- length_eight_census: `False`
- length_nine_census: `False`
- length_eleven_census: `False`
- four_even_lean: `False`
- induction_on_period: `False`
- induction_on_n: `False`

## Decision

**LENGTH11_NONPULLBACK_REFUTED**

rotation cannot exclude an open CycleMin leftover; every internal-E suffix on the 30 words has 3^{#O} < 2^{len+1}, closest 243/256 on v=OOOOOEE; not a length-11 census.

This is not a halt result and not a length-8/9/11 census.

