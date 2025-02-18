## Names
### Description
Additional identifiers for objects in Sources table
### Columns
| Column | Datatype | Length | Units | Description | UCD | Nullable |
| --- | --- | --- | --- | --- | --- | --- |
| source | string | 100 |  | Main identifier for an object; links to Sources table | meta.id;meta.main | False |
| other_name | string | 100 |  | Alternate identifier for an object | meta.id | False |

### Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Names_source | ['#Names.source', '#Names.other_name'] | Primary key for Names table |

### Constraints
| Type | Description | Columns | Referenced Columns |
| --- | --- | --- | --- |
| ForeignKey | Link Names primary identifer to Sources table | ['#Names.source'] | ['#Sources.source'] |

