"""
Functions to test the database contents
As users add their own data, these tests should be modified to reflect the new data.
"""

from sqlalchemy import or_


def test_table_presence(db):
    # Confirm the tables that should be present
    assert len(db.metadata.tables.keys()) == 23
    assert "Sources" in db.metadata.tables.keys()
    assert "Publications" in db.metadata.tables.keys()
    assert "Names" in db.metadata.tables.keys()
    assert "Telescopes" in db.metadata.tables.keys()
    assert "Instruments" in db.metadata.tables.keys()
    assert "Versions" in db.metadata.tables.keys()
    # Kinematic and Astrometric data
    assert "ProperMotions" in db.metadata.tables.keys()
    assert "Parallaxes" in db.metadata.tables.keys()
    assert "RadialVelocities" in db.metadata.tables.keys()
    # Photometric data
    assert "Photometry" in db.metadata.tables.keys()
    assert "RegimeList" in db.metadata.tables.keys()
    assert "PhotometryFilters" in db.metadata.tables.keys()
    # Companion data
    assert "CompanionRelationships" in db.metadata.tables.keys()
    assert "CompanionParameters" in db.metadata.tables.keys()
    assert "CompanionList" in db.metadata.tables.keys()
    # Source Types
    assert "SourceTypeList" in db.metadata.tables.keys()
    assert "SourceTypes" in db.metadata.tables.keys()
    # Associations
    assert "AssociationList" in db.metadata.tables.keys()
    assert "Associations" in db.metadata.tables.keys()
    # Various Parameters
    assert "ModeledParameters" in db.metadata.tables.keys()
    assert "RotationalParameters" in db.metadata.tables.keys()
    assert "ParameterList" in db.metadata.tables.keys()
    assert "Spectra" in db.metadata.tables.keys()


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


def test_companion_relationships(db):
    # Test that Companion Relationships has expected number of entries
    t = db.query(db.CompanionRelationships.c.relationship).astropy()

    n_companion_relationships = 1
    assert (
        len(t) == n_companion_relationships
    ), f"Found {len(t)} entries in the Companion Relationships table, expected {n_companion_relationships}"
