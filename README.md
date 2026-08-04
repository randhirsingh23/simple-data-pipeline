# Simple Data Pipeline

![CI](https://github.com/randhirsingh23/simple-data-pipeline/actions/workflows/ci.yml/badge.svg)

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

## Run the Pipeline

Run with the default input and output paths:

```bash
python src/pipeline.py
```

Run with custom file paths:

```bash
python src/pipeline.py \
  --input data/raw/customers.csv \
  --output data/processed/customers_test.csv
```

View available command-line options:

```bash
python src/pipeline.py --help
```