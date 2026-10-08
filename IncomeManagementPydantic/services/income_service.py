from fastapi import HTTPException

from repositories.income_repository import (
    get_all_income,
    get_income_by_id,
    insert_income,
    update_income,
    delete_income
)

from schemas.income_schema import(
    IncomeCreate,
    IncomeUpdate
)

from models.income_model import IncomeModel
from dataclasses import asdict

from exceptions.income_exceptions import (
    IncomeNotFoundError,
    InvalidExpenseAmountError
)

# calculate tax,net income,cash in hand
def calculate_income(amount,tax_percentage,expense_amount):

    if expense_amount > amount :
        raise InvalidExpenseAmountError(amount,expense_amount)
    
    tax_amount = (amount * tax_percentage)/100
    net_income = amount - tax_amount
    cash_in_hand = net_income - expense_amount

    return (tax_amount ,net_income,cash_in_hand)

# get all income data
async def get_incomes():
    rows = await get_all_income()
    return rows

# get income by id
async def get_income(income_id :int):
    row = await get_income_by_id (income_id)

    if row is None:
        # raise HTTPException(
        #     status_code= 404,
        #     detail= "Income id not found"
        # )
        raise IncomeNotFoundError(income_id)
    return row

# create income data
async def create_income(income:IncomeCreate):
    tax_amount , net_income , cash_in_hand = calculate_income(
        income.amount,
        income.tax_percentage,
        income.expense_amount
    )

    income_data = income.model_dump()

    income_data["tax_amount"] = tax_amount
    income_data["net_income"] = net_income
    income_data["cash_in_hand"] = cash_in_hand

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

    income_data = income.model_dump()
    income_data["tax_amount"] = tax_amount
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