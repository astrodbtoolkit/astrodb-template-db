# ModeledParameters
The ModeledParameters table contains a range of derived/inferred parameters for sources listed in the Sources table. The combination of *source*, *parameter*, and *reference* is expected to be unique. Note that *parameter* is linked to the Parameters table. 


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | Unique identifier for the source; links to Sources table | string | 50 |  | meta.id;meta.main  |
| ❗️ <ins>parameter</ins> | Parameter name; links to ParameterList table | string | 30 |  | meta.id  |
| ❗️ value | Value of the parameter | double |  |  | stat.value;meta.modelled  |
| error | Uncertainty of the parameter value | double |  |  | stat.error;meta.modelled  |
| ❗️ unit | Unit of the parameter value. Should be compatible with astropy.units. | string | 30 |  | meta.unit  |
| comments | Free form comments | string | 100 |  | meta.note  |
| ❗️ <ins>reference</ins> | Reference; links to Publications table | string | 30 |  | meta.ref  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_ModeledParameters | ['#ModeledParameters.source', '#ModeledParameters.parameter', '#ModeledParameters.reference'] | Primary key for ModeledParameters table |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link ModeledParameters source to Sources table | ['#ModeledParameters.source'] | ['#Sources.source'] |
| Link ModeledParameters reference to Publications table | ['#ModeledParameters.reference'] | ['#Publications.reference'] |
| Link ModeledParameters parameter to ParameterList table | ['#ModeledParameters.parameter'] | ['#ParameterList.parameter'] |
