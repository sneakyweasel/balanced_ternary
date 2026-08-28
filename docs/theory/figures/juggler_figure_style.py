"""Shared print style for the Juggler paper figures."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

FRAME_FACE = "#f7f7f7"
FRAME_EDGE = "#b0b0b0"
BOX_FACE = "#ececec"
BOX_EDGE = "#666666"
ARROW = "#444444"
TITLE = "#222222"
SUB = "#555555"
FRAME_LABEL = "#555555"
DEFAULT_BOX = (1.68, 0.56)


def new_axes(fig_w: float, fig_h: float):
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=220)
    ax.set_xlim(0.0, fig_w)
    ax.set_ylim(0.0, fig_h)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def draw_frame(ax, title: str, left: float, right: float, bottom: float, top: float) -> None:
    ax.add_patch(
        Rectangle(
            (left, bottom),
            right - left,
            top - bottom,
            linewidth=0.8,
            edgecolor=FRAME_EDGE,
            facecolor=FRAME_FACE,
            zorder=0,
        )
    )
    ax.text(
        (left + right) / 2,
        top - 0.14,
        title,
        ha="center",
        va="center",
        fontsize=8,
        color=FRAME_LABEL,
        fontstyle="italic",
        zorder=1,
    )


def draw_edge(ax, start: tuple[float, float], end: tuple[float, float], rad: float = 0.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=9,
            linewidth=0.9,
            color=ARROW,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=1.5,
            shrinkB=1.5,
            zorder=2,
        )
    )


def draw_node(
    ax,
    x: float,
    y: float,
    title: str,
    subtitle: str = "",
    size: tuple[float, float] = DEFAULT_BOX,
) -> None:
    w, h = size
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.015,rounding_size=0.05",
            linewidth=0.9,
            edgecolor=BOX_EDGE,
            facecolor=BOX_FACE,
            zorder=3,
        )
    )
    if subtitle:
        ax.text(x, y + 0.08, title, ha="center", va="center", fontsize=8.3, color=TITLE, zorder=4)
        ax.text(x, y - 0.12, subtitle, ha="center", va="center", fontsize=6.8, color=SUB, zorder=4)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=8.3, color=TITLE, zorder=4)


def save(fig, path) -> None:
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(path, dpi=220, facecolor="white")
    plt.close(fig)
