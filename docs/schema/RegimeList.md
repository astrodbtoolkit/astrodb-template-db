# RegimeList
Regime lookup table


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>regime</ins> | Regime identifier string | string | 30 |  | meta.id;meta.main  |
| description | Description of the regime | string | 100 |  | meta.note  |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_RegimeList | ['#RegimeList.regime'] | Primary key for RegimeList table |

