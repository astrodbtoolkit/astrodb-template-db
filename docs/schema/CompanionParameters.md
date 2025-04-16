# CompanionParameters
Parameters for companion objects relevant to sources


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Main identifier for an object; links to Sources table | string | 50 |  | meta.id;meta.main  |
| ❗️ <ins>companion</ins> | Main identifier for a companion object | string | 50 |  | meta.id  |
| ❗️ <ins>parameter</ins> | Parameter name | string | 30 |  | meta.id  |
| value | Value of the parameter | double |  |  |   |
| error | Uncertainty of the parameter value | double |  |  |   |
| unit | Unit of the parameter value. Should be astropy units compatible. | string | 30 |  |   |
| comments | Free-form comments for this entry | string | 100 |  | meta.note  |
| ❗️ reference | Publication reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_CompanionParameters | ['#CompanionParameters.source', '#CompanionParameters.companion', '#CompanionParameters.parameter', '#CompanionParameters.reference'] | Primary key for CompanionParameters table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link CompanionParameters source to Sources table | ['#CompanionParameters.source'] | ['#Sources.source'] |
| Link CompanionParameters companion to CompanionList table | ['#CompanionParameters.companion'] | ['#CompanionList.companion'] |
| Link CompanionParameters reference to Publications table | ['#CompanionParameters.reference'] | ['#Publications.reference'] |
