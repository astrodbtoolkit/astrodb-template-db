# Morphology
The Morphology table contains morphological measurements for sources listed in the Sources table. The combination of *source* and *reference* is expected to be unique.


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Unique identifier for a source; links to Sources table | string | 50 |  | meta.id;meta.main  |
| position_angle_deg | Position angle of the source | double |  | deg | pos.posAng  |
| position_angle_error | Uncertainty of the position angle | double |  | deg | stat.error;pos.posAng  |
| position_angle_error_upper | Upper uncertainty of the position angle | double |  | deg | stat.error;pos.posAng  |
| position_angle_error_lower | Lower uncertainty of the position angle | double |  | deg | stat.error;pos.posAng  |
| ellipticity | Ellipticity of the source (0-1) | double |  |  | phys.size.axisRatio  |
| ellipticity_error | Uncertainty of the ellipticity | double |  |  | stat.error;phys.size.axisRatio  |
| ellipticity_error_upper | Upper uncertainty of the ellipticity | double |  |  | stat.error;phys.size.axisRatio  |
| ellipticity_error_lower | Lower uncertainty of the ellipticity | double |  |  | stat.error;phys.size.axisRatio  |
| half_light_radius_arcmin | Half-light radius of the source | double |  | arcmin | phys.size  |
| half_light_radius_error | Uncertainty of the half-light radius | double |  | arcmin | stat.error;phys.size  |
| half_light_radius_error_upper | Upper uncertainty of the half-light radius | double |  | arcmin | stat.error;phys.size  |
| half_light_radius_error_lower | Lower uncertainty of the half-light radius | double |  | arcmin | stat.error;phys.size  |
| adopted | Flag to indicate if this is the adopted entry | boolean |  |  | meta.code  |
| comments | Free form comments | string | 100 |  | meta.note  |
| ❗️ <ins>reference</ins> | Reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Morphology | ['#Morphology.source', '#Morphology.reference'] | Primary key for Morphology table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Morphology source to Sources table | ['#Morphology.source'] | ['#Sources.source'] |
| Link Morphology reference to Publications table | ['#Morphology.reference'] | ['#Publications.reference'] |
## Checks
| Description | Expression |
| --- | --- |
| Validate ellipticity range | ellipticity >= 0 AND ellipticity <= 1 |
