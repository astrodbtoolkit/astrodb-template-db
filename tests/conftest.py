import pytest
import os
import logging
from astrodbkit.astrodb import create_database, Database
import sys

sys.path.append("./")  # needed for github actions to find the template module
from schema.schema_template import REFERENCE_TABLES
from schema.schema_template import *



# Create a fresh template database for the data and integrity tests
@pytest.fixture(scope="session", autouse=True)
def db():
    DB_NAME = "tests/astrodb_template_tests.sqlite"
    DB_PATH = "data"

    # Remove any existing copy of the test database
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    connection_string = "sqlite:///" + DB_NAME
    create_database(connection_string)
    assert os.path.exists(DB_NAME)

    # Connect to the new database
    db = Database(connection_string, reference_tables=REFERENCE_TABLES)

    # The input data is NOT correct; that needs to be fixed or this commented out
    # Load data into an in-memory sqlite database first, for performance
    db = Database(
        "sqlite://", reference_tables=REFERENCE_TABLES
    )  # creates and connects to a temporary in-memory database
    db.load_database(
        DB_PATH, verbose=False
    )  # loads the data from the data files into the database
    db.dump_sqlite(DB_NAME)  # dump in-memory database to file
    db = Database(
        "sqlite:///" + DB_NAME, reference_tables=REFERENCE_TABLES
    )  # replace database object with new file version

    return db