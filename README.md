astrodb-template-db
---------------------------

[![Test astrotemplate-db](https://github.com/astrodbtoolkit/astrotemplate-db/actions/workflows/run_tests.yml/badge.svg)](https://github.com/astrodbtoolkit/astrotemplate-db/actions/workflows/run_tests.yml)


A template for astronomical databases. This is a [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) — you can use this to create your own repository, then build your use case from there on out.

We encourage users to follow the detailed best practices for astronomical databases outlined in [Chen et al. 2022](https://iopscience.iop.org/article/10.3847/1538-4365/ac6268).


Installation instructions
---------------------------
For detailed and up-to-date installation and database setup instructions, see the [astrodb-scripts installation instructions](https://astrodb-scripts.readthedocs.io/en/latest/pages/installation.html).


How does the database work?
---------------------------
[todo: add a bunch of clear description here]
At the user level, customizing this database involves working with the [schema](https://github.com/astrodbtoolkit/astrotemplate-db/blob/master/src/astrotemplate/schema.py). In database-speak, a "schema" describes how various "tables" (aggregates of related data) are related to one another.

Under the hood, this template leans heavily on [AstrodbKit2](https://github.com/astrodbtoolkit/AstrodbKit2), a codebase built on [SQLAlchemy](https://www.sqlalchemy.org/).

Units
---------------------------
Per [Chen et al. 2022](https://iopscience.iop.org/article/10.3847/1538-4365/ac6268), we explicitly define the units
for each table in their name (e.g., in the `Sources` table, the column with Right Ascension values
is named `ra_deg`). Doing so removes unit ambiguity when querying and modifying the database.

We plan to support passing Astropy units to the database, with the database  automatically converting into the
internal units of each table upon ingest. We aim to have internal tests require that each table with a quantity
has units in the table metadata that resolve to an Astropy unit.

