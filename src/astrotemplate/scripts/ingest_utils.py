"""
Ingest utility functions, drawn from the SIMPLE-db ingest script

todo: consider whether we want to do this from a CSV, as well.
"""
import logging
import sys
import socket
from initialize_utils import *

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


