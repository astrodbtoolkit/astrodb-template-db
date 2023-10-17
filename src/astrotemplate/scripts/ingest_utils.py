"""
Ingest utility functions, drawn from the SIMPLE-db ingest script

todo: consider whether we want to do this from a CSV, as well.
"""
import logging
import sys
import socket
from initialize_utils import *
import requests
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord

logger = logging.getLogger('astrotemplate')

# Logger setup
# This will stream all logger messages to the standard output and apply formatting for that
logger.propagate = False  # prevents duplicated logging messages
LOGFORMAT = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
ch = logging.StreamHandler(stream=sys.stdout)
ch.setFormatter(LOGFORMAT)
# To prevent duplicate handlers, only add if they haven't been set previously
if not len(logger.handlers):
    logger.addHandler(ch)
logger.setLevel(logging.INFO)



def check_internet_connection():
    # get current IP address of  system
    ipaddress = socket.gethostbyname(socket.gethostname())

    # checking system IP is the same as "127.0.0.1" or not.
    if ipaddress == "127.0.0.1": # no internet
        return False, ipaddress
    else:
        return True, ipaddress

def check_url_valid(url):
    """
    Check that the URLs in the spectra table are valid.

    :return:
    """

    request_response = requests.head(url)
    status_code = request_response.status_code  # The website is up if the status code is 200
    if status_code != 200:
        status = 'skipped' # instead of incrememnting n_skipped, just skip this one
        msg = "The spectrum location does not appear to be valid: \n" \
              f'spectrum: {url} \n' \
              f'status code: {status_code}'
        logger.error(msg)
    else:
        msg = f"The spectrum location appears up: {url}"
        logger.debug(msg)
        status = 'added'
    return status

def find_source_in_db(db, source, ra=None, dec=None, search_radius=60.):
    """
    Find a source in the database given a source name and optional coordinates.

    Parameters
    ----------
    db
    source: str
        Source name
    ra: float
        Right ascensions of sources. Decimal degrees.
    dec: float
        Declinations of sources. Decimal degrees.
    search_radius
        radius in arcseconds to use for source matching

    Returns
    -------
    List of strings.

    one match: Single element list with one database source name
    multiple matches: List of possible database names
    no matches: Empty list

    """

    # TODO: In astrodbkit2, convert verbose to using logger

    if ra and dec:
        coords = True
    else:
        coords = False

    source = source.strip()

    logger.debug(f'{source}: Searching for match in database.')

    db_name_matches = db.search_object(source, output_table='Sources', fuzzy_search=False, verbose=False)

    # NO MATCHES
    # If no matches, try fuzzy search
    if len(db_name_matches) == 0:
        logger.debug(f"{source}: No name matches, trying fuzzy search")
        db_name_matches = db.search_object(source, output_table='Sources', fuzzy_search=True, verbose=False)

    # If still no matches, try to resolve the name with Simbad
    if len(db_name_matches) == 0:
        logger.debug(f"{source}: No name matches, trying Simbad search")
        db_name_matches = db.search_object(source, resolve_simbad=True, fuzzy_search=False, verbose=False)

    # if still no matches, try spatial search using coordinates, if provided
    if len(db_name_matches) == 0 and coords:
        location = SkyCoord(ra, dec, frame='icrs', unit='deg')
        radius = u.Quantity(search_radius, unit='arcsec')
        logger.info(f"{source}: No Simbad match, trying coord search around {location.ra.degree}, {location.dec}")
        db_name_matches = db.query_region(location, radius=radius)

    # If still no matches, try to get the coords from SIMBAD
    if len(db_name_matches) == 0:
        simbad_result_table = Simbad.query_object(source)
        if simbad_result_table is not None and len(simbad_result_table) == 1:
            simbad_coords = simbad_result_table['RA'][0] + ' ' + simbad_result_table['DEC'][0]
            simbad_skycoord = SkyCoord(simbad_coords, unit=(u.hourangle, u.deg))
            ra = simbad_skycoord.to_string(style='decimal').split()[0]
            dec = simbad_skycoord.to_string(style='decimal').split()[1]
            msg = f"Coordinates retrieved from SIMBAD {ra}, {dec}"
            logger.debug(msg)
            # Search database around that coordinate
            radius = u.Quantity(search_radius, unit='arcsec')
            db_name_matches = db.query_region(simbad_skycoord, radius=radius)

    if len(db_name_matches) == 1:
        db_names = db_name_matches['source'].tolist()
        logger.debug(f'One match found for {source}: {db_names[0]}')
    elif len(db_name_matches) > 1:
        db_names = db_name_matches['source'].tolist()
        logger.debug(f'More than match found for {source}: {db_names}')
        # TODO: Find way for user to choose correct match
    elif len(db_name_matches) == 0:
        db_names = []
        logger.debug(f' {source}: No match found')
    else:
        raise SimpleError(f'Unexpected condition searching for {source}')

    return db_names


