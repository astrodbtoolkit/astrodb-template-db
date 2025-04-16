"""
Functions to test the contents of the various Parameters tables.
As users add their own data, these tests should be modified to reflect the new data.
"""
from astropy import units as u


def test_companion_parameters(db):
    # Test that the Companion Parameters has expected number of entries
    t = db.query(db.CompanionParameters.c.source).astropy()
    n_companion_parameters = 1
    assert (
        len(t) == n_companion_parameters
    ), f"Found {len(t)} entries in the Companion Parameters table, expected {n_companion_parameters}"

    # Test units are astropy.unit resolvable
    t = (
        db.query(db.CompanionParameters)
        .filter(db.CompanionParameters.c.unit.is_not(None))
        .distinct()
        .astropy()
    )
    unit_fail = []
    for x in t:
        unit = x["unit"]
        try:
            assert u.Unit(unit, parse_strict="raise")
        except ValueError:
            print(f"{unit} is not a recognized astropy unit")
            counts = (
                db.query(db.CompanionParameters)
                .filter(db.CompanionParameters.c.unit == unit)
                .count()
            )
            unit_fail.append({unit: counts})  # count of how many of that unit there is

    assert len(unit_fail) == 0, f"Some parameter units did not resolve: {unit_fail}"


def test_modeled_parameters(db):
    # Test that ModeledParameters has expected number of entries
    t = db.query(db.ModeledParameters.c.parameter).astropy()

    n_parameters = 2
    assert len(t) == n_parameters, f"Found {len(t)} entries in the ModeledParameters table, expected {n_parameters}"

    # Test units are astropy.unit resolvable
    t = (
        db.query(db.ModeledParameters)
        .filter(db.ModeledParameters.c.unit.is_not(None))
        .distinct()
        .astropy()
    )
    unit_fail = []
    for x in t:
        unit = x["unit"]
        try:
            assert u.Unit(unit, parse_strict="raise")
        except ValueError:
            print(f"{unit} is not a recognized astropy unit")
            counts = (
                db.query(db.ModeledParameters)
                .filter(db.ModeledParameters.c.unit == unit)
                .count()
            )
            unit_fail.append({unit: counts})  # count of how many of that unit there is

    assert len(unit_fail) == 0, f"Some parameter units did not resolve: {unit_fail}"


def test_rotational_parameters(db):
    # Test that the Rotational Parameters table has expected number of entries
    t = db.query(db.RotationalParameters.c.source).astropy()
    n_rotational_parameters = 2
    assert (
        len(t) == n_rotational_parameters
    ), f"Found {len(t)} entries in the Rotational Parameters table, expected {n_rotational_parameters}"
