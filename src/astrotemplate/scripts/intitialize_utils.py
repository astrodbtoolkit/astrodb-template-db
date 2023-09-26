"""
Utility functions for initializing a database, including initial table creation.

test: check that the foreign key constraints match the tables to exist
"""
from astrodbkit2.astrodb import create_database, Database
from astrotemplate.schema import *
import os
import logging
import sys
import socket
import requests
logger = logging.getLogger('astrotemplate')

# maybe make this an astropy table so that we don't have to add another dependency?
import pandas as pd

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
    internet = check_internet_connection()
    if internet:
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
    else:
        msg = "No internet connection. Internet is needed to check spectrum files."
        raise ValueError(msg)

class TableNotInitialized(Exception):
    """
    Exception raised when a table is not initialized.
    """
    pass

# find the location of the current file in the user's filesystem
abs_path = os.path.dirname(__file__)


class TableInitializer(object):
    tables_to_exist = []

    def __init__(self):
        self._create_db()

    def _create_db(self):
        """
        Create the database.
        :return:
        """
        connection_string = 'sqlite:///astrotemplate.db'  # connection string for a SQLite database named SIMPLE.db
        create_database(connection_string)
        self.db = Database(connection_string)


    def check_tables_exist(self):
        """
        Check that the tables exist in the database.

        Inputs
        ------
        db: Database
            Database object
        tables_to_exist: list
            List of tables that should exist in the database

        :return:
        """
        for table in self.tables_to_exist:
            if not self.db.table_exists(table):
                raise TableNotInitialized(f"{table} table must be initialized first.")

    def initialize_table(self, table_data, data_type='csv'):
        """
        Initialize the Sources table. this must be created first.

        Inputs
        ------
        table_data: str or dictionary
            Path to the sources table csv file. todo: not just take in a CSV?
        data_type: str
            Type of data to be added to the table. Options are 'csv' or 'pandas'

        :return:
        """
        self.check_tables_exist()
        if data_type == 'csv':
            if type(table_data) != str:
                raise ValueError("table_data must be a string when data_type is 'csv'")


        elif data_type == 'pandas':
            if type(table_data) != pd.DataFrame:
                raise ValueError("table_data must be a DataFrame when data_type is 'pandas'")

        self.db.add_table_data(table_data, table=self.table_name, fmt=data_type)
        self.db.save_database(abs_path + '/data')



class PublicationsTableInitializer(TableInitializer):
    table_name = 'Publications'

class SourceTableInitializer(TableInitializer):
    table_name = 'Sources'
    tables_to_exist = ['Publications']

class NamesTableInitializer(TableInitializer):
    table_name = 'Names'
    tables_to_exist = ['Sources']

class ModesTableInitializer(TableInitializer):
    table_name = 'Modes'
    tables_to_exist = ['Instruments', 'Telescopes']

class RegimesTableInitializer(TableInitializer):
    table_name = 'Regimes'

class PhotometryFiltersTableInitializer(TableInitializer):
    table_name = 'PhotometryFilters'
    tables_to_exist = ['Instruments', 'Telescopes']

class InstrumentsTableInitializer(TableInitializer):
    table_name = 'Instruments'
    tables_to_exist = ['Publications']

class TelescopesTableInitializer(TableInitializer):
    table_name = 'Telescopes'
    tables_to_exist = ['Publications']

class SpectraTableInitializer(TableInitializer):
    table_name = 'Spectra'
    tables_to_exist = ['Sources', 'Publications', 'Instruments', 'Telescopes']

    def initialize_table(self, table_data_path):

        # first, check whether the URL exists when read in from the CSV
        # todo:, get the URL?

        check_url_valid(url)
        # todo: second, cast the date times as correct
        # finally, add the data to the table as usual...as a dictionary
        super().initialize_table(table_data_path)



