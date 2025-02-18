## PhotometryFilters
### Description
Photometry filter information
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| band | string | 30 |  | Band name. | instr.bandpass;meta.main | False |
| ucd | string | 100 |  | Unified Content Descriptor of the photometry filter |  | True |
| effective_wavelength_angstroms | double |  | Angstrom | Effective wavelength of the photometry filter in Angstroms |  | False |
| width_angstroms | double |  | Angstrom | Width of the ephotometry filter in Angstroms | instr.bandwidth | True |

