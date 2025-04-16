# SourceTypes
The SourceTypes table contains types (e.g., spectral type or galaxy type) for sources listed in the Sources table. Source types are defined in the SourceTypeList table. The combination of *source*, *source_type*, and *reference* is expected to be unique.


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| :exclamation:<u>source</u> | Main identifier for an object; links to Sources table | string | 50 |  | meta.id;meta.main  |
| :exclamation:<u>source_type</u> | Source type; links to SourceTypeList table | string | 30 |  | meta.id  |
| comments | Free form comments | string | 100 |  | meta.note  |
| adopted | Flag to indicate if this is the adopted entry | boolean |  |  | meta.code  |
| :exclamation:<u>reference</u> | Reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_SourceTypes | ['#SourceTypes.source', '#SourceTypes.source_type', '#SourceTypes.reference'] | Primary key for SourceTypes table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link SourceTypes source to Sources table | ['#SourceTypes.source'] | ['#Sources.source'] |
| Link SourceTypes source type to SourceTypeList table | ['#SourceTypes.source_type'] | ['#SourceTypeList.source_type'] |
| Link SourceTypes reference to Publications table | ['#SourceTypes.reference'] | ['#Publications.reference'] |
