"""Descriptor for the accelerated (mx+r) campaign adapter."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="mx_plus_r",
    title="Generalized accelerated (mx+r) as a v2 family diagnosis",
    status="EXPLORATORY",
    statement=(
        "Can Research Engine v2 recover a parameterized affine family, "
        "exact valuation-like domain, and control-word obstructions for "
        "T_{m,r}(n)=(m n + r)/2^{v_2(m n + r)} without being told v_2?"
    ),
    bt_relevance="None required. Ordinary integer arithmetic.",
    docs=("docs/problems/engine_campaign.md",),
    lean=("formal/Problems/Engine/MxPlusR.lean",),
)
