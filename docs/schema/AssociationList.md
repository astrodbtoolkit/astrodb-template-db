# AssociationList
Associations lookup table


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| :exclamation:<ins>association</ins> | Main identifier for an association | string | 100 |  | meta.id;meta.main  |
| association_type | Type of association | string | 30 |  |   |
| comments | Free-form comments for this entry | string | 100 |  | meta.note  |
| reference | Publication reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_AssociationList | ['#AssociationList.association'] | Primary key for AssociationList table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link AssociationList reference to Publications table | ['#AssociationList.reference'] | ['#Publications.reference'] |
