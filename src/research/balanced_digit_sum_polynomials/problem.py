"""Descriptor for balanced digit sums of nonlinear polynomial values."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_digit_sum_polynomials",
    title="Balanced digit sums of nonlinear polynomial values",
    status="EXPLORATORY",
    statement=(
        "For nonlinear P in Z[x], decide whether the exact integer "
        "level set {n : s_bal(P(n))=0} or the finite-prefix family "
        "E^{(k)}_{P,0} has a structural law not inherited from ordinary "
        "ternary digit-sum theory. The translation s_bal(m)=s_3(2m)-s_3(m) "
        "recasts the integer predicate and does not by itself close the gate."
    ),
    bt_relevance=(
        "Signed balanced digits make exact digit-sum zero possible by "
        "cancellation. Residual outputAlong supplies the first |w| digits "
        "of P(n_w); the terminal correction is s_bal of the residual at 0."
    ),
    docs=("docs/problems/balanced_digit_sum_polynomials.md",),
)
