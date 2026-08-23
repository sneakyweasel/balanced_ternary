"""Descriptor for 3-adic polynomial congruence lifting trees."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="lifting",
    title="Polynomial congruences and 3-adic lifting trees",
    status="EXPLORATORY",
    statement=(
        "The solution tree of f(x) = 0 (mod 3^k) is exactly the "
        "zero-output subtree of the residual Mealy machine of f, and the "
        "residual state at a node is the scaled Taylor jet. The depth-r "
        "subtree is determined by the finite-horizon class of the "
        "residual, sharply. Existence, counting, and complexity of these "
        "trees are classical; no improvement on known root-counting "
        "algorithms is claimed."
    ),
    bt_relevance=(
        "Balanced digits make the partial sum of output trits smaller "
        "than the modulus, so divisibility of f(n_w) by 3^k is equivalent "
        "to every output trit vanishing. The residual sections and the "
        "Newton invariant Phi_r of bt.calculus are then the lifting state."
    ),
    docs=(
        "docs/problems/lifting.md",
        "docs/theory/padic_lifting_trees.md",
    ),
    lean=("formal/BTCalculus/PadicLifting.lean",),
)
