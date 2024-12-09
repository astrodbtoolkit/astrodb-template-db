# Script to generate an Entity-Relation Diagram (ERD) for the database

import sys

from astrodbkit.astrodb import Database, create_database
from eralchemy2 import render_er

sys.path.append("./")  # needed for github actions to find the template module
from schema.schema_template import *
from schema.schema_template import REFERENCE_TABLES

# Connect to an in-memory sqlite database
create_database(connection_string="sqlite://")
db = Database("sqlite://", reference_tables=REFERENCE_TABLES)

# Create ER model from the database metadata
filename = "schema/schema.png"
render_er(db.metadata, filename)
