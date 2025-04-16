# Sources
The Sources table contains all objects in the database alongside their coordinates. This is considered the 'primary' table in the database, as each source is expected to be unique and is referred to by all other object tables.


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| :exclamation:<u>source</u> | Unique identifier for the source | string | 50 |  | meta.id;src;meta.main  |
| ra_deg | Right Ascension the source, ICRS recommended | double |  | deg | pos.eq.ra;meta.main  |
| dec_deg | Declination of the source, ICRS recommended | double |  | deg | pos.eq.dec;meta.main  |
| epoch_year | Decimal year for coordinates (e.g., 2015.5) | double |  | yr |   |
| equinox | Equinox reference frame year (e.g., J2000). Not needed if using IRCS coordinates. | string | 10 |  |   |
| :exclamation:reference | Discovery reference for the source; links to Publications table | string | 30 |  | meta.ref;meta.main  |
| other_references | Additional references, comma-separated | string | 50 |  | meta.ref  |
| comments | Free form comments | string | 100 |  | meta.note  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Sources_source | ['#Sources.source'] | Primary key for Sources table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Source reference to Publications table | ['#Sources.reference'] | ['#Publications.reference'] |
## Checks
| Description | Expression |
| --- | --- |
| Validate RA range | ra_deg >= 0 AND ra_deg <= 360 |
| Validate Dec range | dec_deg >= -90 AND dec_deg <= 90 |
