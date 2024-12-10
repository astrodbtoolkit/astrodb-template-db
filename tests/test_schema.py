"""
functions to test the schema itself.
"""

import pytest

from schema.schema_template import (
    Instruments,
    Names,
    Photometry,
    PhotometryFilters,
    Publications,
    Sources,
    Telescopes,
    Versions,
    Parallax,
    RadialVelocities,
    Regimes
)

DB_NAME = "test.sqlite"
DB_PATH = "data"

REFERENCE_TABLES = [
    "Publications",
    "Telescopes",
    "Instruments",
    "Modes",
    "PhotometryFilters",
    "Versions",
    "Parameters",
    "Regimes",
]


def schema_tester(table, values, error_state):
    """Helper function to handle the basic testing of the schema classes"""
    if error_state is None:
        _ = table(**values)
    else:
        with pytest.raises(error_state):
            _ = table(**values)


# -----------------------------------------------------------------------
# Schema tests
@pytest.mark.parametrize("values, error_state", [
    ({"reference": "Valid"}, None),
    ({"reference": "Valid", "doi": "LongDOI"*100}, ValueError),  # using multiplier to make a very long string
    ({"reference": "Valid", "bibcode": "LongBibCode"*100}, ValueError),
    ({"reference": "ThisIsASuperLongReferenceThatIsInvalid"}, ValueError),
    ({"telesreferencecope": None}, TypeError),  # invalid column
])
def test_publications_schema(values, error_state):
    schema_tester(Publications, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"band": "new.filter"}, None),
    ({"band": "not_a_filter"}, ValueError),
    ({"band": "new.filter", "effective_wavelength_angstroms": None}, ValueError),
    ({"band": "new.filter", "effective_wavelength_angstroms": -40}, ValueError),
])
def test_photometry_filters_schema(values, error_state):
    schema_tester(PhotometryFilters, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"source": "V4046 Sgr", "band": "2MASS.Ks", "magnitude": 7.249, "telescope": "2MASS", "reference": "Cutri03",}, None),
])
def test_photometry_schema(values, error_state):
    schema_tester(Photometry, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"telescope": "Valid"}, None),
    ({"telescope": "ThisIsASuperLongTelescopeThatIsInvalid"}, ValueError),
    ({"telescope": None}, ValueError),
])
def test_telescopes(values, error_state):
    schema_tester(Telescopes, values, error_state)

@pytest.mark.parametrize("values, error_state", [
    ({"source": "Valid"}, None),
    ({"source": "V4046 Sgr", "ra_deg": 9999, "dec_deg": -32.79, "reference": "Ref 1"}, ValueError),
    ({"source": "V4046 Sgr", "ra_deg": 273.54, "dec_deg": -9999, "reference": "Ref 1"}, ValueError),
    ({"source": "ThisIsASuperLongSourceNameThatIsInvalid"*5}, ValueError),
    ({"source": None}, ValueError),
])
def test_sources_schema(values, error_state):
    schema_tester(Sources, values, error_state)


@pytest.mark.parametrize("values, error_state", [
    ({"version": "1.0"}, None),
    ({"version": "ThisIsASuperLongVersionNameThatIsInvalid"}, ValueError),
    ({"version": None}, ValueError)
])
def test_versions_schema(values, error_state):
    schema_tester(Versions, values, error_state)


@pytest.mark.parametrize("values, error_state",
                         [
                             ({"source": "Valid", "other_name": "OtherName"}, None),
                             ({"source": "ThisIsASuperLongSourceNameThatIsInvalid"*5, "other_name": "OtherName"}, ValueError),
                             ({"source": None, "other_name":"OtherName"}, ValueError),
                             ({"source": "Source", "other_name":"ThisIsASuperLongOtherNameThatIsInvalid"*5}, ValueError),
                             ({"telescope": "Source", "other_name": None}, TypeError)  # telescope is an invalid field
                          ])
def test_names(values, error_state):
    schema_tester(Names, values, error_state)


@pytest.mark.parametrize("values, error_state",
                         [
                             ({"instrument": "Valid"}, None),
                             ({"instrument": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"instrument": None}, ValueError),
                             ({"mode": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"telescope": "ThisIsASuperLongInstrumentNameThatIsInvalid"}, ValueError),
                             ({"telescope": None}, ValueError)
                          ])
def test_instruments_schema(values, error_state):
    schema_tester(Instruments, values, error_state)

@pytest.mark.parametrize("values, error_state",
                         [
                             ({"parallax_mas": 30}, None),
                             ({"parallax_mas": -30}, None),
                             ({"parallax_mas": None}, ValueError),
                             ({"parallax_error": None}, None),
                             ({"parallax_error": 30}, None),
                             ({"parallax_error": -30}, None),
                            ({"comments": 'string i will make far too long' * 1000}, ValueError),
                            ({"comments": 'string that i will not make very long'}, None)
                          ])
def test_parallax_schema(values, error_state):
    """
    These quantities are validated in the schema. For instance, the schema ensures that
    comments must not be more than 1000 characters long.
    """
    schema_tester(Parallax, values, error_state)

@pytest.mark.parametrize("values, error_state",
                         [
                             ({"radial_velocity_km_s": 30}, None),
                             ({"radial_velocity_km_s": -30}, None),
                             ({"radial_velocity_km_s": None}, ValueError),
                             ({"radial_velocity_error_km_s": None}, None),
                             ({"radial_velocity_error_km_s": 30}, None),
                             ({"radial_velocity_error_km_s": -30}, ValueError),
                            ({"comments": 'string i will make far too long' * 1000}, ValueError),
                            ({"comments": 'string that i will not make very long'}, None)
                          ])
def test_radial_velocities_schema(values, error_state):
    """
    These quantities are validated in the schema. For instance, the schema ensures that
    comments must not be more than 1000 characters long.
    """
    schema_tester(RadialVelocities, values, error_state)


    
@pytest.mark.parametrize("values, error_state",
                         [
                             ({"regime": "good"}, None),
                            ({"regime": "ThisIsASuperLongInstrumentNameThatIsInvalid!!!!!!!"}, ValueError)
                          ])
def test_instruments_schema(values, error_state):
    """
    In the schema, there is a validation that makes sure that the length of the regime is less than 30 characters.
    """
    schema_tester(Regimes, values, error_state)


# test the ucds. they're passed to phorometry filter and should break things if they're random strings
@pytest.mark.parametrize("values, error_state",
                            [
                                ({"ucd": "em.IR.H"}, None),
                                ({"ucd": "ThisIsASuperLongUCDThatIsInvalid"}, ValueError),
                                ({"ucd": "fake.IR.H"}, ValueError)
                            ])
def test_photometryfilters_schema(values, error_state):
    schema_tester(PhotometryFilters, values, error_state)

