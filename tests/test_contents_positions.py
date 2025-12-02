"""
Functions to test the contents of the Positions table.
"""

from sqlalchemy import or_


def test_positions(db):
    # Test that Positions has expected number of entries
    t = db.query(db.Positions.c.source).astropy()
    n_positions = 1
    assert len(t) == n_positions, f"Found {len(t)} entries in the Positions table, expected {n_positions}"


def test_for_valid_coordinates(db):
    # Verify that all sources have valid coordinates
    t = (
        db.query(db.Positions.c.source, db.Positions.c.ra_deg, db.Positions.c.dec_deg)
        .filter(
            or_(
                db.Positions.c.ra_deg.is_(None),
                db.Positions.c.ra_deg < 0,
                db.Positions.c.ra_deg > 360,
                db.Positions.c.dec_deg.is_(None),
                db.Positions.c.dec_deg < -90,
                db.Positions.c.dec_deg > 90,
            )
        )
        .astropy()
    )

    assert len(t) == 0, f"{len(t)} Positions failed coordinate checks: {t}"