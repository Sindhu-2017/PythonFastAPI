-- CREATE TABLE income (
--     income_id SERIAL PRIMARY KEY,
--     income_date DATE NOT NULL,
--     source VARCHAR(100) NOT NULL,
--     income_type VARCHAR(50) NOT NULL,
--     amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
--     tax_percentage NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (tax_percentage >= 0 AND tax_percentage <= 100),
--     tax_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
--     expense_amount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (expense_amount >= 0),
--     net_income NUMERIC(12,2) NOT NULL DEFAULT 0,
--     cash_in_hand NUMERIC(12,2) NOT NULL DEFAULT 0,
--     description TEXT
-- );

INSERT INTO income (
    income_date,
    source,
    income_type,
    amount,
    tax_percentage,
    tax_amount,
    expense_amount,
    net_income,
    cash_in_hand,
    description
)
VALUES (
    '2026-10-07',
    'Freelance',
    'Project',
    50000,
    10,
    5000,
    5000,
    45000,
    40000,
    'Website development project'
);