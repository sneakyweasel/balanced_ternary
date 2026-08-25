# Signed-digit residual minimality

Status: **STRUCTURAL**

Once the origin-reachable set `R_{λ,U}` of `F_{λ,U}(s,u)=λ·D(s+u)` is
known, is the minimal Mealy machine smaller than `|R|`?

CLI `btlab research analyze signed_digit_residual_minimality` (aliases
`sdrm`, `sdr_minimality`). Reuses `SignedDigitResidualSpec`. It does
not reopen the finite/infinite law, the `U_m` fill, Collatz, primes,
T/jets, or Ostrowski.

Source revision of this session: `d81d162` plus the uncommitted
geometry/minimality tree.

## Problem

Characterize behavioral equivalence of origin-reachable residuals under
output `lsd(s+u)`, and decide whether `M(λ,U)=|R_{λ,U}|`.

## Exact statement

For every nonempty finite `U` and every gain `λ` not divisible by `3`,
distinct integers `s≠t` are distinguished by the constant word of any
letter `u∈U` of length `v_3(s-t)+1`. Consequently every origin-reachable
finite machine in this regime is already minimal:

```text
M(λ,U)=|R_{λ,U}|.
```

Immediate `lsd` signatures agree if and only if `s≡t (mod 3)`. That is
not a merge: the successor difference is `λ(s-t)/3`, independent of the
control, and the 3-adic valuation drops until the outputs separate.

At `λ=3` the same arithmetic gives a genuine translation symmetry
`s ~ s+3k` on all of `ℤ`. Those extra states are not origin-reachable
when `max|u|≤1`, so `H_sep` still holds on `R_{3,U_1}={0}`.

## Current literature

- Unique balanced-ternary expansion, Avižienis signed-digit conversion,
  and Heuberger–Prodinger carry transducers are `KNOWN`. Distinct carries
  as transducer states are the standard encoding, not a new machine.
- Mealy minimization and distinguishing experiments are `KNOWN`.
- The exact 3-adic length `L_sep(s,t)=v_3(s-t)+1` for this residual
  map, and the contrast that `λ≡0 (mod 3)` produces a translation
  quotient, is `NEW FORMULATION` of unique LSD expansion. It is not a
  new adder.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

- **Target:** when distinct origin-reachable residuals of
  `s↦λ D(s+u)` are observationally equivalent.
- **Novelty hypothesis:** `M=|R|` is a 3-adic rigidity theorem for
  `λ` coprime to 3, not an artifact of the alphabets tested so far.
- **Falsifier:** a nonempty finite `U` at `λ=1` or `λ=2` with two
  equivalent reachable residuals; or a merge not explained by
  `s≡t (mod 3^k)`.
- **Existing machinery:** `signed_step`, `mealy_partition`,
  `SignedDigitResidualSpec`, origin-reachable geometry.
- **Maximum Phase-0 scope:** the listed sparse alphabets at `λ=1,2`;
  the pair `0` vs `3`; Lean of coprime-gain separation and the `λ=3`
  translation.
- **Promotion criterion:** a separation theorem for a clean class, or
  a smallest exact merge with an algebraic explanation.
- **Stop criterion:** uninterpretable merges, or nothing beyond routine
  Mealy minimization.

## Balanced-ternary formulation

Output `o(s,u)=lsd(s+u)` is the unique trit residue of `s+u`. The
successor is existing `λ·D(s+u)`. Equivalence is equality of output
streams on `U^*`.

## Why BT may be relevant

The observation is the least trit. Distinct residuals are distinct
higher-digit strings, and `λ` coprime to 3 cannot hide that difference.

## Candidate operations / invariants

- `s≡t (mod 3)` iff immediate output signatures agree. **EXACT — LEAN VERIFIED**
- `L_sep(s,t)=v_3(s-t)+1` for `λ` not divisible by 3. **EXACT — LEAN VERIFIED**
- `M=|R|` on the listed alphabets and on `U_m` for `m≤6`. **COMPUTATIONALLY VERIFIED** (the general case is the Lean theorem on `ℤ`)
- Identical 1-letter signatures imply `s~t`. **REFUTED** (`0` vs `3` at `λ=1`)
- Some listed `U` has `M<|R|`. **REFUTED**
- At `λ=3`, `s ~ s+3k`. **EXACT — LEAN VERIFIED**

## Experiments

- `btlab research analyze|attack|reproduce|report signed_digit_residual_minimality`
- Discovery:
  `src/research/signed_digit_residual_minimality/discovery.py`
- Tests:
  `tests/research/signed_digit_residual_minimality/test_signed_digit_residual_minimality.py`
- Records in `experiments/balanced_ternary/signed_digit_residual_minimality/`

Search alphabets (each at `λ=1` and `λ=2`):

```text
{0,1}, {-1,0}, {1,2}, {-2,0}, {-2,2}, {-1,1}, {0,2},
{-2,0,2}, {-2,-1,2}, {-2,1,2}
```

All have singleton Mealy classes. The first pairs with agreeing
1-letter signatures appear on `U_m` once the diameter reaches 3
(e.g. `0` and `3` at `λ=1`, `m=6`); they still separate at length 2.

## Conjectures

None opened.

## Counterexamples

- `M<|R|` on a listed alphabet: none. Smallest attempted witnesses
  remain minimal.
- Identical immediate signatures merge: `s=0`, `t=3`, `λ=1`, `U={0}`,
  word `(0,0)`.
- Global merge outside origin-reachability: `s=0`, `t=3`, `λ=3`,
  `U={0}`, no separating word.

## Formalization

`formal/Problems/BalancedTernary/SignedDigitResidualMinimality.lean`.
Theorems `signedOut_eq_iff_cong`, `signedNext_diff_of_cong`,
`residual_separation`, `lambda3_trace_translate`. Reuses `signedNext`,
`signedOut`, `lsdZ_add_mul3`, `DZ_add_mul3`. No `sorry`.

## Results

| object | value |
|--------|--------|
| listed `U`, `λ=1,2` | `M=\|R\|` |
| `U_6`, `λ=1` | `R=[-3,3]`, `M=7`, `L_max=2` |
| `U_6`, `λ=2` | even lattice, `M=\|R\|`, `L_max=3` |
| `0` vs `3` at `λ=1` | same 1-letter signature, separated by `(0,0)` |
| `0` vs `3` at `λ=3` | equivalent on all of `ℤ` |

The measured object is **observed** dynamics `(s,u)↦(λ D(s+u), lsd(s+u))`,
not the state-only graph. Immediate outputs already separate every pair
not congruent mod 3; the remaining pairs are separated by the 3-adic
drop of the control-independent successor difference.

## Open questions

None opened as conjectures.

## Decision

`PROMOTE` the coprime-gain separation theorem: distinct residuals are
intrinsically observable, with exact distinguishing length
`v_3(s-t)+1`. Avižienis / carry transducers remain `KNOWN`. The
promoted content is residual rigidity of this normalizer, not a new
minimization algorithm.

Best next question: answered by
[signed_digit_constrained_controls.md](signed_digit_constrained_controls.md).

## Publication assessment

Status: `STRUCTURAL`. An exact rigidity theorem exists. Not a
`PAPER_CANDIDATE`: unique balanced expansion already implies that
distinct remainders are different numbers, and carry-transducer
minimality is routine once that is granted.
