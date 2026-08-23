"""Streamlit smoke tests for the Residual Explorer page."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

PAGE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "visualization"
    / "app_pages"
    / "residual_explorer.py"
)


def _page_text(at) -> str:
    chunks = []
    for attr in ("markdown", "caption", "code", "text", "title"):
        if hasattr(at, attr):
            chunks.extend(str(el.value) for el in getattr(at, attr))
    return "\n".join(chunks)


def test_residual_explorer_page_loads():
    at = AppTest.from_file(str(PAGE), default_timeout=40)
    at.run()
    assert not at.exception
    labels = [box.label for box in at.selectbox]
    assert any("Polynomial" in str(label) for label in labels)
    buttons = [btn.label for btn in at.button]
    assert any("Run" in str(label) for label in buttons)
    sliders = [slider.label for slider in at.slider]
    assert any("Horizon" in str(label) for label in sliders)
    body = _page_text(at)
    assert "Exact residual" in body or "f_{" in body
    assert "mod 9" in body
    assert "States merged" in body or "Observable" in body


def test_residual_explorer_compare_and_dual_controls():
    at = AppTest.from_file(str(PAGE), default_timeout=40)
    at.run()
    assert not at.exception
    buttons = " ".join(str(btn.label) for btn in at.button)
    assert "Set A" in buttons
    assert "Set B" in buttons
    assert "r=2 two above" in buttons
    assert "Expand subtree" in buttons


def test_scenario_b_and_c_delayed_pair_compare():
    at = AppTest.from_file(str(PAGE), default_timeout=40)
    at.run()
    assert not at.exception
    at.session_state.re_secondary = "Compare"
    at.run()
    demo = next(btn for btn in at.button if "delayed" in str(btn.label).lower())
    demo.click().run()
    assert not at.exception
    body = _page_text(at)
    assert "State A" in body
    assert "State B" in body
    assert at.session_state.re_k == 2
    same = [m for m in at.metric if "Same class" in str(m.label)]
    assert same
    assert str(same[0].value) == "YES"
    at.session_state.re_k = 3
    at.run()
    assert not at.exception
    same = [m for m in at.metric if "Same class" in str(m.label)]
    assert same
    assert str(same[0].value) == "NO"
    body = _page_text(at)
    assert "DIFFERENT" in body or "τ" in body or "tau" in body.lower()


def test_congruence_lifting_view_renders():
    at = AppTest.from_file(str(PAGE), default_timeout=60)
    at.run()
    assert not at.exception
    at.session_state.re_secondary = "Congruence / lifting"
    at.session_state.re_poly = "x^2"
    at.run()
    assert not at.exception
    body = _page_text(at)
    assert "Lifting tree" in body
    assert "zero-output subtree" in body
    labels = " ".join(str(m.label) for m in at.metric)
    assert "Brute force agrees" in labels
    agrees = [m for m in at.metric if "Brute force agrees" in str(m.label)]
    assert agrees and str(agrees[0].value) == "YES"
    sliders = " ".join(str(s.label) for s in at.slider)
    assert "Levels k" in sliders
    assert "Horizon r" in sliders


def test_scenario_d_x2_vs_x3():
    at = AppTest.from_file(str(PAGE), default_timeout=40)
    at.run()
    assert not at.exception
    at.session_state.re_secondary = "x^2 vs x^3"
    at.run()
    assert not at.exception
    body = _page_text(at)
    assert "residual tree preserved" in body
    assert "compressed" in body
    merged = [m for m in at.metric if str(m.label) == "Merged"]
    assert merged
    assert any(str(m.value) == "0" for m in merged)
