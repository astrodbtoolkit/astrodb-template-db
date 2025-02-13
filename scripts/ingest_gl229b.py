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
db = load_astrodb(DB_NAME, recreatedb=False, felis_schema=SCHEMA_PATH)

def already_ingested(db):
    ingest_publication(db, doi="10.1038/378463a0")
    ingest_source(db, "Gl 229b", reference="Naka95")


def ingest_companion(db):
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
        conn.execute(db.ParametersList.insert().values(parameters_data))
        conn.commit()


def ingest_gl229_parameters(db):
    ingest_publication(db, doi="10.1093/mnras/stad343")
    
    


    gl229b_data = [      
        {
            "source": "Gl 229b",
            "companion": "Gl 229",
            "parameter": "age",
            "value": 3.8,
            "value_error": 0.5,
            "value_unit": "Gyr",
            "reference": "Gaid23",
        }
    ]

    with db.engine.connect() as conn:
        conn.execute(db.CompanionParameters.insert().values(gl229b_data))
        conn.commit()


#ingest_age_parameter(db)
ingest_gl229_parameters(db)

db.save_database("data/")
