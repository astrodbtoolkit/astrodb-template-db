# Python script to build the database from the shema.yaml file

import os
import yaml
from astrodbkit.astrodb import Database, create_database
from dotenv import load_dotenv
import subprocess

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema

DB_PATH = "data"
SCHEMA_NAME = "astrodb_template"
SCHEMA_PATH = "schema/schema.yaml"
REFERENCE_TABLES = [
    "Publications",
    "Telescopes",
    "Instruments",
    "PhotometryFilters",
    "Versions",
    "Regimes",
    "AssociationList",
    "SourceTypeList",
    "ParameterList",
    "CompanionList",
]
DELETE_SCHEMA = True
LOAD_DATABASE = True

# Get information from .env file in root directory
load_dotenv()
connection_string = os.environ.get("TEMPLATE_CONNECTION_STRING")

# Get schema name
data = yaml.safe_load(open(SCHEMA_PATH, "r"))
print(f"Preparing for database schema {SCHEMA_NAME}")

# Clear database/schema if requested. Postgres is case-sensitive!
if DELETE_SCHEMA:
    print("Deleting existing schema and database tables")
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        conn.execute(DropSchema(SCHEMA_NAME, cascade=True, if_exists=True))
        conn.execute(DropSchema("TAP_SCHEMA", cascade=True, if_exists=True))
        conn.commit()

# AstrodbKit version of creating and connecting to the database
print(f"Creating {SCHEMA_NAME}")
create_database(connection_string=connection_string, felis_schema=SCHEMA_PATH)

# Create TAP_SCHEMA for later use
print("Creating TAP_SCHEMA")
db = Database(
    connection_string=connection_string,
    schema=SCHEMA_NAME,
    reference_tables=REFERENCE_TABLES,
)
with db.engine.connect() as conn:
    conn.execute(CreateSchema("TAP_SCHEMA", if_not_exists=True))
    conn.commit()

# TAP metadata initialization and load
# Requires the schema to be created first and specified in the call
commands = f"""
echo "Loading TAP_SCHEMA..."
felis init-tap {connection_string} --tap-schema-name=TAP_SCHEMA
felis load-tap --engine-url={connection_string} --tap-schema-name=TAP_SCHEMA schema/schema.yaml
"""
# Run the commands
subprocess.run(commands, shell=True, check=True)

# Actually try to load some data
if LOAD_DATABASE:
    print("Loading database")
    db.load_database(DB_PATH, verbose=False)

print("Database ready")
