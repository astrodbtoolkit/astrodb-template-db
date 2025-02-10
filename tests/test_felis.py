# Test using the Felis validation tools

import yaml
from pydantic import ValidationError

from felis.datamodel import Schema

SCHEMA_PATH = "schema/schema.yaml"


def test_schema():
    data = yaml.safe_load(open(SCHEMA_PATH, "r"))

    try:
        schema = Schema.model_validate(data)
    except ValidationError as e:
        print(e)
