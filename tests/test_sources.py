"""
This module tests the Sources table, mainly to ensure that we have as many sources as we expect.

This forces us to update tests on ingest!
"""

from sqlalchemy import and_, or_
import pytest
from astropy.io.votable.ucd import check_ucd, parse_ucd, UCDWords



@pytest.mark.parametrize(
    "reference, value",
    [
        ("Perlmutter99", 1),
        ("Rubin80", 2),
    ],
)
def test_sources_reference(db, reference, value):
    sources = db.query(db.Sources).filter(
        or_(
            db.Sources.c.reference == reference,

        )
    ).astropy()
    assert len(sources) == value, f"found {len(sources)} sources for {reference}"