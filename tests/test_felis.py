# Tests to validate schema in felis yaml format

import os
import pytest
import yaml
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.schema import CreateSchema

from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder
from felis.db.utils import DatabaseContext

from astrodbkit.astrodb import Database

DB_NAME = "felis_test.sqlite"
SCHEMA_NAME = "astrodb"
CONNECTION_STRING = "sqlite:///" + DB_NAME
# CONNECTION_STRING = "postgresql+psycopg2://postgres:password@localhost:5432/felis"

REFERENCE_TABLES = [
    "Publications",
    "Telescopes",
    "Instruments",
    "Modes",
    "PhotometryFilters",
    "Versions",
    "Parameters",
    "Regimes",
]


@pytest.fixture(scope="module")
def schema():
    # Load and validate schema file
    data = yaml.safe_load(open("schema/schema.yaml", "r"))
    schema = Schema.model_validate(data)
    return schema


@pytest.fixture(scope="module")
def db_object(schema):
    # Build test database

    # Remove any existing copy of the test database
    if CONNECTION_STRING.startswith("sqlite") and os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # Using test file for sqlite; in-memory does not preseve inserts
    engine = create_engine(CONNECTION_STRING)

    # Workaround for SQLite since it doesn't support schema
    if CONNECTION_STRING.startswith("sqlite"):
        with engine.begin() as conn:
            conn.execute(sa.text("ATTACH '" + DB_NAME + "' AS astrodb"))

    # Create database from Felis schema
    metadata = MetaDataBuilder(schema).build()
    if CONNECTION_STRING.startswith("postgresql"):
        with engine.connect() as connection:
            connection.execute(CreateSchema(SCHEMA_NAME, if_not_exists=True))
            connection.commit()
    metadata.create_all(bind=engine)

    # Use AstroDB Database object
    if CONNECTION_STRING.startswith("postgresql"):
        # Set default schema to be using for postgres
        connect_args = {"options": f"-csearch_path={SCHEMA_NAME}"}
    else:
        connect_args = {}
    db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, connection_arguments=connect_args)

    # Confirm DB has been created
    if CONNECTION_STRING.startswith("sqlite"):
        assert os.path.exists(DB_NAME)

    return db


def test_inserts(db_object):
    # Attempt insert with ORM

    engine, metadata = db_object.engine, db_object.metadata

    # Creating basic pointers to the tables
    # If using Felis metadata object (instead of AstroDB.Database), need to include the DB name (astrodb)
    Sources = metadata.tables["Sources"]
    Publications = metadata.tables["Publications"]

    # Data to be loaded, as list of dictionaries
    ref_data = [
        {
            "reference": "Ref 1",
        },
    ]
    source_data = [
        {
            "source": "Fake 1",
            "ra_deg": 9.0673755,
            "dec_deg": 18.352889,
            "reference": "Ref 1",
        },
    ]

    # Actual ingest of data
    with engine.connect() as conn:
        conn.execute(Publications.insert().values(ref_data))
        conn.execute(Sources.insert().values(source_data))
        conn.commit()


def test_orm(db_object):
    # Testing use via ORM objects

    db = db_object

    # Use Automap to prepare SQLAlchemy Table objects
    # DB tables *must* have primary keys to be automapped
    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Publications = Base.classes.Publications
    Sources = Base.classes.Sources
    Names = Base.classes.Names

    # Running ingests
    p = Publications(reference="Ref 2")
    s = Sources(source="V4046 Sgr", ra_deg=273.54, dec_deg=-32.79, reference="Ref 2")
    n = Names(source="V4046 Sgr", other_name="Hen 3-1636")
    with Session(db.engine) as session:
        session.add(p)
        session.add(s)
        session.add(n)
        session.commit()


def test_constraints(db_object):
    # Testing constraints in the DB

    db = db_object

    # Use Automap to prepare SQLAlchemy Table objects
    # DB tables *must* have primary keys to be automapped
    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Sources = Base.classes.Sources

    # Try negative RA
    s = Sources(source="Bad RA 1", ra_deg=-273.54, dec_deg=-32.79, reference="Ref 2")
    with pytest.raises(IntegrityError):
        with Session(db.engine) as session:
            session.add(s)
            session.commit()

    # Try out-of-bounds RA
    s = Sources(source="Bad RA 2", ra_deg=99999, dec_deg=-32.79, reference="Ref 2")
    with pytest.raises(IntegrityError):
        with Session(db.engine) as session:
            session.add(s)
            session.commit()

    # Try adding with missing foreign key (reference)
    s = Sources(source="Bad ref", ra_deg=273.54, dec_deg=-32.79, reference="Missing ref")
    with pytest.raises(IntegrityError):
        with Session(db.engine) as session:
            session.add(s)
            session.commit()

    # Try NULL value (no reference)
    s = Sources(source="Bad ref", ra_deg=273.54, dec_deg=-32.79)
    with pytest.raises(IntegrityError):
        with Session(db.engine) as session:
            session.add(s)
            session.commit()


def test_queries(db_object):
    # Queries using AstroDB

    db = db_object

    # Confirm the right tables are present
    assert len(db.metadata.tables.keys()) == 5
    assert "Sources" in db.metadata.tables.keys()
    assert "Publications" in db.metadata.tables.keys()
    assert "Names" in db.metadata.tables.keys()
    assert "Telescopes" in db.metadata.tables.keys()
    assert "Instruments" in db.metadata.tables.keys()



    # print(db.query(db.Sources).table())
    # print(db.sql_query("select * from Sources", fmt="astropy"))

    # Check counts with some constraints
    assert db.query(db.Publications).count() == 2
    assert db.query(db.Sources).count() == 2
    assert db.query(db.Sources).filter(db.Sources.c.source == "Fake V4046 Sgr").count() == 0
    assert db.query(db.Sources).filter(db.Sources.c.source == "V4046 Sgr").count() == 1

    t = db.inventory("V4046 Sgr")
    assert "Names" in t.keys()
    assert len(t["Names"]) == 1
