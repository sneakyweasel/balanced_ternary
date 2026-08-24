"""Launcher for the Streamlit balanced-ternary laboratory.

Launch:

    python -m pip install -e ".[ui]"
    btlab ui

`btlab collatz ui` and `btlab calculus explorer` remain aliases.
The app is centered on exact balanced-ternary words and a calculator.
The Residual explorer and rewrite companion live under Calculus research.
Collatz pages remain as one research application. The UI does not claim
progress on the Collatz conjecture. Metric deltas are not Lyapunov
decreases. Finite graphs are samples, not the dynamics.
"""

from __future__ import annotations

import sys
from pathlib import Path


def launch() -> int:
    """Start Streamlit on the router. Requires the optional ``ui`` extra."""
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print(
            "Streamlit is not installed. From the project directory:\n"
            '  python -m pip install -e ".[ui]"\n'
            "  btlab ui"
        )
        return 1
    import subprocess

    target = Path(__file__).resolve().with_name("streamlit_app.py")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(target),
        "--browser.gatherUsageStats",
        "false",
    ]
    return int(subprocess.call(cmd))
