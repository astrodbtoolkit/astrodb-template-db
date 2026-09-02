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
        raise AssertionError(f"Schema failed Felis validation:\n{e}") from e


def test_parallax_error_id():
    db_settings = DatabaseSettings(settings_file="database.toml")
    schema = yaml.safe_load(open(db_settings.felis_path, "r"))
    parallaxes = next(table for table in schema["tables"] if table["name"] == "Parallaxes")
    parallax_error = next(column for column in parallaxes["columns"] if column["name"] == "parallax_error")

    assert parallax_error["@id"] == "#Parallaxes.parallax_error"
