# Simple Data Pipeline

![CI](https://github.com/randhirsingh23/simple-data-pipeline/actions/workflows/ci.yml/badge.svg)

A beginner-friendly Python data engineering project that reads customer data from a CSV file, validates it, transforms it, and writes the processed data to another CSV file.

The project demonstrates professional data engineering practices such as:

- Modular ETL functions
- Data and configuration validation
- Runtime configuration
- Dynamic input and output paths
- Operational logging
- Automated testing
- Code-quality checks
- Continuous integration with GitHub Actions

## Pipeline Flow

```text
CSV Input
    ↓
Extract Data
    ↓
Validate Data
    ↓
Transform Data
    ↓
Load Processed CSV
```

The pipeline performs the following operations:

1. Reads customer data from a CSV file.
2. Validates required columns and data quality.
3. Cleans customer names and cities.
4. Classifies customers as `High Value` or `Regular`.
5. Sorts customers by amount in descending order.
6. Writes the transformed data to a CSV file.
7. Logs the number of rows processed at each stage.

## Project Structure

```text
simple-data-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/
│   │   └── customers.csv
│   └── processed/
├── src/
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── config.toml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Requirements

- Python 3.12
- Git

## Setup

Clone the repository:

```bash
git clone https://github.com/randhirsingh23/simple-data-pipeline.git
cd simple-data-pipeline
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the runtime dependencies:

```bash
python -m pip install -r requirements.txt
```

## Development Setup

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Development dependencies include tools such as:

- `pytest` for automated testing
- `ruff` for Python code-quality checks

## Configuration

The pipeline reads business settings from `config.toml`.

```toml
[pipeline]
high_value_threshold = 2000
```

The `high_value_threshold` setting controls customer classification.

For example:

```text
Amount 2500 → High Value
Amount 1500 → Regular
```

A different configuration file can be supplied at runtime:

```bash
python src/pipeline.py --config config-test.toml
```

The configuration is validated before customer data is processed.

The pipeline rejects configurations where:

- The `[pipeline]` section is missing
- `high_value_threshold` is missing
- The threshold is not numeric
- The threshold is zero or negative

## Run the Pipeline

Run with the default input, output, and configuration paths:

```bash
python src/pipeline.py
```

Default paths:

```text
Input         data/raw/customers.csv
Output        data/processed/customers_cleaned.csv
Configuration config.toml
```

Run with custom input, output, and configuration paths:

```bash
python src/pipeline.py \
  --input data/raw/customers.csv \
  --output data/processed/customers_test.csv \
  --config config.toml
```

View all command-line options:

```bash
python src/pipeline.py --help
```

Available arguments:

```text
--input   Path to the input customer CSV file
--output  Path to the processed output CSV file
--config  Path to the pipeline configuration TOML file
```

## Input Data

Example input:

```csv
customer_id,name,city,amount
101,Rahul,Delhi,1200
102,Priya,Mumbai,2500
103,Aman,Delhi,1800
104,Neha,Bangalore,3200
105,Rohit,Mumbai,1500
```

Required columns:

```text
customer_id
name
city
amount
```

The pipeline validates that:

- The input file exists
- The input path is a file, not a directory
- The CSV is not empty
- All required columns are present
- Customer IDs are not missing
- Customer IDs are unique
- Amount values are numeric

## Output Data

Example output:

```csv
customer_id,name,city,amount,customer_type
104,Neha,Bangalore,3200,High Value
102,Priya,Mumbai,2500,High Value
103,Aman,Delhi,1800,Regular
105,Rohit,Mumbai,1500,Regular
101,Rahul,Delhi,1200,Regular
```

If the output directory does not exist, the pipeline creates it automatically.

Files created under `data/processed/` are excluded from Git.

## Logging

The pipeline logs each important execution stage:

```text
Pipeline started
Loading configuration
Validating configuration
Extracting data
Rows extracted
Validating customer data
Rows validated
Transforming customer data
Rows transformed
Loading processed data
Rows loaded
Pipeline completed successfully
```

Example:

```text
2026-08-05 00:01:16,470 | INFO | Rows extracted: 5
2026-08-05 00:01:16,470 | INFO | Rows validated: 5
2026-08-05 00:01:16,470 | INFO | Rows transformed: 5
2026-08-05 00:01:16,471 | INFO | Rows loaded: 5
```

When the pipeline fails, it logs the error and exits with status code `1`.

## Testing and Code Quality

Run Ruff:

```bash
ruff check .
```

Run all automated tests:

```bash
python -m pytest -v
```

The test suite covers:

- Data validation
- Data transformation
- Configuration validation
- Missing input files
- Invalid input directories
- Automatic output-directory creation
- Command-line arguments
- Custom configuration files
- ETL integration
- Complete pipeline execution

## Continuous Integration

GitHub Actions automatically runs the following checks:

```text
Install development dependencies
Run Ruff
Run automated tests
```

The workflow runs when:

- Code is pushed to the `main` branch
- A pull request targets the `main` branch

A green CI badge at the top of this README means the latest workflow completed successfully.