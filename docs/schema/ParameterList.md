# ParameterList
Parameters lookup table


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| :exclamation:**parameter** | Main identifier for a parameter | string | 30 |  | meta.id;meta.main  |
| description | Description of the parameter | string | 100 |  | meta.note  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_ParameterList | ['#ParameterList.parameter'] | Primary key for ParameterList table |

