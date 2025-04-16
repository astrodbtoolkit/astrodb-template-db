# PhotometryFilters
Photometry filter information


Columns marked with an exclamation mark ( :exclamation:) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| :exclamation:<u>band</u> | Band name. | string | 30 |  | instr.bandpass;meta.main  |
| ucd | Unified Content Descriptor of the photometry filter | string | 100 |  | meta.ucd  |
| :exclamation:effective_wavelength_angstroms | Effective wavelength of the photometry filter in Angstroms | double |  | Angstrom |   |
| width_angstroms | Width of the ephotometry filter in Angstroms | double |  | Angstrom | instr.bandwidth  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_PhotometryFilters | ['#PhotometryFilters.band'] | Primary key for PhotometryFilters table |

