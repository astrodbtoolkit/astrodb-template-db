# Tests to validate schema in felis yaml format

import pytest
import yaml
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import IntegrityError
# from sqlite3 import IntegrityError
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

    # TODO: consider switching to real test file
    # Noticing that each test does not know about other inserts
    engine = create_engine("sqlite:///:memory:")

    # Workaround for SQLite since it doesn't support schema
    with engine.begin() as conn:
        conn.execute(sa.text("ATTACH ':memory:' AS astrodb"))

    metadata.create_all(engine)

    return engine, metadata


def test_inserts(db_object):
    # Attempt insert with ORM

    engine, metadata = db_object

    # Creating basic pointers to the tables
    # This requires us to use the DB name (astrodb)
    Sources = metadata.tables['astrodb.Sources']
    Publications = metadata.tables['astrodb.Publications']

    # Data to be loaded, as list of dictionaries
    ref_data = [
        {"reference": "Ref 1",},
    ]
    source_data = [
        {"source": "Fake 1", "ra_deg": 9.0673755, "dec_deg": 18.352889, "reference": "Ref 1"},
    ]

    # Actual ingest of data
    with engine.connect() as conn:
        conn.execute(Publications.insert().values(ref_data))
        conn.execute(Sources.insert().values(source_data))
        conn.commit()


def test_orm(db_object):
    # Testing use via ORM objects

    engine, metadata = db_object

    # Use Automap to prepare SQLAlchemy Table objects
    # DB tables *must* have primary keys to be automapped
    Base = automap_base(metadata=metadata)
    Base.prepare()
    
    # Creating the actual Table objects
    Publications = Base.classes.Publications
    Sources = Base.classes.Sources

    # Session = sessionmaker(bind=engine, query_cls=AstrodbQuery)
    p = Publications(reference="Ref 2")
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 2")
    with Session(engine) as session:
        session.add(p)
        session.add(s)
        session.commit()


def test_constraints(db_object):
    # Testing constraints in the DB

    engine, metadata = db_object

    # Use Automap to prepare SQLAlchemy Table objects
    # DB tables *must* have primary keys to be automapped
    Base = automap_base(metadata=metadata)
    Base.prepare()
    
    # Creating the actual Table objects
    Publications = Base.classes.Publications
    Sources = Base.classes.Sources

    # Actual ingests
    session = Session(engine)
    p = Publications(reference="Ref 2")
    session.add(p)
    session.commit()

    # TODO: Capture errors when they are actually raised!

    # Try negative RA
    s = Sources(source="Bad RA 1", ra_deg=-273.54, dec_deg=-32.79, reference="Ref 2")
    with pytest.raises(IntegrityError, match="CHECK constraint failed: check_ra"):
        session.add(s)
        session.commit()
    
    session.rollback()

    # Try out-of-bounds RA
    s = Sources(source="Bad RA 2", ra_deg=99999, dec_deg=-32.79, reference="Ref 2")
    with pytest.raises(IntegrityError, match="CHECK constraint failed: check_ra"):
        session.add(s)
        session.commit()

    session.rollback()
