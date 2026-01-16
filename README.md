# AWS Lakehouse Mini Platform

## Overview
A mini data lakehouse platform for financial data processing using AWS services.

## Project Structure
aws-lakehouse-mini-platform/
├── data/
│   ├── raw/                        # Raw CSV files
│   │   ├── customers.csv
│   │   ├── accounts.csv
│   │   └── transactions.csv
│   ├── curated/                    # Processed Parquet files
│   └── generate_finance_data.py    # Data generation script
├── glue_jobs/                      # AWS Glue ETL scripts
├── athena_queries/                 # SQL queries for analysis
├── redshift/                       # Redshift configurations
└── docs/                           # Documentation


## Data Schema

### Customers
- `customer_id`: Unique customer identifier (C0000 format)
- `state`: US state code (CA, TX, NY, etc.)
- `credit_score`: Credit score (500-800 range)
- `signup_date`: Customer signup date

### Accounts
- `account_id`: Unique account identifier (A0000 format)
- `customer_id`: Foreign key to customers
- `account_type`: Checking, Savings, Credit Card, or Loan
- `balance`: Current account balance

### Transactions
- `transaction_id`: Unique UUID for each transaction
- `account_id`: Foreign key to accounts
- `transaction_type`: Deposit, Withdrawal, Payment, or Transfer
- `amount`: Transaction amount (always positive)
- `transaction_ts`: Transaction timestamp
- `merchant_category`: Groceries, Utilities, Entertainment, Dining, Travel, Healthcare, or Education

## Curated Layer Rules

The curated layer applies finance-grade data quality and transformations:

### Transformations
- **Format**: Convert CSV → Parquet
- **Deduplication**: Deduplicate by `transaction_id`
- **Timestamp parsing**: Parse `transaction_ts` as proper timestamp type

### Enrichment
- **Date partition**: Add `dt = date(transaction_ts)` for efficient querying
- **Signed amounts**: Add `amount_signed` field based on `transaction_type`:
  - Withdrawal/Payment: negative (-)
  - Deposit/Transfer: positive (+)

### Partitioning
- Partition by `dt` (date) for optimized query performance

### Validation Rules
- **No null account_id**: All transactions must have a valid account
- **Amount > 0**: Transaction amounts must be positive (sign determined by transaction_type)

This ensures data quality and finance-grade standards in the curated layer.

## Setup

1. Create conda environment:
```bash
conda create -p .\env python=3.11
conda activate .\env
```

2. Install dependencies:
```bash
conda install pandas numpy
pip install faker
```

3. Generate sample data:
```bash
python data/generate_finance_data.py
```


## Finance Analytics Use Cases

The curated layer of this lakehouse is designed to support the following
finance-focused analytics and data quality use cases.

### 1. Daily Transaction Volume
- Total number of transactions per day
- Total debit vs credit amounts per day
- Used to monitor transaction trends and system load

Example questions:
- How many transactions occurred each day?
- Are there spikes or drops in activity?

---

### 2. Daily Net Balance Change
- Net balance impact per day derived from transactions
- Debit transactions treated as negative amounts
- Credit transactions treated as positive amounts

Example questions:
- What is the net cash flow per day?
- Which days had unusually high outflows?

---

### 3. High-Spend Customers
- Identify customers with the highest total transaction amounts
- Aggregated over a configurable time window (daily / monthly)

Example questions:
- Who are the top spenders?
- Which customers exceed normal spending thresholds?

---

### 4. Transactions by Merchant Category
- Breakdown of transaction amounts and counts by merchant category
- Used for spending behavior and category-level analysis

Example questions:
- Which merchant categories drive the most spend?
- How does spending vary by category over time?

---

### 5. Data Quality Checks
- Count of bad or invalid records, including:
  - Null account_id or customer_id
  - Duplicate transaction_id
  - Negative or zero transaction amounts
- Used to validate data before loading into analytics or warehouse layers

Example questions:
- How many bad records were detected per day?
- Are data quality issues increasing over time?