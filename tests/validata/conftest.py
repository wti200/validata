"""Setup file for pytest unit tests."""

import pytest
import numpy as np
import pandas as pd


@pytest.fixture
def dummy_data():
    """Generate some dummy data for use in unit tests."""

    rows = 10

    np.random.seed(42)
    size = (np.random.standard_exponential(rows) + 1).astype(int)

    np.random.seed(42)
    income_1 = (np.random.standard_exponential(rows) * 30e3).astype(int)

    np.random.seed(42)
    income_2 = (np.random.standard_exponential(rows) * 20e3).astype(int)

    return pd.DataFrame(
        {
            "id": np.arange(rows),
            "size": size,
            "income_1": income_1,
            "income_2": income_2,
        }
    )
