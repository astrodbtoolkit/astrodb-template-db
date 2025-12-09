"""
Functions to test the contents of the Morphology table.
"""

from sqlalchemy import or_


def test_morphology(db):
    # Test that Morphology has expected number of entries
    t = db.query(db.Morphology.c.source).astropy()
    n_morphology = 1
    assert len(t) == n_morphology, f"Found {len(t)} entries in the Morphology table, expected {n_morphology}"


def test_for_valid_morphology(db):
    # Verify that all sources have valid morphology
    t = (
        db.query(db.Morphology.c.source, db.Morphology.c.position_angle_deg, db.Morphology.c.ellipticity, db.Morphology.c.half_light_radius_arcmin)
        .filter(
            or_(
                db.Morphology.c.position_angle_deg.is_(None),
                db.Morphology.c.position_angle_deg < 0,
                db.Morphology.c.position_angle_deg > 360,
                db.Morphology.c.ellipticity.is_(None),
                db.Morphology.c.ellipticity < 0,
                db.Morphology.c.ellipticity > 1,
                db.Morphology.c.half_light_radius_arcmin.is_(None),
                db.Morphology.c.half_light_radius_arcmin < 0,
            )
        )
        .astropy()
    )

    assert len(t) == 0, f"{len(t)} Morphology failed morphology checks: {t}"
