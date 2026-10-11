from database import get_connection

from repositories.expense_attachment_repository import get_attachments_by_expense


async def insert_expense(income_id: int, expense: dict):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "SELECT income_id FROM income WHERE income_id = %s FOR UPDATE",
                (income_id,)
            )

            if await cursor.fetchone() is None:
                return None

            await cursor.execute("""
                INSERT INTO expense (
                    income_id, expense_name, amount, description
                )
                VALUES (%s, %s, %s, %s)
                RETURNING expense_id
            """, (
                income_id,
                expense["expense_name"],
                expense["amount"],
                expense.get("description")
            ))

            row = await cursor.fetchone()

            await recalculate_income(cursor, income_id)

            await connection.commit()
            return row[0]

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()


async def recalculate_income(cursor, income_id: int):
    await cursor.execute("""
        SELECT
            amount,
            tax_percentage,
            COALESCE(
                (SELECT SUM(e.amount)
                 FROM expense e
                 WHERE e.income_id = income.income_id),
                0
            ) AS total_expenses
        FROM income
        WHERE income_id = %s
    """, (income_id,))

    row = await cursor.fetchone()

    if row is None:
        return

    amount, tax_percentage, total_expenses = row

    tax_amount = amount * tax_percentage / 100
    net_income = amount - tax_amount
    cash_in_hand = net_income - total_expenses

    if cash_in_hand < 0:
        raise ValueError(
            "Total expenses cannot exceed net income"
        )

    await cursor.execute("""
        UPDATE income
        SET expense_amount = %s,
            tax_amount = %s,
            net_income = %s,
            cash_in_hand = %s
        WHERE income_id = %s
    """, (
        total_expenses,
        tax_amount,
        net_income,
        cash_in_hand,
        income_id
    ))



async def get_expenses_by_income(income_id: int):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT expense_id, expense_name, amount, description
                FROM expense
                WHERE income_id = %s
                ORDER BY expense_id
            """, (income_id,))

            rows = await cursor.fetchall()

            columns = [
                "expense_id",
                "expense_name",
                "amount",
                "description"
            ]

            expenses= [
                dict(zip(columns, row))
                for row in rows
            ]

            for expense in expenses:
                expense["attachments"] = await get_attachments_by_expense(
                    expense["expense_id"]
                )

            return expenses

    finally:
        await connection.close()


async def delete_expense(expense_id: int):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT income_id
                FROM expense
                WHERE expense_id = %s
            """, (expense_id,))

            row = await cursor.fetchone()

            if row is None:
                return None

            income_id = row[0]

            await cursor.execute("""
                SELECT income_id
                FROM income
                WHERE income_id = %s
                FOR UPDATE
            """, (income_id,))

            if await cursor.fetchone() is None:
                return None

            await cursor.execute("""
                DELETE FROM expense
                WHERE expense_id = %s
                RETURNING expense_id
            """, (expense_id,))

            deleted = await cursor.fetchone()

            if deleted is None:
                await connection.rollback()
                return None

            await recalculate_income(cursor, income_id)

            await connection.commit()
            return deleted[0]

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()