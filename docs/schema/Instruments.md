## Instruments
### Description
Instrument information
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| instrument | string | 30 |  | Instrument name | instr;meta.main | False |
| mode | string | 30 |  | Instrument mode |  | False |
| telescope | string | 30 |  | Telescope, mission, or survey name; links to Telescopes table |  | False |
| description | string | 100 |  | Instrument description | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | True |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link Instruments reference to Publications table | ['#Instruments.reference'] | ['#Publications.reference'] |

