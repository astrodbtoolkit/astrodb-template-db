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

Under the hood, this template leans heavily on [AstrodbKit](https://github.com/astrodbtoolkit/AstrodbKit), a codebase built on [SQLAlchemy](https://www.sqlalchemy.org/).

