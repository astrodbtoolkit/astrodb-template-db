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

def check_string_length(value, max_length, key):
    if value is None or len(value) > max_length:
        raise ValueError(f"Provided {key} is invalid; too long or None: {value}")
    else:
        pass
    

# -------------------------------------------------------------------------------------------------------------------
# Reference tables
# -------------------------------------------------------------------------------------------------------------------
class Publications(Base):
    """ORM for publications table.
    This stores reference information (DOI, bibcodes, etc) and
    has shortname as the primary key
    """
    reference_string_length = 30
    bibcode_string_length = 100
    doi_string_length = 100
    description_string_length = 1000



    __tablename__ = "Publications"
    reference = Column(String(reference_string_length), primary_key=True, nullable=False)
    bibcode = Column(String(bibcode_string_length))
    doi = Column(String(doi_string_length))
    description = Column(String(description_string_length))

    @validates("reference")
    def validate_reference(self, key, value):
        check_string_length(value, 30, "reference")
        return value

    # @validates("bibcode")
    # def validate_bibcode(self, key, value):
    #     if value is None or len(value) > 100:
    #         raise ValueError(f"Provided bibcode is invalid; too long or None: {value}")
    #     return value

    @validates("doi", "bibcode")
    def validate_doi_and_bibcode(self, key, value):
        check_string_length(value, 100, key)
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is None or len(value) > 1000:
            raise ValueError(f"Provided description is invalid; too long or None: {value}")
        return value





class Telescopes(Base):
    """
    ORM for Telescopes table.
    This stores information about the telescope, its name, and has relationship to Publications.
    """
    telescope_string_length = 30
    description_string_length = 1000
    reference_string_length = 30

    __tablename__ = "Telescopes"
    telescope = Column(String(telescope_string_length), primary_key=True, nullable=False)
    description = Column(String(description_string_length))
    reference = Column(
        String(reference_string_length), ForeignKey("Publications.reference", onupdate="cascade")
    )

    @validates("telescope")
    def validate_telescope(self, key, value):
        if value is None or len(value) > self.telescope_string_length:
            raise ValueError(f"Provided telescope is invalid; too long or None: {value}")
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is None or len(value) > self.description_string_length:
            raise ValueError(f"Provided description is invalid; too long or None: {value}")
        return value

    @validates("reference")
    def validate_reference(self, key, value):
        if value is None or len(value) > self.reference_string_length:
            raise ValueError(f"Provided reference is invalid; too long or None: {value}")
        return value




class Instruments(Base):
    """
    ORM for Instruments table.
    This stores relationships between telescopes and Publications,
    as well as mode, instrument (name), and description.
    """
    instrument_string_length = 30
    mode_string_length = 30
    telescope_string_length = 30
    description_string_length = 1000
    reference_string_length = 30

    __tablename__ = "Instruments"
    instrument = Column(String(instrument_string_length), primary_key=True, nullable=False)
    mode = Column(String(mode_string_length), primary_key=True)
    telescope = Column(
        String(telescope_string_length),
        ForeignKey("Telescopes.telescope", onupdate="cascade"),
        primary_key=True,
    )
    description = Column(String(description_string_length))
    reference = Column(
        String(reference_string_length), ForeignKey("Publications.reference", onupdate="cascade")
    )

    @validates("instrument")
    def validate_instrument(self, key, value):
        if value is None or len(value) > self.instrument_string_length:
            raise ValueError(f"Provided instrument is invalid; too long or None: {value}")
        return value

    @validates("mode")
    def validate_mode(self, key, value):
        if value is None or len(value) > self.mode_string_length:
            raise ValueError(f"Provided mode is invalid; too long or None: {value}")
        return value

    @validates("telescope")
    def validate_telescope(self, key, value):
        if value is None or len(value) > self.telescope_string_length:
            raise ValueError(f"Provided telescope is invalid; too long or None: {value}")
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is None or len(value) > self.description_string_length:
            raise ValueError(f"Provided description is invalid; too long or None: {value}")
        return value

    @validates("reference")
    def validate_reference(self, key, value):
        if value is None or len(value) > self.reference_string_length:
            raise ValueError(f"Provided reference is invalid; too long or None: {value}")
        return value




# instead of having modes...telescope --> instrument --> mode (used mostly for spectra).
# think about SVO.


class PhotometryFilters(Base):
    """
    ORM for PhotometryFilters table.
    This stores information about the filters as well as wavelength and width
    """
    band_string_length = 30
    ucd_string_length = 100

    __tablename__ = "PhotometryFilters"
    band = Column(String(band_string_length), primary_key=True, nullable=False)
    ucd = Column(String(ucd_string_length))
    effective_wavelength_angstroms = Column(Float, nullable=False)
    width_angstroms = Column(Float)

    @validates("band")
    def validate_band(self, key, value):
        if "." not in value:
            raise ValueError("Band name must be of the form instrument.filter")
        return value

    @validates("effective_wavelength_angstroms")
    def validate_wavelength(self, key, value):
        if value is None or value < 0:
            raise ValueError(f"Invalid effective wavelength received: {value}")
        return value

    @validates("width_angstroms")
    def validate_width(self, key, value):
        if value is None or value < 0:
            raise ValueError(f"Invalid width received: {value}")
        return value

    @validates("ucd")
    def validate_ucd(self, key, value):
        if value is None or len(value) > self.ucd_string_length:
            raise ValueError(f"Provided UCD is invalid; too long or None: {value}")
        return value


class Versions(Base):
    """
    ORM for Versions table
    This stores the version numbers for the database
    """
    version_string_length = 30
    start_date_string_length = 30
    end_date_string_length = 30
    description_string_length = 1000

    __tablename__ = "Versions"
    version = Column(String(version_string_length), primary_key=True, nullable=False)
    start_date = Column(String(start_date_string_length))
    end_date = Column(String(end_date_string_length))
    description = Column(String(description_string_length))

    @validates("version")
    def validate_version(self, key, value):
        if value is None or len(value) > self.version_string_length:
            raise ValueError(f"Provided version is invalid; too long or None: {value}")
        return value

    @validates("start_date")
    def validate_start_date(self, key, value):
        if value is None or len(value) > self.start_date_string_length:
            raise ValueError(f"Provided start_date is invalid; too long or None: {value}")
        return value

    @validates("end_date")
    def validate_end_date(self, key, value):
        if value is None or len(value) > self.end_date_string_length:
            raise ValueError(f"Provided end_date is invalid; too long or None: {value}")
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is None or len(value) > self.description_string_length:
            raise ValueError(f"Provided description is invalid; too long or None: {value}")
        return value


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
    source_string_length = 100
    equinox_string_length = 10
    shortname_string_length = 30
    reference_string_length = 30
    other_references_string_length = 100
    comments_string_length = 1000

    source = Column(String(source_string_length), primary_key=True, nullable=False)
    ra_deg = Column(Float)
    dec_deg = Column(Float)
    epoch_year = Column(Float)  # decimal year
    equinox = Column(String(equinox_string_length))  # eg, J2000
    shortname = Column(String(shortname_string_length))  # not needed?
    reference = Column(
        String(reference_string_length),
        ForeignKey("Publications.reference", onupdate="cascade"),
        nullable=False,
    )
    other_references = Column(String(other_references_string_length))
    comments = Column(String(comments_string_length))

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

    @validates("source")
    def validate_source(self, key, value):
        if value is None or len(value) > self.source_string_length:
            raise ValueError(f"Provided source is invalid; too long or None: {value}")
        return value

    @validates("equinox")
    def validate_equinox(self, key, value):
        if value is None or len(value) > self.equinox_string_length:
            raise ValueError(f"Provided equinox is invalid; too long or None: {value}")
        return value

    @validates("shortname")
    def validate_shortname(self, key, value):
        if value is None or len(value) > self.shortname_string_length:
            raise ValueError(f"Provided shortname is invalid; too long or None: {value}")
        return value

    @validates("reference")
    def validate_reference(self, key, value):
        if value is None or len(value) > self.reference_string_length:
            raise ValueError(f"Provided reference is invalid; too long or None: {value}")
        return value

    @validates("other_references")
    def validate_other_references(self, key, value):
        if value is None or len(value) > self.other_references_string_length:
            raise ValueError(f"Provided other_references is invalid; too long or None: {value}")
        return value

    @validates("comments")
    def validate_comments(self, key, value):
        if value is None or len(value) > self.comments_string_length:
            raise ValueError(f"Provided comments is invalid; too long or None: {value}")
        return value




class Names(Base):

    source_string_length = 100
    other_name_string_length = 100
    __tablename__ = "Names"
    source = Column(
        String(100),
        ForeignKey("Sources.source", ondelete="cascade", onupdate="cascade"),
        nullable=False,
        primary_key=True,
    )
    other_name = Column(String(100), primary_key=True, nullable=False)

    @validates("source")
    def validate_source(self, key, value):
        if value is None or len(value) > self.source_string_length:
            raise ValueError(f"Provided source is invalid; too long or None: {value}")
        return value

    @validates("other_name")
    def validate_other_name(self, key, value):
        if value is None or len(value) > self.other_name_string_length:
            raise ValueError(f"Provided other_name is invalid; too long or None: {value}")
        return value


# todo: make "tabulardata" or "physicaldata" abstract classes.


class _DataPointerTable:
    # __tablename__ = 'DataPointerTable'
    # source = Column(String(100),
    #                 nullable=False, primary_key=True)

    data_string_length = 100
    comments_string_length = 1000
    data_type_string_length = 32

    data = Column(String(data_string_length))
    comments = Column(String(comments_string_length))
    data_type = Column(String(data_type_string_length), nullable=False)
    # Other columns common to all child tables

    @validates("data")
    def validate_data(self, key, value):
        if len(value) > self.data_string_length:
            raise ValueError(f"Provided data is invalid; too long or None: {value}")
        return value

    @validates("comments")
    def validate_comments(self, key, value):
        if len(value) > self.comments_string_length:
            raise ValueError(f"Provided comments is invalid; too long or None: {value}")
        return value

    @validates("data_type")
    def validate_data_type(self, key, value):
        if value is None or len(value) > self.data_type_string_length:
            raise ValueError(f"Provided data_type is invalid; too long or None: {value}")
        return value


class Photometry(Base):
    # Table to store photometry information

    source_string_length = 100
    band_string_length = 30
    telescope_string_length = 30
    comments_string_length = 1000
    reference_string_length = 30

    __tablename__ = 'Photometry'

    source = Column(String(source_string_length), ForeignKey('Sources.source', ondelete='cascade', onupdate='cascade'),
                    nullable=False, primary_key=True)
    band = Column(String(band_string_length), ForeignKey('PhotometryFilters.band'), primary_key=True)
    magnitude = Column(Float, nullable=False)
    magnitude_error = Column(Float)
    telescope = Column(String(telescope_string_length), ForeignKey('Telescopes.telescope'))
    epoch = Column(Float)  # decimal year
    comments = Column(String(comments_string_length))
    reference = Column(String(reference_string_length), ForeignKey('Publications.reference', onupdate='cascade'), primary_key=True)


    @validates("source")
    def validate_source(self, key, value):
        if value is None or len(value) > self.source_string_length:
            raise ValueError(f"Provided source is invalid; too long or None: {value}")
        return value

    @validates("band")
    def validate_band(self, key, value):
        if len(value) > self.band_string_length:
            raise ValueError(f"Provided band is invalid; too long: {value}")
        return value

    @validates("magnitude")
    def validate_magnitude(self, key, value):
        if value is None:
            raise ValueError(f"Provided magnitude is invalid; None: {value}")
        return value

    @validates("magnitude_error")
    def validate_magnitude_error(self, key, value):
        if value is None:
            raise ValueError(f"Provided magnitude_error is invalid; None: {value}")
        return value

    @validates("telescope")
    def validate_telescope(self, key, value):
        if value is None or len(value) > self.telescope_string_length:
            raise ValueError(f"Provided telescope is invalid; too long or None: {value}")
        return value

    @validates("epoch")
    def validate_epoch(self, key, value):
        if value is None:
            raise ValueError(f"Provided epoch is invalid; None: {value}")
        return value

    @validates("comments")
    def validate_comments(self, key, value):
        if value is None or len(value) > self.comments_string_length:
            raise ValueError(f"Provided comments is invalid; too long or None: {value}")
        return value

    @validates("reference")
    def validate_reference(self, key, value):
        if value is None or len(value) > self.reference_string_length:
            raise ValueError(f"Provided reference is invalid; too long or None: {value}")
        return value


