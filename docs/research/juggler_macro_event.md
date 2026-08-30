# Juggler macro-event coupling

Status: **MACRO_EVENT_CLOSED**

Successive Q-episodes on leftover and laboratory orbits.
Not a halt theorem. Not a macro automaton.

## Branch budget

```text
Mathematical target     exact pair/triple law on
                        consecutive expansion/reset episodes
Novelty hypothesis      the sequence carries a constraint
                        absent from one episode
Maximum Phase-0 scope   Q-episodes; named starts;
                        window < 401; no Lean
```

## Metadata

- classification: **MACRO_EVENT_CLOSED**
- Q boundary: `True`
- 3375 interior: `True`
- sources 37: `[37, 9317, 2233]`
- climb 365: `[365, 763, 1749, 4447, 12707]`
- no universal triple: `True`
- long-then-long window: `11`

episodes are Q-blocks; 3375 is interior; no named triple law survives; long runs can follow long runs.

## Named episodes

- `37`: runs=`[4, 3, 2]` sources=`[37, 9317, 2233]`
  - X=`37` r=`4` R=`86818724` Q=`9317` s=`1` below=`False`
  - X=`9317` r=`3` R=`24906114455136` Q=`4990602` s=`2` below=`False`
  - X=`2233` r=`2` R=`34276462` Q=`5854` s=`3` below=`False`
- `69`: runs=`[2, 2]` sources=`[69, 117]`
  - X=`69` r=`2` R=`13716` Q=`117` s=`1` below=`False`
  - X=`117` r=`2` R=`44992` Q=`212` s=`2` below=`False`
- `89`: runs=`[2, 2, 1]` sources=`[89, 155, 291]`
  - X=`89` r=`2` R=`24302` Q=`155` s=`1` below=`False`
  - X=`155` r=`2` R=`84722` Q=`291` s=`1` below=`False`
  - X=`291` r=`1` R=`4964` Q=`70` s=`1` below=`True`
- `365`: runs=`[2, 2, 2, 2, 1]` sources=`[365, 763, 1749, 4447, 12707]`
  - X=`365` r=`2` R=`582276` Q=`763` s=`1` below=`False`
  - X=`763` r=`2` R=`3059506` Q=`1749` s=`1` below=`False`
  - X=`1749` r=`2` R=`19782308` Q=`4447` s=`1` below=`False`
  - X=`4447` r=`2` R=`161491284` Q=`12707` s=`1` below=`False`
  - X=`12707` r=`1` R=`1432400` Q=`1196` s=`2` below=`False`
- `501`: runs=`[2, 3, 2, 2, 2, 2, 1]` sources=`[501, 1089, 133347, 763, 1749, 4447, 12707]`
  - X=`501` r=`2` R=`1187360` Q=`1089` s=`1` below=`False`
  - X=`1089` r=`3` R=`17781526790` Q=`133347` s=`1` below=`False`
  - X=`133347` r=`2` R=`339791341082` Q=`582916` s=`2` below=`False`
  - X=`763` r=`2` R=`3059506` Q=`1749` s=`1` below=`False`
  - X=`1749` r=`2` R=`19782308` Q=`4447` s=`1` below=`False`
  - X=`4447` r=`2` R=`161491284` Q=`12707` s=`1` below=`False`
  - X=`12707` r=`1` R=`1432400` Q=`1196` s=`2` below=`False`
- `1517`: runs=`[2, 2, 2, 1, 3]` sources=`[1517, 3789, 10613, 33811, 2493]`
  - X=`1517` r=`2` R=`14362030` Q=`3789` s=`1` below=`False`
  - X=`3789` r=`2` R=`112636568` Q=`10613` s=`1` below=`False`
  - X=`10613` r=`2` R=`1143235850` Q=`33811` s=`1` below=`False`
  - X=`33811` r=`1` R=`6217088` Q=`2493` s=`1` below=`False`
  - X=`2493` r=`3` R=`291028018566` Q=`539470` s=`2` below=`False`
- `6187`: runs=`[2, 3, 2, 1]` sources=`[6187, 18425, 15771571, 11189]`
  - X=`6187` r=`2` R=`339491658` Q=`18425` s=`1` below=`False`
  - X=`18425` r=`3` R=`248742471750750` Q=`15771571` s=`1` below=`False`
  - X=`15771571` r=`2` R=`15675400641582836` Q=`125201440` s=`2` below=`False`
  - X=`11189` r=`1` R=`1183550` Q=`1087` s=`1` below=`True`

## Triple failures

- `x2_lt_x0` universal=`False` fails=`[{'n': 37, 'x0': 37, 'x1': 9317, 'x2': 2233}]`
- `x0_x2_lt_x1_sq` universal=`False` fails=`[{'n': 89, 'x0': 89, 'x1': 155, 'x2': 291}]`
- `x2_sq_lt_x0_x1` universal=`False` fails=`[{'n': 37, 'x0': 37, 'x1': 9317, 'x2': 2233}]`
- `x2_lt_x1` universal=`False` fails=`[{'n': 89, 'x0': 89, 'x1': 155, 'x2': 291}]`
- `x2_x0_lt_x1_x0_plus_x1` universal=`False` fails=`[{'n': 501, 'x0': 501, 'x1': 1089, 'x2': 133347}]`

## Existing Lean (unchanged)

- `AboveAnchor`: `True`
- `EnvelopeState`: `True`
- `oe_block_contracts`: `True`
- `isolatedOddSurvival_bound`: `True`
- `finiteProgress_of_ooe_oe`: `True`
- new Lean file: `False`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- new_episode_law: `False`
- macro_automaton: `False`
- source_descent: `False`
- q_reopen: `False`

## Decision

**MACRO_EVENT_CLOSED**

episodes are Q-blocks; 3375 is interior; no named triple law survives; long runs can follow long runs.

