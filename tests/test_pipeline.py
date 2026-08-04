from pathlib import Path

import pandas as pd
import pytest

from src.pipeline import (
    extract_data,
    load_data,
    parse_args,
    transform_data,
    validate_config,
    validate_data,
)

TEST_HIGH_VALUE_THRESHOLD = 2000


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
    result = transform_data(customers, TEST_HIGH_VALUE_THRESHOLD)

    # Assert: Verify the expected output
    assert result["customer_id"].tolist() == [102, 101]
    assert result["name"].tolist() == ["Priya", "Rahul"]
    assert result["city"].tolist() == ["Mumbai", "Delhi"]
    assert result["customer_type"].tolist() == ["High Value", "Regular"]


def test_validate_data_rejects_duplicate_customer_ids() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": [101, 101],
            "name": ["Rahul", "Priya"],
            "city": ["Delhi", "Mumbai"],
            "amount": [1200, 2500],
        }
    )

    with pytest.raises(
        ValueError,
        match="customer_id contains duplicate values",
    ):
        validate_data(customers)


def test_validate_data_rejects_non_numeric_amount() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": [101],
            "name": ["Rahul"],
            "city": ["Delhi"],
            "amount": ["abc"],
        }
    )

    with pytest.raises(
        ValueError,
        match="amount contains missing or non-numeric values",
    ):
        validate_data(customers)


def test_validate_data_rejects_missing_customer_id() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": [None],
            "name": ["Rahul"],
            "city": ["Delhi"],
            "amount": [1200],
        }
    )

    with pytest.raises(
        ValueError,
        match="customer_id contains missing values",
    ):
        validate_data(customers)


def test_validate_data_rejects_empty_data() -> None:
    customers = pd.DataFrame(columns=["customer_id", "name", "city", "amount"])

    with pytest.raises(
        ValueError,
        match="Customer data is empty",
    ):
        validate_data(customers)


def test_validate_config_rejects_missing_pipeline_section() -> None:
    config = {}

    with pytest.raises(
        ValueError,
        match=r"Missing \[pipeline\] section",
    ):
        validate_config(config)


def test_validate_config_rejects_missing_threshold() -> None:
    config = {"pipeline": {}}

    with pytest.raises(
        ValueError,
        match="Missing high_value_threshold",
    ):
        validate_config(config)


def test_validate_config_rejects_non_numeric_threshold() -> None:
    config = {
        "pipeline": {
            "high_value_threshold": "two thousand",
        }
    }

    with pytest.raises(
        ValueError,
        match="high_value_threshold must be numeric",
    ):
        validate_config(config)


def test_validate_config_rejects_non_positive_threshold() -> None:
    config = {
        "pipeline": {
            "high_value_threshold": 0,
        }
    }

    with pytest.raises(
        ValueError,
        match="high_value_threshold must be greater than zero",
    ):
        validate_config(config)


def test_validate_config_returns_valid_threshold() -> None:
    config = {
        "pipeline": {
            "high_value_threshold": 2000,
        }
    }

    result = validate_config(config)

    assert result == 2000


def test_parse_args_reads_custom_paths(monkeypatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "pipeline.py",
            "--input",
            "data/raw/customers_august.csv",
            "--output",
            "data/processed/customers_august_cleaned.csv",
        ],
    )

    args = parse_args()

    assert args.input_file == Path("data/raw/customers_august.csv")
    assert args.output_file == Path("data/processed/customers_august_cleaned.csv")


def test_extract_data_rejects_missing_file(tmp_path) -> None:
    missing_file = tmp_path / "not_found.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Input file does not exist",
    ):
        extract_data(missing_file)


def test_extract_data_rejects_directory(tmp_path) -> None:
    with pytest.raises(
        ValueError,
        match="Input path is not a file",
    ):
        extract_data(tmp_path)


def test_load_data_creates_output_directory(tmp_path) -> None:
    customers = pd.DataFrame(
        {
            "customer_id": [101],
            "name": ["Rahul"],
            "city": ["Delhi"],
            "amount": [1200],
        }
    )

    output_file = tmp_path / "reports" / "august" / "customers_cleaned.csv"

    load_data(customers, output_file)

    assert output_file.exists()

    saved_customers = pd.read_csv(output_file)

    pd.testing.assert_frame_equal(
        saved_customers,
        customers,
    )


# Integration test for the entire pipeline
def test_etl_stages_work_together(tmp_path) -> None:
    input_file = tmp_path / "customers.csv"
    output_file = tmp_path / "customers_cleaned.csv"

    input_data = pd.DataFrame(
        {
            "customer_id": [101, 102],
            "name": [" rahul ", "PRIYA"],
            "city": [" delhi ", "MUMBAI"],
            "amount": [1200, 2500],
        }
    )
    input_data.to_csv(input_file, index=False)

    customers = extract_data(input_file)
    validate_data(customers)
    customers = transform_data(customers, TEST_HIGH_VALUE_THRESHOLD)
    load_data(customers, output_file)

    result = pd.read_csv(output_file)

    assert output_file.exists()
    assert result["customer_id"].tolist() == [102, 101]
    assert result["name"].tolist() == ["Priya", "Rahul"]
    assert result["customer_type"].tolist() == ["High Value", "Regular"]
