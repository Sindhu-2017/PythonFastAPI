from fastapi import (
    APIRouter,
    Path,
    status,
    HTTPException
)

from schemas.income_schema import (
    IncomeCreate,
    IncomeUpdate,
    IncomeResponse,
    IncomePatch
)

from services.income_service import (
    get_income,
    get_incomes,
    create_income,
    update_existing_income,
    delete_existing_income,
    patch_existing_income
)

from exceptions.income_exceptions import (
    IncomeNotFoundError,
    InvalidExpenseAmountError
)

router = APIRouter(
    prefix="/api/income",
    tags=["Income"]
)

@router.get("/")
async def get_all():
    return await get_incomes()

@router.get("/{income_id}",response_model = list[IncomeResponse])
async def get_one(income_id:int = Path(
    ...,
    gt = 0
)):
    try:
        return await get_income(income_id)

    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post("/",response_model=IncomeResponse,status_code=status.HTTP_201_CREATED)
async def create(income:IncomeCreate):
    try:
        return await create_income(income)

    except InvalidExpenseAmountError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.put("/{income_id}",response_model=IncomeResponse)
async def update(
    income_id: int = Path(..., gt=0),
    income: IncomeUpdate = None
):
    try:
        return await update_existing_income(income_id, income)

    except IncomeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
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
async def patch_income(income_id: int, income: IncomePatch):
    return await patch_existing_income(income_id, income)