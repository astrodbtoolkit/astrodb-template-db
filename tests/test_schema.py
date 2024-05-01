"""
functions to test the schema itself.
"""
import os

import pytest
from astrodbkit2.astrodb import Database, create_database

from schema.schema_template import (
    Instruments,
    Names,
    Photometry,
    PhotometryFilters,
    Publications,
    Sources,
    Telescopes,
    Versions,
)

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


def schema_tester(table, values, error_state):
    """Helper function to handle the basic testing of the schema classes"""
    if error_state is None:
        _ = table(**values)
    else:
        with pytest.raises(error_state):
            _ = table(**values)


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

# -----------------------------------------------------------------------
# Schema tests
@pytest.mark.parametrize("values, error_state", [
    ({"reference": "Valid"}, None),
    ({"reference": "Valid", "doi": "LongDOI"*100}, ValueError),  # using multiplier to make a very long string
    ({"reference": "Valid", "bibcode": "LongBibCode"*100}, ValueError),
    ({"reference": "ThisIsASuperLongReferenceThatIsInvalid"}, ValueError),
    ({"telesreferencecope": None}, TypeError),  # invalid column
])
def test_publications_schema(values, error_state):
    schema_tester(Publications, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"band": "new.filter"}, None),
    ({"band": "not_a_filter"}, ValueError),
    ({"band": "new.filter", "effective_wavelength_angstroms": None}, ValueError),
    ({"band": "new.filter", "effective_wavelength_angstroms": -40}, ValueError),
])
def test_photometry_filters_schema(values, error_state):
    schema_tester(PhotometryFilters, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"source": "V4046 Sgr", "band": "2MASS.Ks", "magnitude": 7.249, "telescope": "2MASS", "reference": "Cutri03",}, None),
])
def test_photometry_schema(values, error_state):
    schema_tester(Photometry, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"telescope": "Valid"}, None),
    ({"telescope": "ThisIsASuperLongTelescopeThatIsInvalid"}, ValueError),
    ({"telescope": None}, ValueError),
])
def test_telescopes(values, error_state):
    schema_tester(Telescopes, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"source": "Valid"}, None),
    ({"source": "V4046 Sgr", "ra_deg": 9999, "dec_deg": -32.79, "reference": "Ref 1"}, ValueError),
    ({"source": "V4046 Sgr", "ra_deg": 273.54, "dec_deg": -9999, "reference": "Ref 1"}, ValueError),
    ({"source": "ThisIsASuperLongSourceNameThatIsInvalid"*5}, ValueError),
    ({"source": None}, ValueError),
])
def test_sources_schema(values, error_state):
    schema_tester(Sources, values, error_state)


@pytest.mark.parametrize("values, error_state", [
    ({"version": "1.0"}, None),
    ({"version": "ThisIsASuperLongVersionNameThatIsInvalid"}, ValueError),
    ({"version": None}, ValueError)
])
def test_versions_schema(values, error_state):
    schema_tester(Versions, values, error_state)


@pytest.mark.parametrize("values, error_state",
                         [
                             ({"source": "Valid", "other_name": "OtherName"}, None),
                             ({"source": "ThisIsASuperLongSourceNameThatIsInvalid"*5, "other_name": "OtherName"}, ValueError),
                             ({"source": None, "other_name":"OtherName"}, ValueError),
                             ({"source": "Source", "other_name":"ThisIsASuperLongOtherNameThatIsInvalid"*5}, ValueError),
                             ({"telescope": "Source", "other_name": None}, TypeError)  # telescope is an invalid field
                          ])
def test_names(values, error_state):
    schema_tester(Names, values, error_state)


@pytest.mark.parametrize("values, error_state",
                         [
                             ({"instrument": "Valid"}, None),
                             ({"instrument": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"instrument": None}, ValueError),
                             ({"mode": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"telescope": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"telescope": None}, ValueError)
                          ])
def test_instruments_schema(values, error_state):
    schema_tester(Instruments, values, error_state)

