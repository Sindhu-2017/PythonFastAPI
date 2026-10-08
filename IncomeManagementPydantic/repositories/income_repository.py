from database import get_connection

# getting all income
async def get_all_income():
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT 
                    income_id , 
                    income_date , 
                    source , 
                    income_type , 
                    amount,
                    tax_percentage ,
                    tax_amount , 
                    expense_amount , 
                    net_income ,
                    cash_in_hand , 
                    description
                FROM income
                ORDER BY income_id
            """)

            rows = await cursor.fetchall()

            return rows
    finally:
        await connection.close()


# get income by id
async def get_income_by_id(income_id : int):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT 
                    income_id , 
                    income_date , 
                    source , 
                    income_type , 
                    amount,
                    tax_percentage ,
                    tax_amount , 
                    expense_amount , 
                    net_income ,
                    cash_in_hand , 
                    description
                FROM income
                WHERE income_id = %s;
            """,(income_id,))

            row = await cursor.fetchone()

            return row

    finally:
        await connection.close()

# create income data
async def insert_income (income_data : dict):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO income 
                (
                    income_date , 
                    source , 
                    income_type , 
                    amount , 
                    tax_percentage ,
                    tax_amount ,
                    expense_amount,
                    net_income , 
                    cash_in_hand , 
                    description
                )
                VALUES 
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING income_id;
            """,(
                income_data["income_date"],
                income_data["source"],
                income_data["income_type"],
                income_data["amount"],
                income_data["tax_percentage"],
                income_data["tax_amount"],
                income_data["expense_amount"],
                income_data["net_income"],
                income_data["cash_in_hand"],
                income_data["description"]
            ))

            row = await cursor.fetchone()
            await connection.commit()
            return row

    except Exception:
        await connection.rollback()
        raise
    finally:
        connection.close()


# update income
async def update_income(income_id:int,income_data:dict):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
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
                RETURNING income_id;
            """,(
                income_data["income_date"],
                income_data["source"],
                income_data["income_type"],
                income_data["amount"],
                income_data["tax_percentage"],
                income_data["tax_amount"],
                income_data["expense_amount"],
                income_data["net_income"],
                income_data["cash_in_hand"],
                income_data["description"],
                income_id
            ))
            row = await cursor.fetchone()
            if row is None:
                await connection.rollback()
                return None
            await connection.commit()
            return row

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()


# delete income data
async def delete_income(income_id:int):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                DELETE FROM income WHERE income_id = %s
                RETURNING income_id;
            """,(income_id,))

            row = await cursor.fetchone()
            if row is None:
                await connection.rollback()
                return None
            await connection.commit()
            return row[0]

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()
