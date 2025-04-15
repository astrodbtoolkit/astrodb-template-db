# RadialVelocities
Radial Velocities of Sources


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| :exclamation:**source** | Main identifier for an object; links to Sources table | string | 50 |  | meta.id;meta.main  |
| rv_kms | Radial velocity value for this entry | double |  | km/s | spect.dopplerVeloc  |
| rv_error | Uncertainty of the radial velocity value | double |  | km/s | stat.error;spect.dopplerVeloc  |
| adopted | Flag to indicate if this is the adopted entry | boolean |  |  | meta.code  |
| comments | Free-form comments for this entry | string | 100 |  | meta.note  |
| :exclamation:**reference** | Publication reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_RadialVelocities | ['#RadialVelocities.source', '#RadialVelocities.reference'] | Primary key for Radial Velocities table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link RadialVelocities source to Sources table | ['#RadialVelocities.source'] | ['#Sources.source'] |
| Link RadialVelocities reference to Publications table | ['#RadialVelocities.reference'] | ['#Publications.reference'] |
## Checks
| Description | Expression |
| --- | --- |
| Validate radial velocity error | rv_error >= 0 |
