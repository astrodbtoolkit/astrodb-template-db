import pytest
from astrodb_utils.photometry import fetch_svo


@pytest.mark.xfail(reason="SVO filter checks are not implemented yet. Issue #164")
def test_filters_svo(db):
    # Check that the filters are in the SVO database
    filters_table = db.query(db.PhotometryFilters).astropy()
    for filter in filters_table:
        fetch_svo(filter_name=filter["band"])

    assert len(t) == 0, f"{len(t)} PhotometryFilters failed SVO checks"
