import pandas as pd
import numpy as np
import os

# Additional imports
import uuid     # For generating unique IDs
from datetime import datetime, timedelta
import random

# Ensure folders exist (important on fresh systems)
os.makedirs("data/raw", exist_ok=True)

random.seed(42)
np.random.seed(42)

n_customers = 300
n_accounts = 400
n_transactions = 6000

states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
account_types = ['Checking', 'Savings', 'Credit Card', 'Loan']
transaction_types = ['Deposit', 'Withdrawal', 'Payment', 'Transfer']
merchant_categories = ['Groceries', 'Utilities', 'Entertainment', 'Dining', 'Travel', 'Healthcare', 'Education']

# Generate Customers
customers = []
for i in range(n_customers):
    customers.append({
        'customer_id': f"C{i:04d}",
        'state': random.choice(states),
        'credit_score': random.randint(500, 800),
        'signup_date': (datetime(2023,1,1) - timedelta(days=random.randint(1, 365))).date().isoformat()
    })

# Generate Accounts
accounts = []
for i in range(n_accounts):
    accounts.append({
        'account_id': f"A{i:04d}",
        'customer_id': f"C{random.randint(0, n_customers - 1):04d}",
        'account_type': random.choice(account_types),
        'balance': round(np.random.normal(5000, 3000), 2)
    })


# Generate Transactions
transactions = []
base_ts = datetime(2023, 1, 1)
for i in range(n_transactions):
    transactions.append({
        'transaction_id': str(uuid.uuid4()),
        'account_id': f"A{random.randint(0, n_accounts - 1):04d}",
        'transaction_type': random.choice(transaction_types),
        'amount':round(np.random.uniform(5, 500), 2),
        'transaction_ts': (base_ts + timedelta(minutes=random.randint(0, 60*24*30))).isoformat(),
        'merchant_category': random.choice(merchant_categories)
    })

# Convert to DataFrames
os.makedirs('data/raw', exist_ok=True)
pd.DataFrame(customers).to_csv('data/raw/customers.csv', index=False)
pd.DataFrame(accounts).to_csv('data/raw/accounts.csv', index=False)
pd.DataFrame(transactions).to_csv('data/raw/transactions.csv', index=False)

print("Finance Data generation complete. Files saved to 'data/raw' directory.")