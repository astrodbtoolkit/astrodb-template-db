## AssociationList
### Description
Associations lookup table
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| association | string | 100 |  | Main identifier for an association | meta.id;meta.main | False |
| association_type | string | 30 |  | Type of association |  | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | True |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_AssociationList | ['#AssociationList.association'] | Primary key for AssociationList table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link AssociationList reference to Publications table | ['#AssociationList.reference'] | ['#Publications.reference'] |

