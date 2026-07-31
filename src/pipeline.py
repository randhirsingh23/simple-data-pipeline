from pathlib import Path

import pandas as pd


# Find the main project directory
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "raw" / "customers.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "customers_cleaned.csv"


def run_pipeline() -> None:
    # Extract: Read raw data
    customers = pd.read_csv(INPUT_FILE)

    # Transform: Clean text columns
    customers["name"] = customers["name"].str.strip().str.title()
    customers["city"] = customers["city"].str.strip().str.title()

    # Transform: Create a new business column
    customers["customer_type"] = customers["amount"].apply(
        lambda amount: "High Value" if amount >= 2000 else "Regular"
    )

    # Transform: Sort customers by amount
    customers = customers.sort_values(
        by="amount",
        ascending=False
    )

    # Load: Save processed data
    customers.to_csv(OUTPUT_FILE, index=False)

    print(f"Pipeline completed successfully.")
    print(f"Output created at: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_pipeline()