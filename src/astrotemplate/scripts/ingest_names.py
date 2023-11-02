import sqlalchemy
from ingest_utils import AstroTemplateError
import logging
logger = logging.getLogger('astrotemplate')

def ingest_names(db, source, other_name):
    '''
    This function ingests an other name into the Names table

    Parameters
    ----------
    db: astrodbkit2.astrodb.Database
        Database object created by astrodbkit2
    source: str
        Name of source as it appears in sources table

    other_name: str
        Name of the source different than that found in source table

    Returns
    -------
    None
   '''
    names_data = [{'source': source, 'other_name': other_name}]
    try:
        with db.engine.connect() as conn:
            conn.execute(db.Names.insert().values(names_data))
            conn.commit()
        logger.info(f" Name added to database: {names_data}\n")
    except sqlalchemy.exc.IntegrityError as e:
        msg = f"Could not add {names_data} to database. Name is likely a duplicate."
        logger.warning(msg)
        raise AstroTemplateError(msg + '\n' + str(e) + '\n')