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
