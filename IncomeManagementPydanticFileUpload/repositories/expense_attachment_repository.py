
from database import get_connection


async def expense_exists(expense_id: int):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                SELECT expense_id
                FROM expense
                WHERE expense_id = %s
                """,
                (expense_id,)
            )

            return await cursor.fetchone() is not None

    finally:
        await connection.close()


async def insert_attachment(
    expense_id: int,
    file_name: str,
    file_path: str
):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO expense_attachments
                    (expense_id, file_name, file_path)
                VALUES (%s, %s, %s)
                RETURNING attachment_id
                """,
                (expense_id, file_name, file_path)
            )

            row = await cursor.fetchone()
            await connection.commit()

            return row[0]

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()