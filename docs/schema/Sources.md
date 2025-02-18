## Sources
### Description
Main identifiers for objects along with coordinates.
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| source | string | 50 | Unique identifier for an object | meta.id;src;meta.main | False |
| ra_deg | double |  | ICRS Right Ascension of object | pos.eq.ra;meta.main | True |
| dec_deg | double |  | ICRS Declination of object | pos.eq.dec;meta.main | True |
| epoch_year | double |  | Decimal year for coordinates (eg, 2015.5) |  | True |
| equinox | string | 10 | Equinox reference frame year (eg, J2000) |  | True |
| reference | string | 30 | Publication reference; links to Publications table | meta.ref;meta.main | False |
| other_references | string | 50 | Additional references | meta.ref | True |
| comments | string | 100 | Free-form comments on this Source | meta.note | True |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Sources_source | ['#Sources.source'] | Primary key for Sources table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| Check | Validate RA range |  |  |
| Check | Validate Dec range |  |  |
| ForeignKey | Link Source reference to Publications table | ['#Sources.reference'] | ['#Publications.reference'] |

