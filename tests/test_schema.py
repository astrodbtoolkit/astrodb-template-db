"""
functions to test the schema itself.
"""
import pytest
import os
from schema.schema_template import *
from astrodbkit2.astrodb import create_database, Database


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
