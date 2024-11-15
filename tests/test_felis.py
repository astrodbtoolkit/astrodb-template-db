# Tests to validate schema in felis yaml format

import pytest
import yaml
import sqlalchemy as sa
from sqlalchemy import create_engine
from pydantic import ValidationError

from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder

@pytest.fixture()
def schema():
    # Load and validate schema file
    data = yaml.safe_load(open("schema/schema.yaml", "r"))
    schema = Schema.model_validate(data)
    return schema


def test_database(schema):
    # Build in-memory database
    metadata = MetaDataBuilder(schema).build()

    engine = create_engine("sqlite:///:memory:")

    # Workaround for SQLite since it doesn't support schema
    with engine.begin() as conn:
        conn.execute(sa.text("ATTACH ':memory:' AS astrodb"))

    metadata.create_all(engine)


# TODO: Confirm ORM usage
# TODO: Check constraints


