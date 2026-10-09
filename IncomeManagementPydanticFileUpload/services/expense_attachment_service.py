
from pathlib import Path
from uuid import uuid4

import aiofiles

from fastapi import HTTPException, UploadFile, status

from repositories.expense_attachment_repository import (
    expense_exists,
    insert_attachment,
)


BASE_UPLOAD_DIR = (
    Path(__file__).resolve().parent.parent
    / "uploads"
    / "expenses"
)

ALLOWED_FILE_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def upload_expense_file(
    expense_id: int,
    file: UploadFile,
):
    # 1. Check the expense exists
    if not await expense_exists(expense_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    # 2. Validate the uploaded file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, JPG and PNG files are allowed",
        )

    # 3. Create a folder for this expense
    expense_directory = BASE_UPLOAD_DIR / str(expense_id)
    expense_directory.mkdir(parents=True, exist_ok=True)

    # 4. Generate a unique filename
    extension = ALLOWED_FILE_TYPES[file.content_type]
    unique_filename = f"{uuid4().hex}{extension}"
    destination = expense_directory / unique_filename

    total_size = 0

    try:
        # 5. Save the file asynchronously in chunks
        async with aiofiles.open(destination, "wb") as output:
            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File size cannot exceed 5 MB",
                    )

                await output.write(chunk)

        # 6. Store a relative path in PostgreSQL
        relative_path = destination.relative_to(
            BASE_UPLOAD_DIR.parent.parent
        ).as_posix()

        attachment_id = await insert_attachment(
            expense_id=expense_id,
            file_name=Path(file.filename or "upload").name,
            file_path=relative_path,
        )

        return {
            "message": "Expense attachment uploaded successfully",
            "attachment_id": attachment_id,
            "expense_id": expense_id,
            "file_path": relative_path,
        }

    except Exception:
        # Remove the file if database insertion or saving fails
        destination.unlink(missing_ok=True)
        raise

    finally:
        await file.close()