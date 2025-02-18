## ProperMotions
### Description
Proper Motions for Sources
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| source | string | 50 | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| pm_ra | double |  | Proper motion in RA*cos(Dec) in mas/yr | pos.pm;pos.eq.ra | True |
| pm_dec | double |  | Proper motion in Dec in mas/yr | pos.pm;pos.eq.dec | True |
| pm_ra_error | double |  | Uncertainty of the proper motion in RA | stat.error;pos.pm;pos.eq.ra | True |
| pm_dec_error | double |  | Uncertainty of the proper motion in Dec | stat.error;pos.pm;pos.eq.dec | True |
| adopted | boolean |  | Flag to indicate if this is the adopted entry |  | True |
| comments | string | 100 | Free-form comments for this entry | meta.note | True |
| reference | string | 30 | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_ProperMotions | ['#ProperMotions.source', '#ProperMotions.reference'] | Primary key for ProperMotions table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link ProperMotions source to Sources table | ['#ProperMotions.source'] | ['#Sources.source'] |
| ForeignKey | Link ProperMotions reference to Publications table | ['#ProperMotions.reference'] | ['#Publications.reference'] |

