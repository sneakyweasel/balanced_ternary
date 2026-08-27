"""Packed O/E words. LSB is the first symbol; 0=E, 1=O."""

from __future__ import annotations

from math import gcd


def pack_word(word: str) -> tuple[int, int]:
    packed = 0
    for i, letter in enumerate(word):
        if letter == "O":
            packed |= 1 << i
        elif letter != "E":
            raise ValueError(f"invalid word letter {letter!r}")
    return len(word), packed


def unpack_word(length: int, packed: int) -> str:
    if length < 0:
        raise ValueError("length must be nonnegative")
    return "".join("O" if (packed >> i) & 1 else "E" for i in range(length))


def word_id(length: int, packed: int) -> int:
    return (length << 32) | packed


def split_word_id(wid: int) -> tuple[int, int]:
    return wid >> 32, wid & 0xFFFFFFFF


def dense_index(length: int, packed: int) -> int:
    return (1 << length) - 2 + packed


def dense_size(k_max: int) -> int:
    if k_max < 0:
        raise ValueError("k_max must be nonnegative")
    if k_max == 0:
        return 0
    return (1 << (k_max + 1)) - 2


def odd_count(length: int, packed: int) -> int:
    mask = (1 << length) - 1 if length else 0
    return (packed & mask).bit_count()


def run_signature(length: int, packed: int) -> str:
    if length == 0:
        return ""
    parts: list[str] = []
    bit = packed & 1
    run = 1
    for i in range(1, length):
        nxt = (packed >> i) & 1
        if nxt == bit:
            run += 1
        else:
            parts.append(f"{'O' if bit else 'E'}{run}")
            bit = nxt
            run = 1
    parts.append(f"{'O' if bit else 'E'}{run}")
    return ",".join(parts)


def append_symbol(length: int, packed: int, odd: int) -> tuple[int, int]:
    if odd not in (0, 1):
        raise ValueError("symbol must be 0 (E) or 1 (O)")
    return length + 1, packed | (odd << length)


def word_metadata(length: int, packed: int) -> dict[str, int | str]:
    o = odd_count(length, packed)
    e = length - o
    pow3 = 3**o
    pow2 = 1 << length
    g = gcd(pow3, pow2)
    return {
        "word_id": word_id(length, packed),
        "length": length,
        "packed": packed,
        "odd_count": o,
        "even_count": e,
        "run_signature": run_signature(length, packed),
        "exponent_surplus": pow3 - pow2,
        "exponent_deficit": pow2 - pow3,
        "beta_num": pow3 // g,
        "beta_den": pow2 // g,
    }


def all_words(k_max: int) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for length in range(1, k_max + 1):
        for packed in range(1 << length):
            rows.append(word_metadata(length, packed))
    return rows
