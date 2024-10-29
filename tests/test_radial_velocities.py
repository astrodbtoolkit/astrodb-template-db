"""
testing module to test the contents of the radial velocities table.
"""
import sys
sys.path.append("tests")  # needed for github actions to find the template module
from conftest import db
from astrodbkit2.astrodb import or_



def test_n_radial_velocities(db):
    # check the number of radial velocities in the table
    t = (
        db.query(db.RadialVelocities.c.radial_velocity_km_s, )
        .astropy()
    )

    assert len(t) == 3, f"{len(t)} Sources failed n_radial velocity check"