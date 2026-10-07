from fastapi import APIRouter,HTTPException
from models import IncomeCreate,IncomeUpdate
from repository.income_respository import (
    get_all_income,get_income,create_income,update_income,delete_income
)

router = APIRouter(
    prefix="/api/income",tags=["Income Deatils"]
)

# get all
@router.get("/")
def get_incomes():
    return get_all_income()


# get one income by id
@router.get("/{income_id}")
def get_income_by_id(income_id:int):
    income = get_income(income_id)

    if income is None:
        raise HTTPException(status_code=404,detail="Income not found")

    return income


# insert
@router.post("/")
def create_new_income(income :IncomeCreate):
    try:
        income_id = create_income(income)
        return {
            "message" : "Income created successfully",
            "income_id":income_id
        }

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


# update
@router.put("/{income_id}")
def update_existing_income(income_id:int , income :IncomeUpdate):
    updated_id = update_income (income_id , income)
    if updated_id is None :
        raise HTTPException (status_code=404 , detail= "Income Not Found")

    return {
        "message" : "Income updated successfully",
        "income_id" :updated_id
    }

# delete
@router.delete("/{income_id}")
def delete_existing_income(income_id:int):
    deleted_id = delete_income(income_id)
    if deleted_id is None:
        raise HTTPException(status_code=404,detail="Income not found")


    return {
        "message" :"Income deleted successfully",
        "income_id":deleted_id
    }
