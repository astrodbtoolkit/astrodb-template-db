# This script ingests data related to Gl 229b into the database
# Relevant websites to use for future ingestions:
# Gl 229: https://simbad.cds.unistra.fr/simbad/sim-id?Ident=Gl+229
# Gl 229b: https://simbad.cds.unistra.fr/simbad/sim-id?Ident=Gl+229b
# Gl 229b in SIMPLE: https://simple-bd-archive.org/load_solo/Gl%20229B

from astrodb_utils import load_astrodb
from astrodb_utils.sources import ingest_source
from astrodb_utils.publications import ingest_publication

# Load the database
DB_NAME = "tests/astrodb_template_tests.sqlite"
SCHEMA_PATH = "schema/schema.yaml"
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
db = load_astrodb(DB_NAME, recreatedb=True, felis_schema=SCHEMA_PATH, reference_tables=REFERENCE_TABLES)

# ingest_publication(db, doi="10.1038/378463a0")
# ingest_publication(db, doi="10.1086/498563")  # Burg06

# ingest_source(db, "Gl 229b", reference="Naka95")

# companion_data = [
#     {
#         "source": "Gl 229b",
#         "companion": "Gl 229",
#         "relationship": "Child",
#         "reference": "Naka95",
#     },
# ]

# with db.engine.connect() as conn:
#     conn.execute(db.CompanionRelationships.insert().values(companion_data))
#     conn.commit()

source_type_list_data = [
    {"source_type": "T7",
     "comments": "T7 dwarf",},
]
source_types_data = [
    {"source": "Gl 229b", "source_type": "T7", "reference": "Burg06"},
]

with db.engine.connect() as conn:
    conn.execute(db.SourceTypeList.insert().values(source_type_list_data))
    conn.execute(db.SourceTypes.insert().values(source_types_data))
    conn.commit()
 
db.save_database("data/")
