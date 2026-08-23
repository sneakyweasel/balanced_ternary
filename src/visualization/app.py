"""Launcher for the Streamlit balanced-ternary laboratory.

Launch:

    python -m pip install -e ".[ui]"
    btprime collatz ui
    btprime calculus explorer

The app is centered on exact balanced-ternary words and a calculator.
The Residual explorer lives under Calculus research.
Collatz pages remain as one research application. The UI does not claim
progress on the Collatz conjecture. Feature deltas are not Lyapunov
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
            "  btprime collatz ui"
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
