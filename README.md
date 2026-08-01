# Simple Data Pipeline

A basic ETL data pipeline built with Python and pandas.

## Pipeline Flow

1. Extract customer data from a CSV file.
2. Clean and transform the data.
3. Classify customers as `High Value` or `Regular`.
4. Sort customers by transaction amount.
5. Save the processed data as a new CSV file.

## Project Structure

```text
simple-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   └── pipeline.py
├── requirements.txt
└── README.md
```
## Development Setup

Install runtime and development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

```bash
ruff check .
```