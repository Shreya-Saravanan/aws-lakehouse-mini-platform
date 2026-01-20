--Analytics + Business Metrics (finance-focused)

--Daily transaction volume

SELECT
  transaction_date,
  COUNT(*) AS txn_count,
  SUM(amount) AS total_amount
FROM transactions
GROUP BY transaction_date
ORDER BY transaction_date;

--Spend by merchant category

select merchant_category,
    count(*) as txn_count,
    round(sum(amount), 2) as total_amount
from finance_curated_db.transactions
group by merchant_category
order by total_amount;

--Account balance distribution

select account_type,
    count(*) as num_accounts,
    avg(balance) as avg_balance
from finance_curated_db.accounts
group by account_type;

--Average Credit score by state

select state,
    round(avg(credit_score), 2) as avg_credit_score
from finance_curated_db.customers
group by state
order by avg_credit_score desc;

--Data quality check

SELECT COUNT(*)
FROM finance_curated_db.transactions t
LEFT JOIN finance_curated_db.accounts a
  ON t.account_id = a.account_id
WHERE a.account_id IS NULL;