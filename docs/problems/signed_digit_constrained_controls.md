# Signed-digit constrained controls

Status: **STRUCTURAL**

Does coprime-gain 3-adic residual rigidity survive when future controls
are a finite-state language rather than a free alphabet?

CLI `btlab research analyze signed_digit_constrained_controls` (aliases
`sdcc`, `sdr_constrained`). Reuses `signed_step` and `mealy_partition`.
It does not reopen the finite/infinite law, Collatz, primes, T/jets, or
Ostrowski.

## Problem

Replace unconstrained `u∈U` by a finite control automaton `(Q,δ,Legal)`
and decide whether distinct residuals at a reachable control state remain
observationally distinguishable.

## Exact statement

If `3∤λ` and `s≠t`, **every** word `w` of length `v_3(s-t)+1` satisfies

```text
signedTrace λ s w ≠ signedTrace λ t w.
```

A common cyclic letter is not required. Consequently, if a control
state `q` admits any legal word of that length, the product states
`(s,q)` and `(t,q)` are distinguishable. `L_sep` remains `v_3(s-t)+1`
along any common legal path; it is not inflated by a synchronization
diameter.

At `λ=3`, translation `s↦s+3k` still preserves every output stream, so
constraints cannot destroy that symmetry (they only thin the set of
words).

Control-state bisimulation can collapse `|Q|` without merging distinct
residuals: equal-parity Model D has `M=|R|<|R|·|Q|` with classes
`(s,0)∼(s,1)`.

## Current literature

- Carry transducers and unique balanced expansion are `KNOWN`.
- Constrained synchronization (reset words in a regular language;
  Fernau–Hoffmann et al.) is `KNOWN` and is a different question: this
  phase does not need a word that resets every control state.
- Heuberger–Prodinger regular-language carry analysis is `KNOWN`
  equidistribution, not residual distinguishability.
- The any-word 3-adic separation, and the split between residual
  rigidity and control bisimulation, is `NEW FORMULATION`.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

- **Target:** whether 3-adic rigidity survives a finite control language.
- **Novelty hypothesis:** the constant-word witness was stronger than
  needed; any word of critical length separates, so no-repeat and
  alternating controls stay residual-rigid.
- **Falsifier:** a Model A–D automaton that merges distinct residuals at
  one control state, or a legal word of length `v_3+1` that fails to
  separate.
- **Existing machinery:** `signed_step`, `mealy_partition`,
  `residual_separation`, `SignedDigitResidualSpec` pattern.
- **Maximum Phase-0 scope:** Models A–D; Lean of any-word separation;
  one `λ=3` symmetry check.
- **Promotion criterion:** a sufficient control-language condition, or
  a smallest residual merge with an arithmetic explanation.
- **Stop criterion:** only automata artifacts; or no interaction between
  3-adic dynamics and constraints.

## Balanced-ternary formulation

Product state `(s,q)`. Residual step `s'=λ D(s+u)`, control step
`q'=δ(q,u)`, output `lsd(s+u)`. Illegal letters are completed by a sink
for exact Mealy partition.

## Why BT may be relevant

The 3-adic drop of the residual gap is independent of the letter. The
control automaton only decides whether a word exists.

## Candidate operations / invariants

- Every word of length `v_3(s-t)+1` separates when `3∤λ`. **EXACT — LEAN VERIFIED**
- Rigidity requires a cyclic/constant letter. **REFUTED** (no-repeat)
- Some Model A–D merges distinct residuals at one `q`. **REFUTED**
- Equal-parity Model D collapses control states, not residuals. **COMPUTATIONALLY VERIFIED**
- `λ=3` translation survives every word. **EXACT — LEAN VERIFIED**

## Experiments

- `btlab research analyze|attack|reproduce|report signed_digit_constrained_controls`
- Discovery:
  `src/research/signed_digit_constrained_controls/discovery.py`
- Tests:
  `tests/research/signed_digit_constrained_controls/test_signed_digit_constrained_controls.py`
- Records in `experiments/balanced_ternary/signed_digit_constrained_controls/`

| model | `λ=1` product | `M` | residual merge |
|-------|---------------|-----|----------------|
| A periodic `{2}` | 2 | 2 | none |
| B alternating `{0,2}` | 3 | 3 | none |
| C no-repeat `U_2` | 10 | 10 | none |
| D unequal parity `{0,2}` vs `{1}` | 4 | 4 | none |
| D equal parity `U_2` | 6 | 3 | none; `(s,0)∼(s,1)` |

## Conjectures

None opened.

## Counterexamples

- Constant-word necessity: no-repeat on `U_2` forbids `uu` but `M=|R_full|=10`.
- Residual merge in A–D: none.
- Product `|R|·|Q|`: equal-parity Model D has `(s,0)∼(s,1)`.

## Formalization

`formal/Problems/BalancedTernary/SignedDigitConstrainedControls.lean`.
Theorems `any_word_separation`, `common_word_separation`,
`lambda3_constrained_symmetry`. Reuses `signedTrace`, `intVal3`. No
`sorry`.

## Results

Arithmetic rigidity is independent of the control language: every
sufficiently long common word separates. The control automaton
contributes only (i) existence of a word of that length from `q`, and
(ii) its own bisimulation quotient. Models A–D that admit infinite
legal paths from every reachable `q` have no residual merge.

The `(r,u)` output probe was not opened: legality is already visible in
the sink completion of the `lsd` machine.

## Open questions

Answered in
[signed_digit_short_horizon.md](signed_digit_short_horizon.md):
finite horizon `L<v_3(s-t)+1` creates genuine residual merges, exactly
when `3^L∣s-t`. Horizon 0 is deadlock.

## Decision

`PROMOTE` the any-word separation theorem. Constrained controls do not
create a new residual quotient in the tested class. Avižienis,
synchronizing automata, and constrained synchronization remain `KNOWN`
and answer different questions.

Best next question: answered in
[signed_digit_short_horizon.md](signed_digit_short_horizon.md).

## Publication assessment

Status: `STRUCTURAL`. An exact rigidity theorem exists. Not a
`PAPER_CANDIDATE`: the any-word strengthening is a laboratory
clarification of the previous constant-word witness.
