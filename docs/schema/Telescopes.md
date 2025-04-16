# Telescopes
The Telescopes table contains names and references for telescopes referred to in other tables. The *telescope* column is required to be unique.


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>telescope</ins> | Short name for telescope, mission, or survey | string | 30 |  | instr.tel;instr.obsty  |
| description | Telescope description | string | 100 |  | meta.note  |
| reference | Publication reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Telescopes | ['#Telescopes.telescope'] | Primary key for Telescopes table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Telescopes reference to Publications table | ['#Telescopes.reference'] | ['#Publications.reference'] |
