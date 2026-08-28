# Juggler minimal-bad survival signatures

Status: **MINIMAL_SURVIVAL_COMPLEX**

Standalone Phase-0 on whether minimality plus exact inverse
arithmetic yields a new constraint on a least bad state. This is not
a termination theorem. The closed well-ordering and stopping-prefix
branches stay closed.

Every statement below is labelled
`LOGICAL CONSEQUENCE` | `LEAN-CERTIFIED` | `EXACT COMPUTATION` |
`COMPUTATIONALLY OBSERVED` | `COUNTEREXAMPLE`.
These are report labels. Ledger tags, when used, remain the seven
standard tags from [docs/README.md](../README.md).

## 1. Already-proved framework

`Good` is `ReachesOne`. `MinimalNonTerm n` is a least bad state.
Label: **LEAN-CERTIFIED**. **KNOWN**.

If `Good m` and `T^k(n)=m` then `Good n`. Label: **LEAN-CERTIFIED**
(`reachesOne_of_iterate`, `good_of_predecessor_certificate`).
**KNOWN**.

`PredClosure` from `{1}` is `ReachesOne`. Label: **LEAN-CERTIFIED**
(`predClosure_iff_reachesOne`). **REPARAMETERIZATION**.

The even map is `T(n)=⌊√n⌋`, not `T(2k)=k^2`. For `n≥2` even,
`T(n)<n`. Label: **LEAN-CERTIFIED**. The informal half-square rule is
discarded.

## 2. SurvivalSignature

On `2≤n≤4000`:

| bucket | count |
| --- | --- |
| one_step | 2000 |
| two_step | 990 |
| leftover | 1009 |

Two-letter counts `{'EO': 977, 'OO': 1009, 'EE': 1023, 'OE': 990}`. Every even is
one-step covered: `True`. No odd is
one-step covered: `True`. Leftover equals
odd-to-odd: `True`. Label:
**EXACT COMPUTATION**. This is `finiteProgress_of_not_odd_odd` /
`unresolved_is_odd_odd`. **KNOWN**.

One-step inverse from a smaller target never hits an odd `n≥3`
(`odd_not_pred_of_le`, `minimal_bad_uncovered_one_step`). Label:
**LEAN-CERTIFIED**.

## 3. Inverse generation is first descent

A smaller `m` generates `n` by exact inverse steps if and only if
some forward iterate equals `m`. For certificates from
`[1,n-1]` that is `T^k(n)<n`. Label: **LOGICAL CONSEQUENCE**.
**REPARAMETERIZATION** of first descent.

Leftover starts in the window that drop below the start:
`1009` of `1009`
(`True`). Sample:

| n | word2 | H_n | dropped |
| --- | --- | --- | --- |
| 3 | OO | 5 | True |
| 5 | OO | 4 | True |
| 9 | OO | 5 | True |
| 25 | OO | 5 | True |
| 33 | OO | 4 | True |
| 35 | OO | 4 | True |
| 37 | OO | 15 | True |
| 39 | OO | 5 | True |
| 43 | OO | 4 | True |
| 45 | OO | 4 | True |
| 49 | OO | 5 | True |
| 53 | OO | 4 | True |

Label: **EXACT COMPUTATION**. That every tested `n` eventually
decreases is the closed-branch window fact, not a new obstruction.
It is stop condition 1 of this attack.

## 4. Residues

Leftover residues mod 8: `{'1': 278, '3': 229, '5': 280, '7': 222}`.
Mod 16: `{'1': 131, '3': 111, '5': 140, '7': 113, '9': 147, '11': 118, '13': 140, '15': 109}`. More than one class occurs.
No single modulus is forced by the leftover. Label:
**COMPUTATIONALLY OBSERVED**. Arbitrary further moduli are not
introduced.

## 5. Novelty

| statement | novelty |
| --- | --- |
| MinimalNonTerm | KNOWN |
| good_of_iterate | KNOWN |
| even_one_step | KNOWN |
| odd_never_one_step | KNOWN |
| leftover_is_odd_odd | KNOWN |
| PredClosure_iff_ReachesOne | REPARAMETERIZATION |
| inverse_generation_is_first_descent | REPARAMETERIZATION |
| new_Phi | REFUTED |

`SURVIVAL_CONSTRAINT_GREEN` is not awarded. There is no new `Φ(n)`
beyond “odd-to-odd and the orbit never drops below `n`”, which is
already `minimal_counterexample_normal_form`. Label:
**COUNTEREXAMPLE** to “minimality plus inverse arithmetic is a new
mechanism”.

## 6. Lean

Cited, not added:

- `MinimalNonTerm`, `minimal_nonterm_odd`, `minimal_nonterm_odd_image_odd`,
  `minimal_nonterm_iterate_ge`
- `UncoveredOneStep`, `odd_not_pred_of_le`, `predClosure_iff_reachesOne`
- `finiteProgress_of_not_odd_odd`, `unresolved_is_odd_odd`

Sorry-free: `True`. Not formalized, and not
claimed: `minimal_bad_impossible`, `predecessor_cover_complete`.

## 7. Decision

Classification: **MINIMAL_SURVIVAL_COMPLEX**.

SurvivalSignature leftover is exactly the odd-to-odd class (1009 starts on n≤4000). Every even is one-step covered; no odd n≥3 is. Inverse generation from a smaller state is first descent: every leftover start in the window drops below itself. Leftover residues mod 8 are [1, 3, 5, 7]. All of this is KNOWN (MinimalNonTerm, UncoveredOneStep, unresolved_is_odd_odd) or a REPARAMETERIZATION of descent. Minimality plus inverse arithmetic does not create a new Φ(n).

Branch status: **CLOSE**. Phase 1 is not launched. A larger
window only lengthens the leftover list of terminating odd-to-odd
starts.
