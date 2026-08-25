"""Integer 1-D diagnostic probes. Censuses are not theorems."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from research_engine.attacks.result import AttackContext, phase_key
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State


DEFAULT_MAGNITUDE_WINDOW = tuple(range(-24, 25))
DEFAULT_RESIDUE_SAMPLE = tuple(range(-30, 31))


def _abs_state(state: State) -> int | None:
    if not state:
        return None
    try:
        return sum(abs(int(part)) for part in state)
    except (TypeError, ValueError):
        return None


def is_integer_state(state: object) -> bool:
    if not isinstance(state, tuple) or not state:
        return False
    return all(isinstance(part, int) and not isinstance(part, bool) for part in state)


def magnitude_census(
    spec: ProblemSpec,
    context: AttackContext | None = None,
    window: Iterable[int] = DEFAULT_MAGNITUDE_WINDOW,
) -> dict[str, Any]:
    """Count one-step |T(s)| vs |s| on a stated integer window.

    Raises are skipped. Empty legal menus are skipped. This is not a
    Lyapunov certificate.
    """
    del context
    phase = spec.initial_phase()
    drops = 0
    growths = 0
    equals = 0
    sampled = 0
    for value in window:
        if spec.dimension == 1:
            raw: State = (int(value),)
        else:
            continue
        try:
            state = spec.canonicalize(raw)
        except (TypeError, ValueError):
            continue
        if not is_integer_state(state):
            continue
        try:
            controls = spec.legal_controls(state, phase)
        except (TypeError, ValueError):
            continue
        if not controls:
            continue
        before = _abs_state(state)
        if before is None:
            continue
        for control in controls:
            try:
                nxt = spec.canonicalize(spec.transition(state, control, phase))
            except (TypeError, ValueError):
                continue
            after = _abs_state(nxt)
            if after is None:
                continue
            sampled += 1
            if after < before:
                drops += 1
            elif after > before:
                growths += 1
            else:
                equals += 1
    if sampled == 0:
        regime = "UNOBSERVED"
    elif growths == 0 and drops > 0:
        regime = "WINDOW_CONTRACTING"
    elif drops == 0 and growths > 0:
        regime = "WINDOW_EXPANDING"
    elif growths > 0 and drops > 0:
        regime = "MIXED_MAGNITUDE"
    else:
        regime = "WINDOW_STATIONARY"
    return {
        "sampled": sampled,
        "drops": drops,
        "growths": growths,
        "equals": equals,
        "regime": regime,
        "phase": phase_key(phase),
    }


def residue_census(
    spec: ProblemSpec,
    context: AttackContext | None = None,
    sample: Iterable[int] = DEFAULT_RESIDUE_SAMPLE,
) -> dict[str, Any]:
    """Observe image residues. A proper subset is not a modular theorem."""
    moduli = (2, 3, 4, 5) if context is None else context.moduli
    phase = spec.initial_phase()
    tables: dict[int, dict[int, set[int]]] = {mod: {} for mod in moduli}
    sampled = 0
    for value in sample:
        if spec.dimension != 1:
            break
        raw: State = (int(value),)
        try:
            state = spec.canonicalize(raw)
            controls = spec.legal_controls(state, phase)
        except (TypeError, ValueError):
            continue
        if not controls or not is_integer_state(state):
            continue
        n = int(state[0])
        for control in controls:
            try:
                nxt = spec.canonicalize(spec.transition(state, control, phase))
            except (TypeError, ValueError):
                continue
            if not is_integer_state(nxt):
                continue
            image = int(nxt[0])
            sampled += 1
            for mod in moduli:
                source = n % mod
                tables[mod].setdefault(source, set()).add(image % mod)
    restrictions: list[dict[str, object]] = []
    for mod, mapping in tables.items():
        images = set()
        for residues in mapping.values():
            images.update(residues)
        if 0 < len(images) < mod:
            restrictions.append(
                {
                    "modulus": mod,
                    "image_count": len(images),
                    "images": tuple(sorted(images)),
                }
            )
    return {
        "sampled": sampled,
        "moduli": moduli,
        "restriction_count": len(restrictions),
        "restrictions": tuple(restrictions),
    }


def run_integer_probes(
    spec: ProblemSpec,
    context: AttackContext | None = None,
) -> Mapping[str, Any]:
    start = spec.canonicalize(spec.initial_state)
    if spec.dimension != 1 or not is_integer_state(start):
        return {}
    return {
        "magnitude": magnitude_census(spec, context),
        "residue": residue_census(spec, context),
    }
