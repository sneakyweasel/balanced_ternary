"""Information profiles and locality classes for existing operators.

Reuses :class:`bt.operators.OperatorMetadata` and :func:`bt.transducers.zoo.zoo`.
Does not re-prove sequentiality theorems.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.operators import OPERATORS, OperatorMetadata


@dataclass(frozen=True)
class InformationProfile:
    operator: str
    reading_direction: str
    output_direction: str
    delay: str
    state_complexity: int | None
    precision_loss: str
    precision_gain: str
    locality_class: str
    proof_status: str
    notes: str

    def as_dict(self) -> dict[str, object]:
        return {
            "operator": self.operator,
            "reading_direction": self.reading_direction,
            "output_direction": self.output_direction,
            "delay": self.delay,
            "state_complexity": self.state_complexity,
            "precision_loss": self.precision_loss,
            "precision_gain": self.precision_gain,
            "locality_class": self.locality_class,
            "proof_status": self.proof_status,
            "notes": self.notes,
        }


_EXTRA: dict[str, dict[str, str]] = {
    "S": {
        "delay": "0 (append LSD 0)",
        "precision_loss": "none",
        "precision_gain": "+1 trailing zero trit",
        "locality_class": "sequential (letter-to-letter morphism)",
        "output_direction": "LSD-first (append)",
    },
    "N": {
        "delay": "0",
        "precision_loss": "none",
        "precision_gain": "none",
        "locality_class": "sequential (letter-to-letter)",
        "output_direction": "either",
    },
    "D": {
        "delay": "1 LSD consumed",
        "precision_loss": "1 least-significant trit",
        "precision_gain": "none",
        "locality_class": "sequential",
        "output_direction": "LSD-first",
    },
    "Im": {
        "delay": "0 (produce LSD -1)",
        "precision_loss": "none",
        "precision_gain": "+1 least-significant trit",
        "locality_class": "sequential",
        "output_direction": "LSD-first (prepend)",
    },
    "Ip": {
        "delay": "0 (produce LSD +1)",
        "precision_loss": "none",
        "precision_gain": "+1 least-significant trit",
        "locality_class": "sequential",
        "output_direction": "LSD-first (prepend)",
    },
    "I0": {
        "delay": "0 (append LSD 0)",
        "precision_loss": "none",
        "precision_gain": "+1 trailing zero trit",
        "locality_class": "sequential (alias of S)",
        "output_direction": "LSD-first (append)",
    },
    "K3": {
        "delay": "unbounded trailing zeros, finite state (2)",
        "precision_loss": "all factors of 3",
        "precision_gain": "none",
        "locality_class": "sequential",
        "output_direction": "LSD-first",
    },
    "M2": {
        "delay": "1 carry trit",
        "precision_loss": "none",
        "precision_gain": "possible extra MSD from carry",
        "locality_class": "sequential",
        "output_direction": "LSD-first",
    },
    "H2": {
        "delay": "1 carry trit (domain 2Z)",
        "precision_loss": "the factor 2",
        "precision_gain": "none",
        "locality_class": "sequential on 2Z",
        "output_direction": "LSD-first",
    },
    "H3": {
        "delay": "1 LSD (must be 0)",
        "precision_loss": "the factor 3",
        "precision_gain": "none",
        "locality_class": "sequential on 3Z",
        "output_direction": "LSD-first",
    },
    "W": {
        "delay": "unbounded (needs word length / MSD)",
        "precision_loss": "canonical trailing zeros after reverse",
        "precision_gain": "none",
        "locality_class": "not one-way sequential",
        "output_direction": "requires both ends",
    },
    "Wz": {
        "delay": "unbounded",
        "precision_loss": "none (keeps trailing zeros)",
        "precision_gain": "none",
        "locality_class": "not one-way sequential",
        "output_direction": "requires both ends",
    },
    "Wt": {
        "delay": "unbounded",
        "precision_loss": "none",
        "precision_gain": "none",
        "locality_class": "not one-way sequential",
        "output_direction": "requires both ends",
    },
}


def _from_metadata(symbol: str, meta: OperatorMetadata) -> InformationProfile:
    extra = _EXTRA.get(symbol, {})
    cls = extra.get("locality_class")
    if cls is None:
        if meta.finite_state is True:
            cls = "sequential"
        elif meta.finite_state is False:
            cls = "not one-way sequential"
        else:
            cls = "unknown"
    return InformationProfile(
        operator=symbol,
        reading_direction=meta.reading_direction,
        output_direction=extra.get("output_direction", meta.reading_direction),
        delay=extra.get("delay", "see operator notes"),
        state_complexity=meta.state_count,
        precision_loss=extra.get("precision_loss", "see notes"),
        precision_gain=extra.get("precision_gain", "see notes"),
        locality_class=cls,
        proof_status=meta.proof_status,
        notes=meta.notes,
    )


def profile(symbol: str) -> InformationProfile:
    if symbol == "odd_part":
        return InformationProfile(
            operator="odd_part",
            reading_direction="LSD-first per fixed k only",
            output_direction="LSD-first per fixed k",
            delay="unbounded v2",
            state_complexity=None,
            precision_loss="all factors of 2",
            precision_gain="none",
            locality_class="not one rational transduction",
            proof_status="PROVED",
            notes="Existing four-step argument. Each fixed k is finite-state.",
        )
    if symbol == "T":
        return InformationProfile(
            operator="T",
            reading_direction="LSD-first on each fixed valuation branch",
            output_direction="inherits odd-part obstruction",
            delay="unbounded v2 after 3n+1",
            state_complexity=None,
            precision_loss="odd-part of 3n+1",
            precision_gain="none",
            locality_class="not one rational transduction (composition)",
            proof_status="PROVED as a composition",
            notes="3n+1 is sequential; unrestricted odd-part is not. Collatz is a client.",
        )
    op = OPERATORS.get(symbol)
    if op is None:
        raise KeyError(f"unknown operator {symbol!r}")
    return _from_metadata(symbol, op.metadata())


def all_profiles() -> tuple[InformationProfile, ...]:
    symbols = tuple(OPERATORS) + ("odd_part", "T")
    return tuple(profile(sym) for sym in symbols)
