"""Registry of research problem descriptors."""

from research.open_problems.definition import ProblemDefinition, STATUSES

__all__ = ["ProblemDefinition", "STATUSES", "get_problem", "list_problems"]


def list_problems() -> tuple[ProblemDefinition, ...]:
    from research.additive_combinatorics.problem import PROBLEM as ADDITIVE
    from research.balanced_digit_sum_polynomials.problem import (
        PROBLEM as BALANCED_DIGIT_SUM_POLYNOMIALS,
    )
    from research.cerny_bt.problem import PROBLEM as CERNY_BT
    from research.collatz.problem import PROBLEM as COLLATZ
    from research.erdos_distinct_subset_sums.problem import (
        PROBLEM as ERDOS_DISTINCT_SUBSET_SUMS,
    )
    from research.lifting.problem import PROBLEM as LIFTING
    from research.misere_quotients.problem import PROBLEM as MISERE_QUOTIENTS
    from research.monna_endpoint_spectra.problem import PROBLEM as MONNA_ENDPOINT_SPECTRA
    from research.operator_dynamics.problem import PROBLEM as OPERATOR_DYNAMICS
    from research.kabelian_complexity.problem import PROBLEM as KABELIAN_COMPLEXITY
    from research.ostrowski.problem import PROBLEM as OSTROWSKI
    from research.padic_dynamics.problem import PROBLEM as PADIC_DYNAMICS
    from research.regular_output_preimages.problem import PROBLEM as REGULAR_OUTPUT_PREIMAGES
    from research.perfect_powers.problem import PROBLEM as PERFECT_POWERS
    from research.primes.problem import PROBLEM as PRIMES
    from research.residuals.problem import PROBLEM as RESIDUALS
    from research.rewrite_calculus.problem import PROBLEM as REWRITE_CALCULUS
    from research.sparse_polynomials.problem import PROBLEM as SPARSE_POLYNOMIALS
    from research.stabilization.problem import PROBLEM as STABILIZATION

    return (
        COLLATZ,
        RESIDUALS,
        LIFTING,
        PADIC_DYNAMICS,
        ADDITIVE,
        PERFECT_POWERS,
        PRIMES,
        SPARSE_POLYNOMIALS,
        OPERATOR_DYNAMICS,
        STABILIZATION,
        CERNY_BT,
        MISERE_QUOTIENTS,
        REGULAR_OUTPUT_PREIMAGES,
        MONNA_ENDPOINT_SPECTRA,
        REWRITE_CALCULUS,
        BALANCED_DIGIT_SUM_POLYNOMIALS,
        ERDOS_DISTINCT_SUBSET_SUMS,
        OSTROWSKI,
        KABELIAN_COMPLEXITY,
    )


def get_problem(problem_id: str) -> ProblemDefinition:
    for problem in list_problems():
        if problem.id == problem_id:
            return problem
    raise KeyError(problem_id)
