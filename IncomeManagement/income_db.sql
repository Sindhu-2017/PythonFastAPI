CREATE TABLE income (
    income_id SERIAL PRIMARY KEY,

    income_date DATE NOT NULL,

    source VARCHAR(100) NOT NULL,

    income_type VARCHAR(50) NOT NULL,

    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),

    tax_percentage NUMERIC(5,2) NOT NULL DEFAULT 0
        CHECK (tax_percentage >= 0 AND tax_percentage <= 100),

    tax_amount NUMERIC(12,2) NOT NULL DEFAULT 0,

    expense_amount NUMERIC(12,2) NOT NULL DEFAULT 0
        CHECK (expense_amount >= 0),

    net_income NUMERIC(12,2) NOT NULL DEFAULT 0,

    cash_in_hand NUMERIC(12,2) NOT NULL DEFAULT 0,

    description TEXT
);