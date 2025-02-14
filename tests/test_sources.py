"""
This module tests the Sources table, mainly to ensure that we have as many sources as we expect.

This forces us to update tests on ingest!
"""

import pytest


@pytest.mark.parametrize(
    "reference, value",
    [("Perlmutter99", 1), ("Rubin80", 2), ("Naka95", 1), ("Eros99", 1)],
)
def test_sources_reference(db, reference, value):
    n_sources = db.query(db.Sources).filter(db.Sources.c.reference == reference).count()
    assert n_sources == value, f"found {n_sources} sources for {reference}"
