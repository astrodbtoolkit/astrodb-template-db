import os
import pytest
import logging

# from astrodbkit.astrodb import Database, create_database
import astrodb_utils
from astrodb_utils import build_db_from_json

logger = logging.getLogger(__name__)

# Create a fresh template database for the data and integrity tests
@pytest.fixture(scope="session", autouse=True)
def db():
    logger.info(f"Using version {astrodb_utils.__version__} of astrodb_utils")

    db = build_db_from_json()

    # Confirm file was created
    assert os.path.exists(
        "astrodb-template.sqlite"
    ), "Database file 'astrodb-template.sqlite' was not created."

    logger.info(
        "Loaded AstroDB Template database using build_db_from_json function in conftest.py"
    )

    return db
