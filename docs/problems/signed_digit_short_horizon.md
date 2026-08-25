# Signed-digit short-horizon controls

Status: **STRUCTURAL**

When the arithmetic needs `v_3(s-t)+1` observations to separate two
residuals, can a finite control language of strictly shorter words make
those residuals genuinely equivalent?

CLI `btlab research analyze signed_digit_short_horizon` (aliases `sdsh`,
`sdr_horizon`). Reuses `signed_step`, `ControlAutomaton`, and
`mealy_partition`. It does not reopen the finite/infinite law, the
unconstrained any-word theorem, Collatz, primes, T/jets, or Ostrowski.

## Problem

Replace unconstrained future controls by a remaining-horizon automaton
and decide whether distinct residuals at the same control state can
become observationally equivalent.

## Exact statement

**Semantics.** Two product states at the same control state `q` are
equivalent when their maps on maximal legal words agree, including
termination (`O_{s,q}=O_{t,q}`). Horizon 0 is deadlock: the only legal
word is empty, and every residual pair is equivalent. That case is
recorded and is not counted as a genuine residual merge.

If `3^L∣s-t` and `|w|≤L`, the `lsd` streams agree on `w`
(`truncated_3adic_equiv`). If `3∤λ`, `s≠t`, and `|w|≥v_3(s-t)+1`, every
such word separates (`short_horizon_separation`). Therefore, for a
remaining-horizon controller and `3∤λ`,

```text
(s,q_L) ∼ (t,q_L)  ⟺  3^L ∣ s-t.
```

The smallest genuine merge is `(0,q_1)∼(3,q_1)`: every length-1 word
agrees, then both terminate. The unconstrained separator of length 2 is
illegal because the horizon has expired.

At `λ=3`, finite horizon cannot destroy translation `s↦s+3k`. For
`L≥1` it creates no additional residual classes: first outputs already
separate whenever `3∤s-t`. Horizon 0 still collapses everything by
deadlock.

## Current literature

- Mealy/Nerode equivalence and finite-language transducers are `KNOWN`.
- Anashin-style `p`-adic automaton functions are `KNOWN` and answer
  finiteness of the automaton, not residual distinguishability of this
  map under a finite admissible language.
- Carry-transducer minimization is `KNOWN`.
- The truncated-congruence characterization for `F_{λ,U}` is
  `NEW FORMULATION` of the previous 3-adic rigidity theorem: arithmetic
  supplies the observation depth, the control language supplies access.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

- **Target:** whether a control language of max length `<v_3(s-t)+1`
  can make `s≠t` equivalent at the same `q`.
- **Novelty hypothesis:** `(s,q_L)∼(t,q_L)` iff `3^L∣s-t`; `L=0` is
  deadlock, `L≥1` is a genuine truncated 3-adic merge.
- **Falsifier:** a pair with `v_3≥L≥1` that still separates on some
  legal word, or a pair with `v_3<L` that merges.
- **Existing machinery:** `signed_step`, `val3`, `any_word_separation`,
  `ControlAutomaton`, `mealy_partition`.
- **Maximum Phase-0 scope:** Models S1–S3 on `(0,3)`, `(0,9)`, `(0,27)`;
  Lean truncated congruence and long-word separation; one `λ=3` check.
- **Promotion criterion:** exact characterization of residual merge
  under finite horizon, or a smallest genuine merge with an arithmetic
  explanation.
- **Stop criterion:** only `L=0` deadlock, or no arithmetic explanation.

## Balanced-ternary formulation

Product state `(s,q_L)`. Residual step `s'=λ D(s+u)`, control step
`q_L↦q_{L-1}`, output `lsd(s+u)`. From `q_0` there is no legal letter.

## Why BT may be relevant

The gap drop `F(s,u)-F(t,u)=λ(s-t)/3` is independent of the letter.
Horizon only decides whether `v_3(s-t)+1` steps are available.

## Candidate operations / invariants

- Traces of length `≤L` agree whenever `3^L∣s-t`. **EXACT — LEAN VERIFIED**
- If `3∤λ` and `|w|≥v_3(s-t)+1`, every such word separates. **EXACT — LEAN VERIFIED**
- Some shorter legal word always separates (H2). **REFUTED** (`0` vs `3` at `L=1`)
- Finite horizon merges only by deadlock (H3). **REFUTED** (same pair takes one legal step)
- Origin-reachable `U_2` product merges distinct residuals at positive remaining horizon. **REFUTED** (only `q_0` deadlock)
- `λ=3` and `L≥1` create residual classes beyond `s≡t (mod 3)`. **REFUTED**

## Experiments

- `btlab research analyze|attack|reproduce|report signed_digit_short_horizon`
- Discovery: `src/research/signed_digit_short_horizon/discovery.py`
- Tests: `tests/research/signed_digit_short_horizon/test_signed_digit_short_horizon.py`
- Records in `experiments/balanced_ternary/signed_digit_short_horizon/`

| pair | `v_3` | `k` | `L<k` | `L=k` |
|------|-------|-----|-------|-------|
| `0` vs `3` | 1 | 2 | merge at `L=1` | separates |
| `0` vs `9` | 2 | 3 | merge at `L=1,2` | separates |
| `0` vs `27` | 3 | 4 | merge at `L=1,2,3` | separates |

Model S2 (branching `U_1`) is the same complete tree as S1 with `|U|>1`.
Model S3 (asymmetric first letter) still obeys the local truncation at
each remaining depth: `(0,1)∼(3,1)` and `(0,2)≁(3,2)`.

Origin-reachable `F_{1,U_2}` with horizon 2 has 7 product states.
Distinct reachable residuals have `v_3=0`, so the only same-`q` merge
in that product is deadlock at remaining 0.

## Conjectures

None opened.

## Counterexamples

- H2: `0` vs `3` at horizon 1, alphabet `U_1`, gain 1. Every legal word
  has length 1 and identical output; unconstrained separator `(u,u)` is
  illegal.
- H3: the same pair takes one legal step before terminating.
- `λ=3` extra classes at `L≥1`: none on the listed probes.

## Formalization

`formal/Problems/BalancedTernary/SignedDigitShortHorizon.lean`.
Theorems `truncated_3adic_equiv`, `short_horizon_equiv`,
`short_horizon_separation`, `control_language_separation`,
`lambda3_short_horizon_symmetry`. Reuses `signedTrace`, `intVal3`,
`any_word_separation`. No `sorry`.

## Results

3-adic arithmetic determines the minimum information depth
`v_3(s-t)+1`. The control language determines whether that depth is
accessible. If it is not, and the remaining language is a complete
tree of depth `L≥1`, distinct residuals merge exactly on the truncated
congruence `s≡t (mod 3^L)`. Deadlock `L=0` is the empty-language
artifact of the same formula (`3^0=1`).

## Open questions

None opened as conjectures.

## Decision

`PROMOTE` the truncated-congruence theorem. Finite horizon creates
genuine residual merges, and they are exactly the 3-adic truncations.
Avižienis, Anashin, and finite-language Nerode equivalence remain
`KNOWN` and answer different questions.

Best next question: if the admissible language from `q` is a proper
subset of the complete tree of depth `L`, can two residuals with
`v_3(s-t)<L` still merge because the separating words are missing, or
does every nonempty language of length `≥v_3(s-t)+1` already separate?

## Publication assessment

Status: `STRUCTURAL`. An exact characterization exists. Not a
`PAPER_CANDIDATE`: it is the missing converse of the previous rigidity
theorem, not a new residual calculus.
