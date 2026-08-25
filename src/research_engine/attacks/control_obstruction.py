"""Generic arithmetic obstructions from certified control-word constraints.

A search miss is not an obstruction. A cycle constraint is not a cycle.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import gcd
from typing import Any

from research_engine.attacks.control_word import compose_affine_steps, subsequent_k_impossible
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope

LEAN_DVD = "Problems.Engine.exists_mul_eq_iff_dvd"
LEAN_ABS = "Problems.Engine.not_dvd_of_abs_gt"
LEAN_CYCLE_DVD = "Problems.Engine.cycle_constraint_dvd"
LEAN_LAST = "Problems.Engine.last_step_remainder"
LEAN_BOUND = "Problems.Engine.cycle_abs_obstruction"


class ObstructionKind(str, Enum):
    DIVISIBILITY = "divisibility"
    GCD = "gcd"
    MODULAR = "modular"
    SIGN = "sign"
    BOUND = "bound"
    DOMAIN = "domain"


class ObstructionStatus(str, Enum):
    REFUTED = "REFUTED"
    CANDIDATE = "CANDIDATE"
    SEARCH_SUPPORTED = "SEARCH_SUPPORTED"
    FINITE_RANGE_SUPPORTED = "FINITE_RANGE_SUPPORTED"
    OBSTRUCTION_CANDIDATE = "OBSTRUCTION_CANDIDATE"
    SYMBOLICALLY_PROVED = "SYMBOLICALLY_PROVED"
    PROVED = "PROVED"
    LEAN_CERTIFIED = "LEAN_CERTIFIED"


class ObstructionScope(str, Enum):
    WORD = "WORD"
    CLASS = "CLASS"
    SYMBOLIC_CLASS = "SYMBOLIC_CLASS"


@dataclass(frozen=True)
class ControlObstructionCertificate:
    kind: str
    scope: str
    status: str
    reason: str
    constraint: Mapping[str, Any]
    summary: Mapping[str, Any]
    contradiction: Mapping[str, Any]
    lean: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "scope": self.scope,
            "status": self.status,
            "reason": self.reason,
            "constraint": dict(self.constraint),
            "summary": dict(self.summary),
            "contradiction": dict(self.contradiction),
            "lean": self.lean,
            "reconstructed_affine": None,
        }


def _divisors(value: int) -> tuple[int, ...]:
    if value == 0:
        return ()
    magnitude = abs(value)
    positive = [index for index in range(1, magnitude + 1) if magnitude % index == 0]
    return tuple(item for index in positive for item in (index, -index))


def _power_exponent(value: int, base: int) -> int | None:
    if base < 2 or value <= 0:
        return None
    exponent = 0
    current = 1
    while current < value:
        current *= base
        exponent += 1
        if exponent > 64:
            return None
    return exponent if current == value else None


def discover_summary(
    family: Mapping[str, Any] | None,
    relations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Infer reduced parameters from composed coefficients. Does not assume a sum."""
    if family is None or not relations:
        return {}
    base = int(family.get("base") or family.get("q_base") or 0)
    p = int(family.get("p") or 0)
    if base < 2:
        return {}
    exponent_sum = True
    length_power = True
    for item in relations:
        word = tuple(item.get("word", {}).get("parameters") or ())
        total = sum(int(part) for part in word)
        if int(item["a"]) != base ** total:
            exponent_sum = False
        if int(item["b"]) != p ** len(word):
            length_power = False
    summary: dict[str, Any] = {}
    if exponent_sum:
        summary["exponent_sum"] = True
    if length_power:
        summary["length_power"] = True
        summary["p"] = p
    if exponent_sum or length_power:
        summary["base"] = base
    independence = last_control_independence(family)
    if independence.get("independent"):
        summary["remainder_independent_of_last"] = True
        summary["variables"] = independence.get("variables")
        summary["exact_relation"] = independence.get("exact_relation")
    return summary


def compose_power_word(
    base: int,
    p: int,
    r: int,
    word: Sequence[int],
) -> tuple[int, int, int]:
    """Evaluate the certified power-family composition on a word.

    Uses ``compose_affine_steps``; does not reimplement the composition law.
    """
    steps = tuple((base ** int(k), p, r) for k in word)
    return compose_affine_steps(steps)


def last_control_independence(family: Mapping[str, Any] | None) -> dict[str, Any]:
    """C of prefix+(k) is independent of last k, derived from composition."""
    if family is None:
        return {"independent": False}
    base = int(family.get("base") or family.get("q_base") or 0)
    if "p" not in family or "r" not in family or base < 2:
        return {"independent": False}
    p = int(family["p"])
    r = int(family["r"])
    for length in (2, 3):
        for prefix in product(range(3), repeat=length - 1):
            values = {
                compose_power_word(base, p, r, prefix + (last,))[2]
                for last in (0, 1, 2, 5)
            }
            if len(values) != 1:
                return {"independent": False}
    return {
        "independent": True,
        "variables": ("prefix_sum", "length"),
        "exact_relation": "C(prefix+(k,)) = p*C_prefix + r*A_prefix",
        "identity_remainder": r,
        "divisibility_mode": "SYMBOLIC_DIVISIBILITY",
    }


def last_k_threshold(base: int, p: int, r: int, length: int) -> int | None:
    """Smallest last-control bound that forces |A-B| > |C| for every prefix.

    Conservative: uses the P=0 worst case of
    ``base^k > |r| * length * max(1,|p|)^{length-1} + |p|^length``.
    """
    if r == 0 or length < 2 or base < 2:
        return None
    coeff = abs(r) * length * max(1, abs(p)) ** (length - 1)
    p_pow = abs(p) ** length
    for k_min in range(1, 49):
        if base ** k_min > coeff + p_pow:
            return k_min
    return None


def _word_divides(base: int, p: int, r: int, word: Sequence[int]) -> bool:
    a, b, c = compose_power_word(base, p, r, word)
    left = a - b
    if left == 0:
        return c == 0
    return c % left == 0


def _scan_dividing_words(
    base: int,
    p: int,
    r: int,
    length: int,
    last_values: Sequence[int],
    max_pre: int,
    *,
    skip_zero_remainder: bool = False,
) -> tuple[tuple[int, ...], ...]:
    hits: list[tuple[int, ...]] = []
    for prefix in product(range(max_pre + 1), repeat=length - 1):
        for last in last_values:
            word = prefix + (last,)
            a, b, c = compose_power_word(base, p, r, word)
            if skip_zero_remainder and c == 0:
                continue
            left = a - b
            divides = (c == 0) if left == 0 else (c % left == 0)
            if divides:
                hits.append(word)
    return tuple(hits)


def _bound_holds(base: int, p: int, r: int, word: Sequence[int]) -> bool:
    a, b, c = compose_power_word(base, p, r, word)
    if c == 0:
        return True
    return abs(a - b) > abs(c)


def length_one_divisor_class(
    base: int,
    p: int,
    r: int,
) -> dict[str, Any]:
    """Length-1 cycle ``(base^k - p) x = r``. Possible k are a finite divisor class."""
    if r == 0:
        return {"possible_k": None, "empty": False, "reason": "r=0 admits x=0"}
    possible: list[int] = []
    for divisor in _divisors(r):
        power = divisor + p
        exponent = _power_exponent(power, base)
        if exponent is None:
            continue
        left = base ** exponent - p
        if left != 0 and r % left == 0:
            possible.append(exponent)
    possible_k = tuple(sorted(set(possible)))
    return {
        "possible_k": possible_k,
        "empty": not possible_k,
        "divisors": _divisors(r),
        "reason": (
            "no exponent makes (base^k - p) divide r"
            if not possible_k
            else "length-1 cycle requires base^k - p in the divisor set of r"
        ),
    }


def _word_cycle_obstruction(relation: Mapping[str, Any]) -> ControlObstructionCertificate | None:
    a = int(relation["a"])
    b = int(relation["b"])
    c = int(relation["c"])
    left = a - b
    word = tuple(relation.get("word", {}).get("parameters") or ())
    constraint = {"kind": "CYCLE_CONSTRAINT", "left": left, "right": c, "word": word}
    if left == 0:
        if c != 0:
            return ControlObstructionCertificate(
                kind=ObstructionKind.DIVISIBILITY.value,
                scope=ObstructionScope.WORD.value,
                status=ObstructionStatus.LEAN_CERTIFIED.value,
                reason="A=B and C≠0: (A-B)x=C has no integer x",
                constraint=constraint,
                summary={"word": word},
                contradiction={"left": left, "right": c},
                lean=LEAN_DVD,
            )
        return None
    if c % left != 0:
        common = gcd(abs(left), abs(c))
        kind = ObstructionKind.GCD.value if common != abs(left) else ObstructionKind.DIVISIBILITY.value
        status = (
            ObstructionStatus.LEAN_CERTIFIED.value
            if abs(left) > abs(c) and c != 0
            else ObstructionStatus.PROVED.value
        )
        lean = LEAN_ABS if status == ObstructionStatus.LEAN_CERTIFIED.value else LEAN_CYCLE_DVD
        return ControlObstructionCertificate(
            kind=kind,
            scope=ObstructionScope.WORD.value,
            status=status,
            reason="(A-B) does not divide C",
            constraint=constraint,
            summary={"word": word},
            contradiction={"left": left, "right": c, "gcd": common, "modulus": abs(left)},
            lean=lean,
        )
    return None


def _length_one_family_obstructions(
    family: Mapping[str, Any],
    relations: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> list[ControlObstructionCertificate]:
    base = int(family.get("base") or family.get("q_base") or 0)
    p = int(family["p"])
    r = int(family["r"])
    if base < 2:
        return []
    classification = length_one_divisor_class(base, p, r)
    possible = classification.get("possible_k")
    certificates: list[ControlObstructionCertificate] = []
    constraint = {
        "kind": "CYCLE_CONSTRAINT",
        "form": "(base^k - p) x = r",
        "base": base,
        "p": p,
        "r": r,
        "length": 1,
    }
    if possible is None:
        return []
    observed: list[int] = []
    for item in relations:
        word = tuple((item.get("word") or {}).get("parameters") or ())
        if len(word) == 1:
            observed.append(int(word[0]))
    surviving = [k for k in observed if k in set(possible)]
    refuted = False
    for item in relations:
        word = tuple((item.get("word") or {}).get("parameters") or ())
        if len(word) != 1:
            continue
        k = int(word[0])
        if k in set(possible):
            continue
        left = (base ** k) - p
        if left != 0 and r % left == 0:
            refuted = True
            certificates.append(
                ControlObstructionCertificate(
                    kind=ObstructionKind.DIVISIBILITY.value,
                    scope=ObstructionScope.CLASS.value,
                    status=ObstructionStatus.REFUTED.value,
                    reason="enumerated word outside the divisor class still divides",
                    constraint=constraint,
                    summary=dict(summary),
                    contradiction={"k": k, "left": left, "right": r},
                )
            )
    if refuted:
        return certificates
    status = ObstructionStatus.LEAN_CERTIFIED.value
    certificates.append(
        ControlObstructionCertificate(
            kind=ObstructionKind.DIVISIBILITY.value,
            scope=ObstructionScope.CLASS.value,
            status=status,
            reason=str(classification["reason"]),
            constraint=constraint,
            summary={**dict(summary), "possible_k": possible, "length": 1},
            contradiction={
                "empty": classification["empty"],
                "possible_k": possible,
                "surviving_observed_k": tuple(surviving),
            },
            lean=LEAN_DVD,
        )
    )
    if r != 0:
        certificates.append(
            ControlObstructionCertificate(
                kind=ObstructionKind.BOUND.value,
                scope=ObstructionScope.CLASS.value,
                status=ObstructionStatus.LEAN_CERTIFIED.value,
                reason="if |base^k - p| > |r| and r≠0 then (base^k - p) does not divide r",
                constraint=constraint,
                summary={**dict(summary), "length": 1},
                contradiction={"bound": abs(r)},
                lean=LEAN_ABS,
            )
        )
    return certificates


def _modular_length_class(
    relations: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> list[ControlObstructionCertificate]:
    by_length: dict[int, list[Mapping[str, Any]]] = {}
    for item in relations:
        length = int((item.get("word") or {}).get("length") or 0)
        if length:
            by_length.setdefault(length, []).append(item)
    certificates: list[ControlObstructionCertificate] = []
    for length, group in by_length.items():
        coefficients = {(int(item["a"]), int(item["b"])) for item in group}
        if len(coefficients) != 1:
            continue
        a, b = next(iter(coefficients))
        left = a - b
        if left == 0:
            continue
        modulus = abs(left)
        blocked = [
            tuple((item.get("word") or {}).get("parameters") or ())
            for item in group
            if int(item["c"]) % left != 0
        ]
        allowed = [
            tuple((item.get("word") or {}).get("parameters") or ())
            for item in group
            if int(item["c"]) % left == 0
        ]
        if not blocked:
            continue
        certificates.append(
            ControlObstructionCertificate(
                kind=ObstructionKind.MODULAR.value,
                scope=ObstructionScope.CLASS.value,
                status=ObstructionStatus.PROVED.value,
                reason="length-m words with fixed (A,B) require (A-B)|C",
                constraint={
                    "kind": "CYCLE_CONSTRAINT",
                    "left": left,
                    "length": length,
                    "a": a,
                    "b": b,
                },
                summary={**dict(summary), "length": length, "modulus": modulus},
                contradiction={
                    "modulus": modulus,
                    "blocked_words": tuple(blocked),
                    "allowed_words": tuple(allowed),
                },
                lean=LEAN_CYCLE_DVD,
            )
        )
    return certificates


def _domain_suffix_class(
    family: Mapping[str, Any],
    relations: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> list[ControlObstructionCertificate]:
    p = int(family["p"])
    r = int(family["r"])
    base = int(family.get("base") or family.get("q_base") or 2)
    alphabet = tuple(int(item) for item in family.get("observed_k") or ())
    forbidden = tuple(k for k in alphabet if subsequent_k_impossible(p, r, base, k))
    if not forbidden:
        return []
    blocked = [
        tuple((item.get("word") or {}).get("parameters") or ())
        for item in relations
        if any(int(part) in forbidden for part in (item.get("word") or {}).get("parameters", ())[1:])
    ]
    return [
        ControlObstructionCertificate(
            kind=ObstructionKind.DOMAIN.value,
            scope=ObstructionScope.CLASS.value,
            status=ObstructionStatus.PROVED.value,
            reason="later-step parameter cannot occur on residues coprime to the family base",
            constraint={"kind": "DOMAIN_INTERSECTION", "forbidden_later_k": forbidden},
            summary=dict(summary),
            contradiction={"forbidden_later_k": forbidden, "blocked_words": tuple(blocked)},
        )
    ]


def _sign_domain_word(
    spec: ProblemSpec,
    realizability: Sequence[Mapping[str, Any]],
) -> list[ControlObstructionCertificate]:
    certificates: list[ControlObstructionCertificate] = []
    phase = spec.initial_phase()
    for item in realizability:
        candidate = item.get("cycle_candidate")
        if candidate is None:
            continue
        try:
            controls = spec.legal_controls((int(candidate),), phase)
        except (TypeError, ValueError):
            continue
        if controls:
            continue
        word = tuple(item.get("word") or ())
        certificates.append(
            ControlObstructionCertificate(
                kind=ObstructionKind.SIGN.value,
                scope=ObstructionScope.WORD.value,
                status=ObstructionStatus.PROVED.value,
                reason="unique cycle candidate is outside the spec domain",
                constraint={"kind": "CYCLE_CONSTRAINT", "word": word, "candidate": int(candidate)},
                summary={"word": word},
                contradiction={"candidate": int(candidate)},
            )
        )
    return certificates


_PROVED_STATUSES = {
    ObstructionStatus.PROVED.value,
    ObstructionStatus.LEAN_CERTIFIED.value,
    ObstructionStatus.SYMBOLICALLY_PROVED.value,
}


def _length_m_total_refutation(
    family: Mapping[str, Any],
    summary: Mapping[str, Any],
    length: int,
) -> ControlObstructionCertificate | None:
    """Attack 'all length-m words are impossible' before any class claim."""
    base = int(family.get("base") or family.get("q_base") or 0)
    p = int(family["p"])
    r = int(family["r"])
    if base < 2 or length < 2:
        return None
    exceptions = _scan_dividing_words(base, p, r, length, range(0, 6), max_pre=4)
    if not exceptions:
        return ControlObstructionCertificate(
            kind=ObstructionKind.DIVISIBILITY.value,
            scope=ObstructionScope.CLASS.value,
            status=ObstructionStatus.CANDIDATE.value,
            reason="no dividing length-m word in the finite probe; not a class theorem",
            constraint={"kind": "CYCLE_CONSTRAINT", "length": length, "form": "all words"},
            summary={**dict(summary), "length": length},
            contradiction={"probe_max": 4, "divisibility_mode": "CLASS_DIVISIBILITY"},
        )
    return ControlObstructionCertificate(
        kind=ObstructionKind.DIVISIBILITY.value,
        scope=ObstructionScope.CLASS.value,
        status=ObstructionStatus.REFUTED.value,
        reason="all-length-m impossibility is false; dividing words exist",
        constraint={"kind": "CYCLE_CONSTRAINT", "length": length, "form": "all words"},
        summary={**dict(summary), "length": length, "divisibility_mode": "CLASS_DIVISIBILITY"},
        contradiction={"exceptions": exceptions[:16], "exception_count": len(exceptions)},
    )


def _symbolic_last_k_obstructions(
    family: Mapping[str, Any],
    relations: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> list[ControlObstructionCertificate]:
    """Infinite class: last control ≥ k_min implies |A-B| > |C|, so D does not divide C."""
    base = int(family.get("base") or family.get("q_base") or 0)
    if "p" not in family or "r" not in family or base < 2:
        return []
    p = int(family["p"])
    r = int(family["r"])
    independence = last_control_independence(family)
    if not independence.get("independent"):
        return []
    certificates: list[ControlObstructionCertificate] = []
    for length in (2, 3):
        total = _length_m_total_refutation(family, summary, length)
        if total is not None:
            certificates.append(total)
        k_min = last_k_threshold(base, p, r, length)
        if k_min is None:
            continue
        constraint = {
            "kind": "CYCLE_CONSTRAINT",
            "form": "(A-B)x=C with A=base^{P+k}, remainder independent of last k",
            "base": base,
            "p": p,
            "r": r,
            "length": length,
        }
        bumped = k_min
        in_class_hits: tuple[tuple[int, ...], ...] = ()
        while bumped <= 48:
            in_class_hits = _scan_dividing_words(
                base, p, r, length, (bumped,), max_pre=4, skip_zero_remainder=True
            )
            bound_ok = all(
                _bound_holds(base, p, r, prefix + (bumped,))
                for prefix in product(range(5), repeat=length - 1)
            )
            if not in_class_hits and bound_ok:
                break
            bumped += 1
        else:
            certificates.append(
                ControlObstructionCertificate(
                    kind=ObstructionKind.BOUND.value,
                    scope=ObstructionScope.SYMBOLIC_CLASS.value,
                    status=ObstructionStatus.FINITE_RANGE_SUPPORTED.value,
                    reason="last-k bound did not clear counterexamples up to the search cap",
                    constraint=constraint,
                    summary={
                        **dict(summary),
                        **independence,
                        "length": length,
                        "k_min": k_min,
                        "symbolic": True,
                        "divisibility_mode": "SYMBOLIC_DIVISIBILITY",
                    },
                    contradiction={"in_class_hits": in_class_hits, "cap": 48},
                )
            )
            continue
        enumerated_hits = []
        for item in relations:
            word = tuple((item.get("word") or {}).get("parameters") or ())
            if len(word) != length or int(word[-1]) < bumped:
                continue
            _, _, remainder = compose_power_word(base, p, r, word)
            if remainder == 0:
                continue
            if _word_divides(base, p, r, word):
                enumerated_hits.append(word)
        if enumerated_hits or in_class_hits:
            certificates.append(
                ControlObstructionCertificate(
                    kind=ObstructionKind.BOUND.value,
                    scope=ObstructionScope.SYMBOLIC_CLASS.value,
                    status=ObstructionStatus.REFUTED.value,
                    reason="a word in the proposed last-k class still divides",
                    constraint=constraint,
                    summary={**dict(summary), "length": length, "k_min": bumped, "symbolic": True},
                    contradiction={
                        "in_class_hits": in_class_hits,
                        "enumerated_hits": tuple(enumerated_hits),
                    },
                )
            )
            continue
        certificates.append(
            ControlObstructionCertificate(
                kind=ObstructionKind.BOUND.value,
                scope=ObstructionScope.SYMBOLIC_CLASS.value,
                status=ObstructionStatus.LEAN_CERTIFIED.value,
                reason=(
                    "remainder C is independent of the last control; "
                    f"last k ≥ {bumped} and C≠0 forces |A-B| > |C|, hence D does not divide C"
                ),
                constraint=constraint,
                summary={
                    **dict(summary),
                    **independence,
                    "length": length,
                    "k_min": bumped,
                    "symbolic": True,
                    "class": f"last k ≥ {bumped} and C≠0",
                    "divisibility_mode": "SYMBOLIC_DIVISIBILITY",
                },
                contradiction={
                    "empty_in_class": True,
                    "k_min": bumped,
                    "exceptions_outside_class": (
                        total.contradiction.get("exceptions") if total is not None else ()
                    ),
                },
                lean=LEAN_BOUND,
            )
        )
        certificates.append(
            ControlObstructionCertificate(
                kind=ObstructionKind.DIVISIBILITY.value,
                scope=ObstructionScope.SYMBOLIC_CLASS.value,
                status=ObstructionStatus.LEAN_CERTIFIED.value,
                reason="last-step remainder p*C_prefix + r*A_prefix does not depend on last k",
                constraint=constraint,
                summary={
                    **dict(summary),
                    **independence,
                    "length": length,
                    "symbolic": True,
                    "divisibility_mode": "SYMBOLIC_DIVISIBILITY",
                },
                contradiction={"remainder_independent_of_last": True},
                lean=LEAN_LAST,
            )
        )
    return certificates


def run_control_obstruction(spec: ProblemSpec, context: AttackContext) -> tuple[ControlObstructionCertificate, ...]:
    prior = next(
        (item for item in reversed(context.prior_results) if getattr(item, "name", None) == "control_word"),
        None,
    )
    if prior is None:
        return ()
    evidence = prior.evidence
    family = evidence.get("family")
    relations = evidence.get("relations") or ()
    realizability = evidence.get("realizability") or ()
    quotient = evidence.get("quotient") or ()
    summary = discover_summary(family, relations)
    if quotient:
        summary = {**summary, "quotient_size": len(quotient)}
    certificates: list[ControlObstructionCertificate] = []
    seen_coefficients: set[tuple[int, int, int]] = set()
    for item in relations:
        key = (int(item["a"]), int(item["b"]), int(item["c"]))
        if key in seen_coefficients:
            continue
        seen_coefficients.add(key)
        word_cert = _word_cycle_obstruction(item)
        if word_cert is not None:
            certificates.append(word_cert)
    if family:
        certificates.extend(_length_one_family_obstructions(family, relations, summary))
        certificates.extend(_domain_suffix_class(family, relations, summary))
        certificates.extend(_symbolic_last_k_obstructions(family, relations, summary))
    certificates.extend(_modular_length_class(relations, summary))
    certificates.extend(_sign_domain_word(spec, realizability))
    return tuple(certificates)


class ControlObstructionAttack:
    """Search for class-level arithmetic contradictions. Does not seed a map law."""

    name = "control_obstruction"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return any(getattr(item, "name", None) == "control_word" for item in context.prior_results)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not self.applicable(spec, context):
            return inapplicable(
                self.name,
                "control-obstruction needs a prior control_word certificate",
                ClaimKind.REACHABLE,
            )
        certificates = run_control_obstruction(spec, context)
        proved = tuple(
            item
            for item in certificates
            if item.status in _PROVED_STATUSES
            and item.scope
            in {ObstructionScope.CLASS.value, ObstructionScope.SYMBOLIC_CLASS.value}
        )
        word_proved = tuple(
            item
            for item in certificates
            if item.status in _PROVED_STATUSES
            and item.scope == ObstructionScope.WORD.value
        )
        symbolic = tuple(
            item for item in proved if item.scope == ObstructionScope.SYMBOLIC_CLASS.value
        )
        evidence = {
            "certificates": tuple(item.as_dict() for item in certificates),
            "class_count": len(proved),
            "word_count": len(word_proved),
            "symbolic_count": len(symbolic),
            "certificate_count": len(certificates),
            "symbolic": bool(symbolic),
            "lean": LEAN_BOUND if symbolic else (LEAN_DVD if proved or word_proved else ""),
            "reconstructed_affine": None,
        }
        if proved:
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=(
                    f"{len(proved)} class-level control-word obstruction(s)"
                    + (f", {len(symbolic)} symbolic" if symbolic else "")
                    + "; a cycle obstruction is not a cycle theorem"
                ),
                evidence=evidence,
                certificates=tuple(item.as_dict() for item in proved),
                certificate_kind=CertificateKind.EXACT_ARITHMETIC_IDENTITY,
                recommended_next_attacks=("closure",),
            )
        if word_proved:
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=(
                    f"{len(word_proved)} word-level obstruction(s); "
                    "family-level impossibility remains unresolved"
                ),
                evidence=evidence,
                certificates=tuple(item.as_dict() for item in word_proved),
                recommended_next_attacks=("closure",),
            )
        if certificates:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="obstruction candidates remain unproved; search failure is not impossibility",
                evidence=evidence,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.INCONCLUSIVE,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim="no arithmetic obstruction derived from the composed constraints",
            evidence=evidence,
        )
