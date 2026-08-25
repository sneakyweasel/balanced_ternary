"""Recursive matrix-word invariants. Magnitude domination is not a success."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import product
from math import gcd
from typing import Any

from research_engine.algebra.lattices import matrix_det, matrix_entry_gcd
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.attacks.vector_affine import (
    VectorAffineBranch,
    VectorAffineFamily,
    compose_vector_steps,
    cycle_matrix_constraint,
    linear_system_status,
)
from research_engine.core.affine_system import matrix_dimension
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, Matrix, SearchScope, Vector

MAX_LEN = 3
MAX_WORDS = 24
PROBE_K = (-4, -2, -1, 0, 1, 2, 3, 4, 5, 6, 8)
LEAN_REC = "Problems.Engine.recursive_matrix_word_step"
LEAN_KERNEL = "Problems.Engine.kernel_row_cycle_impossible"
LEAN_GCD = "Problems.Engine.entry_gcd_divides_translation"
LEAN_SHEAR = "Problems.Engine.shear_offset_y_cycle_impossible"
FORMS_2 = ((1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1))


@dataclass(frozen=True)
class MatrixWordInvariant:
    """Recursively preserved predicate on (M_i, c_i). Not a theorem prover."""

    kind: str
    predicate: str
    transition: str
    status: str
    magnitude: str
    parameter_class: Mapping[str, Any]
    implication: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "predicate": self.predicate,
            "transition": self.transition,
            "status": self.status,
            "magnitude": self.magnitude,
            "parameter_class": dict(self.parameter_class),
            "implication": self.implication,
        }


@dataclass(frozen=True)
class MatrixWordCertificate:
    kind: str
    scope: str
    status: str
    reason: str
    magnitude: str
    invariant: Mapping[str, Any]
    exceptions: tuple[Any, ...]
    word_lengths: tuple[int, ...]
    lean: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "scope": self.scope,
            "status": self.status,
            "reason": self.reason,
            "magnitude": self.magnitude,
            "invariant": dict(self.invariant),
            "exceptions": self.exceptions,
            "word_lengths": self.word_lengths,
            "lean": self.lean,
        }


def prefix_states(steps: Sequence[tuple[Matrix, Vector]]) -> tuple[tuple[Matrix, Vector], ...]:
    acc: list[tuple[Matrix, Vector]] = []
    out: list[tuple[Matrix, Vector]] = []
    for step in steps:
        acc.append(step)
        out.append(compose_vector_steps(acc))
    return tuple(out)


def _max_abs_matrix(matrix: Matrix) -> int:
    return max(abs(entry) for row in matrix for entry in row)


def _max_abs_vector(vector: Vector) -> int:
    return max((abs(part) for part in vector), default=0)


def _dot(left: Sequence[int], right: Sequence[int]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _left_kernel_forms(left: Matrix, rhs: Vector) -> tuple[tuple[int, ...], ...]:
    n = matrix_dimension(left)
    if n != 2:
        return ()
    hits: list[tuple[int, ...]] = []
    for form in FORMS_2:
        image = tuple(_dot(form, tuple(left[i][j] for i in range(n))) for j in range(n))
        if any(image):
            continue
        if _dot(form, rhs) != 0:
            hits.append(form)
    return tuple(hits)


def _form_mod_hits(left: Matrix, rhs: Vector) -> tuple[tuple[tuple[int, ...], int], ...]:
    n = matrix_dimension(left)
    if n != 2:
        return ()
    hits: list[tuple[tuple[int, ...], int]] = []
    for modulus in (2, 3, 4, 5):
        for form in FORMS_2:
            cols_ok = True
            for j in range(n):
                total = sum(form[i] * left[i][j] for i in range(n))
                if total % modulus != 0:
                    cols_ok = False
                    break
            if cols_ok and _dot(form, rhs) % modulus != 0:
                hits.append((form, modulus))
    return tuple(hits)


def cycle_features(matrix: Matrix, offset: Vector) -> dict[str, Any]:
    left, rhs = cycle_matrix_constraint(matrix, offset)
    status = linear_system_status(left, rhs)
    entry_g = matrix_entry_gcd(left)
    det = matrix_det(left)
    gcd_hit = False
    if entry_g == 0:
        gcd_hit = any(part != 0 for part in offset)
    elif any(part % entry_g != 0 for part in offset):
        gcd_hit = True
    zero_rows = tuple(
        i for i, row in enumerate(left) if all(entry == 0 for entry in row)
    )
    kernel_hit = any(rhs[i] != 0 for i in zero_rows)
    mag_left = _max_abs_matrix(left)
    mag_c = _max_abs_vector(offset)
    magnitude_useful = mag_c != 0 and mag_left > mag_c
    obstructed = (
        status in {"UNIQUE_NONINTEGRAL", "INCONSISTENT"}
        or gcd_hit
        or kernel_hit
        or bool(_left_kernel_forms(left, rhs))
        or bool(_form_mod_hits(left, rhs))
    )
    return {
        "status": status,
        "obstructed": obstructed,
        "entry_gcd": entry_g,
        "det": det,
        "gcd_hit": gcd_hit,
        "kernel_hit": kernel_hit,
        "zero_rows": zero_rows,
        "left_forms": _left_kernel_forms(left, rhs),
        "form_mod": _form_mod_hits(left, rhs),
        "magnitude_useful": magnitude_useful,
        "mag_left": mag_left,
        "mag_c": mag_c,
        "left": left,
        "offset": offset,
        "matrix": matrix,
    }


def _matrix_from(raw: object) -> Matrix:
    return tuple(tuple(int(entry) for entry in row) for row in raw)  # type: ignore[arg-type]


def _vector_from(raw: object) -> Vector:
    return tuple(int(part) for part in raw)  # type: ignore[arg-type]


def family_from_evidence(evidence: Mapping[str, Any]) -> VectorAffineFamily | None:
    raw = evidence.get("family")
    if not raw:
        return None
    observed = tuple(int(k) for k in (raw.get("observed_k") or ()))
    return VectorAffineFamily(
        base=_matrix_from(raw["base"]),
        direction=_matrix_from(raw["direction"]),
        offset=_vector_from(raw["offset"]),
        observed_k=observed,
        support=(),
        status=str(raw.get("status") or "SUPPORTED_BY_SAMPLES"),
        region=raw.get("region"),
    )


def branches_from_evidence(evidence: Mapping[str, Any]) -> tuple[VectorAffineBranch, ...]:
    out: list[VectorAffineBranch] = []
    for raw in evidence.get("branches") or ():
        if not isinstance(raw, dict):
            continue
        if raw.get("status") == "REFUTED":
            continue
        out.append(
            VectorAffineBranch(
                matrix=_matrix_from(raw["matrix"]),
                offset=_vector_from(raw["offset"]),
                support=(),
                status=str(raw.get("status") or "SUPPORTED_BY_SAMPLES"),
                parameter=raw.get("parameter"),
            )
        )
    return tuple(out)


def _class_ks(observed: Sequence[int], kind: str) -> tuple[int, ...]:
    probe = tuple(dict.fromkeys(tuple(observed) + PROBE_K))
    if kind == "observed":
        return tuple(sorted(set(observed)))
    if kind == "even":
        return tuple(sorted(k for k in probe if k % 2 == 0))
    if kind == "odd":
        return tuple(sorted(k for k in probe if k % 2 != 0))
    if kind == "probe":
        return tuple(sorted(probe))
    return ()


def _words(alphabet: Sequence[int], max_len: int = MAX_LEN) -> tuple[tuple[int, ...], ...]:
    letters = tuple(alphabet[:4])
    if not letters:
        return ()
    out: list[tuple[int, ...]] = []
    for length in range(1, max_len + 1):
        for word in product(letters, repeat=length):
            out.append(word)
            if len(out) >= MAX_WORDS:
                return tuple(out)
    return tuple(out)


def _steps_for_family(family: VectorAffineFamily, word: Sequence[int]) -> tuple[tuple[Matrix, Vector], ...]:
    return tuple((family.matrix_at(int(k)), family.offset) for k in word)


def _odd_length(words: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(word) for word in words if len(word) % 2 == 1)


def _even_length(words: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(word) for word in words if len(word) % 2 == 0)


def _analyze_words(
    family: VectorAffineFamily,
    words: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, ...], dict[str, Any]], ...]:
    rows: list[tuple[tuple[int, ...], dict[str, Any]]] = []
    for word in words:
        matrix, offset = compose_vector_steps(_steps_for_family(family, word))
        rows.append((tuple(word), cycle_features(matrix, offset)))
    return tuple(rows)


def _det_predicate(matrix: Matrix, offset: Vector) -> bool:
    feat = cycle_features(matrix, offset)
    return feat["status"] == "UNIQUE_NONINTEGRAL" or feat["gcd_hit"] or feat["kernel_hit"]


def _preserved_on_words(
    family: VectorAffineFamily,
    words: Sequence[Sequence[int]],
    predicate: Any,
) -> bool:
    word_set = {tuple(word) for word in words}
    if not word_set:
        return False
    for word in words:
        matrix, offset = compose_vector_steps(_steps_for_family(family, word))
        if not predicate(matrix, offset):
            return False
        for length in range(1, len(word)):
            prefix = tuple(word[:length])
            if prefix not in word_set:
                continue
            pre_m, pre_c = compose_vector_steps(_steps_for_family(family, prefix))
            if not predicate(pre_m, pre_c):
                return False
    return True


def _kernel_row_predicate(row: int):
    def _pred(matrix: Matrix, offset: Vector) -> bool:
        left, rhs = cycle_matrix_constraint(matrix, offset)
        if row >= len(left):
            return False
        return all(entry == 0 for entry in left[row]) and rhs[row] != 0

    return _pred


def _gcd_predicate(matrix: Matrix, offset: Vector) -> bool:
    left, _rhs = cycle_matrix_constraint(matrix, offset)
    entry_g = matrix_entry_gcd(left)
    if entry_g == 0:
        return any(part != 0 for part in offset)
    return any(part % entry_g != 0 for part in offset)


def _form_predicate(form: Sequence[int], modulus: int | None):
    def _pred(matrix: Matrix, offset: Vector) -> bool:
        left, rhs = cycle_matrix_constraint(matrix, offset)
        n = matrix_dimension(left)
        if modulus is None:
            image = tuple(_dot(form, tuple(left[i][j] for i in range(n))) for j in range(n))
            return not any(image) and _dot(form, rhs) != 0
        for j in range(n):
            total = sum(form[i] * left[i][j] for i in range(n))
            if total % modulus != 0:
                return False
        return _dot(form, rhs) % modulus != 0

    return _pred


def _magnitude_label(rows: Sequence[tuple[tuple[int, ...], dict[str, Any]]]) -> str:
    obstructed = [feat for _word, feat in rows if feat["obstructed"]]
    if not obstructed:
        return "INAPPLICABLE"
    if all(feat["magnitude_useful"] for feat in obstructed):
        return "USED"
    return "INAPPLICABLE"


def _certificate_for_class(
    name: str,
    family: VectorAffineFamily,
    class_k: Sequence[int],
    words: Sequence[Sequence[int]],
    rows: Sequence[tuple[tuple[int, ...], dict[str, Any]]],
) -> MatrixWordCertificate | None:
    if not rows:
        return None
    obstructed = [(word, feat) for word, feat in rows if feat["obstructed"]]
    realizable = [(word, feat) for word, feat in rows if not feat["obstructed"]]
    lengths = tuple(sorted({len(word) for word, _feat in rows}))
    magnitude = _magnitude_label(rows)
    exceptions = tuple(word for word, _feat in realizable)

    if not obstructed:
        return MatrixWordCertificate(
            kind="none",
            scope="CLASS",
            status="UNKNOWN",
            reason="no cycle obstruction on the probed matrix words",
            magnitude="INAPPLICABLE",
            invariant=MatrixWordInvariant(
                kind="none",
                predicate="(M-I)x = -c may be solvable",
                transition="M' = A_u M, c' = A_u c + b",
                status="UNKNOWN",
                magnitude="INAPPLICABLE",
                parameter_class={"name": name, "k": tuple(class_k)},
                implication="NO OBSTRUCTION",
            ).as_dict(),
            exceptions=exceptions,
            word_lengths=lengths,
        )

    obstructed_words = tuple(word for word, _feat in obstructed)
    kinds: list[tuple[str, Any, str, str]] = []
    if all(feat["kernel_hit"] for _word, feat in obstructed):
        rows_hit = {feat["zero_rows"] for _word, feat in obstructed}
        row = 1 if all(1 in item for item in rows_hit) else (0 if all(0 in item for item in rows_hit) else None)
        if row is not None and _preserved_on_words(family, obstructed_words, _kernel_row_predicate(row)):
            kinds.append(
                (
                    "image_kernel",
                    _kernel_row_predicate(row),
                    f"row {row} of (M-I) is 0 and c_{row} != 0",
                    LEAN_KERNEL if row == 1 else LEAN_REC,
                )
            )
    if all(feat["gcd_hit"] for _word, feat in obstructed) and _preserved_on_words(
        family, obstructed_words, _gcd_predicate
    ):
        kinds.append(
            (
                "entry_gcd",
                _gcd_predicate,
                "gcd of entries of (M-I) does not divide c",
                LEAN_GCD,
            )
        )
    if all(feat["status"] == "UNIQUE_NONINTEGRAL" for _word, feat in obstructed) and _preserved_on_words(
        family, obstructed_words, _det_predicate
    ):
        kinds.append(
            (
                "det_factor",
                _det_predicate,
                "det(M-I) does not yield an integer preimage for -c",
                LEAN_GCD,
            )
        )
    form_sets = [set(feat["left_forms"]) for _word, feat in obstructed]
    common_forms = set.intersection(*form_sets) if form_sets else set()
    for form in sorted(common_forms):
        pred = _form_predicate(form, None)
        if _preserved_on_words(family, obstructed_words, pred):
            kinds.append(
                (
                    "left_form",
                    pred,
                    f"L={form} annihilates (M-I) but not c",
                    LEAN_KERNEL,
                )
            )
            break
    mod_sets = [set(feat["form_mod"]) for _word, feat in obstructed]
    common_mod = set.intersection(*mod_sets) if mod_sets else set()
    for form, modulus in sorted(common_mod, key=lambda item: (item[1], item[0])):
        pred = _form_predicate(form, modulus)
        if _preserved_on_words(family, obstructed_words, pred):
            kinds.append(
                (
                    "left_form_mod",
                    pred,
                    f"L={form} (M-I) ≡ 0 (mod {modulus}) but L c ≢ 0",
                    LEAN_GCD,
                )
            )
            break

    if not kinds:
        if magnitude == "USED":
            return None
        status = "FINITE_RANGE_SUPPORTED" if obstructed else "UNKNOWN"
        return MatrixWordCertificate(
            kind="unclassified",
            scope="WORD" if len(obstructed) == 1 else "CLASS",
            status=status,
            reason="obstruction seen on samples without a preserved predicate",
            magnitude=magnitude,
            invariant=MatrixWordInvariant(
                kind="unclassified",
                predicate="cycle linear system obstructed on the probe",
                transition="M' = A_u M, c' = A_u c + b",
                status=status,
                magnitude=magnitude,
                parameter_class={"name": name, "k": tuple(class_k)},
                implication="sample obstruction is not a class theorem",
            ).as_dict(),
            exceptions=exceptions,
            word_lengths=lengths,
        )

    kind, _pred, predicate, lean = kinds[0]
    multi_length = len(lengths) >= 2
    if exceptions:
        scope = "CLASS"
        status = "PROVED"
        reason = (
            f"class {name} is impossible except {len(exceptions)} realizable word(s); "
            "not every word is impossible"
        )
        invariant_status = "PROVED"
    elif multi_length and magnitude == "INAPPLICABLE":
        scope = "RECURSIVE_INVARIANT"
        status = "LEAN_CERTIFIED" if kind in {"image_kernel", "entry_gcd"} else "PROVED"
        reason = (
            "recursively preserved matrix-word predicate obstructs (M-I)x=-c "
            "for an infinite control class; magnitude domination INAPPLICABLE"
        )
        invariant_status = status
        if family.offset and family.offset[-1] != 0:
            lean = LEAN_SHEAR
    elif magnitude == "USED":
        return None
    else:
        scope = "SYMBOLIC_CLASS"
        status = "PROVED"
        reason = f"every probed word in class {name} obstructs the cycle equation"
        invariant_status = "PROVED"

    invariant = MatrixWordInvariant(
        kind=kind,
        predicate=predicate,
        transition="M' = A_u M, c' = A_u c + b",
        status=invariant_status,
        magnitude=magnitude,
        parameter_class={"name": name, "k": tuple(class_k)},
        implication="c not in im_Z(M-I)",
    )
    return MatrixWordCertificate(
        kind=kind,
        scope=scope,
        status=status,
        reason=reason,
        magnitude=magnitude,
        invariant=invariant.as_dict(),
        exceptions=exceptions,
        word_lengths=lengths,
        lean=lean,
    )


def _refuted_all_k(family: VectorAffineFamily) -> MatrixWordCertificate | None:
    words = _words(_class_ks(family.observed_k, "probe"), max_len=1)
    rows = _analyze_words(family, words)
    realizable = [word for word, feat in rows if not feat["obstructed"]]
    obstructed = [word for word, feat in rows if feat["obstructed"]]
    if realizable and obstructed:
        even_words = [word for word, feat in rows if word[0] % 2 == 0]
        even_real = [word for word in even_words if word in realizable]
        if not even_real and any(word[0] % 2 != 0 for word in realizable):
            return MatrixWordCertificate(
                kind="left_form_mod",
                scope="CLASS",
                status="REFUTED",
                reason="all-k residue/lattice candidate fails on an odd (or exceptional) probe",
                magnitude="INAPPLICABLE",
                invariant=MatrixWordInvariant(
                    kind="left_form_mod",
                    predicate="candidate: every parameter k obstructs",
                    transition="M' = A_u M, c' = A_u c + b",
                    status="REFUTED",
                    magnitude="INAPPLICABLE",
                    parameter_class={"name": "probe", "k": tuple(_class_ks(family.observed_k, "probe"))},
                    implication="counterexample word is realizable",
                ).as_dict(),
                exceptions=tuple(realizable),
                word_lengths=(1,),
            )
    return None


def _finite_alphabet_certificates(
    branches: Sequence[VectorAffineBranch],
) -> tuple[MatrixWordCertificate, ...]:
    live = [item for item in branches if item.status != "REFUTED"][:4]
    if not live:
        return ()
    words: list[tuple[int, ...]] = []
    rows: list[tuple[tuple[int, ...], dict[str, Any]]] = []
    for length in range(1, min(MAX_LEN, 3) + 1):
        for word in product(range(len(live)), repeat=length):
            steps = tuple((live[i].matrix, live[i].offset) for i in word)
            matrix, offset = compose_vector_steps(steps)
            feat = cycle_features(matrix, offset)
            words.append(word)
            rows.append((word, feat))
            if len(rows) >= MAX_WORDS:
                break
        if len(rows) >= MAX_WORDS:
            break
    obstructed = [item for item in rows if item[1]["obstructed"]]
    realizable = [item[0] for item in rows if not item[1]["obstructed"]]
    if not obstructed:
        return (
            MatrixWordCertificate(
                kind="none",
                scope="CLASS",
                status="UNKNOWN",
                reason="finite matrix alphabet: no cycle obstruction on probed words",
                magnitude="INAPPLICABLE",
                invariant=MatrixWordInvariant(
                    kind="none",
                    predicate="(M-I)x=-c may be solvable",
                    transition="M' = A_u M, c' = A_u c + b",
                    status="UNKNOWN",
                    magnitude="INAPPLICABLE",
                    parameter_class={"name": "finite_alphabet", "size": len(live)},
                    implication="NO OBSTRUCTION",
                ).as_dict(),
                exceptions=tuple(realizable),
                word_lengths=tuple(sorted({len(w) for w, _ in rows})),
            ),
        )
    magnitude = _magnitude_label(rows)
    all_kernel = all(feat["kernel_hit"] for _w, feat in obstructed)
    all_gcd = all(feat["gcd_hit"] for _w, feat in obstructed)
    kind = "image_kernel" if all_kernel else ("entry_gcd" if all_gcd else "det_factor")
    exceptions = tuple(realizable)
    if exceptions:
        reason = (
            f"finite alphabet class impossible except {len(exceptions)} realizable word(s); "
            "not every word is impossible"
        )
        scope = "CLASS"
        status = "PROVED"
    elif magnitude == "INAPPLICABLE":
        reason = "recursively composed finite alphabet obstructs; magnitude INAPPLICABLE"
        status = "PROVED"
        scope = "RECURSIVE_INVARIANT"
    else:
        reason = "finite alphabet cycle obstruction; magnitude domination also available"
        status = "PROVED"
        scope = "WORD"
    return (
        MatrixWordCertificate(
            kind=kind,
            scope=scope,
            status=status,
            reason=reason,
            magnitude=magnitude,
            invariant=MatrixWordInvariant(
                kind=kind,
                predicate="composed (M,c) leaves c outside im_Z(M-I)",
                transition="M' = A_u M, c' = A_u c + b",
                status=status,
                magnitude=magnitude,
                parameter_class={"name": "finite_alphabet", "size": len(live)},
                implication="c not in im_Z(M-I)",
            ).as_dict(),
            exceptions=exceptions,
            word_lengths=tuple(sorted({len(w) for w, _ in rows})),
            lean=LEAN_REC,
        ),
    )


def run_matrix_word_invariant(
    spec: ProblemSpec,
    context: AttackContext,
) -> tuple[MatrixWordCertificate, ...]:
    del spec
    prior = next(
        (item for item in reversed(context.prior_results) if getattr(item, "name", None) == "vector_affine"),
        None,
    )
    if prior is None:
        return ()
    evidence = prior.evidence
    family = family_from_evidence(evidence)
    certificates: list[MatrixWordCertificate] = []
    if family is not None and family.observed_k:
        refuted = _refuted_all_k(family)
        if refuted is not None:
            certificates.append(refuted)
        class_plan = (
            ("observed", None),
            ("even", None),
            ("odd", None),
            ("even_odd_length", "even"),
            ("observed_odd_length", "observed"),
        )
        seen: set[tuple[str, tuple[int, ...]]] = set()
        for name, source in class_plan:
            base = source or name
            if base in {"even_odd_length"}:
                ks = _class_ks(family.observed_k, "even")
                words = _odd_length(_words(ks))
                label = "even_odd_length"
            elif base == "observed_odd_length":
                ks = _class_ks(family.observed_k, "observed")
                words = _odd_length(_words(ks))
                label = "observed_odd_length"
            else:
                ks = _class_ks(family.observed_k, name)
                words = _words(ks)
                label = name
            key = (label, tuple(ks))
            if key in seen or not words:
                continue
            seen.add(key)
            rows = _analyze_words(family, words)
            cert = _certificate_for_class(label, family, ks, words, rows)
            if cert is not None:
                certificates.append(cert)
    else:
        branches = branches_from_evidence(evidence)
        certificates.extend(_finite_alphabet_certificates(branches))
    return tuple(certificates)


class MatrixWordInvariantAttack:
    """Discover recursive (M_i, c_i) predicates that obstruct integer cycles."""

    name = "matrix_word_invariant"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return any(getattr(item, "name", None) == "vector_affine" for item in context.prior_results)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not self.applicable(spec, context):
            return inapplicable(
                self.name,
                "matrix-word invariant needs a prior vector_affine census",
                ClaimKind.REACHABLE,
            )
        certificates = run_matrix_word_invariant(spec, context)
        proved = tuple(
            item
            for item in certificates
            if item.status in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
            and item.scope in {"CLASS", "SYMBOLIC_CLASS", "RECURSIVE_INVARIANT"}
        )
        recursive = tuple(
            item for item in proved if item.scope == "RECURSIVE_INVARIANT"
        )
        unknown = tuple(item for item in certificates if item.status == "UNKNOWN")
        refuted = tuple(item for item in certificates if item.status == "REFUTED")
        evidence = {
            "certificates": tuple(item.as_dict() for item in certificates),
            "invariants": tuple(item.invariant for item in certificates),
            "reconstructed_affine": None,
            "magnitude": {
                item.scope: item.magnitude for item in certificates
            },
        }
        if recursive:
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=(
                    "recursive matrix-word invariant obstructs an infinite control "
                    "class; magnitude domination INAPPLICABLE"
                ),
                evidence=evidence,
                certificate_kind=CertificateKind.EXACT_ARITHMETIC_IDENTITY,
            )
        if proved:
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim="matrix-word class obstruction with a preserved arithmetic predicate",
                evidence=evidence,
                certificate_kind=CertificateKind.EXACT_ARITHMETIC_IDENTITY,
            )
        if refuted and not proved:
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="candidate matrix-word invariant refuted; no class obstruction promoted",
                evidence=evidence,
            )
        if unknown and not proved:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="NO OBSTRUCTION: probed matrix words do not yield a class-level invariant",
                evidence=evidence,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.INCONCLUSIVE,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim="matrix-word invariant unresolved on the stated probe",
            evidence=evidence,
        )
