"""Launcher for the Streamlit research explorer.

Launch:

    python -m pip install -e ".[ui]"
    btprime collatz ui

This UI inspects exact identities already implemented. It does not claim
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
