# Validata

## Goal

The goal of the `validata` package is to make data validation easy. The package allows you to write simple conditional statements which are applied to each row in a data set. This results in a single `True` or `False` outcome for each row. A simple example:

```python
import pandas
from validata.parser import Parser

df = pd.DataFrame({
    "gender": [1, 2, 1, None],
    "height": [182, 172, 278, 176],
})

# Find missing values
ps = Parser("gender not missing")
print(ps.evaluate(df))
# Outputs [True, True, True, False]

# Find (too) extreme values for height
ps = Parser("height between 140:240")
print(ps.evaluate(df))
# Outputs [True, True, False, True]
```

The `Validator` class allows you to provide many of these simple validations in a `DataFrame`. You can simply store them in a file, load the file, and then run all the validations.

For example:

```python
import pandas as pd
from validata.validator import Validator

# Load the validatsion from file
# Note: this file should contain a "name" and "expression" column
validations = pd.read_csv("validations.csv")

# Load the data from file
data = pd.read_csv("data_file.csv")

# Perform all validations on the data
vd = Validator(validations)
result = vd.evaluate(data)

# Prints a DataFrame with a column for each validation
print(result)
```

