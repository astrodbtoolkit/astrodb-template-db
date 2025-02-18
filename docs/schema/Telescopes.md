## Telescopes
### Description
Telescope, mission, and survey information
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| telescope | string | 30 | Telescope, mission, or survey name | meta.id;meta.main | False |
| description | string | 100 | Telescope description | meta.note | True |
| reference | string | 30 | Publication reference; links to Publications table |  | True |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link Telescopes reference to Publications table | ['#Telescopes.reference'] | ['#Publications.reference'] |

