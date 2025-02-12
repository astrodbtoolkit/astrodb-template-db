from astrodb_utils import load_astrodb
from astrodb_utils.sources import ingest_source
from astrodb_utils.publications import ingest_publication

# Load the database
DB_NAME = "tests/astrodb_template_tests.sqlite"
SCHEMA_PATH = "schema/schema.yaml"
db = load_astrodb(DB_NAME, recreatedb=True, felis_schema=SCHEMA_PATH)


ingest_publication(db, doi="10.1038/378463a0")

ingest_source(db, "Gl 229b", reference="Naka95")

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

db.save_database("data/")
