"""
These tests are not called on every push or pull request. They're time-intensive, so on GitHub they're only called
monthly. To run them locally, use the following command:

    pytest -s -rpP tests/scheduled_checks.py

Because the filename doesn't begin with test_, it's not automatically run with pytest. The -s flag is used to print
the results of the tests, and the -rpP flags are used to suppress the output of the tests that pass.

"""
from astroquery.simbad import Simbad

from astrodbkit2.utils import _name_formatter

def test_SIMBAD_resolvable(db):
    # Verify that all sources have valid names
    results = db.query(db.Sources.c.source).all()
    name_list = [s[0] for s in results]

    # Add all IDS to the Simbad output as well as the user-provided id
    Simbad.add_votable_fields("ids")
    Simbad.add_votable_fields("typed_id")

    simbad_results = Simbad.query_objects(name_list)
    not_found_in_simbad = []
    multiple_matches_in_db = []
    for row in simbad_results[["TYPED_ID", "IDS"]].iterrows():
        try:
            name, ids = row[0].decode("utf-8"), row[1].decode("utf-8")
        except AttributeError:
            # Catch decoding error
            name, ids = row[0], row[1]

        simbad_names = [
            _name_formatter(s)
            for s in ids.split("|")
            if _name_formatter(s) != "" and _name_formatter(s) is not None
        ]
        if len(simbad_names == 0):
            no_result_rows += [row]


        # Examine DB for each input, displaying results when more than one source matches
        t = db.search_object(
            simbad_names, output_table="Sources", fmt="astropy", fuzzy_search=False
        )
        if len(t) != 1:
            duplicate_rows += [row]

    assert len(no_result_rows) == 0 and len(duplicate_rows) == 0, (f"No SIMBAD names for {no_result_rows},"
                                                                   f" duplicate rows for {duplicate_rows}")
