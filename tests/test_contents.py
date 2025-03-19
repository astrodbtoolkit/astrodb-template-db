"""
Functions to test the database contents
As users add their own data, these tests should be modified to reflect the new data.
"""

from sqlalchemy import func, or_


def test_table_presence(db):
    # Confirm the tables that should be present

    assert len(db.metadata.tables.keys()) == 22
    assert "Sources" in db.metadata.tables.keys()
    assert "Publications" in db.metadata.tables.keys()
    assert "Names" in db.metadata.tables.keys()
    assert "Telescopes" in db.metadata.tables.keys()
    assert "Instruments" in db.metadata.tables.keys()
    assert "PhotometryFilters" in db.metadata.tables.keys()
    assert "Versions" in db.metadata.tables.keys()
    assert "Parallaxes" in db.metadata.tables.keys()
    assert "RadialVelocities" in db.metadata.tables.keys()
    assert "Photometry" in db.metadata.tables.keys()
    assert "Regimes" in db.metadata.tables.keys()
    assert "AssociationList" in db.metadata.tables.keys()
    assert "Associations" in db.metadata.tables.keys()
    assert "CompanionRelationships" in db.metadata.tables.keys()
    assert "ParameterList" in db.metadata.tables.keys()
    assert "CompanionParameters" in db.metadata.tables.keys()
    assert "CompanionList" in db.metadata.tables.keys()
    assert "SourceTypeList" in db.metadata.tables.keys()
    assert "SourceTypes" in db.metadata.tables.keys()
    assert "ProperMotions" in db.metadata.tables.keys()
    assert "ModeledParameters" in db.metadata.tables.keys()
    assert "RotationalParameters" in db.metadata.tables.keys()


def test_magnitudes(db):
    # Check that magnitudes make sense.
    t = (
        db.query(db.Photometry.c.magnitude)
        .filter(
            or_(
                db.Photometry.c.magnitude.is_(None),
                db.Photometry.c.magnitude > 100,
                db.Photometry.c.magnitude < -1,
            )
        )
        .astropy()
    )

    if len(t) > 0:
        print(f"\n{len(t)} Photometry failed magnitude checks")
        print(t)

    assert len(t) == 0, f"{len(t)} Photometry failed magnitude checks"


def test_parallax_error(db):
    # Verify that all sources have valid parallax errors
    t = (
        db.query(db.Parallaxes.c.parallax_error)
        .filter(
            or_(
                db.Parallaxes.c.parallax_error < 0,
            )
        )
        .astropy()
    )

    if len(t) > 0:
        print(f"\n{len(t)} Parallax failed parallax error checks")
        print(t)

    assert len(t) == 0, f"{len(t)} Parallax failed parallax error checks"


def test_companion_relationships(db):
    # Test that Companion Relationships has expected number of entries
    t = db.query(db.CompanionRelationships.c.relationship).astropy()

    n_companion_relationships = 1
    assert (
        len(t) == n_companion_relationships
    ), f"Found {len(t)} entries in the Companion Relationships table, expected {n_companion_relationships}"


def test_radial_velocities(db):
    # Test that Radial Velocities has expected number of entries
    t = db.query(db.RadialVelocities.c.rv_kms).astropy()

    n_radial_velocities = 1
    assert (
        len(t) == n_radial_velocities
    ), f"Found {len(t)} entries in the Radial Velocities table, expected {n_radial_velocities}"

    # Test that there is one adopted radial velocity measurement per source
    t = (
        db.query(
            db.RadialVelocities.c.source,
            func.sum(db.RadialVelocities.c.adopted).label("adopted_counts"),
        )
        .group_by(db.RadialVelocities.c.source)
        .having(func.sum(db.RadialVelocities.c.adopted) != 1)
        .astropy()
    )

    assert (
        len(t) == 0
    ), f"Found {len(t)} radial velocity measurements with incorrect 'adopted' labels"


def test_proper_motions(db):
    # Test that Radial Velocities has expected number of entries
    t = db.query(db.ProperMotions.c.pm_ra).astropy()

    n_proper_motions = 1
    assert (
        len(t) == n_proper_motions
    ), f"Found {len(t)} entries in the Proper Motions table, expected {n_proper_motions}"

    # Test that there is one adopted proper motion measurement per source
    t = (
        db.query(
            db.ProperMotions.c.source,
            func.sum(db.ProperMotions.c.adopted).label("adopted_counts"),
        )
        .group_by(db.ProperMotions.c.source)
        .having(func.sum(db.ProperMotions.c.adopted) != 1)
        .astropy()
    )

    assert (
        len(t) == 0
    ), f"Found {len(t)} proper motion measurements with incorrect 'adopted' labels"
