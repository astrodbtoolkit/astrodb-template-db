import sqlalchemy
import logging
logger = logging.getLogger('astrotemplate')

def ingest_instrument(db, telescope=None, instrument=None, mode=None):
    """
    Script to ingest instrumentation
    TODO: Add option to ingest references for the telescope and instruments

    Parameters
    ----------
    db: astrodbkit2.astrodb.Database
        Database object created by astrodbkit2
    telescope: str
    instrument: str
    mode: str

    Returns
    -------

    None

    """

    # Make sure enough inputs are provided
    if telescope is None and (instrument is None or mode is None):
        msg = "Telescope, Instrument, and Mode must be provided"
        logger.error(msg)
        raise SimpleError(msg)

    msg_search = f'Searching for {telescope}, {instrument}, {mode} in database'
    logger.info(msg_search)

    # Search for the inputs in the database
    telescope_db = db.query(db.Telescopes).filter(db.Telescopes.c.telescope == telescope).table()
    mode_db = db.query(db.Instruments).filter(and_(db.Instruments.c.mode == mode,
                                                    db.Instruments.c.instrument == instrument,
                                                    db.Instruments.c.telescope == telescope)).table()

    if len(telescope_db) == 1 and len(mode_db) == 1:
        msg_found = f'{telescope}, {instrument}, and {mode} are already in the database.'
        logger.info(msg_found)
        return

    # Ingest telescope entry if not already present
    if telescope is not None and len(telescope_db) == 0:
        telescope_add = [{'telescope': telescope}]
        try:
            with db.engine.connect() as conn:
                conn.execute(db.Telescopes.insert().values(telescope_add))
                conn.commit()
            msg_telescope = f'{telescope} was successfully ingested in the database'
            logger.info(msg_telescope)
        except sqlalchemy.exc.IntegrityError as e:  # pylint: disable=invalid-name
            msg = 'Telescope could not be ingested'
            logger.error(msg)
            raise SimpleError(msg + '\n' + str(e))

    # Ingest instrument+mode (requires telescope) if not already present
    if telescope is not None and instrument is not None and mode is not None and len(mode_db) == 0:
        instrument_add = [{'instrument': instrument,
                           'mode': mode,
                           'telescope': telescope}]
        try:
            with db.engine.connect() as conn:
                conn.execute(db.Instruments.insert().values(instrument_add))
                conn.commit()
            msg_instrument = f'{instrument} was successfully ingested in the database.'
            logger.info(msg_instrument)
        except sqlalchemy.exc.IntegrityError as e:  # pylint: disable=invalid-name
            msg = 'Instrument/Mode could not be ingested'
            logger.error(msg)
            raise SimpleError(msg + '\n' + str(e))

    return

