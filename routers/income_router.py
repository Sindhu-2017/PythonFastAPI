from fastapi import APIRouter, HTTPException

from models import (
    IncomeCreate,
    IncomeUpdate,
    IncomeResponse,
    IncomeSummary
)

from crud.income_crud import (
    create_income,
    get_all_income,
    get_income_by_id,
    update_income,
    delete_income,
    get_income_summary
)


router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


def convert_to_response(row):

    return IncomeResponse(
        income_id=row[0],
        income_date=row[1],
        source=row[2],
        income_type=row[3],
        amount=row[4],
        tax_percentage=row[5],
        tax_amount=row[6],
        expense_amount=row[7],
        net_income=row[8],
        cash_in_hand=row[9],
        description=row[10]
    )


@router.post("/", response_model=IncomeResponse)
def add_income(income: IncomeCreate):

    result = create_income(income)

    return convert_to_response(result)


@router.get("/", response_model=list[IncomeResponse])
def read_all_income():

    rows = get_all_income()

    return [
        convert_to_response(row)
        for row in rows
    ]


@router.get("/{income_id}", response_model=IncomeResponse)
def read_income(income_id: int):

    result = get_income_by_id(income_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Income record not found"
        )

    return convert_to_response(result)


@router.put("/{income_id}", response_model=IncomeResponse)
def edit_income(
    income_id: int,
    income: IncomeUpdate
):

    result = update_income(
        income_id,
        income
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Income record not found"
        )

    return convert_to_response(result)


@router.delete("/{income_id}")
def remove_income(income_id: int):

    result = delete_income(income_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Income record not found"
        )

    return {
        "message": "Income deleted successfully",
        "income_id": income_id
    }


@router.get(
    "/summary/total",
    response_model=IncomeSummary
)
def income_summary():

    result = get_income_summary()

    return IncomeSummary(
        total_income=result[0],
        total_tax=result[1],
        total_expenses=result[2],
        total_net_income=result[3],
        total_cash_in_hand=result[4]
    )