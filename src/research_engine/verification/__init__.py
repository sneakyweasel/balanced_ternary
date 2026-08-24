"""Emit theorem targets from exact certificates. This is not a prover."""

from research_engine.verification.targets import (
    FORBIDDEN_LEAN_TOKENS,
    TheoremTarget,
    assert_no_proof_tokens,
    attach_lean,
    exportable_targets,
    render_lean_comment,
    render_yaml,
    target_from_result,
    targets_from_report,
    targets_from_results,
)

__all__ = [
    "FORBIDDEN_LEAN_TOKENS",
    "TheoremTarget",
    "assert_no_proof_tokens",
    "attach_lean",
    "exportable_targets",
    "render_lean_comment",
    "render_yaml",
    "target_from_result",
    "targets_from_report",
    "targets_from_results",
]
