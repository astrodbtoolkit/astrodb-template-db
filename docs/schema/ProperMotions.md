# ProperMotions
The ProperMotions table contains proper motion measurements for sources listed in the Sources table. The combination of *source* and *reference* is expected to be unique.


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Main identifier for an object; links to Sources table | string | 50 |  | meta.id;meta.main  |
| ❗️ pm_ra | Proper motion in RA*cos(Dec) | double |  | mas/yr | pos.pm;pos.eq.ra  |
| pm_ra_error | Uncertainty of the proper motion in RA | double |  | mas/yr | stat.error;pos.pm;pos.eq.ra  |
| ❗️ pm_dec | Proper motion in declination | double |  | mas/yr | pos.pm;pos.eq.dec  |
| pm_dec_error | Uncertainty of the proper motion in Dec | double |  | mas/yr | stat.error;pos.pm;pos.eq.dec  |
| adopted | Flag to indicate if this is the adopted entry | boolean |  |  |   |
| comments | Free form comments | string | 100 |  | meta.note  |
| ❗️ <ins>reference</ins> | Reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_ProperMotions | ['#ProperMotions.source', '#ProperMotions.reference'] | Primary key for ProperMotions table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link ProperMotions source to Sources table | ['#ProperMotions.source'] | ['#Sources.source'] |
| Link ProperMotions reference to Publications table | ['#ProperMotions.reference'] | ['#Publications.reference'] |
