"""View-model for the finite-dynamics note companion.

Instantiates existing Juggler maps. Does not prove anything: Lean remains
the authority. Bit caps keep Streamlit reruns bounded.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from typing import Any

from research.juggler_sequence.cycle_length_seven import (
    cycle_word_hits,
    orbit_until_fail,
)
from research.juggler_sequence.cycle_ooo_scale import cyclemin_orientation
from research.juggler_sequence.cycle_word import follows_word, image_after
from research.juggler_sequence.envelope_defect import BIT_LIMIT, tiny_deficit
from research.juggler_sequence.expansion_slack import FOUR_BLOCK
from research.juggler_sequence.floor_cells import even_cell, odd_cell_integers
from research.juggler_sequence.global_defect import (
    compose_formula,
    is_monochrome,
    local_defect,
    pow_gap,
)
from research.juggler_sequence.power_words import floor_power, odd_count, regime_of
from research.juggler_sequence.progress_coverage import coverage_bucket, first_even_residual

ORBIT_STEPS_MAX = 80
DISPLAY_BITS_MAX = 256
DEFECT_BITS = BIT_LIMIT
WORD_MAX = 8
CYCLE_WORD_MAX = 16
LEFTOVER_REPLAY_MAX = 256
DESCENT_WINDOW_MAX = 500
EVEN_CELL_LIST_MAX = 40

N_PRESETS: dict[str, int] = {
    "3 (note orbit)": 3,
    "37 (note peak)": 37,
    "1999 (four-block)": 1999,
}

WORD_PRESETS: tuple[str, ...] = (
    "OOE",
    "OOOEE",
    "OOOEOE",
    "OOOOEE",
    "OOOOEOE",
    "OOOOOEE",
)

CYCLE_WORD_PRESETS: tuple[str, ...] = (
    "OEO",
    "OOE",
    "EOOOOE",
    "OEOOOE",
    "OOOEOE",
    "OOOOEE",
    "OOEOOE",
    "OOOOOOEE",
    "OOEOOOOE",
    "OOOOOO",
)

THREE_EVEN_LEFTOVER = "OOOOOOEEE"

_EXCLUDING_KINDS = frozenset(
    {
        "all-odd",
        "all-even",
        "not expanding",
        "odd-run",
        "threshold",
        "bootstrap",
        "leftover",
        "two-even leftover",
        "three-even leftover",
        "excluded",
    }
)

NOTE_PEAK_37 = 24_906_114_455_136
NOTE_ORBIT_3: tuple[int, ...] = (3, 5, 11, 36, 6, 2, 1)

LEFTOVER_CUTOFF: dict[str, int] = {
    "OOOEOE": 256,
    "OOOOEE": 256,
    "OOOOEOE": 14,
    "OOOOOEE": 14,
}

# Note classifications for even-terminating expanding words of length ≤ 7.
# Length 8 is open and is not listed here.
_WORD_CLASS: dict[str, tuple[str, str]] = {
    "OOE": ("threshold", "Lemma 3.4(i): OO next-square vs last-even cell"),
    "OOOE": ("odd-run", "Lemma 3.4(v)"),
    "OOOOE": ("odd-run", "Lemma 3.4(v)"),
    "OOOOOE": ("odd-run", "Lemma 3.4(v)"),
    "EOOOOE": ("rotation", "rotates onto OOOOEE"),
    "OEOOOE": ("rotation", "rotates onto OOOEOE"),
    "OOEOOE": ("bootstrap", "Theorem 3.6: cycle-min + OO threshold"),
    "OOOEOE": ("leftover", "Lemma 3.5"),
    "OOOOEE": ("leftover", "Lemma 3.5"),
    "OOOOOOE": ("odd-run", "Lemma 3.4(v)"),
    "EOOOOOE": ("rotation", "rotates onto OOOOOEE"),
    "OEOOOOE": ("rotation", "rotates onto OOOOEOE"),
    "OOEOOOE": ("bootstrap", "Lemma 3.4(ii) at threshold 3"),
    "OOOEOOE": ("bootstrap", "Lemma 3.4(i) at threshold 5"),
    "OOOOEOE": ("leftover", "Lemma 3.7"),
    "OOOOOEE": ("leftover", "Lemma 3.7"),
}

CLAIM_ROWS: tuple[dict[str, str], ...] = (
    {
        "text": "Theorem 2.1 fixed-word monotonicity",
        "lean": "image_monotone_of_follows",
        "ledger": "J-fixed-word-image-monotone",
    },
    {
        "text": "Theorem 2.2 / Corollary 2.3 power envelope",
        "lean": "power_bound_word / power_bound_contracts",
        "ledger": "J-power-envelope-contraction",
    },
    {
        "text": "Theorems 2.4–2.6 global defect",
        "lean": "global_defect_identity / global_defect_append",
        "ledger": "J-global-defect-identity",
    },
    {
        "text": "Lemma 3.1 odd cells unique",
        "lean": "odd_cell_unique",
        "ledger": "J-inverse-cell-asymmetry",
    },
    {
        "text": "Theorem 3.2 cycle restrictions",
        "lean": "cycle_word_formally_expanding",
        "ledger": "J-cycle-finite-structure",
    },
    {
        "text": "Lemma 3.5 leftovers OOOEOE, OOOOEE",
        "lean": "no_cycle_word_oooeoe / no_cycle_word_ooooee",
        "ledger": "J-leftover-length-six-orientations",
    },
    {
        "text": "Theorem 3.6 census length ≤ 6",
        "lean": "no_cycle_word_length_le_six",
        "ledger": "J-small-cycle-census",
    },
    {
        "text": "Lemma 3.7 leftovers OOOOEOE, OOOOOEE",
        "lean": "no_cycle_word_ooooeoe / no_cycle_word_oooooee",
        "ledger": "J-leftover-length-seven-orientations",
    },
    {
        "text": "Theorem 3.8 census length ≤ 7",
        "lean": "no_cycle_word_length_le_seven",
        "ledger": "J-small-cycle-census-seven",
    },
    {
        "text": "Theorem 4.1 uniform short certificates",
        "lean": "even_finiteProgress / odd_even_finiteProgress",
        "ledger": "J-finite-progress-boundary",
    },
)

CENSUS_LEDGER_IDS: tuple[str, ...] = (
    "J-small-cycle-census",
    "J-small-cycle-census-seven",
    "J-leftover-length-six-orientations",
    "J-leftover-length-seven-orientations",
)


def parse_word(raw: str) -> str | None:
    """Return a canonical O/E word, or None if the spelling is invalid."""

    word = "".join(raw.split()).upper()
    if len(word) > WORD_MAX:
        return None
    if word and any(letter not in {"O", "E"} for letter in word):
        return None
    return word


def parse_cycle_word(raw: str) -> str | None:
    """Return a canonical O/E cycle word, allowing the two-even lengths."""

    word = "".join(raw.split()).upper()
    if len(word) > CYCLE_WORD_MAX:
        return None
    if word and any(letter not in {"O", "E"} for letter in word):
        return None
    return word


def rotate_cycle_word(word: str, shift: int = 1) -> str:
    """Rotate `word` left by `shift` letters."""

    if not word:
        return word
    step = shift % len(word)
    return word[step:] + word[:step]


def cycle_rotations(word: str) -> tuple[str, ...]:
    if not word:
        return ("",)
    return tuple(rotate_cycle_word(word, index) for index in range(len(word)))


def two_even_family(word: str) -> str | None:
    length = len(word)
    if length < 6:
        return None
    if word == "O" * (length - 2) + "EE":
        return "EE"
    if word == "O" * (length - 3) + "EOE":
        return "EOE"
    return None


def format_int(value: int) -> str:
    text = str(value)
    if len(text) <= 18:
        return text
    return f"{text[:6]}…{text[-4:]} ({len(text)} digits)"


def _pow_bits(base: int, exp: int) -> int:
    if exp <= 0 or base <= 1:
        return 1
    return max(1, abs(base).bit_length() * exp)


def expanding(word: str) -> bool:
    return 2 ** len(word) < 3 ** odd_count(word)


def length_eight_open_words() -> tuple[str, ...]:
    found: list[str] = []
    for prefix in product("OE", repeat=7):
        word = "".join(prefix) + "E"
        if expanding(word):
            found.append(word)
    return tuple(found)


@dataclass(frozen=True)
class OrbitView:
    n: int
    steps_asked: int
    states: tuple[int, ...]
    word: str
    reached_one: bool
    bit_capped: bool
    too_large: bool
    rows: tuple[dict[str, Any], ...]


def walk_orbit(n: int, steps: int) -> OrbitView:
    if n < 1:
        raise ValueError("walk_orbit requires n ≥ 1")
    cap = min(max(steps, 0), ORBIT_STEPS_MAX)
    if n.bit_length() > DISPLAY_BITS_MAX:
        return OrbitView(
            n=n,
            steps_asked=cap,
            states=(n,),
            word="",
            reached_one=n == 1,
            bit_capped=True,
            too_large=True,
            rows=({"step": 0, "state": n, "letter": "", "parity": "odd" if n % 2 else "even", "bits": n.bit_length()},),
        )
    path = [n]
    letters: list[str] = []
    bit_capped = False
    current = n
    for _ in range(cap):
        if current.bit_length() > DISPLAY_BITS_MAX:
            bit_capped = True
            break
        letter = "O" if current % 2 else "E"
        nxt = floor_power(current)
        if nxt.bit_length() > DISPLAY_BITS_MAX:
            bit_capped = True
            letters.append(letter)
            path.append(nxt)
            break
        letters.append(letter)
        path.append(nxt)
        current = nxt
        if current == 1:
            break
    rows = []
    for index, state in enumerate(path):
        letter = letters[index] if index < len(letters) else ""
        rows.append(
            {
                "step": index,
                "state": state,
                "letter": letter,
                "parity": "odd" if state % 2 else "even",
                "bits": state.bit_length(),
            }
        )
    return OrbitView(
        n=n,
        steps_asked=cap,
        states=tuple(path),
        word="".join(letters),
        reached_one=path[-1] == 1,
        bit_capped=bit_capped,
        too_large=False,
        rows=tuple(rows),
    )


@dataclass(frozen=True)
class EnvelopeView:
    n: int
    word: str
    odd: int
    length: int
    regime: str
    follows: bool
    fail_index: int | None
    fail_state: int | None
    image: int | None
    compared: str
    slack: int | None
    slack_too_large: bool
    delta: int | None
    delta_too_large: bool
    monochrome: bool
    vanishing: str
    steps: tuple[dict[str, Any], ...]


def _defect_steps(n: int, word: str) -> tuple[tuple[dict[str, Any], ...], int | None, bool]:
    current = n
    running = 0
    ok = True
    rows: list[dict[str, Any]] = []
    for index, letter in enumerate(word):
        parity_ok = (letter == "O" and current % 2 == 1) or (
            letter == "E" and current % 2 == 0
        )
        rho = local_defect(current) if parity_ok else None
        nxt = floor_power(current) if parity_ok else None
        d_out: int | None = None
        if parity_ok and ok and nxt is not None and rho is not None:
            exp = 2**index
            if letter == "E":
                if _pow_bits(nxt * nxt + rho, exp) > DEFECT_BITS:
                    ok = False
                else:
                    running = running + pow_gap(nxt * nxt, rho, exp)
                    d_out = running
            else:
                if (
                    _pow_bits(nxt * nxt + rho, exp) > DEFECT_BITS
                    or _pow_bits(current, exp) > DEFECT_BITS
                ):
                    ok = False
                else:
                    lifted = current**exp
                    running = pow_gap(nxt * nxt, rho, exp) + pow_gap(lifted, running, 3)
                    d_out = running
        rows.append(
            {
                "index": index,
                "state": current,
                "letter": letter,
                "parity_ok": parity_ok,
                "rho": rho,
                "image": nxt,
                "D": d_out if parity_ok else None,
            }
        )
        if not parity_ok:
            break
        assert nxt is not None
        current = nxt
    delta = running if ok and (not word or rows[-1]["parity_ok"]) else None
    return tuple(rows), delta, not ok


def envelope_view(n: int, word: str) -> EnvelopeView:
    if n < 1:
        raise ValueError("envelope_view requires n ≥ 1")
    parsed = parse_word(word)
    if parsed is None:
        raise ValueError("envelope_view requires an O/E word of length ≤ 8")
    word = parsed
    odds = odd_count(word)
    follows = follows_word(n, word) if word else True
    fail_index = None
    fail_state = None
    if word and not follows:
        failed = next((row for row in orbit_until_fail(n, word) if not row["parity_ok"]), None)
        if failed is not None:
            fail_index = int(failed["index"])
            fail_state = int(failed["state"])
    image = image_after(n, word) if follows else None
    compared = "—"
    if image is not None:
        if image < n:
            compared = "<"
        elif image > n:
            compared = ">"
        else:
            compared = "="
    slack = None
    slack_too_large = False
    if image is not None:
        slack = tiny_deficit(n, image, len(word), odds, bit_limit=DEFECT_BITS)
        slack_too_large = slack is None
    steps, delta, delta_too_large = _defect_steps(n, word) if follows else ((), None, False)
    if follows and word and delta is None and not delta_too_large:
        delta_too_large = slack_too_large
    mixed = bool(word) and not is_monochrome(word)
    if not follows:
        vanishing = "word not realized"
    elif not word:
        vanishing = "empty word, Δ = 0"
    elif mixed:
        vanishing = "mixed word, Δ > 0"
    elif delta == 0:
        vanishing = "monochrome tower, Δ = 0"
    elif any(row["rho"] for row in steps):
        vanishing = "monochrome but a local remainder is positive"
    else:
        vanishing = "monochrome; Δ not instantiated"
    return EnvelopeView(
        n=n,
        word=word,
        odd=odds,
        length=len(word),
        regime=regime_of(len(word), odds) if word else "empty",
        follows=follows,
        fail_index=fail_index,
        fail_state=fail_state,
        image=image,
        compared=compared,
        slack=slack,
        slack_too_large=slack_too_large,
        delta=delta,
        delta_too_large=delta_too_large,
        monochrome=is_monochrome(word),
        vanishing=vanishing,
        steps=steps,
    )


@dataclass(frozen=True)
class ComposeView:
    n: int
    u: str
    v: str
    follows: bool
    mid: int | None
    end: int | None
    delta_u: int | None
    delta_v: int | None
    delta_uv: int | None
    composed: int | None
    too_large: bool


def compose_view(n: int, u: str, v: str) -> ComposeView:
    if n < 1:
        raise ValueError("compose_view requires n ≥ 1")
    left = parse_word(u)
    right = parse_word(v)
    if left is None or right is None:
        raise ValueError("compose_view requires O/E factors of total length ≤ 8")
    if len(left) + len(right) > WORD_MAX:
        raise ValueError("compose_view requires |uv| ≤ 8")
    word = left + right
    follows = follows_word(n, word) if word else True
    if not follows:
        return ComposeView(n, left, right, False, None, None, None, None, None, None, False)
    mid = image_after(n, left) if left else n
    end = image_after(mid, right) if right else mid
    slack_u = tiny_deficit(n, mid, len(left), odd_count(left), bit_limit=DEFECT_BITS)
    slack_v = tiny_deficit(mid, end, len(right), odd_count(right), bit_limit=DEFECT_BITS)
    slack_uv = tiny_deficit(n, end, len(word), odd_count(word), bit_limit=DEFECT_BITS)
    too_large = slack_u is None or slack_v is None or slack_uv is None
    composed = None
    if not too_large:
        u_bits = _pow_bits(mid, 2 ** len(left)) if left else 1
        v_bits = _pow_bits(end, 2 ** len(right)) if right else 1
        if u_bits <= DEFECT_BITS and v_bits <= DEFECT_BITS:
            composed = compose_formula(n, left, right)
    return ComposeView(
        n=n,
        u=left,
        v=right,
        follows=True,
        mid=mid,
        end=end,
        delta_u=slack_u,
        delta_v=slack_v,
        delta_uv=slack_uv,
        composed=composed,
        too_large=too_large,
    )


@dataclass(frozen=True)
class EvenCellView:
    q: int
    lo: int
    hi: int
    even_count: int
    evens: tuple[int, ...]
    truncated: bool


def even_cell_view(q: int) -> EvenCellView:
    if q < 0:
        raise ValueError("even_cell_view requires q ≥ 0")
    lo, hi = even_cell(q)
    evens = tuple(range(lo + (lo % 2), hi, 2))
    truncated = len(evens) > EVEN_CELL_LIST_MAX
    shown = evens[:EVEN_CELL_LIST_MAX] if truncated else evens
    return EvenCellView(
        q=q,
        lo=lo,
        hi=hi,
        even_count=len(evens),
        evens=shown,
        truncated=truncated,
    )


@dataclass(frozen=True)
class OddCellView:
    m: int
    integers: tuple[int, ...]


def odd_cell_view(m: int) -> OddCellView:
    if m < 0:
        raise ValueError("odd_cell_view requires m ≥ 0")
    return OddCellView(m=m, integers=tuple(odd_cell_integers(m)))


@dataclass(frozen=True)
class WordClass:
    word: str
    length: int
    odd: int
    expanding: bool
    even_terminating: bool
    kind: str
    reason: str


def classify_word(word: str) -> WordClass:
    parsed = parse_word(word)
    if parsed is None:
        raise ValueError("classify_word requires an O/E word of length ≤ 8")
    word = parsed
    is_exp = expanding(word) if word else False
    even_term = bool(word) and word.endswith("E")
    if not word:
        kind, reason = "empty", "empty word"
    elif not even_term:
        kind, reason = "odd-terminating", "census reduces to an even-terminating rotation"
    elif not is_exp:
        kind, reason = "not expanding", "Theorem 3.2(i): a cycle word is formally expanding"
    elif word in _WORD_CLASS:
        kind, reason = _WORD_CLASS[word]
    elif len(word) <= 7:
        kind, reason = "excluded", "note census of length ≤ 7"
    else:
        kind, reason = "open", "length eight is the first open even-terminating expanding length"
    return WordClass(
        word=word,
        length=len(word),
        odd=odd_count(word),
        expanding=is_exp,
        even_terminating=even_term,
        kind=kind,
        reason=reason,
    )


def census_inventory(*, max_len: int = 7) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for length in range(3, max_len + 1):
        for prefix in product("OE", repeat=length - 1):
            word = "".join(prefix) + "E"
            if not expanding(word):
                continue
            info = classify_word(word)
            rows.append(
                {
                    "word": info.word,
                    "k": info.length,
                    "o": info.odd,
                    "kind": info.kind,
                    "reason": info.reason,
                }
            )
    return tuple(rows)


@dataclass(frozen=True)
class LeftoverTable:
    word: str
    n_lo: int
    n_hi: int
    checked: int
    follows: int
    hits: tuple[int, ...]
    rows: tuple[dict[str, Any], ...]


@lru_cache(maxsize=8)
def leftover_table(word: str, n_hi: int | None = None) -> LeftoverTable:
    parsed = parse_word(word)
    if parsed is None or parsed not in LEFTOVER_CUTOFF:
        raise ValueError("leftover_table requires a note leftover word")
    cutoff = LEFTOVER_CUTOFF[parsed]
    hi = cutoff if n_hi is None else min(n_hi, cutoff, LEFTOVER_REPLAY_MAX)
    summary = cycle_word_hits(parsed, 2, hi)
    rows: list[dict[str, Any]] = []
    for n in range(2, hi):
        ok = follows_word(n, parsed)
        image = image_after(n, parsed) if ok else None
        rows.append(
            {
                "n": n,
                "realized": ok,
                "image": image,
                "returned": bool(ok and image == n),
            }
        )
    return LeftoverTable(
        word=parsed,
        n_lo=2,
        n_hi=hi,
        checked=int(summary["checked"]),
        follows=int(summary["follows"]),
        hits=tuple(summary["hits"]),
        rows=tuple(rows),
    )


@dataclass(frozen=True)
class NextSquareView:
    n: int
    prefix: str
    follows: bool
    image: int | None
    threshold: int
    met: bool | None


def next_square_view(n: int, prefix: str) -> NextSquareView:
    if n < 1:
        raise ValueError("next_square_view requires n ≥ 1")
    parsed = parse_word(prefix)
    if parsed not in {"OO", "OOO"}:
        raise ValueError("next_square_view requires prefix OO or OOO")
    threshold = (n + 1) ** 2
    ok = follows_word(n, parsed)
    image = image_after(n, parsed) if ok else None
    met = None if image is None else image >= threshold
    return NextSquareView(
        n=n,
        prefix=parsed,
        follows=ok,
        image=image,
        threshold=threshold,
        met=met,
    )


@dataclass(frozen=True)
class DescentView:
    n: int
    bucket: str
    certificate: str
    residual: dict[str, Any] | None


def descent_view(n: int) -> DescentView:
    if n < 1:
        raise ValueError("descent_view requires n ≥ 1")
    bucket = coverage_bucket(n)
    if bucket == "EVEN_PROGRESS":
        certificate = "E"
    elif bucket == "OE_PROGRESS":
        certificate = "OE"
    elif bucket == "ODD_ODD":
        certificate = "none of length ≤ 2"
    else:
        certificate = "—"
    residual = first_even_residual(n) if n >= 2 else None
    return DescentView(n=n, bucket=bucket, certificate=certificate, residual=residual)


def descent_window(n_max: int) -> dict[str, int]:
    cap = min(max(n_max, 2), DESCENT_WINDOW_MAX)
    counts = {"EVEN_PROGRESS": 0, "OE_PROGRESS": 0, "ODD_ODD": 0, "EXCLUDED": 0}
    for n in range(2, cap + 1):
        counts[coverage_bucket(n)] += 1
    counts["n_max"] = cap
    return counts


@dataclass(frozen=True)
class ChainStep:
    start: int
    word: str
    image: int
    follows: bool
    matches: bool


def four_block_replay() -> tuple[ChainStep, ...]:
    starts = FOUR_BLOCK["xs"]
    words = FOUR_BLOCK["words"]
    steps: list[ChainStep] = []
    for index, word in enumerate(words):
        start = int(starts[index])
        expected = int(starts[index + 1])
        ok = follows_word(start, word)
        image = image_after(start, word) if ok else -1
        steps.append(
            ChainStep(
                start=start,
                word=word,
                image=image,
                follows=ok,
                matches=ok and image == expected,
            )
        )
    return tuple(steps)


def leftover_words() -> tuple[str, ...]:
    return tuple(LEFTOVER_CUTOFF)


@dataclass(frozen=True)
class ArgumentStep:
    title: str
    body: str
    status: str
    ledger: str | None = None


@dataclass(frozen=True)
class RotationRow:
    shift: int
    word: str
    even_terminating: bool
    expanding: bool
    legal_cyclemin: bool
    blocked_by: str | None
    kind: str
    reason: str
    selected: bool


@dataclass(frozen=True)
class CycleTryView:
    n: int
    word: str
    follows: bool
    fail_index: int | None
    fail_state: int | None
    image: int | None
    returned: bool | None
    bit_capped: bool


@dataclass(frozen=True)
class CycleClassView:
    word: str
    current: str
    shift: int
    length: int
    odd: int
    even: int
    expanding: bool
    verdict: str
    verdict_reason: str
    ledger: str | None
    steps: tuple[ArgumentStep, ...]
    rotations: tuple[RotationRow, ...]
    legal_reps: tuple[str, ...]
    current_kind: str
    current_reason: str
    current_legal: bool
    current_blocked_by: str | None


def _is_odd_run(word: str) -> bool:
    return (
        len(word) >= 4
        and word.endswith("E")
        and word[:-1] == "O" * (len(word) - 1)
    )


def _orientation_ledger(kind: str, word: str) -> str | None:
    if kind in {"all-odd", "all-even", "not expanding", "odd-terminating"}:
        return "J-cycle-finite-structure"
    if kind == "odd-run":
        return "J-small-cycle-census-seven" if len(word) <= 7 else "J-cycle-finite-structure"
    if kind == "leftover":
        if word in {"OOOEOE", "OOOOEE"}:
            return "J-leftover-length-six-orientations"
        if word in {"OOOOEOE", "OOOOOEE"}:
            return "J-leftover-length-seven-orientations"
        return "J-small-cycle-census-seven"
    if kind == "two-even leftover":
        return "J-two-even-leftover-ee" if word.endswith("EE") else "J-two-even-leftover-eoe"
    if kind == "three-even leftover":
        return "J-leftover-ooooooeee"
    if kind in {"threshold", "bootstrap", "rotation", "excluded", "not CycleMin"}:
        return "J-small-cycle-census-seven" if len(word) <= 7 else "J-small-cycle-census"
    return None


def _base_kind(word: str) -> tuple[str, str]:
    """Classify one spelling without chasing a rotation target."""

    if not word:
        return "empty", "empty word"
    if all(letter == "O" for letter in word):
        return "all-odd", "an all-odd word is a strict ascent and cannot close"
    if all(letter == "E" for letter in word):
        return "all-even", "Theorem 3.2(i): a cycle word is formally expanding"
    if not expanding(word):
        return "not expanding", "Theorem 3.2(i): a cycle word is formally expanding"
    if not word.endswith("E"):
        return "odd-terminating", "census reduces to an even-terminating rotation"
    if _is_odd_run(word):
        odds = len(word) - 1
        return "odd-run", f"no_cycle_odd_run_append_even for O^{odds}E, a ≥ 3"
    if word == THREE_EVEN_LEFTOVER:
        return "three-even leftover", "OOOOOOEEE is excluded (no_cycle_word_ooooooeee)"
    named = _WORD_CLASS.get(word)
    if named is not None and named[0] != "rotation":
        return named
    family = two_even_family(word)
    if family == "EE":
        return (
            "two-even leftover",
            f"O^{len(word) - 2}EE is excluded for every k ≥ 6 "
            "(no_cycle_word_two_even_ee)",
        )
    if family == "EOE":
        return (
            "two-even leftover",
            f"O^{len(word) - 3}EOE is excluded for every k ≥ 6 "
            "(no_cycle_word_two_even_eoe)",
        )
    if word.startswith("E"):
        return "rotation", "rotate the leading evens onto an even-terminating spelling"
    if word.startswith("OE"):
        return "not CycleMin", "cycleMin_not_odd_even"
    if named is not None:
        return named
    if len(word) <= 7:
        return "excluded", "note census of length ≤ 7"
    return "open", "not excluded by the recorded census"


def _preferred_target(word: str) -> str | None:
    named: list[str] = []
    legal: list[str] = []
    even_term: list[str] = []
    for rotated in cycle_rotations(word):
        kind, _reason = _base_kind(rotated)
        if rotated.endswith("E") and kind in _EXCLUDING_KINDS:
            named.append(rotated)
        if rotated and cyclemin_orientation(rotated)["legal_cyclemin"] and expanding(rotated):
            legal.append(rotated)
        if rotated.endswith("E"):
            even_term.append(rotated)
    if named:
        return named[0]
    if legal:
        return legal[0]
    if even_term:
        return even_term[0]
    return None


def _with_target(kind: str, reason: str, word: str) -> tuple[str, str]:
    if kind not in {"odd-terminating", "rotation", "not CycleMin"}:
        return kind, reason
    target = _preferred_target(word)
    if not target or target == word:
        return kind, reason
    if kind == "odd-terminating":
        return kind, f"rotate onto the even-terminating spelling {target}"
    if kind == "rotation":
        return kind, f"rotates onto {target}"
    return kind, f"cycleMin_not_odd_even; the even-terminating target is {target}"


def _orientation_kind(word: str) -> tuple[str, str]:
    kind, reason = _base_kind(word)
    return _with_target(kind, reason, word)


def orientation_obstruction(word: str) -> tuple[str, str, str | None]:
    parsed = parse_cycle_word(word)
    if parsed is None:
        raise ValueError("orientation_obstruction requires an O/E word of length ≤ 16")
    kind, reason = _orientation_kind(parsed)
    return kind, reason, _orientation_ledger(kind, parsed)


def try_cycle_word(n: int, word: str) -> CycleTryView:
    if n < 1:
        raise ValueError("try_cycle_word requires n ≥ 1")
    parsed = parse_cycle_word(word)
    if parsed is None:
        raise ValueError("try_cycle_word requires an O/E word of length ≤ 16")
    if n.bit_length() > DISPLAY_BITS_MAX:
        return CycleTryView(n, parsed, False, None, None, None, None, True)
    current = n
    for index, letter in enumerate(parsed):
        if current.bit_length() > DISPLAY_BITS_MAX:
            return CycleTryView(n, parsed, False, index, current, None, None, True)
        parity_ok = (letter == "O" and current % 2 == 1) or (
            letter == "E" and current % 2 == 0
        )
        if not parity_ok:
            return CycleTryView(n, parsed, False, index, current, None, None, False)
        nxt = floor_power(current)
        if nxt.bit_length() > DISPLAY_BITS_MAX:
            return CycleTryView(n, parsed, False, index, current, None, None, True)
        current = nxt
    return CycleTryView(
        n=n,
        word=parsed,
        follows=True,
        fail_index=None,
        fail_state=None,
        image=current,
        returned=bool(parsed) and current == n,
        bit_capped=False,
    )


def _class_verdict(
    word: str,
    legal: tuple[str, ...],
) -> tuple[str, str, str | None]:
    if not word:
        return "empty", "empty word", None
    kind, reason = _orientation_kind(word)
    if kind in {"all-odd", "all-even", "not expanding"}:
        return "excluded", reason, _orientation_ledger(kind, word)
    if not legal:
        return (
            "excluded",
            "no legal CycleMin orientation exists in this rotation class",
            "J-cycle-finite-structure",
        )
    open_reps = []
    excluded_reps = []
    for rep in legal:
        rep_kind, rep_reason = _orientation_kind(rep)
        if rep_kind == "open":
            open_reps.append((rep, rep_reason))
        elif rep_kind in _EXCLUDING_KINDS:
            excluded_reps.append((rep, rep_kind, rep_reason))
        else:
            open_reps.append((rep, rep_reason))
    if open_reps:
        sample = open_reps[0][0]
        return (
            "open",
            f"{sample} is a legal CycleMin spelling that the recorded census does not exclude",
            None,
        )
    if not excluded_reps:
        return "open", "not excluded by the recorded census", None
    first = excluded_reps[0]
    return "excluded", first[2], _orientation_ledger(first[1], first[0])


def cycle_class_view(word: str, shift: int = 0) -> CycleClassView:
    parsed = parse_cycle_word(word)
    if parsed is None:
        raise ValueError("cycle_class_view requires an O/E word of length ≤ 16")
    word = parsed
    current = rotate_cycle_word(word, shift) if word else ""
    current_kind, current_reason = _orientation_kind(current)
    current_orient = (
        cyclemin_orientation(current)
        if current
        else {
            "legal_cyclemin": False,
            "blocked_by": None,
        }
    )
    rows: list[RotationRow] = []
    legal: list[str] = []
    for index, rotated in enumerate(cycle_rotations(word)):
        kind, reason = _orientation_kind(rotated)
        orientation = (
            cyclemin_orientation(rotated)
            if rotated
            else {"legal_cyclemin": False, "blocked_by": None}
        )
        if orientation["legal_cyclemin"] and expanding(rotated):
            legal.append(rotated)
        rows.append(
            RotationRow(
                shift=index,
                word=rotated,
                even_terminating=bool(rotated) and rotated.endswith("E"),
                expanding=expanding(rotated) if rotated else False,
                legal_cyclemin=bool(orientation["legal_cyclemin"]),
                blocked_by=orientation["blocked_by"],
                kind=kind,
                reason=reason,
                selected=rotated == current,
            )
        )
    legal_reps = tuple(dict.fromkeys(legal))
    verdict, verdict_reason, ledger = _class_verdict(word, legal_reps)
    odds = odd_count(word)
    evens = word.count("E")
    is_exp = expanding(word) if word else False
    mixed = bool(word) and not (odds in {0, len(word)})
    even_term_reps = tuple(row.word for row in rows if row.even_terminating)
    steps = (
        ArgumentStep(
            title="Formal expansion",
            body=(
                f"2^{len(word)} = {2 ** len(word)} compared with "
                f"3^{odds} = {3 ** odds}. A nontrivial cycle word is "
                "formally expanding."
                if word
                else "Enter a nonempty word."
            ),
            status="blocks" if word and not is_exp else "ok" if word else "info",
            ledger="J-cycle-finite-structure" if word and not is_exp else None,
        ),
        ArgumentStep(
            title="Mixed word",
            body=(
                "An all-odd word is a strict ascent and cannot return. "
                "An all-even word is not expanding. A cycle word is mixed."
                if word
                else "Empty word."
            ),
            status=(
                "blocks"
                if word and not mixed
                else "ok"
                if mixed
                else "info"
            ),
            ledger="J-cycle-finite-structure" if word and not mixed else None,
        ),
        ArgumentStep(
            title="Rotate to even-terminating",
            body=(
                "Cycle words are cyclic: if n follows w and returns, every "
                "rotation is a cycle word at a rotated start. The even-"
                f"terminating spellings are {', '.join(even_term_reps) or '—'}."
            ),
            status="ok" if even_term_reps else "info",
            ledger="J-cycle-finite-structure",
        ),
        ArgumentStep(
            title="CycleMin filter",
            body=(
                "A cycle-minimum orientation cannot start even, start OE, "
                "or end odd. Legal CycleMin spellings in this class: "
                f"{', '.join(legal_reps) or 'none'}."
            ),
            status="blocks" if word and mixed and is_exp and not legal_reps else "ok",
            ledger="J-cycle-finite-structure",
        ),
        ArgumentStep(
            title="Named obstruction",
            body=verdict_reason,
            status="blocks" if verdict == "excluded" else "open" if verdict == "open" else "info",
            ledger=ledger,
        ),
    )
    return CycleClassView(
        word=word,
        current=current,
        shift=(shift % len(word)) if word else 0,
        length=len(word),
        odd=odds,
        even=evens,
        expanding=is_exp,
        verdict=verdict,
        verdict_reason=verdict_reason,
        ledger=ledger,
        steps=steps,
        rotations=tuple(rows),
        legal_reps=legal_reps,
        current_kind=current_kind,
        current_reason=current_reason,
        current_legal=bool(current_orient["legal_cyclemin"]),
        current_blocked_by=current_orient["blocked_by"],
    )
