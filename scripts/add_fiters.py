import requests
from io import BytesIO
import logging
import sqlalchemy.exc
import astropy.units as u
from astropy.io.votable import parse
from astrodb_scripts import load_astrodb, ingest_instrument, ingest_publication
from astrodb_scripts import check_internet_connection as internet_connection
from schema.schema_template import *

from astrodb_scripts import AstroDBError

logger = logging.getLogger("AstroDB")
logger.setLevel(logging.DEBUG)

SAVE_DB = True
RECREATE_DB = True

db = load_astrodb("astrodb-template.sqlite", recreatedb=RECREATE_DB)

ingest_publication(db, bibcode="2003AJ....126.1090C")
ingest_publication(db, bibcode="2003tmc..book.....C")
ingest_publication(db, bibcode="2010AJ....140.1868W")
ingest_publication(db, bibcode="2016A&A...595A...1G", publication="Gaia")
ingest_publication(db, bibcode="2023A&A...674A...1G")

ingest_instrument(db, telescope="2MASS", instrument="2MASS", mode="Imaging")
with db.engine.connect() as conn:
    conn.execute(
        db.Telescopes.update()
        .where(db.Telescopes.c.telescope == "2MASS")
        .values(reference="Cutr03", description="The Two Micron All Sky Survey")
    )

    conn.execute(
        db.Instruments.update()
        .where(db.Instruments.c.instrument == "2MASS")
        .values(reference="Cohe03")
    )
    conn.commit()

ingest_instrument(db, telescope="Gaia", instrument="Gaia3", mode="Imaging")
with db.engine.connect() as conn:
    conn.execute(
        db.Telescopes.update()
        .where(db.Telescopes.c.telescope == "Gaia")
        .values(description="Gaia")
    )
    conn.execute(
        db.Instruments.update()
        .where(db.Instruments.c.instrument == "Gaia3")
        .values(reference="Gaia23")
    )
    conn.commit()
ingest_instrument(db, telescope="SLOAN", instrument="SDSS", mode="Imaging")
with db.engine.connect() as conn:
    conn.execute(
        db.Telescopes.update()
        .where(db.Telescopes.c.telescope == "SLOAN")
        .values(description="The Sloan Digital Sky Survey")
    )
    conn.commit()

ingest_instrument(db, telescope="WISE", instrument="WISE", mode="Imaging")
with db.engine.connect() as conn:
    conn.execute(
        db.Telescopes.update()
        .where(db.Telescopes.c.telescope == "WISE")
        .values(reference="Wrig10", description="Wide-field Infrared Survey Explorer")
    )
    conn.commit()

ingest_instrument(db, telescope="Generic", instrument="Johnson", mode="Imaging")
with db.engine.connect() as conn:
    conn.execute(
        db.Telescopes.update()
        .where(db.Telescopes.c.telescope == "Generic")
        .values(description="Generic telescope")
    )
    conn.commit()
ingest_instrument(db, telescope="Generic", instrument="Cousins", mode="Imaging")

ingest_photometry_filter(db, filter_name="J", telescope="2MASS", instrument="2MASS")
ingest_photometry_filter(db, filter_name="H", telescope="2MASS", instrument="2MASS")
ingest_photometry_filter(db, filter_name="Ks", telescope="2MASS", instrument="2MASS")

ingest_photometry_filter(db, filter_name="G", telescope="Gaia", instrument="Gaia3")
ingest_photometry_filter(db, filter_name="Gbp", telescope="Gaia", instrument="Gaia3")
ingest_photometry_filter(db, filter_name="Grp", telescope="Gaia", instrument="Gaia3")

ingest_photometry_filter(db, filter_name="u", telescope="SLOAN", instrument="SDSS")
ingest_photometry_filter(db, filter_name="g", telescope="SLOAN", instrument="SDSS")
ingest_photometry_filter(db, filter_name="r", telescope="SLOAN", instrument="SDSS")
ingest_photometry_filter(db, filter_name="i", telescope="SLOAN", instrument="SDSS")
ingest_photometry_filter(db, filter_name="z", telescope="SLOAN", instrument="SDSS")

ingest_photometry_filter(db, filter_name="W1", telescope="WISE", instrument="WISE")
ingest_photometry_filter(db, filter_name="W2", telescope="WISE", instrument="WISE")
ingest_photometry_filter(db, filter_name="W3", telescope="WISE", instrument="WISE")
ingest_photometry_filter(db, filter_name="W4", telescope="WISE", instrument="WISE")

ingest_photometry_filter(db, filter_name="U", telescope="Generic", instrument="Johnson")
ingest_photometry_filter(db, filter_name="B", telescope="Generic", instrument="Johnson")
ingest_photometry_filter(db, filter_name="V", telescope="Generic", instrument="Johnson")
ingest_photometry_filter(db, filter_name="R", telescope="Generic", instrument="Johnson")
ingest_photometry_filter(db, filter_name="I", telescope="Generic", instrument="Johnson")
ingest_photometry_filter(db, filter_name="J", telescope="Generic", instrument="Johnson")
ingest_photometry_filter(db, filter_name="M", telescope="Generic", instrument="Johnson")

ingest_photometry_filter(db, filter_name="R", telescope="Generic", instrument="Cousins")
ingest_photometry_filter(db, filter_name="I", telescope="Generic", instrument="Cousins")

if SAVE_DB:
    db.save_database("data/")

## These scripts will eventually live in astrodb_scripts package


def ingest_photometry_filter(
    db, *, telescope=None, instrument=None, filter_name=None, ucd=None
):
    """
    Add a new photometry filter to the database
    """
    # Fetch existing telescopes, add if missing
    existing = (
        db.query(db.Telescopes).filter(db.Telescopes.c.telescope == telescope).table()
    )
    if len(existing) == 0:
        with db.engine.connect() as conn:
            conn.execute(db.Telescopes.insert().values({"telescope": telescope}))
            conn.commit()
        logger.debug(f"Added telescope {telescope}.")
    else:
        logger.debug(f"Telescope {telescope} already exists.")

    # Fetch existing instruments, add if missing
    existing = (
        db.query(db.Instruments)
        .filter(db.Instruments.c.instrument == instrument)
        .table()
    )
    if len(existing) == 0:
        with db.engine.connect() as conn:
            conn.execute(db.Instruments.insert().values({"instrument": instrument}))
            conn.commit()
        logger.debug(f"Added instrument {instrument}.")
    else:
        logger.debug(f"Instrument {instrument} already exists.")

    # Get data from SVO
    filter_id, eff_wave, fwhm, width_effective = fetch_svo(
        telescope, instrument, filter_name
    )
    logger.debug(
        f"Filter {filter_id} has effective wavelength {eff_wave} "
        "and FWHM {fwhm} and width_effective {width_effective}."
    )

    if ucd is None:
        ucd = assign_ucd(eff_wave)
    logger.debug(f"UCD for filter {filter_id} is {ucd}")

    # Add the filter
    try:
        with db.engine.connect() as conn:
            conn.execute(
                db.PhotometryFilters.insert().values(
                    {
                        "band": filter_id,
                        "ucd": ucd,
                        "effective_wavelength_angstroms": eff_wave.to(u.Angstrom).value,
                        "width_angstroms": width_effective.to(u.Angstrom).value,
                    }
                )
            )
            conn.commit()
        logger.info(
            f"Added filter {filter_id} with effective wavelength {eff_wave}, "
            f"FWHM {fwhm}, and UCD {ucd}."
        )
    except sqlalchemy.exc.IntegrityError as e:
        if "UNIQUE constraint failed:" in str(e):
            msg = str(e) + f"Filter {filter_id} already exists in the database."
            raise AstroDBError(msg)
        else:
            msg = str(e) + f"Error adding filter {filter_id}."
            raise AstroDBError(msg)
    except Exception as e:
        msg = str(e)
        raise AstroDBError(msg)


def fetch_svo(telescope: str = None, instrument: str = None, filter_name: str = None):
    """
    Fetch photometry filter information from the SVO Filter Profile Service
    http://svo2.cab.inta-csic.es/theory/fps/

    Could use better error handling when instrument name or filter name is not found

    Parameters
    ----------
    telescope: str
        Telescope name
    instrument: str
        Instrument name
    filter_name: str
        Filter name

    Returns
    -------
    filter_id: str
        Filter ID
    eff_wave: Quantity
        Effective wavelength
    fwhm: Quantity
        Full width at half maximum (FWHM)


    Raises
    ------
    AstroDBError
        If the SVO URL is not reachable or the filter information is not found
    KeyError
        If the filter information is not found in the VOTable
    """

    if internet_connection() == False:
        msg = "No internet connection. Cannot fetch photometry filter information from the SVO website."
        logger.error(msg)
        raise AstroDBError(msg)

    url = (
        f"http://svo2.cab.inta-csic.es/svo/theory/fps3/fps.php?ID="
        f"{telescope}/{instrument}.{filter_name}"
    )
    r = requests.get(url)

    if r.status_code != 200:
        msg = f"Error retrieving {url}. Status code: {r.status_code}"
        logger.error(msg)
        raise AstroDBError(msg)

    # Parse VOTable contents
    content = BytesIO(r.content)
    votable = parse(content)

    # Get Filter ID
    try:
        filter_id = votable.get_field_by_id("filterID").value
    except KeyError:
        msg = f"Filter {telescope}, {instrument}, {filter_name} not found in SVO."
        raise AstroDBError(msg)

    # Get effective wavelength and FWHM
    eff_wave = votable.get_field_by_id("WavelengthEff")
    fwhm = votable.get_field_by_id("FWHM")
    width_effective = votable.get_field_by_id("WidthEff")

    if eff_wave.unit == "AA" and fwhm.unit == "AA" and width_effective.unit == "AA":
        eff_wave = eff_wave.value * u.Angstrom
        fwhm = fwhm.value * u.Angstrom
        width_effective = width_effective.value * u.Angstrom
    else:
        msg = f"Wavelengths from SVO may not be Angstroms as expected: {eff_wave.unit}, {fwhm.unit}, {width_effective.unit}."
        raise AstroDBError(msg)

    logger.debug(
        f"Found in SVO: "
        f"Filter {filter_id} has effective wavelength {eff_wave} and "
        f"FWHM {fwhm} and width_effective {width_effective}."
    )

    return filter_id, eff_wave, fwhm, width_effective


def assign_ucd(eff_wave_quantity: u.Quantity):
    """
    Assign a Unified Content Descriptors (UCD) to a photometry filter
    based on its effective wavelength
    UCDs are from the UCD1+ controlled vocabulary
    https://www.ivoa.net/documents/UCD1+/20200212/PEN-UCDlist-1.4-20200212.html#tth_sEcB

    Parameters
    ----------
    eff_wave: Quantity
        Effective wavelength in Angstroms

    Returns
    -------
    ucd: str
        UCD string

    """
    eff_wave_quantity.to(u.Angstrom)
    eff_wave = eff_wave_quantity.value

    if 3000 < eff_wave <= 4000:
        ucd = "em.opt.U"
    elif 4000 < eff_wave <= 5000:
        ucd = "em.opt.B"
    elif 5000 < eff_wave <= 6000:
        ucd = "em.opt.V"
    elif 6000 < eff_wave <= 7500:
        ucd = "em.opt.R"
    elif 7500 < eff_wave <= 10000:
        ucd = "em.opt.I"
    elif 10000 < eff_wave <= 15000:
        ucd = "em.IR.J"
    elif 15000 < eff_wave <= 20000:
        ucd = "em.IR.H"
    elif 20000 < eff_wave <= 30000:
        ucd = "em.IR.K"
    elif 30000 < eff_wave <= 40000:
        ucd = "em.IR.3-4um"
    elif 40000 < eff_wave <= 80000:
        ucd = "em.IR.4-8um"
    elif 80000 < eff_wave <= 150000:
        ucd = "em.IR.8-15um"
    elif 150000 < eff_wave <= 300000:
        ucd = "em.IR.15-30um"
    else:
        ucd = None

    return ucd
