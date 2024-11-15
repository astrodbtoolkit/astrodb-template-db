# Tests to validate schema in felis yaml format

import pytest
import yaml
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
from astrodbkit.astrodb import AstrodbQuery

from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder

@pytest.fixture()
def schema():
    # Load and validate schema file
    data = yaml.safe_load(open("schema/schema.yaml", "r"))
    schema = Schema.model_validate(data)
    return schema

@pytest.fixture()
def db_object(schema):
    # Build in-memory database
    metadata = MetaDataBuilder(schema).build()

    engine = create_engine("sqlite:///:memory:")

    # Workaround for SQLite since it doesn't support schema
    with engine.begin() as conn:
        conn.execute(sa.text("ATTACH ':memory:' AS astrodb"))

    metadata.create_all(engine)
    return engine, metadata

# TODO: Confirm ORM usage
# TODO: Check constraints

def test_inserts(db_object):
    # Attempt insert with ORM

    engine, metadata = db_object
    
    with engine.connect() as conn:
        metadata.reflect(conn)

    # This requires us to use the DB name (astrodb)
    Sources = metadata.tables['astrodb.Sources']
    source_data = [
        {"source": "Fake 1", "ra_deg": 9.0673755, },
    ]

    with engine.connect() as conn:
        conn.execute(Sources.insert().values(source_data))
        conn.commit()

    # Explicitly with ORM
    # Does not work because the Table object (Sources) is not callable
    # Session = sessionmaker(bind=engine, query_cls=AstrodbQuery)
    # s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 1")
    # with Session() as session:
    #     session.add(s)
    #     session.commit()