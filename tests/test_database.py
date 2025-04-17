"""
Tests that the database functions work as expected.
Users should hopefully not need to modify these tests.
"""

from sqlalchemy.ext.automap import automap_base


def test_orm_use(db):
    # Tests validation using the SQLAlchemy ORM

    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Sources = Base.classes.Sources
    Names = Base.classes.Names

    # Adding and removing a basic source
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Cohe03")
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


def test_adding_data(db):

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
    RegimeList = Base.classes.RegimeList

    # Insert supporting data to (Sources, Publications, Telescopes, PhotometryFilters)
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Cohe03")
    ref = Publications(reference="Cutri03")
    tel = Telescopes(telescope="Fake 2MASS", reference="Cutri03")
    pf = PhotometryFilters(band="Fake 2MASS.Ks", effective_wavelength_angstroms=2.159)
    reg = RegimeList(regime="fake optical")

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
