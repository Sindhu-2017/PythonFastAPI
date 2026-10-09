from database import get_connection

# getting all income

async def get_all_income(limit:int,offset:int):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT COUNT(*)
                FROM income
            """)
            total = (await cursor.fetchone())[0]

            await cursor.execute("""
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
                LIMIT %s OFFSET %s
            """,(limit,offset))

            rows = await cursor.fetchall()

            columns = [
                "income_id",
                "income_date",
                "source",
                "income_type",
                "amount",
                "tax_percentage",
                "tax_amount",
                "expense_amount",
                "net_income",
                "cash_in_hand",
                "description",
            ]

            records= [
                dict(zip(columns, row))
                for row in rows
            ]

            return {
                "total" : total,
                "records" : records
            }
        

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
        await connection.close()


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


# patch
async def patch_income(income_id: int, data: dict):

    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                UPDATE income
                SET income_date = %s,
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
                RETURNING income_id
            """, (
                data["income_date"],
                data["source"],
                data["income_type"],
                data["amount"],
                data["tax_percentage"],
                data["tax_amount"],
                data["expense_amount"],
                data["net_income"],
                data["cash_in_hand"],
                data["description"],
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



# get income with expenses

async def get_all_income_with_expenses():
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                SELECT
                    i.income_id,
                    i.income_date,
                    i.source,
                    i.income_type,
                    i.amount,
                    i.tax_percentage,
                    i.tax_amount,
                    i.expense_amount,
                    i.net_income,
                    i.cash_in_hand,
                    i.description,
                    e.expense_id,
                    e.expense_name,
                    e.amount AS individual_expense_amount,
                    e.description AS expense_description
                FROM income AS i
                LEFT JOIN expense AS e
                    ON i.income_id = e.income_id
                ORDER BY i.income_id, e.expense_id
            """)

            rows = await cursor.fetchall()

            columns = [
                "income_id", "income_date", "source",
                "income_type", "amount", "tax_percentage",
                "tax_amount", "expense_amount", "net_income",
                "cash_in_hand", "description", "expense_id",
                "expense_name", "individual_expense_amount",
                "expense_description"
            ]

            income_data = {}

            for row in rows:
                data = dict(zip(columns, row))
                income_id = data["income_id"]

                if income_id not in income_data:
                    income_data[income_id] = {
                        key: data[key] for key in columns[:11]
                    }
                    income_data[income_id]["expenses"] = []

                if data["expense_id"] is not None:
                    income_data[income_id]["expenses"].append({
                        "expense_id": data["expense_id"],
                        "expense_name": data["expense_name"],
                        "amount": data["individual_expense_amount"],
                        "description": data["expense_description"]
                    })

            return list(income_data.values())

    finally:
        await connection.close()