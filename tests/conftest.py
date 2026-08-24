"""Suite options: skip exhaustive census / UI / million-range tests by default."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="run exhaustive census, million-range, and Streamlit AppTests",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="slow; pass --runslow to include")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
