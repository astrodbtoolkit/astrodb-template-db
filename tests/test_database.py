"""
Functions to test the database and example files
"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func, or_


def test_setup_db(db):
    # Some setup tasks to ensure some data exists in the database first
    ref_data = [
        {
            "reference": "Ref 1",
            "doi": "10.1093/mnras/staa1522",
            "bibcode": "2020MNRAS.496.1922B",
        },
        {"reference": "Ref 2", "doi": "Doi2", "bibcode": "2012yCat.2311....0C"},
    ]

    with db.engine.connect() as conn:
        conn.execute(db.Publications.insert().values(ref_data))
        # conn.execute(db.Sources.insert().values(source_data))
        conn.commit()


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


def test_orm_use(db):
    # Tests validation using the SQLAlchemy ORM

    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Sources = Base.classes.Sources
    Names = Base.classes.Names

    # Adding and removing a basic source
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 1")
    n = Names(source="V4046 Sgr", other_name="Hen 3-1636")
    with db.session as session:
        session.add(s)
        session.add(n)
        session.commit()

    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 1
    assert db.query(db.Names).filter(db.Names.c.other_name == "Hen 3-1636").count() == 1

    # Remove added source so other tests don't include it
    with db.session as session:
        session.delete(n)  # delete Names before Sources
        session.delete(s)
        session.commit()

    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 0


def test_photometry(db):

    # Confirm the source isn't already present
    assert (
        db.query(db.Sources).filter(db.Sources.c.source == "Fake V4046 Sgr").count()
        == 0
    )

    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Sources = Base.classes.Sources
    Publications = Base.classes.Publications
    Telescopes = Base.classes.Telescopes
    Photometry = Base.classes.Photometry
    PhotometryFilters = Base.classes.PhotometryFilters
    Regimes = Base.classes.Regimes

    # Insert supporting data to (Sources, Publications, Telescopes, PhotometryFilters)
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 1")
    ref = Publications(reference="Cutri03")
    tel = Telescopes(telescope="Fake 2MASS", reference="Cutri03")
    pf = PhotometryFilters(band="Fake 2MASS.Ks", effective_wavelength_angstroms=2.159)
    reg = Regimes(regime="fake optical")

    with db.session as session:
        session.add_all([ref, pf, tel, s, reg])
        session.commit()

    # Verify supporting information was stored
    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 1
    assert (
        db.query(db.Telescopes)
        .filter(db.Telescopes.c.telescope == "Fake 2MASS")
        .count()
        == 1
    )
    assert (
        db.query(db.PhotometryFilters)
        .filter(db.PhotometryFilters.c.band == "Fake 2MASS.Ks")
        .count()
        == 1
    )

    # Insert Photometry data, which refers to the supporting tables
    # Using it within add_all can cause issues since it may insert
    # the value before the supporting information is in place
    phot = Photometry(
        source="V4046 Sgr",
        band="Fake 2MASS.Ks",
        magnitude=7.249,
        telescope="Fake 2MASS",
        reference="Cutri03",
        regime="fake optical",
    )
    with db.session as session:
        session.add(phot)
        session.commit()

    # Verify Photometry was added
    assert (
        db.query(db.Photometry).filter(db.Photometry.c.source == "V4046 Sgr").count()
        == 1
    )


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
