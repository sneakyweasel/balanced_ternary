"""CLI subcommands for ``btlab collatz ...``."""

from .coordinator import run_collatz
from .parsers import add_collatz_subparser

__all__ = ["add_collatz_subparser", "run_collatz"]
