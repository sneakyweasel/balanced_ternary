"""Streamlit smoke tests. Skipped when the UI extra is not installed."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402


APP = Path(__file__).resolve().parents[2] / "src" / "visualization" / "streamlit_app.py"
REGISTERED_TITLES = (
    "Overview",
    "Number explorer",
    "Trajectory",
    "Inverse tree",
    "Exponent-code geometry",
    "Affine-center census",
    "2-adic automaton",
    "Odd-part transducer",
    "Valuation prefixes",
    "Valuation languages",
    "Joint graph",
)


def test_router_starts_on_overview():
    at = AppTest.from_file(str(APP), default_timeout=20)
    at.run()
    assert not at.exception
    titles = [element.value for element in at.title]
    assert any("Overview" in str(value) for value in titles)
    source = APP.read_text(encoding="utf-8")
    for title in REGISTERED_TITLES:
        assert title in source
    assert "url_path=\"exponent-code\"" in source


def test_exponent_code_page_loads():
    at = AppTest.from_file(str(APP), default_timeout=20)
    at.switch_page("app_pages/exponent_code.py")
    at.run()
    assert not at.exception
    assert any("Exponent-code" in str(value) for value in [h.value for h in at.header])
    assert any("valuation" in str(box.label).lower() for box in at.text_input)
