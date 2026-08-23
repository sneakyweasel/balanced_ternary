# Documentation map

The documentation records exact mathematics, bounded computations, open
questions, and literature comparisons separately. Claim labels have the same
meaning throughout:

- **PROVED** = **EXACT — HUMAN PROOF**: supported by an argument in the mathematical record;
- **PROVED — LEAN** = **EXACT — LEAN VERIFIED**: the same statement has a compiled Lean proof;
- **COMPUTATIONALLY VERIFIED**: checked on a stated finite domain;
- **CONJECTURE**: open and paired with counterexample search;
- **OBSERVATION**: empirical, without necessity or universality;
- **REFUTED**: a counterexample is recorded;
- **REPARAMETERIZATION**: a classical construction under a local name.

These seven are the only tags allowed in
[theory/theorem_ledger.json](theory/theorem_ledger.json). Collatz notes
may still write **PROVED**; that is **EXACT — HUMAN PROOF**. Prose that
writes **VERIFIED COMPUTATIONALLY** means **COMPUTATIONALLY VERIFIED**.

Novelty is a separate axis, used in dossiers and theory pages and never
as a ledger tag: **KNOWN** (in the literature, cite a `literature/` id),
**PROJECT-SPECIFIC** (what this project measures or refines), and
**OPEN** (no proof and no refutation yet). **REPARAMETERIZATION** sits on
both axes. See [methodology.md](methodology.md).

## Foundations

- [Balanced-ternary mathematics](mathematics.md): canonical representation,
  arithmetic, features, and residue invariants.
- [Operators](balanced_ternary_operators.md): shift, negation, digit
  derivative, reversal, and the integer/word interface.
- [Operator algebra](operator_algebra.md): compositions and commutators.
- [Finite-state maps](balanced_ternary_automata.md): which arithmetic maps
  are sequential transductions.
- [Additive combinatorics](balanced_ternary_additive_combinatorics.md):
  digit-restricted sumsets and carry defect.
- [Polynomials](balanced_ternary_polynomials.md): \(P_n(x)\) with
  \(P_n(3)=n\).
- [Collatz mathematics](collatz_mathematics.md): the consolidated exact record
  for the accelerated odd-only map.
- [Research questions](collatz_research_questions.md): answered questions,
  open targets, conjectures, and preserved counterexamples.

## Exponent-code structure

- [Itinerary compatibility](collatz_itinerary_compatibility.md): affine
  exponent codes, minimum realizers, and nested cylinders.
- [Zero-lift dynamics](collatz_zero_lift.md): stabilization, zero-lift
  successors, periodic itineraries, and finite certificates.
- [Dual coding](collatz_dual_coding.md): valuation/lift two-coding and
  mixed-radix reconstruction.
- [Affine-center geometry](collatz_affine_center.md): exact fixed centers,
  contracting/expanding regimes, and coordinate inequalities.
- [Fixed-integer asymptotics](collatz_fixed_integer_asymptotics.md): affine
  gap \(G_m\) of one actual start, and the refutation of \(n_*\le n\).
- [Cycle languages](collatz_cycle_languages.md): primitive exponent codes,
  amplitude, and exact cycle pruning.
- [BT word maps](collatz_bt_warp.md): OEIS reversal \(W\), commutators with
  \(T\), palindromes, and realizer warps.

## Four-coordinate and literature work

- [Literature comparison](literature_comparison.md): project conventions
  against 2-adic/3-adic exponent-code literature.
- [Balanced ternary versus Collatz literature](balanced_ternary_vs_collatz_literature.md):
  what balanced ternary does and does not add.
- [Cycle literature comparison](cycle_literature_comparison.md): 2026 cycle
  preprints versus the exponent-code dictionary.
- [Cycle literature replication](cycle_literature_replication.md): independent
  finite checks, with preprint claims not assumed.

## Problems and journal

- [Discovery methodology](methodology.md): the research loop, branch
  budgets, and the `PROMOTE` / `PARK` / `CLOSE` decision.
- [Problem template](problems/TEMPLATE.md)
- [Collatz](problems/collatz.md)
- [Residuals](problems/residuals.md)
- [Lifting trees](problems/lifting.md)
- [3-adic polynomial dynamics](problems/padic_dynamics.md)
- [Local vs global root-count bounds](problems/stabilization.md)
- [Černý residual-quotient gate](problems/cerny_bt.md)
- [Misere-quotient finite-context gate](problems/misere_quotients.md)
- [Monna endpoint spectra](problems/monna_endpoint_spectra.md)
- [Additive combinatorics](problems/additive_combinatorics.md)
- [Perfect powers](problems/perfect_powers.md)
- [Primes](problems/primes.md)
- [Sparse polynomials](problems/sparse_polynomials.md)
- [Operator dynamics](problems/operator_dynamics.md)
- [Rewrite calculus](problems/rewrite_calculus.md)
- [Research journal](research_journal.md)
- [Theorem ledger](theory/theorem_ledger.md)
- [Balanced-ternary calculus](theory/balanced_ternary_calculus.md)
- [Trit algebra](theory/trit_algebra.md)
- [Digit derivative](theory/digit_derivative.md)
- [Rewrite calculus](theory/rewrite_calculus.md)
- [Rewrite-calculus formalization gate](theory/rewrite_calculus_formalization.md)
- [Trit control](theory/trit_control.md)
- [Setun connection](theory/setun_connection.md)
- [Balanced-ternary normalization](theory/balanced_ternary_normalization.md)
- [Normalization rewrite system](theory/normalization_rewrite_system.md)
- [Normalization complexity](theory/normalization_complexity.md)
- [Setun normalization](theory/setun_normalization.md)
- [Balanced-ternary jets](theory/balanced_ternary_jets.md)
- [Polynomial jet calculus](theory/polynomial_jet_calculus.md)
- [Jet transducers](theory/jet_transducers.md)
- [Residual-state complexity](theory/residual_state_complexity.md)
- [Quadratic residual complexity](theory/quadratic_residual_complexity.md)
- [Polynomial function congruence](theory/polynomial_function_congruence.md)
- [3-adic lifting trees](theory/padic_lifting_trees.md)
- [Minimal lifting state](theory/lifting_state_complexity.md)
- [Local vs global root-count bounds](theory/local_vs_global_stabilization.md)
- [Cubic Newton stratum](theory/cubic_newton_stratum.md)
- [Residual versus classical](theory/residual_vs_classical.md)
- [Cubic residual image](theory/cubic_residual_image.md)
- [Cubic residual fibres](theory/cubic_residual_fibres.md)
- [Cubic deepest layer](theory/cubic_deepest_layer.md)
- [Cubic intermediate layer](theory/cubic_intermediate_layer.md)
- [Cubic depth-deficit 2](theory/cubic_deficit_two.md)
- [Cubic N1 valuation strata](theory/cubic_n1_valuation.md)
- [Cubic N0 reduction](theory/cubic_n0_reduction.md)
- [Mismatched cubic quotient](theory/mismatched_cubic_quotient.md)
- [Balanced-Monna endpoint spectra](theory/monna_endpoint_spectra.md)
- [Residual explorer](tools/residual_explorer.md)

## Architecture

The laboratory layout (core vs research, experiments, conjectures,
formalization, literature) is recorded under
[docs/architecture/](architecture/overview.md):

- [Overview](architecture/overview.md)
- [Core](architecture/core.md)
- [Research modules](architecture/research_modules.md)
- [Experiments](architecture/experiments.md)
- [Conjectures](architecture/conjectures.md)
- [Formalization](architecture/formalization.md)
- [Literature](architecture/literature.md)

## Formal verification

See [the Lean project](../formal/README.md) for theorem names, build
instructions, and the boundary between abstract formal statements and Python
implementations.

## Reading paths

For the current research frontier, read:

1. [Balanced-ternary calculus](theory/balanced_ternary_calculus.md)
2. [Cubic Newton stratum](theory/cubic_newton_stratum.md)
3. [Residual versus classical sources](theory/residual_vs_classical.md)
4. [Theorem ledger](theory/theorem_ledger.md)

Collatz is one application, not the frontier. Its record starts at
[collatz_mathematics.md](collatz_mathematics.md).

For the balanced-ternary foundation, begin with
[Balanced-ternary mathematics](mathematics.md), then
[operators](balanced_ternary_operators.md).
