from decimal import Decimal
from database import get_connection

def calculate_income(amount, tax_percentage, expense_amount):
    tax_amount = (amount * tax_percentage) / Decimal("100")
    net_income = amount - tax_amount
    cash_in_hand = net_income - expense_amount
    return (tax_amount,net_income,cash_in_hand)


def create_income(income):
    tax_amount, net_income, cash_in_hand = calculate_income(income.amount,income.tax_percentage,income.expense_amount)

    query = """
        INSERT INTO income (income_date,source,income_type,amount,tax_percentage,tax_amount,expense_amount,net_income,cash_in_hand,description)
        VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
        RETURNING
            income_id,
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
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    income.income_date,
                    income.source,
                    income.income_type,
                    income.amount,
                    income.tax_percentage,
                    tax_amount,
                    income.expense_amount,
                    net_income,
                    cash_in_hand,
                    income.description
                )
            )

            result = cursor.fetchone()

            connection.commit()

            return result


def get_all_income():

    query = """
        SELECT
            income_id,
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
        FROM income
        ORDER BY income_id
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchall()


def get_income_by_id(income_id):

    query = """
        SELECT
            income_id,
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
        FROM income
        WHERE income_id = %s
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query, (income_id,))

            return cursor.fetchone()


def update_income(income_id, income):

    tax_amount, net_income, cash_in_hand = calculate_income(
        income.amount,
        income.tax_percentage,
        income.expense_amount
    )

    query = """
        UPDATE income
        SET
            income_date = %s,
            source = %s,
            income_type = %s,
            amount = %s,
            tax_percentage = %s,
            tax_amount = %s,
            expense_amount = %s,
            net_income = %s,
            cash_in_hand = %s,
            description = %s
        WHERE income_id = %s

        RETURNING
            income_id,
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
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    income.income_date,
                    income.source,
                    income.income_type,
                    income.amount,
                    income.tax_percentage,
                    tax_amount,
                    income.expense_amount,
                    net_income,
                    cash_in_hand,
                    income.description,
                    income_id
                )
            )

            result = cursor.fetchone()

            connection.commit()

            return result


def delete_income(income_id):

    query = """
        DELETE FROM income
        WHERE income_id = %s
        RETURNING income_id
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query, (income_id,))

            result = cursor.fetchone()

            connection.commit()

            return result


def get_income_summary():

    query = """
        SELECT
            COALESCE(SUM(amount), 0),
            COALESCE(SUM(tax_amount), 0),
            COALESCE(SUM(expense_amount), 0),
            COALESCE(SUM(net_income), 0),
            COALESCE(SUM(cash_in_hand), 0)
        FROM income
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchone()