## RotationalParameters
### Description
Rotational parameters for sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 50 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| period_hr | double |  | hr | Rotational period in hours | time.period | True |
| period_error | double |  | hr | Uncertainty of the rotational period | stat.error;time.period | True |
| v_sin_i_kms | double |  | km/s | Projected rotational velocity in km/s | phys.veloc.rotat | True |
| v_sin_i_error | double |  | km/s | Uncertainty of the projected rotational velocity | stat.error;phys.veloc.rotat | True |
| inclination | double |  | deg | Inclination of the rotation axis in degrees | pos.posAng | True |
| inclination_error | double |  | deg | Uncertainty of the inclination | stat.error;pos.posAng | True |
| adopted | boolean |  |  | Flag to indicate if this is the adopted entry | meta.code | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_RotationalParameters | ['#RotationalParameters.source', '#RotationalParameters.reference'] | Primary key for RotationalParameters table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link RotationalParameters source to Sources table | ['#RotationalParameters.source'] | ['#Sources.source'] |
| ForeignKey | Link RotationalParameters reference to Publications table | ['#RotationalParameters.reference'] | ['#Publications.reference'] |

