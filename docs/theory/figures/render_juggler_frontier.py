"""Render the research-frontier figure at the same print scale as the Lean graph."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from juggler_figure_style import DEFAULT_BOX, draw_edge, draw_frame, draw_node, new_axes, save

OUT = Path(__file__).with_name("juggler_frontier.png")

NODES = {
    "Juggler": ("Juggler map", ""),
    "Lean": ("Exact Lean", "semantics"),
    "Atlas": ("Finite words", ""),
    "Covered": ("Even and odd-to-even", "finite progress"),
    "Tests": ("Further tests", ""),
    "Frontier": ("Odd-to-odd", "frontier"),
    "Words": ("Words", ""),
    "States": ("States", ""),
    "Geometry": ("Geometry", ""),
    "Cycles": ("Cycles", ""),
    "Statistics": ("Statistics", ""),
    "ClosedA": ("No extra word law", ""),
    "ClosedB": ("No state quotient", ""),
    "ClosedC": ("Exact cells", ""),
    "Partial": ("Partial restrictions", ""),
    "Descriptive": ("Descriptive bounds", ""),
    "Gap": ("Remaining pointwise gap", ""),
}

FRAMES = [
    ("Map", 0.12, 1.88, 1.15, 4.55),
    ("Sources", 2.02, 3.92, 1.15, 4.55),
    ("Coverage", 4.06, 6.22, 1.15, 4.55),
    ("Families", 6.36, 8.12, 1.15, 4.55),
    ("Verdicts", 8.26, 10.93, 1.15, 4.55),
]

POS = {
    "Juggler": (1.00, 2.85),
    "Lean": (2.97, 3.85),
    "Atlas": (2.97, 1.85),
    "Covered": (5.14, 3.85),
    "Tests": (5.14, 2.85),
    "Frontier": (5.14, 1.70),
    "Words": (7.24, 4.10),
    "States": (7.24, 3.42),
    "Geometry": (7.24, 2.74),
    "Cycles": (7.24, 2.06),
    "Statistics": (7.24, 1.38),
    "ClosedA": (9.60, 4.10),
    "ClosedB": (9.60, 3.42),
    "ClosedC": (9.60, 2.74),
    "Partial": (9.60, 2.06),
    "Descriptive": (9.60, 1.38),
    "Gap": (5.525, 0.48),
}

BOX = {
    "Covered": (2.00, 0.56),
    "Tests": (2.00, 0.56),
    "Frontier": (2.00, 0.56),
    "ClosedA": (2.48, 0.48),
    "ClosedB": (2.48, 0.48),
    "ClosedC": (2.48, 0.48),
    "Partial": (2.48, 0.48),
    "Descriptive": (2.48, 0.48),
    "Words": (1.60, 0.48),
    "States": (1.60, 0.48),
    "Geometry": (1.60, 0.48),
    "Cycles": (1.60, 0.48),
    "Statistics": (1.60, 0.48),
    "Gap": (10.50, 0.56),
}

EDGES = [
    ("Juggler", "Lean", "d", 0.08),
    ("Juggler", "Atlas", "d", -0.08),
    ("Lean", "Covered", "h", 0.0),
    ("Lean", "Tests", "d", 0.05),
    ("Atlas", "Tests", "d", -0.05),
    ("Covered", "Frontier", "bypass", 0.12),
    ("Tests", "Words", "d", 0.10),
    ("Tests", "States", "d", 0.04),
    ("Tests", "Geometry", "h", 0.0),
    ("Tests", "Cycles", "d", -0.04),
    ("Tests", "Statistics", "d", -0.10),
    ("Words", "ClosedA", "h", 0.0),
    ("States", "ClosedB", "h", 0.0),
    ("Geometry", "ClosedC", "h", 0.0),
    ("Cycles", "Partial", "h", 0.0),
    ("Statistics", "Descriptive", "h", 0.0),
    ("Descriptive", "Gap", "sink", 0.0),
    ("Frontier", "Gap", "sink", 0.0),
]

FIG_W = 11.05
FIG_H = 4.85


def box_size(name: str) -> tuple[float, float]:
    return BOX.get(name, DEFAULT_BOX)


def ports(src: str, dst: str, kind: str) -> tuple[tuple[float, float], tuple[float, float]]:
    x0, y0 = POS[src]
    x1, y1 = POS[dst]
    w0, h0 = box_size(src)
    w1, h1 = box_size(dst)
    if kind == "bypass":
        return (x0 - w0 / 2, y0), (x1 - w1 / 2, y1)
    if kind == "sink":
        left, right = x1 - w1 / 2 + 0.18, x1 + w1 / 2 - 0.18
        x_land = min(max(x0, left), right)
        return (x0, y0 - h0 / 2), (x_land, y1 + h1 / 2)
    if kind == "v":
        if y1 < y0:
            return (x0, y0 - h0 / 2), (x1, y1 + h1 / 2)
        return (x0, y0 + h0 / 2), (x1, y1 - h1 / 2)
    if kind == "h":
        if x1 > x0:
            return (x0 + w0 / 2, y0), (x1 - w1 / 2, y1)
        return (x0 - w0 / 2, y0), (x1 + w1 / 2, y1)
    if abs(x1 - x0) >= abs(y1 - y0):
        if x1 > x0:
            return (x0 + w0 / 2, y0), (x1 - w1 / 2, y1)
        return (x0 - w0 / 2, y0), (x1 + w1 / 2, y1)
    if y1 < y0:
        return (x0, y0 - h0 / 2), (x1, y1 + h1 / 2)
    return (x0, y0 + h0 / 2), (x1, y1 - h1 / 2)


def main() -> None:
    fig, ax = new_axes(FIG_W, FIG_H)
    for title, left, right, bottom, top in FRAMES:
        draw_frame(ax, title, left, right, bottom, top)
    for src, dst, kind, rad in EDGES:
        draw_edge(ax, *ports(src, dst, kind), rad=rad)
    for name, (x, y) in POS.items():
        title, subtitle = NODES[name]
        draw_node(ax, x, y, title, subtitle, size=box_size(name))
    save(fig, OUT)
    print(OUT)


if __name__ == "__main__":
    main()
