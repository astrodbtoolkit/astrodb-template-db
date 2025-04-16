"""
These tests are not called on every push or pull request. They're time-intensive, so on GitHub they're only called
monthly. To run them locally, use the following command:

    pytest -s -rpP tests/scheduled_checks.py

Because the filename doesn't begin with test_, it's not automatically run with pytest. The -s flag is used to print
the results of the tests, and the -rpP flags are used to suppress the output of the tests that pass.

"""
import pytest
import tqdm
import requests
from astroquery.simbad import Simbad

from astrodbkit.utils import _name_formatter, internet_connection


def test_SIMBAD_resolvable(db):
    # Verify that sources have SIMBAD-resolvable names```
    all_sources = db.query(db.Sources.c.source).all()
    name_list = [s[0] for s in all_sources]
    # print(f"SIMBAD name list: {name_list}")

    # Include all SIMBAD Identifiers and our provided name to the SIMBAD query results table.
    Simbad.add_votable_fields("ids")

    simbad_results = Simbad.query_objects(name_list)
    no_result_rows = []
    duplicate_rows = []
    no_db_matches = []
    unique_matches = []
    for row in simbad_results[["main_id", "ids"]].iterrows():
        try:
            name, ids = row[0].decode("utf-8"), row[1].decode("utf-8")
            # print(f"SIMBAD name: {name}")
        except AttributeError:
            # Catch decoding error
            name, ids = row[0], row[1]

        simbad_names = [
            _name_formatter(s)
            for s in ids.split("|")
            if _name_formatter(s) != "" and _name_formatter(s) is not None
        ]
        if len(simbad_names) == 0:
            no_result_rows += [row]
            print(f"No SIMBAD names for {name}")

        # Examine DB for each input, displaying results when more than one source matches
        t = db.search_object(
            simbad_names, output_table="Sources", fmt="astropy", fuzzy_search=False
        )
        if len(t) > 1:
            duplicate_rows += [row]
            print(f"Duplicate rows for {name}\n")
            print(f"   Searched simbad names: {simbad_names}")
            print(f"   Database matches: \n {t}")
        elif len(t) == 0:
            no_db_matches += [row]
            print(f"No database matches for {name}")
        else:
            unique_matches += [row]

    assert len(no_result_rows) == 0, f"No SIMBAD names for {no_result_rows}"
    assert len(duplicate_rows) == 0, f" duplicate rows for {duplicate_rows}"
    assert len(no_db_matches) == 0, f"No database matches for {no_db_matches}"
    assert len(unique_matches) == len(
        all_sources
    ), f"Unique matches for {unique_matches}, expected {len(all_sources)}"


@pytest.mark.skip(reason="There are no spectra yet in the template")
def test_spectra_urls(db):
    spectra_urls = db.query(db.Spectra.c.access_url).astropy()
    broken_urls = []
    codes = []
    internet, _ = internet_connection()
    if internet:
        for spectrum_url in tqdm(spectra_urls["access_url"]):
            request_response = requests.head(spectrum_url)
            status_code = request_response.status_code
            # The website is up if the status code is 200
            # cuny academic commons links give 301 status code
            if status_code not in (200, 301):
                broken_urls.append(spectrum_url)
                codes.append(status_code)

    # Display broken spectra regardless if it's the number we expect or not
    print(f"found {len(broken_urls)} broken spectra urls: {broken_urls}, {codes}")

    assert len(broken_urls) == 4
