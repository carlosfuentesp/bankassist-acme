"""Shared pytest fixtures; Databricks Connect is initialized only when requested."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest


@pytest.fixture()
def spark():
    databricks_connect = pytest.importorskip("databricks.connect")
    return databricks_connect.DatabricksSession.builder.getOrCreate()


@pytest.fixture()
def load_fixture(spark):
    def _loader(filename: str):
        path = Path(__file__).parent.parent / "fixtures" / filename
        if path.suffix.lower() == ".json":
            return spark.createDataFrame(json.loads(path.read_text()))
        if path.suffix.lower() == ".csv":
            with path.open(newline="") as handle:
                return spark.createDataFrame(list(csv.DictReader(handle)))
        raise ValueError(f"Unsupported fixture type: {filename}")

    return _loader
