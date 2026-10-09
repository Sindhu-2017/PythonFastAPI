
from fastapi import APIRouter, File, UploadFile, Path

from services.expense_attachment_service import (
    upload_expense_file,
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expense Attachments"],
)


@router.post("/{expense_id}/attachments")
async def upload_attachment(
    expense_id: int = Path(..., gt=0),
    file: UploadFile = File(...),
):
    return await upload_expense_file(
        expense_id=expense_id,
        file=file,
    )