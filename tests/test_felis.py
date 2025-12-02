# Test using the Felis validation tools

import yaml
from pydantic import ValidationError

from felis.datamodel import Schema
from astrodb_utils.loaders import DatabaseSettings

def test_schema():
    db_settings = DatabaseSettings(settings_file="database.toml")
    schema_path = db_settings.felis_path
    data = yaml.safe_load(open(schema_path, "r"))

    try:
        schema = Schema.model_validate(data)  # noqa: F841
    except ValidationError as e:
        print(e)
