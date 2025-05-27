# Spectra
The Spectra table contains spectral data for sources listed in the Sources table. The combination of *source*, *regime*, *observation_date*, and *reference* is expected to be unique.


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Unique identifier for the source; links to Sources table | string | 50 |  | meta.id;meta.main  |
| access_url | URL to access the spectral data | string | 200 |  | meta.ref.url;meta.file;meta.dataset  |
| original_spectrum | URL for the original spectrum | string | 200 |  | meta.ref.url;meta.file;meta.dataset  |
| local_spectrum | Local file path to the spectrum data | string | 200 |  | meta.dataset;meta.file  |
| ❗️ <ins>regime</ins> | Spectral regime (e.g., optical, IR, radio); links to RegimeList table | string | 30 |  | meta.id  |
| telescope | Telescope, mission, or survey name; links to Telescopes table | string | 30 |  | instr.tel;instr.obsty  |
| ❗️ instrument | Instrument used for the observation; links to Instruments table | string | 30 |  | instr  |
| ❗️ <ins>mode</ins> | Observation mode (e.g., imaging, spectroscopy) | string | 30 |  | instr.setup  |
| observation_date | Date of the observation in ISO format (YYYY-MM-DD) | string | 30 |  | time.epoch  |
| comments | Free form comments | string | 100 |  | meta.note  |
| ❗️ <ins>reference</ins> | Reference; links to Publications table | string | 30 |  | meta.ref  |
| other_references | Additional references for the spectrum, comma delimited. | string | 100 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Spectra | ['#Spectra.source', '#Spectra.regime', '#Spectra.mode', '#Spectra.observation_date', '#Spectra.reference'] | Primary key for Spectra table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Spectra source to Sources table | ['#Spectra.source'] | ['#Sources.source'] |
| Link Spectra regime to RegimeList table | ['#Spectra.regime'] | ['#RegimeList.regime'] |
| Link Spectra telescope to Telescopes table | ['#Spectra.telescope'] | ['#Telescopes.telescope'] |
| Link Spectra instrument to Instruments table | ['#Spectra.instrument', '#Spectra.mode', '#Spectra.telescope'] | ['#Instruments.instrument', '#Instruments.mode', '#Instruments.telescope'] |
| Link Spectra reference to Publications table | ['#Spectra.reference'] | ['#Publications.reference'] |
