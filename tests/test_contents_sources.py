"""
This module tests the contents of Sources table.
As users add their own data, these tests should be modified to reflect the new data.

"""

import pytest
from sqlalchemy import or_


def test_sources(db):
    # Test that Sources has expected number of entries
    n_sources = db.query(db.Sources).count()
    assert n_sources == 7, f"found {n_sources} sources"


@pytest.mark.parametrize(
    "reference, value",
    [("Perlmutter99", 1), ("Rubin80", 2), ("Naka95", 1), ("Eros99", 1)],
)
def test_sources_reference(db, reference, value):
    n_sources = db.query(db.Sources).filter(db.Sources.c.reference == reference).count()
    assert n_sources == value, f"found {n_sources} sources for {reference}"


def test_coordinates(db):
    # Verify that all sources have valid coordinates
    t = (
        db.query(db.Sources.c.source, db.Sources.c.ra_deg, db.Sources.c.dec_deg)
        .filter(
            or_(
                db.Sources.c.ra_deg.is_(None),
                db.Sources.c.ra_deg < 0,
                db.Sources.c.ra_deg > 360,
                db.Sources.c.dec_deg.is_(None),
                db.Sources.c.dec_deg < -90,
                db.Sources.c.dec_deg > 90,
            )
        )
        .astropy()
    )

    assert len(t) == 0, f"{len(t)} Sources failed coordinate checks: {t}"
