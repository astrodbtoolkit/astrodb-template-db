## CompanionRelationships
### Description
The CompanionRelationships table contains companions to sources listed in the Sources table. The combination of *source* and *companion_name* is expected to be unique.
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 50 |  | Unique identifier for the source; links to Sources table | meta.id;meta.main | False |
| companion | string | 50 |  | External identifier for a companion object. Does not link to Sources table. | meta.id | False |
| relationship | string | 30 |  | Relationship of the source to the companion, e.g., "parent", "child", "sibling" |  | False |
| projected_separation_arcsec | double |  | arcsec | Projected separation between the source and companion | pos.angDistance | True |
| projected_separation_error | double |  | arcsec | Uncertainty of the projected separation | stat.error;pos.angDistance | True |
| comments | string | 1000 |  | Free form comments | meta.note | True |
| reference | string | 30 |  | Reference; links to Publications table | meta.ref | False |
| other_companion_names | string | 1000 |  | Additional names for the companion object, comma delimited. | meta.id | True |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_CompanionRelationships | ['#CompanionRelationships.source', '#CompanionRelationships.companion'] | Primary key for CompanionRelationships table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link CompanionRelationships source to Sources table | ['#CompanionRelationships.source'] | ['#Sources.source'] |
| ForeignKey | Link CompanionRelationships companion to CompanionList table | ['#CompanionRelationships.companion'] | ['#CompanionList.companion'] |
| ForeignKey | Link CompanionRelationships reference to Publications table | ['#CompanionRelationships.reference'] | ['#Publications.reference'] |

