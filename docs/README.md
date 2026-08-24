# Documentation map

The documentation records exact mathematics, bounded computations, open
questions, and literature comparisons separately. Claim labels have the same
meaning throughout:

- **EXACT — HUMAN PROOF**: supported by an argument in the mathematical record;
- **EXACT — LEAN VERIFIED**: the same statement has a compiled Lean proof;
- **COMPUTATIONALLY VERIFIED**: checked on a stated finite domain;
- **CONJECTURE**: open and paired with counterexample search;
- **OBSERVATION**: empirical, without necessity or universality;
- **REFUTED**: a counterexample is recorded;
- **REPARAMETERIZATION**: a classical construction under a local name.

These seven are the only tags allowed in
[theory/theorem_ledger.json](theory/theorem_ledger.json) and in research
notes. Do not write **PROVED** or **VERIFIED COMPUTATIONALLY**.

Novelty is a separate axis, used in dossiers and theory pages and never
as a ledger tag: **KNOWN** (in the literature, cite a `literature/` id),
**PROJECT-SPECIFIC** (what this project measures or refines), and
**OPEN** (no proof and no refutation yet). **REPARAMETERIZATION** sits on
both axes. See [methodology.md](methodology.md).

## Start here

The live publication task is the rewrite-calculus note. Send the
[reviewer packet](theory/rewrite_calculus_reviewer_packet.md) with the
[draft](theory/rewrite_calculus_note.md).

Last promoted mathematical theory (STRUCTURAL; no new monomial strata):

1. [Balanced-ternary calculus](theory/balanced_ternary_calculus.md)
2. [Cubic Newton stratum](theory/cubic_newton_stratum.md)
3. [Residual versus classical sources](theory/residual_vs_classical.md)
4. [Theorem ledger](theory/theorem_ledger.md)

Foundation, then operators: [mathematics.md](mathematics.md),
[balanced_ternary_operators.md](balanced_ternary_operators.md).
Collatz is one application: [collatz_mathematics.md](collatz_mathematics.md).
Method: [methodology.md](methodology.md).

## Foundations

- [Balanced-ternary mathematics](mathematics.md): canonical representation,
  arithmetic, metrics, and residue invariants.
- [Operators](balanced_ternary_operators.md): shift, negation, digit
  derivative, reversal, and the integer/word interface.
- [Operator algebra](operator_algebra.md): compositions and commutators.
- [Finite-state maps](balanced_ternary_automata.md): which arithmetic maps
  are sequential transductions.
- [Additive combinatorics](balanced_ternary_additive_combinatorics.md):
  digit-restricted sumsets and carry defect.
- [Polynomials](balanced_ternary_polynomials.md): \(P_n(x)\) with
  \(P_n(3)=n\).

## Calculus and rewrite

- [Balanced-ternary calculus](theory/balanced_ternary_calculus.md)
- [Trit algebra](theory/trit_algebra.md)
- [Digit derivative](theory/digit_derivative.md)
- [Rewrite calculus](theory/rewrite_calculus.md)
- [Rewrite-calculus paper note](theory/rewrite_calculus_note.md)
- [Rewrite-calculus reviewer packet](theory/rewrite_calculus_reviewer_packet.md)
- [Rewrite-calculus formalization gate](theory/rewrite_calculus_formalization.md)
- [Trit control](theory/trit_control.md)
- [Setun connection](theory/setun_connection.md)
- [Normalization](theory/balanced_ternary_normalization.md),
  [rewrite system](theory/normalization_rewrite_system.md),
  [complexity](theory/normalization_complexity.md),
  [Setun normalization](theory/setun_normalization.md)
- [Jets](theory/balanced_ternary_jets.md),
  [polynomial jet calculus](theory/polynomial_jet_calculus.md),
  [jet transducers](theory/jet_transducers.md)
- [Residual-state complexity](theory/residual_state_complexity.md)
- [Quadratic residual complexity](theory/quadratic_residual_complexity.md)
- [Polynomial function congruence](theory/polynomial_function_congruence.md)
- [3-adic lifting trees](theory/padic_lifting_trees.md)
- [Minimal lifting state](theory/lifting_state_complexity.md)
- [Local vs global root-count bounds](theory/local_vs_global_stabilization.md)
- [Residual explorer](tools/residual_explorer.md)

## Newton stratum

Canonical cubic record: [cubic_newton_stratum.md](theory/cubic_newton_stratum.md).
Short extract: [newton_stratum_note.md](theory/newton_stratum_note.md).
Classical comparison: [residual_vs_classical.md](theory/residual_vs_classical.md).

Historical layer notes (stubs that point at the monograph):
[image](theory/cubic_residual_image.md),
[fibres](theory/cubic_residual_fibres.md),
[deepest layer](theory/cubic_deepest_layer.md),
[intermediate layer](theory/cubic_intermediate_layer.md),
[depth-deficit 2](theory/cubic_deficit_two.md),
[N1 valuation](theory/cubic_n1_valuation.md),
[N0 reduction](theory/cubic_n0_reduction.md),
[mismatched quotient](theory/mismatched_cubic_quotient.md).

## Collatz application

- [Collatz mathematics](collatz_mathematics.md): consolidated exact record
  for the accelerated odd-only map.
- [Research questions](collatz_research_questions.md): answered questions,
  open targets, conjectures, and preserved counterexamples.
- [Itinerary compatibility](collatz_itinerary_compatibility.md)
- [Zero-lift dynamics](collatz_zero_lift.md)
- [Dual coding](collatz_dual_coding.md)
- [Affine-center geometry](collatz_affine_center.md)
- [Fixed-integer asymptotics](collatz_fixed_integer_asymptotics.md)
- [Cycle languages](collatz_cycle_languages.md)
- [BT word maps](collatz_bt_warp.md)
- [Literature comparison](literature_comparison.md)
- [Balanced ternary versus Collatz literature](balanced_ternary_vs_collatz_literature.md)
- [Cycle literature comparison](cycle_literature_comparison.md)
- [Cycle literature replication](cycle_literature_replication.md)

## Problem dossiers

Each dossier follows [problems/TEMPLATE.md](problems/TEMPLATE.md).

- [Rewrite calculus](problems/rewrite_calculus.md)
- [Residuals](problems/residuals.md)
- [Collatz](problems/collatz.md)
- [Ostrowski order-m adder](problems/ostrowski_order_m_adder.md)
- [Regular-output preimages](problems/regular_output_preimages.md)
- [Monna endpoint spectra](problems/monna_endpoint_spectra.md)
- [Lifting trees](problems/lifting.md)
- [Additive combinatorics](problems/additive_combinatorics.md)
- [Perfect powers](problems/perfect_powers.md)
- [Primes](problems/primes.md)
- [Sparse polynomials](problems/sparse_polynomials.md)
- [Operator dynamics](problems/operator_dynamics.md)
- [Balanced digit sums of nonlinear polynomial values](problems/balanced_digit_sum_polynomials.md)
- [Erdős distinct subset sums](problems/erdos_distinct_subset_sums.md)
- [k-abelian complexity](problems/kabelian_complexity.md)
- [3-adic polynomial dynamics](problems/padic_dynamics.md)
- [Local vs global root-count bounds](problems/stabilization.md)
- [Černý residual-quotient gate](problems/cerny_bt.md)
- [Misere-quotient finite-context gate](problems/misere_quotients.md)

Journal: [research_journal.md](research_journal.md).
Ledger: [theory/theorem_ledger.md](theory/theorem_ledger.md).
Monna spectra theory: [theory/monna_endpoint_spectra.md](theory/monna_endpoint_spectra.md).
Regular-output preimages: [theory/regular_output_preimages.md](theory/regular_output_preimages.md).

## Architecture

Laboratory layout under [docs/architecture/](architecture/overview.md):

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
