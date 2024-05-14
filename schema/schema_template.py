"""
Schema for the AstroDB Template database.

The following tables are expected by AstroDB Toolkit and the AstroDB_scripts package:
- Sources
- Publications
- Instruments
You may modify these tables, but doing so may decrease the interoperability of your database with other tools.

"""

import enum

from astrodbkit2.astrodb import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import validates

# Globals
REFERENCE_STRING_LENGTH = 30
DESCRIPTION_STRING_LENGTH = 1000

# TODO: make "tabulardata" or "physicaldata" abstract classes.

def check_string_length(value, max_length, key):
    if value is None or len(value) > max_length:
        raise ValueError(f"Provided {key} is invalid; too long or None: {value}")
    else:
        pass
    

# -------------------------------------------------------------------------------------------------------------------
# Reference tables
# -------------------------------------------------------------------------------------------------------------------
REFERENCE_TABLES = [
    "Publications",
    "Telescopes",
    "Instruments",
    "PhotometryFilters",
    "Versions",
    "Regimes"
]


class Publications(Base):
    """ORM for publications table.
    This stores reference information (DOI, bibcodes, etc) and
    has shortname as the primary key
    """

    __tablename__ = "Publications"
    reference = Column(String(REFERENCE_STRING_LENGTH), primary_key=True, nullable=False)
    bibcode = Column(String(100))
    doi = Column(String(100))
    description = Column(String(DESCRIPTION_STRING_LENGTH))

    @validates("reference")
    def validate_reference(self, key, value):
        check_string_length(value, REFERENCE_STRING_LENGTH, "reference")
        return value

    @validates("doi", "bibcode")
    def validate_doi_and_bibcode(self, key, value):
        check_string_length(value, 100, key)
        return value

    @validates("description")
    def validate_description(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value


class Telescopes(Base):
    """
    ORM for Telescopes table.
    This stores information about the telescope, its name, and has relationship to Publications.
    """

    __tablename__ = "Telescopes"
    telescope = Column(String(30), primary_key=True, nullable=False)
    description = Column(String(DESCRIPTION_STRING_LENGTH))
    reference = Column(
        String(REFERENCE_STRING_LENGTH), ForeignKey("Publications.reference", onupdate="cascade")
    )

    @validates("telescope")
    def validate_telescope(self, key, value):
        check_string_length(value, 30, key)
        return value

    @validates("description")
    def validate_description(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value


class Instruments(Base):
    """
    ORM for Instruments table.
    This stores relationships between telescopes and Publications,
    as well as mode, instrument (name), and description.
    """

    __tablename__ = "Instruments"
    instrument = Column(String(30), primary_key=True, nullable=False)
    mode = Column(String(30), primary_key=True)
    telescope = Column(
        String(30),
        ForeignKey("Telescopes.telescope", onupdate="cascade"),
        primary_key=True,
    )
    description = Column(String(DESCRIPTION_STRING_LENGTH))
    reference = Column(
        String(REFERENCE_STRING_LENGTH), ForeignKey("Publications.reference", onupdate="cascade")
    )

    @validates("instrument", "mode", "telescope")
    def validate_instrument(self, key, value):
        check_string_length(value, 30, key)
        return value

    @validates("description")
    def validate_description(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value


# instead of having modes...telescope --> instrument --> mode (used mostly for spectra).
# think about SVO.


class PhotometryFilters(Base):
    """
    ORM for PhotometryFilters table.
    This stores information about the filters as well as wavelength and width
    """

    __tablename__ = "PhotometryFilters"
    band = Column(String(30), primary_key=True, nullable=False)
    ucd = Column(String(100))
    effective_wavelength_angstroms = Column(Float, nullable=False)
    width_angstroms = Column(Float)

    @validates("band")
    def validate_band(self, key, value):
        if "." not in value:
            raise ValueError("Band name must be of the form instrument.filter")
        return value

    @validates("effective_wavelength_angstroms", "width_angstroms")
    def validate_wavelength(self, key, value):
        if value is None or value < 0:
            raise ValueError(f"Invalid {key} received: {value}")
        return value

    @validates("ucd")
    def validate_ucd(self, key, value):
        check_string_length(value, 100, key)
        return value


class Versions(Base):
    """
    ORM for Versions table
    This stores the version numbers for the database
    """

    __tablename__ = "Versions"
    version = Column(String(30), primary_key=True, nullable=False)
    start_date = Column(String(30))
    end_date = Column(String(30))
    description = Column(String(DESCRIPTION_STRING_LENGTH))

    @validates("version", "start_date", "end_date")
    def validate_version(self, key, value):
        check_string_length(value, 30, key)
        return value

    @validates("description")
    def validate_description(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value


# -------------------------------------------------------------------------------------------------------------------
# Hard-coded enumerations
class Regimes(Base):
    """Enumeration for spectral type, spectra, and photometry regimes
    Use UCD controlled vocabulary:
    https://www.ivoa.net/documents/UCD1+/20200212/PEN-UCDlist-1.4-20200212.html#tth_sEcB
    The string values are used, not the variable names.
    """
    __tablename__ = "Regimes"
    # todo: validate that it's a valid UCD regime.

    regime = Column(String(REFERENCE_STRING_LENGTH), primary_key=True, nullable=False)


# -------------------------------------------------------------------------------------------------------------------
# Main tables
class Sources(Base):
    """ORM for the sources table.
    This stores the main identifiers for our objects along with ra and dec"""
    __tablename__ = "Sources"

    source = Column(String(100), primary_key=True, nullable=False)
    ra_deg = Column(Float)
    dec_deg = Column(Float)
    epoch_year = Column(Float)  # decimal year
    equinox = Column(String(10))  # eg, J2000
    shortname = Column(String(30))  # not needed?
    reference = Column(
        String(REFERENCE_STRING_LENGTH),
        ForeignKey("Publications.reference", onupdate="cascade"),
        nullable=False,
    )
    other_references = Column(String(100))
    comments = Column(String(DESCRIPTION_STRING_LENGTH))

    @validates("ra_deg")
    def validate_ra(self, key, value):
        if value > 360 or value < 0:
            raise ValueError("RA not in allowed range (0..360)")
        return value

    @validates("dec_deg")
    def validate_dec(self, key, value):
        if value > 90 or value < -90:
            raise ValueError("Dec not in allowed range (-90..90)")
        return value

    @validates("source", "other_references")
    def validate_source(self, key, value):
        check_string_length(value, 100, key)
        return value

    @validates("equinox")
    def validate_equinox(self, key, value):
        check_string_length(value, 10, key)
        return value

    @validates("shortname")
    def validate_shortname(self, key, value):
        check_string_length(value, 30, key)
        return value

    @validates("comments")
    def validate_comments(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value


class Names(Base):
    """Names table"""

    __tablename__ = "Names"
    source = Column(
        String(100),
        ForeignKey("Sources.source", ondelete="cascade", onupdate="cascade"),
        nullable=False,
        primary_key=True,
    )
    other_name = Column(String(100), primary_key=True, nullable=False)

    @validates("source", "other_name")
    def validate_source(self, key, value):
        check_string_length(value, 100, key)
        return value

# todo: make "tabulardata" or "physicaldata" abstract classes.


class _DataPointerTable:
    # __tablename__ = 'DataPointerTable'
    # source = Column(String(100),
    #                 nullable=False, primary_key=True)

    data = Column(String(100))
    comments = Column(String(DESCRIPTION_STRING_LENGTH))
    data_type = Column(String(32), nullable=False)
    # Other columns common to all child tables

    @validates("data")
    def validate_data(self, key, value):
        check_string_length(value, 100, key)
        return value

    @validates("comments")
    def validate_comments(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value

    @validates("data_type")
    def validate_data_type(self, key, value):
        check_string_length(value, 32, key)
        return value


class Photometry(Base):
    # Table to store photometry information
    __tablename__ = 'Photometry'

    source = Column(String(100), ForeignKey('Sources.source', ondelete='cascade', onupdate='cascade'),
                    nullable=False, primary_key=True)
    band = Column(String(30), ForeignKey('PhotometryFilters.band'), primary_key=True)
    magnitude = Column(Float, nullable=False)
    magnitude_error = Column(Float)
    telescope = Column(String(30), ForeignKey('Telescopes.telescope'))
    epoch = Column(Float)  # decimal year
    comments = Column(String(DESCRIPTION_STRING_LENGTH))
    reference = Column(String(REFERENCE_STRING_LENGTH), ForeignKey('Publications.reference', onupdate='cascade'), primary_key=True)
    regime = Column(
        String(REFERENCE_STRING_LENGTH),
        ForeignKey("Regimes.regime", onupdate="cascade"),
        nullable=False,
    )

    @validates("band")
    def validate_band(self, key, value):
        check_string_length(value, 30, key)
        return value

    @validates("magnitude", "magnitude_error", "epoch")
    def validate_magnitude(self, key, value):
        if value is None:
            raise ValueError(f"Provided {key} is invalid; None: {value}")
        return value

    @validates("telescope")
    def validate_telescope(self, key, value):
        check_string_length(value, 30, key)
        return value

    @validates("comments")
    def validate_comments(self, key, value):
        check_string_length(value, DESCRIPTION_STRING_LENGTH, key)
        return value


