"""One-shot scan: Lean floor that kills L=19, orbit sizes, leftover lengths."""

from __future__ import annotations

import math
from math import isqrt


def o_min(length: int) -> int:
    pow2 = 1 << length
    pow3 = 1
    odd = 0
    while pow3 <= pow2:
        pow3 *= 3
        odd += 1
    return odd


def needed_nlnn(length: int) -> float:
    odd = o_min(length)
    gap = 3**odd - (1 << length)
    return length * (3**odd) / gap


# Lean finance: n log n > L * 3^o / (3^o - 2^L)
TARGET_19 = needed_nlnn(19)
print("L=19 needed n ln n", TARGET_19)
print("297 ln 297", 297 * math.log(297))
print("256 ln 256", 256 * math.log(256))
print("255 ln 255", 255 * math.log(255))

smallest = None
for n in range(2, 400):
    if n * math.log(n) > TARGET_19:
        smallest = n
        print("smallest n with n ln n > target", n, n * math.log(n))
        break

E = 2.7182818286  # exp_one_lt_d9


def d9_ok(n: int, a: int, b: int) -> bool:
    # E^a < n^b  (sufficient for exp(a/b) < n)
    return E**a < n**b


def search_fraction(n: int) -> tuple[int, int] | None:
    need = TARGET_19 / n
    for b in range(1, 21):
        for a in range(1, 80):
            if a / b <= need:
                continue
            if d9_ok(n, a, b):
                return a, b
    return None


print("fractions:")
for n in range(smallest or 255, 320):
    frac = search_fraction(n)
    if frac:
        a, b = frac
        print(f"  n={n} a/b={a}/{b}={a/b:.6f} n*a/b={n*a/b:.4f} needed={TARGET_19:.4f}")
        break
else:
    print("  no fraction b<=20")
    for n in (256, 257, 259, 271, 277, 281, 293, 297, 307):
        print("  try", n, "need", TARGET_19 / n, "ln", math.log(n))


def orbit(n: int) -> tuple[int, int, int]:
    x = n
    steps = 0
    peak_bits = x.bit_length()
    peak = x
    while x != 1:
        if x % 2 == 0:
            x = isqrt(x)
        else:
            x = isqrt(x * x * x)
        steps += 1
        bits = x.bit_length()
        if bits > peak_bits:
            peak_bits = bits
            peak = x
        if steps > 10000:
            return steps, peak_bits, -1
    return steps, peak_bits, peak if peak_bits < 80 else 0


print("orbit scan odds 53..319")
worst_steps = (0, 0)
worst_bits = (0, 0)
for n in range(53, 320, 2):
    steps, bits, _ = orbit(n)
    if steps > worst_steps[0]:
        worst_steps = (steps, n)
    if bits > worst_bits[0]:
        worst_bits = (bits, n)
print("worst steps", worst_steps, "worst bits", worst_bits)

print("lengths that survive 53 but die at candidate floors")
floor_nlnn = {
    53: 53 * math.log(53),
    256: 256 * math.log(256),
    271: 271 * math.log(271),
    297: 297 * math.log(297),
}
print("floor nlnn", {k: round(v, 3) for k, v in floor_nlnn.items()})
for length in range(19, 90):
    need = needed_nlnn(length)
    s53 = need >= floor_nlnn[53]
    s256 = need >= floor_nlnn[256]
    s271 = need >= floor_nlnn[271]
    if s53:
        print(
            f"  L={length} o={o_min(length)} need={need:.1f} "
            f"surv53={s53} surv256={s256} surv271={s271}"
        )
