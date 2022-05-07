## Background

The primary input of Dora CLP SaaS is the cargo data file (CSV format) uploaded by the user. Quite often, the cargo data has invalid or missing information. Hence, our SaaS must check the uploaded CSV content, and let the user know of data issues.




## Task Description

Implement a `CargoDataSource` class:


```python
class CargoDataSource:

	def load(self, input_file_path):
		...

	def export(self, output_file_path):
		...

	# Then, methods to allow operations between sources, or
	# any other methods you consider necessary  
	# ...
```

which is able to do these:

#### Load Cargoes

Given a path of the cargo data's CSV file (see `cargo.csv`), read, validate and transform its content. If the content is invalid, return a `dict` object telling why.

Validation rules are

- **Weight** value must be greater than 10. Unit is optional but "kg" is the only allowed unit.
- **Dimensions** are separated by "\*" character. Unit is required and "cm" and "mm" are the only two allowed units, but they can't be used together (so 1cm\*2cm\*3mm is invalid). Each dimension value must be greater than 0.
- **Destination** is optional.
- **Index** must be unique.

Transformation should:

- Create 4 new fields "**length**", "**width**", "**height**" and "**dim_unit**", using cargo's "dimensions" value.
- Drop the "dimensions" field



#### Export Cargoes

Given a destination path, exports the validated and transformed cargo data content as JSON (see `validated-cargo.json`).



#### Diff another cargo source

*Note: this is a bonus feature*.

Given another `CargoDataSource` instance, return the cargoes that are NOT in the other source. 



Example

```python
print(source_1.data)
"""
[
    {"weight": 20, "length": 1, "width": 2, "height": 3,
     "dim_unit": "cm", "destination": "SZ", "index": 1},

    {"weight": 10, "length": 4, "width": 2, "height": 1,
     "dim_unit": "cm", "destination": "SZ", "index": 2}
    ]
"""
print(source_2.data)
"""
[
    {"weight": 20, "length": 1, "width": 2, "height": 3,
     "dim_unit": "cm", "destination": "SZ", "index": 1},

    {"weight": 15, "length": 8, "width": 4, "height": 2,
     "dim_unit": "mm", "destination": "HZ", "index": 2}
    ]
"""
difference = source_1.diff(source_2)
print(difference)
"""
[
    {"weight": 10, "length": 4, "width": 2, "height": 1,
     "dim_unit": "cm", "destination": "SZ", "index": 2}
]
"""

```





