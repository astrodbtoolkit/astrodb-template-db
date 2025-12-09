# Positions
The Positions table contains the positions of sources in the Sources table. The combination of *source* and *reference* is expected to be unique.


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Unique identifier for a source; links to Sources table | string | 100 |  | meta.id;meta.main  |
| ra_deg | Right Ascension the source, ICRS recommended | double |  | deg | pos.eq.ra;meta.main  |
| dec_deg | Declination of the source, ICRS recommended | double |  | deg | pos.eq.dec;meta.main  |
| epoch_year | Decimal year for coordinates (e.g., 2015.5) | double |  | yr |   |
| ❗️ <ins>reference</ins> | Reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Positions_source | ['#Positions.source', '#Positions.reference'] | Primary key for Positions table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Positions reference to Publications table | ['#Positions.reference'] | ['#Publications.reference'] |
## Checks
| Description | Expression |
| --- | --- |
| Validate RA range | ra_deg >= 0 AND ra_deg <= 360 |
| Validate Dec range | dec_deg >= -90 AND dec_deg <= 90 |
