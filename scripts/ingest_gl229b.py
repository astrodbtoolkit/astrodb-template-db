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
    "Versions",
    "PhotometryFilters",
    "Regimes",
    "AssociationList",
    "ParameterList",
    "CompanionList",
    "SourceTypeList",
]

db = load_astrodb(
    DB_NAME,
    recreatedb=True,
    felis_schema=SCHEMA_PATH,
    reference_tables=REFERENCE_TABLES,
)


def ingest_gl229b(db):
    # ingest_publication(db, doi="10.1038/378463a0")
    ingest_source(db, "Gl 229b", reference="Naka95")


# ingest_publication(
#     db,
#     doi="10.1093/mnras/stad343",
#     bibcode="2023MNRAS.520.5283G",
#     reference="Gaid23",
#     description="The TIME Table: rotation and ages of cool exoplanet host stars",
#     ignore_ads=True,
# )


def ingest_companion(db):
    gl229_data = [
        {
            "companion": "Gl 229",
        }
    ]
    with db.engine.connect() as conn:
        conn.execute(db.CompanionList.insert().values(gl229_data))
        conn.commit()


def ingest_companion_data(db):
    companion_data = [
        {
            "source": "Gl 229b",
            "companion": "Gl 229",
            "relationship": "Child",
            "reference": "Naka95",
        },
    ]
    with db.engine.connect() as conn:
        conn.execute(db.CompanionRelationships.insert().values(companion_data))
        conn.commit()


def ingest_age_parameter(db):
    parameters_data = [
        {
            "parameter": "age",
            "description": "Age of the object",
        },
    ]

    with db.engine.connect() as conn:
        conn.execute(db.ParameterList.insert().values(parameters_data))
        conn.commit()


def ingest_gl229_parameters(db):
    gl229b_data = [
        {
            "source": "Gl 229b",
            "companion": "Gl 229",
            "parameter": "age",
            "value": 3.8,
            "error": 0.5,
            "unit": "Gyr",
            "reference": "Gaid23",
        }
    ]

    with db.engine.connect() as conn:
        conn.execute(db.CompanionParameters.insert().values(gl229b_data))
        conn.commit()


def ingest_sourcetype(db):
    source_type_list_data = [
        {
            "source_type": "T7",
            "comments": "T7 dwarf",
        },
    ]
    source_types_data = [
        {"source": "Gl 229b", "source_type": "T7", "reference": "Burg06"},
    ]

    with db.engine.connect() as conn:
        conn.execute(db.SourceTypeList.insert().values(source_type_list_data))
        conn.execute(db.SourceTypes.insert().values(source_types_data))
        conn.commit()


DB_SAVE = True
ingest_gl229b(db)  # add to Sources table
# ingest_age_parameter(db)  # add to ParameterList table
ingest_companion(db)  # add to CompanionList table
ingest_gl229_parameters(db)  # add to CompanionParameters table
ingest_companion_data(db)  # add to CompanionRelationships table
ingest_sourcetype(db)  # add to SourceTypes table

if DB_SAVE:
    db.save_database("data/")
