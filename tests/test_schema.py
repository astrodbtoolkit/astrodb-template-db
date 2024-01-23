"""
functions to test the schema itself.
"""

import pytest
import os
from schema.schema import *
DB_NAME = 'test.db'
DB_PATH = 'data'
print(os.getcwd())

from astrodbkit2.astrodb import create_database, Database
REFERENCE_TABLES = ['Publications', 'Telescopes', 'Instruments', 'Modes', 'PhotometryFilters', 'Versions', 'Parameters']

# Load the database for use in individual tests
@pytest.fixture(scope="module")
def db():
    # Create a fresh temporary database and assert it exists
    # Because we've imported simple.schema, we will be using that schema for the database

    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    connection_string = 'sqlite:///' + DB_NAME
    create_database(connection_string)
    assert os.path.exists(DB_NAME)

    # Connect to the new database and confirm it has the Sources table
    db = Database(connection_string, reference_tables=REFERENCE_TABLES)
    assert db
    assert 'source' in [c.name for c in db.Sources.columns]

    return db


def test_setup_db(db):
    # Some setup tasks to ensure some data exists in the database first
    ref_data = [{'reference': 'Ref 1', 'doi': '10.1093/mnras/staa1522', 'bibcode': '2020MNRAS.496.1922B'},
                {'reference': 'Ref 2', 'doi': 'Doi2', 'bibcode': '2012yCat.2311....0C'},
                {'reference': 'Burn08', 'doi': 'Doi3', 'bibcode': '2008MNRAS.391..320B'}]

    source_data = [{'source': 'Fake 1', 'ra': 9.0673755, 'dec': 18.352889, 'reference': 'Ref 1'},
                   {'source': 'Fake 2', 'ra': 9.0673755, 'dec': 18.352889, 'reference': 'Ref 1'},
                   {'source': 'Fake 3', 'ra': 9.0673755, 'dec': 18.352889, 'reference': 'Ref 2'},
                   ]

    with db.engine.connect() as conn:
        conn.execute(db.Publications.insert().values(ref_data))
        conn.execute(db.Sources.insert().values(source_data))
        conn.commit()

    return db
