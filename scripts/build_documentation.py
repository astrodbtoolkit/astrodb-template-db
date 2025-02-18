# Script to build markdown documentation from the schema/schema.yaml file

import yaml

SCHEMA_PATH = "schema/schema.yaml"
OUT_DIR = "docs/schema/"

# Loop over each table in the schema
with open(SCHEMA_PATH, "r") as schema_file:
    schema = yaml.safe_load(schema_file)

    # Go line-by-line and build the markdown
    for table in schema["tables"]:
        table_name = table["name"]
        with open(f"{OUT_DIR}{table_name}.md", "w") as out_file:
            out_file.write(f"## {table_name}\n")
            out_file.write("### Description\n")
            out_file.write(f"{table['description']}\n")
            out_file.write("### Columns\n")
            out_file.write(
                "| Column | Datatype | Length | Description | UCD | Nullable |\n"
            )
            out_file.write("| --- | --- | --- | --- | --- | --- |\n")
            for column in table["columns"]:
                out_file.write(
                    f"| {column['name']} | {column['datatype']} | {column.get('length', '')} | {column['description']} | {column.get('ivoa:ucd', '')} | {column.get('nullable', 'True')} |\n"
                )
            out_file.write("\n")
            # Indexes
            if "indexes" in table:
                out_file.write("### Indexes\n")
                out_file.write("| Name | Columns | Description |\n")
                out_file.write("| --- | --- | --- |\n")
                for index in table["indexes"]:
                    out_file.write(
                        f"| {index['name']} | {index['columns']} | {index.get('description', '')} |\n"
                    )
                out_file.write("\n")
            # Constraints
            if "constraints" in table:
                out_file.write("### Constraints\n")
                out_file.write(
                    "| Type | Description | Columns | Referenced Columns |\n"
                )
                out_file.write("| --- | --- | --- | --- |\n")
                for constraint in table["constraints"]:
                    out_file.write(
                        f"| {constraint['@type']} | {constraint['description']} | {constraint.get('columns', '')} | {constraint.get('referencedColumns', '')} |\n"
                    )
                out_file.write("\n")
