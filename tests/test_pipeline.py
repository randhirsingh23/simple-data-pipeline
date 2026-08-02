import pandas as pd
import pytest

from src.pipeline import transform_data, validate_data


def test_validate_data_rejects_missing_columns() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": [101],
            "name": ["Rahul"],
            "city": ["Delhi"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns:.*amount",
    ):
        validate_data(customers)


def test_transform_data_cleans_classifies_and_sorts() -> None:
    # Arrange: Create test data
    customers = pd.DataFrame(
        {
            "customer_id": [101, 102],
            "name": [" rahul ", "PRIYA"],
            "city": [" delhi ", "MUMBAI"],
            "amount": [1200, 2500],
        }
    )

    # Act: Run the transformation
    result = transform_data(customers)

    # Assert: Verify the expected output
    assert result["customer_id"].tolist() == [102, 101]
    assert result["name"].tolist() == ["Priya", "Rahul"]
    assert result["city"].tolist() == ["Mumbai", "Delhi"]
    assert result["customer_type"].tolist() == ["High Value", "Regular"]
