from PythonFastAPI.IncomeManagement.database import get_connection
from PythonFastAPI.IncomeManagement.models import IncomeCreate,IncomeUpdate

def get_all_income():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
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
            rows = cursor.fetchall()
            incomes = []
            for row in rows:
                incomes.append({
                    "income_id" : row[0],
                    "income_date" : row[1],
                    "source" : row[2],
                    "income_type": row[3],
                    "amount": row[4],
                    "tax_percentage": row[5],
                    "tax_amount": row[6],
                    "expense_amount": row[7],
                    "net_income": row[8],
                    "cash_in_hand": row[9],
                    "description": row[10]
                })
            return incomes

    finally:
        connection.close()


def get_income(income_id : int):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
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
            row = cursor.fetchone()

            if row is None:
                return None
            
            return {
                "income_id" : row[0],
                "income_date" : row[1],
                "source" : row[2],
                "income_type": row[3],
                "amount": row[4],
                "tax_percentage": row[5],
                "tax_amount": row[6],
                "expense_amount": row[7],
                "net_income": row[8],
                "cash_in_hand": row[9],
                "description": row[10]
            }

    finally:
        connection.close()


# calculate tax,net income,cash in hand
def calculate_income(amount,tax_percentage,expense_amount):
    tax_amount = (amount * tax_percentage)/100
    net_income = amount - tax_amount
    cash_in_hand = net_income - expense_amount

    return (tax_amount ,net_income,cash_in_hand)

# insert
def create_income (income :IncomeCreate):
    connection = get_connection()
    try:
        tax_amount ,net_income ,cash_in_hand = calculate_income(income.amount,income.tax_percentage,income.expense_amount)

        with connection.cursor() as cursor:
            cursor.execute("""
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
            ))
            income_id = cursor.fetchone()[0]
            connection.commit()
            return income_id

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# update
def update_income(income_id :int , income :IncomeUpdate):
    connection = get_connection()
    try :
        tax_amount ,net_income ,cash_in_hand = calculate_income(income.amount,income.tax_percentage,income.expense_amount)
        with connection.cursor() as cursor:
            cursor.execute("""
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
            ))
            row = cursor.fetchone()
            if row is None :
                connection.rollback()
                return None
            connection.commit()
            return row[0]

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

# delete
def delete_income(income_id:int):
    connection = get_connection()
    try :
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM income WHERE income_id = %s
                RETURNING income_id;
            """,(income_id,))
            row =cursor.fetchone()
            if row is None :
                connection.rollback()
                return None
            connection.commit()
            return row[0]

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
