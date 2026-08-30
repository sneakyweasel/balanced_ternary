# Juggler maximal odd-run block map Q

Status: **BLOCK_MAP_Q_PARK**

Standalone application phase. Not a Research Engine experiment,
not a run-length automaton, not a residue search, and not a
halt theorem. The leftover is the arithmetic map Q on odd
AboveAnchor landings.

## Convention

For odd `x`, `a(x)` counts consecutive odd states starting at
`x`. Then `T^{a(x)}(x)` is even and `Q(x)=T^{a(x)+1}(x)` is
the post-even landing. The even state is interior. `Q(x)` may
be even. Domain `D_n` is odd landings `>= n` on the path of `n`.

## Branch budget

```text
Mathematical target     smallest exact state that gives Q a
                        transition law on residual D_n
Novelty hypothesis      (x,Q(x)) or a two-block relation
                        predicts the next run
Falsifier               every finite descriptor fails; the
                        integer landing is the only predictor
Existing machinery      a(x), pe_blocks, leftover controls,
                        oe_block_contracts, isolated OE
Maximum Phase-0 scope   leftovers + odd n<2001; no automaton
```

## Metadata

- classification: **BLOCK_MAP_Q_PARK**
- Q^3(365): `4447` a=`2`
- Q^3(1517): `33811` a=`1`
- intrinsic shared: `False`
- repeated endpoints: `0`
- (2,+) next a: `[1, 2, 3, 4, 5, 6, 7, 8, 9]`
- 222 next: `{'1': 3, '2': 1}`
- contract then Q^2 stays: `144`

Q on D_n is no more predictive than the raw landing: after (2,2,2) the states 4447 and 33811 share no intrinsic coordinate, (a,sign) and (prev a,a) do not determine the next run, first-odd defect and even remainder collide, Q>x need not force Q^2 descent, and Q<x with Q>=n need not force Q^2 below the anchor; no exact endpoint repeats.

## Leftover Q-orbits

- 365 starts: `[365, 763, 1749, 4447, 12707]` runs=`[2, 2, 2, 2, 1]`
- 1517 starts: `[1517, 3789, 10613, 33811, 2493]` runs=`[2, 2, 2, 1, 3]`
- 501 starts: `[501, 1089, 133347, 763, 1749, 4447, 12707]`
- 6187 starts: `[6187, 18425, 15771571, 11189]`

## Existing Lean (unchanged)

- `oe_block_contracts`: `True`
- `isolatedOddSurvival_bound`: `True`
- `finiteProgress_of_ooe_oe`: `True`
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
- block_transition_theorem: `False`
- finite_q_descriptor: `False`
- two_block_return_law: `False`
- run_length_graph: `False`
- residue_automaton: `False`

## Decision

**BLOCK_MAP_Q_PARK**

Q on D_n is no more predictive than the raw landing: after (2,2,2) the states 4447 and 33811 share no intrinsic coordinate, (a,sign) and (prev a,a) do not determine the next run, first-odd defect and even remainder collide, Q>x need not force Q^2 descent, and Q<x with Q>=n need not force Q^2 below the anchor; no exact endpoint repeats.

This is not a halt result and not a Q-frequency theorem.

