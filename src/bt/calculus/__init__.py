"""Balanced-ternary calculus: trit algebra, D/I_a, rewrite, and control.

Problem-independent. Wraps :mod:`bt.operators` and :mod:`bt.representation`.
Does not import research modules.
"""

from bt.calculus.complexity import Complexity, measure
from bt.calculus.derivative import D, D_k, S, digit_at, lsd, reconstruct
from bt.calculus.differential import D_of_product, D_of_sum, add_correction, mul_correction
from bt.calculus.discovery import IdentityCandidate, discover_closed
from bt.calculus.expressions import Expr, e_int, e_trit, render
from bt.calculus.integral import I, I_minus, I_plus, I_zero, P
from bt.calculus.locality import InformationProfile, all_profiles, profile
from bt.calculus.normalization import normal_form, normalize_expr
from bt.calculus.order import cmp3
from bt.calculus.rewrite import REWRITE_RULES, rewrite_expr, rewrite_word
from bt.calculus.select import abs_z, clamp_z, max_z, median_z, min_z, select3, sign_z
from bt.calculus.semantics import evaluate
from bt.calculus.trit import Trit, algebraic_name, as_trit, neg, trit_max, trit_min
from bt.calculus.vm import VMResult, evaluate_direct, run_postfix

__all__ = [
    "Complexity",
    "D",
    "D_k",
    "D_of_product",
    "D_of_sum",
    "Expr",
    "I",
    "I_minus",
    "I_plus",
    "I_zero",
    "IdentityCandidate",
    "InformationProfile",
    "P",
    "REWRITE_RULES",
    "S",
    "Trit",
    "VMResult",
    "abs_z",
    "add_correction",
    "algebraic_name",
    "all_profiles",
    "as_trit",
    "clamp_z",
    "cmp3",
    "digit_at",
    "discover_closed",
    "e_int",
    "e_trit",
    "evaluate",
    "evaluate_direct",
    "lsd",
    "max_z",
    "measure",
    "median_z",
    "min_z",
    "mul_correction",
    "neg",
    "normal_form",
    "normalize_expr",
    "profile",
    "reconstruct",
    "render",
    "rewrite_expr",
    "rewrite_word",
    "run_postfix",
    "select3",
    "sign_z",
    "trit_max",
    "trit_min",
]
