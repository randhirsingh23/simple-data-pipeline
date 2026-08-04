import logging
import tomllib
from pathlib import Path

import pandas as pd

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "raw" / "customers.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "customers_cleaned.csv"
REQUIRED_COLUMNS = {"customer_id", "name", "city", "amount"}

CONFIG_FILE = BASE_DIR / "config.toml"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def load_config(file_path: Path) -> dict:
    """Read pipeline configuration from a TOML file."""
    logging.info("Loading configuration from: %s", file_path)

    with file_path.open("rb") as config_file:
        return tomllib.load(config_file)


def validate_config(config: dict) -> int | float:
    """Validate configuration and return the high-value threshold."""
    logging.info("Validating pipeline configuration.")

    if "pipeline" not in config:
        raise ValueError("Missing [pipeline] section in config.toml.")

    pipeline_config = config["pipeline"]

    if "high_value_threshold" not in pipeline_config:
        raise ValueError("Missing high_value_threshold in the [pipeline] section.")

    threshold = pipeline_config["high_value_threshold"]

    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
        raise ValueError("high_value_threshold must be numeric.")

    if threshold <= 0:
        raise ValueError("high_value_threshold must be greater than zero.")

    return threshold


def extract_data(file_path: Path) -> pd.DataFrame:
    """Read customer data from a CSV file."""
    logging.info("Extracting data from: %s", file_path)
    return pd.read_csv(file_path)


def validate_data(customers: pd.DataFrame) -> None:
    """Validate that required columns are present."""
    logging.info("Validating customer data.")

    if customers.empty:
        raise ValueError("Customer data is empty.")

    missing_columns = REQUIRED_COLUMNS - set(customers.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if customers["customer_id"].isna().any():
        raise ValueError("customer_id contains missing values.")

    if customers["customer_id"].duplicated().any():
        raise ValueError("customer_id contains duplicate values.")

    numeric_amount = pd.to_numeric(customers["amount"], errors="coerce")

    if numeric_amount.isna().any():
        raise ValueError("amount contains missing or non-numeric values.")


def transform_data(
    customers: pd.DataFrame,
    high_value_threshold: int,
) -> pd.DataFrame:
    """Clean and transform customer data."""
    logging.info("Transforming customer data.")

    customers["name"] = customers["name"].str.strip().str.title()
    customers["city"] = customers["city"].str.strip().str.title()

    customers["customer_type"] = customers["amount"].apply(
        lambda amount: "High Value" if amount >= high_value_threshold else "Regular"
    )

    customers = customers.sort_values(by="amount", ascending=False)

    return customers


def load_data(customers: pd.DataFrame, file_path: Path) -> None:
    """Save processed customer data to a CSV file."""
    logging.info("Loading processed data to: %s", file_path)
    customers.to_csv(file_path, index=False)


def run_pipeline() -> None:
    logging.info("Pipeline started.")

    config = load_config(CONFIG_FILE)
    high_value_threshold = validate_config(config)

    # Extract
    customers = extract_data(INPUT_FILE)

    # Validate
    validate_data(customers)

    # Transform
    customers = transform_data(customers, high_value_threshold)

    # Load
    load_data(customers, OUTPUT_FILE)

    logging.info("Pipeline completed successfully.")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as error:
        logging.error("Pipeline failed: %s", error)
        raise SystemExit(1) from None
