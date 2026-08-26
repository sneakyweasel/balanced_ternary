"""Registry of research problem descriptors."""

from research.open_problems.definition import ProblemDefinition, STATUSES

__all__ = ["ProblemDefinition", "STATUSES", "get_problem", "list_problems"]


def list_problems() -> tuple[ProblemDefinition, ...]:
    from research.additive_combinatorics.problem import PROBLEM as ADDITIVE
    from research.balanced_digit_sum_polynomials.problem import (
        PROBLEM as BALANCED_DIGIT_SUM_POLYNOMIALS,
    )
    from research.balanced_ternary.problem import PROBLEM as BALANCED_TERNARY
    from research.balanced_ternary_digit_sum_dynamics.problem import (
        PROBLEM as BALANCED_TERNARY_DIGIT_SUM_DYNAMICS,
    )
    from research.balanced_ternary_weight_dynamics.problem import (
        PROBLEM as BALANCED_TERNARY_WEIGHT_DYNAMICS,
    )
    from research.balanced_ternary_weight_drift.problem import (
        PROBLEM as BALANCED_TERNARY_WEIGHT_DRIFT,
    )
    from research.cerny_bt.problem import PROBLEM as CERNY_BT
    from research.collatz.problem import PROBLEM as COLLATZ
    from research.collatz_finite_descent.problem import PROBLEM as COLLATZ_FINITE_DESCENT
    from research.erdos_distinct_subset_sums.problem import (
        PROBLEM as ERDOS_DISTINCT_SUBSET_SUMS,
    )
    from research.lifting.problem import PROBLEM as LIFTING
    from research.misere_quotients.problem import PROBLEM as MISERE_QUOTIENTS
    from research.monna_endpoint_spectra.problem import PROBLEM as MONNA_ENDPOINT_SPECTRA
    from research.operator_dynamics.problem import PROBLEM as OPERATOR_DYNAMICS
    from research.operator_dynamics.signed_p0.problem import (
        PROBLEM as OPERATOR_DYNAMICS_BENCHMARK,
    )
    from research.kabelian_complexity.problem import PROBLEM as KABELIAN_COMPLEXITY
    from research.ostrowski.problem import PROBLEM as OSTROWSKI
    from research.padic_dynamics.problem import PROBLEM as PADIC_DYNAMICS
    from research.regular_output_preimages.problem import PROBLEM as REGULAR_OUTPUT_PREIMAGES
    from research.residual_complexity.problem import PROBLEM as RESIDUAL_COMPLEXITY
    from research.perfect_powers.problem import PROBLEM as PERFECT_POWERS
    from research.prime_residual_complexity.problem import PROBLEM as PRIME_RESIDUAL
    from research.primes.problem import PROBLEM as PRIMES
    from research.residuals.problem import PROBLEM as RESIDUALS
    from research.rewrite_calculus.problem import PROBLEM as REWRITE_CALCULUS
    from research.signed_digit_residual.problem import PROBLEM as SIGNED_DIGIT_RESIDUAL
    from research.signed_digit_residual_geometry.problem import (
        PROBLEM as SIGNED_DIGIT_RESIDUAL_GEOMETRY,
    )
    from research.signed_digit_residual_minimality.problem import (
        PROBLEM as SIGNED_DIGIT_RESIDUAL_MINIMALITY,
    )
    from research.signed_digit_constrained_controls.problem import (
        PROBLEM as SIGNED_DIGIT_CONSTRAINED_CONTROLS,
    )
    from research.signed_digit_short_horizon.problem import (
        PROBLEM as SIGNED_DIGIT_SHORT_HORIZON,
    )
    from research.multiplicative_residual.problem import PROBLEM as MULTIPLICATIVE_RESIDUAL
    from research.sparse_polynomials.problem import PROBLEM as SPARSE_POLYNOMIALS
    from research.stabilization.problem import PROBLEM as STABILIZATION
    from research.syracuse.problem import PROBLEM as SYRACUSE
    from research.engine_campaign.problem import PROBLEM as ENGINE_CAMPAIGN
    from research.engine_memory.problem import PROBLEM as ENGINE_MEMORY
    from research.target_board.problem import PROBLEM as TARGET_BOARD
    from research.research_strategy.problem import PROBLEM as RESEARCH_STRATEGY
    from research.aliquot_dynamics.problem import PROBLEM as ALIQUOT_DYNAMICS
    from research.skolem_lrs.problem import PROBLEM as SKOLEM_LRS
    from research.positivity_lrs.problem import PROBLEM as POSITIVITY_LRS
    from research.switching_affine_z2_origin.problem import PROBLEM as SWITCHING_AFFINE_Z2
    from research.skolem_order2_known_zero.problem import PROBLEM as SKOLEM_ORDER2
    from research.bb5_map.problem import PROBLEM as BB5_MAP
    from research.linear_constraint_loops.problem import PROBLEM as LINEAR_CONSTRAINT_LOOPS
    from research.mx_plus_r.problem import PROBLEM as MX_PLUS_R
    from research.mx_plus_r_7x1_class_obstruction.problem import PROBLEM as MX_PLUS_R_7X1
    from research.euclidean_quotient.problem import PROBLEM as EUCLIDEAN_QUOTIENT
    from research.vector_affine.problem import PROBLEM as VECTOR_AFFINE
    from research.matrix_word_invariant.problem import PROBLEM as MATRIX_WORD_INVARIANT

    return (
        COLLATZ,
        COLLATZ_FINITE_DESCENT,
        SYRACUSE,
        ENGINE_CAMPAIGN,
        ENGINE_MEMORY,
        TARGET_BOARD,
        RESEARCH_STRATEGY,
        LINEAR_CONSTRAINT_LOOPS,
        BB5_MAP,
        ALIQUOT_DYNAMICS,
        SKOLEM_LRS,
        POSITIVITY_LRS,
        SWITCHING_AFFINE_Z2,
        SKOLEM_ORDER2,
        MX_PLUS_R,
        MX_PLUS_R_7X1,
        EUCLIDEAN_QUOTIENT,
        VECTOR_AFFINE,
        MATRIX_WORD_INVARIANT,
        RESIDUALS,
        LIFTING,
        PADIC_DYNAMICS,
        ADDITIVE,
        PERFECT_POWERS,
        PRIMES,
        PRIME_RESIDUAL,
        SPARSE_POLYNOMIALS,
        OPERATOR_DYNAMICS,
        OPERATOR_DYNAMICS_BENCHMARK,
        STABILIZATION,
        CERNY_BT,
        MISERE_QUOTIENTS,
        REGULAR_OUTPUT_PREIMAGES,
        RESIDUAL_COMPLEXITY,
        MONNA_ENDPOINT_SPECTRA,
        REWRITE_CALCULUS,
        SIGNED_DIGIT_RESIDUAL,
        SIGNED_DIGIT_RESIDUAL_GEOMETRY,
        SIGNED_DIGIT_RESIDUAL_MINIMALITY,
        SIGNED_DIGIT_CONSTRAINED_CONTROLS,
        SIGNED_DIGIT_SHORT_HORIZON,
        MULTIPLICATIVE_RESIDUAL,
        BALANCED_DIGIT_SUM_POLYNOMIALS,
        BALANCED_TERNARY_DIGIT_SUM_DYNAMICS,
        BALANCED_TERNARY_WEIGHT_DYNAMICS,
        BALANCED_TERNARY_WEIGHT_DRIFT,
        ERDOS_DISTINCT_SUBSET_SUMS,
        OSTROWSKI,
        KABELIAN_COMPLEXITY,
        BALANCED_TERNARY,
    )


def get_problem(problem_id: str) -> ProblemDefinition:
    for problem in list_problems():
        if problem.id == problem_id:
            return problem
    raise KeyError(problem_id)
