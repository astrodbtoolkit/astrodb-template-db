def ingest_publication(db, doi: str = None, bibcode: str = None, publication: str = None, description: str = None,
                    ignore_ads: bool = False):
    """
    Adds publication to the database using DOI or ADS Bibcode, including metadata found with ADS.

    In order to auto-populate the fields, An $ADS_TOKEN environment variable must be set.
    See https://ui.adsabs.harvard.edu/user/settings/token

    Parameters
    ----------
    db
        Database object
    doi, bibcode: str
        The DOI or ADS Bibcode of the reference. One of these is required input.
    publication: str, optional
        The publication shortname, otherwise it will be generated [optional]
        Convention is the first four letters of first authors last name and two digit year (e.g., Smit21)
        For last names which are less than four letters, use '_' or first name initial(s). (e.g, Xu__21 or LiYB21)
    description: str, optional
        Description of the paper, typically the title of the papre [optional]
    ignore_ads: bool

    See Also
    --------
    search_publication: Function to find publications in the database

    """

    if not (publication or doi or bibcode):
        logger.error('Publication, DOI, or Bibcode is required input')
        return

    ads.config.token = os.getenv('ADS_TOKEN')

    if not ads.config.token and (not publication and (not doi or not bibcode)):
        logger.error("An ADS_TOKEN environment variable must be set in order to auto-populate the fields.\n"
                     "Without an ADS_TOKEN, name and bibcode or DOI must be set explicity.")
        return

    if ads.config.token and not ignore_ads:
        use_ads = True
    else:
        use_ads = False
    logger.debug(f"Use ADS set to {use_ads}")

    if bibcode:
        if 'arXiv' in bibcode:
            arxiv_id = bibcode
            bibcode = None
        else:
            arxiv_id = None
    else:
        arxiv_id = None

    name_add, bibcode_add, doi_add = '', '', ''
    # Search ADS uing a provided arxiv id
    if arxiv_id and use_ads:
        arxiv_matches = ads.SearchQuery(q=arxiv_id, fl=['id', 'bibcode', 'title', 'first_author', 'year', 'doi'])
        arxiv_matches_list = list(arxiv_matches)
        if len(arxiv_matches_list) != 1:
            logger.error('should only be one matching arxiv id')
            return

        if len(arxiv_matches_list) == 1:
            logger.debug(f"Publication found in ADS using arxiv id: , {arxiv_id}")
            article = arxiv_matches_list[0]
            logger.debug(f"{article.first_author}, {article.year}, {article.bibcode}, {article.title}")
            if not publication:  # generate the name if it was not provided
                name_stub = article.first_author.replace(',', '').replace(' ', '')
                name_add = name_stub[0:4] + article.year[-2:]
            else:
                name_add = publication
            description = article.title[0]
            bibcode_add = article.bibcode
            doi_add = article.doi[0]

    elif arxiv_id:
        name_add = publication
        bibcode_add = arxiv_id
        doi_add = doi

    # Search ADS using a provided DOI
    if doi and use_ads:
        doi_matches = ads.SearchQuery(doi=doi, fl=['id', 'bibcode', 'title', 'first_author', 'year', 'doi'])
        doi_matches_list = list(doi_matches)
        if len(doi_matches_list) != 1:
            logger.error('should only be one matching DOI')
            return

        if len(doi_matches_list) == 1:
            logger.debug(f"Publication found in ADS using DOI: {doi}")
            using = doi
            article = doi_matches_list[0]
            logger.debug(f"{article.first_author}, {article.year}, {article.bibcode}, {article.title}")
            if not publication:  # generate the name if it was not provided
                name_stub = article.first_author.replace(',', '').replace(' ', '')
                name_add = name_stub[0:4] + article.year[-2:]
            else:
                name_add = publication
            description = article.title[0]
            bibcode_add = article.bibcode
            doi_add = article.doi[0]
    elif doi:
        name_add = publication
        bibcode_add = bibcode
        doi_add = doi

    if bibcode and use_ads:
        bibcode_matches = ads.SearchQuery(bibcode=bibcode, fl=['id', 'bibcode', 'title', 'first_author', 'year', 'doi'])
        bibcode_matches_list = list(bibcode_matches)
        if len(bibcode_matches_list) == 0:
            logger.error('not a valid bibcode:' + str(bibcode))
            logger.error('nothing added')
            raise

        elif len(bibcode_matches_list) > 1:
            logger.error('should only be one matching bibcode for:' + str(bibcode))
            logger.error('nothing added')
            raise

        elif len(bibcode_matches_list) == 1:
            logger.debug("Publication found in ADS using bibcode: " + str(bibcode))
            using = str(bibcode)
            article = bibcode_matches_list[0]
            logger.debug(f"{article.first_author}, {article.year}, {article.bibcode}, {article.doi}, {article.title}")
            if not publication:  # generate the name if it was not provided
                name_stub = article.first_author.replace(',', '').replace(' ', '')
                name_add = name_stub[0:4] + article.year[-2:]
            else:
                name_add = publication
            description = article.title[0]
            bibcode_add = article.bibcode
            if article.doi is None:
                doi_add = None
            else:
                doi_add = article.doi[0]
    elif bibcode:
        name_add = publication
        bibcode_add = bibcode
        doi_add = doi

    if publication and not bibcode and not doi:
        name_add = publication
        using = 'user input'

    new_ref = [{'reference': name_add, 'bibcode': bibcode_add, 'doi': doi_add, 'description': description}]

    try:
        with db.engine.connect() as conn:
            conn.execute(db.Publications.insert().values(new_ref))
            conn.commit()
        logger.info(f'Added {name_add} to Publications table using {using}')
    except sqlalchemy.exc.IntegrityError as error:
        msg = f"Not able to add {new_ref} to the database. " \
              f"It's possible that a similar publication already exists in database\n"\
              "Use find_publication function before adding a new record"
        logger.error(msg)
        raise SimpleError(msg + str(error))

    return