from fastapi import HTTPException

from repositories.income_repository import (
    get_all_income,
    get_income_by_id,
    insert_income,
    update_income,
    delete_income,
    patch_income,
    get_all_income_with_expenses
)

from repositories.expense_repository import (
    insert_expense,
    get_expenses_by_income,
    delete_expense,
)

from schemas.income_schema import(
    IncomeCreate,
    IncomeUpdate,
    IncomePatch,
    IncomePagination,
    IncomePaginatedResponse,
    ExpenseCreate
)

from models.income_model import IncomeModel
from dataclasses import asdict

from exceptions.income_exceptions import (
    IncomeNotFoundError,
    InvalidExpenseAmountError
)

# # calculate tax,net income,cash in hand
# def calculate_income(amount, tax_percentage, expense_amount):
#     amount = float(amount)
#     tax_percentage = float(tax_percentage)
#     expense_amount = float(expense_amount)

#     if expense_amount > amount :
#             raise InvalidExpenseAmountError(expense_amount,amount)

#     tax_amount = (amount * tax_percentage) / 100
#     net_income = amount - tax_amount
#     cash_in_hand = net_income - expense_amount

#     return tax_amount, net_income, cash_in_hand


from decimal import Decimal


def calculate_income(amount, tax_percentage, expense_amount):
    amount = Decimal(str(amount))
    tax_percentage = Decimal(str(tax_percentage))
    expense_amount = Decimal(str(expense_amount))

    tax_amount = amount * tax_percentage / 100
    net_income = amount - tax_amount
    cash_in_hand = net_income - expense_amount

    if expense_amount < 0 or cash_in_hand < 0:
        raise ValueError(
            "Total expenses cannot exceed net income"
        )

    return tax_amount, net_income, cash_in_hand


# Get all income records
async def get_incomes(page:int,page_size:int) -> IncomePaginatedResponse:

    offset = (page -1) * page_size
    rows = await get_all_income(
        limit = page_size,
        offset = offset
    )
    total = rows["total"]
    records = rows["records"]


    total_pages = (total + page_size -1) // page_size

    pagination = IncomePagination (
        total_records = total,
        page_size = page_size,
        offset = offset,
        total_pages =total_pages,
        page_number= page,
        has_previous= offset > 0,
        has_next = (offset + len(records)) < total
    )

    return IncomePaginatedResponse(
        records = records,
        pagination= pagination
    )

# Get one income record by ID
async def get_income(income_id: int):
    row = await get_income_by_id(income_id)

    if row is None:
        raise IncomeNotFoundError(income_id)

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

    return dict(zip(columns, row))

# create income data
async def create_income(income:IncomeCreate):
    tax_amount , net_income , cash_in_hand = calculate_income(
        income.amount,
        income.tax_percentage,
        Decimal("0")
    )

    income_model = IncomeModel(
        income_id =0,
        income_date=income.income_date,
        source=income.source,
        income_type=income.income_type,
        amount=income.amount,
        tax_percentage=income.tax_percentage,
        tax_amount=tax_amount,
        expense_amount=0.0,
        net_income=net_income,
        cash_in_hand=cash_in_hand,
        description=income.description
    )

    income_data = {
        "income_date": income_model.income_date,
        "source": income_model.source,
        "income_type": income_model.income_type,
        "amount": income_model.amount,
        "tax_percentage": income_model.tax_percentage,
        "tax_amount": income_model.tax_amount,
        "expense_amount": income_model.expense_amount,
        "net_income": income_model.net_income,
        "cash_in_hand": income_model.cash_in_hand,
        "description": income_model.description
    }


    row = await insert_income(income_data)

    return {
        "message" : "Income data created successfully",
        "income_id":row[0]
    }


# update income

async def update_existing_income(income_id:int , income :IncomeUpdate):
    existing = await get_income_by_id(income_id)
    if existing is None :
        raise IncomeNotFoundError(income_id)
    
    tax_amount , net_income , cash_in_hand = calculate_income(
        income.amount,
        income.tax_percentage,
        income.expense_amount
    )


    expenses = await get_expenses_by_income(income_id)
    total_expenses = sum(
        (Decimal(str(item["amount"])) for item in expenses),
        Decimal("0")
    )

    tax_amount, net_income, cash_in_hand = calculate_income(
        income.amount,
        income.tax_percentage,
        total_expenses
    )

    income_data = income.model_dump()
    income_data["tax_amount"] = tax_amount
    income_data["expense_amount"] = total_expenses
    income_data["net_income"] = net_income
    income_data["cash_in_hand"] = cash_in_hand

    row = await update_income(income_id,income_data)
    return {
        "message" : "Income data updated successfully",
        "income_id":row[0]
    }


# delete
async def delete_existing_income(income_id:int):
    existing = await get_income_by_id(income_id)
    if existing is None :
        raise IncomeNotFoundError(income_id)

    deleted_id = await delete_income(income_id)

    return {
        "message" : "Income data deleted successfully",
        "income_id":deleted_id
    }


# PATCH
async def patch_existing_income(income_id: int,income: IncomePatch):

    existing = await get_income_by_id(income_id)

    if existing is None:
        raise IncomeNotFoundError(income_id)

    data = income.model_dump(exclude_unset=True)

    if not data:
        raise ValueError(
            "At least one field must be provided for PATCH"
        )

    
    current = {
        "income_date": existing[1],
        "source": existing[2],
        "income_type": existing[3],
        "amount": existing[4],
        "tax_percentage": existing[5],
        "expense_amount": existing[7],
        "description": existing[10]
    }

    current.update(data)

    expenses = await get_expenses_by_income(income_id)
    total_expenses = sum(
        (Decimal(str(item["amount"])) for item in expenses),
        Decimal("0")
    )

    tax_amount, net_income, cash_in_hand = calculate_income(
        current["amount"],
        current["tax_percentage"],
        total_expenses
    )

    current["tax_amount"] = tax_amount
    current["expense_amount"] = total_expenses
    current["net_income"] = net_income
    current["cash_in_hand"] = cash_in_hand

    row = await patch_income(income_id, current)

    return {
        "message": "Income data partially updated successfully",
        "income_id": row[0]
    }



async def get_incomes_with_expenses():
    return await get_all_income_with_expenses()


async def create_expense_for_income(
    income_id: int,
    expense: ExpenseCreate
):
    expense_id = await insert_expense(
        income_id,
        expense.model_dump()
    )

    if expense_id is None:
        raise IncomeNotFoundError(income_id)

    return {
        "message": "Expense created successfully",
        "expense_id": expense_id,
        "income_id": income_id
    }


async def get_incomes_with_expenses():
    return await get_all_income_with_expenses()


async def delete_existing_expense(expense_id: int):
    deleted_id = await delete_expense(expense_id)

    if deleted_id is None:
        raise ValueError(
            f"Expense with ID {expense_id} was not found"
        )

    return {
        "message": "Expense deleted successfully",
        "expense_id": deleted_id
    }


