## ParameterList
### Description
Parameters lookup table
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| parameter | string | 30 | Main identifier for a parameter | meta.id;meta.main | False |
| description | string | 100 | Description of the parameter | meta.note | True |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_ParameterList | ['#ParameterList.parameter'] | Primary key for ParameterList table |

