## RadialVelocities
### Description
Radial Velocities of Sources
### Columns
| Column | Datatype | Length | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- |
| source | string | 50 | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| rv_kms | double |  | Radial velocity value for this entry | spect.dopplerVeloc | True |
| rv_error | double |  | Uncertainty of the radial velocity value | stat.error;spect.dopplerVeloc | True |
| adopted | boolean |  | Flag to indicate if this is the adopted entry | meta.code | True |
| comments | string | 100 | Free-form comments for this entry | meta.note | True |
| reference | string | 30 | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_RadialVelocities | ['#RadialVelocities.source', '#RadialVelocities.reference'] | Primary key for Radial Velocities table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link RadialVelocities source to Sources table | ['#RadialVelocities.source'] | ['#Sources.source'] |
| ForeignKey | Link RadialVelocities reference to Publications table | ['#RadialVelocities.reference'] | ['#Publications.reference'] |
| Check | Validate radial velocity error |  |  |

