## CompanionParameters
### Description
Parameters for companion objects relevant to sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 50 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| companion | string | 50 |  | Main identifier for a companion object | meta.id | False |
| parameter | string | 30 |  | Parameter name | meta.id | False |
| value | double |  |  | Value of the parameter |  | True |
| error | double |  |  | Uncertainty of the parameter value |  | True |
| unit | string | 30 |  | Unit of the parameter value. Should be astropy units compatible. |  | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_CompanionParameters | ['#CompanionParameters.source', '#CompanionParameters.companion', '#CompanionParameters.parameter', '#CompanionParameters.reference'] | Primary key for CompanionParameters table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link CompanionParameters source to Sources table | ['#CompanionParameters.source'] | ['#Sources.source'] |
| ForeignKey | Link CompanionParameters companion to CompanionList table | ['#CompanionParameters.companion'] | ['#CompanionList.companion'] |
| ForeignKey | Link CompanionParameters reference to Publications table | ['#CompanionParameters.reference'] | ['#Publications.reference'] |

