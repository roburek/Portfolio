
-- TASK 1
SELECT
    client_id,
    CAST(date_of_birth AS DATE) AS date_of_birth,
    CASE
        WHEN LOWER(TRIM(employment_status)) = 'unemployed' THEN 'unemployed'
        ELSE 'employed'
    END AS employment_status,
    UPPER(TRIM(country)) AS country
FROM client;


-- TASK 2
SELECT
    repayment_id,
    loan_id,
    repayment_date,
    repayment_amount,
    CASE
        WHEN (repayment_channel IS NULL OR repayment_channel = '')
             AND repayment_amount > 4000 THEN 'bank account'
        WHEN (repayment_channel IS NULL OR repayment_channel = '')
             AND repayment_amount < 1000 THEN 'mail'
        ELSE repayment_channel
    END AS repayment_channel
FROM repayment;


-- TASK 3
SELECT
    c.client_id,
    ct.contract_date,
    l.principal_amount,
    l.loan_type
FROM loan l
JOIN client c ON l.client_id = c.client_id
JOIN contract ct ON l.contract_id = ct.contract_id
WHERE c.country = 'USA'
  AND ct.contract_date >= '2022-01-01';


-- TASK 4
SELECT
    l.loan_type,
    c.country,
    AVG(l.interest_rate) AS avg_rate
FROM loan l
JOIN client c 
    ON l.client_id = c.client_id
GROUP BY 
    l.loan_type,
    c.country
ORDER BY 
    l.loan_type,
    c.country;
