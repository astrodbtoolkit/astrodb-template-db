## Versions
### Description
Database version information
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| version | string | 30 | Version identifier | meta.id;meta.main | False |
| start_date | string | 30 | Date when this version started being used |  | True |
| end_date | string | 30 | Release date of this version |  | True |
| description | string | 1000 | Description of changes associated with this version |  | True |

