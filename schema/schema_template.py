"""
Schema for the AstroDB Template database.

The following tables are expected by AstroDB Toolkit and the AstroDB_scripts package:
- Sources
- Publications
- Instruments
You may modify these tables, but doing so may decrease the interoperability of your database with other tools.

"""


from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import validates
import enum
from astrodbkit2.astrodb import Base


# TODO: make "tabulardata" or "physicaldata" abstract classes.

# -------------------------------------------------------------------------------------------------------------------
# Reference tables
# -------------------------------------------------------------------------------------------------------------------
class Publications(Base):
    """ORM for publications table.
    This stores reference information (DOI, bibcodes, etc) and
    has shortname as the primary key
    """

    __tablename__ = "Publications"
    reference = Column(String(30), primary_key=True, nullable=False)
    bibcode = Column(String(100))
    doi = Column(String(100))
    description = Column(String(1000))


class Telescopes(Base):
    """
    ORM for Telescopes table.
    This stores information about the telescope, its name, and has relationship to Publications.
    """
    __tablename__ = "Telescopes"
    telescope = Column(String(30), primary_key=True, nullable=False)
    description = Column(String(1000))
    reference = Column(
        String(30), ForeignKey("Publications.reference", onupdate="cascade")
    )


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
    description = Column(String(1000))
    reference = Column(
        String(30), ForeignKey("Publications.reference", onupdate="cascade")
    )


# instead of having modes...telescope --> instrument --> mode (used mostly for spectra).
# think about SVO.


class PhotometryFilters(Base):
    """
    ORM for PhotometryFilters table.
    This stores information about the filters as well as wavelength and width
    """

    __tablename__ = "PhotometryFilters"
    band = Column(String(30), primary_key=True, nullable=False)  # of the form instrument.filter (see SVO)
    effective_wavelength = Column(Float, nullable=False)
    width = Column(Float)

    @validates("band")
    def validate_band(self, key, value):
        if "." not in value:
            raise ValueError("Band name must be of the form instrument.filter")
        return value

    @validates("effective_wavelength")
    def validate_wavelength(self, key, value):
        if value is None or value < 0:
            raise ValueError(f"Invalid effective wavelength received: {value}")
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
    description = Column(String(1000))


# -------------------------------------------------------------------------------------------------------------------
# Hard-coded enumerations


class Regime(enum.Enum):
    """Enumeration for spectral type, spectra, and photometry regimes
    Use UCD controlled vocabulary:
    https://www.ivoa.net/documents/UCD1+/20200212/PEN-UCDlist-1.4-20200212.html#tth_sEcB
    The string values are used, not the variable names.
    """

    ultraviolet = "em.UV"
    optical_UCD = "em.opt"
    optical = "optical"
    nir_UCD = "em.IR.NIR"  # Near-Infrared, 1-5 microns
    nir = "nir"
    infrared = "em.IR"  # Infrared part of the spectrum
    mir_UCD = "em.IR.MIR"  # Medium-Infrared, 5-30 microns
    mir = "mir"
    millimeter = "em.mm"
    radio = "em.radio"
    unknown = "unknown"


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
        String(30),
        ForeignKey("Publications.reference", onupdate="cascade"),
        nullable=False,
    )
    other_references = Column(String(100))
    comments = Column(String(1000))

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


class Names(Base):
    __tablename__ = "Names"
    source = Column(
        String(100),
        ForeignKey("Sources.source", ondelete="cascade", onupdate="cascade"),
        nullable=False,
        primary_key=True,
    )
    other_name = Column(String(100), primary_key=True, nullable=False)


# todo: make "tabulardata" or "physicaldata" abstract classes.


class _DataPointerTable:
    # __tablename__ = 'DataPointerTable'
    # source = Column(String(100),
    #                 nullable=False, primary_key=True)
    data = Column(String(100))
    comments = Column(String(1000))
    data_type = Column(String(32), nullable=False)
    # Other columns common to all child tables


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
    comments = Column(String(1000))
    reference = Column(String(30), ForeignKey('Publications.reference', onupdate='cascade'), primary_key=True)
