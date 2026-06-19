# GitHub Actions workflows

This directory holds the CI/CD workflows for this AstroDB database repo. The table below
summarizes each one; details follow.

| Workflow | File | Triggers | What it does |
|----------|------|----------|--------------|
| Test database contents | [run_tests.yml](run_tests.yml) | push/PR to `main`, manual | Runs the full pytest suite on Python 3.11–3.13 |
| Test astrodb-utils with this database | [run_astrodb_utils.yml](run_astrodb_utils.yml) | push/PR to `main`, manual | Runs `astrodb_utils`'s own test suite against this branch of the database |
| Scheduled tests | [run_scheduled_tests.yml](run_scheduled_tests.yml) | monthly cron, manual | Runs the slow checks that hit external services (SIMBAD, SVO) |
| Make ER diagram | [make_erd.yml](make_erd.yml) | push to `main`, manual | Regenerates `docs/figures/schema_erd.png` and commits it |
| Generate Database SQLite file | [generate_db.yml](generate_db.yml) | manual, release published | Builds the SQLite database file and commits it (plus a release-tagged copy) |

## Test database contents — [run_tests.yml](run_tests.yml)

The primary CI gate. On every push and pull request to `main` (and on manual
dispatch), it installs the dependencies and runs the full test suite across a
matrix of Python 3.11, 3.12, and 3.13:

```bash
uv run pytest -p no:warnings tests
```

These tests rebuild the SQLite database from `schema.yaml` + `data/` and validate
both the schema and the JSON data (foreign keys resolve, required fields populated,
units/values sane).

## Test astrodb-utils with this database — [run_astrodb_utils.yml](run_astrodb_utils.yml)

Reverse-direction integration check: it checks out the
[`astrodbtoolkit/astrodb_utils`](https://github.com/astrodbtoolkit/astrodb_utils)
companion package, checks out *this* database repo into a subdirectory, and runs
`astrodb_utils`'s own pytest suite against the current branch of the database.
This catches cases where a schema/data change here would break the downstream
tooling.

Runs on push/PR to `main` and on manual dispatch. The manual-dispatch form takes a
`scripts_branch` input so you can test against a non-`main` branch of
`astrodb_utils`.

> **Most databases can delete this workflow.** It exists to test the `astrodb_utils`
> package itself against the template, which matters for maintainers of the
> `astrodbtoolkit` ecosystem. If you've forked this repo to build your own database,
> you can safely remove [run_astrodb_utils.yml](run_astrodb_utils.yml).

## Scheduled tests — [run_scheduled_tests.yml](run_scheduled_tests.yml)

Runs the slow checks in `tests/scheduled_checks.py` that hit external services
(e.g. SIMBAD name resolution, SVO filter validation). These are too slow/flaky to
run on every push, so they run on a monthly cron (first of the month, 01:30 UTC)
across Python 3.11–3.13, and can also be triggered manually:

```bash
uv run pytest -s -rpP tests/scheduled_checks.py
```

## Make ER diagram — [make_erd.yml](make_erd.yml)

Regenerates the entity-relationship diagram from `schema.yaml` and commits the
result. It installs graphviz, runs `scripts/make_schema_erd.py`, and—only if the
PNG actually changed—commits `docs/figures/schema_erd.png` back to the repo.

Runs on push to `main` and on manual dispatch. Uses `secrets.GH_TOKEN` so the
commit it pushes can re-trigger other workflows if needed.

## Generate Database SQLite file — [generate_db.yml](generate_db.yml)

Builds the committed SQLite database file via `build_db_from_json database.toml`
and commits it back to the repo. This is **not** run on every push, so the
committed sqlite file can lag behind `schema.yaml` / `data/` between runs.

Triggers:

- **Manual dispatch** — rebuilds and commits the sqlite file to the current branch.
- **Release published** — additionally creates a release-tagged copy of the sqlite
  file, commits both to `main`, and moves the release tag to the new commit.

## Repository secrets

The two workflows that commit back to the repo — [make_erd.yml](make_erd.yml) and
[generate_db.yml](generate_db.yml) — need repository secrets to identify the
committer and (for the ER diagram) to push with a token that can re-trigger other
workflows. If these secrets are missing, those workflows will fail or commit with
an empty/blank identity; the read-only test workflows are unaffected.

| Secret | Used by | What it is |
| --- | --- | --- |
| `USER_LOGIN` | `make_erd.yml`, `generate_db.yml` | The GitHub username used for the bot commits (sets `git config user.name`). |
| `USER_ID` | `make_erd.yml`, `generate_db.yml` | The numeric GitHub user ID, used to build the no-reply commit email `${USER_ID}+${USER_LOGIN}@users.noreply.github.com`. |
| `GH_TOKEN` | `make_erd.yml` | A personal access token used to check out and push. Unlike the default `GITHUB_TOKEN`, pushes made with a PAT can trigger other workflows (e.g. the test suite on the auto-commit). |

Note that only `make_erd.yml` checks out with `GH_TOKEN`. `generate_db.yml` pushes its
auto-commit using the default `GITHUB_TOKEN`, so **commits it makes do not re-trigger
other workflows** (the test suite won't run on the auto-committed sqlite file). This is
usually fine, but if you want the generated database committed *and* re-tested, switch
`generate_db.yml`'s checkout to use `GH_TOKEN` as well.

### Finding the values

- **`USER_LOGIN`** — the account whose identity should appear on the automated
  commits. This can be your own username or a dedicated bot account.
- **`USER_ID`** — the numeric ID for that login. Look it up via the GitHub API:

  ```bash
  curl -s https://api.github.com/users/<USER_LOGIN> | grep '"id"'
  ```

- **`GH_TOKEN`** — create a Personal Access Token at
  **GitHub → Settings → Developer settings → Personal access tokens**. A fine-grained
  token scoped to this repository with **Contents: Read and write** permission is
  sufficient (a classic token needs the `repo` scope). Treat it as a password and
  set it to expire/rotate as appropriate.

### Adding them to the repo

In the repository on GitHub, go to **Settings → Secrets and variables → Actions →
New repository secret**, then add each secret by name (`USER_LOGIN`, `USER_ID`,
`GH_TOKEN`) with its value. Secrets are write-only — once saved you can update or
delete them, but not view the stored value.

You can also set them with the [GitHub CLI](https://cli.github.com/):

```bash
gh secret set USER_LOGIN --body "<your-username>"
gh secret set USER_ID    --body "<your-numeric-id>"
gh secret set GH_TOKEN    # prompts for the value without echoing it
```

> If you delete [make_erd.yml](make_erd.yml) and [generate_db.yml](generate_db.yml)
> (e.g. you don't commit a generated ER diagram or sqlite file), none of these
> secrets are required.

## Notes

- All workflows use [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv)
  and `uv pip install` to manage dependencies; there is no `pyproject.toml` in this
  repo, so dependencies are listed explicitly in each workflow.
