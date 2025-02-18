## CompanionRelationships
### Description
Relationships between sources
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| source | string | 50 | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| companion | string | 50 | External identifier for a companion object. Does not link to Sources table. | meta.id | False |
| relationship | string | 30 | Relationship of the source to the companion, e.g., "parent", "child", "sibling" |  | False |
| projected_separation_arcsec | double |  | Projected separation between the source and companion in arcseconds | pos.angDistance | True |
| projected_separation_error | double |  | Uncertainty of the projected separation in arcseconds | stat.error;pos.angDistance | True |
| comments | string | 100 | Free-form comments for this entry | meta.note | True |
| reference | string | 30 | Publication reference; links to Publications table | meta.ref | False |
| other_companion_names | string | 100 | Additional names for the companion object, comma delimited. | meta.id | True |

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

