# Test using the Felis validation tools

import yaml
from pydantic import ValidationError

from felis.datamodel import Schema
from astrodb_utils import read_database_settings

def test_schema():
    settings = read_database_settings()
    schema_path = settings["felis_path"]
    data = yaml.safe_load(open(schema_path, "r"))

    try:
        schema = Schema.model_validate(data)  # noqa: F841
    except ValidationError as e:
        print(e)
