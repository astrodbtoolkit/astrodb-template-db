# Associations
Association Membership for Sources


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Main identifier for an object; links to Sources table | string | 50 |  | meta.id;meta.main  |
| ❗️ <ins>association</ins> | Association name; links to Associations table | string | 100 |  | meta.id  |
| membership_probability | Probability of membership in this association | double |  |  | stat.probability  |
| comments | Free-form comments for this entry | string | 100 |  | meta.note  |
| adopted | Flag to indicate if this is the adopted entry | boolean |  |  |   |
| ❗️ reference | Publication reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Associations | ['#Associations.source', '#Associations.association'] | Primary key for Associations table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Associations source to Sources table | ['#Associations.source'] | ['#Sources.source'] |
| Link Associations association to AssociationList table | ['#Associations.association'] | ['#AssociationList.association'] |
| Link Associations reference to Publications table | ['#Associations.reference'] | ['#Publications.reference'] |
## Checks
| Description | Expression |
| --- | --- |
| Validate membership probability | membership_probability >= 0 AND membership_probability <= 1 |
