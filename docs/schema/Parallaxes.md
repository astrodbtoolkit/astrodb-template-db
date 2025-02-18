## Parallaxes
### Description
Parallaxes for Sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 100 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| parallax_mas | double |  | mas | Parallax value for this entry | pos.parallax | True |
| parallax_error | double |  | mas | Uncertainty of this parallax value | stat.error;pos.parallax | True |
| adopted | boolean |  |  | Flag to indicate if this is the adopted entry |  | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Parallaxes | ['#Parallaxes.source', '#Parallaxes.reference'] | Primary key for Parallaxes table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link Parallaxes source to Sources table | ['#Parallaxes.source'] | ['#Sources.source'] |
| ForeignKey | Link Parallaxes reference to Publications table | ['#Parallaxes.reference'] | ['#Publications.reference'] |

