# Lychrel / Reverse-and-Add dynamics

Status: **EXPLORATORY**

This is **problem registration and attack-surface characterization only**.
It does **not** launch a research attack, thaw `DEFAULT_ATTACK_ORDER`, or
reopen the closed campaign [`reverse_and_add_base3.md`](reverse_and_add_base3.md).

The closed campaign studies \(T(n)=n+W(n)\) with canonical balanced-ternary
reverse \(W\). Seed 196 is reverse-fixed there (\(W(196)=196\),
\(T(196)=392\)) and reaches 0 in eight steps. Unsigned decimal
\(R_{10}(196)=196+691=887\) is a different map.

## Problem

Lychrel / Reverse-and-Add dynamics: whether repeated
\(R_b(n)=n+\operatorname{rev}_b(n)\) always reaches a base-\(b\) palindrome.

## Exact statement

Let \(b\ge 2\) be an integer. Write \(\operatorname{rev}_b(n)\) for the
integer obtained by reversing the ordinary unsigned base-\(b\) digits of
the positive integer \(n\) (no leading zeros except for \(n=0\)). Define

\[
R_b(n)=n+\operatorname{rev}_b(n).
\]

**Canonical instance \(b=10\).** Does there exist \(n>0\) such that the
trajectory \(n,\,R_{10}(n),\,R_{10}^2(n),\ldots\) never reaches a
palindrome?

**Secondary instance \(b=3\).** The same question in unsigned ternary.
OEIS A077408 records 103 as a historically noted candidate; that is
computational context, not a theorem.

**Optional signed / balanced digits.** An exploratory representation
branch, not a claim that balanced ternary solves the problem, and not a
transfer theorem from unsigned bases.

Do not assume that a result for one base transfers automatically to
another.

Allowed research dimensions, none executed here: arbitrary integer
\(b\ge 2\); unsigned digits; optional signed/balanced digits;
trajectory-level properties; finite-prefix reachability; palindrome
reachability; candidate non-termination; residual-state equivalence;
transducer representations.

Evidence hygiene:

```text
known computational evidence
≠
mathematical proof
≠
conjectural status
```

This distinction applies to decimal 196, ternary 103, and any future
computational observation.

## Current literature

Project relationship: **known**. No new number-theory theorem is claimed.
No project conjecture is opened.

- OEIS A023108 (`oeis-A023108`): positive integers that apparently never
  result in a palindrome under \(A056964(x)=x+(x\text{ with digits reversed})\).
  196 is listed first and is conjectured there to be the smallest such
  seed. **KNOWN** computational candidate list; not a proof that any
  listed term is Lychrel.
- OEIS A006960 (`oeis-A006960`): Reverse-and-Add trajectory of 196.
  **KNOWN** computational sequence.
- OEIS A056964 (`oeis-A056964`): the one-step reverse-then-add map.
  **KNOWN** definition.
- OEIS A060382 (`oeis-A060382`): smallest possible Lychrel candidate in
  each base. Base 3 is recorded as 103 (written \(10211_3\)). **KNOWN**
  computational table.
- OEIS A077408 (`oeis-A077408`): base-3 trajectory of 103, written in
  base 10. Comments conjecture that 103 is the smallest such seed and
  state that the palindrome-free method used for some base-2 and base-4
  trajectories is **not applicable**. **KNOWN** computational context;
  not a proof that 103 never palindromizes.
- Weisstein, 196-Algorithm (`weisstein-196-algorithm`): reverse-then-add
  until a palindrome; 196 is the smallest number not known to produce
  one. **KNOWN**.
- Prosper–Veigneau, *On the palindromic reversal process*, CALCOLO 38
  (2001) (`prosper-veigneau-2001-palindromic-reversal`): scholarly
  treatment of the palindromic reversal process. **KNOWN**. Cited as
  prior theoretical work; this registration does not claim to extend it.

Closed laboratory campaign `reverse_and_add_base3` (`oeis-A134028` for
\(W\)): related representation, **not** this problem. Phase-9 excluded
reopening it.

Novelty review of automata / transducer formulations, of any exact
invariant we might later propose, and of further ternary / balanced-digit
work is **mandatory and not complete**. Prior-art ids on this dossier are
recorded; that does not finish the review.

## Branch budget

```text
Mathematical target     Register R_b(n)=n+rev_b(n) as a pipeline candidate:
                        palindrome reachability in base 10, with explicit
                        base-b / base-3 / exploratory BT dimensions.
Novelty hypothesis      A digit-transducer / residual / PalReach formulation
                        might be new relative to computational Lychrel lore.
Falsifier               Rediscovery of a known transducer/invariant billed as
                        new math; conflation with reverse_and_add_base3;
                        computational 196/103 status billed as a theorem.
Existing machinery      bt.transducers, bt.operators reverse, engine
                        residual/separation/quotient/closure, Lean ReverseAdd
                        (BT map, not this problem).
Maximum Phase-0 scope   Dossier + thin ProblemDefinition + pipeline record +
                        non-executable attack-family metadata + literature
                        ids + tests. No runner, adapter, Lean, or attack.
Promotion criterion     Not this phase. Novelty review must complete before
                        any selection-to-execution promotion.
Stop criterion          Any attack execution; DEFAULT_ATTACK_ORDER change;
                        reopening reverse_and_add_base3; project conjecture
                        restating the literature-open question.
```

## Balanced-ternary formulation

Exploratory only. Questions to expose later, not claimed:

1. Does balanced ternary reduce carry-state complexity?
2. Does canonical normalization produce a smaller transducer?
3. Are residual states easier to distinguish?
4. Does reversal interact naturally with balanced normalization?
5. Are there invariants invisible in ordinary unsigned ternary?
6. Can existing BT differential / operator machinery contribute structure?

The immediate purpose is representation research. Canonical unsigned
base \(b\) remains the primary object. Do not identify this branch with
\(T(n)=n+W(n)\).

## Why BT may be relevant

Signed digits \(\{-1,0,1\}\) with canonical normalization may change
carry alphabets and residual distinguishability. That is a
representation hypothesis, not a solving claim.

## Candidate operations / invariants

None executed. Labels below are registration of intended attack
surfaces, not theorems.

- \(R_b(n)=n+\operatorname{rev}_b(n)\) — **KNOWN** (definition; A056964
  for \(b=10\)).
- Digit transducer \((d_i,d_{k-i},c_i)\mapsto(d'_i,c_{i+1})\) or an
  equivalent local step — **proposed family** `digit_transducer`. Not a
  theorem that a bounded carry alphabet exists.
- Residual-state collapse of prefixes — **proposed family**
  `residual_state_analysis`. Reuse the existing residual / Mealy
  quotient unless that abstraction is inapplicable.
- Palindrome separation
  \(q_1\not\equiv q_2\iff\exists w.\;\operatorname{PalReach}(q_1,w)\ne\operatorname{PalReach}(q_2,w)\)
  — **proposed family** `palindrome_separation`. Smallest exact
  definition later; this formula is not assumed final.
- Forbidden digit/carry patterns, distinguishing syntactic, locally
  valid, globally realizable, and origin-live words — **proposed family**
  `forbidden_pattern_search`.
- Exact or eventually contracting potentials (length, ends, carry
  profile, digit sums, symmetric differences, residual state) —
  **proposed family** `potential_energy`. Heuristics are not proved
  invariants. Do not assume monotone decrease.

196 and 103 are **literature computational candidates**, not
**EXACT** statements of this project.

## Experiments

None. There is no runner, adapter, spec, or scout. Candidate attack
families live in `research.lychrel_dynamics.attack_families` and are
not in `DEFAULT_ATTACK_ORDER`.

## Conjectures

None opened. The decimal Lychrel existence question remains
literature-open and is not restated as a project conjecture.

## Counterexamples

- “This problem is the closed campaign `reverse_and_add_base3`.”
  **REFUTED** as identification: \(W\) is canonical balanced-ternary
  reverse; \(R_b\) is unsigned base-\(b\) reverse. Seed 196 is
  reverse-fixed for \(W\) and a Lychrel *candidate* for \(R_{10}\).
- “196 is a proved Lychrel number.” **Not claimed.** A023108 lists it
  as apparently never palindromizing; that is not a proof.
- “103 is a proved base-3 Lychrel number.” **Not claimed.** A077408 is
  computational context and notes that a known palindrome-free method
  does not apply.

## Formalization

None exist yet. No `sorry`. Do not reuse
`formal/Problems/Engine/ReverseAdd.lean` as unsigned Lychrel.

Prospective objects for a later milestone of executable definitions and
elementary correctness lemmas, **not** the conjecture:

`DigitBase`, `Digits`, `Reverse`, `ReverseAdd`, `Palindrome`,
`Trajectory`, `ResidualState`, `Transition`, `Reachable`, `PalReach`.

Preferred first lemmas:

\[
\operatorname{eval}(\operatorname{Reverse}(d))
=
\operatorname{rev}_b(\operatorname{eval}(d))
\]

and exact correspondence between a digit-level transducer and the
integer map \(R_b\).

## Results

Registration only.

```text
Problem registered: YES
Attack executed: NO
DEFAULT_ATTACK_ORDER changed: NO
New attack family registered: YES
Novelty review required: YES
```

“New attack family registered: YES” means candidate metadata
(`digit_transducer`, `residual_state_analysis`,
`palindrome_separation`, `forbidden_pattern_search`,
`potential_energy`), not a production or flood-order attack.

Qualitative selection labels, not a numeric score:

```text
new_math_probability: high
frontier_strength: high
Lean_path: high
cost: medium/high
novelty_risk: very high
```

Intended consequence: a serious candidate that must not automatically
outrank targets with substantially lower novelty risk.

## Open questions

Does there exist a positive integer whose base-10 Reverse-and-Add
trajectory never reaches a palindrome? The analogous question for
unsigned base 3, and whether a balanced-ternary representation changes
transducer or residual complexity, remain unattacked. Complete the
novelty-review searches before any attack.

## Decision

**PARK**. The family is registered as a pipeline candidate with explicit
base-\(b\) scope, a base-3 instance, an exploratory balanced-ternary
branch, five non-executable attack families, Lean-facing names, and a
mandatory novelty gate. Novelty risk is very high. Do not execute. Do
not thaw `DEFAULT_ATTACK_ORDER`. Do not reopen
`reverse_and_add_base3`. Do not open a project conjecture that restates
the literature question.

Best next question: complete the novelty-review searches (exact
transducer/invariant prior art, automata formulations, remaining
generalized-base and balanced-digit literature) before any promotion
from selection to execution.

## Publication assessment

Status: `EXPLORATORY`. Registration intelligence, not a paper candidate.
