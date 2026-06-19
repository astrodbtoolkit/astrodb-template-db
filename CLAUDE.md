# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A template schema for astronomical databases, part of the `astrodbtoolkit` ecosystem. The repo itself contains no
application code — it defines a database schema (Felis YAML), example data (JSON), and the test suite that
validates them. Downstream users fork this repo as a starting point for their own astronomical database.

## Git and GitHub

The user handles all *state-changing* git and GitHub actions by hand. Do **not** run anything
that mutates history or remote state on the user's behalf — e.g. `git commit`, `git push`,
`git merge`, branch operations, or `gh` commands that create/edit/close things (PRs, issues,
releases, comments). Even when asked to "commit," default to preparing the change and letting
the user perform the git step themselves.

Read-only work is fine and encouraged: inspecting local state (`git status`, `git diff`,
`git log`) and GitHub *research* via `gh` (e.g. `gh pr view`, `gh pr list`, `gh issue view`,
`gh run list`, `gh api` GET requests) to gather context.

When work is at a natural commit point: remind the user that it's ready, summarize what
changed, and offer to help (e.g. draft a commit message or PR description, show the diff).
Wait for the user to do the actual commit/push/PR.

Keep suggested commit messages brief — a short one-line summary is usually enough. Don't
spend many tokens overthinking them.

## Documentation

- **Companion package (astrodb-utils)**: <https://astrodb-utils.readthedocs.io/en/latest/>
- **Getting started with a new database**: <https://astrodb-utils.readthedocs.io/en/latest/pages/make_new_db/getting_started_new_database.html>
- **Schema docs**: [docs/schema/](docs/schema/) (auto-generated, one markdown file per table)
- **CI/CD workflows**: [.github/workflows/README.md](.github/workflows/README.md) (what each GitHub Actions
  workflow does, and the repo secrets the committing workflows need)

## Commands

There is no `pyproject.toml` in this repo — dependencies are not pinned/locked here, and `uv sync`/`uv add` won't
work. Install the packages tests/scripts need directly:

```bash
uv pip install astrodbkit astrodb-utils lsst-felis pytest pytest-cov
```

Run the full test suite (this is what CI does):

```bash
uv run pytest -p no:warnings tests
```

Run a single test file or test:

```bash
uv run pytest tests/test_contents_sources.py
uv run pytest tests/test_contents_sources.py::test_source_names
```

Run the monthly scheduled checks (slow — hits SIMBAD/external services, not run on every push):

```bash
uv run pytest -s -rpP tests/scheduled_checks.py
```

Regenerate the per-table markdown docs in `docs/schema/` from `schema.yaml`:

```bash
uv run python scripts/build_schema_docs.py
```

Regenerate the ER diagram (`docs/figures/schema_erd.png`) — requires graphviz:

```bash
uv run python scripts/make_schema_erd.py
```

`astrodb-template.sqlite` is also built and committed automatically by the "Generate Database SQLite file"
GitHub Actions workflow. It runs on manual `workflow_dispatch` or when a release is published — on a release it
additionally creates a release-tagged copy of the sqlite file and moves the release tag to the new commit. It
does not run on every push/PR, so the committed sqlite file can lag behind `schema.yaml`/`data/` between manual
runs or releases.

## Architecture

**Source of truth is `schema.yaml`**, a Felis-format schema defining every table, column, datatype, and foreign
key relationship in the database. `database.toml` points at this schema file and at `data/`, and lists which
tables are "lookup tables" (reference tables that must be loaded before tables that depend on them).

**Data lives as JSON, not SQL:**

- [data/source/](data/source/) — one JSON file per astronomical object (e.g. `gl_229b.json`), containing rows
  for that object across multiple tables (Sources, Names, Photometry, CompanionParameters, etc.)
- [data/reference/](data/reference/) — JSON files for lookup/reference tables (Publications, Instruments,
  PhotometryFilters, etc.) shared across all objects

**The build pipeline** (`astrodb_utils.build_db_from_json`, called from `tests/conftest.py` and CI) reads
`schema.yaml` + `database.toml`, creates a fresh SQLite database, and loads every JSON file in `data/` into it,
honoring the lookup-table load order. This produces `astrodb-template.sqlite`. The `db` fixture in
`tests/conftest.py` is session-scoped and autouse — every test gets a freshly rebuilt database, so tests don't
need to manage database state themselves.

**Test suite shape**: `test_felis.py` validates `schema.yaml` itself against the Felis schema spec.
`test_database.py` exercises the SQLAlchemy ORM layer generically. `test_contents_*.py` files validate the
*data* — e.g. that foreign keys resolve, required fields are populated, units/values are sane for a given table
group (kinematics, morphology, parameters, positions, sources). When adding a new object's data under
`data/source/`, the relevant `test_contents_*.py` checks are what will catch malformed entries.

**`scripts/`** is a mix of current and legacy tooling — not everything there reflects current practice:

- `build_schema_docs.py`, `make_schema_erd.py` — current, used by CI
- `ingest_gl229b.py`, `ingest_pso0318` — example/reference ingestion scripts showing how to use
  `astrodb_utils.sources.ingest_source` etc. to add a new object's data; not run automatically
- `build_postgres.py`, `intitialize_utils.py` — older scripts predating the current Felis/JSON-based workflow;
  treat with suspicion before relying on them (e.g. they reference `schema/schema.yaml` and a Postgres path that
  isn't how the template is built today)
