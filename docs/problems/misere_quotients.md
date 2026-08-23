# Finite-context signatures and misere quotients

## Problem

Whether the laboratory’s finite-context behavioural-state methodology
can discover or certify structure in misere quotients that is not
already given by the classical Plambeck–Siegel construction.

## Exact statement

Fix an impartial heap game and a closed position algebra `A`. Contextual
indistinguishability is

`G ≡ H  ⇔  o^-(G+X) = o^-(H+X)  for every X ∈ A`,

where `o^-` is the misere outcome. The relation is a congruence under
disjunctive sum. The quotient `Q = A/≡` is a commutative monoid with a
distinguished losing set `P`.

For a finite context set `C ⊆ A` define the finite signature

`Σ_C(G) = (o^-(G+X))_{X ∈ C}`.

Equality of signatures is `FINITE-CONTEXT EQUIVALENCE`. It is strictly
weaker than `TRUE MISÈRE QUOTIENT EQUIVALENCE` unless `C` contains a
complete set of distinguishing contexts.

Question: does finite-context refinement, minimal distinguishing
contexts, or candidate-monoid audit produce a new exact construction,
a finite-context completeness theorem for a meaningful class, or a
rigorous reduction of an existing open problem such as

`is Q_34(0.07) infinite?`

Here `Q_n` is the quotient of all sums of heaps whose *individual*
sizes are at most `n`. The question is not the outcome of the single
heap `H_34`, nor the normal-play period 34.

## Current literature

The construction and its algorithms are `KNOWN`.

- `plambeck-2005-taming-the-wild`: indistinguishability congruence;
  complete 20-element presentation of octal `0.123`
  `⟨x,z,a,b | x²=a²=1, z⁴=z², b⁴=b², abz=b, b³x=b², z³a=z²⟩` with
  `P = {x, xa, b², z², zb}` and pretending function of preperiod 5,
  period 5. `KNOWN`.
- `plambeck-siegel-2008-misere-quotients`: partial quotients `Q_n`,
  Guy–Smith–Plambeck periodicity, transition algebras, mex functions,
  MisereSolver. `|Q_33(0.07)| = 638`, `|P_33| = 109`; whether `Q_34`
  is infinite is stated as open. `KNOWN`.
- `plambeck-siegel-2007-supplement`: verification / least-failure /
  recalibration loop; reducedness means every distinct pair has a
  distinguishing context `z` with exactly one of `xz, yz` in `P`.
  `KNOWN`.
- `siegel-2007-structure-classification`: even order of finite
  nontrivial quotients; no order 4; uniqueness of orders 1, 2, 6, 8;
  `T_n` / `R_n` classification for `|P|=2`; valid transition tables.
  `KNOWN`.
- `nowakowski-unsolved-cgt`: the heap-34 question; Rédei’s theorem
  (a finitely generated commutative monoid is finitely presented);
  distinguish Dawson’s Chess `·137` from Dawson’s Kayles `·07`. The
  historical `miseregames.org` Q33 heading “Complete Solution is
  Known” is a template artefact (blank period / preperiod) and is not
  a proof that the full quotient is finite. `KNOWN`.

Finite-context signatures are the definition of `≡` restricted to a
finite list of tests. Distinguishing contexts are the reducedness
witnesses of a bipartite monoid. Candidate verification is the first
step of MisereSolver. No source located in the gate states this
project’s `Σ_C` notation. New notation for a standard restriction is
not evidence of novelty.

## Branch budget

```text
Mathematical target     Can finite-context signatures yield a new certificate or structural reduction for a concrete misere quotient, beyond established quotient algorithms?
Novelty hypothesis      Minimal distinguishing-context data or a bounded-context completeness criterion may expose structure not represented in pretending-function / transition-algebra computations.
Falsifier               Known algorithms already compute the same refinement and witnesses, and the Dawson’s Kayles reproduction yields only previously known tables without a rigorous reduction.
Existing machinery      Laboratory signature / witness / partition discipline; no BT arithmetic is used.
Maximum Phase-0 scope   Literature gate, one known finite quotient (0.123), one exact refinement experiment, and one bounded Dawson’s Kayles reproduction that stops before unrestricted Q_34 recalibration.
Promotion criterion     A new exact quotient method, finite-context theorem, structural theorem, or rigorous open-problem reduction (P1–P4). Faster code or recovered known tables do not promote.
Stop criterion          CLOSE if the transfer is reparameterization / tooling only; PARK only if one precise plausible theorem remains and Phase 0 cannot decide it.
```

## Balanced-ternary formulation

None. Positions are sorted heap tuples, for example `(1,1,3,5,5)`.
Outcomes are the classical pair `{P, N}`. A ternary outcome alphabet
is not imposed. The empty position and every other terminal position
are `N`: the player to move cannot move, so the previous player made
the last legal move and loses.

## Why BT may be relevant

It is not relevant as arithmetic. The only transferred object is the
laboratory pattern

```text
BT:      residual → finite-horizon signature → distinguishing witness → behavioural quotient
misere:  position → finite-context signature  → distinguishing context → misere quotient
```

The structures are not identical. Residual `≡_r` is a finite-horizon
relation and is not a transition congruence (closed Černý gate).
Misere `≡` is already a congruence under addition. That is why this
branch is a better methodological test than the Černý branch, and
also why a positive transfer is harder: the native congruence is
already the classical one.

## Candidate operations / invariants

- True misere quotient `≡` — **KNOWN**.
- Finite-context equivalence `Σ_C` — **REPARAMETERIZATION** of
  indistinguishability restricted to `C`.
- Minimal distinguishing context, metric = total heap size, then heap
  count, then the tuple — **REPARAMETERIZATION** of reducedness
  witnesses; the size order is **PROJECT-SPECIFIC**.
- Context-refinement traces `#classes` versus `|C|` — **PROJECT-SPECIFIC**
  census, not a construction of `Q`.
- Candidate monoid audit (closure, well-defined products, identity,
  unresolved pairs) — **REPARAMETERIZATION** of the first verification
  step of MisereSolver.
- Sprague–Grundy nimbers — **KNOWN**; finite-context refinement does
  not recover them. Mex recursion is a different algorithm.
- `Q_n(0.07)` orders `24,144,176,360,520,552,638` at heap bounds
  `24,26,29,30,31,32,33` — **KNOWN**. Finite-context class counts on a
  bounded-multiplicity slice are not these numbers.

## Experiments

`research.misere_quotients.triage` implements only the gate:

- exact options for `0.123` (Plambeck’s three taking rules) and
  `0.07` (remove two adjacent counters);
- memoized misere recursion with terminals classified `N`;
- `context_signature`, `distinguish`, `refine_partition`,
  `candidate_quotient`;
- the published 20-element `0.123` table as an oracle;
- single-heap outcomes of `0.07` through heap 33 against the published
  Q33 pretending-function P-membership;
- a finite-context growth slice for `0.07` with heap size `≤ 8`, at
  most 4 heaps, total size `≤ 16`.

Phase-0 universe for `0.123`: 2116 positions with each heap `≤ 16`,
at most 5 heaps, total size `≤ 24`. Contexts of total size `≤ 12`
number 197.

No CLI, visualization, Lean module, generic game framework, or
MisereSolver reimplementation was added. `Q_34` recalibration was not
attempted. Timeout or class growth is not evidence of infinity.

## Conjectures

None registered. Recovering a known finite quotient is not a
conjecture. The heap-34 question remains the literature’s `OPEN`
problem and is not claimed here.

## Counterexamples

1. **Finite-context equivalence is not the true quotient.** On the
   `0.123` universe, the empty context yields 2 classes (raw outcomes).
   Single-heap contexts yield 11 classes. Contexts of total size `≤ 12`
   yield 20 classes, matching the published monoid on that universe.
   The 11-class table is a proper coarsening of `Q`. This is the
   expected incompleteness of a short context list, not a new
   obstruction.

2. **A finite universe is not additively closed.** The candidate
   20-element multiplication is well-defined on every represented
   product (`0` ill-defined products, `30933` represented checks), but
   `4446523` pairs leave the 2116-element slice. Stability on a slice
   is `COMPUTATIONALLY STABLE THROUGH N`, not a quotient theorem.

3. **Finite-context class counts are not `|Q_n|`.** On the Dawson
   slice the refinement trace ends at 6 classes. The published
   `|Q_24(0.07)|` is already 24. The slice does not contain the
   algebra `A_24`.

The witnesses are regression-tested in
`tests/research/misere_quotients/test_triage.py`.

## Formalization

None. No `sorry`. Lean is not opened on a closed literature-and-reproduction
gate. Hypothetical later objects (`Position`, `Context`, `MisereOutcome`,
`QuotientClass`) were not implemented.

## Results

### Known-game validation (`0.123`)

`COMPUTATIONALLY VERIFIED` on the stated slice; the quotient itself
is `KNOWN`.

- The published table satisfies the six relations, commutativity, and
  identity; `|Q|=20`, `|P|=5`.
- Exact misere outcomes agree with membership of `Φ(G)` in `P` on all
  2116 positions.
- Context refinement class counts: `2,3,3,4,5,10,15,20` at context
  totals `0,1,2,3,4,6,8,12`.
- All 20 published elements occur; every distinct pair among the 20
  recovered classes has a distinguishing context in the 197-element
  list (`190` witnesses, `0` missing).
- Represented products match the published multiplication
  (`0` mismatches).

This is exact reproduction of Plambeck’s Theorem 1 on a finite slice,
not an independent construction of the quotient.

### Open-problem reproduction (`0.07`)

`COMPUTATIONALLY VERIFIED` for single-heap outcomes through heap 33;
the partial-quotient orders remain `KNOWN` and were not recomputed.

- Single-heap P-positions:
  `2,3,7,8,12,16,17,21,22,26,30,31`.
  These agree with P-membership of the published Q33 pretending
  labels.
- Finite-context trace on the multiplicity-bounded slice:
  `2,3,4,4,6` classes at context totals `0,2,4,6,8`.
- Published checkpoints
  `|Q_n| ∈ {24,144,176,360,520,552,638}` at
  `n ∈ {24,26,29,30,31,32,33}` were recorded, not reproduced as
  monoids.
- `Q_34` was not opened. No nontermination, growth trace, or resource
  bound is reported as evidence of infinity.

### Method transfer

What carries: the *discipline* of naming an observable, hashing a
finite signature, searching a shortest witness, and refusing to call
a stable table a theorem.

What does not carry: residual arithmetic, trit words, `≡_r`, Newton
residues, or any balanced-ternary encoding of heaps.

The correspondence “BT future behaviour ↔ game behaviour under
contexts” is accurate as methodology and empty as mathematics: the
right-hand side is already the definition of the misere quotient.

### Literature classification

- `KNOWN`: misere quotients, reduced bipartite monoids, transition
  algebras, MisereSolver, the `0.123` presentation, `Q_33(0.07)`,
  the heap-34 question, finite-quotient classification facts.
- `REPARAMETERIZATION`: `Σ_C`, distinguishing-context search, and
  candidate-monoid audit as the classical congruence, reducedness
  witnesses, and verification loop.
- `PROJECT-SPECIFIC`: the exact `0.123` refinement trace, the 2116 /
  197 census, the Dawson single-heap P-list check, and the explicit
  refusal of `Q_34`.
- `OPEN`: none promoted. `Q_34(0.07)` remains the literature’s open
  problem and is not a laboratory conjecture.

### Gate verdict

`CLOSE`

Finite-context refinement recovered a known finite quotient exactly
when the context list became rich enough to contain reducedness
witnesses, and recovered only previously published single-heap
outcomes for Dawson’s Kayles. That is the falsifier.

## Open questions

None retained on this branch. In particular:

- a finite-context completeness theorem for a class of games is the
  classical statement that a finite reduced quotient is separated by
  its own elements;
- synchronization-style or BT-residual encodings of heaps are not
  opened;
- `Q_34(0.07)` is not reopened here.

## Decision

`CLOSE — REPARAMETERIZATION / TOOLING ONLY`. The surviving statements
are the classical indistinguishability congruence, Plambeck’s
20-element quotient of `0.123`, and the published Dawson’s Kayles
checkpoint. Finite-context signatures are that congruence evaluated
on a finite list. The open-problem experiment produced a single-heap
outcome table that agrees with known Φ-labels and a slice whose class
counts are not `|Q_n|`. No P1–P4 promotion criterion survived.
Faster implementation or recovered known tables do not promote.

Best next question: none; the branch is not promoted.

## Publication assessment

Status: `ARCHIVED`.

The branch records a precise negative methodological gate and a
reusable exact checker for two octal rulesets. It contains no new
theorem and no literature-separated computational result.
