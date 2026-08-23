"""Problem-independent balanced-ternary normalization theory.

Coefficient vectors over ``ℤ``, not a second encoder and not expression-tree
NF (that lives in ``bt.calculus.normalization``).
"""

from bt.normtheory.arithmetic import add_coeff, compare_fma, mul_coeff
from bt.normtheory.coeffword import CoeffWord, coefficient, degree, is_canonical, value
from bt.normtheory.complexity import measure
from bt.normtheory.rewrite import balanced_divmod, irreducible, legal_sites, normalize_step
from bt.normtheory.strategies import all_strategies, normal_form, normalize_lsd_to_msd
from bt.normtheory.hatd import hatD, hatD_raw

__all__ = [
    "CoeffWord",
    "add_coeff",
    "all_strategies",
    "balanced_divmod",
    "coefficient",
    "compare_fma",
    "degree",
    "irreducible",
    "is_canonical",
    "legal_sites",
    "measure",
    "mul_coeff",
    "normal_form",
    "normalize_lsd_to_msd",
    "normalize_step",
    "hatD",
    "hatD_raw",
    "value",
]
