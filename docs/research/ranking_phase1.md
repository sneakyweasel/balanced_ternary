# Ranking-function Phase-1 enriched falsifier

Status: **PHASE_1_ENRICHED_RANKING_FALSIFIER**

This is not a ranking synthesizer and not a termination proof.
Phase 0 parked scalar one-step ranking. Phase 1 tests the three
named enrichments on the same frozen transition tables.

## Branch budget

```text
Mathematical target     Do the three Phase-0 enrichments survive exact
                        bounded falsification on their intended domains?
Novelty hypothesis      k=2 odd-even composition, reverse_gap, or
                        composite-versus-prime piecewise V_C might repair
                        the scalar obstruction without a general synthesizer.
Falsifier               Each named form fails on an exact transition in its
                        stated domain, without a shared next ranking language.
Existing machinery      Phase-0 grid; frozen windows/orbits; encode/bt_reverse;
                        factor_trial / concat_from_factors.
Maximum Phase-1 scope   k=2 only; reverse_gap L1 on canonical digits; V_C on
                        composite-to-composite; no grid enlargement.
Promotion criterion     A nontrivial bounded survivor on a stated domain,
                        not a restatement of an existing halt.
Stop criterion          k>2, 4D exhaustive search, new residual state,
                        thawing DEFAULT_ATTACK_ORDER, or a global theorem claim.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_1_ENRICHED_RANKING_FALSIFIER`
- family decision: **MIXED**
- decision reason: enriched ranking survives on a restricted domain but not as a uniform attack family
- formalization: `not_yet_formalization_ready`

## Target `juggler_sequence`

- Hypothesis: `odd_even_composed_ranking`
- Available features: log_bit, digit=bit_length, parity
- Candidate count: 145
- Survivor count: 72
- Transition depth: 2
- Domain: odd x with T(x) even and T^2(x) defined, on the frozen window/orbit
- Exceptional set: 1
- Transitions tested: 11
- Exactness: exact integer V(T(T(x)))<V(x); Phase-0 7^3 grid, no enlargement
- Classification: **COMPOSED_RANKING_PROMISING**
- Lean: `formalization_ready`
- Next proposal: `odd_odd_branch_composition`

### Survivors

- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 1, 'digit': 0, 'residue': 0}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 0, 'digit': 1, 'residue': 1}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 1, 'digit': 0, 'residue': 1}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 1, 'digit': 1, 'residue': 0}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 0, 'digit': 1, 'residue': 2}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 0, 'digit': 2, 'residue': 1}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 1, 'digit': 0, 'residue': 2}
- `a*log_bit + b*digit + c*parity on T^2` with {'log_bit': 1, 'digit': 2, 'residue': 0}

### Strongest candidate

`{'log_bit': 1, 'digit': 0, 'residue': 0, 'q': 0, 'form': 'a*log_bit + b*digit + c*parity on T^2'}`

### First counterexamples

- `{'log_bit': 1, 'digit': -1, 'residue': 1, 'q': 0, 'form': 'a*log_bit + b*digit + c*parity on T^2'}` fails at `15 -> 7` (FLOOR_EFFECT: V fails to decrease on this exact transition)
  source features `{'log_bit': 5, 'digit': 4, 'residue': 1, 'abs_value': 15}`; image features `{'log_bit': 4, 'digit': 3, 'residue': 1, 'abs_value': 7}`; V 2 -> 2
- `{'log_bit': 1, 'digit': 1, 'residue': -1, 'q': 0, 'form': 'a*log_bit + b*digit + c*parity on T^2'}` fails at `7 -> 4` (PARITY_COORDINATE: residue/parity changes without a compensating size drop)
  source features `{'log_bit': 4, 'digit': 3, 'residue': 1, 'abs_value': 7}`; image features `{'log_bit': 3, 'digit': 3, 'residue': 0, 'abs_value': 4}`; V 6 -> 6

### Failure mechanisms

- residue/parity changes without a compensating size drop
- V fails to decrease on this exact transition
- residue-only ranking cannot separate these states
- Domain: observed odd x with T(x) even and T(T(x)) defined. Depth k=2 only.
- Odd-to-odd one-step states such as 3->5 are outside this hypothesis.
- 9 observed odd-to-odd one-step transitions remain outside the composed domain.

## Target `reverse_and_add_base3`

- Hypothesis: `reverse_gap_or_palindrome_ranking`
- Available features: log_bit, digit=bt_length, parity, reverse_gap
- Candidate count: 43
- Survivor count: 0
- Transition depth: 1
- Domain: frozen reverse-add window/orbit; T(x)=x+bt_reverse(x)
- Exceptional set: 0
- Transitions tested: 48
- Exactness: exact integer V; reverse_gap is L1 of canonical MSD digits vs reverse
- Classification: **REVERSE_GAP_IMPLAUSIBLE**
- Lean: `not_yet_formalization_ready`
- Next proposal: `symbolic_nonlinear_composition`

### Survivors

None.

### Strongest candidate

None.

### First counterexamples

- `{'log_bit': 0, 'digit': 0, 'residue': 0, 'reverse_gap': 1, 'q': 0, 'form': 'a*log_bit + b*digit + c*parity + d*reverse_gap'}` fails at `1 -> 2` (PALINDROME_NOT_ATTRACTOR: a palindrome (reverse_gap=0) maps to a non-palindrome; palindromes are not an attractor)
  source features `{'log_bit': 2, 'digit': 1, 'residue': 1, 'abs_value': 1, 'reverse_gap': 0}`; image features `{'log_bit': 2, 'digit': 2, 'residue': 0, 'abs_value': 2, 'reverse_gap': 4}`; V 0 -> 4
- `{'log_bit': 1, 'digit': 0, 'residue': 0, 'reverse_gap': -3, 'q': 0, 'form': 'a*log_bit + b*digit + c*parity + d*reverse_gap'}` fails at `2 -> 0` (FEATURE_INSUFFICIENT: reverse_gap and the frozen scalar features do not strictly decrease)
  source features `{'log_bit': 2, 'digit': 2, 'residue': 0, 'abs_value': 2, 'reverse_gap': 4}`; image features `{'log_bit': 1, 'digit': 1, 'residue': 0, 'abs_value': 0, 'reverse_gap': 0}`; V -10 -> 1

### Failure mechanisms

- a palindrome (reverse_gap=0) maps to a non-palindrome; palindromes are not an attractor
- reverse_gap and the frozen scalar features do not strictly decrease
- reverse_gap is the L1 digit discrepancy between the canonical MSD word and its reverse.
- One-step V(T(x))<V(x) only. Scalar (a,b,c) held to a tiny Phase-0 basis; only d varies.
- Palindrome defect ranks toward palindromes, but reverse-plus-add sends palindromes away.

## Target `home_prime_49`

- Hypothesis: `composite_concat_piecewise_ranking`
- Available features: decimal_length, factor_count=Omega, omega=distinct primes
- Candidate count: 145
- Survivor count: 0
- Transition depth: 1
- Domain: composite x with composite T(x); primes are the terminal regime
- Exceptional set: (empty)
- Transitions tested: 28
- Exactness: exact integer V_C; features from existing factor_trial, no new factorization engine
- Classification: **PIECEWISE_RANKING_NEEDS_RICHER_STATE**
- Lean: `not_yet_formalization_ready`
- Next proposal: `concat_word_composition`

### Survivors

None.

### Strongest candidate

None.

### First counterexamples

- `{'digit': 1, 'factor_count': 1, 'omega': 1, 'q': 0, 'form': 'a*decimal_length + b*factor_count + c*omega'}` fails at `4 -> 22` (CONCAT_GROWTH: factor concatenation increases decimal length on a composite-to-composite step)
  source features `{'log_bit': 3, 'digit': 1, 'residue': 1, 'abs_value': 4, 'factor_count': 2, 'omega': 1}`; image features `{'log_bit': 5, 'digit': 2, 'residue': 2, 'abs_value': 22, 'factor_count': 2, 'omega': 2}`; V 4 -> 6
- `{'digit': 2, 'factor_count': 3, 'omega': -3, 'q': 0, 'form': 'a*decimal_length + b*factor_count + c*omega'}` fails at `10 -> 25` (FACTOR_NONDECREASE: factor_count does not decrease on this composite-to-composite concatenation)
  source features `{'log_bit': 4, 'digit': 2, 'residue': 2, 'abs_value': 10, 'factor_count': 2, 'omega': 2}`; image features `{'log_bit': 5, 'digit': 2, 'residue': 1, 'abs_value': 25, 'factor_count': 2, 'omega': 1}`; V 4 -> 7

### Failure mechanisms

- factor concatenation increases decimal length on a composite-to-composite step
- factor_count does not decrease on this composite-to-composite concatenation
- V_C is tested only on composite x with composite T(x).
- Composite-to-prime steps are terminal-region entries, not required decreases.
- Recorded terminal entries: 9.

## Cross-hypothesis comparison

| Target | Hypothesis | Survivors | First failure | Structural lesson | Classification |
| --- | --- | ---: | --- | --- | --- |
| Juggler | odd_even_composed_ranking | 72 | none on the stated domain | Odd-to-odd one-step states such as 3->5 are outside this hypothesis. | COMPOSED_RANKING_PROMISING |
| Reverse-add | reverse_gap_or_palindrome_ranking | 0 | 1 -> 2 | a palindrome (reverse_gap=0) maps to a non-palindrome; palindromes are not an attractor | REVERSE_GAP_IMPLAUSIBLE |
| Home Prime | composite_concat_piecewise_ranking | 0 | 4 -> 22 | factor concatenation increases decimal length on a composite-to-composite step | PIECEWISE_RANKING_NEEDS_RICHER_STATE |

## Decision

**MIXED**

enriched ranking survives on a restricted domain but not as a uniform attack family.

A bounded survivor is `BOUNDED_SURVIVOR`, not `GLOBAL_RANKING`.
Updated Top-3 proposals live in the machine-readable record and are not
executed. Frozen v2.3 campaign files are unchanged.

## Best next question

Should the surviving restricted ranking subfamily be specified as an attack, or should the failing targets move to symbolic composition first?
