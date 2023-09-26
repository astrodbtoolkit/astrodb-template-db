"""
Ingest utility functions, drawn from the SIMPLE-db ingest script

todo: consider whether we want to do this from a CSV, as well.
"""
import logging
import sys
import socket

def check_internet_connection():
    # get current IP address of  system
    ipaddress = socket.gethostbyname(socket.gethostname())

    # checking system IP is the same as "127.0.0.1" or not.
    if ipaddress == "127.0.0.1": # no internet
        return False, ipaddress
    else:
        return True, ipaddress


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
        raise SimpleError(msg + '\n' + str(e) + '\n')

# SOURCES
def ingest_sources(db, sources, references=None, ras=None, decs=None, comments=None, epochs=None,
                   equinoxes=None, other_references=None, raise_error=True, search_db=True):
    """
    Script to ingest sources
    TODO: better support references=None
    Parameters
    ----------
    db: astrodbkit2.astrodb.Database
        Database object created by astrodbkit2
    sources: list[str]
        Names of sources
    references: str or list[strings]
        Discovery references of sources
    ras: list[floats], optional
        Right ascensions of sources. Decimal degrees.
    decs: list[floats], optional
        Declinations of sources. Decimal degrees.
    comments: list[strings], optional
        Comments
    epochs: str or list[str], optional
        Epochs of coordinates
    equinoxes: str or list[string], optional
        Equinoxes of coordinates
    other_references: str or list[strings]
    raise_error: bool, optional
        True (default): Raise an error if a source cannot be ingested
        False: Log a warning but skip sources which cannot be ingested
    search_db: bool, optional
        True (default): Search database to see if source is already ingested
        False: Ingest source without searching the database

    Returns
    -------

    None

    """
    # TODO: add example

    # SETUP INPUTS
    if ras is None and decs is None:
        coords = False
    else:
        coords = True

    if isinstance(sources, str):
        n_sources = 1
    else:
        n_sources = len(sources)

    # Convert single element input values into lists
    input_values = [sources, references, ras, decs, epochs, equinoxes, comments, other_references]
    for i, input_value in enumerate(input_values):
        if input_value is None:
            input_values[i] = [None] * n_sources
        elif isinstance(input_value, (str, float)):
            input_values[i] = [input_value] * n_sources
    sources, references, ras, decs, epochs, equinoxes, comments, other_references = input_values

    n_added = 0
    n_existing = 0
    n_names = 0
    n_alt_names = 0
    n_skipped = 0
    n_multiples = 0

    if n_sources > 1:
        logger.info(f"Trying to add {n_sources} sources")

    # Loop over each source and decide to ingest, skip, or add alt name
    for i, source in enumerate(sources):
        # Find out if source is already in database or not
        if coords and search_db:
            name_matches = find_source_in_db(db, source, ra=ras[i], dec=decs[i])
        elif search_db:
            name_matches = find_source_in_db(db, source)
        elif not search_db:
            name_matches = []
        else:
            name_matches = None
            ra = None
            dec = None

        if len(name_matches) == 1 and search_db:  # Source is already in database
            n_existing += 1
            msg1 = f"{i}: Skipping {source}. Already in database as {name_matches[0]}. \n "
            logger.debug(msg1)

            # Figure out if ingest name is an alternate name and add
            db_matches = db.search_object(source, output_table='Sources', fuzzy_search=False)
            if len(db_matches) == 0:
                #add other name to names table
                ingest_names(db, name_matches[0], source)
                n_alt_names += 1
            continue
        elif len(name_matches) > 1 and search_db:  # Multiple source matches in the database
            n_multiples += 1
            msg1 = f"{i} Skipping {source} "
            msg = f"{i} More than one match for {source}\n {name_matches}\n"
            logger.warning(msg1 + msg)
            if raise_error:
                raise SimpleError(msg)
            else:
                continue
        elif len(name_matches) == 0 or not search_db:  # No match in the database, INGEST!
            if coords:  # Coordinates were provided as input
                ra = ras[i]
                dec = decs[i]
                epoch = None if ma.is_masked(epochs[i]) else epochs[i]
                equinox = None if ma.is_masked(equinoxes[i]) else equinoxes[i]
            else:  # Try to get coordinates from SIMBAD
                simbad_result_table = Simbad.query_object(source)
                if simbad_result_table is None:
                    n_skipped += 1
                    ra = None
                    dec = None
                    msg = f"{i}: Skipping: {source}. Coordinates are needed and could not be retrieved from SIMBAD. \n"
                    logger.warning(msg)
                    if raise_error:
                        raise SimpleError(msg)
                    else:
                        continue
                elif len(simbad_result_table) == 1:
                    simbad_coords = simbad_result_table['RA'][0] + ' ' + simbad_result_table['DEC'][0]
                    simbad_skycoord = SkyCoord(simbad_coords, unit=(u.hourangle, u.deg))
                    ra = simbad_skycoord.to_string(style='decimal').split()[0]
                    dec = simbad_skycoord.to_string(style='decimal').split()[1]
                    epoch = '2000'  # Default coordinates from SIMBAD are epoch 2000.
                    equinox = 'J2000'  # Default frame from SIMBAD is IRCS and J2000.
                    msg = f"Coordinates retrieved from SIMBAD {ra}, {dec}"
                    logger.debug(msg)
                else:
                    n_skipped += 1
                    ra = None
                    dec = None
                    msg = f"{i}: Skipping: {source}. Coordinates are needed and could not be retrieved from SIMBAD. \n"
                    logger.warning(msg)
                    if raise_error:
                        raise SimpleError(msg)
                    else:
                        continue

            logger.debug(f"{i}: Ingesting {source}. Not already in database. ")
        else:
            msg = f"{i}: unexpected condition encountered ingesting {source}"
            logger.error(msg)
            raise SimpleError(msg)

        # Construct data to be added
        source_data = [{'source': source,
                        'ra': ra,
                        'dec': dec,
                        'reference': references[i],
                        'epoch': epoch,
                        'equinox': equinox,
                        'other_references': other_references[i],
                        'comments': None if ma.is_masked(comments[i]) else comments[i]}]
        names_data = [{'source': source,
                       'other_name': source}]

        # Try to add the source to the database
        try:
            with db.engine.connect() as conn:
                conn.execute(db.Sources.insert().values(source_data))
                conn.commit()
            n_added += 1
            msg = f"Added {str(source_data)}"
            logger.debug(msg)
        except sqlalchemy.exc.IntegrityError:
            if ma.is_masked(source_data[0]['reference']):  # check if reference is blank
                msg = f"{i}: Skipping: {source}. Discovery reference is blank. \n"
                msg2 = f"\n {str(source_data)}\n"
                logger.warning(msg)
                logger.debug(msg2)
                n_skipped += 1
                if raise_error:
                    raise SimpleError(msg + msg2)
                else:
                    continue
            elif db.query(db.Publications).filter(db.Publications.c.publication == references[i]).count() == 0:
                # check if reference is in Publications table
                msg = f"{i}: Skipping: {source}. Discovery reference {references[i]} is not in Publications table. \n" \
                      f"(Add it with add_publication function.) \n "
                msg2 = f"\n {str(source_data)}\n"
                logger.warning(msg)
                logger.debug(msg2)
                n_skipped += 1
                if raise_error:
                    raise SimpleError(msg + msg2)
                else:
                    continue
            else:
                msg = f"{i}: Skipping: {source}. Not sure why."
                msg2 = f"\n {str(source_data)} "
                logger.warning(msg)
                logger.debug(msg2)
                n_skipped += 1
                if raise_error:
                    raise SimpleError(msg + msg2)
                else:
                    continue

        # Try to add the source name to the Names table
        try:
            ingest_names(db, source, source)
            n_names += 1
        except sqlalchemy.exc.IntegrityError:
            msg = f"{i}: Could not add {names_data} to database"
            logger.warning(msg)
            if raise_error:
                raise SimpleError(msg)
            else:
                continue

    if n_sources > 1:
        logger.info(f"Sources added to database: {n_added}")
        logger.info(f"Names added to database: {n_names} \n")
        logger.info(f"Sources already in database: {n_existing}")
        logger.info(f"Alt Names added to database: {n_alt_names}")
        logger.info(f"Sources NOT added to database because multiple matches: {n_multiples}")
        logger.info(f"Sources NOT added to database: {n_skipped} \n")

    if n_added != n_names:
        msg = f"Number added should equal names added."
        raise SimpleError(msg)

    if n_added + n_existing + n_multiples + n_skipped != n_sources:
        msg = f"Number added + Number skipped doesn't add up to total sources"
        raise SimpleError(msg)

    return

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

def ingest_spectra(db, sources, spectra, regimes, telescopes, instruments, modes, obs_dates, references,original_spectra=None,
                   wavelength_units=None, flux_units=None, wavelength_order=None,
                   comments=None, other_references=None, raise_error=True):
    """

    Parameters
    ----------
    db: astrodbkit2.astrodb.Database
    sources: list[str]
        List of source names
    spectra: list[str]
        List of filenames corresponding to spectra files
    regimes: str or list[str]
        List or string
    telescopes: str or list[str]
        List or string
    instruments: str or list[str]
        List or string
    modes: str or list[str]
        List or string
    obs_dates: str or datetime
        List of strings or datetime objects
    references: list[str]
        List or string
    original_spectra: list[str]
        List of filenames corresponding to original spectra files
    wavelength_units: str or list[str] or Quantity, optional
        List or string
    flux_units: str or list[str] or Quantity, optional
        List or string
    wavelength_order: list[int], optional
    comments: list[str], optional
        List of strings
    other_references: list[str], optional
        List of strings
    raise_error: bool

    """

    # Convert single value input values to lists
    if isinstance(sources, str):
        sources = [sources]

    if isinstance(spectra, str):
        spectra = [spectra]

    input_values = [regimes, telescopes, instruments, modes, obs_dates, wavelength_order, wavelength_units, flux_units,
                    references,comments, other_references]
    for i, input_value in enumerate(input_values):
        if isinstance(input_value, str):
            input_values[i] = [input_value] * len(sources)
        elif isinstance(input_value, type(None)):
            input_values[i] = [None] * len(sources)
    regimes, telescopes, instruments, modes, obs_dates, wavelength_order, wavelength_units, flux_units, \
    references, comments, other_references = input_values

    n_spectra = len(spectra)
    n_skipped = 0
    n_dupes = 0
    n_missing_instrument = 0
    n_added = 0
    n_blank = 0

    msg = f'Trying to add {n_spectra} spectra'
    logger.info(msg)

    for i, source in enumerate(sources):
        # TODO: check that spectrum can be read by astrodbkit

        # Get source name as it appears in the database
        db_name = find_source_in_db(db, source)

        if len(db_name) != 1:
            msg = f"No unique source match for {source} in the database"
            raise SimpleError(msg)
        else:
            db_name = db_name[0]

        # Check if spectrum file is accessible
        # First check for internet
        internet = check_internet_connection()
        if internet:
            request_response = requests.head(spectra[i])
            status_code = request_response.status_code  # The website is up if the status code is 200
            if status_code != 200:
                n_skipped += 1
                msg = "The spectrum location does not appear to be valid: \n" \
                      f'spectrum: {spectra[i]} \n' \
                      f'status code: {status_code}'
                logger.error(msg)
                if raise_error:
                    raise SimpleError(msg)
                else:
                    continue
            else:
                msg = f"The spectrum location appears up: {spectra[i]}"
                logger.debug(msg)
            if original_spectra:
                request_response1 = requests.head(original_spectra[i])
                status_code1 = request_response1.status_code
                if status_code1 != 200:
                    n_skipped += 1
                    msg = "The spectrum location does not appear to be valid: \n" \
                          f'spectrum: {original_spectra[i]} \n' \
                          f'status code: {status_code1}'
                    logger.error(msg)
                    if raise_error:
                        raise SimpleError(msg)
                    else:
                        continue
                else:
                    msg = f"The spectrum location appears up: {original_spectra[i]}"
                    logger.debug(msg)
        else:
            msg = "No internet connection. Internet is needed to check spectrum files."
            raise SimpleError(msg)

        # Find what spectra already exists in database for this source
        source_spec_data = db.query(db.Spectra).filter(db.Spectra.c.source == db_name).table()

        # SKIP if observation date is blank
        # TODO: try to populate obs date from meta data in spectrum file
        if ma.is_masked(obs_dates[i]) or obs_dates[i] == '':
            obs_date = None
            missing_obs_msg = f"Skipping spectrum with missing observation date: {source} \n"
            missing_row_spe = f"{source, obs_dates[i], references[i]} \n"
            logger.info(missing_obs_msg)
            logger.debug(missing_row_spe)
            n_blank += 1
            continue
        else:
            try:
                obs_date = pd.to_datetime(obs_dates[i])  # TODO: Another method that doesn't require pandas?
            except ValueError:
                n_skipped += 1
                if raise_error:
                    msg = f"{source}: Can't convert obs date to Date Time object: {obs_dates[i]}"
                    logger.error(msg)
                    raise SimpleError
            except dateutil.parser._parser.ParserError:
                n_skipped += 1
                if raise_error:
                    msg = f"{source}: Can't convert obs date to Date Time object: {obs_dates[i]}"
                    logger.error(msg)
                    raise SimpleError
                else:
                    msg = f"Skipping {source} Can't convert obs date to Date Time object: {obs_dates[i]}"
                    logger.warning(msg)
                continue

        # TODO: make it possible to ingest units and order
        row_data = [{'source': db_name,
                     'spectrum': spectra[i],
                     'original_spectrum': None,  # if ma.is_masked(original_spectra[i]) or isinstance(original_spectra,None)
                                               # else original_spectra[i],
                     'local_spectrum': None,  # if ma.is_masked(local_spectra[i]) else local_spectra[i],
                     'regime': regimes[i],
                     'telescope': telescopes[i],
                     'instrument': None if ma.is_masked(instruments[i]) else instruments[i],
                     'mode': None if ma.is_masked(modes[i]) else modes[i],
                     'observation_date': obs_date,
                     'wavelength_units': None if ma.is_masked(wavelength_units[i]) else wavelength_units[i],
                     'flux_units': None if ma.is_masked(flux_units[i]) else flux_units[i],
                     'wavelength_order': None if ma.is_masked(wavelength_order[i]) else wavelength_order[i],
                     'comments': None if ma.is_masked(comments[i]) else comments[i],
                     'reference': references[i],
                     'other_references': None if ma.is_masked(other_references[i]) else other_references[i]}]
        logger.debug(row_data)

        try:
            with db.engine.connect() as conn:
                conn.execute(db.Spectra.insert().values(row_data))
                conn.commit()
            n_added += 1
        except sqlalchemy.exc.IntegrityError as e:

            if "CHECK constraint failed: regime" in str(e):
                msg = f"Regime provided is not in schema: {regimes[i]}"
                logger.error(msg)
                if raise_error:
                    raise SimpleError(msg)
                else:
                    continue
            if db.query(db.Publications).filter(db.Publications.c.publication == references[i]).count() == 0:
                msg = f"Spectrum for {source} could not be added to the database because the reference {references[i]} is not in Publications table. \n" \
                      f"(Add it with ingest_publication function.) \n "
                logger.warning(msg)
                if raise_error:
                    raise SimpleError(msg)
                else:
                    continue
                # check telescope, instrument, mode exists
            telescope = db.query(db.Telescopes).filter(db.Telescopes.c.name == row_data[0]['telescope']).table()
            instrument = db.query(db.Instruments).filter(db.Instruments.c.name == row_data[0]['instrument']).table()
            mode = db.query(db.Modes).filter(db.Modes.c.name == row_data[0]['mode']).table()

            if len(source_spec_data) > 0:  # Spectra data already exists
                # check for duplicate measurement
                ref_dupe_ind = source_spec_data['reference'] == references[i]
                date_dupe_ind = source_spec_data['observation_date'] == obs_date
                instrument_dupe_ind = source_spec_data['instrument'] == instruments[i]
                mode_dupe_ind = source_spec_data['mode'] == modes[i]
                if sum(ref_dupe_ind) and sum(date_dupe_ind) and sum(instrument_dupe_ind) and sum(mode_dupe_ind):
                    msg = f"Skipping suspected duplicate measurement\n{source}\n"
                    msg2 = f"{source_spec_data[ref_dupe_ind]['source', 'instrument', 'mode', 'observation_date', 'reference']}"
                    msg3 = f"{instruments[i], modes[i], obs_date, references[i], spectra[i]} \n"
                    logger.warning(msg)
                    logger.debug(msg2 + msg3 + str(e))
                    n_dupes += 1
                    if raise_error:
                        raise SimpleError
                    else:
                        continue  # Skip duplicate measurement
                # else:
                #     msg = f'Spectrum could not be added to the database (other data exist): \n ' \
                #           f"{source, instruments[i], modes[i], obs_date, references[i], spectra[i]} \n"
                #     msg2 = f"Existing Data: \n "
                #            # f"{source_spec_data[ref_dupe_ind]['source', 'instrument', 'mode', 'observation_date', 'reference', 'spectrum']}"
                #     msg3 = f"Data not able to add: \n {row_data} \n "
                #     logger.warning(msg + msg2)
                #     source_spec_data[ref_dupe_ind][
                #               'source', 'instrument', 'mode', 'observation_date', 'reference', 'spectrum'].pprint_all()
                #     logger.debug(msg3)
                #     n_skipped += 1
                #     continue
            if len(instrument) == 0 or len(mode) == 0 or len(telescope) == 0:
                msg = f'Spectrum for {source} could not be added to the database. \n' \
                      f' Telescope, Instrument, and/or Mode need to be added to the appropriate table. \n' \
                      f" Trying to find telescope: {row_data[0]['telescope']}, instrument: {row_data[0]['instrument']}, " \
                      f" mode: {row_data[0]['mode']} \n" \
                      f" Telescope: {telescope}, Instrument: {instrument}, Mode: {mode} \n"
                logger.error(msg)
                n_missing_instrument += 1
                if raise_error:
                    raise SimpleError
                else:
                    continue
            else:
                msg = f'Spectrum for {source} could not be added to the database for unknown reason: \n {row_data} \n '
                logger.error(msg)
                raise SimpleError(msg)

    msg = f"SPECTRA ADDED: {n_added} \n" \
          f" Spectra with blank obs_date: {n_blank} \n" \
          f" Suspected duplicates skipped: {n_dupes}\n" \
          f" Missing Telescope/Instrument/Mode: {n_missing_instrument} \n" \
          f" Spectra skipped for unknown reason: {n_skipped} \n"
    if n_spectra == 1:
        logger.info(f"Added {source} : \n"
                    f"{row_data}")
    else:
        logger.info(msg)


    if n_added + n_dupes + n_blank + n_skipped + n_missing_instrument != n_spectra:
        msg = "Numbers don't add up: "
        logger.error(msg)
        raise SimpleError(msg)

    spec_count = db.query(Spectra.regime, func.count(Spectra.regime)).group_by(Spectra.regime).all()

    spec_ref_count = db.query(Spectra.reference, func.count(Spectra.reference)). \
        group_by(Spectra.reference).order_by(func.count(Spectra.reference).desc()).limit(20).all()

    telescope_spec_count = db.query(Spectra.telescope, func.count(Spectra.telescope)). \
        group_by(Spectra.telescope).order_by(func.count(Spectra.telescope).desc()).limit(20).all()

    # logger.info(f'Spectra in the database: \n {spec_count} \n {spec_ref_count} \n {telescope_spec_count}')

    return