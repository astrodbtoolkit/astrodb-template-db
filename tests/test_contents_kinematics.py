"""
Test kinematic and astrometry data
As users add their own data, these tests should be modified to reflect the new data.
"""

from sqlalchemy import func, or_


def test_radial_velocities(db):
    # Test that Radial Velocities has expected number of entries
    t = db.query(db.RadialVelocities.c.rv_kms).astropy()

    n_radial_velocities = 1
    assert (
        len(t) == n_radial_velocities
    ), f"Found {len(t)} entries in the Radial Velocities table, expected {n_radial_velocities}"

    # Test that there is one adopted radial velocity measurement per source
    t = (
        db.query(
            db.RadialVelocities.c.source,
            func.sum(db.RadialVelocities.c.adopted).label("adopted_counts"),
        )
        .group_by(db.RadialVelocities.c.source)
        .having(func.sum(db.RadialVelocities.c.adopted) != 1)
        .astropy()
    )

    assert (
        len(t) == 0
    ), f"Found {len(t)} radial velocity measurements with incorrect 'adopted' labels"


def test_proper_motions(db):
    # Test that Radial Velocities has expected number of entries
    t = db.query(db.ProperMotions.c.pm_ra).astropy()

    n_proper_motions = 1
    assert (
        len(t) == n_proper_motions
    ), f"Found {len(t)} entries in the Proper Motions table, expected {n_proper_motions}"

    # Test that there is one adopted proper motion measurement per source
    t = (
        db.query(
            db.ProperMotions.c.source,
            func.sum(db.ProperMotions.c.adopted).label("adopted_counts"),
        )
        .group_by(db.ProperMotions.c.source)
        .having(func.sum(db.ProperMotions.c.adopted) != 1)
        .astropy()
    )

    assert (
        len(t) == 0
    ), f"Found {len(t)} proper motion measurements with incorrect 'adopted' labels"


def test_parallaxes(db):
    # Test that Parallaxes has expected number of entries
    t = db.query(db.Parallaxes.c.parallax_mas).astropy()

    n_parallaxes = 0
    assert (
        len(t) == n_parallaxes
    ), f"Found {len(t)} entries in the Parallaxes table, expected {n_parallaxes}"

    # Test that there is one adopted parallax measurement per source
    t = (
        db.query(
            db.Parallaxes.c.source,
            func.sum(db.Parallaxes.c.adopted).label("adopted_counts"),
        )
        .group_by(db.Parallaxes.c.source)
        .having(func.sum(db.Parallaxes.c.adopted) != 1)
        .astropy()
    )

    assert (
        len(t) == 0
    ), f"Found {len(t)} parallax measurements with incorrect 'adopted' labels"


def test_parallax_error(db):
    # Verify that all sources have valid parallax errors
    t = (
        db.query(db.Parallaxes.c.parallax_error)
        .filter(
            or_(
                db.Parallaxes.c.parallax_error < 0,
            )
        )
        .astropy()
    )

    if len(t) > 0:
        print(f"\n{len(t)} Parallax failed parallax error checks")
        print(t)

    assert len(t) == 0, f"{len(t)} Parallax failed parallax error checks"
