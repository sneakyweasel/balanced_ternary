"""Registry of research problem descriptors."""

from research.open_problems.definition import ProblemDefinition, STATUSES

__all__ = ["ProblemDefinition", "STATUSES", "get_problem", "list_problems"]


def list_problems() -> tuple[ProblemDefinition, ...]:
    from research.additive_combinatorics.problem import PROBLEM as ADDITIVE
    from research.collatz.problem import PROBLEM as COLLATZ
    from research.operator_dynamics.problem import PROBLEM as OPERATOR_DYNAMICS
    from research.perfect_powers.problem import PROBLEM as PERFECT_POWERS
    from research.primes.problem import PROBLEM as PRIMES
    from research.sparse_polynomials.problem import PROBLEM as SPARSE_POLYNOMIALS

    return (
        COLLATZ,
        ADDITIVE,
        PERFECT_POWERS,
        PRIMES,
        SPARSE_POLYNOMIALS,
        OPERATOR_DYNAMICS,
    )


def get_problem(problem_id: str) -> ProblemDefinition:
    for problem in list_problems():
        if problem.id == problem_id:
            return problem
    raise KeyError(problem_id)
