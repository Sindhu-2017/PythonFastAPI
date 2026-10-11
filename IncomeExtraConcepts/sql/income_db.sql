


DROP TABLE IF EXISTS expense_attachments CASCADE;
DROP TABLE IF EXISTS expense CASCADE;
DROP TABLE IF EXISTS income CASCADE;


CREATE TABLE income (
    income_id SERIAL PRIMARY KEY,
    income_date DATE NOT NULL,
    source VARCHAR(100) NOT NULL,
    income_type VARCHAR(50) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    tax_percentage NUMERIC(5,2) NOT NULL DEFAULT 0,
    tax_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    expense_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    net_income NUMERIC(12,2) NOT NULL,
    cash_in_hand NUMERIC(12,2) NOT NULL,
    description TEXT
);



CREATE TABLE expense (
    expense_id SERIAL PRIMARY KEY,
    income_id INTEGER NOT NULL,
    expense_name VARCHAR(100) NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    description TEXT,

    CONSTRAINT fk_expense_income
        FOREIGN KEY (income_id)
        REFERENCES income(income_id)
        ON DELETE CASCADE
);



CREATE TABLE expense_attachments (
    attachment_id SERIAL PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,

    CONSTRAINT expense_attachments_expense_id_fkey
        FOREIGN KEY (expense_id)
        REFERENCES expense(expense_id)
        ON DELETE CASCADE
);



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
VALUES
(
    '2026-10-04', 'Investment', 'Dividend',
    30000, 5, 1500, 3000, 28500, 25500,
    'Dividend income'
),
(
    '2026-10-05', 'Part Time Job', 'Hourly',
    22000, 2, 440, 4000, 21560, 17560,
    'Part time work'
),
(
    '2026-10-06', 'Consulting', 'IT Consulting',
    90000, 12, 10800, 25000, 79200, 54200,
    'IT consulting project'
),
(
    '2026-10-02', 'Freelance', 'Design',
    35000, 8, 2800, 5000, 32200, 27200,
    'Logo design project'
);



INSERT INTO expense (
    income_id,
    expense_name,
    amount,
    description
)
VALUES
(1, 'Travel', 2000, 'Business travel'),
(1, 'Maintenance', 1500, 'Equipment maintenance');



SELECT * FROM income ORDER BY income_id;

SELECT * FROM expense ORDER BY expense_id;

SELECT * FROM expense_attachments ORDER BY attachment_id;
