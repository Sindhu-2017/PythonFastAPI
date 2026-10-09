from fastapi import (
    APIRouter,
    Path,
    Query,
    status,
    HTTPException
)

from schemas.income_schema import (
    IncomeCreate,
    IncomeUpdate,
    IncomeResponse,
    IncomePatch,
    IncomeActionResponse,
    IncomePaginatedResponse,
    IncomeWithExpensesResponse,
    ExpenseCreate
)

from services.income_service import (
    get_income,
    get_incomes,
    create_income,
    update_existing_income,
    delete_existing_income,
    patch_existing_income,
    get_all_income_with_expenses,
    create_expense_for_income,
    get_incomes_with_expenses,
    delete_existing_expense,
)

from exceptions.income_exceptions import (
    IncomeNotFoundError,
    InvalidExpenseAmountError
)

router = APIRouter(
    prefix="/api/income",
    tags=["Income"]
)


@router.get("/",response_model=IncomePaginatedResponse)
async def get_all(
    page : int =Query(1,ge=1),
    page_size : int = Query(3,ge=1,le=5)
):
    return await get_incomes(page ,page_size)

@router.get(
    "/with-expenses",
    response_model=list[IncomeWithExpensesResponse]
)
async def get_income_expenses():
    return await get_all_income_with_expenses()


@router.get("/{income_id}", response_model=IncomeResponse)
async def get_one(
    income_id: int = Path(..., gt=0)
):
    try:
        return await get_income(income_id)

    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/",
    response_model=IncomeActionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(income: IncomeCreate):
    try:
        return await create_income(income)

    except InvalidExpenseAmountError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.put(
    "/{income_id}",
    response_model=IncomeActionResponse,
)
async def update(
    income_id: int = Path(..., gt=0),
    income: IncomeUpdate = None,
):
    try:
        return await update_existing_income(income_id, income)

    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except InvalidExpenseAmountError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    

@router.delete("/{income_id}")
async def delete(income_id:int = Path(...,gt=0)):
    try:
        return await delete_existing_income(income_id)

    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    
@router.patch("/{income_id}")
async def patch_income(
    income_id: int = Path(
        ...,
        gt=0
    ),
    income: IncomePatch = None
):
    try:
        return await patch_existing_income(income_id,income)
    
    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InvalidExpenseAmountError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




@router.get(
    "/with-expenses",
    response_model=list[IncomeWithExpensesResponse]
)
async def get_all_with_expenses():
    return await get_incomes_with_expenses()


@router.post("/{income_id}/expenses", status_code=201)
async def create_expense(
    income_id: int = Path(..., gt=0),
    expense: ExpenseCreate = ...
):
    try:
        return await create_expense_for_income(
            income_id,
            expense
        )
    except IncomeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int = Path(..., gt=0)
):
    try:
        return await delete_existing_expense(expense_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))