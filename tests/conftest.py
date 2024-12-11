import os
import sys

import pytest
from astrodbkit.astrodb import Database, create_database

sys.path.append("./")  # needed for github actions to find the template module
from schema.schema_template import REFERENCE_TABLES

DB_PATH = "data"
DB_NAME = "tests/astrodb_template_tests.sqlite"
SCHEMA_PATH = "schema/schema.yaml"
CONNECTION_STRING = "sqlite:///" + DB_NAME


# Create a fresh template database for the data and integrity tests
@pytest.fixture(scope="session", autouse=True)
def db():

    # Remove any existing copy of the test database
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # Create the database using the Felis schema
    create_database(CONNECTION_STRING, felis_schema=SCHEMA_PATH)
    assert os.path.exists(DB_NAME)

    # Load data into an in-memory sqlite database first, for performance
    db = Database("sqlite://", reference_tables=REFERENCE_TABLES)
    db.load_database(DB_PATH, verbose=False)
    db.dump_sqlite(DB_NAME)

    # Connect to the new database
    db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES)

    return db