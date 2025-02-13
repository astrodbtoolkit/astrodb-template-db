import os
import sys

import pytest
from astrodbkit.astrodb import Database, create_database

REFERENCE_TABLES = [
    "Publications",
    "Telescopes",
    "Instruments",
    "PhotometryFilters",
    "Versions",
    "Regimes",
    "AssociationList",
    "SourceTypeList"
]
DB_PATH = "data"
DB_NAME = "tests/astrodb_template_tests.sqlite"
SCHEMA_PATH = "schema/schema.yaml"
CONNECTION_STRING = "sqlite:///" + DB_NAME


# Create a fresh template database for the data and integrity tests
@pytest.fixture(scope="session", autouse=True)
def db():

    # Confirm the schema yaml file is present
    assert os.path.exists(SCHEMA_PATH)

    # Remove any existing copy of the test database
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        assert not os.path.exists(DB_NAME)

    # Create the database using the Felis schema
    create_database(CONNECTION_STRING, felis_schema=SCHEMA_PATH)
    assert os.path.exists(DB_NAME)

    # Connect and load to the database
    db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES)
    db.load_database(DB_PATH, verbose=False)

    return db