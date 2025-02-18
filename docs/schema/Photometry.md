## Photometry
### Description
Photometry for Sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 100 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| band | string | 30 |  | Photometry band for this measurement; links to PhotometryFilters table |  | True |
| magnitude | double |  | mag | Magnitude value for this entry |  | True |
| magnitude_error | double |  | mag | Uncertainty of this magnitude value |  | True |
| telescope | string | 30 |  | Telescope, mission, or survey name; links to Telescopes table |  | True |
| epoch | double |  | yr | Decimal year |  | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table |  | False |
| regime | string | 30 |  | Regime for this entry; links to Regimes table |  | True |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Photometry | ['#Photometry.source', '#Photometry.band', '#Photometry.reference'] | Primary key for Photometry table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link Photometry source to Sources table | ['#Photometry.source'] | ['#Sources.source'] |
| ForeignKey | Link Photometry band to PhotometryFilters table | ['#Photometry.band'] | ['#PhotometryFilters.band'] |
| ForeignKey | Link Photometry telescope to Telescopes table | ['#Photometry.telescope'] | ['#Telescopes.telescope'] |
| ForeignKey | Link Photometry reference to Publications table | ['#Photometry.reference'] | ['#Publications.reference'] |
| ForeignKey | Link Photometry regime to Regimes table | ['#Photometry.regime'] | ['#Regimes.regime'] |

