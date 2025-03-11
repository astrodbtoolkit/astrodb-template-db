## Associations
### Description
Association Membership for Sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 50 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| association | string | 100 |  | Association name; links to Associations table | meta.id | False |
| membership_probability | double |  |  | Probability of membership in this association | stat.probability | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| adopted | boolean |  |  | Flag to indicate if this is the adopted entry |  | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Associations | ['#Associations.source', '#Associations.association'] | Primary key for Associations table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link Associations source to Sources table | ['#Associations.source'] | ['#Sources.source'] |
| ForeignKey | Link Associations association to AssociationList table | ['#Associations.association'] | ['#AssociationList.association'] |
| ForeignKey | Link Associations reference to Publications table | ['#Associations.reference'] | ['#Publications.reference'] |
| Check | Validate membership probability |  |  |

