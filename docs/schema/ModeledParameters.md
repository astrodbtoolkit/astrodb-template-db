## ModeledParameters
### Description
Derived/modeled parameters for sources
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 50 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| parameter | string | 30 |  | Parameter name | meta.id | False |
| value | double |  |  | Value of the parameter |  | True |
| error | double |  |  | Uncertainty of the parameter value |  | True |
| unit | string | 30 |  | Unit of the parameter value. Should be astropy units compatible. |  | True |
| comments | string | 100 |  | Free-form comments for this entry | meta.note | True |
| reference | string | 30 |  | Publication reference; links to Publications table | meta.ref | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_ModeledParameters | ['#ModeledParameters.source', '#ModeledParameters.parameter', '#ModeledParameters.reference'] | Primary key for ModeledParameters table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link ModeledParameters source to Sources table | ['#ModeledParameters.source'] | ['#Sources.source'] |
| ForeignKey | Link ModeledParameters reference to Publications table | ['#ModeledParameters.reference'] | ['#Publications.reference'] |
| ForeignKey | Link ModeledParameters parameter to ParameterList table | ['#ModeledParameters.parameter'] | ['#ParameterList.parameter'] |

