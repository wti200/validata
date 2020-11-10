# Validata

## Goal

The goal of the `validata` package is to make data validation easy. The package allows you to write simple logical statements which are applied to each row of a data set. This results in a single `True` or `False` outcome for each row.

Validata is intended as a convenience package; it allows users to formulate simple logical statements which are then applied to a data set. Even user without extensive Python knowledge should be able to perform logical validations on a data set.

## Examples

The example below shows some very basic usages of the `validata` package:

```python
import pandas as pd
from validata.parser import Parser

# Create a very simple data set
df = pd.DataFrame({
    "gender": [1, 2, 1, None],
    "height": [182, 172, 278, 176],
})

# Find missing values
ps = Parser("gender not missing")
print(ps.evaluate(df))
# Outputs [True, True, True, False]

# Find (too) extreme values for height
ps = Parser(
    """
    (gender == 1 & height between 140:200) |
    (gender == 2 & height between 160:220)
    """
)
print(ps.evaluate(df))
# Outputs [True, True, False, False]
```

While the `Parser` class allows you to test a single logical expressions on a data set, you probably want to perform many of such validations in one go. This is where the `Validator` class comes in.

With `Validator` class you can provide many validations using a pandas `DataFrame`. You can simply read your validations from file (CSV, Excel, et cetera) and then run them all at the same time. For example:

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
result = vd.validate(data)

# Prints a DataFrame with a column for each validation
print(result)
```

The `Validator` returns a `DataFrame` which again can be stored as a file or even uploaded to a database or dashboard. This interface makes it easy to run data validations even for non-Python users!

## Installation

Installing the `validata` package is simple and works just like any other package. Simply clone the code and install it:

```bash
git clone https://github.com/LFKoning/validata.git
cd validata
python -m pip install .
```

If you want to help develop `validata`, use the `dev` option instead and also install the `pre-commit` hooks:

```bash
python -m pip install -e .[dev]
pre-commit install
```

The `-e` (`--editable`) flag allows you to make code changes to the `validata` package on the fly. Using `pre-commit` is optional, but helps you write clean code (using `black` and `pylint`) before commiting it to the `git` repo.

Linux users can also use the makefile for convenience, to install the package use:

```bash
make install
```

Or for development use:

```bash
make develop
```
