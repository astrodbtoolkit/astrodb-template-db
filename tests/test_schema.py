"""
functions to test the schema itself.
"""
import pytest
import os
from schema.schema_template import (
    Sources,
    Names,
    Publications,
    Telescopes,
    Instruments,
    PhotometryFilters,
    Photometry,
    Versions,
)
from astrodbkit2.astrodb import create_database, Database

def schema_tester(table, values, error_state):
    """Helper function to handle the basic testing of the schema classes"""
    if error_state is None:
        _ = table(**values)
    else:
        with pytest.raises(error_state):
            _ = table(**values)


DB_NAME = "test.sqlite"
DB_PATH = "data"

REFERENCE_TABLES = [
    "Publications",
    "Telescopes",
    "Instruments",
    "Modes",
    "PhotometryFilters",
    "Versions",
    "Parameters",
]


# Load the database for use in individual tests
@pytest.fixture(scope="module")
def db():
    # Create a fresh temporary database and assert it exists
    # Because we've imported simple.schema, we will be using that schema for the database

    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    connection_string = "sqlite:///" + DB_NAME
    create_database(connection_string)
    assert os.path.exists(DB_NAME)

    # Connect to the new database and confirm it has the Sources table
    db = Database(connection_string, reference_tables=REFERENCE_TABLES)
    assert db
    assert "source" in [c.name for c in db.Sources.columns]

    return db


def test_setup_db(db):
    # Some setup tasks to ensure some data exists in the database first
    ref_data = [
        {
            "reference": "Ref 1",
            "doi": "10.1093/mnras/staa1522",
            "bibcode": "2020MNRAS.496.1922B",
        },
        {"reference": "Ref 2", "doi": "Doi2", "bibcode": "2012yCat.2311....0C"},
        {"reference": "Burn08", "doi": "Doi3", "bibcode": "2008MNRAS.391..320B"},
    ]

    source_data = [
        {"source": "Fake 1", "ra_deg": 9.0673755, "dec_deg": 18.352889, "reference": "Ref 1"},
        {"source": "Fake 2", "ra_deg": 9.0673755, "dec_deg": 18.352889, "reference": "Ref 1"},
        {"source": "Fake 3", "ra_deg": 9.0673755, "dec_deg": 18.352889, "reference": "Ref 2"},
    ]

    with db.engine.connect() as conn:
        conn.execute(db.Publications.insert().values(ref_data))
        conn.execute(db.Sources.insert().values(source_data))
        conn.commit()


def test_orm_use(db):
    # Tests validation using the SQLAlchemy ORM

    # Adding and removing a basic source
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 1")
    with db.session as session:
        session.add(s)
        session.commit()

    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 1

    # Remove added source so other tests don't include it
    with db.session as session:
        session.delete(s)
        session.commit()

    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 0

    # Adding a source with problematic ra/dec to test validation
    with pytest.raises(ValueError):
        s2 = Sources(source="V4046 Sgr", ra_deg=9999, dec_deg=-32.79, reference="Ref 1")
    with pytest.raises(ValueError):
        s2 = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-9999, reference="Ref 1")


def test_photometry_filters(db):
    # filter should have a '.' in it
    with pytest.raises(ValueError):
        pf = PhotometryFilters(band="not_a_filter")

    # effective_wavelength should be a positive number
    with pytest.raises(ValueError):
        pf = PhotometryFilters(band="new.filter", effective_wavelength_angstroms=None)
    with pytest.raises(ValueError):
        pf = PhotometryFilters(band="new.filter2", effective_wavelength_angstroms=-40)

    # NOTE: this does not raise an error because effective_wavelength is not provided
    _ = PhotometryFilters(band="2MASS.H") 


def test_photometry(db):
    # Insert supporting data to (Sources, Publications, Telescopes, PhotometryFilters)
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 1")
    ref = Publications(reference="Cutri03")
    tel = Telescopes(telescope="2MASS", reference="Cutri03")
    pf = PhotometryFilters(band="2MASS.Ks", effective_wavelength_angstroms=2.159)
    with db.session as session:
        session.add_all([ref, pf, tel, s])
        session.commit()

    # Verify supporting information was stored
    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 1
    assert (
        db.query(db.Telescopes).filter(db.Telescopes.c.telescope == "2MASS").count()
        == 1
    )
    assert (
        db.query(db.PhotometryFilters)
        .filter(db.PhotometryFilters.c.band == "2MASS.Ks")
        .count()
        == 1
    )

    # Insert Photometry data, which refers to the supporting tables
    # Using it within add_all can cause issues since it may insert
    # the value before the supporting information is in place
    phot = Photometry(
        source="V4046 Sgr",
        band="2MASS.Ks",
        magnitude=7.249,
        telescope="2MASS",
        reference="Cutri03",
    )
    with db.session as session:
        session.add(phot)
        session.commit()

    # Verify Photometry was added
    assert (
        db.query(db.Photometry).filter(db.Photometry.c.source == "V4046 Sgr").count()
        == 1
    )


def test_publications(db):
    with pytest.raises(ValueError):
        ref = Publications(reference="ThisIsASuperLongReferenceThatIsInvalid")
    with pytest.raises(ValueError):
        ref = Publications(reference=None)

def test_telescopes(db):
    with pytest.raises(ValueError):
        tel = Telescopes(telescope="ThisIsASuperLongTelescopeNameThatIsInvalid")
    with pytest.raises(ValueError):
        tel = Telescopes(telescope=None)

def test_sources(db):
    with pytest.raises(ValueError):
        s = Sources(source="ThisIsASuperLongSourceNameThatIsInvalid")
    with pytest.raises(ValueError):
        s = Sources(source=None)

def test_versions(db):
    with pytest.raises(ValueError):
        ver = Versions(version="ThisIsASuperLongVersionNameThatIsInvalid")
    with pytest.raises(ValueError):
        ver = Versions(version=None)


@pytest.mark.parametrize("values, error_state",
                         [
                             ({"source": "ThisIsASuperLongSourceNameThatIsInvalid", "other_name": "OtherName"}, ValueError),
                             ({"source": None, other_name="OtherName"}, ValueError),
                             ({"source": "Source", other_name="ThisIsASuperLongOtherNameThatIsInvalid"}, ValueError),
                             ({"telescope": "Source", "other_name": None}, ValueError)
                          ])
def test_names(db):
    schema_tester(Names, values, error_state)
    with pytest.raises(ValueError):
        n = Names(source="ThisIsASuperLongSourceNameThatIsInvalid", other_name="OtherName")
    with pytest.raises(ValueError):
        n = Names(source=None, other_name="OtherName")
    with pytest.raises(ValueError):
        n = Names(source="Source", other_name="ThisIsASuperLongOtherNameThatIsInvalid")
    with pytest.raises(ValueError):
        n = Names(source="Source", other_name=None)


@pytest.mark.parametrize("values, error_state",
                         [
                             ({"instrument": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"instrument": None}, ValueError),
                             ({"mode": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"telescope": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                              ({"telescope": None}, ValueError)
                          ])
def test_instruments(db):
    schema_tester(Instruments, values, error_state)

