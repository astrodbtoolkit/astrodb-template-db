"""
Utility functions for initializing a database, including initial table creation.
"""
from astrodbkit2.astrodb import create_database, Database
from astrotemplate.schema import *
import os

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
        self.create_db()

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

    def initialize_table(self, table_data_path):
        """
        Initialize the Sources table. this must be created first.

        Inputs
        ------
        table_data_path: str
            Path to the sources table csv file. todo: not just take in a CSV?

        :return:
        """
        self.check_tables_exist()
        self.db.add_table_data(table_data_path, table=self.table_name, fmt='csv')
        self.db.save_database(abs_path + '/data')

def SourceTableInitializer(TableInitializer):
    table_name = 'Sources'
    def __init__(self):
        super().__init__()

def PublicationsTableInitializer(TableInitializer):
    table_name = 'Publications'
    def __init__(self):
        super().__init__()

def InstrumentsTableInitializer(TableInitializer):
    table_name = 'Instruments'
    def __init__(self):
        super().__init__()

def TelescopesTableInitializer(TableInitializer):
    table_name = 'Telescopes'
    def __init__(self):
        super().__init__()

def SpectraTableInitializer(TableInitializer):
    table_name = 'Spectra'
    tables_to_exist = ['Sources', 'Publications', 'Instruments', 'Telescopes']
    def __init__(self):
        super().__init__()


