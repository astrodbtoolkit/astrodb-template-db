"""
Utility functions for initializing a database, including initial table creation.

test: check that the foreign key constraints match the tables to exist
test: make sure the spectrum columns from the schema match what I read in from the CSV.
"""
from astrodbkit.astrodb import create_database, Database
from astrotemplate.schema import *
import os
import logging
logger = logging.getLogger('astrotemplate')

# maybe make this an astropy table so that we don't have to add another dependency?
import pandas as pd

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

        names = ["source", 'reference', 'spectrum','original_spectrum', 'local_spectrum', 'telescope', 'instrument',
                    'mode', 'observation_date', 'wavelength_units', 'flux_units', 'wavelength_order', 'other_references']

        # first, check whether the URL exists when read in from the CSV

        data = pd.read_csv(table_data_path,
                           names=names) # we know the table names from the schema

        for url in data.url:
            check_url_valid(url)

        for i, row in data.iterrows():
            data.loc[i, 'observation_date'] = pd.to_datetime(row.observation_date) # astropy datetime?

        # finally, add the data to the table as usual...as a dataframe
        super().initialize_table(table_data_path,  data_type='pandas')



