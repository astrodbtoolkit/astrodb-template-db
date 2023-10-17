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