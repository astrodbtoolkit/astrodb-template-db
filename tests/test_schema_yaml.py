# Tests to validate schema in felis yaml format

import yaml
from pydantic import ValidationError

from felis.datamodel import Schema


def test_schema():
    data = yaml.safe_load(open("schema/schema.yaml", "r"))
    schema = Schema.model_validate(data)

# TODO: Build database
# TODO: Confirm ORM usage
# TODO: Check constraints
