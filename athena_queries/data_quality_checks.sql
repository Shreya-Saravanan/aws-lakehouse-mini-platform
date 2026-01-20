--Simple Data Quality checks

--Null Check
select count(*) 
from finance_curated_db.transactions
where amount is null;

--Negative Amount Check
select count(*)
from finance_curated_db.transactions
where amount < 0;

--Orphan records (checking if every transactions had an account_id associated)
select count(*)
from finance_curated_db.transactions t
left join finance_curated_db.accounts a
    on t.account_id = a.account_id
where a.account_id is null;