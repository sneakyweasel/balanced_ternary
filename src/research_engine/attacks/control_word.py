"""Control-word composition of a certified parameterized affine family.

A formally composed word is not a realized trajectory. A cycle constraint
is not evidence that a cycle exists.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import gcd
from typing import Any

from research_engine.attacks.parameter_domain import ParameterDomain, predicate_holds
from research_engine.attacks.piecewise_affine import (
    DEFAULT_FALSIFY_WINDOW,
    DEFAULT_SAMPLE_WINDOW,
    _collect_samples,
    _eval_map,
    _is_power_of_base,
)
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope

LEAN_COMPOSITION = "Problems.Engine.compose_two_affine"
LEAN_CYCLE = "Problems.Engine.cycle_of_composed"

MAX_WORD_LENGTH = 3
MAX_WORDS = 36


class WordEvidence(str, Enum):
    ALGEBRAICALLY_COMPOSED = "ALGEBRAICALLY_COMPOSED"
    DOMAIN_SUPPORTED = "DOMAIN_SUPPORTED"
    REALIZABLE = "REALIZABLE"
    CYCLE_CONSTRAINT_PROVED = "CYCLE_CONSTRAINT_PROVED"
    LEAN_CERTIFIED = "LEAN_CERTIFIED"


class Realizability(str, Enum):
    REALIZABLE = "REALIZABLE"
    REALIZABLE_FOR_SOME_SEED = "REALIZABLE_FOR_SOME_SEED"
    IMPOSSIBLE = "IMPOSSIBLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ControlWord:
    """Finite parameter sequence. Not a realized orbit."""

    parameters: tuple[int, ...]
    kind: str = "concrete"

    @property
    def length(self) -> int:
        return len(self.parameters)

    def as_dict(self) -> dict[str, Any]:
        return {"parameters": self.parameters, "kind": self.kind, "length": self.length}


@dataclass(frozen=True)
class ComposedAffineRelation:
    """Cleared relation ``A x_m = B x_0 + C``. Integer coefficients only."""

    word: ControlWord
    a: int
    b: int
    c: int
    evidence: str
    lean: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "word": self.word.as_dict(),
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "evidence": self.evidence,
            "lean": self.lean,
            "reconstructed_affine": None,
        }


@dataclass(frozen=True)
class ControlWordConstraint:
    kind: str
    left: int
    right: int
    evidence: str
    modulus: int | None = None
    residue: int | None = None

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "kind": self.kind,
            "left": self.left,
            "right": self.right,
            "evidence": self.evidence,
        }
        if self.modulus is not None:
            payload["modulus"] = self.modulus
        if self.residue is not None:
            payload["residue"] = self.residue
        return payload


@dataclass(frozen=True)
class ControlComposition:
    family: Mapping[str, Any] | None
    relations: tuple[ComposedAffineRelation, ...]
    constraints: tuple[ControlWordConstraint, ...]
    realizability: tuple[Mapping[str, Any], ...]
    quotient: tuple[Mapping[str, Any], ...]
    impossible_words: tuple[tuple[int, ...], ...]
    queries: int
    lean: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "family": None if self.family is None else dict(self.family),
            "relations": tuple(item.as_dict() for item in self.relations),
            "constraints": tuple(item.as_dict() for item in self.constraints),
            "realizability": self.realizability,
            "quotient": self.quotient,
            "impossible_words": self.impossible_words,
            "queries": self.queries,
            "word_count": len(self.relations),
            "quotient_size": len(self.quotient),
            "lean": self.lean,
            "reconstructed_affine": None,
        }


def compose_affine_steps(steps: Sequence[tuple[int, int, int]]) -> tuple[int, int, int]:
    """``a y = b x + c`` composed left-to-right. Identity is ``1·x = 1·x + 0``."""
    a_tot, b_tot, c_tot = 1, 1, 0
    for a, b, c in steps:
        a_tot, b_tot, c_tot = a_tot * a, b * b_tot, b * c_tot + c * a_tot
    return a_tot, b_tot, c_tot


def cycle_constraint(a: int, b: int, c: int) -> ControlWordConstraint:
    """``A x = B x + C`` implies ``(A-B) x = C``. Not existence of a cycle."""
    left = a - b
    modulus = abs(left) if left != 0 else None
    residue = None
    if left != 0 and c % left == 0 and modulus:
        residue = (c // left) % modulus
    return ControlWordConstraint(
        kind="CYCLE_CONSTRAINT",
        left=left,
        right=c,
        evidence=WordEvidence.CYCLE_CONSTRAINT_PROVED.value,
        modulus=modulus,
        residue=residue,
    )


def _alphabet(family: Mapping[str, Any], domains: Sequence[Mapping[str, Any]]) -> tuple[int, ...]:
    observed = family.get("observed_k") if family else None
    if observed:
        return tuple(int(item) for item in observed)
    labels = tuple(int(item["parameter"]) for item in domains if "parameter" in item)
    return labels or ()


def _step_coefficients(
    k: int,
    family: Mapping[str, Any] | None,
    branches: Sequence[Mapping[str, Any]],
) -> tuple[int, int, int]:
    if family:
        base = int(family.get("base") or family.get("q_base") or 2)
        p = int(family["p"])
        r = int(family["r"])
        return base ** k, p, r
    branch = next((item for item in branches if int(item.get("parameter", -1)) == k), None)
    if branch is None and 0 <= k < len(branches):
        branch = branches[k]
    if branch is None:
        raise KeyError(k)
    q = int(branch.get("q") or 1)
    p = int(branch["p"])
    r = int(branch["r"])
    return q, p, r


def _parameter_of_step(x: int, y: int, p: int, r: int, base: int) -> int | None:
    target = p * x + r
    if y == 0:
        return 0 if target == 0 else None
    if target % y != 0:
        return None
    return _is_power_of_base(target // y, base)


def _branch_index_of_step(
    x: int,
    y: int,
    branches: Sequence[Mapping[str, Any]],
) -> int | None:
    for index, branch in enumerate(branches):
        q = int(branch.get("q") or 1)
        p = int(branch["p"])
        r = int(branch["r"])
        if q * y != p * x + r:
            continue
        region = branch.get("domain") or branch.get("region") or {}
        kind = str(region.get("kind", ""))
        if kind and kind not in {"unknown", ""}:
            domain = ParameterDomain(
                kind,
                {key: value for key, value in region.items() if key != "kind"},
            )
            if not predicate_holds(domain, x, p, r, 2):
                continue
        return int(branch.get("parameter", index))
    return None


def subsequent_k_impossible(p: int, r: int, base: int, k: int) -> bool:
    """If every residue coprime to ``base`` has valuation ≠ k, later k is impossible.

    The test uses modulus ``base^{k+1}`` so it is not secretly a mod-2 trap.
    Failure to prove impossibility is not impossibility.
    """
    if base < 2 or k < 0:
        return False
    try:
        modulus = base ** (k + 1)
    except OverflowError:
        return False
    if modulus > 4096:
        return False
    residues = [res for res in range(modulus) if gcd(res, base) == 1]
    if not residues:
        return False
    matches = 0
    for res in residues:
        value = p * res + r
        if k == 0:
            if value % base != 0:
                matches += 1
        else:
            power = base ** k
            if value % power == 0 and value % (power * base) != 0:
                matches += 1
    return matches == 0


def _enumerate_words(alphabet: Sequence[int], max_length: int, cap: int) -> tuple[tuple[int, ...], ...]:
    words: list[tuple[int, ...]] = []
    for length in range(1, max_length + 1):
        for word in product(alphabet, repeat=length):
            words.append(tuple(int(item) for item in word))
            if len(words) >= cap:
                return tuple(words)
    return tuple(words)


def _realize_word(
    spec: ProblemSpec,
    word: Sequence[int],
    family: Mapping[str, Any] | None,
    branches: Sequence[Mapping[str, Any]],
    window: Sequence[int],
) -> tuple[str, tuple[int, ...], int]:
    phase = spec.initial_phase()
    queries = 0
    seeds: list[int] = []
    p = int(family["p"]) if family else 0
    r = int(family["r"]) if family else 0
    base = int(family.get("base") or family.get("q_base") or 2) if family else 2
    for value in window:
        queries += 1
        current = int(value)
        ok = True
        for k in word:
            image = _eval_map(spec, current, phase)
            if image is None:
                ok = False
                break
            if family is not None:
                got = _parameter_of_step(current, image, p, r, base)
            else:
                got = _branch_index_of_step(current, image, branches)
            if got != k:
                ok = False
                break
            current = image
        if ok:
            seeds.append(int(value))
            if len(seeds) >= 4:
                break
    if seeds:
        return Realizability.REALIZABLE_FOR_SOME_SEED.value, tuple(seeds[:4]), queries
    return Realizability.UNKNOWN.value, (), queries


def compose_certified_family(
    spec: ProblemSpec,
    context: AttackContext,
    family: Mapping[str, Any] | None,
    domains: Sequence[Mapping[str, Any]],
    branches: Sequence[Mapping[str, Any]],
) -> ControlComposition:
    alphabet = _alphabet(family or {}, domains)
    if not alphabet and branches:
        alphabet = tuple(range(len(branches)))
    words = _enumerate_words(alphabet, MAX_WORD_LENGTH, MAX_WORDS)
    relations: list[ComposedAffineRelation] = []
    constraints: list[ControlWordConstraint] = []
    realizability: list[dict[str, Any]] = []
    impossible: list[tuple[int, ...]] = []
    queries = 0
    groups: dict[tuple[int, int, int], list[tuple[int, ...]]] = defaultdict(list)
    coprime_obstruction: set[int] = set()
    if family is not None:
        p = int(family["p"])
        r = int(family["r"])
        base = int(family.get("base") or family.get("q_base") or 2)
        for k in alphabet:
            if subsequent_k_impossible(p, r, base, k):
                coprime_obstruction.add(k)
    samples = _collect_samples(spec, context, DEFAULT_SAMPLE_WINDOW)
    window: Sequence[int] = tuple(samples) if samples else DEFAULT_FALSIFY_WINDOW
    for raw in words:
        steps = tuple(_step_coefficients(k, family, branches) for k in raw)
        a, b, c = compose_affine_steps(steps)
        composed = ComposedAffineRelation(
            word=ControlWord(raw),
            a=a,
            b=b,
            c=c,
            evidence=(
                WordEvidence.LEAN_CERTIFIED.value
                if len(raw) <= 2
                else WordEvidence.ALGEBRAICALLY_COMPOSED.value
            ),
            lean=LEAN_COMPOSITION if len(raw) <= 2 else "",
        )
        relations.append(composed)
        groups[(a, b, c)].append(raw)
        constraints.append(cycle_constraint(a, b, c))
        status, seeds, count = _realize_word(spec, raw, family, branches, window)
        queries += count
        later = raw[1:]
        if family is not None and any(k in coprime_obstruction for k in later):
            status = Realizability.IMPOSSIBLE.value
        if a == b:
            cycle_status = (
                Realizability.IMPOSSIBLE.value if c != 0 else Realizability.UNKNOWN.value
            )
            candidate = None
        elif c % (a - b) != 0:
            cycle_status = Realizability.IMPOSSIBLE.value
            candidate = None
        else:
            cycle_status = Realizability.UNKNOWN.value
            candidate = c // (a - b)
        record = {
            "word": raw,
            "status": status,
            "seeds": seeds,
            "cycle_status": cycle_status,
            "cycle_candidate": candidate,
        }
        realizability.append(record)
        if status == Realizability.IMPOSSIBLE.value:
            impossible.append(raw)
    quotient = tuple(
        {"a": key[0], "b": key[1], "c": key[2], "words": tuple(value)}
        for key, value in groups.items()
        if len(value) > 1
    )
    return ControlComposition(
        family=None if family is None else dict(family),
        relations=tuple(relations),
        constraints=tuple(constraints),
        realizability=tuple(realizability),
        quotient=quotient,
        impossible_words=tuple(impossible),
        queries=queries,
        lean=LEAN_COMPOSITION,
    )


def _prior_domain(context: AttackContext) -> Any | None:
    for item in reversed(context.prior_results):
        if getattr(item, "name", None) == "parameter_domain":
            return item
    return None


def run_control_word(spec: ProblemSpec, context: AttackContext) -> ControlComposition | None:
    prior = _prior_domain(context)
    if prior is None:
        return None
    family = prior.evidence.get("family")
    domains = prior.evidence.get("domains") or ()
    if family:
        return compose_certified_family(spec, context, family, domains, ())
    piecewise = next(
        (item for item in context.prior_results if getattr(item, "name", None) == "piecewise_affine"),
        None,
    )
    raw_branches = () if piecewise is None else (piecewise.evidence.get("branches") or ())
    if raw_branches:
        labeled = tuple({**dict(branch), "parameter": index} for index, branch in enumerate(raw_branches))
        return compose_certified_family(spec, context, None, domains, labeled)
    if domains:
        branches = tuple(
            {
                "parameter": item.get("parameter"),
                "p": (item.get("domain") or {}).get("p", 0),
                "q": (item.get("domain") or {}).get("q", 1),
                "r": (item.get("domain") or {}).get("r", 0),
                "domain": item.get("domain") or {},
            }
            for item in domains
        )
        return compose_certified_family(spec, context, None, domains, branches)
    return None


class ControlWordAttack:
    """Compose certified one-step affine relations. Does not seed a map law."""

    name = "control_word"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        prior = _prior_domain(context)
        if prior is None:
            return False
        if prior.evidence.get("family"):
            return True
        return bool(prior.evidence.get("domains"))

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not self.applicable(spec, context):
            return inapplicable(
                self.name,
                "control-word composition needs a prior parameter_domain certificate",
                ClaimKind.REACHABLE,
            )
        composition = run_control_word(spec, context)
        if composition is None or not composition.relations:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="no control words could be composed from the prior certificate",
            )
        evidence = composition.as_dict()
        some = any(
            item.get("status") == Realizability.REALIZABLE_FOR_SOME_SEED.value
            for item in composition.realizability
        )
        impossible = bool(composition.impossible_words)
        claim = (
            f"composed {len(composition.relations)} control words of a certified "
            "affine family; a cycle constraint is not a cycle"
        )
        if some or impossible:
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=claim,
                evidence=evidence,
                certificates=(evidence,),
                certificate_kind=CertificateKind.EXACT_ARITHMETIC_IDENTITY,
                recommended_next_attacks=("block", "modular", "closure"),
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim=claim + "; realizability remains unresolved on the sample window",
            evidence=evidence,
            certificates=(evidence,),
            recommended_next_attacks=("closure",),
        )
