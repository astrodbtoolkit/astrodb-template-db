## SourceTypes
### Description
Source Types for Sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 50 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| source_type | string | 30 |  | Source type; links to SourceTypeList table | meta.id | False |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| adopted | boolean |  |  | Flag to indicate if this is the adopted entry | meta.code | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_SourceTypes | ['#SourceTypes.source', '#SourceTypes.source_type'] | Primary key for SourceTypes table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link SourceTypes source to Sources table | ['#SourceTypes.source'] | ['#Sources.source'] |
| ForeignKey | Link SourceTypes source type to SourceTypeList table | ['#SourceTypes.source_type'] | ['#SourceTypeList.source_type'] |
| ForeignKey | Link SourceTypes reference to Publications table | ['#SourceTypes.reference'] | ['#Publications.reference'] |

