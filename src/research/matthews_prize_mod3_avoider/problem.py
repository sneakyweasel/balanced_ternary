"""Descriptor for the frozen-engine three-branch mod-3 campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="matthews_prize_mod3_avoider",
    title="Frozen Engine campaign: three-branch mod-3 avoider class",
    status="EXPLORATORY",
    statement=(
        "On the hint-free three-branch map T(x)=2x when 3|x, "
        "T(x)=(7x+2)/3 when x ≡ 1 (mod 3), T(x)=(x-2)/3 when x ≡ 2 (mod 3), "
        "does frozen v2.3 recover a class obstruction that forces ±1 (mod 3) "
        "avoiders into the known cycles, without new attacks and without "
        "taking branch reconstruction or 0 (mod 3) divergence as the yield?"
    ),
    bt_relevance="Not required. Ordinary integer arithmetic.",
    docs=("docs/problems/matthews_prize_mod3_avoider.md",),
    lean=("formal/Problems/Engine/MatthewsMod3.lean",),
)
