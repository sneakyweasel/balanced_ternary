# Balanced-ternary calculus

Master record for Milestone 13. Claim labels have the usual meaning.
This is **not** a Collatz milestone. Collatz is one future client of
the library `bt.calculus`.

## Levels

**Level A — trit calculus.** Primitive objects `{-1,0,+1}`; constructors
`I_a(x)=a+3x`; destructor `D(x)=(x-lsd(x))/3`.

**Level B — integer arithmetic.** Existing exact `bt` arithmetic and
operators.

**Level C — symbolic calculus.** Expression trees, rewrite, postfix VM,
`cmp3`/`select3`.

## Honesty

Much of Level A is unique balanced-ternary representation under a new
name. The milestone is a success if those facts become one language
*and* if a few identities are more than a change of notation.

**Elegant reformulation of standard facts**

- unique expansion, `D` = drop LSD, `I_a` = prepend LSD
- `D ∘ I_a = id`, `S = I_0`, `S ∘ D(n) = n - lsd(n)`
- addition correction = existing `rewrite_sum` carry table
- finite-state classification of `S,N,D,I_a,K3,M2,H2,W,odd-part,T`
  already in [balanced_ternary_automata.md](../balanced_ternary_automata.md)

**Identities that are calculus-shaped rather than mere uniqueness slogans**

- twisted Leibniz rule `D(xy)=lsd(x)D(y)+lsd(y)D(x)+3 D(x)D(y)`
- left-zero band of projections `P_a ∘ P_b = P_a`
- trit-valued `cmp3` laws and `select3` as a control algebra
- classified rewrite fragment `{D,I_a,S,N}` with a terminating
  confluent tree TRS, including `N(D(x)) → D(N(x))`, and an
  explicit NF grammar whose irreducibles are unique integer
  operator functions; exact `Add` extensions (push-in or factor-out)
  are not a tiny tree core — they are trit-carry / AC-engine territory
- information profiles (delay / precision / state) as a thin layer
  over existing `OperatorMetadata`

Whether this is enough for a standalone paper is a later editorial
question. The mathematics is specified; it is not automatically “new
analysis”.

## Pointers

- [Trit algebra](trit_algebra.md)
- [Digit derivative](digit_derivative.md)
- [Rewrite](rewrite_calculus.md)
- [Trit control](trit_control.md)
- [Setun connection](setun_connection.md)
- Package: `src/bt/calculus/`
- Lean: `formal/BTCalculus/`
- CLI: `btprime calculus …`
- Coefficient-vector NF (Milestone 14): [balanced_ternary_normalization.md](balanced_ternary_normalization.md). Different object from expression-tree NF.
- Section/jet calculus (Milestone 15): [polynomial_jet_calculus.md](polynomial_jet_calculus.md). `D_coeff` is not `D`.
- Residual automata (Milestone 16): [residual_state_complexity.md](residual_state_complexity.md). Sample minimization is not `M_k`.
- Quadratic MN count (Milestone 17): [quadratic_residual_complexity.md](quadratic_residual_complexity.md). `M_k(x^2)=(3^k−1)/2`.
- Cubic Newton stratum (canonical): [cubic_newton_stratum.md](cubic_newton_stratum.md).
- Residual versus classical sources: [residual_vs_classical.md](residual_vs_classical.md).
- Layer notes (corollaries): [cubic_residual_image.md](cubic_residual_image.md),
  [cubic_residual_fibres.md](cubic_residual_fibres.md),
  [cubic_deepest_layer.md](cubic_deepest_layer.md),
  [cubic_intermediate_layer.md](cubic_intermediate_layer.md),
  [cubic_deficit_two.md](cubic_deficit_two.md),
  [cubic_n1_valuation.md](cubic_n1_valuation.md),
  [cubic_n0_reduction.md](cubic_n0_reduction.md),
  [mismatched_cubic_quotient.md](mismatched_cubic_quotient.md).
  Invariant decision: [cubic_newton_stratum.md](cubic_newton_stratum.md) §6.

## Finite-state locality (reused, not re-proved)

| Operator | Class |
|----------|--------|
| `S`, `N`, `D`, `I_a`, `H3` | sequential |
| `K3` | sequential, 2 states |
| `M2`, `H2` | sequential, 3-state Mealy |
| `W`, `Wz`, `Wt` | not one-way sequential |
| odd-part | not one rational transduction |
| Collatz `T` | inherits the odd-part obstruction |

Information profiles: `bt.calculus.locality.profile`.

## Stack VM

Postfix operations: `ADD SUB MUL NEG D I- I0 I+ S M2 H2 CMP3 SELECT3`.
Measures: expression size, stack depth, trit operations, carry
operations (via existing `CarryTrace` when addition is used).

## Identity discovery

`bt.calculus.discovery` clusters closed unary terms of depth `≤ 6`.
It never writes `sorry` into the Lean project and never labels a
candidate **PROVED**.
