"""Shared experiment I/O (manifests, JSONL, optional Parquet)."""

from research.experiments.schema import ExperimentManifest
from research.experiments.table_io import read_jsonl, write_experiment, write_rows
